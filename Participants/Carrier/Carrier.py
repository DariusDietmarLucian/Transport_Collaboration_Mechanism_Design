from Mechanism.Request_Selection.RequestSelector import RequestSelector
from Mechanism.Bidding.Strategic_Bidding.StrategicBidder import StrategicBidder
from Mechanism.Bidding.Conspiring_Bidding.ConspiringBidder import ConspiringBidder
from Participants.Carrier.Profitability import Profitability

from Routing.RoutingManager import RoutingManager


class Carrier:

    def __init__(self, id, other_player_ids, depot, other_depots, requests, graph, configuration):
        self.id = id
        self.other_player_ids = other_player_ids
        self.depot = depot
        self.other_depots = other_depots
        self.requests = requests
        self.graph = graph
        self.configuration = configuration

        self.fix_rev = 20
        self.var_rev = 2
        self.fix_cost = None
        self.var_cost = None
        self.infeasible_request_sets = []
        self.external_payments = 0
        self.routing_manager = None
        self.request_selector = None
        self.conspiring_bidder = None
        self.strategic_bidder = None
        self.current_routing_solution = None
        self.max_capacity = None

        self.__set_up()

    # player should figure out the routing solution and the max capacity from the start
    def __set_up(self):
        self.current_routing_solution = self.get_current_routing_solution()
        self.max_capacity = self.get_max_capacity()

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __calc_revenue_request(fix_rev, var_rev, request):
        return fix_rev + var_rev * request.get_distance()

    @staticmethod
    def __calc_revenue(fix_rev, var_rev, requests):
        return sum(
            Carrier.__calc_revenue_request(fix_rev=fix_rev, var_rev=var_rev, request=request) for request in requests)

    @staticmethod
    def __calc_costs(fix_cost, var_cost, requests, distance):
        num_requests = len(requests)
        return num_requests * fix_cost + distance * var_cost

    @staticmethod
    def __calc_profit(fix_rev, var_rev, fix_cost, var_cost, requests, distance):
        revenue = Carrier.__calc_revenue(fix_rev=fix_rev, var_rev=var_rev, requests=requests)
        costs = Carrier.__calc_costs(fix_cost=fix_cost, var_cost=var_cost, requests=requests, distance=distance)
        return revenue - costs

    @staticmethod
    def __calc_marginal_distance(current_solution, current_requests, other_requests, manager, deletion):
        current_route, current_distance = current_solution

        if deletion:
            new_route, new_distance = manager.calculate_remove_solution(route=current_route,
                                                                        requests=current_requests,
                                                                        del_requests=other_requests)
        else:
            new_route, new_distance = manager.calculate_insertion_solution(route=current_route,
                                                                           current_requests=current_requests,
                                                                           new_requests=other_requests)
        return new_distance - current_distance

    """
    update variables
    """

    def __add_infeasible_request_set(self, requests):
        self.infeasible_request_sets.append(set(requests))

    def __add_external_payment(self, payment):
        current_external_payments = self.get_external_payments()
        self.set_external_payments(current_external_payments + payment)

    def __add_requests(self, add_requests):
        current_requests = self.get_requests()
        updated_requests = current_requests + add_requests
        self.set_requests(requests=updated_requests)

    def __delete_requests(self, del_requests):
        current_requests = self.get_requests()
        deleted_requests_ids = [request.id for request in del_requests]
        updated_requests = [request for request in current_requests if request.id not in deleted_requests_ids]
        self.set_requests(requests=updated_requests)

    """
    translations to static methods
    """

    def __get_revenue(self, requests):
        return self.__calc_revenue(fix_rev=self.get_fix_rev(), var_rev=self.get_var_rev(), requests=requests)

    def __get_costs(self, requests, distance):
        return self.__calc_costs(fix_cost=self.get_fix_cost(), var_cost=self.get_var_cost(), requests=requests, distance=distance)

    def __get_profit(self, requests, distance):
        return self.__calc_profit(fix_rev=self.get_fix_rev(), var_rev=self.get_var_rev(), fix_cost=self.get_fix_cost(),
                                  var_cost=self.get_var_cost(), requests=requests, distance=distance)

    """
    calculations
    """

    def __calc_marginal_profit(self, requests, deletion):
        if len(requests) == 0:
            return 0

        if deletion:
            return self.__calc_marginal_profit_del_rqts(del_requests=requests)
        else:
            return self.__calc_marginal_profit_new_rqsts(new_requests=requests)

    def __calc_marginal_profit_new_rqsts(self, new_requests):
        current_requests = self.get_requests()
        max_capacity = self.get_max_capacity()
        manager = self.get_routing_manager()
        current_solution = self.get_current_routing_solution()
        current_route, current_distance = current_solution

        all_requests = current_requests + new_requests

        if max_capacity is not None:
            all_rqst_set = set(all_requests)
            infeasible_request_sets = self.get_infeasible_request_sets()
            # if subset is already infeasible then the bigger set will most likely (because heuristics) be infeasible as well
            subset_is_infeasible = (
                    True in [rqst_set.issubset(all_rqst_set) for rqst_set in infeasible_request_sets])
            if subset_is_infeasible:
                return None

        marginal_distance = self.__calc_marginal_distance(current_solution=current_solution,
                                                          current_requests=current_requests,
                                                          other_requests=new_requests, manager=manager, deletion=False)

        if max_capacity is not None and (current_distance + marginal_distance) > max_capacity:
            self.__add_infeasible_request_set(requests=all_requests)
            return None

        return self.__get_profit(requests=new_requests, distance=marginal_distance)

    def __calc_marginal_profit_del_rqts(self, del_requests):

        manager = self.get_routing_manager()
        current_requests = self.get_requests()
        current_solution = self.get_current_routing_solution()

        marginal_distance = self.__calc_marginal_distance(current_solution=current_solution,
                                                          current_requests=current_requests,
                                                          other_requests=del_requests, manager=manager, deletion=True)

        return self.__get_profit(requests=del_requests, distance=-marginal_distance)

    """
    ************
    ***PUBLIC***
    ************
    """

    def submit_offer(self, num_requests, attempt):

        current_requests = self.get_requests()
        num_requests = max(0, min(len(current_requests) - self.configuration.min_num_requests, num_requests))

        strategic_bidder = self.get_strategic_bidder()
        selector = self.get_request_selector()

        selected_requests = selector.select(requests=current_requests, num_requests=num_requests, attempt=attempt)
        valuation = strategic_bidder.calculate_valuation_own_requests(requests=selected_requests)

        if num_requests == 0:
            return [], valuation

        # Routing problem has to change after offering requests
        self.__delete_requests(del_requests=selected_requests)

        return selected_requests, valuation

    def valuate_requests(self, requests):

        strategic_bidder = self.get_strategic_bidder()
        valuation = strategic_bidder.calculate_valuation_other_requests(requests=requests)

        if valuation is None:
            return None
        else:
            return valuation

    def submit_conspired_bids(self, input_bids, bundles, bid_matrix, profit_sharing_strategy):

        conspiring_bidder = self.get_conspiring_bidder()
        input_bid, bundle_bids = conspiring_bidder.get_conspired_bids(input_bids=input_bids, bundles=bundles,
                                                                      bid_matrix=bid_matrix,
                                                                      profit_sharing_strategy=profit_sharing_strategy)
        return input_bid, bundle_bids

    def receive_requests(self, requests):
        self.__add_requests(add_requests=requests)

    def receive_payment(self, payment):
        self.__add_external_payment(payment=payment)

    """
    *************
    ***SETTERS***
    *************
    """

    def set_external_payments(self, external_payments):
        self.external_payments = external_payments

    def set_requests(self, requests):
        self.requests = requests

        # if the player has to fulfill a new set of requests -> the routing solution needs to be updated
        manager = self.get_routing_manager()
        updated_solution = manager.calculate_solution(requests=requests)
        self.set_current_routing_solution(solution=updated_solution)

    def set_current_routing_solution(self, solution):
        self.current_routing_solution = solution

    """
    *************
    ***GETTERS***
    *************
    """

    def get_id(self):
        return self.id

    def get_other_player_ids(self):
        return self.other_player_ids

    def get_fix_rev(self):
        return self.fix_rev

    def get_var_rev(self):
        return self.var_rev

    def get_fix_cost(self):
        if self.fix_cost is None:

            if self.configuration.profitability == Profitability.HIGH_PROFITABILITY:
                self.fix_cost = 10
            elif self.configuration.profitability == Profitability.MEDIUM_PROFITABILITY:
                self.fix_cost = 11
            elif self.configuration.profitability == Profitability.LOW_PROFITABILITY:
                self.fix_cost = 12

        return self.fix_cost

    def get_var_cost(self):
        if self.var_cost is None:

            if self.configuration.profitability == Profitability.HIGH_PROFITABILITY:
                self.var_cost = 1
            elif self.configuration.profitability == Profitability.MEDIUM_PROFITABILITY:
                self.var_cost = 1.1
            elif self.configuration.profitability == Profitability.LOW_PROFITABILITY:
                self.var_cost = 1.2

        return self.var_cost

    def get_graph(self):
        return self.graph

    def get_depot(self):
        return self.depot

    def get_other_depots(self):
        return self.other_depots

    def get_requests(self):
        return self.requests

    def get_external_payments(self):
        return self.external_payments

    def get_infeasible_request_sets(self):
        return self.infeasible_request_sets

    def get_routing_manager(self):
        if self.routing_manager is None:
            graph = self.get_graph()
            depot = self.get_depot()
            self.routing_manager = RoutingManager(graph=graph, depot=depot,
                                                  configuration=self.configuration.routing_manager_configuration)

        return self.routing_manager

    def get_strategic_bidder(self):
        if self.strategic_bidder is None:
            self.strategic_bidder = StrategicBidder(profit_func=self.__calc_marginal_profit,
                                                    configuration=self.configuration.strategic_bidder_configuration)

        return self.strategic_bidder

    def get_conspiring_bidder(self):
        if self.conspiring_bidder is None:
            my_id = self.get_id()
            other_ids = self.get_other_player_ids()
            configuration = self.configuration.conspiring_bidder_configuration
            self.conspiring_bidder = ConspiringBidder(player_id=my_id, other_player_ids=other_ids,
                                                      configuration=configuration)

        return self.conspiring_bidder

    def get_current_routing_solution(self):
        if self.current_routing_solution is None:
            requests = self.get_requests()
            manager = self.get_routing_manager()
            self.current_routing_solution = manager.calculate_solution(requests=requests)

        return self.current_routing_solution

    def get_max_capacity(self):
        if self.configuration.max_capacity is not None and self.max_capacity is None:
            self.max_capacity = self.get_current_route_distance() * self.configuration.max_capacity

        return self.max_capacity

    def get_request_selector(self):
        if self.request_selector is None:
            graph = self.get_graph()
            depot = self.get_depot()
            other_depots = self.get_other_depots()
            m_prof_func = self.__calc_marginal_profit_del_rqts

            self.request_selector = RequestSelector(graph=graph, depot=depot, other_depots=other_depots,
                                                    marginal_profit_function=m_prof_func,
                                                    configuration=self.configuration.request_selector_configuration)

        return self.request_selector

    def get_current_route_distance(self):
        return self.get_current_routing_solution()[1]

    def get_current_route(self):
        return self.get_current_routing_solution()[0]

    # profit without taking into account external payments (received or paid during auction rounds)
    def get_base_profit(self):
        return self.__get_profit(requests=self.get_requests(), distance=self.get_current_route_distance())

    def get_total_profit(self):
        return self.get_base_profit() + self.get_external_payments()

    def get_revenue(self):
        return self.__get_revenue(requests=self.get_requests())

    def get_costs(self):
        return self.__get_costs(requests=self.get_requests(), distance=self.get_current_route_distance())

    """
    **************
    ***CONFORMS***
    **************
    """

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __hash__(self):
        return hash(('id', self.get_id()))
