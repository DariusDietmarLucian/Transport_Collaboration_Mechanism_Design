from itertools import compress, product
import math
from Mechanism.Payment_Calculation.ProfitSharingStrategy import ProfitSharingStrategy


class PaymentCalculator:

    def __init__(self, input_bids, winning_bids, collaboration_gain, carriers, determinator, configuration):

        self.input_bids = input_bids
        self.winning_bids = winning_bids
        self.collaboration_gain = collaboration_gain
        self.carriers = carriers
        self.determinator = determinator
        self.configuration = configuration

        self.initial_profit = None
        self.winning_profit = None
        self.absolute_initial_profit = None
        self.absolute_winning_profit = None
        self.total_margins = None
        self.carrier_margins = None
        self.carrier_coalitions = None
        self.coalition_valuations = None

    """
    ************
    ***PRIVATE**
    ************
    """

    @staticmethod
    def __get_carrier_bids(input_bids, winning_bids, carrier):
        input_bid = next(bid for bid in input_bids if bid.get_carrier_id() == carrier.id)
        winning_bid = next(bid for bid in winning_bids if bid.get_carrier_id() == carrier.id)
        return input_bid, winning_bid

    @staticmethod
    def calculate_egalitarian_share(carrier_id, input_bids, winning_bids, requires_contribution):

        if not requires_contribution:
            return 1 / len(winning_bids)

        contribution_bids = [bid for bid in input_bids if bid not in winning_bids]

        input_bid = next(bid for bid in input_bids if bid.get_carrier_id() == carrier_id)
        winning_bid = next(bid for bid in winning_bids if bid.get_carrier_id() == carrier_id)

        if input_bid != winning_bid:
            return 1 / len(contribution_bids)
        else:
            return 0

    """
    Based on:
    Gansterer, M., Hartl, R.F. and Sörensen, K., 2020. 
    Pushing frontiers in auction-based transport collaborations. Omega, 94, p.102042.
    """
    @staticmethod
    def __calc_purchase_sale_weight(input_bid, winning_bid, absolute_initial_profit, absolute_winning_profit):

        if input_bid is not None:
            sales_weight = abs(input_bid.get_valuation()) / absolute_initial_profit
        else:
            sales_weight = 0

        purchase_weight = abs(winning_bid.get_valuation()) / absolute_winning_profit

        return (sales_weight + purchase_weight) / 2

    @staticmethod
    def __calc_margins(input_bids, winning_profit, determinator, exponent):
        total_margin = 0
        carrier_margins = {}

        for input_bid in input_bids:
            alt_winning_bids = determinator.determine_winners(enforced_bids=[input_bid])
            alt_winning_valuation = sum([bid.get_valuation() for bid in alt_winning_bids])
            margin = winning_profit - alt_winning_valuation
            carrier_margins[input_bid.get_carrier_id()] = (margin ** exponent)
            total_margin += (margin ** exponent)

        return total_margin, carrier_margins

    @staticmethod
    def __calc_coalition_values(carriers, input_bids, determinator):
        coalition_values = {}
        carrier_coalitions = list(
            list(compress(carriers, mask)) for mask in list(product(range(2), repeat=len(carriers))))[1:]

        for coalition in carrier_coalitions:
            coalition_carrier_ids = [carrier.get_id() for carrier in coalition]
            coalition_value = 0

            if len(coalition) > 1:
                other_input_bids = [bid for bid in input_bids if bid.get_carrier_id() not in coalition_carrier_ids]
                winning_coalition_bids = determinator.determine_winners(enforced_bids=other_input_bids)

                winning_coalition_value = sum([bid.get_valuation() for bid in winning_coalition_bids])
                input_value = sum([bid.get_valuation() for bid in input_bids])

                coalition_value = winning_coalition_value - input_value

            coalition_id = frozenset(coalition_carrier_ids)
            coalition_values[coalition_id] = coalition_value

        return carrier_coalitions, coalition_values

    """
    Based on:
    Shapley, L.S., 2016. 17. A value for n-person games (pp. 307-318). Princeton University Press.
    """
    @staticmethod
    def __calc_shapley_value(carrier, carrier_coalitions, coalition_valuations):

        shapley_value = 0

        max_len = max([len(coalition) for coalition in carrier_coalitions])
        other_carrier_coalitions = [coalition for coalition in carrier_coalitions if carrier not in coalition]

        for other_carrier_coalition in other_carrier_coalitions:
            other_carrier_coalition_ids = [carrier.get_id() for carrier in other_carrier_coalition]
            full_coalition_ids = other_carrier_coalition_ids + [carrier.get_id()]

            other_id = frozenset(other_carrier_coalition_ids)
            full_id = frozenset(full_coalition_ids)

            len_other = len(other_carrier_coalition_ids)

            weight = (math.factorial(len_other) * math.factorial(max_len - len_other - 1)) / math.factorial(max_len)
            coalition_val_difference = coalition_valuations[full_id] - coalition_valuations[other_id]

            shapley_value += weight * coalition_val_difference

        return shapley_value

    """
    ************
    ***PUBLIC***
    ************
    """

    def calculate_payment(self, carrier):
        input_bids = self.get_input_bids()
        winning_bids = self.get_winning_bids()

        input_bid, winning_bid = self.__get_carrier_bids(input_bids=input_bids, winning_bids=winning_bids,
                                                         carrier=carrier)

        if input_bid is not None:
            input_compensation = input_bid.get_valuation()
        else:
            input_compensation = 0

        bid_payment = winning_bid.get_valuation()

        if self.configuration.strategy == ProfitSharingStrategy.EGALITARIAN or self.configuration.strategy == ProfitSharingStrategy.MODIFIED_EGALITARIAN:
            weight = self.calculate_egalitarian_share(carrier_id=carrier.get_id(), input_bids=input_bids,
                                                      winning_bids=winning_bids,
                                                      requires_contribution=self.configuration.strategy.requires_contribution())

        elif self.configuration.strategy == ProfitSharingStrategy.PURCHASE_SALE_WEIGHT:
            abs_initial_profit = self.get_absolute_initial_profit()
            abs_winning_profit = self.get_absolute_winning_profit()
            weight = self.__calc_purchase_sale_weight(input_bid=input_bid, winning_bid=winning_bid,
                                                      absolute_initial_profit=abs_initial_profit,
                                                      absolute_winning_profit=abs_winning_profit)

        elif self.configuration.strategy == ProfitSharingStrategy.CRITICAL_WEIGHT:
            carrier_margin = self.get_carrier_margin(carrier_id=carrier.get_id(), exponent=1)
            total_margins = self.get_total_margins(exponent=1)
            weight = carrier_margin / total_margins

        elif self.configuration.strategy == ProfitSharingStrategy.CRITICAL_WEIGHT_SQUARED:
            carrier_margin = self.get_carrier_margin(carrier_id=carrier.get_id(), exponent=2)
            total_margins = self.get_total_margins(exponent=2)
            weight = carrier_margin / total_margins

        elif self.configuration.strategy == ProfitSharingStrategy.CRITICAL_WEIGHT_CUBIC:
            carrier_margin = self.get_carrier_margin(carrier_id=carrier.get_id(), exponent=3)
            total_margins = self.get_total_margins(exponent=3)
            weight = carrier_margin / total_margins

        elif self.configuration.strategy == ProfitSharingStrategy.SHAPLEY_VALUE:
            coalition_valuations = self.get_coalition_valuations()
            carrier_coalitions = self.get_carrier_coalitions()
            shapley_value = self.__calc_shapley_value(carrier=carrier, carrier_coalitions=carrier_coalitions,
                                                      coalition_valuations=coalition_valuations)
            return input_compensation - bid_payment + shapley_value

        return input_compensation - bid_payment + (weight * self.get_collaboration_gain())

    """
    *************
    ***GETTERS***
    *************
    """

    def get_carriers(self):
        return self.carriers

    def get_input_bids(self):
        return self.input_bids

    def get_winning_bids(self):
        return self.winning_bids

    def get_collaboration_gain(self):
        return self.collaboration_gain

    def get_determinator(self):
        return self.determinator

    def get_initial_profit(self):
        if self.initial_profit is None:
            input_bids = self.get_input_bids()
            self.initial_profit = sum([bid.get_valuation() for bid in input_bids])

        return self.initial_profit

    def get_winning_profit(self):
        if self.winning_profit is None:
            winning_bids = self.get_winning_bids()
            self.winning_profit = sum([bid.get_valuation() for bid in winning_bids])

        return self.winning_profit

    def get_absolute_initial_profit(self):
        if self.absolute_initial_profit is None:
            input_bids = self.get_input_bids()
            self.absolute_initial_profit = sum([abs(bid.get_valuation()) for bid in input_bids])

        return self.absolute_initial_profit

    def get_absolute_winning_profit(self):
        if self.absolute_winning_profit is None:
            winning_bids = self.get_winning_bids()
            self.absolute_winning_profit = sum([abs(bid.get_valuation()) for bid in winning_bids])

        return self.absolute_winning_profit

    def get_total_margins(self, exponent):
        if self.total_margins is None:
            input_bids = self.get_input_bids()
            winning_profit = self.get_winning_profit()
            determinator = self.get_determinator()
            total_margins, carrier_margins = self.__calc_margins(input_bids=input_bids, winning_profit=winning_profit,
                                                                 determinator=determinator, exponent=exponent)
            self.total_margins = total_margins
            self.carrier_margins = carrier_margins

        return self.total_margins

    def get_carrier_margin(self, carrier_id, exponent):
        if self.carrier_margins is None:
            input_bids = self.get_input_bids()
            winning_profit = self.get_winning_profit()
            determinator = self.get_determinator()
            total_margins, carrier_margins = self.__calc_margins(input_bids=input_bids, winning_profit=winning_profit,
                                                                 determinator=determinator, exponent=exponent)
            self.total_margins = total_margins
            self.carrier_margins = carrier_margins

        return self.carrier_margins[carrier_id]

    def get_carrier_coalitions(self):
        if self.carrier_coalitions == None:
            carriers = self.get_carriers()
            determinator = self.get_determinator()
            input_bids = self.get_input_bids()
            carrier_coalitions, coalition_valuations = self.__calc_coalition_values(carriers=carriers,
                                                                                    input_bids=input_bids,
                                                                                    determinator=determinator)
            self.carrier_coalitions = carrier_coalitions
            self.coalition_valuations = coalition_valuations

        return self.carrier_coalitions

    def get_coalition_valuations(self):
        if self.coalition_valuations == None:
            carriers = self.get_carriers()
            determinator = self.get_determinator()
            input_bids = self.get_input_bids()
            carrier_coalitions, coalition_valuations = self.__calc_coalition_values(carriers=carriers,
                                                                                    input_bids=input_bids,
                                                                                    determinator=determinator)
            self.carrier_coalitions = carrier_coalitions
            self.coalition_valuations = coalition_valuations

        return self.coalition_valuations
