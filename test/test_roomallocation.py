import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect. \
    getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pprint import pprint
from app.amity import Amity
from app.fellow import Fellow
from app.livingroom import LivingRoom
from app.office import Office
from app.roomallocation import RoomAllocation
from app.staff import Staff
from app.allocation_db import AllocationDb


class TestRoomAllocation(unittest.TestCase):

    def setUp(self):
        amity_obj = Amity()
        self.roomallocation = RoomAllocation(amity_obj)
        self.livingA = LivingRoom("Spata", "M")
        self.officeB = Office("Trafford")
        self.officeA = Office("Mars")
        self.personA = Fellow("Malik Wahab", "M", "Y", "D1", "Python")
        self.personB = Staff("Joe Jack", "M", "Training")
        self.roomallocation.create_room(self.livingA)
        self.roomallocation.create_room(self.officeA)
        self.roomallocation.create_room(self.officeB)
        self.roomallocation.create_person(self.personA)
        self.roomallocation.create_person(self.personB)

    def test_create_room(self):
        self.roomallocation.create_room(self.livingA)
        self.assertIn("spata", self.roomallocation.amity.get_rooms())

    def test_allocate_office(self):
        self.roomallocation.allocate_office(self.personB.get_id())
        self.assertTrue(self.personB.is_allocated("office"))

    def test_allocate_office_two(self):
        self.roomallocation.allocate_office(self.personB.get_id())
        self.assertIn(self.personB.get_allocation("office"), ['mars', 'trafford'])

    def test_allocate_office_three(self):
        self.roomallocation.allocate_office(self.personB.get_id())
        self.assertIn(self.personB.get_allocation("office"), ['mars', 'trafford', 'spata'])

    def test_allocate_livingroom(self):
        self.roomallocation.allocate_livingroom(self.personA.get_id())
        self.assertTrue(self.personA.is_allocated("livingroom"))

    def test_allocate_livingroom_two(self):
        self.roomallocation.allocate_livingroom(self.personA.get_id())
        self.assertIn("malikwahab", self.livingA.get_occupants())

    def test_allocate_livingroom_three(self):
        self.roomallocation.allocate_livingroom(self.personA.get_id())
        self.assertEqual("spata", self.personA.get_allocation("livingroom"))

    def test_rellocate_room(self):
        self.roomallocation.allocate_livingroom(self.personA.get_id())
        self.roomallocation.allocate_office(self.personA.get_id())
        self.roomallocation.rellocate_person(self.personA.get_id(), self.officeB.get_id())
        self.assertEqual("trafford", self.personA.get_allocation("office"))

    def test_remove_person(self):
        person_id = self.personA.get_id()
        self.roomallocation.remove_person(person_id)
        self.assertIsNone(self.roomallocation.amity.get_person(person_id))

    def test_remove_person_two(self):
        person_id = self.personA.get_id()
        room = self.roomallocation.amity.get_room(self.personA.get_allocation("office"))
        self.roomallocation.remove_person(person_id)
        self.assertNotIn(person_id, room.get_occupants())

    def test_remove_room(self):
        room_id = self.livingA.get_id()
        self.roomallocation.remove_room(room_id)
        self.assertIsNone(self.roomallocation.amity.get_room(room_id))

    def test_remove_room_two(self):
        room_id = self.livingA.get_id()
        occupants = self.livingA.get_occupants()
        self.roomallocation.remove_room(room_id)
        for i in occupants:
            occupant = occupants[i]
            self.assertEqual(9, occupant.get_allocation("livingroom"))

    def test_select_random(self):
        aDict = {"one":1, "two":2, "three": 3, "four": 4}
        random = self.roomallocation.select_random(aDict)
        self.assertIn(random, aDict.values())

    def test_allocate_room(self):
        self.roomallocation.allocate_room(self.personA.get_id(), {"spata": self.livingA})
        self.assertIn("malikwahab", self.livingA.get_occupants())

    def test_get_unallocated(self):
        fellow1 = Fellow("Jose Morinho", "M", "Y")
        fellow2 = Fellow("Wayne Rooney", "M", "Y")
        fellow3 = Fellow("Rio Fedinand", "M", "Y")
        fellow4 = Fellow("Micheal Carrick", "M", "Y")
        fellow5 = Fellow("David Degea", "M", "Y")
        fellow6 = Fellow("Steve Maccoy", "M", "Y")
        fellow7 = Fellow("Steve Jobs", "M", "Y")
        self.roomallocation.create_person(fellow1)
        self.roomallocation.create_person(fellow2)
        self.roomallocation.create_person(fellow3)
        self.roomallocation.create_person(fellow4)
        self.roomallocation.create_person(fellow5)
        self.roomallocation.create_person(fellow6)
        self.roomallocation.create_person(fellow7)
        self.assertIn(fellow7, self.roomallocation.get_unallocated()[1].values())

    def test_print_person(self):
        person_string = self.roomallocation.print_person(self.personA)
        expected_string = "MALIK WAHAB FELLOW Y\n"
        self.assertEqual(person_string, expected_string)

    def test_print_person_two(self):
        person_string = self.roomallocation.print_person(self.personB)
        expected_string = "JOE JACK STAFF \n"
        self.assertEqual(person_string, expected_string)

    def test_print_room(self):
        room_string = self.roomallocation.print_room(self.livingA.get_id())
        expected_string = "\n--Spata(Living Room)--\n"
        expected_string += "MALIK WAHAB FELLOW Y\n"
        self.assertEqual(room_string, expected_string)

    def test_build_allocation_string(self):
        allocation_string = self.roomallocation.build_allocation_string()
        rooms = self.roomallocation.amity.get_rooms()
        expected_string = ""
        for room_id in rooms:
            expected_string += self.roomallocation.print_room(room_id)
        self.assertEqual(allocation_string, expected_string)

    def test_build_unallocated_string(self):
        self.roomallocation.remove_room('spata')
        unallocated_string = self.roomallocation.build_unallocation_string()
        expected_string = "  --Unallocated for Office-- \n\n"
        expected_string += "\n \n --Unallocated for LivingRoom-- \n\n"
        expected_string += "MALIK WAHAB FELLOW Y\n"
        self.assertEqual(unallocated_string, expected_string)

    def test_print_allocation_to_file(self):
        self.roomallocation.print_allocation_to_file("test/test_allocation_to_file.txt")
        rooms = self.roomallocation.amity.get_rooms()
        expected_string = ""
        for room_id in rooms:
            expected_string += self.roomallocation.print_room(room_id)
        allocation_string_from_file = ""
        with open("test/test_allocation_to_file.txt", 'r') as allocation_line:
            allocation_string_from_file += allocation_line.read()
        os.remove("test/test_allocation_to_file.txt")
        self.assertEqual(allocation_string_from_file, expected_string)


    def test_print_unallocated_to_file(self):
        self.roomallocation.remove_room('spata')
        self.roomallocation.print_unallocated_to_file('test/test_unallocated_to_file.txt')
        unallocated_string = self.roomallocation.build_unallocation_string()
        expected_string = "  --Unallocated for Office-- \n\n"
        expected_string += "\n \n --Unallocated for LivingRoom-- \n\n"
        expected_string += "MALIK WAHAB FELLOW Y\n"
        with open("test/test_unallocated_to_file.txt", 'r') as allocation_line:
            unallocated_string_from_file = allocation_line.read()
        os.remove('test/test_unallocated_to_file.txt')
        self.assertEqual(expected_string, unallocated_string_from_file)

    def test_save_to_database(self):
        db = AllocationDb('test/test_save.db')
        self.roomallocation.save_to_database(db)
        rooms = db.get_rooms()
        os.remove('test/test_save.db')
        self.assertIn('spata', rooms)

    def test_save_to_database_two(self):
        db = AllocationDb('test/test_save.db')
        self.roomallocation.save_to_database(db)
        persons = db.get_persons()
        os.remove('test/test_save.db')
        self.assertIn('malikwahab', persons)

    def test_load_from_database(self):
        db = AllocationDb('test/test_save.db')
        self.roomallocation.save_to_database(db)
        self.roomallocation.remove_person('malikwahab')
        self.roomallocation.remove_room('spata')
        self.roomallocation.load_from_database(db)
        self.assertIn('malikwahab', self.roomallocation.amity.get_persons())
