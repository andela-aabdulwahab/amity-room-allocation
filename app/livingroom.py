from app.fellow import Fellow
from app.room import Room


class LivingRoom(Room):

    """ object container for living room
    Inherits
        Room

    Attributes:
        gender(str): gender of allowed occupants

    """

    def __init__(self, name, gender):
        """set the size of the room to 4 by calling the base class
        constructor to 4
        set gender of allowed occupants

        Arguments
            name(str): name of the room
            gener(str): the gender allowed for the room
        """
        super().__init__(name, 4)
        self.gender = gender

    def add_occupant(self, person_obj):
        """ override the Room add_occupant
        determining if is a fellow or gender

        Arguments:
            person: instance person_object

        Returns:
        """
        if not isinstance(person_obj, Fellow):
            return 5
        elif self.gender != person_obj.gender:
            return 4
        else:
            return super().add_occupant(person_obj)

    def get_gender(self):
        """ return the gender allowed for room"""
        return self.gender
