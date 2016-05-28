from app.room import Room


class Office(Room):
    """ object container for living room
    Inherits:
        Rooms

    """

    def __init__(self, name):
        """Calls the room constructor with size equals 6

        """
        super().__init__(name, 6)
