import unittest

from app.person import Person


class PersonTest(unittest.TestCase):

    def setUp(self):
        self.person_male = Person("Wahab Malik", "M")
        self.person_female = Person("Janet John", "F")
        self.person_male.room_name['office'] = 'Mars'
        self.person_male.room_name['livingspace'] = 'Sapele'

    def test_init_name(self):
        self.assertEqual("Wahab Malik", self.person_male.name)

    def test_init_gender(self):
        self.assertEqual("M", self.person_male.gender)

    def test_is_allocated(self):
        self.assertTrue(self.person_male.is_allocated('office'))

    def test_is_allocated_two(self):
        self.assertFalse(self.person_female.is_allocated("office"))

    def test_generate_id(self):
        first_id = self.person_male.generate_id()
        second_id = self.person_male.generate_id()
        self.assertNotEqual(first_id, second_id)

    def test_generate_id_two(self):
        first_id = self.person_male.generate_id()
        second_id = self.person_female.generate_id()
        self.assertNotEqual(first_id, second_id)
