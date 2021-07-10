import config


class PaymentCalculatorConfiguration:

    def __init__(self, strategy=None):
        self.strategy = strategy if strategy is not None else config.payment_calculator_configuration["strategy"]

    def get_dictionary(self):
        dic = {}

        dic["profit sharing method"] = str(self.strategy)

        return dic
