from Models.RequestBundle import RequestBundle


class CandidateSolution:

    def __init__(self, norm_code_string, requests, solver, graph):
        self.norm_code_string = norm_code_string
        self.requests = requests
        self.solver = solver
        self.graph = graph

        self.bundles = None
        self.score = None
        self.isolation = None
        self.max_tour_length = None
        self.density = None

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __assign_requests(norm_code_string, requests):
        num_bundles = len(set(norm_code_string))

        bundle_requests = [[] for _ in range(num_bundles)]
        for index, pos in enumerate(norm_code_string):
            bundle_requests[int(pos)].append(requests[index])

        return bundle_requests

    @staticmethod
    def __calc_min_isolation(bundles):

        isolation = None

        if len(bundles) == 1:
            return 1

        for i in range(len(bundles) - 1):
            for j in range(i + 1, len(bundles)):
                sv = bundles[i].get_separation_value(other_bundle=bundles[j])
                if isolation is None or sv < isolation:
                    isolation = sv

        return isolation

    @staticmethod
    def __calc_min_density(bundles):
        return min([bundle.get_density() for bundle in bundles])

    @staticmethod
    def __calc_max_tour_length(bundles):
        return max([bundle.get_tour_length() for bundle in bundles])

    def __assign_bundles(self):
        norm_cs = self.get_norm_code_string()
        requests = self.get_requests()

        bundle_requests = CandidateSolution.__assign_requests(norm_code_string=norm_cs, requests=requests)

        solver = self.get_solver()
        graph = self.get_graph()

        bundles = []
        for rqsts in bundle_requests:
            bundles.append(RequestBundle(requests=rqsts, solver=solver, graph=graph))

        return bundles

    def __calc_score(self):
        min_isolation = self.get_isolation()
        min_density = self.get_density()
        max_tour_length = self.get_max_tour_length()

        return (min_isolation * min_density) / (max_tour_length * len(self.get_bundles()))

    """
    *************
    ***GETTERS***
    *************
    """

    def get_graph(self):
        return self.graph

    def get_solver(self):
        return self.solver

    def get_bundles(self):
        if self.bundles is None:
            self.bundles = self.__assign_bundles()
        return self.bundles

    def get_requests(self):
        return self.requests

    def get_max_tour_length(self):
        if self.max_tour_length is None:
            self.max_tour_length = self.__calc_max_tour_length(bundles=self.get_bundles())
        return self.max_tour_length

    def get_density(self):
        if self.density is None:
            self.density = self.__calc_min_density(bundles=self.get_bundles())
        return self.density

    def get_isolation(self):
        if self.isolation is None:
            self.isolation = self.__calc_min_isolation(bundles=self.get_bundles())
        return self.isolation

    def get_score(self):
        if self.score is None:
            self.score = self.__calc_score()
        return self.score

    def get_norm_code_string(self):
        return self.norm_code_string

    """
    **************
    ***CONFORMS***
    **************
    """

    def __eq__(self, other):
        return self.norm_code_string == other.get_norm_code_string()

    def __hash__(self):
        return hash(('code', self.norm_code_string))
