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