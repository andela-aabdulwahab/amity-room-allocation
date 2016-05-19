import unittest
from app.person import Person
from app.staff import Staff


class TestStaff(unittest.TestCase):

	def setUp(self):
		self.staff_obj = Staff("Joe Jack", "M", "Engineering")
	def test_person_inheritance(self):
		self.assertTrue(issubclass(Staff, Person))
	def test_get_dept(self):
		self.assertEqual(self.staff_obj.get_department(), "Engineering")
	def test_get_name(self):
		self.assertEqual("Joe Jack", self.staff_obj.get_name())
