class Site:

    def __init__(self, location, area_id):
        self.location = location
        self.area_id = area_id

    """
    *************
    ***GETTERS***
    *************
    """

    def get_location(self):
        return self.location

    def get_location_id(self):
        return self.get_location().get_id()

    def get_location_x(self):
        return self.get_location().get_x()

    def get_location_y(self):
        return self.get_location().get_y()

    def get_area_id(self):
        return self.area_id
