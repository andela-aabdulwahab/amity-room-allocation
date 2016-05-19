import unittest

from app.fellow import Fellow
from app.person import Person


class FellowTest(unittest.TestCase):
    def setUp(self):
        self.fellowA = Fellow("Malik Wahab", "M", "Y", "1", "Python")
        self.fellowB = Fellow("Jola Ade", "M")

    def test_person_inheritance(self):
        self.assertTrue(issubclass(Fellow, Person))

    def test_set_level(self):
        self.fellowB.set_level("1")
        self.assertEqual(self.fellowB.level, "1")

    def test_get_level(self):
        self.assertEqual(self.fellowA.get_level(), "1")

    def test_set_stack(self):
        self.fellowB.set_stack("ruby")
        self.assertEqual(self.fellowB.stack, "ruby")

    def test_get_stack(self):
        self.assertEqual(self.fellowA.get_stack(), "Python")

    def test_wants_accomodation(self):
        self.assertTrue(self.fellowA.wants_accomodation())

    def test_wants_accomdation_two(self):
        self.assertFalse(self.fellowB.wants_accomodation())

    def test_set_wants_accomdation(self):
        self.fellowA.set_wants_accom("N")
        self.assertFalse(self.fellowA.wants_accomodation())
