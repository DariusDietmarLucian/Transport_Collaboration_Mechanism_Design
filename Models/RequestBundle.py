from Models.Graph import Graph


class RequestBundle:

    def __init__(self, requests, solver, graph):
        self.requests = requests
        self.solver = solver
        self.graph = graph

        self.id = None
        self.separation_values = {}
        self.centroid = None
        self.radius = None
        self.density = None
        self.tour_length = None

        self.__set_up()

    def __set_up(self):
        self.id = self.get_id()

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __calc_request_to_point_distance(request, point):

        distance = 0

        p_node = request.get_pickup_node()
        distance += Graph.calculate_point_distance(point=p_node.get_coordinates(), other_point=point)

        d_node = request.get_delivery_node()
        distance += Graph.calculate_point_distance(point=d_node.get_coordinates(), other_point=point)

        return distance

    @staticmethod
    def __calc_average_distance_request_nodes_to_point(requests, point):

        distances = 0
        for request in requests:
            distances += RequestBundle.__calc_request_to_point_distance(request=request, point=point)

        return distances / (2 * (len(requests)))

    @staticmethod
    def __calc_centroid(requests):

        total_distances = sum([request.get_distance() for request in requests])

        centroid_x = 0
        centroid_y = 0

        for request in requests:
            centroid_x += request.get_distance() / total_distances * request.get_center()[0]
            centroid_y += request.get_distance() / total_distances * request.get_center()[1]

        return centroid_x, centroid_y

    @staticmethod
    def __calc_radius(requests, centroid):
        radius = RequestBundle.__calc_average_distance_request_nodes_to_point(requests=requests, point=centroid)
        return radius

    @staticmethod
    def __calc_density(requests, centroid):
        average_dir_dist = sum([request.get_distance() for request in requests]) / len(requests)
        max_rqst_cntr_dist = max(
            [RequestBundle.__calc_request_to_point_distance(request=request, point=centroid) for request in requests])

        density = average_dir_dist / max_rqst_cntr_dist
        return density

    @staticmethod
    def __calc_tour_length(graph, requests, solver):
        if len(requests) == 0:
            return 0

        route = solver.solve(requests=requests)
        return graph.calculate_route_distance(route=route)

    @staticmethod
    def calc_separation_value(bundle, other_bundle):
        centroid = bundle.get_centroid()
        other_centroid = other_bundle.get_centroid()
        distance = Graph.calculate_point_distance(point=centroid, other_point=other_centroid)

        radius = bundle.get_radius()
        other_radius = other_bundle.get_radius()
        max_radius = max(radius, other_radius)

        return distance / max_radius

    """
    *************
    ***GETTERS***
    *************
    """

    def get_requests(self):
        return self.requests

    def get_graph(self):
        return self.graph

    def get_solver(self):
        return self.solver

    def get_id(self):
        if self.id is None:
            requests = self.get_requests()
            self.id = frozenset([request.id for request in requests])

        return self.id

    def get_separation_value(self, other_bundle):
        if other_bundle.get_id() not in self.separation_values:
            self.separation_values[other_bundle.get_id()] = self.calc_separation_value(bundle=self,
                                                                                       other_bundle=other_bundle)

        return self.separation_values[other_bundle.get_id()]

    def get_centroid(self):
        if self.centroid is None:
            requests = self.get_requests()
            self.centroid = self.__calc_centroid(requests=requests)

        return self.centroid

    def get_radius(self):
        if self.radius is None:
            requests = self.get_requests()
            centroid = self.get_centroid()
            self.radius = self.__calc_radius(requests=requests, centroid=centroid)

        return self.radius

    def get_density(self):
        if self.density is None:
            requests = self.get_requests()
            centroid = self.get_centroid()
            self.density = self.__calc_density(requests=requests, centroid=centroid)

        return self.density

    def get_tour_length(self):
        if self.tour_length is None:
            graph = self.get_graph()
            requests = self.get_requests()
            solver = self.get_solver()
            self.tour_length = self.__calc_tour_length(graph=graph, requests=requests, solver=solver)

        return self.tour_length

    """
    **************
    ***CONFORMS***
    **************
    """

    def __eq__(self, other):
        return self.get_id() == other.get_id()
