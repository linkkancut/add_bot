class Worker:
    def __init__(self, id, name, phone):
        self.WorkerId = id
        self.Name = name
        self.Phone = phone

    def toTuple(self):
        return (self.WorkerId, self.Name, self.Phone)

    def toString(self):
        return F"{self.WorkerId} - {self.Name} - {self.Phone}"
