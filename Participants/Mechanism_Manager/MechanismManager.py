"""
Mechanism based on:
Berger, S. and Bierwirth, C., 2010. Solutions to the request reassignment problem in collaborative carrier networks.
Transportation Research Part E: Logistics and Transportation Review, 46(5), pp.627-638.
"""


from Models.Bid import Bid
from Models.RequestBundle import RequestBundle

from Mechanism.Bundle_Generation.BundleGenerator import BundleGenerator
from Mechanism.Winner_Determination.WinnerDeterminator import WinnerDeterminator
from Mechanism.Payment_Calculation.PaymentCalculator import PaymentCalculator

from Routing.Heuristics_Routing.RoutingSolver import RoutingSolver


class MechanismManager:

    def __init__(self, carriers, graph, configuration):
        self.carriers = carriers
        self.graph = graph
        self.configuration = configuration

        self.solver = None
        self.past_trade_ids = []

    """
    *************
    ***PRIVATE***
    *************
    """

    def __start_trading_round(self, attempt):

        carriers = self.get_carriers()

        # 1) collect bids that the carriers want to offer
        input_bids = self.__collect_offers(attempt)
        requests = [request for bid in input_bids for request in bid.get_requests()]
        if len(requests) == 0:
            return 0

        # print(f"len requests = {len([request for bid in input_bids for request in bid.get_requests()])}")

        # it's not allowed to trade exactly the same requests again (because auction might never terminate otherwise)
        trade_id = str([list(bid.get_bundle_id()) for bid in input_bids])
        if trade_id in self.past_trade_ids:
            self.__allocate_requests(bids=input_bids)
            return 0
        else:
            self.past_trade_ids.append(trade_id)

        # 2) generate bundles from the offered bids
        generator = BundleGenerator(input_bids=input_bids, solver=self.solver, graph=self.graph,
                                    configuration=self.configuration.bundle_generator_configuration)
        bundles = generator.generate_bundles()

        # 3) collect bids for the generated bundles
        bid_matrix = self.__collect_bids(input_bids=input_bids, bundles=bundles)

        # ( 3.5) conspire with carrier 0 )
        new_input_bid, new_bundle_bids = carriers[0].submit_conspired_bids(input_bids, bundles, bid_matrix,
                                                                          self.configuration.payment_calculator_configuration.strategy)
        if new_input_bid is not None and new_bundle_bids is not None:
            input_bids[0] = new_input_bid
            bid_matrix[0] = new_bundle_bids

        # 4) determine the best bundle allocation
        determinator = WinnerDeterminator(requests=requests, bundles=bundles, bid_matrix=bid_matrix)
        winning_bids = determinator.determine_winners()

        # 5) allocate requests and calculate payment to/from the carriers
        initial_profit = sum([input_bid.get_valuation() for input_bid in input_bids])
        profit = sum([winning_bid.get_valuation() for winning_bid in winning_bids])
        collaboration_gain = profit - initial_profit

        if collaboration_gain > 0:
            self.__allocate_requests(bids=winning_bids)
            calculator = PaymentCalculator(input_bids=input_bids, winning_bids=winning_bids,
                                           collaboration_gain=collaboration_gain, carriers=carriers,
                                           determinator=determinator,
                                           configuration=self.configuration.payment_calculator_configuration)


            for carrier in carriers:
                payment = calculator.calculate_payment(carrier=carrier)
                carrier.receive_payment(payment=payment)

            return collaboration_gain
        else:
            self.__allocate_requests(bids=input_bids)
            return 0

    """
    INPUT
    """

    def __collect_offers(self, attempt):

        carriers = self.get_carriers()
        solver = self.get_solver()
        graph = self.get_graph()

        offer_bids = []

        for carrier in carriers:
            requests, valuation = carrier.submit_offer(num_requests=self.configuration.num_requests, attempt=attempt)

            bundle = RequestBundle(requests=requests, solver=solver, graph=graph)
            bid = Bid(bundle=bundle, valuation=valuation, carrier_id=carrier.id)
            offer_bids.append(bid)

        return offer_bids

    def __collect_bids(self, input_bids, bundles):

        carriers = self.get_carriers()

        bid_matrix = []

        for i, carrier in enumerate(carriers):
            bids = []
            input_bid = next(bid for bid in input_bids if bid.get_carrier_id() == carrier.get_id())

            for j, bundle in enumerate(bundles):

                if bundle == input_bid.get_bundle():
                    valuation = input_bid.get_valuation()
                else:
                    valuation = carrier.valuate_requests(requests=bundle.get_requests())

                bid = Bid(bundle=bundle, valuation=valuation, carrier_id=carrier.id)
                bids.append(bid)

            bid_matrix.append(bids)

        return bid_matrix

    """
    OUTPUT
    """

    def __allocate_requests(self, bids):
        carriers = self.get_carriers()

        for bid in bids:
            carrier = next(carrier for carrier in carriers if carrier.id == bid.get_carrier_id())
            requests = bid.get_requests()
            carrier.receive_requests(requests=requests)

    """
    ************
    ***PUBLIC***
    ************
    """

    def start_managing_trade(self):

        total_collaboration_gain = 0
        attempts = 0
        iterations = 0

        while True:
            iterations += 1
            collaboration_gain = self.__start_trading_round(attempt=attempts)
            total_collaboration_gain += collaboration_gain

            if not collaboration_gain:
                attempts += 1
                if attempts > self.configuration.num_retries:
                    break
            else:
                attempts = 0

        return total_collaboration_gain, iterations

    """
    *************
    ***GETTERS***
    *************
    """

    def get_carriers(self):
        return self.carriers

    def get_graph(self):
        return self.graph

    def get_solver(self):

        if self.solver is None:
            self.solver = RoutingSolver(self.get_graph())

        return self.solver
