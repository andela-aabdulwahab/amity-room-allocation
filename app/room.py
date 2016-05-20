class Room():
    """ The container for rooms
    save the room information and also has functions to add person
    to room

    instance Variable
    name - room name
    size - the maxumum number of occupants

    methods:
    get_name - return the name of the room
    get_size - return the size of the room
    is_full - checks the status of the room
              retuen true if filled
                     false id other wise
    add_occupants - add occupants to the room
    remove_occupants - remove occupant to the room
    get_occupants - return the occupants of a room in a dictionary
    get_id - creates id for the room

    subclasses
    LivingRoom
    Office

    __init__
    Initialize the class with name and the size
    arguments
    name - name of the class
    size - the size of the class
    """

    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.occupants = {}

    def get_name(self):
        """ return the name of room"""
        return self.name

    def get_size(self):
        """ return the size of the room """
        return self.size

    def is_full(self):
        """ checks of if the room is filled
        compare size with the name of occupants in room
        return Boolean base on status
        """
        if len(self.occupants) < self.size:
            return False
        else:
            return True

    def add_occupant(self, person_obj):
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
        if name_key in self.occupants:
            return 3
        else:
            self.occupants[name_key] = person_obj
            return 1

    def remove_occupant(self, person_obj):
        """ Remove the person object from the occupants of a room
        arguemnt
        person_object - an instance of person

        return - status code of the operation
                 1 - successful
                 7 - name not in room
        """
        name_key = person_obj.get_id()
        if name_key in self.occupants:
            del self.occupants[name_key]
            return 1
        else:
            return 7

    def get_occupants(self):
        """return the occupants of the room in dictionary, id, object pair """
        return self.occupants

    def get_id(self):
        """ Create Id for the room using the room name
        return a string
        """
        name_key = self.name.replace(" ", "")
        return name_key.lower()
