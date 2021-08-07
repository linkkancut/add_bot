from .ms import Member
import sqlite3


class MemberRepository:

    def Add(db: sqlite3.Connection, member: Member):
        try:
            command = "INSERT INTO members(memberId,Name,Added) VALUES(?,?,?)"
            db.execute(command, member.toTuple())
            return True
        except Exception as err:
            return err

    def Delete(db: sqlite3.Connection, member: Member):
        try:
            command = "DELETE FROM members WHERE memberId=?"
            db.execute(command, F"{member.MemberId}")
            return True
        except Exception as err:
            return err

    def DeleteById(db: sqlite3.Connection, id):
        try:
            command = "DELETE FROM members WHERE memberId=?"
            db.execute(command, F"{id}")
            return True
        except Exception as err:
            return err

    def Edit(db: sqlite3.Connection, member: Member):
        try:
            command = "UPDATE members SET Name=?, Added=? WHERE memberId=?"
            m = (member.Name, member.IsAdded, member.MemberId)
            db.execute(command, m)
            return True
        except Exception as err:
            return err

    def SelectById(db: sqlite3.Connection, id: int):
        try:
            command = "SELECT * FROM members WHERE memberId=?"
            result = db.execute(command, F"{id}").fetchone()
            return Member(result[0], result[1], result[2])
        except Exception as err:
            return err

    def SelectAll(db: sqlite3.Connection):
        try:
            command = "SELECT * FROM members"
            result = db.execute(command).fetchall()
            members = []
            for member in result:
                members.append(Member(member[0], member[1], member[2]))
            return members
        except Exception as err:
            return err

    def Commit(db: sqlite3.Connection):
        try:
            db.commit()
        except Exception as err:
            return err
