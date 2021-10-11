## Introduction

Logistic carriers face the challenge of fulfilling delivery requests for several customers.
Thus, they have to solve routing problems. If the carriers exchanged requests between each other,
they could improve the respective routing solutions. The exchange of requests can be implemented through
an auction-based mechanism (see [Berger, S. and Bierwirth, C., 2010. Solutions to the request reassignment problem in collaborative carrier networks.](https://doi.org/10.1016/j.tre.2009.12.006))

## Auction-based Mechanism
The basic steps of the auction-based mechanism are:
1) Request Selection = Each carrier has to decide which requests to offer
2) Bundling = The offered requests have to be bundled into packages
3) Bidding = The carriers have to bid prices on the packages
4) Winner Determination = The best bids have to be selected
5) Payment Calculation = The payment to and from each carrier has to be determined

All of the steps are topic of ongoing research.

For an overview of the theoretical foundations, please take a look at the presentation "MasterPresentation_Darius_Dresp.pdf".

## Purpose
The purpose of the program is to develop and test the auction-based mechanism with various configurations.
In particular, the program was used to test the potential for strategic manipulation during the bidding phase.

## Test Setup

The default configurations for a test are saved in the config.py file. 
In addition, it is possible to change the configuration of a test by passing customized configurations as parameters.

*Example of conducting a test with default configurations*
```python:
from Testing.Tester import Tester

tester = Tester(prints_results=True, draws_results=True, saves_results=False)
tester.test()
```

*Example of conducting a test with customized configurations*
```python:
from Testing.Tester import Tester
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
```

On the high level, you can customize the following configurations and pass them as parameters:
1) i_config = Configuration for the Instance Generation 
2) mm_config = Configuration for the Mechanism Manager
3) c_config = Configuration for the Carrier with index 0 (used for strategic evaluation)
4) oc_config = Configuration for the remaining Carriers

- for i_config see Configurations->Instance Generation
- for mm_config see Configurations->Participants->Mechanism Manager
- for c_config and oc_config see Configurations->Participants->Carrier

## Configurations

### Instance Generation
1) Competition level, i.e. the overlap of pickup/delivery locations between carriers 
    - LOW
    - MEDIUM
    - HIGH
2) Number of requests per carriers (initially)
3) Number of carriers
4) Number of test runs
5) Strategy, i.e. how instances are generated
    - According to [Berger, S. and Bierwirth, C., 2010. Solutions to the request reassignment problem in collaborative carrier networks.](https://doi.org/10.1016/j.tre.2009.12.006)
    - According to [Gansterer, M. and Hartl, R.F., 2016. Request evaluation strategies for carriers in auction-based collaborations.](https://doi.org/10.1007/s00291-015-0411-1)
    - Custom, new method (**has to be used if the number of carriers are not 3!**)

*Example*  
```python:
from Instance_Generation.InstanceGenerationManagerConfiguration import InstanceGenerationManagerConfiguration
from Instance_Generation.CompetitionLevel import CompetitionLevel
from Instance_Generation.GenerationStrategy import GenerationStrategy

i_config = InstanceGenerationManagerConfiguration(competition_level=CompetitionLevel.MEDIUM, num_carrier_requests=3, num_carriers=3, num_runs=100, strategy=GenerationStrategy.Custom)
```

### Mechanism

#### Request Selection
1) Strategy, i.e. how to select requests
    - MIN_PROFIT
    - CLUSTER
    - COMBO
    - COMBO_NEIGH
   
According to [Gansterer, M. and Hartl, R.F., 2016. Request evaluation strategies for carriers in auction-based collaborations.](https://doi.org/10.1007/s00291-015-0411-1)

*Example*
```python:
from Mechanism.Request_Selection.RequestSelectorConfiguration import RequestSelectorConfiguration
from Mechanism.Request_Selection.RequestSelectionStrategy import RequestSelectionStrategy

rs_config = RequestSelectorConfiguration(strategy=RequestSelectionStrategy.COMBO_NEIGH)
```

#### Bundle Generation
1) Strategy, i.e. how bundles should be generated
    - All possible bundles are generated
    - Best bundles are generated through a genetic algorithm according to 
    [Gansterer, M. and Hartl, R.F., 2018. Centralized bundle generation in auction-based collaborative transportation.](https://doi.org/10.1007/s00291-018-0516-4)
2) Genetic Algorithm Configuration (only important if you actually use the genetic algorithm for bundle generation)

*Genetic Algorithm Configuration*
1) Size of the population
2) Number of bundles that should be generated
3) Share of the population that should be considered elite
4) Number of rounds that the algorithm should run before termination
5) Probability of cross-over
6) Probability of mutation

