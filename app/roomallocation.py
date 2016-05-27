import random
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect. \
    getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from app.office import Office
from app.fellow import Fellow
from app.allocation_db import AllocationDb
from app.amity import Amity
from app.staff import Staff
from app.livingroom import LivingRoom



class RoomAllocation():
    ''' The main class for communication with the room
    allocation application. provides an API for all action
    that the application can perform

    instance variable
    amity - an instance of class Amity

    methods
    create_room - add room to the amity class i.e the application
    create_person - add person the application by adding the amity object
    select_random - return a random meeber of a dictionaty passed
    allocate_office - allocate office to person
    allocate_room - allocate room to person
    rellocate_person - rellocate person to the specified room
    get_unallocated - return all unallocated person
    print_unallocated_to_file - print all unallocated person information to file
    print_allocation_to_file - print rooms and persons allocated to them
    print_person_to_file - extract neccessary person information and print it to file
    print_room_to_file - print person of a given room to file
    save to database - save all rooms and persons in amity to the specified database
    load_from_database - loads all persons and rooms in database into Amity

    __init__
    creates an instance variable of type Amity with the
    object passed to it

    arguments
    amity_obj - object of class Amity

    '''

    def __init__(self, amity_obj):
        self.amity = amity_obj

    def create_room(self, room_obj):
        ''' Create a room and add to Amity

        arguments
        room_obj - room to be added to database
        '''
        self.amity.add_room(room_obj)

    def create_person(self, person_obj):
        ''' Create a person and add to Amity

        arguments
        person_obj - person to be added to database
        '''
        person_id = person_obj.get_id()
        if not self.amity.get_person(person_id):
            self.amity.add_person(person_obj)
            office_status = self.allocate_office(person_id)
            if isinstance(person_obj, Fellow) and person_obj.wants_accomodation():
                livingroom_status = self.allocate_livingroom(person_id)
                return {"office_status": office_status, "room_status": livingroom_status}
            return {"office_status": office_status}


    def select_random(self, adict):
        ''' Return a random member of the database provided
        arguments
        adict - this is the dictionary where random member will be selected

        sample picks "1" from keys and return a list. reason for [0]

        '''
        #random_key = random.sample(adict.keys(), 1)[0]
        random_key = random.choice(list(adict.keys()))
        return adict[random_key]

    def allocate_office(self, person_id):
        ''' allocate office to person of specified id
        arguments
        person_id - id of person object that will be allocated to an office

        returns the status of the allocation
        '''
        return self.allocate_room(person_id, self.amity.get_offices())

    def allocate_livingroom(self, person_id):
        ''' allocate livingroom to person of specified id
        arguments
        person_id - id of person object that will be allocated to a livingroom

        returns the status of the allocation
        '''
        person_obj = self.amity.get_person(person_id)
        if person_obj is None:
            return 14
        gender = person_obj.get_gender()
        gender_livingrooms = self.amity.get_livingrooms(gender)
        return self.allocate_room(person_id, gender_livingrooms)

    def allocate_room(self, person_id, room_dict):
        ''' allocate a random room from the supplied room dictionary
        to person of specified id

        arguments
        person_id - id pf person object to be allocated to a random room
        room_dict - a dictionary object of type room

        return 1 if successfull or error code if otherwise
        '''
        person_obj = self.amity.get_person(person_id)
        no_of_rooms = room_dict.keys().__len__()
        if no_of_rooms < 1:
            return 14
        i = 0
        while i <= no_of_rooms:
            i += 1
            room_obj = self.select_random(room_dict)
            if not room_obj.is_full():
                break
            if i == no_of_rooms:
                return 12
        if isinstance(room_obj, Office):
            room_type = "office"
        else:
            room_type = "livingroom"
        if person_obj.is_allocated(room_type):
            return 8
        else:
            status = room_obj.add_occupant(person_obj)
            if status == 1:
                person_obj.set_allocation(room_type, room_obj.get_id())
                return 1
            else:
                return status

    def rellocate_person(self, person_id, new_room_id):
        ''' rellocate person to the room specified

        arguments
        person_id - Id of person to be rellocated
        new_room_id - room to be relocated to

        '''
        person_obj = self.amity.get_person(person_id)
        if person_obj is None:
            return 14
        new_room_obj = self.amity.get_room(new_room_id)
        if isinstance(new_room_obj, Office):
            room_type = "office"
        else:
            room_type = "livingroom"
        old_room_name = person_obj.get_allocation(room_type)
        old_room_obj = self.amity.get_room(old_room_name)
        if person_id in old_room_obj.get_occupants():
            old_room_obj.remove_occupant(person_obj)
            status = new_room_obj.add_occupant(person_obj)
            if status == 1:
                person_obj.set_allocation(room_type, new_room_obj.get_id())
            return 1
        else:
            return 7


    def remove_room(self, room_id):
        ''' Remove a specified room from amity
        render all person in room unallocated

        arguments
        room_id - id of room to be remove from amity
        '''
        room = self.amity.get_room(room_id)
        if room is None:
            return 14
        room_type = self.amity.room_type(room)
        if room:
            persons = room.get_occupants()
            for i in persons:
                person = persons[i]
                del person.room_name[room_type]
            del self.amity.rooms[room_id]
        return self


    def remove_person(self, person_id):
        ''' Remove a specified person from amity
        remove person form room occupied

        arguments
        person_id - id of the person to be remove
        '''
        person = self.amity.get_person(person_id)
        if person is None:
            return 14
        office_allocation = person.get_allocation("office")
        livingroom_allocation = person.get_allocation("livingroom")
        if office_allocation != 9:
            office = self.amity.get_room(office_allocation)
            office.remove_occupant(person)
        if livingroom_allocation != 9:
            livingroom = self.amity.get_room(livingroom_allocation)
            livingroom.remove_occupant(person)
        del self.amity.persons[person_id]
        return self

    def get_unallocated(self):
        ''' gets all person in amity without an office
        or a livingroom

        return
        a list of dictionary of persons unallocated for livingroom and office
        '''
        persons = self.amity.get_persons()
        office_unallocated = {}
        livingroom_unallocated = {}
        for person_id in persons:
            if isinstance(persons[person_id], Fellow):
                if not persons[person_id].is_allocated("office") and not persons[person_id].is_allocated("livingroom"):
                    office_unallocated[person_id] = persons[person_id]
                    livingroom_unallocated[person_id] = persons[person_id]
                elif not persons[person_id].is_allocated("office"):
                    office_unallocated[person_id] = persons[person_id]
                elif not persons[person_id].is_allocated('livingroom'):
                    livingroom_unallocated[person_id] = persons[person_id]
        return [office_unallocated, livingroom_unallocated]

    def allocate_free(self):
        pass

    def print_unallocated_to_file(self, file_name):
        ''' Prints name of unallocated person to file specified

        arguments
        file_name - path and name to file where information will be printed
        '''
        file_obj = open(file_name, "w")
        unallocated_string = self.build_unallocation_string()
        file_obj.write(unallocated_string)
        file_obj.close()

    def build_unallocation_string(self):
        ''' Builds the string of unallocated persons

        return
        string of unallocated persons
        '''
        unallocated = self.get_unallocated()
        office_unallocated = unallocated[0]
        livingroom_unallocated = unallocated[1]
        office_head = " --Unallocated for Office-- \n\n"
        livingroom_head = "\n \n --Unallocated for LivingRoom-- \n\n"
        unallocated_string = " "
        unallocated_string += " --Unallocated for Office-- \n\n"
        for person_id in office_unallocated:
            unallocated_string += self.print_person(office_unallocated[person_id])
        unallocated_string += "\n \n --Unallocated for LivingRoom-- \n\n"
        for person_id in livingroom_unallocated:
            unallocated_string += self.print_person(livingroom_unallocated[person_id])
        return unallocated_string

    def print_allocation_to_file(self, file_name):
        ''' Prints the room allocation at Amity to file

        arguments
        file_name - path and name to file where information will be printed
        '''
        file_obj = open(file_name, "w")
        allocation_string = self.build_allocation_string()
        file_obj.write(allocation_string)
        file_obj.close()

    def build_allocation_string(self):
        ''' BUild the string of the allocation in amity with rooms
        and persons in rooms

        return
        a string of the allocation
        '''
        rooms = self.amity.get_rooms()
        allocation_string = ""
        for i in rooms:
            room = rooms[i]
            allocation_string += self.print_room(room.get_id())
        return allocation_string

    def print_room(self, room_id):
        ''' Builds the string of a room with the persons in it

        arguments
        room_id - id of room to print

        '''
        room = self.amity.get_room(room_id)
        room_string = ""
        if isinstance(room, Office):
                room_type = "Office"
        else:
            room_type = "Living Room"
        room_string += "\n--"+room.get_name()+"("+room_type+")--\n"
        persons = room.get_occupants()
        for i in persons:
            room_string += self.print_person(persons[i])
        return room_string

    def print_person(self, person_obj):
        ''' Builds a string of person object printing out the name

        arguments
        person_obj - person to printed to file

        returns
        a string of the persons name, person_type and accomodation status
        '''
        name = person_obj.get_name().upper()
        want_accomodation = ""
        if isinstance(person_obj, Fellow):
                person_type = "FELLOW"
                want_accomodation = person_obj.want_accom.upper()
        else:
            person_type = "STAFF"
        return name + ' ' + person_type + ' ' + want_accomodation + "\n"

    def save_to_database(self, allocation_db_obj):
        ''' Save the current state of person to database, saving all
        persons and rooms in Amity to database

        argument
        allocation_db_obj - database connection to be use to save data
        '''
        allocation_db_obj.empty_tables()
        persons = self.amity.get_persons()
        rooms = self.amity.get_rooms()
        for i in persons:
            allocation_db_obj.add_person(persons[i])
        for i in rooms:
            allocation_db_obj.add_room(rooms[i])
        return self

    def load_from_database(self, allocation_db_obj):
        ''' load database information to create a new application state
        reset Amity to the new state

        argument
        allocation_db_obj - database connection to be use to save data
        '''
        persons = allocation_db_obj.get_persons()
        rooms = allocation_db_obj.get_rooms()
        amity = Amity()

        for i in persons:
            person = persons[i]
            if isinstance(person, Fellow):
                livingroom_allocation = person.get_allocation("livingroom")
                office_allocation = person.get_allocation("office")
                if livingroom_allocation != 9:
                    livingroom = rooms[livingroom_allocation]
                    livingroom.add_occupant(person)
                if person.get_allocation("office") != 9:
                    office = rooms[office_allocation]
                    office.add_occupant(person)
            else:
                office_allocation = person.get_allocation("office")
                if office_allocation != 9:
                    office = rooms[office_allocation]
                    office.add_occupant(person)
            amity.add_person(person)

        for i in rooms:
            amity.add_room(rooms[i])
        self.amity = amity
        return self
