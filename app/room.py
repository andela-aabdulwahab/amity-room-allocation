from app.exceptions import PersonInRoomError, RoomIsFullError


class Room():
    """ The container for rooms
    save the room information and also has functions to add person
    to room

    Attibutes:
        name - room name
        size - the maxumum number of occupants

    Subclasses:
        LivingRoom
        Office

    """

    def __init__(self, name, size):
        """Initialize the class with name and the size
        Arguments:
            name: name of the class
            size: the size of the class

        """
        self.name = name
        self.size = size
        self._occupants = {}

    def is_full(self):
        """ checks of if the room is filled
        compare size with the name of occupants in room

        Returns:
            True if occupancy exceeded False otherwise

        """
        if len(self._occupants) < self.size:
            return False
        else:
            return True

    def add_occupants(self, person_obj):
        """ adds occupant to the instance dicttionary
        arguments
        person_obj - an instance of Person

        Raises:
            RoomIsFullError : When room is full
            PersonInRoomError: When person objec already in room

        returns:
           True on success
        """
        if self.is_full():
            raise RoomIsFullError("Person cannot be add to a full room")
        elif person_obj.identifier in self.occupants:
            raise PersonInRoomError("Person Object already in room")
        else:
            self._occupants[person_obj.identifier] = person_obj
            return True

    def get_occupants(self):
        return self._occupants

    def get_id(self):
        """ Create Id for the room using the room name
        return:
            room_id: represent room Id
        """
        name_key = self.name.replace(" ", "")
        return name_key.lower()

    occupants = property(get_occupants, add_occupants)
