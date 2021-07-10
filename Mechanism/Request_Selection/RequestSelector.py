"""
Algorithms based on:
Gansterer, M. and Hartl, R.F., 2016. Request evaluation strategies for carriers in auction-based collaborations.
OR spectrum, 38(1), pp.3-23.
"""

from itertools import combinations
from Mechanism.Request_Selection.RequestSelectionStrategy import RequestSelectionStrategy


class RequestSelector:

    def __init__(self, graph, depot, other_depots, marginal_profit_function, configuration):
        self.graph = graph
        self.depot = depot
        self.other_depots = other_depots
        self.marginal_profit_function = marginal_profit_function
        self.configuration = configuration

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __calc_requests_cluster_distance(graph, requests):
        pairs = list(combinations(requests, 2))
        return sum([graph.calculate_request_distance(request=pair[0], other_request=pair[1]) for pair in pairs])

    @staticmethod
    def __calc_min_distance_request_depots(graph, request, depots):
        return min([graph.calculate_request_node_distance(request, depot) for depot in depots])

    @staticmethod
    def __calc_combo_value(graph, request, depot, other_depots, profit_function):
        min_dist_other_depots = RequestSelector.__calc_min_distance_request_depots(graph=graph, request=request,
                                                                                   depots=other_depots)
        marginal_profit = profit_function([request])
        dist_depot = graph.calculate_request_node_distance(request=request, node=depot, d_sum=True)

        return min_dist_other_depots + marginal_profit - dist_depot

    @staticmethod
    def __calc_requests_closeness(graph, request, other_request):
        pp_distance = graph.calculate_node_distance(request.get_pickup_node(), other_request.get_pickup_node())
        pd_distance = graph.calculate_node_distance(request.get_pickup_node(), other_request.get_delivery_node())
        dp_distance = graph.calculate_node_distance(request.get_delivery_node(), other_request.get_pickup_node())
        dd_distance = graph.calculate_node_distance(request.get_delivery_node(), other_request.get_delivery_node())
        return pp_distance + pd_distance + dp_distance + dd_distance

    @staticmethod
    def __neigh_requests(graph, selected_request, all_requests, num_requests):
        other_requests = [request for request in all_requests if request.id != selected_request.id]
        sorted_other_requests = sorted(other_requests,
                                       key=lambda rqst: RequestSelector.__calc_requests_closeness(graph=graph,
                                                                                                  request=selected_request,
                                                                                                  other_request=rqst))
        return sorted_other_requests[:num_requests]

    """
    implementations of different selection strategies
    """

    @staticmethod
    def __select_min_profit(profit_func, requests, num_requests, attempt):

        sorted_requests = sorted(requests, key=lambda request: profit_func([request]))

        if attempt >= len(requests):
            return [sorted_requests[-1]]
        elif (attempt + num_requests) > len(requests):
            return sorted_requests[attempt:]
        else:
            return sorted_requests[attempt:(attempt + num_requests)]

    @staticmethod
    def __select_cluster(graph, requests, num_requests, attempt):

        request_clusters = list(combinations(requests, num_requests))
        sorted_clusters = sorted(request_clusters,
                                 key=lambda cluster: RequestSelector.__calc_requests_cluster_distance(graph=graph,
                                                                                                      requests=cluster))
        if attempt >= len(requests):
            return list(sorted_clusters[-1])
        else:
            return list(sorted_clusters[attempt])

    # test sorted order
    @staticmethod
    def __select_combo(graph, profit_func, depot, other_depots, requests, num_requests, attempt):
        sorted_requests = sorted(requests,
                                 key=lambda rqst: RequestSelector.__calc_combo_value(graph=graph, request=rqst,
                                                                                     depot=depot,
                                                                                     other_depots=other_depots,
                                                                                     profit_function=profit_func))

        if attempt >= len(requests):
            return [sorted_requests[-1]]
        elif (attempt + num_requests) > len(requests):
            return sorted_requests[attempt:]
        else:
            return sorted_requests[attempt:(attempt + num_requests)]

    @staticmethod
    def __select_combo_neigh(graph, profit_func, depot, other_depots, requests, num_requests, attempt):

        if num_requests == 0:
            return []

        selected_request = \
            RequestSelector.__select_combo(graph=graph, profit_func=profit_func, depot=depot, other_depots=other_depots,
                                           requests=requests, num_requests=num_requests, attempt=attempt)[0]

        if num_requests == 1:
            return [selected_request]
        else:
            return [selected_request] + RequestSelector.__neigh_requests(graph=graph, selected_request=selected_request,
                                                                         all_requests=requests,
                                                                         num_requests=num_requests - 1)

    """
    ************
    ***PUBLIC***
    ************
    """

    def select(self, requests, num_requests, attempt):

        if num_requests > len(requests):
            return requests

        profit_func = self.marginal_profit_function
        graph = self.get_graph()
        depot = self.get_depot()
        other_depots = self.get_other_depots()

        if self.configuration.strategy == RequestSelectionStrategy.MIN_PROFIT:
            return self.__select_min_profit(profit_func=profit_func, requests=requests, num_requests=num_requests,
                                            attempt=attempt)
        elif self.configuration.strategy == RequestSelectionStrategy.CLUSTER:
            return self.__select_cluster(graph=graph, requests=requests, num_requests=num_requests, attempt=attempt)
        elif self.configuration.strategy == RequestSelectionStrategy.COMBO:
            return self.__select_combo(graph=graph, profit_func=profit_func, depot=depot, other_depots=other_depots,
                                       requests=requests, num_requests=num_requests, attempt=attempt)
        elif self.configuration.strategy == RequestSelectionStrategy.COMBO_NEIGH:
            return self.__select_combo_neigh(graph=graph, profit_func=profit_func, depot=depot,
                                             other_depots=other_depots, requests=requests, num_requests=num_requests,
                                             attempt=attempt)

    """
    *************
    ***GETTERS***
    *************
    """

    def get_graph(self):
        return self.graph

    def get_depot(self):
        return self.depot

    def get_other_depots(self):
        return self.other_depots
