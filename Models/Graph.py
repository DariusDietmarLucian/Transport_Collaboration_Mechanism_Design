import numpy as np
import random
import math


class Graph:

    def __init__(self, locations):
        self.locations = locations

        self.distance_matrix = None
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __comp_eucl_matrix(locations):
        distances = np.zeros(shape=(len(locations), len(locations)))
        locations.sort(key=lambda loc: loc.get_id())

        for from_counter, from_loc in enumerate(locations):
            for to_counter, to_loc in enumerate(locations):
                distance = Graph.calculate_point_distance(point=(from_loc.get_x(), from_loc.get_y()),
                                                          other_point=(to_loc.get_x(), to_loc.get_y()))
                distances[from_counter][to_counter] = distance

        return distances

    """
    ************
    ***PUBLIC***
    ************
    """

    @staticmethod
    def calculate_point_distance(point, other_point):
        return math.hypot((point[0] - other_point[0]), (point[1] - other_point[1]))

    def calculate_route_distance(self, route):
        total_distance = 0
        for i in range(len(route) - 1):
            distance = self.calculate_node_distance(node=route[i], other_node=route[i + 1])
            total_distance += distance

        return total_distance

    def calculate_node_distance(self, node, other_node):
        distance_matrix = self.get_distance_matrix()
        return distance_matrix[node.get_location_id()][other_node.get_location_id()]

    def calculate_request_distance(self, request, other_request, d_sum=True):
        pickup_distance = self.calculate_node_distance(request.get_pickup_node(), other_request.get_pickup_node())
        delivery_distance = self.calculate_node_distance(request.get_delivery_node(), other_request.get_delivery_node())

        if d_sum:
            return pickup_distance + delivery_distance
        else:
            return max(pickup_distance, delivery_distance)

    def calculate_request_node_distance(self, request, node, d_sum=True):
        pickup_distance = self.calculate_node_distance(request.get_pickup_node(), node)
        delivery_distance = self.calculate_node_distance(request.get_delivery_node(), node)

        if d_sum:
            return pickup_distance + delivery_distance
        else:
            return max(pickup_distance, delivery_distance)

    def create_random_point(self):
        min_x = self.get_min_x()
        max_x = self.get_max_x()
        min_y = self.get_min_y()
        max_y = self.get_max_y()

        return random.randrange(min_x, max_x), random.randrange(min_y, max_y)

    """
    *************
    ***GETTERS***
    *************
    """

    def get_locations(self):
        return self.locations

    def get_distance_matrix(self):
        if self.distance_matrix is None:
            locations = self.get_locations()
            self.distance_matrix = self.__comp_eucl_matrix(locations=locations)

        return self.distance_matrix

    def get_min_x(self):
        if self.min_x is None:
            locations = self.get_locations()
            self.min_x = min([loc.get_x() for loc in locations])

        return self.min_x

    def get_max_x(self):
        if self.max_x is None:
            locations = self.get_locations()
            self.max_x = max([loc.get_x() for loc in locations])

        return self.max_x

    def get_min_y(self):
        if self.min_y is None:
            locations = self.get_locations()
            self.min_y = min([loc.get_y() for loc in locations])

        return self.min_y

    def get_max_y(self):
        if self.max_y is None:
            locations = self.get_locations()
            self.max_y = max([loc.get_y() for loc in locations])

        return self.max_y
