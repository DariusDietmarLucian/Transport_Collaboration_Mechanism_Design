import config
from Mechanism.Bundle_Generation.BundleGeneratorConfiguration import BundleGeneratorConfiguration
from Mechanism.Payment_Calculation.PaymentCalculatorConfiguration import PaymentCalculatorConfiguration


class MechanismManagerConfiguration:

    def __init__(self, num_requests=None, num_retries=None, is_conspiring=None, payment_calculator_configuration=None,
                 bundle_generator_configuration=None):
        self.num_requests = num_requests if num_requests is not None else config.mechanism_manager_configuration[
            "num_requests"]
        self.num_retries = num_retries if num_retries is not None else config.mechanism_manager_configuration[
            "num_retries"]
        self.is_conspiring = is_conspiring if is_conspiring is not None else config.mechanism_manager_configuration[
            "is_conspiring"]

        self.payment_calculator_configuration = \
            payment_calculator_configuration if payment_calculator_configuration is not None \
                else PaymentCalculatorConfiguration()

        self.bundle_generator_configuration = \
            bundle_generator_configuration if bundle_generator_configuration is not None \
                else BundleGeneratorConfiguration()

    def get_dictionary(self):
        dic = {}

        dic["number of traded requests per carrier"] = self.num_requests
        dic["number of retries"] = self.num_retries
        dic["is conspiring"] = self.is_conspiring

        dic["payment_calculator_configuration"] = self.payment_calculator_configuration.get_dictionary()
        dic["bundle_generator_configuration"] = self.bundle_generator_configuration.get_dictionary()

        return dic
