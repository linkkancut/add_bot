from .ms import Group
import sqlite3


class GroupRepository:

    def Add(db: sqlite3.Connection, group: Group):
        try:
            if(group.IsSelected == "yes"):
                countOfYes = GroupRepository.CountOfYes(db)
                if(countOfYes != 0):
                    return Exception("One Group is yes!")
            command = "INSERT INTO groups(groupId,Name,Selected) VALUES(?,?,?)"
            db.execute(command, group.toTuple())
            return True
        except Exception as err:
            return err

    def Delete(db: sqlite3.Connection, group: Group):
        try:
            command = "DELETE FROM groups WHERE groupId=?"
            db.execute(command, F"{group.GroupId}")
            return True
        except Exception as err:
            return err

    def DeleteById(db: sqlite3.Connection, id):
        try:
            command = "DELETE FROM groups WHERE groupId=?"
            db.execute(command, F"{id}")
            return True
        except Exception as err:
            return err

    def Edit(db: sqlite3.Connection, group: Group):
        try:
            if(group.IsSelected == "yes"):
                countOfYes = GroupRepository.CountOfYes(db)
                if(countOfYes != 0):
                    return Exception("One Group is yes!")
            command = "UPDATE groups SET Name=?, Selected=? WHERE groupId=?"
            g = (group.Name, group.IsSelected, group.GroupId)
            db.execute(command, g)
            return True
        except Exception as err:
            return err

    def SelectById(db: sqlite3.Connection, id: int):
        try:
            command = "SELECT * FROM groups WHERE groupId=?"
            result = db.execute(command, F"{id}").fetchone()
            return Group(result[0], result[1], result[2])
        except Exception as err:
            return err

    def SelectAll(db: sqlite3.Connection):
        try:
            command = "SELECT * FROM groups"
            result = db.execute(command).fetchall()
            groups = []
            for group in result:
                groups.append(Group(group[0], group[1], group[2]))
            return groups
        except Exception as err:
            return err

    def CountOfYes(db):
        groups = GroupRepository.SelectAll(db)
        countOfYes = 0
        for group in groups:
            if group.IsSelected == "yes":
                countOfYes += 1
        return countOfYes

    def Commit(db: sqlite3.Connection):
        try:
            db.commit()
        except Exception as err:
            return err
