import unittest
from app.person import Person

class PersonTest(unittest.TestCase):

	def setUp(self):
		self.person_male = Person("Wahab Malik", "M")
		self.person_female = Person("Janet John")
		self.person_male.set_allocation("WhiteHouse")

	def test_init_name(self):
		self.assertEqual("Wahab Malik", self.person_male.name)

	def test_init_gender(self):
		self.assertEqual("M", self.person_male.gender)

	def test_get_name(self):
		self.assertEqual("Wahab Malik", self.person_male.get_name())

	def test_get_gender(self):
		self.assertEqual("M", self.person_male.get_gender())

	def test_defualt_gender(self):
		self.assertEqual(None, self.person_female.get_gender())

	def test_set_gender(self):
		self.person_female.set_gender("F")
		self.assertEqual("F", self.person_female.get_gender())

	def test_get_allocation(self):
		self.assertEqual(self.person_male.get_allocation(), "WhiteHouse")

	def test_set_allocation(self):
		self.person_male.set_allocation("brownFire")
		self.assertEqual(self.person_male.room_name, "brownFire")

	def test_is_allocated(self):
		self.assertTrue(self.person_male.is_allocated())

	def test_is_allocated_two(self):
		self.assertFalse(self.person_female.is_allocated())

	def test_get_id(self):
		self.assertEqual(self.person_male.get_id(), 'wahabmalik')