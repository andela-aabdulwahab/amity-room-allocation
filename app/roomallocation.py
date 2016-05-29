import random

from app.amity import Amity
from app.exceptions import NoRoomError, PersonAllocatedError
from app.fellow import Fellow


class RoomAllocation():
    ''' The main class for communication with the room
    allocation application. provides an API for all action
    that the application can perform

    Attributes:
        amity - an instance of class Amity

    '''

    def __init__(self, amity_obj):
        """ creates an instance variable of type Amity with the
        object passed to it

        Arguments
            amity_obj: object of class Amity
        """
        self.amity = amity_obj

    def create_room(self, room_obj):
        """ Create a room and add to Amity

        Arguments:
            room_obj: room to be added to database

        Raises:
            TypeError
        """
        self.amity.rooms = room_obj

    def create_person(self, person_obj):
        """ Create a person and add to Amity

        Arguments:
            person_obj: person to be added to database

        Raises:
            TypeError

        Returns:
            Dict: of the rooms allocated person
        """
        try:
            self.amity.persons = person_obj
        except:
            raise TypeError
        else:
            try:
                office_status = self.allocate_office(person_obj.identifier)
            except NoRoomError:
                office_status = False
            if (isinstance(person_obj, Fellow) and
               person_obj.wants_accomodation()):
                try:
                    livingspace_status = \
                        self.allocate_livingspace(person_obj.identifier)
                except NoRoomError:
                    livingspace_status = False
                return (office_status, livingspace_status)
            return (office_status)

    def select_random(self, adict):
        """ Return a random member of the database provided

        Arguments:
            adict: this is the dictionary where random member will be selected
        """
        random_key = random.choice(list(adict.keys()))
        return adict[random_key]

    def allocate_office(self, person_id):
        """ allocate office to person of specified id

        Arguments:
            person_id: id of person object that will be allocated to an office

        Returns:
            the status of the allocation
        """
        return self.allocate_room(person_id, self.amity.get_offices())

    def allocate_livingspace(self, person_id):
        """ allocate livingroom to person of specified id
        Arguments:
            person_id - id of person object that will be allocated to a
                        livingroom

        Returns:
            the status of the allocation
        """
        try:
            person_obj = self.amity.persons[person_id]
            gender = person_obj.gender
            gender_livingrooms = self.amity.get_livingspaces(gender)
        except KeyError:
            raise KeyError("Invalid person Id provided")
        return self.allocate_room(person_id, gender_livingrooms)

    def allocate_room(self, person_id, room_dict):
        """ allocate a random room from the supplied room dictionary
        to person of specified id

        Raises:
            KeyError
            PersonInRoomError

        Arguments
            person_id: id pf person object to be allocated to a random room
            room_dict: a dictionary object of type room

        Return:
            boolean: true on successful allocation

        """

        person_obj = self.amity.persons[person_id]
        no_of_rooms = len(room_dict.keys())
        if no_of_rooms < 1:
            raise NoRoomError
        i = 0
        while i <= no_of_rooms:
            i += 1
            room_obj = self.select_random(room_dict)
            if not room_obj.is_full():
                break
            if i == no_of_rooms:
                raise NoRoomError("No free room to allocate Person")
        room_type = self.amity.room_type(room_obj)
        if person_obj.is_allocated(room_type):
            raise PersonAllocatedError
        else:
            room_obj.occupants = person_obj
            person_obj.room_name[room_type] = room_obj.get_id()
            return True

    def rellocate_person(self, person_id, new_room_id):
        """ rellocate person to the room specified

        Raises:
            KeyError

        Arguments
            person_id: Id of person to be rellocated
            new_room_id: room to be relocated to

        """
        try:
            person_obj = self.amity.persons[person_id]
        except KeyError:
            raise KeyError("Invalid Person Id provided")
        try:
            new_room_obj = self.amity.rooms[new_room_id]
        except KeyError:
            raise KeyError("Invalid Room Id provided")
        room_type = self.amity.room_type(new_room_obj)
        old_room_name = person_obj.room_name[room_type]
        old_room_obj = self.amity.rooms[old_room_name]
        if person_id in old_room_obj.occupants:
            del old_room_obj.occupants[person_obj.identifier]
            new_room_obj.occupants = person_obj
            person_obj.room_name[room_type] = new_room_obj.get_id()

    def remove_room(self, room_id):
        """ Remove a specified room from amity
        render all person in room unallocated

        Arguments
            room_id - id of room to be remove from amity

        """
        room = self.amity.rooms[room_id]
        room_type = self.amity.room_type(room)
        persons = room.occupants
        for i in persons:
            person = persons[i]
            del person.room_name[room_type]
        del self.amity.rooms[room_id]

    def remove_person(self, person_id):
        """ Remove a specified person from amity
        remove person form room occupied

        Arguments:
            person_id: id of the person to be remove
        """
        person = self.amity.persons[person_id]
        office_allocation = person.room_name.get("office")
        livingroom_allocation = person.room_name.get("livingroom")
        if office_allocation:
            office = self.amity.rooms[office_allocation]
            del office.occupants[person.identifier]
        if livingroom_allocation:
            livingroom = self.amity.rooms[livingroom_allocation]
            del livingroom.occupants[person.identifier]
        del self.amity.persons[person_id]

    def get_unallocated(self):
        """ gets all person in amity without an office
        or a livingroom

        Returns:
            list: a list of dictionary of persons unallocated for livingroom
            and office
        """
        persons = self.amity.persons
        office_unallocated = {}
        livingroom_unallocated = {}
        for person_id in persons:
            if isinstance(persons[person_id], Fellow):
                if not persons[person_id].is_allocated("office"):
                    office_unallocated[person_id] = persons[person_id]
                if not persons[person_id].is_allocated('livingspace'):
                    livingroom_unallocated[person_id] = persons[person_id]
            else:
                if not persons[person_id].is_allocated("office"):
                    office_unallocated[person_id] = persons[person_id]
        return [office_unallocated, livingroom_unallocated]

    def print_unallocated_to_file(self, file_name):
        """ Prints name of unallocated person to file specified

        Arguments:
            file_name: path and name to file where information will be printed
        """
        file_obj = open(file_name, "w")
        unallocated_string = self.build_unallocation_string()
        file_obj.write(unallocated_string)
        file_obj.close()

    def build_unallocation_string(self):
        """ Builds the string of unallocated persons

        Return
            string of unallocated persons

        """
        unallocated = self.get_unallocated()
        office_unallocated = unallocated[0]
        livingroom_unallocated = unallocated[1]
        unallocated_string = " "
        unallocated_string += " --Unallocated for Office-- \n\n"
        for person_id in office_unallocated:
            unallocated_string += \
                self.print_person(office_unallocated[person_id])
        unallocated_string += "\n \n --Unallocated for LivingSpace-- \n\n"
        for person_id in livingroom_unallocated:
            unallocated_string += \
                self.print_person(livingroom_unallocated[person_id])
        return unallocated_string

    def print_allocation_to_file(self, file_name):
        """ Prints the room allocation at Amity to file

        Arguments:
            file_name: path and name to file where information will be printed
        """
        file_obj = open(file_name, "w")
        allocation_string = self.build_allocation_string()
        file_obj.write(allocation_string)
        file_obj.close()

    def build_allocation_string(self):
        """ BUild the string of the allocation in amity with rooms
        and persons in rooms

        Return
            a string of the allocation
        """
        rooms = self.amity.rooms
        allocation_string = ""
        for i in rooms:
            room = rooms[i]
            allocation_string += self.print_room(room.get_id())
        return allocation_string

    def print_room(self, room_id):
        """ Builds the string of a room with the persons in it

        Arguments:
            room_id - id of room to print

        """
        room = self.amity.rooms[room_id]
        room_string = ""
        room_type = self.amity.room_type(room)
        room_string += "\n--" + room.name + "(" + room_type + ")--\n"
        persons = room.occupants
        for i in persons:
            room_string += self.print_person(persons[i])
        return room_string

    def print_person(self, person_obj):
        """ Builds a string of person object printing out the name

        Arguments:
            person_obj - person to printed to file

        Returns:
            string: of the persons name, person_type and accomodation status
        """
        name = person_obj.name.upper()
        want_accomodation = ""
        person_type = self.amity.person_type(person_obj)
        if person_type == "fellow":
            want_accomodation = person_obj.wants_accom
        return (name + ' ' + person_type.upper() + ' ' +
                want_accomodation + "\n")

    def save_to_database(self, allocation_db_obj):
        """ Save the current state of person to database, saving all
        persons and rooms in Amity to database

        Arguments:
            allocation_db_obj: database connection to be use to save data
        """
        allocation_db_obj.empty_tables()
        persons = self.amity.persons
        rooms = self.amity.rooms
        for i in persons:
            allocation_db_obj.add_person(persons[i])
        for i in rooms:
            allocation_db_obj.add_room(rooms[i])

    def load_from_database(self, allocation_db_obj):
        """ load database information to create a new application state
        reset Amity to the new state

        Arguments
            allocation_db_obj: database connection to be use to save data
        """
        persons = allocation_db_obj.get_persons()
        rooms = allocation_db_obj.get_rooms()
        amity = Amity()

        for i in persons:
            person = persons[i]
            if isinstance(person, Fellow):
                livingroom_allocation = person.room_name.get("livingroom")
                office_allocation = person.room_name.get("office")
                if livingroom_allocation:
                    livingroom = rooms[livingroom_allocation]
                    livingroom.add_occupant(person)
                if office_allocation:
                    office = rooms[office_allocation]
                    office.add_occupant(person)
            else:
                office_allocation = person.room_name.get("office")
                if office_allocation:
                    office = rooms[office_allocation]
                    office.add_occupant(person)
            amity.add_person(person)

        for i in rooms:
            amity.add_room(rooms[i])
        self.amity = amity