*Example*
```python:
from Mechanism.Bundle_Generation.BundleGeneratorConfiguration import BundleGeneratorConfiguration
from Mechanism.Bundle_Generation.BundleGeneratorStrategy import BundleGeneratorStrategy
from Mechanism.Bundle_Generation.Genetic_Algorithm_Bundle_Generation.GABundleGeneratorConfiguration import GABundleGeneratorConfiguration

ga_config = GABundleGeneratorConfiguration(population_size=100, number_bundles=1000, elite_share=0.2, rounds=60, cross_over_prob=0.4, mutate_prob=0.3)
bg_config = BundleGeneratorConfiguration(strategy=BundleGeneratorStrategy.BEST_GA_BUNDLES, ga_bundle_generator_configuration=ga_config)
```


#### Bidding
*Conspiring Biddinng Configuration*
1) Strategies, i.e. which conspiring strategies should be used
    - AUTO_COMB0 (automatically selects the most promising)
    - INPUT_MAX
    - INPUT_ENTER
    - BID_KICKOUT
    - DESTROY_WEIGHT

(please see "MasterPresentation_Darius_Dresp.pdf")

*Strategic Bidding Configuration*
1) Strategy, i.e. which bidding strategy should be used
    - TRUTHFUL
    - INPUT_MANIPULATION
    - HIGH_ABS
    - BID_MANIPULATION_REL
    - CONSPIRING
2) Input bid manipulation as percentage of the real input bid value (important if you use INPUT_MANIPULATION)
3) Absolute bid manipulation as multiple of the real input bid value (important if you use HIGH_ABS)
4) Relative bid manipulation as percentage of the real value of the respective bid (important if you use BID_MANIPULATION_REL)

(please see "MasterPresentation_Darius_Dresp.pdf")

*Example*
```python:
from Mechanism.Bidding.Strategic_Bidding.StrategicBidderConfiguration import StrategicBidderConfiguration
from Mechanism.Bidding.Strategic_Bidding.BiddingStrategy import BiddingStrategy
from Mechanism.Bidding.Conspiring_Bidding.ConspiringBidderConfiguration import ConspiringBidderConfiguration
from Mechanism.Bidding.Conspiring_Bidding.ConspiringStrategy import ConspiringStrategy

sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING, input_bid_percentage=None, input_bid_multiple=None, relative_margin=None)
cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_MAX, ConspiringStrategy.INPUT_ENTER])
```

#### Winner Determination
No configuration available. Always solved optimally as a set-partitioning problem with [Google OR-Tools](https://developers.google.com/optimization/mip/integer_opt)

#### Payment Calculation
1) Strategy, i.e. how the collaboration gain should be shared between carriers
    - EGALITARIAN 
    - PURCHASE_SALE_WEIGHT according to [Pushing frontiers in auction-based transport collaborations](https://doi.org/10.1016/j.omega.2019.01.011)
    - MODIFIED_EGALITARIAN
    - CRITICAL_WEIGHT
    - CRITICAL_WEIGHT_SQUARED
    - CRITICAL_WEIGHT_CUBIC
    - SHAPLEY_VALUE according to [Shapley, L.S., 2016. 17. A value for n-person games](https://doi.org/10.1515/9781400881970-018)
    
(please see "MasterPresentation_Darius_Dresp.pdf")

*Example*
```python:
from Mechanism.Payment_Calculation.PaymentCalculatorConfiguration import PaymentCalculatorConfiguration
from Mechanism.Payment_Calculation.ProfitSharingStrategy import ProfitSharingStrategy

pc_config = PaymentCalculatorConfiguration(strategy=ProfitSharingStrategy.MODIFIED_EGALITARIAN)
```

### Routing
1) Solution strategy, i.e. how to find the initial routing solution
    - DOUBLE_INSERTION according to [Renaud, J., Boctor, F.F. and Ouenniche, J., 2000. A heuristic for the pickup and delivery traveling salesman problem.](https://doi.org/10.1016/S0305-0548(99)00066-0)
    - GOOGLE_PATH_CHEAPEST_ARC
    - GOOGLE_LOCAL_CHEAPEST_ARC
    - GOOGLE_PARALLEL_CHEAPEST_INSERTION
2) Insertion strategy, i.e. how to insert requests in an existing routing solution
    - NEW_ROUTE (calculate new route according to the solution strategy)
    - DOUBLE_INSERTION_NO_OPT (this time, just inserting in the existing solution)
    - DOUBLE_INSERTION_2_OPT
    - DOUBLE_INSERTION_3_OPT
    - CHEAP_INSERTION_NO_OPT
    - CHEAP_INSERTION_2_OPT
    - CHEAP_INSERTION_3_OPT
    - CHEAP_INSERTION_GOOGLE_PATH_CHEAPEST_ARC (this time, passes the initial solution to OR-Tools)
    - CHEAP_INSERTION_GOOGLE_LOCAL_CHEAPEST_ARC
    - CHEAP_INSERTION_GOOGLE_PARALLEL_CHEAPEST_INSERTION
 3) Removal strategy, i.e. how to remove requests from an existing routing solution
    - NEW_ROUTE (calculate new route according to the solution strategy)
    - SIMPLE_REMOVAL_NO_OPT (just removes the nodes without changing the remaining routing solution)
    - SIMPLE_REMOVAL_2_OPT
    - SIMPLE_REMOVAL_3_OPT
 

