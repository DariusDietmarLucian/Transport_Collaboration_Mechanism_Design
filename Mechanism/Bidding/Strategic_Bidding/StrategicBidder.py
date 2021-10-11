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

        # if len(requests) == 0:
        #     return None

        if self.configuration.strategy == BiddingStrategy.TRUTHFUL \
                or self.configuration.strategy == BiddingStrategy.CONSPIRING\
                or self.configuration.strategy == BiddingStrategy.HIGH_ABS_ISO\
                or self.configuration.strategy == BiddingStrategy.BID_MANIPULATION_REL:
            return true_valuation

        elif self.configuration.strategy == BiddingStrategy.INPUT_MANIPULATION:
            manipulated_valuation = true_valuation + abs(true_valuation) * self.configuration.input_bid_percentage
            return manipulated_valuation

        elif self.configuration.strategy == BiddingStrategy.HIGH_ABS:
            manipulated_valuation = true_valuation + abs(true_valuation) * self.configuration.input_bid_multiple
            return manipulated_valuation

        # elif self.configuration.strategy == BiddingStrategy.BID_MANIPULATION_REL:
        #     manipulated_valuation = true_valuation + abs(true_valuation) * self.configuration.relative_margin
        #     return manipulated_valuation

    def calculate_valuation_other_requests(self, requests):

        true_valuation = self.profit_func(requests=requests, deletion=False)


        if true_valuation is None:
            # if len(requests) == 0:
                # print("debug: return NONE")
            return None
        # if true_valuation is None:
        #     return -999999

        # if len(requests) == 0:
        #     return None
            # print("debug: ah ya")

        if self.configuration.strategy == BiddingStrategy.HIGH_ABS \
                or self.configuration.strategy == BiddingStrategy.HIGH_ABS_ISO:
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
