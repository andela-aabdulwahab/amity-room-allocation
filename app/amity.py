from app.exceptions import SameNameRoomError
from app.fellow import Fellow
from app.livingspace import LivingSpace
from app.office import Office
from app.person import Person
from app.room import Room
from app.staff import Staff


class Amity():

    """ Serve as the container for persons and rooms
    available.

    Attributes:
        rooms: Dictionary container for all available rooms
        persons: Dictionary container for all persons

    """

    def __init__(self):
        """Initialize instance variable rooms and person with empty dict"""

        self._rooms = {}
        self._persons = {}

    def add_room(self, room_obj):
        """ Property fucntion for _rooms

        Arguments:
            room_obj: Object of type room
        """
        if isinstance(room_obj, Room):
            if not self._rooms.get(room_obj.get_id()):
                self._rooms[room_obj.get_id()] = room_obj
            else:
                raise SameNameRoomError
        else:
            raise TypeError("Argument passed not of type Room")

    def get_rooms(self):
        """ Property fucntion for _rooms

        Return:
            _rooms: dictionary for person obj
        """
        return self._rooms

    def add_person(self, person_obj):
        """ Add person_obj to the persons class

        Arguments:
            person_obj: Object of type Person
        """
        if isinstance(person_obj, Person):
            self._persons[person_obj.identifier] = person_obj
        else:
            raise TypeError("Argument passed not of type Person")

    def get_persons(self):
        """ Property fucntion for _person

        Return:
            _person: dictionary for person obj
        """
        return self._persons

    def get_offices(self):
        """Get all room of type Office.

        Returns:
            offices: Rooms of type office
        """
        offices = {}
        for i in self._rooms:
            if isinstance(self._rooms[i], Office):
                offices[i] = self._rooms[i]
        return offices

    def get_livingspaces(self, gender=None):
        """Gets all the living sapces in _room

        Arguments:
            gender: Gender of the room to return

        Returns:
            gender_livingspaces: Rooms of the gender specify
        """
        livingspaces = {}
        for i in self._rooms:
            if isinstance(self._rooms[i], LivingSpace):
                livingspaces[i] = self._rooms[i]
        if not gender:
            return livingspaces
        gender_livingspaces = {}
        for i in livingspaces:
            if livingspaces[i].gender == gender:
                gender_livingspaces[i] = livingspaces[i]
        return gender_livingspaces

    @staticmethod
    def get_room_type(room_obj):
        """ Return the type of a room

        Arguments:
            room_obj: room object to check

        Returns:
            string of type of room or None if neither
        """

        if isinstance(room_obj, Office):
            return "office"
        elif isinstance(room_obj, LivingSpace):
            return "livingspace"
        else:
            return None

    @staticmethod
    def get_person_type(person_obj):
        """ Return the type of a person

        Arguments
            person_obj: person to check

        Returns
            String of person type or None if neither
        """
        if isinstance(person_obj, Fellow):
            return "fellow"
        elif isinstance(person_obj, Staff):
            return "staff"
        else:
            return None

    rooms = property(get_rooms, add_room)
    persons = property(get_persons, add_person)
