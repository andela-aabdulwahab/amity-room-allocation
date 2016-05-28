class Error(Exception):
    """Base class for all other exception"""
    pass


class RoomIsFullError(Exception):
    """Raised when person is added to a room which is full"""
    pass
