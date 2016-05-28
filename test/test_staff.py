import unittest

from app.person import Person
from app.staff import Staff


class TestStaff(unittest.TestCase):
    def setUp(self):
        self.staff_obj = Staff("Joe Jack", "M", "Engineering")

    def test_person_inheritance(self):
        self.assertTrue(issubclass(Staff, Person))

    def test_person_inheritance_two(self):
        self.assertTrue(isinstance(self.staff_obj, Person))
