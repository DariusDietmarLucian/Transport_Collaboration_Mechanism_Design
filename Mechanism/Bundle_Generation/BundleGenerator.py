from itertools import compress, product
from Models.RequestBundle import RequestBundle
from Mechanism.Bundle_Generation.Genetic_Algorithm_Bundle_Generation.GABundleGenerator import GABundleGenerator
from Mechanism.Bundle_Generation.BundleGeneratorStrategy import BundleGeneratorStrategy


class BundleGenerator:

    def __init__(self, input_bids, solver, graph, configuration):
        self.input_bids = input_bids
        self.solver = solver
        self.graph = graph
        self.configuration = configuration

        self.requests = None

    """
    ************
    ***PRIVATE***
    ************
    """

    @staticmethod
    def __compose_all_bundles(requests, solver, graph):

        composed_requests = list(
            list(compress(requests, mask)) for mask in list(product(range(2), repeat=len(requests))))
        bundles = []

        for requests in composed_requests:
            bundles.append(RequestBundle(requests=requests, solver=solver, graph=graph))

        return bundles

    """
    ************
    ***PUBLIC***
    ************
    """

    def generate_bundles(self):
        requests = self.get_requests()
        solver = self.get_solver()
        graph = self.get_graph()

        if self.configuration.strategy == BundleGeneratorStrategy.ALL_BUNDLES:
            bundles = self.__compose_all_bundles(requests=requests, solver=solver, graph=graph)
        elif self.configuration.strategy == BundleGeneratorStrategy.BEST_GA_BUNDLES:
            generator = GABundleGenerator(solver=solver, graph=graph,
                                          configuration=self.configuration.ga_bundle_generator_configuration)
            input_bids = self.get_input_bids()
            # collected request bundles from all players (ensures feasibility)
            required_bundles = [bid.get_bundle() for bid in input_bids]
            # empty request bundle (not every player needs to get a request)
            required_bundles.append(RequestBundle(requests=[], solver=solver, graph=graph))
            bundles = generator.generate_bundles(required_bundles=required_bundles, requests=requests)
            if bundles is None:
                bundles = self.__compose_all_bundles(requests=requests, solver=solver, graph=graph)

        return bundles

    """
    *************
    ***GETTERS***
    *************
    """

    def get_input_bids(self):
        return self.input_bids

    def get_requests(self):
        if self.requests is None:
            input_bids = self.get_input_bids()
            return [request for bid in input_bids for request in bid.get_requests()]

        return self.requests

    def get_solver(self):
        return self.solver

    def get_graph(self):
        return self.graph
