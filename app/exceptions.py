class Error(Exception):
    """Base class for all other exception"""
    pass


class RoomIsFullError(Error):
    """Raise when person is added to a room which is full"""
    pass


class PersonNotInRoomError(Error):
    """Raise when person not in room is accessed"""
    pass


class PersonNotFellowError(Error):
    """Raise when A Fellow Action is performed on Person Not a Fellow"""
    pass


class RoomGenderDiffError(Error):
    """Raise when room and person Gender don't match"""
    pass


class PersonInRoomError(Error):
    """Person already in Room"""
    pass
