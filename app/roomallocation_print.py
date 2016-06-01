from app.fellow import Fellow

class RoomAllocationPrint():
    """Formats and print data in to Amity

    Attribute:
        amity: Object of type amity

    """

    def __init__(self, amity_obj):
        """Creates an instance variable of type Amity with the
        object passed to it

        Arguments
            amity: object of class Amity

        """
        self.amity = amity_obj

    def print_persons(self):
        """Print a list of persons in amity.

        Returns
            String: names and identifier of persons in Amity

        """
        persons = self.amity.persons
        persons_string = "List of Persons with Id\n"
        for i in persons:
            person = persons[i]
            persons_string += (person.name + " " + self
                               .amity.person_type(person) + " " +
                               person.identifier + "\n")
        return persons_string

    def get_unallocated(self):
        """Get all person in amity without an office
        or a living space

        Returns:
            list: a list of dictionary of persons unallocated for Living space
            and office
        """
        persons = self.amity.persons
        office_unallocated = {}
        livingspace_unallocated = {}
        for person_id in persons:
            if not persons[person_id].is_allocated("office"):
                    office_unallocated[person_id] = persons[person_id]
            if isinstance(persons[person_id], Fellow):
                if not persons[person_id].is_allocated('livingspace'):
                    livingspace_unallocated[person_id] = persons[person_id]
        return [office_unallocated, livingspace_unallocated]

    def print_unallocated_to_file(self, file_name):
        """Print name of unallocated person to file specified.

        Arguments:
            file_name: path and name to file where information will be printed
        """
        file_obj = open(file_name, "w")
        unallocated_string = self.build_unallocation_string()
        file_obj.write(unallocated_string)
        file_obj.close()

    def build_unallocation_string(self):
        """Build the string of unallocated persons.

        Return
            string of unallocated persons

        """
        unallocated = self.get_unallocated()
        office_unallocated = unallocated[0]
        livingspace_unallocated = unallocated[1]
        unallocated_string = self.unallocated_persons_list(
            office_unallocated, "Office")
        unallocated_string += self.unallocated_persons_list(
            livingspace_unallocated, "LivingSpace")
        return unallocated_string

    def unallocated_persons_list(self, unallocated_dict, unallocated_type):
        """Build the string of unallocated person in the dict supplied.

        Arguments:
            unallocated_dict: Dict of persons object
            unallocated_type: String specifying the type allocation

        Returns:
            String: Of formated list of persons info

        """
        unallocated_string = "--Unallocated for {}-- \n\n" \
                             .format(unallocated_type)
        for person_id in unallocated_dict:
            unallocated_string += \
                self.print_person(unallocated_dict[person_id])
        return unallocated_string

    def print_allocation_to_file(self, file_name):
        """Print the room allocation at Amity to file.

        Arguments:
            file_name: path and name to file where information will be printed
        """
        file_obj = open(file_name, "w")
        allocation_string = self.build_allocation_string()
        file_obj.write(allocation_string)
        file_obj.close()

    def build_allocation_string(self):
        """Build the string of the allocation in amity with rooms
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
        """Build the string of a room with the persons in it.

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
        """Build a string of person object printing out the name.

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
