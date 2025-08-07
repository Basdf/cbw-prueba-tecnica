class NotFoundError(Exception):
    def __init__(self, message: str = "Resource not found"):
        self.message = message


class DatabaseError(Exception):
    def __init__(self, message: str = "Database error"):
        self.message = message


class WorkerError(Exception):
    def __init__(self, message: str = "Worker error"):
        self.message = message
