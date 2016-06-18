import sqlite3

from app.fellow import Fellow
from app.livingspace import LivingSpace
from app.office import Office
from app.staff import Staff


class AllocationDb():
    """ Create the interface for communication between
    room allocation and the database. Uses an instance of
    SQLite3 to manage Sqlite database

    Attributes
        db: the database connection
        cursor: the db cursor for databse actions
        error_log: saves the db error if one happens

    """

    def __init__(self, db_path):
        """create a sqlite3 database object in the specified path
        Create the tables for storing application data
        Uses a try block to handle exections that may occur

        Arguments
            db_path: the paths to the database objects to use/create
        """
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.error_log = {}

        self.db.execute(
            '''
            CREATE TABLE IF NOT EXISTS roomallocation_persons(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            person_id VARCHAR(50) NOT NULL,
            person_type VARCHAR(10) NOT NULL,
            name VARCHAR(50) NOT NULL,
            gender CHARACTER(1) NOT NULL,
            want_accomodation CHARACTER(1) NOT NULL,
            office_id INTEGER NULL,
            livingspace_id INTEGER NULL
            );
            ''')

        self.db.execute(
            '''
            CREATE TABLE IF NOT EXISTS roomallocation_rooms(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            room_id VARCHAR(20) NOT NULL,
            room_type VARCHAR(20) NOT NULL,
            name VARCHAR(50) NOT NULL,
            gender CHARACTER(1) NULL
            );
            ''')

    def add_person(self, person_obj):
        """Extract data from the person object and save it into the database.

        Arguments
            person_object: Object to be save into the database

        """
        person_id = person_obj.identifier
        name = person_obj.name
        gender = person_obj.gender
        office_id = ""
        livingspace_id = ""
        want_accomodation = ""

        if person_obj.is_allocated("office"):
                office_id = self.get_db_room_id(person_obj.room_name["office"])
        if isinstance(person_obj, Fellow):
            person_type = "FELLOW"
            want_accomodation = person_obj.wants_accom
            if person_obj.is_allocated("livingspace"):
                livingspace_id = self.get_db_room_id(
                person_obj.room_name["livingspace"])
        else:
            person_type = "STAFF"
        if self.person_in_database(person_id):
            self.update_person((office_id, livingspace_id, person_id))
            return self
        values = (person_id, person_type, name, gender, want_accomodation,
                  office_id, livingspace_id)

        self.db.execute("INSERT INTO roomallocation_persons(person_id, " +
                        "person_type, name, gender, want_accomodation, " +
                        "office_id, livingspace_id) VALUES(?, ?, ?, ?, " +
                        "?, ?, ?)", values)
        self.db.commit()
        return self

    def add_room(self, room_obj):
        """ Extract all information to the database and add it to the database

        Arguments:
            room_obj: Room object that will be added to the database
        """

        room_id = room_obj.get_id()
        name = room_obj.name
        gender = ""
        if isinstance(room_obj, Office):
            room_type = "office"
        else:
            room_type = "livingspace"
            gender = room_obj.gender
        values = (room_id, room_type, name, gender)
        if not self.room_in_database(room_id):
            (self.db.execute("INSERT INTO roomallocation_rooms(room_id, room" +
                             "_type, name, gender) VALUES(?, ?, ?, ?)", values))
            self.db.commit()
        return self

    def room_in_database(self, room_id):
        result = self.cursor.execute("SELECT * FROM roomallocation_rooms WHERE "
                                     +"room_id ='"+room_id+"'")
        row = result.fetchall()
        return len(row) == 1

    def person_in_database(self, person_id):
        result = self.cursor.execute("SELECT * FROM roomallocation_persons "
                                     +"WHERE person_id ='"+person_id+"'")
        row = result.fetchall()
        return len(row) == 1

    def update_person(self, values):
        result = self.cursor.execute("UPDATE roomallocation_persons SET "+
                                     "office_id = ?, livingspace_id = ? WHERE "+
                                     "person_id = ?", values)
        self.db.commit()
        return self

    def get_db_room_id(self, room_id):
        result = self.cursor.execute("SELECT id FROM roomallocation_rooms WHERE"
                                     +" room_id ='"+room_id+"'")
        row = result.fetchone()
        if row:
            return row[0]
        return ""

    def get_room_id(self, db_id):
        result = self.cursor.execute("SELECT room_id FROM roomallocation_rooms "
                                     +"WHERE id ='"+str(db_id)+"'")
        row = result.fetchone()
        return row[0]

    def get_rooms(self):
        """Return all rooms in the database.

        Returns:
            Dict: a dictionary of Room objects
        """
        result = self.cursor.execute("SELECT * FROM roomallocation_rooms")
        rows = result.fetchall()
        rooms = {}
        for row in rows:
            if row[2] == "livingspace":
                rooms[row[1]] = LivingSpace(row[3], row[4])
            elif row[2] == "office":
                rooms[row[1]] = Office(row[3])
        return rooms

    def get_persons(self):
        """ return all persons in the database

        Returns:
            Dict: a dictionary of Person objects
        """
        result = self.cursor.execute("SELECT * FROM roomallocation_persons")
        rows = result.fetchall()
        persons = {}
        for row in rows:
            if row[2] == "FELLOW":
                person = Fellow(row[3], row[4], row[5])
                if row[6] != "":
                    person.room_name["office"] = self.get_room_id(row[6])
                if row[7] != "":
                    person.room_name["livingspace"] = self.get_room_id(row[7])
            elif row[2] == "STAFF":
                person = Staff(row[3], row[4])
                if row[6] != "":
                    person.room_name["office"] = self.get_room_id(row[6])
            person.identifier = row[1]
            persons[row[1]] = person
        return persons
