import sqlite3


class Context:
    db = None

    def __init__(self, name):
        if(self.db == None):
            self.db = sqlite3.connect(name)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS groups(groupId INTEGER, Name Text, Selected TEXT)")
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS members(memberId INTEGER, Name Text, Added TEXT)")
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS workers(workerId INTEGER, Name Text, Phone TEXT)")
        self.db.commit()

    def getDB(self):
        return self.db
