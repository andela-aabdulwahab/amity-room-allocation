import unittest

from app.person import Person
from app.room import Room


class TestRoom(unittest.TestCase):

    def setUp(self):
        self.mars = Room("Mars", 4)
        self.pluto = Room("Pluto", 4)
        self.personA = Person("Malik Wahab", "M")
        self.personB = Person("Jola Ade", "M")
        self.personC = Person("Temi Tope", "F")
        self.personD = Person("Ose Oko", "F")
        self.personE = Person("TJ Peters", "M")

    def test_init_name(self):
        self.assertEqual(self.mars.name, "Mars")

    def test_init_size(self):
        self.assertEqual(self.mars.size, 4)

    def test_get_name(self):
        self.assertEqual(self.mars.name, "Mars")

    def test_occupants_empty(self):
        self.assertEqual(self.mars.occupants, {})

    def test_add_occupant(self):
        self.mars.add_occupant(self.personA)
        self.assertEqual(self.mars.occupants["malikwahab"], self.personA)

    def test_add_occupant_exist(self):
        self.mars.add_occupant(self.personA)
        self.assertEqual(self.mars.add_occupant(self.personA), 3)

    def test_remove_occupant(self):
        self.mars.add_occupant(self.personD)
        self.mars.remove_occupant(self.personD)
        self.assertNotIn("oseoko", self.mars.occupants)

    def test_is_full(self):
        self.pluto.add_occupant(self.personA)
        self.pluto.add_occupant(self.personB)
        self.pluto.add_occupant(self.personC)
        self.pluto.add_occupant(self.personD)
        self.assertTrue(self.pluto.is_full())

    def test_add_occupant_when_full(self):
        self.pluto.add_occupant(self.personA)
        self.pluto.add_occupant(self.personB)
        self.pluto.add_occupant(self.personC)
        self.pluto.add_occupant(self.personD)
        self.assertEqual(self.pluto.add_occupant(self.personE), 2)

    def test_get_id(self):
        self.assertEqual(self.pluto.get_id(), "pluto")
