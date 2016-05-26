from app.livingroom import LivingRoom
from app.office import Office


class Amity():

    ''' Serve as the container for persons and rooms
    available.

    instance variable
    rooms - Dictionary container for all available rooms
    persons - Dictionary container for all persons

    add_room - add a room object to the rooms variable
    add_person - add person to the person variable
    get_room - return the room with the given id
    get_rooms - return all rooms
    get_person - return the person with the given id
    get_persons - return the all persons
    get_offices - return rooms of instance Office
    get_livingroom - return rooms of instance LivingRoom with the given gender
    get_all_livingroom - return all rooms of instance LivingRoom

    __init__
    initialize instance variable rooms and person with empty dict
    arguments:
    '''

    def __init__(self):
        self.rooms = {}
        self.persons = {}

    def add_room(self, room_obj):
        ''' Add room_obj to the class variable room_obj
        arguments:
        room_obj - object of type Room
        '''
        self.rooms[room_obj.get_id()] = room_obj

    def get_room(self, room_key):
        ''' Return the room of key room_key for the rooms dict
        argument:
        room_key
        '''
        return self.rooms.get(room_key)

    def get_rooms(self):
        ''' Returns all rooms '''
        return self.rooms

    def add_person(self, person_obj):
        ''' Add person_obj to the persons class
        arguments
        person_obj - Object of type Person
        '''
        self.persons[person_obj.get_id()] = person_obj

    def get_person(self, person_id):
        ''' Return the Object with person_id in the persons dict

        arguments
        person_id - of type person
        '''
        return self.persons.get(person_id)

    def get_persons(self):
        ''' return all persons in the person'''
        return self.persons

    def get_offices(self):
        ''' Return all room of instance Office '''
        rooms = self.get_rooms()
        offices = {}
        for i in rooms:
            if isinstance(rooms[i], Office):
                offices[i] = rooms[i]
        return offices

    def get_all_livingrooms(self):
        ''' Return all rooms of instance LivingRoom '''
        rooms = self.get_rooms()
        livingrooms = {}
        for i in rooms:
            if isinstance(rooms[i], LivingRoom):
                livingrooms[i] = rooms[i]
        return livingrooms

    def get_livingrooms(self, gender):
        ''' Return all rooms of instance LivingRoom with gender
        argument
        gender - gender of rooms to return
        '''
        gender_livingrooms = {}
        livingrooms = self.get_all_livingrooms()
        for i in livingrooms:
            if livingrooms[i].get_gender() == gender:
                gender_livingrooms[i] = livingrooms[i]
        return gender_livingrooms

    def room_type(self, room_obj):
        ''' Return the type of a room

        arguments
        room_obj - room object to check

        return
        "office" if an instance of office
        "livingroom" if an instance of livingroom
        None - if niether
        '''

        if isinstance(room_obj, Office):
            return "office"
        elif isinstance(room_obj, LivingRoom):
            return "livingroom"
        else:
            return None

    def person_type(self, person_obj):
        ''' Return the type of a person

        arguments
        person_obj - person to check

        return
        "FELLOW" - if an instance of Fellow
        "STAFF" - if an instance of Staff
        "None" - if neither
        '''
        if isinstance(person_obj, Fellow):
            return "FELLOW"
        elif isinstance(person_obj, Staff):
            return "STAFF"
        else:
            return None
