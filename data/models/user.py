class User:
    def __init__(self, id: int, first_name: str, last_name: str, username: str, date: int, isBlocked: bool):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.date = date
        self.isBlocked = isBlocked

    def __str__(self):
        return (f"{self.id} {self.first_name} {self.last_name} {self.username} "
                f"{self.date.__format__('dd MM yyy')} {self.isBlocked}")
