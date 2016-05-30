import unittest

from app.exceptions import PersonNotFellowError, RoomGenderDiffError
from app.fellow import Fellow
from app.livingspace import LivingSpace
from app.room import Room
from app.staff import Staff


class TestLivingSpace(unittest.TestCase):
    def setUp(self):
        self.spata = LivingSpace("spata", "M")
        self.personA = Fellow("Malik Wahab", "M", "Y")
        self.personB = Fellow("Temi Tope", "F", "N")
        self.personC = Staff("Joe Jack", "F")

    def test_room_inheritance(self):
        self.assertTrue(issubclass(LivingSpace, Room))

    def test_init_name(self):
        self.assertEqual("spata", self.spata.name)

    def test_init_size(self):
        self.assertEqual(4, self.spata.size)

    def test_gender(self):
        self.assertEqual("M", self.spata.gender)

    def test_add_occupants(self):
        with self.assertRaises(PersonNotFellowError):
            self.spata.occupants = self.personC

    def test_add_occupants_two(self):
        with self.assertRaises(RoomGenderDiffError):
            self.spata.occupants = self.personB

    def test_add_occupants_three(self):
        self.spata.occupants = self.personA
        key = self.personA.identifier
        self.assertIn(key, self.spata.occupants)
