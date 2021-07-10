from Testing.Tester import Tester

# Example simple test using the default configurations (from the the config file):
tester = Tester(prints_results=True, draws_results=True, saves_results=False)
tester.test()


# Example of tests with dynamic, customized configurations:
from Participants.Carrier.Profitability import Profitability
from Instance_Generation.InstanceGenerationManagerConfiguration import InstanceGenerationManagerConfiguration
from Participants.Carrier.CarrierConfiguration import CarrierConfiguration


tester = Tester(prints_results=True, draws_results=True, saves_results=False)

profitability_levels = [Profitability.LOW_PROFITABILITY, Profitability.HIGH_PROFITABILITY]
num_carrier_requests = [5, 6, 7]

for profitability in profitability_levels:
    for num_requests in num_carrier_requests:
        i_config = InstanceGenerationManagerConfiguration(num_carrier_requests=num_requests)
        c_config = CarrierConfiguration(profitability=profitability)
        tester.test(i_config=i_config, c_config=c_config)

# Further Configuration Examples

# Instance Generation
from Instance_Generation.InstanceGenerationManagerConfiguration import InstanceGenerationManagerConfiguration
from Instance_Generation.CompetitionLevel import CompetitionLevel
from Instance_Generation.GenerationStrategy import GenerationStrategy

i_config = InstanceGenerationManagerConfiguration(competition_level=CompetitionLevel.MEDIUM, num_carrier_requests=3, num_carriers=3, num_runs=100, strategy=GenerationStrategy.Custom)

#Request Selection
from Mechanism.Request_Selection.RequestSelectorConfiguration import RequestSelectorConfiguration
from Mechanism.Request_Selection.RequestSelectionStrategy import RequestSelectionStrategy

rs_config = RequestSelectorConfiguration(strategy=RequestSelectionStrategy.COMBO_NEIGH)

# Bundle Generation
from Mechanism.Bundle_Generation.BundleGeneratorConfiguration import BundleGeneratorConfiguration
from Mechanism.Bundle_Generation.BundleGeneratorStrategy import BundleGeneratorStrategy
from Mechanism.Bundle_Generation.Genetic_Algorithm_Bundle_Generation.GABundleGeneratorConfiguration import GABundleGeneratorConfiguration

ga_config = GABundleGeneratorConfiguration(population_size=100, number_bundles=1000, elite_share=0.2, rounds=60, cross_over_prob=0.4, mutate_prob=0.3)
bg_config = BundleGeneratorConfiguration(strategy=BundleGeneratorStrategy.BEST_GA_BUNDLES, ga_bundle_generator_configuration=ga_config)

# Bidding
from Mechanism.Bidding.Strategic_Bidding.StrategicBidderConfiguration import StrategicBidderConfiguration
from Mechanism.Bidding.Strategic_Bidding.BiddingStrategy import BiddingStrategy
from Mechanism.Bidding.Conspiring_Bidding.ConspiringBidderConfiguration import ConspiringBidderConfiguration
from Mechanism.Bidding.Conspiring_Bidding.ConspiringStrategy import ConspiringStrategy

sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING, input_bid_percentage=None, input_bid_multiple=None, relative_margin=None)
cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_MAX, ConspiringStrategy.INPUT_ENTER])

# Payment Calculation
from Mechanism.Payment_Calculation.PaymentCalculatorConfiguration import PaymentCalculatorConfiguration
from Mechanism.Payment_Calculation.ProfitSharingStrategy import ProfitSharingStrategy

pc_config = PaymentCalculatorConfiguration(strategy=ProfitSharingStrategy.MODIFIED_EGALITARIAN)

# Routing
from Routing.RoutingManagerConfiguration import RoutingManagerConfiguration
from Routing.SolutionStrategy import SolutionStrategy
from Routing.InsertionStrategy import InsertionStrategy
from Routing.RemovalStrategy import RemovalStrategy

rm_config = RoutingManagerConfiguration(solution_strategy=SolutionStrategy.DOUBLE_INSERTION, insertion_strategy=InsertionStrategy.DOUBLE_INSERTION_2_OPT, removal_strategy=RemovalStrategy.SIMPLE_REMOVAL_2_OPT)

# Mechanism Manager
from Participants.Mechanism_Manager.MechanismManagerConfiguration import MechanismManagerConfiguration

mm_config = MechanismManagerConfiguration(num_requests=3, num_retries=2, is_conspiring=True, payment_calculator_configuration=pc_config, bundle_generator_configuration=bg_config)

# Carrier
from Participants.Carrier.CarrierConfiguration import CarrierConfiguration
from Participants.Carrier.Profitability import Profitability

c_config = CarrierConfiguration(max_capacity=1.3, min_num_requests=4, profitability=Profitability.LOW_PROFITABILITY, routing_manager_configuration=rm_config, request_selector_configuration=rs_config, strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
