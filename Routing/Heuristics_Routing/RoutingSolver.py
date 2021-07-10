"""
Based on:
Renaud, J., Boctor, F.F. and Ouenniche, J., 2000.
A heuristic for the pickup and delivery traveling salesman problem. Computers & Operations Research, 27(9), pp.905-916.
"""


from Routing.Heuristics_Routing.RoutingInserter import RoutingInserter
from Routing.Heuristics_Routing.RoutingOptimizer import RoutingOptimizer


class RoutingSolver:

    def __init__(self, graph):
        self.graph = graph

        self.routes = {}

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __select_max_distance_request(graph, depot, requests):
        max_distance = 0
        selected_request = None

        for request in requests:
            pickup_distance = graph.calculate_node_distance(node=depot, other_node=request.get_pickup_node())
            dir_distance = request.get_distance()
            delivery_distance = graph.calculate_node_distance(node=request.get_delivery_node(), other_node=depot)

            distance = pickup_distance + dir_distance + delivery_distance

            if distance > max_distance:
                max_distance = distance
                selected_request = request

        return selected_request

    @staticmethod
    def __solve_from_initial_route(graph, route, requests):

        inserter = RoutingInserter(graph=graph)
        optimizer = RoutingOptimizer(graph=graph)

        for request in requests:
            route = inserter.calculate_double_insert_single(route=route, request=request)

        return optimizer.optimize(route, requests, 3)

    @staticmethod
    def __route_requests(graph, requests):

        if len(requests) == 0:
            return []

        requests.sort(key=lambda rqst: rqst.get_distance())
        first_rqst = requests[-1]
        route = [first_rqst.get_pickup_node(), first_rqst.get_delivery_node(), first_rqst.get_pickup_node()]

        remaining_requests = [request for request in requests if request.id != first_rqst.id]
        return RoutingSolver.__solve_from_initial_route(graph=graph, route=route, requests=remaining_requests)

    @staticmethod
    def __route_requests_with_depot(graph, requests, depot):

        if len(requests) == 0:
            return [depot, depot]

        selected_request = RoutingSolver.__select_max_distance_request(graph=graph, depot=depot, requests=requests)
        route = [depot, selected_request.get_pickup_node(), selected_request.get_delivery_node(), depot]

        remaining_requests = [request for request in requests if request.id != selected_request.id]
        return RoutingSolver.__solve_from_initial_route(graph=graph, route=route, requests=remaining_requests)

    """
    ***********
    ***PUBLIC***
    ***********
    """

    def solve(self, requests, depot=None):

        key = self.get_route_key(requests=requests, depot=depot)
        graph = self.get_graph()

        if key not in self.routes:
            if depot is None:
                self.routes[key] = self.__route_requests(graph=graph, requests=requests)
            else:
                self.routes[key] = self.__route_requests_with_depot(graph=graph, requests=requests, depot=depot)

        return self.routes[key]

    """
    *************
    ***GETTERS***
    *************
    """

    def get_graph(self):
        return self.graph

    def get_route_key(self, requests, depot=None):
        if depot is None:
            return frozenset([request.get_id() for request in requests])
        else:
            return frozenset([request.get_id() for request in requests] + [depot.get_id()])