- GOOGLE solutions and references: [Google OR-TOOLS, Routing Options](https://developers.google.com/optimization/routing/routing_options)
- CHEAP_INSERTION, in contrast to DOUBLE_INSERTION, calculates the insertion of the pickup and delivery node of a request sequentially -> Faster, but less optimal 
- Improvement phases (2_OPT, 3_OPT) according to [Lin, S., 1965. Computer solutions of the traveling salesman problem.](https://doi.org/10.1002/j.1538-7305.1965.tb04146.x)
- Easy extensions: >3_OPT (since {x}-OPT improvement-phase is coded generically) and inclusion of other Google OR-Tools solution strategies 

*Example*
```python:
from Routing.RoutingManagerConfiguration import RoutingManagerConfiguration
from Routing.SolutionStrategy import SolutionStrategy
from Routing.InsertionStrategy import InsertionStrategy
from Routing.RemovalStrategy import RemovalStrategy

rm_config = RoutingManagerConfiguration(solution_strategy=SolutionStrategy.DOUBLE_INSERTION, insertion_strategy=InsertionStrategy.DOUBLE_INSERTION_2_OPT, removal_strategy=RemovalStrategy.SIMPLE_REMOVAL_2_OPT)
```

### Participants

#### Mechanism Manager
1) Number of requests traded each round for each carrier
2) Number of retries if no improvement can be found after a round
3) Payment Calculation configuration (see above)
4) Bundle Generation configuration (see above)

*Example*
```{python}
from Participants.Mechanism_Manager.MechanismManagerConfiguration import MechanismManagerConfiguration

mm_config = MechanismManagerConfiguration(num_requests=3, num_retries=2, payment_calculator_configuration=pc_config, bundle_generator_configuration=bg_config)
```

#### Carrier
1) Maximum distance capacity of a routing solution in terms of percentage of the initial routing solution's distance
2) Minimum number of requests that should be withhold 
3) Profitability 
     - LOW_PROFITABILITY
     - MEDIUM_PROFITABILITY
     - HIGH_PROFITABILITY (same as [Berger, S. and Bierwirth, C., 2010. Solutions to the request reassignment problem in collaborative carrier networks.](https://doi.org/10.1016/j.tre.2009.12.006))
4) Routing configuration (see above)
5) Request Selection configuration (see above)
6) Strategic Bidding configuration (see above)
7) Conspiring Bidding configuration (see above)

*Example*
```python:
from Participants.Carrier.CarrierConfiguration import CarrierConfiguration
from Participants.Carrier.Profitability import Profitability

c_config = CarrierConfiguration(max_capacity=1.3, min_num_requests=4, profitability=Profitability.LOW_PROFITABILITY, routing_manager_configuration=rm_config, request_selector_configuration=rs_config, strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
```
## Input/Output Data
For real tests it might be necessary to save the input and output data.
If you want to save the input/output data, please state the parent_directory that you want to use in the config.py file.
In addition, set the parameter "saves_results" to True.

```python:
from Testing.Tester import Tester

tester = Tester(saves_results=True)
tester.test()
```

The input and output data will now be saved in JSON-format.

Also, the saved instances will now be reused if possible.
This will make the results more comparable.


## License
No License. Please ask for permission if you want to share the code. Only to read/run on your own.
