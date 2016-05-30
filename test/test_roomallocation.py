import os
import unittest

from app.allocation_db import AllocationDb
from app.amity import Amity
from app.exceptions import NoRoomError, PersonAllocatedError
from app.fellow import Fellow
from app.livingspace import LivingSpace
from app.office import Office
from app.roomallocation import RoomAllocation
from app.staff import Staff


class TestRoomAllocation(unittest.TestCase):

    def setUp(self):
        amity_obj = Amity()
        self.personA = Fellow("Malik Wahab", "M", "Y")
        self.personB = Staff("Joe Jack", "M")
        amity_obj.persons = self.personA
        amity_obj.persons = self.personB
        self.roomallocation = RoomAllocation(amity_obj)
        self.livingA = LivingSpace("Spata", "M")
        self.officeB = Office("Trafford")
        self.officeA = Office("Mars")
        self.roomallocation.create_room(self.livingA)
        self.roomallocation.create_room(self.officeA)
        self.roomallocation.create_room(self.officeB)

    def test_create_room(self):
        self.roomallocation.create_room(self.livingA)
        self.assertIn("spata", self.roomallocation.amity.rooms)

    def test_create_person(self):
        fellow = Fellow("Jose Morinho", "M", "Y")
        self.roomallocation.create_person(fellow)
        self.assertTrue(fellow.is_allocated("livingspace"))

    def test_creat_person_two(self):
        self.roomallocation.remove_room(self.officeA.get_id())
        self.roomallocation.remove_room(self.officeB.get_id())
        status = self.roomallocation.create_person(self.personB)
        self.assertFalse(status[0])

    def test_create_person_two(self):
        fellow = Fellow("Jose Morinho", "M", "Y")
        self.roomallocation.create_person(fellow)
        self.assertTrue(fellow.is_allocated("office"))

    def test_allocate_office(self):
        self.roomallocation.allocate_office(self.personB.identifier)
        self.assertTrue(self.personB.is_allocated("office"))

    def test_allocate_office_two(self):
        self.roomallocation.allocate_office(self.personB.identifier)
        self.assertIn(self.personB.room_name["office"], ['mars', 'trafford'])

    def test_allocate_livingspace(self):
        self.roomallocation.allocate_livingspace(self.personA.identifier)
        self.assertTrue(self.personA.is_allocated("livingspace"))

    def test_allocate_livingspace_two(self):
        self.roomallocation.allocate_livingspace(self.personA.identifier)
        self.assertIn(self.personA.identifier, self.livingA.occupants)

    def test_allocate_livingspace_three(self):
        self.roomallocation.allocate_livingspace(self.personA.identifier)
        self.assertEqual("spata", self.personA.room_name["livingspace"])

    def test_allocate_livingspace_four(self):
        with self.assertRaises(KeyError):
            self.roomallocation.allocate_livingspace("ahmed")

    def test_allocate_room(self):
        with self.assertRaises(NoRoomError):
            self.roomallocation.allocate_room(self.personA.identifier, {})

    def test_allocate_room_two(self):
        self.roomallocation.allocate_livingspace(self.personA.identifier)
        with self.assertRaises(PersonAllocatedError):
            self.roomallocation.allocate_room(self.personA.identifier,
                                              {'spata': self.livingA})

    def test_rellocate_person(self):
        self.roomallocation.allocate_livingspace(self.personA.identifier)
        self.roomallocation.allocate_office(self.personA.identifier)
        self.roomallocation.rellocate_person(self.personA.identifier,
                                             self.officeB.get_id())
        self.assertEqual("trafford", self.personA.room_name["office"])

    def test_rellocate_person_four(self):
        with self.assertRaises(KeyError):
            self.roomallocation.rellocate_person(self.personA.identifier, 'om')

    def test_rellocate_person_two(self):
        with self.assertRaises(KeyError):
            self.roomallocation.rellocate_person("malik", 'spata')

    def test_remove_person(self):
        person_id = self.personA.identifier
        self.roomallocation.remove_person(person_id)
        self.assertIsNone(self.roomallocation.amity.persons.get(person_id))

    def test_remove_person_two(self):
        person_id = self.personA.identifier
        self.roomallocation.allocate_office(self.personA.identifier)
        self.roomallocation.allocate_livingspace(self.personA.identifier)
        room = self.roomallocation.amity \
            .rooms[self.personA.room_name["office"]]
        self.roomallocation.remove_person(person_id)
        self.assertNotIn(person_id, room.occupants)

    def test_remove_person_three(self):
        with self.assertRaises(KeyError):
            self.roomallocation.remove_person('invalidname')

    def test_remove_room(self):
        room_id = self.livingA.get_id()
        self.roomallocation.remove_room(room_id)
        self.assertIsNone(self.roomallocation.amity.rooms.get(room_id))

    def test_remove_room_two(self):
        room_id = self.livingA.get_id()
        occupants = self.livingA.get_occupants()
        self.roomallocation.remove_room(room_id)
        for i in occupants:
            occupant = occupants[i]
            self.assertEqual(9, occupant.get_allocation("livingspace"))

    def test_remove_room_three(self):
        with self.assertRaises(KeyError):
            self.roomallocation.remove_room('notthere')

    def test_select_random(self):
        a_dict = {"one": 1, "two": 2, "three": 3, "four": 4}
        random = self.roomallocation.select_random(a_dict)
        self.assertIn(random, a_dict.values())

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
        try:
            self.roomallocation.create_person(fellow7)
        except NoRoomError:
            pass
        self.assertIn(fellow7, self.roomallocation.
                      get_unallocated()[1].values())

    def test_get_unallocated_two(self):
        fellow1 = Fellow("Jose Morinho", "M", "Y")
        self.roomallocation.create_person(fellow1)
        office_id = fellow1.room_name.get('office')
        self.roomallocation.remove_room(office_id)
        self.assertIn(fellow1, self.roomallocation.
                      get_unallocated()[0].values())

    def test_print_person(self):
        person_string = self.roomallocation.print_person(self.personA)
        expected_string = "MALIK WAHAB FELLOW Y\n"
        self.assertEqual(person_string, expected_string)

    def test_print_person_two(self):
        person_string = self.roomallocation.print_person(self.personB)
        expected_string = "JOE JACK STAFF \n"
        self.assertEqual(person_string, expected_string)

    def test_print_room(self):
        self.livingA.add_occupant(self.personA)
        room_string = self.roomallocation.print_room(self.livingA.get_id())
        expected_string = "\n--Spata(livingspace)--\n"
        expected_string += "MALIK WAHAB FELLOW Y\n"
        self.assertEqual(room_string, expected_string)

    def test_build_allocation_string(self):
        allocation_string = self.roomallocation.build_allocation_string()
        rooms = self.roomallocation.amity.rooms
        expected_string = ""
        for room_id in rooms:
            expected_string += self.roomallocation.print_room(room_id)
        self.assertEqual(allocation_string, expected_string)

    def test_build_unallocated_string(self):
        self.roomallocation.remove_person(self.personB.identifier)
        unallocated_string = self.roomallocation.build_unallocation_string()
        expected_string = "  --Unallocated for Office-- \n\n"
        expected_string += "MALIK WAHAB FELLOW Y\n"
        expected_string += "\n \n --Unallocated for LivingSpace-- \n\n"
        expected_string += "MALIK WAHAB FELLOW Y\n"
        self.assertEqual(unallocated_string, expected_string)

    def test_print_allocation_to_file(self):
        self.roomallocation.print_allocation_to_file("test/test" +
                                                     "_allocation_to_file.txt")
        rooms = self.roomallocation.amity.rooms
        expected_string = ""
        for room_id in rooms:
            expected_string += self.roomallocation.print_room(room_id)
        allocation_string_from_file = ""
        with open("test/test_allocation_to_file.txt", 'r') as allocation_line:
            allocation_string_from_file += allocation_line.read()
        os.remove("test/test_allocation_to_file.txt")
        self.assertEqual(allocation_string_from_file, expected_string)

    def test_print_unallocated_to_file(self):
        self.roomallocation.remove_person(self.personB.identifier)
        self.roomallocation \
            .print_unallocated_to_file('test/test_unallocated_to_file.txt')
        expected_string = "  --Unallocated for Office-- \n\n"
        expected_string += "MALIK WAHAB FELLOW Y\n"
        expected_string += "\n \n --Unallocated for LivingSpace-- \n\n"
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
        self.assertIn(self.personA.identifier, persons)

    def test_load_from_database(self):
        db = AllocationDb('test/test_save.db')
        fellow = Fellow("Jose Morinho", "M", "Y")
        staff = Staff("Alex Fergie", "M")
        self.roomallocation.create_person(fellow)
        self.roomallocation.create_person(staff)
        self.roomallocation.save_to_database(db)
        del self.roomallocation.amity.persons[self.personA.identifier]
        self.roomallocation.remove_room('spata')
        self.roomallocation.load_from_database(db)
        self.assertIn(self.personA.identifier,
                      self.roomallocation.amity.persons)
