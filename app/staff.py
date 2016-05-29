from app.person import Person


class Staff(Person):
    """ Class Staff; Acts as object class for Staff

    Inherits:
        Person

    """

    def __init__(self, name, gender):
        """involves the constructor of Person class which it's
        replacing

        Arguments:
            name: Name of the staff
            gender: the sex of the staff
        """
        super().__init__(name, gender)
