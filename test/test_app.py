import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.
    getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from app.amity import Amity
from app.app import *
from app.roomallocation import RoomAllocation
from app.fellow import Fellow
from app.staff import Staff
from app.office import Office
from app.livingspace import LivingSpace
from io import StringIO

class Capturing(list):

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


class TestApp(unittest.TestCase):

    def setUp(self):
        amity = Amity()
        self.roomallocation = RoomAllocation(amity)
        self.args = {'create_room': False, 'add_person': False,
                     'relocate_person': False, 'print_allocation': False,
                     'print_unallocated': False, 'print_room': False,
                     'load_state': False, 'print_room': False,
                     'save_state': False, 'delete_room': False,
                     'delete_person': False, 'print_persons': False}
        self.args['<room_name>'] = ['Mars', 'Sapele']
        self.args['<room_type>'] = ['office', 'livingspace']
        self.args['--rgender'] = ['M']
        self.args['create_room'] = True
        main(self.args)
        self.args['<first_name>'] = 'Malik'
        self.args['<last_name>'] = 'Wahab'
        self.args['<gender>'] = 'M'
        self.args['<person_type>'] = 'fellow'
        self.args["--wants_accom"] = 'Y'
        self.args['add_person'] = True
        main(self.args)


    def tearDown(self):
        if os.path.isfile('roomallocation.p'):
            os.remove('roomallocation.p')

    def reset_call(self):
        self.args['create_room'] = False
        self.args['add_person'] = False

    def test_load_state(self):
        roomallocation = load_state()
        self.assertTrue(isinstance(roomallocation, RoomAllocation))

    def test_save_state(self):
        save_state(self.roomallocation)
        self.assertTrue(os.path.isfile('roomallocation.p'))

    def test_add_person(self):
        self.args['<first_name>'] = 'Jide'
        self.args['<last_name>'] = 'Olu'
        self.args['<gender>'] = 'M'
        self.args['<person_type>'] = 'fellow'
        self.args["--wants_accom"] = 'Y'
        self.args['add_person'] = True
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Jide allocated to Office mars\n"
        expected_string += "Jide allocated to Living Space sapele\n"
        self.assertEqual(output_string, expected_string)

    def test_add_person_staff(self):
        self.args['<first_name>'] = 'Malik'
        self.args['<last_name>'] = 'Wahab'
        self.args['<gender>'] = 'M'
        self.args['<person_type>'] = 'staff'
        self.args["--wants_accom"] = 'Y'
        self.args['add_person'] = True
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Malik allocated to Office mars\n"
        self.assertEqual(output_string, expected_string)

    def test_add_person_three(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['delete_room'] = True
        self.args['<room_name>'] = ['mars']
        main(self.args)
        self.args['<room_name>'] = ['sapele']
        main(self.args)
        self.args['<first_name>'] = 'Malik'
        self.args['<last_name>'] = 'Wahab'
        self.args['<gender>'] = 'M'
        self.args['<person_type>'] = 'Fellow'
        self.args["--wants_accom"] = 'Y'
        self.args['add_person'] = True
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "No available Office to allocate Malik\n"
        expected_string += "No available Living Space to allocate Malik\n"
        self.assertEqual(output_string, expected_string)

    def test_add_person_invalid(self):
        self.args['<first_name>'] = 'Malik'
        self.args['<last_name>'] = 'Wahab'
        self.args['<gender>'] = 'M'
        self.args['<person_type>'] = 'invalid'
        self.args["--wants_accom"] = 'Y'
        self.args['add_person'] = True
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Invalid type: person can be fellow or staff"
        self.assertEqual(output_string, expected_string)

    def test_create_room(self):
        self.args['<room_name>'] = ['Mecury']
        self.args['<room_type>'] = ['office']
        self.args['--rgender'] = []
        self.args['create_room'] = True
        self.args['add_person'] = False
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Room(s) created with Id (type): \n"
        expected_string += "mecury (office) \n"
        self.assertEqual(output_string, expected_string)

    def test_create_room_exist(self):
        self.args['<room_name>'] = ['Mars']
        self.args['<room_type>'] = ['Office']
        self.args['--rgender'] = ['']
        self.args['create_room'] = True
        self.args['add_person'] = False
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Room(s) created with Id (type): \n"
        expected_string += "[Error] Room with name Mars already exit in Amity"
        self.assertEqual(output_string, expected_string)

    def test_create_room_invalid(self):
        self.args['<room_name>'] = ['Mars']
        self.args['<room_type>'] = ['invalid']
        self.args['--rgender'] = ['']
        self.args['create_room'] = True
        self.args['add_person'] = False
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Room(s) created with Id (type): \n"
        expected_string += "Invalid room type for [Mars invalid]\n"
        self.assertEqual(output_string, expected_string)

    def test_relocate_room(self):
        self.args['<room_name>'] = ['Mecury']
        self.args['<room_type>'] = ['office']
        self.args['--rgender'] = []
        self.args['create_room'] = True
        self.args['add_person'] = False
        main(self.args)
        roomallocation = load_state()
        for i in roomallocation.amity.persons:
            person = roomallocation.amity.persons[i]
        self.args['relocate_person'] = True
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['<person_identifier>'] = person.identifier
        self.args['<new_room_name>'] = 'mecury'
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Person relocated to mecury"
        self.assertEqual(output_string, expected_string)

    def test_relocate_room_two(self):
        self.args['relocate_person'] = True
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['<person_identifier>'] = 'malikwahab'
        self.args['<new_room_name>'] = 'mecury'
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Invalid Id supplied"
        self.assertEqual(output_string, expected_string)

    def test_print_allocation(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['print_allocation'] = True
        self.args['--option'] = ''
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        roomallocation = load_state()
        expected_string = roomallocation.build_allocation_string()
        self.assertEqual(output_string, expected_string)

    def test_print_allocation_file(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['print_allocation'] = True
        self.args['--option'] = 'test/test_print_allocation.txt'
        main(self.args)
        file_created = os.path.isfile('test/test_print_allocation.txt')
        os.remove('test/test_print_allocation.txt')
        self.assertTrue(file_created)

    def test_print_unallocated(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['print_unallocated'] = True
        self.args['--option'] = ''
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        roomallocation = load_state()
        expected_string = roomallocation.build_unallocation_string()
        self.assertEqual(output_string, expected_string)

    def test_print_unallocated_file(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['print_unallocated'] = True
        self.args['--option'] = 'test/test_print_unallocated.txt'
        main(self.args)
        file_created = os.path.isfile('test/test_print_unallocated.txt')
        os.remove('test/test_print_unallocated.txt')
        self.assertTrue(file_created)

    def test_print_room(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['print_room'] = True
        self.args['<room_name>'] = ['mars']
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        roomallocation = load_state()
        expected_string = roomallocation.print_room('mars')
        self.assertEqual(output_string, expected_string)

    def test_print_room_invalid(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['print_room'] = True
        self.args['<room_name>'] = ['invalid']
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Invalid room id supplied"
        self.assertEqual(output_string, expected_string)

    def print_persons(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['print_persons'] = True
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        roomallocation = load_state()
        expected_string = roomallocation.print_persons()
        self.assertEqual(output_string, expected_string)

    def test_delete_person(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['delete_person'] = True
        roomallocation = load_state()
        for i in roomallocation.amity.persons:
            person = roomallocation.amity.persons[i]
        self.args['<person_id>'] = person.identifier
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = person.identifier + " deleted from Amity"
        self.assertEqual(output_string, expected_string)

    def test_delete_person_invalid(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['delete_person'] = True
        self.args['<person_id>'] = 'invalid'
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Invalid Id supplied"
        self.assertEqual(output_string, expected_string)

    def test_delete_room(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['delete_room'] = True
        self.args['<room_name>'] = ['mars']
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "mars deleted from Amity"
        self.assertEqual(output_string, expected_string)

    def test_delete_room_invalid(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['delete_room'] = True
        self.args['<room_name>'] = 'invalid'
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Invalid Id supplied"
        self.assertEqual(output_string, expected_string)

    def test_save_state_db(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['save_state'] = True
        self.args["--db"] = ''
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Data Successfully saved to database"
        self.assertEqual(output_string, expected_string)

    def test_save_state_db_two(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['save_state'] = True
        self.args["--db"] = 'test/roomallocation.db'
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Data Successfully saved to database"
        os.remove('test/roomallocation.db')
        self.assertEqual(output_string, expected_string)

    def test_load_state_db(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        self.args['load_state'] = True
        self.args["<db_path>"] = 'roomallocation.db'
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "Application State reload from database"
        self.assertEqual(output_string, expected_string)

    def test_main_no_args(self):
        self.args['create_room'] = False
        self.args['add_person'] = False
        with Capturing() as output:
            main(self.args)
        output_string = '\n'.join(output)
        expected_string = "use the usage instruction below to build command"
        self.assertEqual(output_string, expected_string)