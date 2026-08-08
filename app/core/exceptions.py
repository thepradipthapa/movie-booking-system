class NotFoundError(Exception):
    """Base class for 'the requested resource does not exist' errors."""


class ScreenNotFoundError(NotFoundError):
    pass


class DuplicateSeatError(Exception):
    """Raised when a seat with the same (screen_id, row_label, seat_number) already exists."""