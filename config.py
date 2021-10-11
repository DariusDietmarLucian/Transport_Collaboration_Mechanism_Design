from Instance_Generation.CompetitionLevel import CompetitionLevel
from Instance_Generation.GenerationStrategy import GenerationStrategy
from Mechanism.Request_Selection.RequestSelectionStrategy import RequestSelectionStrategy
from Routing.SolutionStrategy import SolutionStrategy
from Routing.InsertionStrategy import InsertionStrategy
from Routing.RemovalStrategy import RemovalStrategy
from Mechanism.Bidding.Strategic_Bidding.BiddingStrategy import BiddingStrategy
from Mechanism.Bidding.Conspiring_Bidding.ConspiringStrategy import ConspiringStrategy
from Participants.Carrier.Profitability import Profitability
from Mechanism.Bundle_Generation.BundleGeneratorStrategy import BundleGeneratorStrategy
from Mechanism.Payment_Calculation.ProfitSharingStrategy import ProfitSharingStrategy

# parent_directory = None  # Insert your parent_directory for saving data here (for saving input instances and results)
# r101_filepath = None  # Insert your filepath for the r101 data here (if you want to use the Berger&Bierwirth Instance Generation)
parent_directory = "/Users/dariusdresp/Documents/Software/PythonProjects/Auction_based_transport_collaboration"
r101_filepath = "/Users/dariusdresp/Documents/Software/PythonProjects/Auction_based_transport_collaboration/r101"

# -----Instances

instance_generation_configuration = dict(
    competition_level=CompetitionLevel.MEDIUM,
    num_carrier_requests=7,
    num_runs=50,
    num_carriers=5,
    strategy=GenerationStrategy.Custom
)

# -----Mechanism Settings

# Request Selection
request_selector_configuration = dict(
    strategy=RequestSelectionStrategy.COMBO_NEIGH
)

# Bundle Generation
bundle_generator_configuration = dict(
    strategy=BundleGeneratorStrategy.ALL_BUNDLES,
)

ga_bundling_generator_configuration = dict(
    population_size=100,
    number_bundles=600,
    elite_share=0.25,
    rounds=40,
    cross_over_prob=0.3,
    mutate_prob=0.3
)

# Bidding
strategic_bidder_configuration = dict(
    strategy=BiddingStrategy.TRUTHFUL,
    input_bid_percentage=0,
    input_bid_multiple=0,
    relative_margin=1
)

conspiring_bidder_configuration = dict(
    strategies=[ConspiringStrategy.AUTO_COMBO]
)

# Payment Calculation
payment_calculator_configuration = dict(
    strategy=ProfitSharingStrategy.EGALITARIAN
)

# -----Participants Settings

mechanism_manager_configuration = dict(
    num_requests=2,
    num_retries=1
)

carrier_configuration = dict(
    max_capacity=1.3,
    min_num_requests=4,
    profitability=Profitability.HIGH_PROFITABILITY
)

# -----Routing Settings

routing_manager_configuration = dict(
    solution_strategy=SolutionStrategy.DOUBLE_INSERTION,
    insertion_strategy=InsertionStrategy.DOUBLE_INSERTION_2_OPT,
    removal_strategy=RemovalStrategy.SIMPLE_REMOVAL_2_OPT
)
