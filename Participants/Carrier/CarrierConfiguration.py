import config
from Mechanism.Request_Selection.RequestSelectorConfiguration import RequestSelectorConfiguration
from Mechanism.Bidding.Strategic_Bidding.StrategicBidderConfiguration import StrategicBidderConfiguration
from Mechanism.Bidding.Conspiring_Bidding.ConspiringBidderConfiguration import ConspiringBidderConfiguration
from Routing.RoutingManagerConfiguration import RoutingManagerConfiguration
from Mechanism.Bidding.Strategic_Bidding.BiddingStrategy import BiddingStrategy


class CarrierConfiguration:

    def __init__(self, max_capacity=None, min_num_requests=None, profitability=None, routing_manager_configuration=None,
                 request_selector_configuration=None,
                 strategic_bidder_configuration=None, conspiring_bidder_configuration=None):
        self.max_capacity = max_capacity if max_capacity is not None else config.carrier_configuration[
            "max_capacity"]
        self.min_num_requests = min_num_requests if min_num_requests is not None else config.carrier_configuration[
            "min_num_requests"]
        self.profitability = profitability if profitability is not None else config.carrier_configuration[
            "profitability"]

        self.routing_manager_configuration = \
            routing_manager_configuration if routing_manager_configuration is not None \
                else RoutingManagerConfiguration()

        self.request_selector_configuration = \
            request_selector_configuration if request_selector_configuration is not None \
                else RequestSelectorConfiguration()

        self.strategic_bidder_configuration = \
            strategic_bidder_configuration if strategic_bidder_configuration is not None \
                else StrategicBidderConfiguration()

        if self.strategic_bidder_configuration.strategy == BiddingStrategy.CONSPIRING:
            self.conspiring_bidder_configuration = \
                conspiring_bidder_configuration if conspiring_bidder_configuration is not None \
                    else ConspiringBidderConfiguration()
        else:
            self.conspiring_bidder_configuration = None

    def get_dictionary(self):
        dic = {}

        dic["max capacity"] = self.max_capacity
        dic["min number of requests"] = self.min_num_requests
        dic["profitability"] = str(self.profitability)

        dic["routing manager configuration"] = self.routing_manager_configuration.get_dictionary()
        dic["request selector configuration"] = self.request_selector_configuration.get_dictionary()
        dic["strategic bidder configuration"] = self.strategic_bidder_configuration.get_dictionary()

        if self.conspiring_bidder_configuration is not None:
            dic["conspiring bidder configuration"] = self.conspiring_bidder_configuration.get_dictionary()

        return dic
