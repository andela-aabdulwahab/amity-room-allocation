from app.exceptions import PersonNotFellowError, RoomGenderDiffError
from app.fellow import Fellow
from app.room import Room


class LivingSpace(Room):

    """ object container for living room
    Inherits:
        Room

    Raises:
        PersonNotFellowError
        RoomGenderDiffError

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

    def get_occupants(self):
        """ getter class for the occupants

        Returns:
            _occupants
        """
        return self._occupants

    def add_occupants(self, person_obj):
        """ override the Room add_occupant
        determining if is a fellow or gender

        Raises:
            PersonNotFellowError
            RoomGenderDiffError
            RoomIsFullError

        Arguments:
            person: instance person_object

        Returns:
            True
        """
        if not isinstance(person_obj, Fellow):
            raise PersonNotFellowError()
        elif self.gender != person_obj.gender:
            raise RoomGenderDiffError("Fellow can't be added to room of " +
                                      "opposite gender")
        else:
            return super().add_occupants(person_obj)

    occupants = property(get_occupants, add_occupants)
