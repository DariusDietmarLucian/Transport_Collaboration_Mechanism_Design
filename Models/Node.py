from Models.Location import Location
from Models.Site import Site


class Node:

    def __init__(self, id, site):
        self.id = int(id)
        self.site = site

    """
    *************
    ***GETTERS***
    *************
    """
    def get_id(self):
        return self.id

    def get_site(self):
        return self.site

    def get_location(self):
        return self.get_site().get_location()

    def get_area_id(self):
        return self.get_site().get_area_id()

    def get_x(self):
        return self.get_site().get_location_x()

    def get_y(self):
        return self.get_site().get_location_y()

    def get_coordinates(self):
        return self.get_x(), self.get_y()

    def get_location_id(self):
        return self.get_site().get_location_id()

    """
    ************
    ***CODING***
    ************
    """

    @classmethod
    def decode(cls, node_dic):
        id = node_dic["id"]
        x = node_dic["x"]
        y = node_dic["y"]
        location_id = node_dic["location_id"]
        area_id = node_dic["area_id"]
        location = Location(id=location_id, x=x, y=y)
        site = Site(location=location, area_id=area_id)
        return cls(id=id, site=site)

    def encode(self):
        node_dic = {}
        node_dic["id"] = self.get_id()
        node_dic["x"] = self.get_x()
        node_dic["y"] = self.get_y()
        node_dic["location_id"] = self.get_location_id()
        node_dic["area_id"] = self.get_area_id()
        return node_dic
