import numpy as np
from ortools.linear_solver import pywraplp


class WinnerDeterminator:

    def __init__(self, requests, bundles, bid_matrix):
        self.requests = requests
        self.bundles = bundles
        self.bid_matrix = bid_matrix

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __create_request_in_bundle_matrix(requests, bundles):
        matrix = np.zeros((len(requests), len(bundles)))

        for i, request in enumerate(requests):
            for j, bundle in enumerate(bundles):

                if request in bundle.get_requests():
                    matrix[i][j] = 1

        return matrix

    @staticmethod
    def __select_bids(bid_matrix, request_in_bundle_matrix, enforced_bid_positions=None, forbidden_bid_positions=None):
        solver = pywraplp.Solver.CreateSolver('SCIP')

        num_players = len(bid_matrix)
        num_bundles = len(bid_matrix[0])

        x = {}

        for i in range(num_players):
            for j in range(num_bundles):
                x[i, j] = solver.IntVar(0, 1, '')

        for i in range(num_players):
            for j in range(num_bundles):
                if bid_matrix[i][j].get_valuation() is None:
                    solver.Add(x[i, j] == 0)

        if enforced_bid_positions is not None:
            for pos in enforced_bid_positions:
                solver.Add(x[pos[0], pos[1]] == 1)

        if forbidden_bid_positions is not None:
            for pos in forbidden_bid_positions:
                solver.Add(x[pos[0], pos[1]] == 0)

        # allocate one bundle to each player
        for i in range(num_players):
            solver.Add(solver.Sum([x[i, j] for j in range(num_bundles)]) == 1)

        # allocate each request to some player
        for request_in_bundle in request_in_bundle_matrix:
            solver.Add(solver.Sum(
                x[i, j] * request_in_bundle[j] for j in range(len(request_in_bundle)) for i in range(num_players)) == 1)

        objective_terms = []
        for i in range(num_players):
            for j in range(num_bundles):
                if bid_matrix[i][j].get_valuation() is not None:
                    objective_terms.append(bid_matrix[i][j].get_valuation() * x[i, j])

        solver.Maximize(solver.Sum(objective_terms))

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:

            winning_bids = []

            for i in range(num_players):
                for j in range(num_bundles):
                    if x[i, j].solution_value() > 0.5:
                        winning_bids.append(bid_matrix[i][j])

            return winning_bids

        else:
            return None

    """
    ************
    ***PUBLIC***
    ************
    """

    def determine_winners(self, enforced_bids=None, forbidden_bids=None):
        requests = self.get_requests()
        bundles = self.get_bundles()
        bid_matrix = self.get_bid_matrix()

        request_in_bundle_matrix = self.__create_request_in_bundle_matrix(requests=requests, bundles=bundles)

        enforced_bid_positions = None
        if enforced_bids:
            enforced_bid_positions = []
            for bid in enforced_bids:
                bundle_index = bundles.index(bid.get_bundle())
                player_index = bid.get_carrier_id()
                enforced_bid_pos = (player_index, bundle_index)
                enforced_bid_positions.append(enforced_bid_pos)

        forbidden_bid_positions = None
        if forbidden_bids:
            forbidden_bid_positions = []
            for bid in forbidden_bids:
                bundle_index = bundles.index(bid.get_bundle())
                player_index = bid.get_carrier_id()
                forbidden_bid_pos = (player_index, bundle_index)
                forbidden_bid_positions.append(forbidden_bid_pos)

        winning_bids = self.__select_bids(bid_matrix=bid_matrix, request_in_bundle_matrix=request_in_bundle_matrix,
                                          enforced_bid_positions=enforced_bid_positions, forbidden_bid_positions=forbidden_bid_positions)

        return winning_bids

    """
    ************
    ***GETTERS**
    ************
    """

    def get_bundles(self):
        return self.bundles

    def get_bid_matrix(self):
        return self.bid_matrix

    def get_requests(self):
        return self.requests