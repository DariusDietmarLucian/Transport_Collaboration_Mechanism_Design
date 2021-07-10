from Instance_Generation.GenerationStrategy import GenerationStrategy
from Instance_Generation.CompetitionLevel import CompetitionLevel

from Mechanism.Payment_Calculation.PaymentCalculator import ProfitSharingStrategy
from Mechanism.Bidding.Strategic_Bidding.StrategicBidder import BiddingStrategy
from Mechanism.Bidding.Conspiring_Bidding.ConspiringBidder import ConspiringStrategy
from Participants.Carrier.Profitability import Profitability

from Instance_Generation.InstanceGenerationManagerConfiguration import InstanceGenerationManagerConfiguration
from Participants.Mechanism_Manager.MechanismManagerConfiguration import MechanismManagerConfiguration
from Participants.Carrier.CarrierConfiguration import CarrierConfiguration

import json
import os
from datetime import date


class OutputFileManager:

    def __init__(self, results, parent_directory, input_config=None, carrier_config=None, other_carriers_config=None,
                 mechanism_manager_config=None, ):
        self.results = results
        self.parent_directory = parent_directory

        self.input_config = input_config if input_config is not None else InstanceGenerationManagerConfiguration()
        self.mechanism_manager_config = mechanism_manager_config if mechanism_manager_config is not None else MechanismManagerConfiguration()
        self.carrier_config = carrier_config if carrier_config is not None else CarrierConfiguration()
        self.other_carriers_config = other_carriers_config if other_carriers_config is not None else CarrierConfiguration()

    """
    *************
    ***PRIVATE***
    *************
    """

    def __get_output_directory(self):
        parent_directory = self.get_parent_directory()
        return os.path.join(parent_directory, "Output")

    def __get_configuration_dic(self):
        config_dic = {}
        config_dic["input"] = self.get_input_configuration().get_dictionary()
        config_dic["mechanism manager"] = self.get_mechanism_manager_configuration().get_dictionary()
        config_dic["carrier"] = self.get_carrier_configuration().get_dictionary()
        config_dic["other carriers"] = self.get_other_carriers_configuration().get_dictionary()
        return config_dic

    def __get_output_dic(self):
        output_dic = {}
        output_dic["configuration"] = self.__get_configuration_dic()
        output_dic["results"] = self.get_results()
        return output_dic

    @staticmethod
    def __get_conspiring_strategy_string(strategy):
        if strategy == ConspiringStrategy.AUTO_COMBO:
            return "AUTO"
        elif strategy == ConspiringStrategy.DESTROY_WEIGHT:
            return "DESTROY_WEIGHT"
        elif strategy == ConspiringStrategy.BID_KICKOUT:
            return "BID_KICKOUT"
        elif strategy == ConspiringStrategy.INPUT_ENTER:
            return "INPUT_ENTER"
        elif strategy == ConspiringStrategy.INPUT_MAX:
            return "INPUT_MAX"

    @staticmethod
    def __extend_path(path, extension):
        extended_path = os.path.join(path, extension)

        if not os.path.isdir(extended_path):
            os.mkdir(extended_path)

        return extended_path

    @staticmethod
    def __translate_number_of_carriers(num_players):
        return f"Num_Carriers={num_players}"

    @staticmethod
    def __translate_instance_type(generation_strategy, competition_level, num_requests):

        if generation_strategy == GenerationStrategy.BB:

            if competition_level == CompetitionLevel.LOW:
                return f"BB-LOW_{num_requests}"
            elif competition_level == CompetitionLevel.MEDIUM:
                return f"BB-MEDIUM_{num_requests}"
            elif competition_level == CompetitionLevel.HIGH:
                return f"BB-HIGH_{num_requests}"

        elif generation_strategy == GenerationStrategy.GH:

            if competition_level == CompetitionLevel.LOW:
                return f"GH-LOW_{num_requests}"
            elif competition_level == CompetitionLevel.MEDIUM:
                return f"GH-MEDIUM_{num_requests}"
            elif competition_level == CompetitionLevel.HIGH:
                return f"GH-HIGH_{num_requests}"

        elif generation_strategy == GenerationStrategy.Custom:

            if competition_level == CompetitionLevel.LOW:
                return f"LOW_{num_requests}"
            elif competition_level == CompetitionLevel.MEDIUM:
                return f"MEDIUM_{num_requests}"
            elif competition_level == CompetitionLevel.HIGH:
                return f"HIGH_{num_requests}"

    @staticmethod
    def __translate_profitability_type(profitability):

        if profitability == Profitability.HIGH_PROFITABILITY:
            return "Profitability=High"
        elif profitability == Profitability.MEDIUM_PROFITABILITY:
            return "Profitability=Normal"
        elif profitability == Profitability.LOW_PROFITABILITY:
            return "Profitability=Low"

    @staticmethod
    def __translate_profit_sharing_type(profit_sharing_strategy):

        if profit_sharing_strategy == ProfitSharingStrategy.EGALITARIAN:
            return "EGALITARIAN"
        elif profit_sharing_strategy == ProfitSharingStrategy.MODIFIED_EGALITARIAN:
            return "MODIFIED_EGALITARIAN"
        elif profit_sharing_strategy == ProfitSharingStrategy.PURCHASE_SALE_WEIGHT:
            return "PURCHASE_SALE_WEIGHT"
        elif profit_sharing_strategy == ProfitSharingStrategy.CRITICAL_WEIGHT:
            return "CRITICAL_WEIGHT"
        elif profit_sharing_strategy == ProfitSharingStrategy.CRITICAL_WEIGHT_SQUARED:
            return "CRITICAL_WEIGHT_SQUARED"
        elif profit_sharing_strategy == ProfitSharingStrategy.CRITICAL_WEIGHT_CUBIC:
            return "CRITICAL_WEIGHT_CUBIC"
        elif profit_sharing_strategy == ProfitSharingStrategy.SHAPLEY_VALUE:
            return "SHAPLEY_VALUE"

    @staticmethod
    def __translate_bidder_type(strategic_bidder_configuration):

        strategy = strategic_bidder_configuration.strategy

        if strategy == BiddingStrategy.TRUTHFUL:
            return "TRUTHFUL"
        elif strategy == BiddingStrategy.INPUT_MANIPULATION:
            return f"INPUT_MANIPULATION_{strategic_bidder_configuration.input_bid_percentage}"
        elif strategy == BiddingStrategy.HIGH_ABS:
            return f"HIGH_ABS_{strategic_bidder_configuration.all_bid_margin_input_value}"
        elif strategy == BiddingStrategy.BID_MANIPULATION_REL:
            return f"BID_MANIPULATION_REL_{strategic_bidder_configuration.relative_margin}"
        elif strategy == BiddingStrategy.CONSPIRING:
            return "CONSPIRING"

    @staticmethod
    def __translate_conspiring_type(conspiring_bidder_configuration):

        strategies = conspiring_bidder_configuration.strategies

        strategy_string = OutputFileManager.__get_conspiring_strategy_string(strategy=strategies[0])

        remaining_strategies = strategies[1:]
        for strategy in remaining_strategies:
            strategy_string += f"_{OutputFileManager.__get_conspiring_strategy_string(strategy=strategy)}"

        return strategy_string

    """
    *************
    ***PUBLIC***
    *************
    """

    def save_output(self):
        i_config = self.get_input_configuration()
        a_config = self.get_mechanism_manager_configuration()
        p_config = self.get_carrier_configuration()

        output_directory = self.__get_output_directory()

        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)

        num_carriers_type = self.__translate_number_of_carriers(num_players=i_config.num_carriers)
        path = self.__extend_path(path=output_directory, extension=num_carriers_type)

        instance_type = self.__translate_instance_type(generation_strategy=i_config.strategy,
                                                       competition_level=i_config.competition_level,
                                                       num_requests=i_config.num_carrier_requests)
        path = self.__extend_path(path=path, extension=instance_type)

        profitability_type = self.__translate_profitability_type(
            profitability=p_config.profitability)
        path = self.__extend_path(path=path, extension=profitability_type)

        profit_sharing_type = self.__translate_profit_sharing_type(
            profit_sharing_strategy=a_config.payment_calculator_configuration.strategy)
        path = self.__extend_path(path=path, extension=profit_sharing_type)

        bidder_type = self.__translate_bidder_type(
            strategic_bidder_configuration=p_config.strategic_bidder_configuration)
        path = self.__extend_path(path=path, extension=bidder_type)

        if p_config.conspiring_bidder_configuration:
            conspiring_type = self.__translate_conspiring_type(
                conspiring_bidder_configuration=p_config.conspiring_bidder_configuration)

            self.__extend_path(path=path, extension=conspiring_type)

        today = date.today()
        time_date = today.strftime("%d-%m-%Y")

        name = f"RUNS_{i_config.num_runs}_DATE_{time_date}"

        output_dic = self.__get_output_dic()
        file_object = open(f"{path}/{name}.json", "w+")
        json.dump(output_dic, file_object, indent=5)
        file_object.close()

    """
    ************
    ***GETTERS***
    ************
    """

    def get_input_configuration(self):
        return self.input_config

    def get_carrier_configuration(self):
        return self.carrier_config

    def get_other_carriers_configuration(self):
        return self.other_carriers_config

    def get_mechanism_manager_configuration(self):
        return self.mechanism_manager_config

    def get_results(self):
        return self.results

    def get_parent_directory(self):
        return self.parent_directory
