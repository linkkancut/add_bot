class Group:
    def __init__(self, id, name, selected):
        self.GroupId = id
        self.Name = name
        self.IsSelected = selected

    def toTuple(self):
        return (self.GroupId, self.Name, self.IsSelected)

    def toString(self):
        return F"{self.GroupId} - {self.Name} - {self.IsSelected}"


class Member:
    def __init__(self, id, name, added):
        self.MemberId = id
        self.Name = name
        self.IsAdded = added

    def toTuple(self):
        return (self.MemberId, self.Name, self.IsAdded)

    def toString(self):
        return F"{self.MemberId} - {self.Name} - {self.IsAdded}"


class Worker:
    def __init__(self, id, name, phone):
        self.WorkerId = id
        self.Name = name
        self.Phone = phone

    def toTuple(self):
        return (self.WorkerId, self.Name, self.Phone)

    def toString(self):
        return F"{self.WorkerId} - {self.Name} - {self.Phone}"
