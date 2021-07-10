from Mechanism.Winner_Determination.WinnerDeterminator import WinnerDeterminator
from Mechanism.Payment_Calculation.PaymentCalculator import PaymentCalculator
from Mechanism.Payment_Calculation.ProfitSharingStrategy import ProfitSharingStrategy
from Mechanism.Bidding.Conspiring_Bidding.ConspiringStrategy import ConspiringStrategy

from Models.Bid import Bid


class ConspiringBidder:

    def __init__(self, player_id, other_player_ids, configuration):
        self.player_id = player_id
        self.other_player_ids = other_player_ids
        self.configuration = configuration

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __exchange_bid(bundle_bids, new_bid):
        new_bundle_bids = bundle_bids.copy()

        for index, bid in enumerate(bundle_bids):
            if bid.get_bundle() == new_bid.get_bundle():
                new_bundle_bids[index] = new_bid

        return new_bundle_bids

    @staticmethod
    def __update_input_bids(old_input_bid, new_input_bid, input_bids, bundle_bids):
        new_bundle_bids = ConspiringBidder.__exchange_bid(bundle_bids=bundle_bids, new_bid=new_input_bid)
        new_input_bids = [new_input_bid if bid == old_input_bid else bid for bid in input_bids]
        return new_input_bids, new_bundle_bids

    @staticmethod
    def __gen_input_bid_max(input_bid, winning_bids_value, determinator):

        forced_winning_bids = determinator.determine_winners(enforced_bids=[input_bid])
        forced_winning_bids_value = sum([bid.get_valuation() for bid in forced_winning_bids])

        value_difference = winning_bids_value - forced_winning_bids_value - 1

        if value_difference < 0:
            return input_bid
        else:
            new_input_bid = Bid(bundle=input_bid.get_bundle(), valuation=input_bid.get_valuation() + value_difference,
                                player_id=input_bid.get_carrier_id())
            return new_input_bid

    @staticmethod
    def __gen_input_bid_enter(input_bid, input_bids, winning_bids, determinator):

        winning_bids_value = sum([bid.get_valuation() for bid in winning_bids])

        alt_winning_bids = determinator.determine_winners(forbidden_bids=[input_bid])
        alt_winning_bids_value = sum([bid.get_valuation() for bid in alt_winning_bids])

        value_difference = winning_bids_value - alt_winning_bids_value + 1

        new_share = PaymentCalculator.calculate_egalitarian_share(player_id=input_bid.get_carrier_id(), input_bids=input_bids,
                                                                  winning_bids=alt_winning_bids, requires_contribution=True)

        new_input_bid = Bid(bundle=input_bid.get_bundle(), valuation=input_bid.get_valuation() - value_difference,
                            player_id=input_bid.get_carrier_id())

        new_input_bids = [new_input_bid if bid == input_bid else bid for bid in input_bids]
        new_collaboration_gain = alt_winning_bids_value - sum([bid.get_valuation() for bid in new_input_bids])

        marginal_profit = new_share * new_collaboration_gain - value_difference

        if marginal_profit > 0:
            return new_input_bid, alt_winning_bids
        else:
            return input_bid, winning_bids

    @staticmethod
    def __gen_bids_destroy(player_id, other_player_ids, input_bids, winning_bids, determinator, bundle_bids):

        winning_bids_value = sum([bid.get_valuation() for bid in winning_bids])
        input_bid = next(bid for bid in input_bids if bid.get_carrier_id() == player_id)
        winning_bid = next(bid for bid in winning_bids if bid.get_carrier_id() == player_id)

        destruction_bids = []

        for o_player_id in other_player_ids:
            max_reachable_valuation = None
            o_input_bid = next(bid for bid in input_bids if bid.get_carrier_id() == o_player_id)
            destruction_bid = None
            set_o_requests = set(o_input_bid.get_requests())

            for bid in bundle_bids:

                if bid == input_bid or bid == winning_bid or not bid.get_valuation():
                    continue

                set_requests = set(bid.get_requests())

                if len(set_o_requests.intersection(set_requests)) > 0:
                    continue

                alt_winning_bids = determinator.determine_winners(enforced_bids=[o_input_bid, bid])

                if alt_winning_bids is None:
                    continue

                alt_winning_bids_value = sum([bid.get_valuation() for bid in alt_winning_bids])

                other_winning_bids = determinator.determine_winners(enforced_bids=[bid])
                other_winning_bids_value = sum([bid.get_valuation() for bid in other_winning_bids])

                value_difference = winning_bids_value - other_winning_bids_value - 1
                reachable_valuation = alt_winning_bids_value + value_difference

                if max_reachable_valuation is None or reachable_valuation > max_reachable_valuation:
                    max_reachable_valuation = reachable_valuation

                    destruction_bid = Bid(bundle=bid.get_bundle(),
                                          valuation=bid.get_valuation() + value_difference,
                                          player_id=player_id)

                    if max_reachable_valuation >= (winning_bids_value - 1):
                        break

            if destruction_bid is not None:
                destruction_bids.append(destruction_bid)

        return destruction_bids

    @staticmethod
    def __gen_bid_kickout(player_id, other_player_ids, input_bids, winning_bids, determinator):

        winning_bids_value = sum([bid.get_valuation() for bid in winning_bids])
        input_bids_value = sum([bid.get_valuation() for bid in input_bids])
        collaboration_gain = winning_bids_value - input_bids_value
        current_share = PaymentCalculator.calculate_egalitarian_share(player_id=player_id, input_bids=input_bids,
                                                                      winning_bids=winning_bids, requires_contribution=True)

        max_collaboration_share_gain = (0.5 - current_share) * collaboration_gain

        best_marginal_gain_found = 0
        kickout_bid = None

        for o_player_id in other_player_ids:
            o_input_bid = next(bid for bid in input_bids if bid.get_carrier_id() == o_player_id)
            tried_bids = []

            while True:

                alt_winning_bids = determinator.determine_winners(enforced_bids=[o_input_bid],
                                                                  forbidden_bids=tried_bids)
                alt_winning_bids_value = sum([bid.get_valuation() for bid in alt_winning_bids])

                new_share = PaymentCalculator.calculate_egalitarian_share(player_id=player_id, input_bids=input_bids,
                                                                          winning_bids=alt_winning_bids,
                                                                          requires_contribution=True)

                value_difference = winning_bids_value - alt_winning_bids_value + 1
                marginal_gain = (new_share - current_share) * collaboration_gain - value_difference
                player_winner_bid = next(bid for bid in alt_winning_bids if bid.get_carrier_id() == player_id)

                if marginal_gain > best_marginal_gain_found:

                    other_bids = determinator.determine_winners(enforced_bids=[player_winner_bid])
                    other_winning_bids_value = sum([bid.get_valuation() for bid in other_bids])

                    if alt_winning_bids_value >= other_winning_bids_value:
                        best_marginal_gain_found = marginal_gain
                        kickout_bid = Bid(bundle=player_winner_bid.get_bundle(),
                                          valuation=player_winner_bid.get_valuation() + value_difference,
                                          player_id=player_id)
                        winning_bids = [kickout_bid if bid == player_winner_bid else bid for bid in alt_winning_bids]
                        break

                elif max_collaboration_share_gain < value_difference:
                    break

                tried_bids.append(player_winner_bid)

        return kickout_bid, winning_bids

    @staticmethod
    def play_input_max(player_id, input_bids, winning_bids, bundle_bids, determinator):
        input_bid = next(bid for bid in input_bids if bid.get_carrier_id() == player_id)
        winning_bids_value = sum([bid.get_valuation() for bid in winning_bids])
        new_input_bid = ConspiringBidder.__gen_input_bid_max(input_bid=input_bid, winning_bids_value=winning_bids_value,
                                                             determinator=determinator)
        if new_input_bid != input_bid:
            new_input_bids, new_bundle_bids = ConspiringBidder.__update_input_bids(old_input_bid=input_bid,
                                                                                   new_input_bid=new_input_bid,
                                                                                   input_bids=input_bids,
                                                                                   bundle_bids=bundle_bids)
            return new_input_bids, new_bundle_bids
        else:
            return input_bids, bundle_bids

    @staticmethod
    def play_input_enter(player_id, input_bids, winning_bids, bundle_bids, determinator):
        winning_bids_value = sum([bid.get_valuation() for bid in winning_bids])
        input_bids_value = sum([bid.get_valuation() for bid in input_bids])

        if winning_bids_value <= input_bids_value:
            return input_bids, winning_bids, bundle_bids

        current_share = PaymentCalculator.calculate_egalitarian_share(player_id=player_id, input_bids=input_bids,
                                                                      winning_bids=winning_bids,
                                                                      requires_contribution=True)
        if current_share > 0:
            return input_bids, winning_bids, bundle_bids

        input_bid = next(bid for bid in input_bids if bid.get_carrier_id() == player_id)
        new_input_bid, new_winning_bids = ConspiringBidder.__gen_input_bid_enter(input_bid=input_bid,
                                                                                 input_bids=input_bids,
                                                                                 winning_bids=winning_bids,
                                                                                 determinator=determinator)
        if new_input_bid != input_bid:
            new_input_bids, new_bundle_bids = ConspiringBidder.__update_input_bids(old_input_bid=input_bid,
                                                                                   new_input_bid=new_input_bid,
                                                                                   input_bids=input_bids,
                                                                                   bundle_bids=bundle_bids)
            return new_input_bids, new_winning_bids, new_bundle_bids
        else:
            return input_bids, winning_bids, bundle_bids

    @staticmethod
    def play_bid_kickout(player_id, other_player_ids, input_bids, winning_bids, bundle_bids, determinator):
        winning_bids_value = sum([bid.get_valuation() for bid in winning_bids])
        input_bids_value = sum([bid.get_valuation() for bid in input_bids])

        if winning_bids_value <= input_bids_value:
            return winning_bids, bundle_bids

        current_share = PaymentCalculator.calculate_egalitarian_share(player_id=player_id, input_bids=input_bids,
                                                                      winning_bids=winning_bids,
                                                                      requires_contribution=True)
        if current_share >= 0.5:
            return winning_bids, bundle_bids

        kickout_bid, new_winning_bids = ConspiringBidder.__gen_bid_kickout(player_id=player_id,
                                                                           other_player_ids=other_player_ids,
                                                                           input_bids=input_bids,
                                                                           winning_bids=winning_bids,
                                                                           determinator=determinator)
        if kickout_bid is not None:
            new_bundle_bids = ConspiringBidder.__exchange_bid(bundle_bids=bundle_bids, new_bid=kickout_bid)
            return new_winning_bids, new_bundle_bids
        else:
            return winning_bids, bundle_bids

    @staticmethod
    def play_bids_destroy(player_id, other_player_ids, input_bids, winning_bids, bundle_bids, determinator):
        winning_bids_value = sum([bid.get_valuation() for bid in winning_bids])
        input_bids_value = sum([bid.get_valuation() for bid in input_bids])

        if winning_bids_value <= input_bids_value:
            return bundle_bids

        destruction_bids = ConspiringBidder.__gen_bids_destroy(player_id=player_id,
                                                               other_player_ids=other_player_ids,
                                                               input_bids=input_bids,
                                                               winning_bids=winning_bids,
                                                               determinator=determinator,
                                                               bundle_bids=bundle_bids)
        if destruction_bids:

            new_bundle_bids = bundle_bids
            for bid in destruction_bids:
                new_bundle_bids = ConspiringBidder.__exchange_bid(bundle_bids=new_bundle_bids, new_bid=bid)

            return new_bundle_bids

        else:
            return bundle_bids

    @staticmethod
    def get_combo_strategies(profit_sharing_strategy):

        if profit_sharing_strategy == ProfitSharingStrategy.EGALITARIAN:
            return [ConspiringStrategy.INPUT_MAX]
        elif profit_sharing_strategy == ProfitSharingStrategy.MODIFIED_EGALITARIAN:
            return [ConspiringStrategy.INPUT_MAX, ConspiringStrategy.INPUT_ENTER, ConspiringStrategy.BID_KICKOUT]
        elif profit_sharing_strategy == ProfitSharingStrategy.CRITICAL_WEIGHT:
            return [ConspiringStrategy.INPUT_MAX, ConspiringStrategy.DESTROY_WEIGHT]
        elif profit_sharing_strategy == ProfitSharingStrategy.CRITICAL_WEIGHT_SQUARED:
            return [ConspiringStrategy.INPUT_MAX, ConspiringStrategy.DESTROY_WEIGHT]
        elif profit_sharing_strategy == ProfitSharingStrategy.CRITICAL_WEIGHT_CUBIC:
            return [ConspiringStrategy.INPUT_MAX, ConspiringStrategy.DESTROY_WEIGHT]
        elif profit_sharing_strategy == ProfitSharingStrategy.PURCHASE_SALE_WEIGHT:
            return None
        elif profit_sharing_strategy == ProfitSharingStrategy.SHAPLEY_VALUE:
            return [ConspiringStrategy.INPUT_MAX]
        else:
            return None

    """
    ************
    ***PUBLIC***
    ************
    """

    def __make_new_bids(self, input_bids, winning_bids, bundle_bids, determinator, strategies):
        player_id = self.get_player_id()
        other_player_ids = self.get_other_player_ids()

        if ConspiringStrategy.INPUT_MAX in strategies:
            input_bids, bundle_bids = ConspiringBidder.play_input_max(player_id=player_id, input_bids=input_bids,
                                                                      winning_bids=winning_bids,
                                                                      bundle_bids=bundle_bids,
                                                                      determinator=determinator)

        if ConspiringStrategy.INPUT_ENTER in strategies:
            input_bids, winning_bids, bundle_bids = ConspiringBidder.play_input_enter(player_id=player_id,
                                                                                      input_bids=input_bids,
                                                                                      winning_bids=winning_bids,
                                                                                      bundle_bids=bundle_bids,
                                                                                      determinator=determinator)

        if ConspiringStrategy.BID_KICKOUT in strategies:
            winning_bids, bundle_bids = ConspiringBidder.play_bid_kickout(player_id=player_id,
                                                                          other_player_ids=other_player_ids,
                                                                          input_bids=input_bids,
                                                                          winning_bids=winning_bids,
                                                                          bundle_bids=bundle_bids,
                                                                          determinator=determinator)

        if ConspiringStrategy.DESTROY_WEIGHT in strategies:
            bundle_bids = ConspiringBidder.play_bids_destroy(player_id=player_id, other_player_ids=other_player_ids,
                                                             input_bids=input_bids, winning_bids=winning_bids,
                                                             bundle_bids=bundle_bids, determinator=determinator)

        input_bid = next(bid for bid in input_bids if bid.get_carrier_id() == player_id)

        return input_bid, bundle_bids

    def get_conspired_bids(self, input_bids, bundles, bid_matrix, profit_sharing_strategy):

        strategies = self.configuration.strategies
        player_id = self.get_player_id()
        bundle_bids = bid_matrix[player_id]

        if strategies is None:
            return None, None
        if ConspiringStrategy.AUTO_COMBO in strategies:
            strategies = self.get_combo_strategies(profit_sharing_strategy=profit_sharing_strategy)

        requests = [request for bid in input_bids for request in bid.get_requests()]
        determinator = WinnerDeterminator(requests=requests, bundles=bundles, bid_matrix=bid_matrix)

        winning_bids = determinator.determine_winners()
        winning_bids_value = sum([bid.get_valuation() for bid in winning_bids])
        input_bids_value = sum([bid.get_valuation() for bid in input_bids])

        if winning_bids_value <= input_bids_value:
            return None, None

        return self.__make_new_bids(input_bids=input_bids, winning_bids=winning_bids, bundle_bids=bundle_bids,
                                  determinator=determinator, strategies=strategies)

    """
    *************
    ***GETTERS***
    *************
    """

    def get_player_id(self):
        return self.player_id

    def get_other_player_ids(self):
        return self.other_player_ids
