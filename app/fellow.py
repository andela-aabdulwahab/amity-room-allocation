from app.person import Person


class Fellow(Person):

    """ Hold the information of a fellow
    Acts as an object for Fellow. Inherit from Person

    instance Variable:
    level - developer level of fellow, D0, D1, D2..
    stack - the stack the fellow works with

    methods:
    set_level/get_level - setter and getter method for fellow's level
    set_stack/get_stack - setter and getter method for fellow'd level
    want_accomodation - return the true/false base on fellow choice
    set_accomodation - setter fucntion for want accom

    __init__
    Initialize the Superclass constructor
    arguments:
    level
    stack
    want_accom
    """

    def __init__(self, name, gender, want_accom="N", level="Unknown", stack="Unknown"):
        super().__init__(name, gender)
        self.level = level
        self.stack = stack
        self.want_accom = want_accom

    def set_level(self, level):
        """ Set the level of fellow
        arguments:
        level
        """
        self.level = level

    def set_stack(self, stack):
        """ Set the stack of fellow
        arguments
        stack - the stack fellow is working
        """
        self.stack = stack

    def get_level(self):
        """ return the level fellow is """
        return self.level

    def get_stack(self):
        """ return the stack of the fellow """
        return self.stack

    def wants_accomodation(self):
        """ return value base on the value of want_accom"""
        if self.want_accom == "Y":
            return True
        else:
            return False

    def set_wants_accom(self, want_accom):
        """ set value for value for want_accom
        arguments - want_accom
        """
        self.want_accom = want_accom
