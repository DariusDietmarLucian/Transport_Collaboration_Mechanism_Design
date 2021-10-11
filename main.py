from Testing.Tester import Tester
from Participants.Carrier.CarrierConfiguration import CarrierConfiguration
from Participants.Mechanism_Manager.MechanismManagerConfiguration import MechanismManagerConfiguration
from Mechanism.Payment_Calculation.PaymentCalculatorConfiguration import PaymentCalculatorConfiguration
from Mechanism.Payment_Calculation.ProfitSharingStrategy import ProfitSharingStrategy
from Mechanism.Bidding.Conspiring_Bidding.ConspiringBidderConfiguration import ConspiringBidderConfiguration
from Mechanism.Bidding.Conspiring_Bidding.ConspiringStrategy import ConspiringStrategy
from Mechanism.Bidding.Strategic_Bidding.StrategicBidderConfiguration import StrategicBidderConfiguration
from Mechanism.Bidding.Strategic_Bidding.BiddingStrategy import BiddingStrategy


#Test smaller margins + Test input manipulation with 0
#INPUT ENTER for SVPM and CWPM

# input_manipulations = [-0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
# absolute_margin_manipulations = [1.5, 2.5].,
# input_manipulations = [0.025, 0.05, 0.075]
# absolute_margin_manipulations = [0.1, 0.5, 1, 2, 3, 10, 100]
relative_margin_manipulations = [0.1, 0.15, 0.2]
# relative_margin_manipulations = [-0.2, -0.1, 0.1, 0.2]
# iso_absolute_margin_manipulations = [0.1, 0.2, 0.3, 0.4, 0.5, 10]

tester = Tester(draws_results=False, saves_results=True)




#
# '''
#
# EGALITARIAN
#
# '''
#
# mm_config = MechanismManagerConfiguration(
#     payment_calculator_configuration=PaymentCalculatorConfiguration(strategy=ProfitSharingStrategy.EGALITARIAN))

# Truthful
# tester.test(mm_config=mm_config)
#
# # Conspiring
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_MAX])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)

# # WIN_LOW
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.WIN_LOW])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)

#
# # Strategic
#
# Input Manipulation
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.INPUT_MANIPULATION,
#                                              input_bid_percentage=manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)

# # Absolute Underbidding
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO,
#                                              input_bid_multiple=-manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)
#
# '''
#
# MODIFIED_EGALITARIAN
#
# '''
#
# mm_config = MechanismManagerConfiguration(
#     payment_calculator_configuration=PaymentCalculatorConfiguration(
#         strategy=ProfitSharingStrategy.MODIFIED_EGALITARIAN))
#
# # Truthful
# tester.test(mm_config=mm_config)
#
# # Conspiring
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_MAX])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)

# # WIN_LOW
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.WIN_LOW])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)

# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_ENTER])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)
#
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.BID_KICKOUT])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)
# #
# # Strategic
#
# Input Manipulation
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.INPUT_MANIPULATION,
#                                              input_bid_percentage=manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)

# Absolute Underbidding
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO,
#                                              input_bid_multiple=-manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)


# '''
#
# PURCHASE_SALE_WEIGHT
#
# '''
#
# mm_config = MechanismManagerConfiguration(
#     payment_calculator_configuration=PaymentCalculatorConfiguration(
#         strategy=ProfitSharingStrategy.PURCHASE_SALE_WEIGHT))
#
# # # Truthful
# tester.test(mm_config=mm_config)
# #
# # # Conspiring/Strategic
# for manipulation in absolute_margin_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS,
#                                              input_bid_multiple=manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)

# '''
#
# CRITICAL_WEIGHT
#
# '''
#
mm_config = MechanismManagerConfiguration(
    payment_calculator_configuration=PaymentCalculatorConfiguration(
        strategy=ProfitSharingStrategy.CRITICAL_WEIGHT))

# Truthful
# tester.test(mm_config=mm_config)

# Conspiring
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_MAX])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)

# # WIN_LOW
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.WIN_LOW])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)

# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.DESTROY_WEIGHT])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)


# Strategic
# for manipulation in iso_absolute_margin_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO, input_bid_multiple=manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)

# Input Manipulation
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.INPUT_MANIPULATION,
#                                              input_bid_percentage=manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)

# # Absolute Underbidding
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO,
#                                              input_bid_multiple=-manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)

# Relative Margin Manipulation
for manipulation in relative_margin_manipulations:
    sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.BID_MANIPULATION_REL,
                                             relative_margin=manipulation)
    c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
    tester.test(mm_config=mm_config, c_config=c_config)


# '''
#
# SHAPLEY_VALUE
#
# '''

mm_config = MechanismManagerConfiguration(
    payment_calculator_configuration=PaymentCalculatorConfiguration(
        strategy=ProfitSharingStrategy.SHAPLEY_VALUE))

# Truthful
# tester.test(mm_config=mm_config)

# Conspiring
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_MAX])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)

# # WIN_LOW
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.WIN_LOW])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)

# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.DESTROY_WEIGHT])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)

# Strategic
# for manipulation in iso_absolute_margin_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO, input_bid_multiple=manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)

# Input Manipulation
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.INPUT_MANIPULATION,
#                                              input_bid_percentage=manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)

# Absolute Underbidding
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO,
#                                              input_bid_multiple=-manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)

# Relative Margin Manipulation
for manipulation in relative_margin_manipulations:
    sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.BID_MANIPULATION_REL,
                                             relative_margin=manipulation)
    c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
    tester.test(mm_config=mm_config, c_config=c_config)


























