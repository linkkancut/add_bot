from .ms import Worker
import sqlite3


class WorkerRepository:

    def Add(db: sqlite3.Connection, worker: Worker):
        try:
            command = "INSERT INTO workers(workerId,Name,Phone) VALUES(?,?,?)"
            db.execute(command, worker.toTuple())
            return True
        except Exception as err:
            return err

    def Delete(db: sqlite3.Connection, worker: Worker):
        try:
            command = "DELETE FROM workers WHERE workerId=?"
            db.execute(command, F"{worker.WorkerId}")
            return True
        except Exception as err:
            return err

    def DeleteById(db: sqlite3.Connection, id):
        try:
            command = "DELETE FROM workers WHERE workerId=?"
            db.execute(command, F"{id}")
            return True
        except Exception as err:
            return err

    def Edit(db: sqlite3.Connection, worker: Worker):
        try:
            command = "UPDATE workers SET Name=?, Phone=? WHERE workerId=?"
            w = (worker.Name, worker.Phone, worker.WorkerId)
            db.execute(command, w)
            return True
        except Exception as err:
            return err

    def SelectById(db: sqlite3.Connection, id: int):
        try:
            command = "SELECT * FROM workers WHERE workerId=?"
            result = db.execute(command, F"{id}").fetchone()
            return Worker(result[0], result[1], result[2])
        except Exception as err:
            return err

    def SelectAll(db: sqlite3.Connection):
        try:
            command = "SELECT * FROM workers"
            result = db.execute(command).fetchall()
            workers = []
            for worker in result:
                workers.append(Worker(worker[0], worker[1], worker[2]))
            return workers
        except Exception as err:
            return err

    def SelectByPhone(db: sqlite3.Connection, phone):
        try:
            command = "SELECT * FROM workers WHERE Phone=?"
            result = db.execute(command, (phone,)).fetchone()
            return Worker(result[0], result[1], result[2])
        except Exception as err:
            return err

    def Commit(db: sqlite3.Connection):
        try:
            db.commit()
        except Exception as err:
            return err
