import unittest

from app.fellow import Fellow
from app.person import Person


class FellowTest(unittest.TestCase):
    def setUp(self):
        self.fellowA = Fellow("Malik Wahab", "M", "Y")
        self.fellowB = Fellow("Jola Ade", "M")

    def test_person_inheritance(self):
        self.assertTrue(issubclass(Fellow, Person))

    def test_person_inheritance_two(self):
        self.assertTrue(isinstance(self.fellowA, Person))

    def test_wants_accomodation(self):
        self.assertTrue(self.fellowA.wants_accomodation())

    def test_wants_accomdation_two(self):
        self.assertFalse(self.fellowB.wants_accomodation())
