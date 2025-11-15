class InvalidCommandError(Exception):
    pass


class NotFoundError(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class InvalidDataError(Exception):
    pass


class EmptyDataError(Exception):
    pass


class IncorrectNoteFormatError(Exception):
    def __init__(self, message: str = "Incorrect note format.") -> None:
        super().__init__(message)
