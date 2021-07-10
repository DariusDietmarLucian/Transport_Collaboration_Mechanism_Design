import config
from Mechanism.Bidding.Strategic_Bidding.BiddingStrategy import BiddingStrategy


class StrategicBidderConfiguration:

    def __init__(self, strategy=None, input_bid_percentage=None, input_bid_multiple=None, relative_margin=None):

        self.strategy = strategy if strategy is not None else config.strategic_bidder_configuration[
            "strategy"]
        self.input_bid_percentage = input_bid_percentage if input_bid_percentage is not None else \
        config.strategic_bidder_configuration[
            "input_bid_percentage"]
        self.input_bid_multiple = input_bid_multiple if input_bid_multiple is not None else \
        config.strategic_bidder_configuration[
            "input_bid_multiple"]
        self.relative_margin = relative_margin if relative_margin is not None else \
        config.strategic_bidder_configuration[
            "relative_margin"]

    def get_dictionary(self):
        dic = {}

        dic["bidding strategy"] = str(self.strategy)

        if self.strategy == BiddingStrategy.INPUT_MANIPULATION:
            dic["input bid percentage"] = self.input_bid_percentage
        elif self.strategy == BiddingStrategy.HIGH_ABS:
            dic["absolute margin (multiple of input value)"] = self.input_bid_multiple
        elif self.strategy == BiddingStrategy.BID_MANIPULATION_REL:
            dic["relative margin"] = self.relative_margin

        return dic
