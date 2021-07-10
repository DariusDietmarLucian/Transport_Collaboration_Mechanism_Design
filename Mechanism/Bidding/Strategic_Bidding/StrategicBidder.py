from Mechanism.Bidding.Strategic_Bidding.BiddingStrategy import BiddingStrategy

class StrategicBidder:

    def __init__(self, profit_func, configuration):
        self.profit_func = profit_func
        self.configuration = configuration

        self.last_true_input_bid_valuation = None

    """
    ************
    ***PUBLIC***
    ************
    """

    def calculate_valuation_own_requests(self, requests):
        true_valuation = self.profit_func(requests=requests, deletion=True)

        self.last_true_input_bid_valuation = true_valuation

        if self.configuration.strategy == BiddingStrategy.TRUTHFUL or self.configuration.strategy == BiddingStrategy.CONSPIRING:
            return true_valuation

        elif self.configuration.strategy == BiddingStrategy.INPUT_MANIPULATION:
            manipulated_valuation = true_valuation + abs(true_valuation) * self.configuration.input_bid_percentage
            return manipulated_valuation

        elif self.configuration.strategy == BiddingStrategy.HIGH_ABS:
            manipulated_valuation = true_valuation + abs(true_valuation) * self.configuration.input_bid_multiple
            return manipulated_valuation

        elif self.configuration.strategy == BiddingStrategy.BID_MANIPULATION_REL:
            manipulated_valuation = true_valuation + abs(true_valuation) * self.configuration.relative_margin
            return manipulated_valuation

    def calculate_valuation_other_requests(self, requests):

        true_valuation = self.profit_func(requests=requests, deletion=False)

        if true_valuation is None:
            return None

        if self.configuration.strategy == BiddingStrategy.HIGH_ABS:
            last_true_input_bid_valuation = self.get_last_true_input_valuation()
            manipulated_valuation = true_valuation + abs(last_true_input_bid_valuation) * self.configuration.input_bid_multiple
            return manipulated_valuation
        elif self.configuration.strategy == BiddingStrategy.BID_MANIPULATION_REL:
            manipulated_valuation = true_valuation + abs(true_valuation) * self.configuration.relative_margin
            return manipulated_valuation
        else:
            return true_valuation

    def get_last_true_input_valuation(self):
        return self.last_true_input_bid_valuation

    def get_bidding_strategy(self):
        return self.configuration.strategy