# #
# # '''
# #
# # EGALITARIAN
# #
# # '''
# #
# mm_config = MechanismManagerConfiguration(
#     payment_calculator_configuration=PaymentCalculatorConfiguration(strategy=ProfitSharingStrategy.EGALITARIAN))
#
# # Truthful
# # tester.test(mm_config=mm_config)
#
# # Conspiring
# # sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# # cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_MAX])
# # c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
# #
# # tester.test(mm_config=mm_config, c_config=c_config)
#
# # WIN_LOW
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.WIN_LOW])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)
#
# #
# # # Strategic
# #
# # # Input Manipulation
# # for manipulation in input_manipulations:
# #     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.INPUT_MANIPULATION,
# #                                              input_bid_percentage=manipulation)
# #     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
# #     tester.test(mm_config=mm_config, c_config=c_config)
#
# # Absolute Underbidding
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO,
#                                              input_bid_multiple=-manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)
# #
# # '''
# #
# # MODIFIED_EGALITARIAN
# #
# # '''
# #
# mm_config = MechanismManagerConfiguration(
#     payment_calculator_configuration=PaymentCalculatorConfiguration(
#         strategy=ProfitSharingStrategy.MODIFIED_EGALITARIAN))
# #
# # # Truthful
# # tester.test(mm_config=mm_config)
# #
# # # Conspiring
# # sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# # cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_MAX])
# # c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
# #
# # tester.test(mm_config=mm_config, c_config=c_config)
#
# # WIN_LOW
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.WIN_LOW])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)
#
# # sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# # cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_ENTER])
# # c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
# #
# # tester.test(mm_config=mm_config, c_config=c_config)
# #
# # sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# # cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.BID_KICKOUT])
# # c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
# #
# # tester.test(mm_config=mm_config, c_config=c_config)
# # #
# # # Strategic
# #
# # # Input Manipulation
# # for manipulation in input_manipulations:
# #     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.INPUT_MANIPULATION,
# #                                              input_bid_percentage=manipulation)
# #     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
# #     tester.test(mm_config=mm_config, c_config=c_config)
#
# # Absolute Underbidding
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO,
#                                              input_bid_multiple=-manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)
#
#
# # '''
# #
# # PURCHASE_SALE_WEIGHT
# #
# # '''
# #
# # mm_config = MechanismManagerConfiguration(
# #     payment_calculator_configuration=PaymentCalculatorConfiguration(
# #         strategy=ProfitSharingStrategy.PURCHASE_SALE_WEIGHT))
# #
# # # # Truthful
# # tester.test(mm_config=mm_config)
# # #
# # # # Conspiring/Strategic
# # for manipulation in absolute_margin_manipulations:
# #     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS,
# #                                              input_bid_multiple=manipulation)
# #     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
# #     tester.test(mm_config=mm_config, c_config=c_config)
#
# # '''
# #
# # CRITICAL_WEIGHT
# #
# # '''
# #
# mm_config = MechanismManagerConfiguration(
#     payment_calculator_configuration=PaymentCalculatorConfiguration(
#         strategy=ProfitSharingStrategy.CRITICAL_WEIGHT))
#
# # Truthful
# # tester.test(mm_config=mm_config)
#
# # Conspiring
# # sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# # cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_MAX])
# # c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
# #
# # tester.test(mm_config=mm_config, c_config=c_config)
#
# # WIN_LOW
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.WIN_LOW])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)
#
# # sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# # cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.DESTROY_WEIGHT])
# # c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
# #
# # tester.test(mm_config=mm_config, c_config=c_config)
#
#
# # Strategic
# # for manipulation in iso_absolute_margin_manipulations:
# #     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO, input_bid_multiple=manipulation)
# #     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
# #     tester.test(mm_config=mm_config, c_config=c_config)
#
# # Input Manipulation
# # for manipulation in input_manipulations:
# #     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.INPUT_MANIPULATION,
# #                                              input_bid_percentage=manipulation)
# #     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
# #     tester.test(mm_config=mm_config, c_config=c_config)
#
# # Absolute Underbidding
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO,
#                                              input_bid_multiple=-manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)
#
# # Relative Margin Manipulation
# # for manipulation in relative_margin_manipulations:
# #     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.BID_MANIPULATION_REL,
# #                                              relative_margin=manipulation)
# #     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
# #     tester.test(mm_config=mm_config, c_config=c_config)
#
#
# # '''
# #
# # SHAPLEY_VALUE
# #
# # '''
#
# mm_config = MechanismManagerConfiguration(
#     payment_calculator_configuration=PaymentCalculatorConfiguration(
#         strategy=ProfitSharingStrategy.SHAPLEY_VALUE))
#
# # Truthful
# # tester.test(mm_config=mm_config)
#
# # Conspiring
# # sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# # cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.INPUT_MAX])
# # c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
# #
# # tester.test(mm_config=mm_config, c_config=c_config)
#
# # WIN_LOW
# sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.WIN_LOW])
# c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
#
# tester.test(mm_config=mm_config, c_config=c_config)
#
# # sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.CONSPIRING)
# # cb_config = ConspiringBidderConfiguration(strategies=[ConspiringStrategy.DESTROY_WEIGHT])
# # c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config, conspiring_bidder_configuration=cb_config)
# #
# # tester.test(mm_config=mm_config, c_config=c_config)
#
# # Strategic
# # for manipulation in iso_absolute_margin_manipulations:
# #     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO, input_bid_multiple=manipulation)
# #     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
# #     tester.test(mm_config=mm_config, c_config=c_config)
#
# # Input Manipulation
# # for manipulation in input_manipulations:
#     # sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.INPUT_MANIPULATION,
#     #                                          input_bid_percentage=manipulation)
#     # c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     # tester.test(mm_config=mm_config, c_config=c_config)
#
# # Absolute Underbidding
# for manipulation in input_manipulations:
#     sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.HIGH_ABS_ISO,
#                                              input_bid_multiple=-manipulation)
#     c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     tester.test(mm_config=mm_config, c_config=c_config)
#
# # Relative Margin Manipulation
# # for manipulation in relative_margin_manipulations:
#     # sb_config = StrategicBidderConfiguration(strategy=BiddingStrategy.BID_MANIPULATION_REL,
#     #                                          relative_margin=manipulation)
#     # c_config = CarrierConfiguration(strategic_bidder_configuration=sb_config)
#     # tester.test(mm_config=mm_config, c_config=c_config)

