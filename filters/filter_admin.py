from data.config import ADMINS


def isAdmin(userId: int):
    if userId in ADMINS:
        return True
    return False
