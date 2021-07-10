from Models.Graph import Graph
from Models.Node import Node


class Request:

    def __init__(self, p_node, d_node):
        self.p_node = p_node
        self.d_node = d_node

        self.id = None
        self.distance = None
        self.center = None

        self.__set_up()

    def __set_up(self):
        self.id = self.get_id()

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __calc_dir_dist(node, other_node):
        return Graph.calculate_point_distance(point=(node.get_coordinates()),
                                              other_point=(other_node.get_coordinates()))

    @staticmethod
    def __calc_center(node, other_node):
        return (node.get_x() + other_node.get_x()) / 2, (node.get_y() + other_node.get_y()) / 2


    """
    *************
    ***GETTERS***
    *************
    """

    def get_id(self):
        if self.id is None:
            self.id = f"{self.get_pickup_node().get_id()}" + "," + f"{self.get_delivery_node().get_id()}"

        return self.id

    def get_pickup_node(self):
        return self.p_node

    def get_delivery_node(self):
        return self.d_node

    def get_center(self):
        if self.center is None:
            pickup_node = self.get_pickup_node()
            delivery_node = self.get_delivery_node()
            self.center = self.__calc_center(node=pickup_node, other_node=delivery_node)

        return self.center

    def get_distance(self):
        if self.distance is None:
            pickup_node = self.get_pickup_node()
            delivery_node = self.get_delivery_node()
            self.distance = self.__calc_dir_dist(node=pickup_node, other_node=delivery_node)

        return self.distance

    """
    ************
    ***CODING***
    ************
    """

    @classmethod
    def decode(cls, request_dic):
        p_node_dic = request_dic["p_node"]
        d_node_dic = request_dic["d_node"]
        p_node = Node.decode(node_dic=p_node_dic)
        d_node = Node.decode(node_dic=d_node_dic)
        return cls(p_node=p_node, d_node=d_node)

    def encode(self):
        request_dic = {}
        request_dic["p_node"] = self.get_pickup_node().encode()
        request_dic["d_node"] = self.get_delivery_node().encode()
        return request_dic

    """
    **************
    ***CONFORMS***
    **************
    """

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __hash__(self):
        return hash(('id', self.get_id()))
