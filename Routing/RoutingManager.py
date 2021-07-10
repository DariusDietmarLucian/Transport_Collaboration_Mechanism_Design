from Routing.Google_Routing.GoogleRoutingSolver import GoogleRoutingSolver
from Routing.Google_Routing.GoogleRoutingTranslator import GoogleRoutingTranslator

from Routing.Heuristics_Routing.RoutingOptimizer import RoutingOptimizer
from Routing.Heuristics_Routing.RoutingInserter import RoutingInserter
from Routing.Heuristics_Routing.RoutingRemover import RoutingRemover
from Routing.Heuristics_Routing.RoutingSolver import RoutingSolver

from Routing.InsertionStrategy import InsertionStrategy
from Routing.RemovalStrategy import RemovalStrategy
from Routing.SolutionStrategy import SolutionStrategy


class RoutingManager:

    def __init__(self, graph, depot, configuration):
        self.graph = graph
        self.depot = depot
        self.configuration = configuration

        self.solutions = {}

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __calc_google_route(graph, depot, requests, strategy):

        translator = GoogleRoutingTranslator(depot=depot, requests=requests, graph=graph)
        transl_dist_matrix, transl_depot_index, transl_pickup_deliveries = translator.translate_matrix_depot_requests()

        solver = GoogleRoutingSolver(distance_matrix=transl_dist_matrix, pickup_deliveries=transl_pickup_deliveries,
                                     depot_index=transl_depot_index, strategy=strategy)

        transl_route = solver.solve()
        return translator.translate_route_from_google(transl_route)

    @staticmethod
    def __calc_google_route_insertion(graph, depot, requests, route, strategy):

        translator = GoogleRoutingTranslator(depot=depot, requests=requests, graph=graph)
        transl_dist_matrix, transl_depot_index, transl_pickup_deliveries = translator.translate_matrix_depot_requests()

        transl_initial_route = translator.translate_route_to_google(route)

        if strategy == InsertionStrategy.CHEAP_INSERTION_GOOGLE_LOCAL_CHEAPEST_ARC:
            sol_strategy = SolutionStrategy.GOOGLE_LOCAL_CHEAPEST_INSERTION

        elif strategy == InsertionStrategy.CHEAP_INSERTION_GOOGLE_PATH_CHEAPEST_ARC:
            sol_strategy = SolutionStrategy.GOOGLE_PATH_CHEAPEST_ARC

        elif strategy == InsertionStrategy.CHEAP_INSERTION_GOOGLE_PARALLEL_CHEAPEST_INSERTION:
            sol_strategy = SolutionStrategy.GOOGLE_PARALLEL_CHEAPEST_INSERTION

        solver = GoogleRoutingSolver(distance_matrix=transl_dist_matrix, pickup_deliveries=transl_pickup_deliveries,
                                     depot_index=transl_depot_index, strategy=sol_strategy,
                                     initial_route=transl_initial_route)

        transl_route = solver.solve()
        return translator.translate_route_from_google(transl_route)

    @staticmethod
    def optimize(graph, route, requests, k_opt):
        optimizer = RoutingOptimizer(graph=graph)
        return optimizer.optimize(route=route, requests=requests, k_opt=k_opt)

    @staticmethod
    def __calc_route(graph, depot, requests, strategy):

        if len(requests) == 0:
            return [depot, depot]

        if strategy == SolutionStrategy.DOUBLE_INSERTION:
            solver = RoutingSolver(graph=graph)
            route = solver.solve(requests=requests, depot=depot)

        elif strategy.uses_google():
            route = RoutingManager.__calc_google_route(graph=graph, depot=depot, requests=requests,
                                                       strategy=strategy)

        return route

    @staticmethod
    def __calc_route_insertion(graph, depot, all_requests, route, new_requests, strategy):

        inserter = RoutingInserter(graph=graph)

        if strategy.uses_double_insertion():
            new_route = inserter.calculate_double_insert_multiple(route=route, requests=new_requests)
        elif strategy.uses_cheap_insertion():
            new_route = inserter.calculate_cheap_insert_multiple(route=route, requests=new_requests)

        if strategy.uses_two_opt:
            new_route = RoutingManager.optimize(graph=graph, route=new_route, requests=all_requests, k_opt=2)
        elif strategy.uses_three_opt:
            new_route = RoutingManager.optimize(graph=graph, route=new_route, requests=all_requests, k_opt=3)
        elif strategy.uses_google_opt:
            new_route = RoutingManager.__calc_google_route_insertion(graph=graph, depot=depot, requests=all_requests,
                                                                     route=new_route, strategy=strategy)
        return new_route

    @staticmethod
    def __calc_route_removal(graph, remaining_requests, route, del_requests, strategy):

        remover = RoutingRemover()
        new_route = remover.remove_multiple_requests(route=route, requests=del_requests)

        if strategy.uses_two_opt():
            new_route = RoutingManager.optimize(graph=graph, route=new_route, requests=remaining_requests, k_opt=2)
        elif strategy.uses_three_opt():
            new_route = RoutingManager.optimize(graph=graph, route=new_route, requests=remaining_requests, k_opt=3)

        return new_route

    """
    ************
    ***PUBLIC***
    ************
    """

    def calculate_solution(self, requests):
        solution_strategy = self.configuration.solution_strategy

        key = self.get_solution_key(requests=requests)
        graph = self.get_graph()
        depot = self.get_depot()

        if key not in self.solutions:
            route = self.__calc_route(graph=graph, depot=depot, requests=requests, strategy=solution_strategy)
            self.solutions[key] = route, graph.calculate_route_distance(route=route)

        return self.solutions[key]

    def calculate_insertion_solution(self, route, current_requests, new_requests):
        insertion_strategy = self.configuration.insertion_strategy

        if insertion_strategy is None:
            return None

        all_requests = current_requests + new_requests
        key = self.get_solution_key(all_requests)
        graph = self.get_graph()
        depot = self.get_depot()

        if key not in self.solutions:

            if insertion_strategy == InsertionStrategy.NEW_ROUTE:
                self.solutions[key] = self.calculate_solution(all_requests)

            else:
                route = RoutingManager.__calc_route_insertion(graph=graph, depot=depot,
                                                              all_requests=all_requests, route=route,
                                                              new_requests=new_requests,
                                                              strategy=insertion_strategy)
                self.solutions[key] = route, graph.calculate_route_distance(route=route)

        return self.solutions[key]

    def calculate_remove_solution(self, route, requests, del_requests):
        removal_strategy = self.configuration.removal_strategy

        if removal_strategy is None:
            return None

        del_ids = [request.id for request in del_requests]
        remaining_requests = [request for request in requests if request.id not in del_ids]
        key = self.get_solution_key(requests=remaining_requests)
        graph = self.get_graph()

        if key not in self.solutions:

            if removal_strategy == RemovalStrategy.NEW_ROUTE:
                self.solutions[key] = self.calculate_solution(requests=remaining_requests)
            else:
                route = self.__calc_route_removal(graph=graph, remaining_requests=remaining_requests, route=route,
                                                  del_requests=del_requests, strategy=removal_strategy)
                self.solutions[key] = route, graph.calculate_route_distance(route)

        return self.solutions[key]

    """
    *************
    ***GETTERS***
    *************
    """

    def get_graph(self):
        return self.graph

    def get_depot(self):
        return self.depot

    def get_solution_key(self, requests):
        return frozenset([request.get_id() for request in requests])