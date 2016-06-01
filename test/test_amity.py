import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.
    getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from app.amity import Amity
from app.exceptions import SameNameRoomError
from app.fellow import Fellow
from app.livingspace import LivingSpace
from app.office import Office
from app.staff import Staff


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.fellowA = Fellow("Malik Wahab", "M", "Y")
        self.fellowB = Fellow("Ose Oko", "F", "N")
        self.staffA = Staff("Joe Jack", "M")
        self.staffB = Staff("Nengi Adoki", "F")
        self.officeA = Office("Moon")
        self.officeB = Office("Mecury")
        self.livingA = LivingSpace("Spata", "M")
        self.livingB = LivingSpace("Roses", "F")
        self.amity = Amity()
        self.amity.rooms = self.livingB

    def test_init(self):
        amity = Amity()
        self.assertEqual(amity.rooms, {})

    def test_add_room(self):
        self.amity.rooms = self.livingA
        self.assertIn("spata", self.amity.rooms)

    def test_add_room_two(self):
        with self.assertRaises(TypeError):
            self.amity.rooms = "spata"

    def test_ad_room_two(self):
        with self.assertRaises(SameNameRoomError):
            self.amity.add_room(self.livingB)

    def test_get_rooms(self):
        self.amity.rooms = self.livingA
        room_dict = {'roses': self.livingB, 'spata': self.livingA}
        self.assertEqual(self.amity.rooms, room_dict)

    def test_get_persons_two(self):
        self.amity.persons = self.fellowA
        self.amity.persons = self.staffA
        self.amity.persons = self.fellowB
        self.amity.persons = self.staffB
        self.assertIn(self.staffB.identifier, self.amity.persons)

    def test_get_person(self):
        self.amity.add_person(self.fellowA)
        self.assertEqual(self.amity.persons[self.fellowA.identifier],
                         self.fellowA)

    def test_get_offices(self):
        self.amity.rooms = self.officeA
        self.amity.rooms = self.officeB
        self.amity.rooms = self.livingA
        office_dict = {"moon": self.officeA, "mecury": self.officeB}
        self.assertEqual(office_dict, self.amity.get_offices())

    def test_get_livingspaces(self):
        self.amity.rooms = self.officeA
        self.amity.rooms = self.officeB
        self.amity.rooms = self.livingA
        living_dict = {"spata": self.livingA}
        self.assertEqual(living_dict, self.amity.get_livingspaces("M"))

    def test_get_all_livingspaces(self):
        self.amity.rooms = self.officeA
        self.amity.rooms = self.officeB
        self.amity.rooms = self.livingA
        living_dict = {"spata": self.livingA, "roses": self.livingB}
        self.assertEqual(living_dict, self.amity.get_all_livingspaces())

    def test_add_person(self):
        self.amity.persons = self.fellowA
        self.assertIn(self.fellowA.identifier, self.amity.persons)

    def test_add_person_two(self):
        with self.assertRaises(TypeError):
            self.amity.persons = "malik wahab"

    def test_room_type(self):
        self.assertEqual(self.amity.room_type(self.livingA), 'livingspace')

    def test_room_type_two(self):
        self.assertEqual(self.amity.room_type(self.officeA), 'office')

    def test_room_type_thee(self):
        self.assertIsNone(self.amity.room_type({}))

    def test_person_type(self):
        self.assertEqual(self.amity.person_type(self.fellowA), 'fellow')

    def test_person_type_two(self):
        self.assertEqual(self.amity.person_type(self.staffB), 'staff')

    def test_person_type_three(self):
        self.assertIsNone(self.amity.person_type({}))
