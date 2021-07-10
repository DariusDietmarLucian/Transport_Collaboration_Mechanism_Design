"""
Overview of the used routing strategies and references:
https://developers.google.com/optimization/routing/routing_options
"""


import numpy as np

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from Routing.RoutingManagerEnums import SolutionStrategy


class GoogleRoutingSolver:

    def __init__(self, distance_matrix, pickup_deliveries, depot_index, strategy, initial_route=None):
        self.distance_matrix = distance_matrix
        self.pickup_deliveries = pickup_deliveries
        self.depot_index = depot_index
        self.strategy = strategy
        self.initial_route = initial_route

        self.capacity = None

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __get_index_route(solution, routing, manager):
        index_route = []
        index = routing.Start(0)

        while not routing.IsEnd(index):
            index_route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))

        return index_route

    """
    ************
    ***PUBLIC***
    ************
    """

    def solve(self):

        distance_matrix = self.get_distance_matrix()
        depot_index = self.get_depot_index()
        pickup_deliveries = self.get_pickup_deliveries()
        initial_route = self.get_initial_route()
        capacity = self.get_capacity()

        length = np.shape(distance_matrix)[0]
        manager = pywrapcp.RoutingIndexManager(length, 1, int(depot_index))
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return round(
                distance_matrix[from_node][to_node] * 100)  # scale and round because or-tools work with integers

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        dimension_name = "Distance"
        routing.AddDimension(
            transit_callback_index,
            0,
            capacity,
            True,
            dimension_name
        )
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        for request in pickup_deliveries:
            pickup_index = manager.NodeToIndex(request[0])
            delivery_index = manager.NodeToIndex(request[1])
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            routing.solver().Add(
                distance_dimension.CumulVar(pickup_index) <=
                distance_dimension.CumulVar(delivery_index)
            )

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()

        if self.strategy == SolutionStrategy.GOOGLE_LOCAL_CHEAPEST_INSERTION:
            search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_INSERTION

        elif self.strategy == SolutionStrategy.GOOGLE_PATH_CHEAPEST_ARC:
            search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

        elif self.strategy == SolutionStrategy.GOOGLE_PARALLEL_CHEAPEST_INSERTION:
            search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

        if initial_route is None:
            solution = routing.SolveWithParameters(search_parameters)
        else:
            initial_assignment = routing.ReadAssignmentFromRoutes([initial_route], True)
            solution = routing.SolveFromAssignmentWithParameters(initial_assignment, search_parameters)

        return self.__get_index_route(solution=solution, routing=routing, manager=manager)

    """
    *************
    ***GETTERS***
    *************
    """

    def get_distance_matrix(self):
        return self.distance_matrix

    def get_depot_index(self):
        return self.depot_index

    def get_pickup_deliveries(self):
        return self.pickup_deliveries

    def get_initial_route(self):
        return self.initial_route

    def get_capacity(self):
        if self.capacity is None:
            self.capacity = int(sum([x for row in self.get_distance_matrix() for x in row])) * 10000

        return self.capacity
