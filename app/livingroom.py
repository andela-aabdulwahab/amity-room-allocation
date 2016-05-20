from app.fellow import Fellow
from app.room import Room


class LivingRoom(Room):

    """ object container for living room
    inherit Room

    instance variable
    gender - gender of allowed occupants

    methods
    get_gender - return the allowed occupants gender
    add_occupant - override that of Room

    __init__
    set the size of the room to 4 by calling the base class
    constructor to 4
    set gender of allowed occupants

    argument
    name - name of the room
    gener - the gender allowed for the room
    """

    def __init__(self, name, gender):
        super().__init__(name, 4)
        self.gender = gender

    def add_occupant(self, person_obj):
        """ override the Room add_occupant
        determining if is a fellow or gender

        arguments
        person - instance person_object

        return status code
           1 - successful
           5 - person is not a fellow
           4 - Gender not in room
        """
        if not isinstance(person_obj, Fellow):
            return 5
        elif self.gender != person_obj.gender:
            return 4
        else:
            return super().add_occupant(person_obj)

    def get_gender(self):
        """ return the gender allowed for room"""
        return self.gender
