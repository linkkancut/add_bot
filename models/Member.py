class Member:
    def __init__(self, id, name, added):
        self.MemberId = id
        self.Name = name
        self.IsAdded = added

    def toTuple(self):
        return (self.MemberId, self.Name, self.IsAdded)

    def toString(self):
        return F"{self.MemberId} - {self.Name} - {self.IsAdded}"
