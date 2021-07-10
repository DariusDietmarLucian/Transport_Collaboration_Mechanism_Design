class Location:

    def __init__(self, id, x, y):
        self.id = int(id)
        self.x = int(x)
        self.y = int(y)

    """
    *************
    ***GETTERS***
    *************
    """

    def get_id(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    """
    **************
    ***CONFORMS***
    **************
    """

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __hash__(self):
        return hash(('id', self.id))
