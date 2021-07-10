import config


class ConspiringBidderConfiguration:

    def __init__(self, strategies=None):
        self.strategies = strategies if strategies is not None else config.conspiring_bidder_configuration[
            "strategies"]

    def get_dictionary(self):
        dic = {}

        dic["conspiring strategies"] = [str(strategy) for strategy in self.strategies]

        return dic
