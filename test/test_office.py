import unittest

from app.office import Office
from app.room import Room


class TestOffice(unittest.TestCase):

    def setUp(self):
        self.orion = Office("Orion")

    def test_room_inheritance(self):
        self.assertTrue(issubclass(Office, Room))

    def test_init_name(self):
        self.assertEqual("Orion", self.orion.name)

    def test_init_size(self):
        self.assertEqual(6, self.orion.size)
