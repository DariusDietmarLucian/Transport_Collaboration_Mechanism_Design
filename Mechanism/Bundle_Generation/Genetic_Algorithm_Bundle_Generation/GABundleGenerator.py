"""
Algorithm based on:
Gansterer, M. and Hartl, R.F., 2018. Centralized bundle generation in auction-based collaborative transportation.
Or Spectrum, 40(3), pp.613-635.
"""

from Mechanism.Bundle_Generation.Genetic_Algorithm_Bundle_Generation.CandidateSolution import CandidateSolution
import numpy as np
import bisect
import random


class GABundleGenerator:

    def __init__(self, solver, graph, configuration):
        self.solver = solver
        self.graph = graph
        self.configuration = configuration

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __norm(code):
        norm_dic = {}
        norm_code = ""

        for pos in code:
            if pos not in norm_dic:
                norm_dic[pos] = len(norm_dic)
            norm_code += str(norm_dic[pos])

        return norm_code

    @staticmethod
    def __random_merge(norm_code_string):
        num_bundles = len(set(norm_code_string))

        if num_bundles == 1:
            return norm_code_string

        indices = random.sample(range(num_bundles), 2)

        new_str = ""
        for c in norm_code_string:
            if int(c) == indices[0]:
                new_str += str(indices[1])
            else:
                new_str += c
        return GABundleGenerator.__norm(new_str)

    @staticmethod
    def __delete_duplicates(candidates):
        return list(set(candidates))

    @staticmethod
    def __roulette_index(weights):
        random_number = np.random.random()
        index = bisect.bisect_left(weights, random_number)
        return index

    @staticmethod
    def __bundles_from_candidates(required_bundles, candidates, num_bundles):
        candidates.sort(key=lambda solution: solution.get_score(), reverse=True)

        collected_bundles = required_bundles

        for candidate in candidates:
            bundles = candidate.get_bundles()
            collected = False

            for bundle in bundles:
                if bundle in collected_bundles:
                    collected = True
                    break

            if not collected:
                collected_bundles.extend(bundles)
                if num_bundles <= len(collected_bundles):
                    break

        return collected_bundles

    """
    population generation
    """

    def __initial_population(self, requests, size):

        while True:
            random_code_matrix = np.random.randint(3, size=(size, len(requests)))
            norm_code_matrix = [str(self.__norm(random_code)) for random_code in random_code_matrix]
            if len(set(norm_code_matrix)) == size:
                break

        return norm_code_matrix

    """
    cross-over
    """

    def __cross_over(self, candidates, offspring_size):
        total_score = sum([candidate.get_score() for candidate in candidates])

        weights = []
        weight = 0

        for candidate in candidates:
            weight += candidate.get_score() / total_score
            weights.append(weight)

        weights[-1] = 1.0  # because of rounding errors

        new_candidates = []

        for i in range(offspring_size):

            while True:
                first_index = self.__roulette_index(weights=weights)
                second_index = self.__roulette_index(weights=weights)
                if first_index != second_index:
                    break

            cd = self.__cross(candidate=candidates[first_index], other_candidate=candidates[second_index])
            new_candidates.append(cd)

        return new_candidates

    def __cross(self, candidate, other_candidate):

        if np.random.random() < 0.5:
            return self.__uniform_cross(candidate=candidate, other_candidate=other_candidate)
        else:
            return self.__geo_cross(candidate=candidate, other_candidate=other_candidate)

    def __uniform_cross(self, candidate, other_candidate):
        solver = self.get_solver()
        graph = self.get_graph()

        cs = candidate.get_norm_code_string()
        ocs = other_candidate.get_norm_code_string()

        new_cs = ""

        for i in range(len(cs)):
            if np.random.random() > 0.5:
                new_cs += cs[i]
            else:
                new_cs += ocs[i]

        norm_new_cs = self.__norm(code=new_cs)
        new_candidate = CandidateSolution(norm_code_string=norm_new_cs, requests=candidate.get_requests(),
                                          solver=solver, graph=graph)

        return new_candidate

    def __geo_cross(self, candidate, other_candidate):
        graph = self.get_graph()
        solver = self.get_solver()
        requests = candidate.get_requests()

        a = graph.create_random_point()
        b = graph.create_random_point()

        cs = candidate.get_norm_code_string()
        ocs = other_candidate.get_norm_code_string()
        off_ocs = "".join([str(int(ocs[i]) + 3) for i in range(len(ocs))])

        new_cs = ""

        for i, request in enumerate(requests):
            center = request.get_center()

            a_distance = graph.calculate_point_distance(center, a)
            b_distance = graph.calculate_point_distance(center, b)

            if a_distance < b_distance:
                new_cs += cs[i]
            else:
                new_cs += off_ocs[i]

        norm_new_cs = self.__norm(code=new_cs)

        while len(set(norm_new_cs)) > 3:
            norm_new_cs = self.__random_merge(norm_code_string=norm_new_cs)

        return CandidateSolution(norm_code_string=norm_new_cs, requests=candidate.get_requests(), solver=solver,
                                 graph=graph)

    """
    mutation
    """

    def __mutate(self, candidates):

        mutated_candidates = []

        for candidate in candidates:

            if self.configuration.mutate_prob >= np.random.random():
                random_num = np.random.random()

                if random_num <= 0.25:
                    mutated_candidate = self.__move(candidate=candidate)
                elif random_num <= 0.5:
                    mutated_candidate = self.__join(candidate=candidate)
                elif random_num <= 0.75:
                    mutated_candidate = self.__create(candidate=candidate)
                else:
                    mutated_candidate = self.__shift(candidate=candidate)

                mutated_candidates.append(mutated_candidate)
            else:
                mutated_candidates.append(candidate)

        return mutated_candidates

    def __move(self, candidate):

        norm_code_string = candidate.get_norm_code_string()
        num_bundles = len(set(norm_code_string))
        num_requests = len(norm_code_string)

        num_mutations = random.randint(1, num_requests)
        mut_indices = random.sample(range(num_requests), num_mutations)

        new_code = []

        for i in range(num_requests):
            if i not in mut_indices:
                new_code.append(norm_code_string[i])
            else:
                new_code.append(str(random.randint(0, num_bundles - 1)))

        norm_new_cs = self.__norm(code=new_code)
        return CandidateSolution(norm_code_string=norm_new_cs, requests=candidate.get_requests(),
                                 solver=self.get_solver(), graph=self.get_graph())

    def __create(self, candidate):
        norm_code_string = candidate.get_norm_code_string()
        num_bundles = len(set(norm_code_string))
        num_requests = len(norm_code_string)

        random_request_index = random.randint(0, num_requests - 1)

        new_cs = norm_code_string[:random_request_index] + str(num_bundles) + norm_code_string[
                                                                              random_request_index + 1:]
        norm_new_cs = self.__norm(code=new_cs)

        while len(set(norm_new_cs)) > 3:
            norm_new_cs = self.__random_merge(norm_code_string=norm_new_cs)

        return CandidateSolution(norm_code_string=norm_new_cs, requests=candidate.get_requests(),
                                 solver=self.get_solver(),
                                 graph=self.get_graph())

    def __join(self, candidate):
        norm_code_string = candidate.get_norm_code_string()
        norm_new_cs = self.__random_merge(norm_code_string=norm_code_string)
        return CandidateSolution(norm_code_string=norm_new_cs, requests=candidate.get_requests(),
                                 solver=self.get_solver(),
                                 graph=self.get_graph())

    def __shift(self, candidate):
        centroids = [bundle.get_centroid() for bundle in candidate.get_bundles()]
        requests = candidate.get_requests()
        graph = self.get_graph()

        new_code = []

        for request in requests:
            distances = []
            for i in range(len(centroids)):
                distances.append(graph.calculate_point_distance(request.get_center(), centroids[i]))
            centroid_index = np.argmin(distances)
            new_code.append(centroid_index)

        norm_new_cs = self.__norm(code=new_code)

        return CandidateSolution(norm_code_string=norm_new_cs, requests=requests, solver=self.get_solver(),
                                 graph=graph)

    """
    mating
    """

    def __make_offspring(self, parents):
        offspring_size = int(len(parents) * self.configuration.cross_over_prob)
        offspring = self.__cross_over(candidates=parents, offspring_size=offspring_size)
        mutated_offspring = self.__mutate(candidates=offspring)

        return mutated_offspring

    """
    selection
    """

    def __kill_parents(self, parents, num_kills):
        random.shuffle(parents)
        return parents[num_kills:]

    """
    ************
    ***PUBLIC***
    ************
    """

    def generate_bundles(self, required_bundles, requests):

        # if no more than 10 requests -> genetic algorithm doesn't make sense
        # + initial_population might not be possible
        if len(requests) < 10:
            return None

        solver = self.get_solver()
        graph = self.get_graph()

        population_norm_code = self.__initial_population(requests=requests, size=self.configuration.population_size)
        elite_size = int(self.configuration.population_size * self.configuration.elite_share)

        initial_candidates = []
        for index, code in enumerate(population_norm_code):
            cs = CandidateSolution(norm_code_string=code, requests=requests, solver=solver, graph=graph)
            initial_candidates.append(cs)

        all_candidates = []
        candidates = initial_candidates
        all_candidates.append(candidates)

        for _ in range(self.configuration.rounds):
            candidates = self.__delete_duplicates(candidates=candidates)
            candidates.sort(key=lambda solution: solution.get_score(), reverse=True)

            elite = candidates[:elite_size]
            parents = candidates[elite_size:]

            offspring = self.__make_offspring(parents=parents)
            div_offspring = list(
                set([cd for cd in offspring if cd not in elite and cd not in parents]))  # maintains diversity

            surviving_parents = self.__kill_parents(parents=parents, num_kills=len(div_offspring))

            candidates = elite + div_offspring + surviving_parents

            all_candidates.append(candidates)

        potential_candidates = list(set([candidate for candidates in all_candidates for candidate in candidates]))
        return self.__bundles_from_candidates(required_bundles=required_bundles, candidates=potential_candidates,
                                              num_bundles=self.configuration.number_bundles)

    """
    *************
    ***GETTERS***
    *************
    """

    def get_solver(self):
        return self.solver

    def get_graph(self):
        return self.graph
