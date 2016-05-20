import unittest

from app.fellow import Fellow
from app.livingroom import LivingRoom
from app.room import Room
from app.staff import Staff


class TestLivingRoom(unittest.TestCase):
    def setUp(self):
        self.spata = LivingRoom("spata", "M")
        self.personA = Fellow("Malik Wahab", "M", "1", "Python")
        self.personB = Fellow("Temi Tope", "F", "1", "Ruby")
        self.personC = Staff("Joe Jack", "F", "Engineering")

    def test_room_inheritance(self):
        self.assertTrue(issubclass(LivingRoom, Room))

    def test_init_name(self):
        self.assertEqual("spata", self.spata.get_name())

    def test_init_size(self):
        self.assertEqual(4, self.spata.get_size())

    def test_get_gender(self):
        self.assertEqual("M", self.spata.get_gender())

    def test_allocation(self):
        self.assertEqual(self.spata.add_occupant(self.personA), 1)

    def test_allocation_two(self):
        self.spata.add_occupant(self.personA)
        self.assertIn("malikwahab", self.spata.get_occupants())

    def test_allocation_opposite_sex(self):
        self.assertEqual(self.spata.add_occupant(self.personB), 4)

    def test_allocation_staff(self):
        self.assertEqual(self.spata.add_occupant(self.personC), 5)
