class WrongKeysError(Exception):
    def __init__(self, keys, wrong_keys):
        self.message = {
            "valid_options": keys,
            "received_options": wrong_keys
        }
        
        super().__init__(self.message)


class NotFoundDataError(Exception):
    ...

class NotStringError(Exception):
    ...

class NotIntegerError(Exception):
    ...

class EmptyStringError(Exception):
    ...

class MissingKeyError(Exception):
    def __init__(self, keys, wrong_keys):
        self.message = {
            "required_keys": keys,
            "missing_key": wrong_keys
        }
        
        super().__init__(self.message)

class DateError(Exception):
    ...

class PathOwnerError(Exception):
    ...

class EmailAlreadyExists(Exception):
    ...

class UsernameAlreadyExists(Exception):
    ...

class PasswordConfirmationDontMatch(Exception):
    ...