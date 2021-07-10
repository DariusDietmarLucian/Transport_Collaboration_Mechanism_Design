import config


class RequestSelectorConfiguration:

    def __init__(self, strategy=None):
        self.strategy = strategy if strategy is not None else config.request_selector_configuration[
            "strategy"]

    def get_dictionary(self):
        dic = {}

        dic["selection strategy"] = str(self.strategy)

        return dic
