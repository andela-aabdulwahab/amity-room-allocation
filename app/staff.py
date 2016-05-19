from app.person import Person


class Staff(Person):
    """ Class Staff; Acts as object class for Staff
    Inherit the class Person
    Instance Variable:
    depertment - The department of the staff
    methods:
    get_department - returns the department of the staff
    set_department - use to set the department variable
    __init__
    involves the constructor of Person class which it's
    replacing
    arguments:
    name - Name of the staff
    gender - the sex of the staff
    department - department of the staff of the staff
    """
    def __init__(self, name, gender, department="Unknown"):
        self.department = department
        #Person.__init__(name, gender)
        super().__init__(name, gender)

    def get_department(self):
        """ return the department of the staff """
        return self.department

    def set_department(self, department):
        """ Set the department instance variable
        arguments:
        department - the department of the staff
        """
        self.department = department
