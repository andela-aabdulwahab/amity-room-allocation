import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect. \
    getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from app.amity import Amity
from app.fellow import Fellow
from app.livingroom import LivingRoom
from app.office import Office
from app.staff import Staff


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.fellowA = Fellow("Malik Wahab", "M", "D1", "Python")
        self.fellowB = Fellow("Ose Oko", "F", "D1", "Ruby")
        self.staffA = Staff("Joe Jack", "M", "Training")
        self.staffB = Staff("Nengi Adoki", "F", "Beliefs")
        self.officeA = Office("Moon")
        self.officeB = Office("Mecury")
        self.livingA = LivingRoom("Spata", "M")
        self.livingB = LivingRoom("Roses", "F")
        self.amity = Amity()
        self.amity.add_room(self.livingB)

    def test_add_room(self):
        self.amity.add_room(self.livingA)
        self.assertIn("spata", self.amity.rooms)

    def test_get_room(self):
        self.assertEqual(self.amity.get_room("roses"), self.livingB)

    def test_get_room_all(self):
        self.amity.add_room(self.livingA)
        room_dict = {'roses': self.livingB, 'spata': self.livingA}
        self.assertEqual(self.amity.get_rooms(), room_dict)

    def test_get_persons(self):
        self.amity.add_person(self.fellowA)
        self.amity.add_person(self.staffA)
        self.amity.add_person(self.fellowB)
        self.amity.add_person(self.staffB)
        self.amity.add_room(self.officeA)
        self.amity.add_room(self.officeB)
        person_dict = {"malikwahab": self.fellowA, "oseoko": self.fellowB, "joejack": self.staffA, "nengiadoki": self.staffB}
        self.assertEqual(person_dict, self.amity.get_persons())

    def test_get_offices(self):
        self.amity.add_room(self.officeA)
        self.amity.add_room(self.officeB)
        self.amity.add_room(self.livingA)
        self.amity.add_room(self.livingB)
        office_dict = {"moon": self.officeA, "mecury": self.officeB}
        self.assertEqual(office_dict, self.amity.get_offices())

    def test_get_livingrooms(self):
        self.amity.add_room(self.officeA)
        self.amity.add_room(self.officeB)
        self.amity.add_room(self.livingA)
        self.amity.add_room(self.livingB)
        living_dict = {"spata": self.livingA}
        self.assertEqual(living_dict, self.amity.get_livingrooms("M"))

    def test_get_all_livingrooms(self):
        self.amity.add_room(self.officeA)
        self.amity.add_room(self.officeB)
        self.amity.add_room(self.livingA)
        self.amity.add_room(self.livingB)
        living_dict = {"spata": self.livingA, "roses": self.livingB}
        self.assertEqual(living_dict, self.amity.get_all_livingrooms())

    def test_add_person(self):
        person = self.fellowA
        self.amity.add_person(person)
        self.assertIn(person.get_id(), self.amity.persons)
