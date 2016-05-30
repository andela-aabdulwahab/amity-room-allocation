"""

usage:
    docopt_test.py create_room (<room_name> <room_type> [-g=RG])...
    docopt_test.py add_person <first_name> <last_name> <gender> <person_type> [-w=WA]
    docopt_test.py relocate_person <person_identifier> <new_room_name>
    docopt_test.py delete_room <room_name>
    docopt_test.py delete_person <person_id>
    docopt_test.py print_allocation [-o=FN]
    docopt_test.py print_unallocated [-o=FN]
    docopt_test.py print_room <room_name>
    docopt_test.py save_state [-b=SQLD]
    docopt_test.py load_state <db_path>

option:
   -help -h                               Geting help on using the program
   -g RG, --rgender=RG                    To specify gender of Occupant of a living room
   -w WA, --wants_accom=WA                 An option argument to specify that person
                                          want accomodation
   -o FN, --option=FN                     Optional file name when printing to file
   -b SQLD --db=SQLD                      Database to load from the path provided

"""
from docopt import docopt
import pickle
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.
    getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from app.allocation_db import AllocationDb
from app.amity import Amity
from app.exceptions import PersonNotFellowError
from app.fellow import Fellow
from app.livingspace import LivingSpace
from app.office import Office
from app.roomallocation import RoomAllocation
from app.staff import Staff


def load_state():
    file_path = "roomallocation.p"
    if os.path.isfile(file_path):
        amity_object = pickle.load(open(file_path, "rb"))
        return RoomAllocation(amity_object)
    else:
        amity_object = Amity()
        return RoomAllocation(amity_object)


def save_state(room_allocation_obj):
    file_path = "roomallocation.p"
    pickle.dump(room_allocation_obj.amity, open(file_path, "wb"))


def add_person(args):
    first_name = args["<first_name>"]
    last_name = args["<last_name>"]
    gender = args["<gender>"]
    person_type = args["<person_type>"]
    wants_accom = "N"
    is_fellow = False
    if args["--wants_accom"]:
        wants_accom = args["--wants_accom"]
    name = first_name + " " + last_name
    roomallocation = load_state()
    person_type = person_type.lower()
    if person_type == "fellow":
        person = Fellow(name, gender, wants_accom)
        is_fellow = True
    elif person_type == "staff":
        person = Staff(name, gender)
    else:
        return "Invalid type: person can be fellow or staff"
    roomallocation.create_person(person)
    save_state(roomallocation)
    rooms = person.room_name
    message = ""
    if rooms.get('office'):
        message += first_name + " allocated to Office " + rooms.get('office') \
                              + "\n"
    else:
        message += "No available Office to allocate " + first_name + "\n"
    if is_fellow and rooms.get('livingroom'):
        message += first_name + " allocated to Living Room" \
                              + rooms.get('livingroom') + "\n"
    elif is_fellow:
        message += "No available Living Space to allocate " + first_name + "\n"
    return message


def create_room(args):
    rooms = get_room_values(args)
    roomallocation = load_state()
    room_id = []
    message = "Room(s) created with Id: \n"
    for i in range(len(rooms)):
        room_name = rooms[i][0]
        room_type = rooms[i][1]
        if room_type == "livingroom":
            gender = rooms[i][2]
            room = LivingSpace(room_name, gender)
            roomallocation.create_room(room)
            room_id = room.get_id()
        elif room_type == 'office':
            room = Office(room_name)
            roomallocation.create_room(room)
            room_id = room.get_id()
        else:
            room_id = None
        if room_id:
            message += room_id + "(" + room_type + ")\n"
        else:
            message += "Invalid room type for "+
    save_state(roomallocation)
    return room_id


def relocate_person(person_identifier, new_room_name):
    new_room_name = new_room_name.lower()
    roomallocation = load_state()
    status = roomallocation.rellocate_person(person_identifier, new_room_name)
    save_state(roomallocation)


def print_allocation(file_name=False):
    allocation = load_state()

    if file_name:
        allocation.print_allocation_to_file(file_name)
        print(file_name+" Created")
    else:
        print(allocation.build_allocation_string())

def print_unallocated(file_name=False):
    allocation = load_state()
    if file_name:
        allocation.print_unallocated_to_file(file_name)
        print(file_name+" Created")
    else:
        print(allocation.build_unallocation_string())

def print_room(room_name):
    allocation = load_state()
    print(allocation.print_room(room_name))

def save_state_to_db(db_path=False):
    if not db_path:
        db_path = "roomallocation.db"
    roomallocation = load_state()
    db = AllocationDb(db_path)
    roomallocation.save_to_database(db)
    print("Data Successfully saved to database")

def load_from_database(db_path):
    roomallocation = load_state()
    db = AllocationDb(db_path)
    roomallocation.load_from_database(db)
    save_state(roomallocation)
    print("Application State reload from database")


def get_room_values(args):
    j = 0
    rooms = []
    for i in range(len(args["<room_name>"])):
        room_name = args["<room_name>"][i]
        room_type = args["<room_type>"][i].lower()
        if room_type == "livingroom":
            gender = args["--rgender"][j]
            j += 1
            rooms.append([room_name, room_type, gender])
        else:
            rooms.append([room_name, room_type])
    return rooms

def delete(del_id, del_type):
    roomallocation = load_state()
    if del_type == "person":
        status = roomallocation.remove_person(del_id)
    else:
        status = roomallocation.remove_room(del_id)
    if status == 14:
        print(del_id+ " not a valid Id")
    else:
        print(del_id+" Deleted from Amity")
    save_state(roomallocation)







def main(args):

    if args["add_person"]:
        print(add_person(args))
    elif args["create_room"]:
        status = create_room(args)
        print("Room(s) Created with Id :")
        for i in range(len(status)):
            print(status[i])
    elif args["relocate_person"]:
        person_identifier = args["<person_identifier>"]
        new_room_name = args["<new_room_name>"]
        relocate_person(person_identifier, new_room_name)
    elif args["print_allocation"]:
        if args["--option"]:
            print_allocation(args["--option"])
        else:
            print_allocation()
    elif args["print_unallocated"]:
        if args["--option"]:
            print_unallocated(args["--option"])
        else:
            print_unallocated()
    elif args["print_room"]:
        print_room(args["<room_name>"][0])
    elif args["load_state"]:
        load_from_database(args["<db_path>"])
    elif args["save_state"]:
        if args["--db"]:
            save_state_to_db(args["--db"])
        else:
            save_state_to_db()
    elif args["delete_room"]:
        delete(args["<room_name>"][0], 'room')
    elif args["delete_person"]:
        delete(args["<person_id>"], 'person')
    else:
        print("use the usage instruction below to build command")

if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
