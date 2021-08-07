class Group:
    def __init__(self, id, name, selected):
        self.GroupId = id
        self.Name = name
        self.IsSelected = selected

    def toTuple(self):
        return (self.GroupId, self.Name, self.IsSelected)
