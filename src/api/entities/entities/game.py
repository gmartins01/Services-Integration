import uuid
from datetime import datetime


class Game:
    def __init__(self, date, id=None, created_on=None, updated_on=None):
        self.id = id or uuid.uuid4()
        self.date = date
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()
