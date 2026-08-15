class NotFoundError(Exception):
    """Base class for 'the requested resource does not exist' errors."""


class ScreenNotFoundError(NotFoundError):
    pass


class MovieNotFoundError(NotFoundError):
    pass


class DuplicateSeatError(Exception):
    """Raised when a seat with the same (screen_id, row_label, seat_number) already exists."""
    

class DuplicateShowError(Exception):
    """Raised when a show with the same (screen_id, start_time) already exists."""
    
    
class EmailAlreadyExistsError(Exception):
    """Raised when signup is attempted with an email that's already registered."""