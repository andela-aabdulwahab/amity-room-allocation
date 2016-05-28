from app.person import Person


class Staff(Person):
    ''' Class Staff; Acts as object class for Staff

    Inherits:
        Person

    Instance Variable:
        depertment - The department of the staff

    '''

    def __init__(self, name, gender, department="Unknown"):
        '''involves the constructor of Person class which it's
        replacing

        Arguments:
            name - Name of the staff
            gender - the sex of the staff
            department - department of the staff of the staff
        '''
        self.department = department
        super().__init__(name, gender)
