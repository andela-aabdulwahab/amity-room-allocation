import random

from app.amity import Amity
from app.exceptions import *
from app.fellow import Fellow
from app.roomallocation_print import RoomAllocationPrint
from app.staff import Staff


class RoomAllocation():
    """The main class for communication with the room
    allocation application. provides an API for all action
    that the application can perform

    Attributes:
        amity - an instance of class Amity

    """

    def __init__(self, amity_obj):
        """Creates an instance variable of type Amity with the
        object passed to it

        Arguments
            amity_obj: object of class Amity
            rmprint: Object of type RoomAllocationPrint
        """
        self.amity = amity_obj
        self.rmprint = RoomAllocationPrint(self.amity)

    def create_room(self, room_obj):
        """Create a room and add to Amity.

        Arguments:
            room_obj: room to be added to database

        Raises:
            TypeError
        """
        try:
            self.amity.add_room(room_obj)
        except SameNameRoomError:
            return False
        else:
            return True

    def create_person(self, person_obj):
        """Create a person and add to Amity.

        Arguments:
            person_obj: person to be added to database

        Raises:
            TypeError

        Returns:
            Dict: of the rooms allocated person
        """
        self.amity.add_person(person_obj)
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
            return [office_status, livingspace_status]
        return [office_status]

    def load_persons_from_text(self, file_name):
        """Load persons from file and add to Amity.

        Arguments:
            file_name: string, location to load txt

        Return:
            List: of the status for every line
        """
        with open(file_name, 'r') as f:
            names = [x.strip('\n') for x in f.readlines()]
        f.close()
        status = []
        for person_info in names:
            person_obj = RoomAllocation.get_person_from_line(person_info)
            status.append(self.create_person(person_obj))
        return status

    @staticmethod
    def get_person_from_line(person_info):
        """Create person object from the person info.

        Arguments:
            person_info: String Line of text containing person info

        Returns:
            Person: Type Fellow or Staff
        """
        person = person_info.split(' ')
        name = person[0] + ' ' + person[1]
        gender = person[2]
        if person[3].lower() == 'fellow':
            return Fellow(name, gender, person[4])
        return Staff(name, gender)

    @staticmethod
    def select_random(adict):
        """Return a random member of the database provided.

        Arguments:
            adict: this is the dictionary where random member will be selected

        Returns:
            random value of a dict
        """
        random_key = random.choice(list(adict.keys()))
        return adict[random_key]

    def allocate_office(self, person_id):
        """Allocate office to person of specified id.

        Arguments:
            person_id: id of person object that will be allocated to an office

        Returns:
            the status of the allocation
        """
        return self.allocate_room(person_id, self.amity.get_offices())

    def allocate_livingspace(self, person_id):
        """Allocate livingspace to person of specified id.

        Arguments:
            person_id - id of person object that will be allocated to a
                        livingspace
        Returns:
            the status of the allocation
        """
        try:
            person_obj = self.amity.persons[person_id]
            gender = person_obj.gender
            gender_livingspaces = self.amity.get_livingspaces(gender)
        except KeyError:
            raise KeyError("Invalid person Id provided")
        return self.allocate_room(person_id, gender_livingspaces)

    def allocate_room(self, person_id, room_dict):
        """Allocate a random room from the supplied room dictionary
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
            room_obj = RoomAllocation.select_random(room_dict)
            if not room_obj.is_full():
                break
            if i == no_of_rooms:
                raise NoRoomError("No free room to allocate Person")
        room_type = Amity.get_room_type(room_obj)
        if person_obj.is_allocated(room_type):
            raise PersonAllocatedError
        else:
            room_obj.add_occupant(person_obj)
            person_obj.room_name[room_type] = room_obj.get_id()
            return True

    def rellocate_person(self, person_id, new_room_id):
        """Rellocate person to the room specified.

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
        room_type = Amity.get_room_type(new_room_obj)
        old_room_name = person_obj.room_name.get(room_type)
        try:
            new_room_obj.add_occupant(person_obj)
        except (RoomIsFullError, PersonInRoomError) as err:
            raise err
        else:
            if old_room_name:
                old_room_obj = self.amity.rooms[old_room_name]
                del old_room_obj.occupants[person_obj.identifier]
            person_obj.room_name[room_type] = new_room_obj.get_id()

    def remove_room(self, room_id):
        """Remove a specified room from amity
        render all person in room unallocated

        Arguments
            room_id - id of room to be remove from amity

        """
        room = self.amity.rooms[room_id]
        room_type = Amity.get_room_type(room)
        persons = room.occupants
        for i in persons:
            person = persons[i]
            del person.room_name[room_type]
        del self.amity.rooms[room_id]

    def remove_person(self, person_id):
        """Remove a specified person from amity
        remove person form room occupied

        Arguments:
            person_id: id of the person to be remove
        """
        person = self.amity.persons[person_id]
        office_allocation = person.room_name.get("office")
        livingspace_allocation = person.room_name.get("livingspace")
        if office_allocation:
            office = self.amity.rooms[office_allocation]
            del office.occupants[person.identifier]
        if livingspace_allocation:
            livingspace = self.amity.rooms[livingspace_allocation]
            del livingspace.occupants[person.identifier]
        del self.amity.persons[person_id]

    def save_to_database(self, allocation_db_obj):
        """Save the current state of person to database, saving all
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
        """Load database information to create a new application state
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
                livingspace_allocation = person.room_name.get("livingspace")
                office_allocation = person.room_name.get("office")
                if livingspace_allocation:
                    livingspace = rooms[livingspace_allocation]
                    livingspace.add_occupant(person)
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

        # update the amity object
        self.amity = amity
