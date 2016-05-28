class Room():
    """ The container for rooms
    save the room information and also has functions to add person
    to room

    instance Variable
        name - room name
        size - the maxumum number of occupants

    Methods:
        get_name - return the name of the room
        get_size - return the size of the room
        is_full - checks the status of the room
                  retuen true if filled
                         false id other wise
        add_occupants - add occupants to the room
        remove_occupants - remove occupant to the room
        get_occupants - return the occupants of a room in a dictionary
        get_id - creates id for the room

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
        return Boolean base on status
        """
        if len(self.occupants) < self.size:
            return False
        else:
            return True

    def add_occupants(self, person_obj):
        """ adds occupant to the instance dicttionary
        arguments
        person_obj - an instance of Person

        return - status code to determine of status of the operation
                 1 - successfull
                 2 - room is full
                 3 - already in rooom
        """
        if self.is_full():
            return 2
        name_key = person_obj.get_id()
        if name_key in self._occupants:
            return 3
        else:
            self._occupants[name_key] = person_obj
            return 1

    def get_occupants(self):
        return self._occupants

    def remove_occupant(self, person_obj):
        """ Remove the person object from the occupants of a room
        Arguemnt
            person_object: an instance of person

        Return:
            status code of the operation
            1 - successful
            7 - name not in room
        """
        name_key = person_obj.get_id()
        if name_key in self.occupants:
            del self.occupants[name_key]
            return 1
        else:
            return 7

    def get_id(self):
        """ Create Id for the room using the room name
        return:
            A string of the room id
        """
        name_key = self.name.replace(" ", "")
        return name_key.lower()

    occupants = property(get_occupants, add_occupants)
