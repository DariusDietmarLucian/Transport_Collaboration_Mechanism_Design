"""
Based on:
Lin, S., 1965. Computer solutions of the traveling salesman problem. Bell System Technical Journal, 44(10), pp.2245-2269.
"""


class RoutingOptimizer:

    cut_combis = {}
    cuts_and_glues = {}

    def __init__(self, graph):
        self.graph = graph

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __get_cut_combis(len_route, k_opt):

        # a cut spot is a pair of two consecutive nodes in a route
        # between those nodes an edge could be removed
        cut_spots = [(i, i + 1) for i in range(len_route - 1)]
        return RoutingOptimizer.__cut(cut_spots=cut_spots, num_cuts=k_opt, initial_length=len(cut_spots))

    @staticmethod
    def __cut(cut_spots, num_cuts, initial_length):

        if num_cuts == 1:
            return [[cut_spot] for cut_spot in cut_spots]

        all_cut_combis = []
        for i in range(len(cut_spots) - (2 * num_cuts - 2)):

            # Because a route has the following structure [depot, node, ..., depot]
            # -> we shouldn't cut at the very first and last edge (because contiguous cuts aren't allowed)
            if i == 0 and len(cut_spots) == initial_length:
                new_cut_combis = RoutingOptimizer.__cut(cut_spots[(i + 2):-1], num_cuts - 1, initial_length)
            else:
                new_cut_combis = RoutingOptimizer.__cut(cut_spots[(i + 2):], num_cuts - 1, initial_length)

            all_cut_combis = all_cut_combis + [([cut_spots[i]] + cut_combi) for cut_combi in new_cut_combis]

        return all_cut_combis

    # an arrangement is simply a way to permutate a list of indices
    # but: 2-tuples of consecutive indices can't be split (only reversed)
    @staticmethod
    def __bld_arrangements(indices):

        if len(indices) == 2:
            return [indices, list(reversed(indices))]
        else:
            combinations = []

            for i in range(0, len(indices), 2):
                remaining_indices = [indices[j] for j in range(len(indices)) if (j != i and j != (i + 1))]
                ends = RoutingOptimizer.__bld_arrangements(remaining_indices)

                start = [indices[i], indices[i + 1]]
                combinations.extend([(start + end) for end in ends])

                other_start = [indices[i + 1], indices[i]]
                combinations.extend([(other_start + end) for end in ends])

        return combinations

    # cut defines the position where indices of a list are split (deleted connection)
    # glue defines the position where indices of a list are reconnected (added connection)
    # -> number of cuts and glues has to be the same (every split of indices needs to be followed by a reconnection)
    # k_opt defines the max number of cuts that we allow
    @staticmethod
    def __get_generic_cuts_and_glues(k_opt):

        old_path = list(range(0, 2 * k_opt))
        old_connections = [(old_path[i], old_path[i + 1]) for i in range(0, len(old_path), 2)]

        arrangements = RoutingOptimizer.__bld_arrangements(old_path[1:-1])
        new_paths = [[old_path[0]] + arrangement + [old_path[-1]] for arrangement in arrangements]

        cuts_and_glues = []
        for new_path in new_paths:
            new_connections = [(new_path[i], new_path[i + 1]) for i in range(0, len(new_path), 2)]
            added_connections = [con for con in new_connections if con not in old_connections]
            deleted_connections = [con for con in old_connections if con not in new_connections]

            if not added_connections and not deleted_connections:
                continue
            else:
                cuts_and_glues.append((deleted_connections, added_connections))

        return cuts_and_glues

    @staticmethod
    def __get_superior_routes(graph, route, cut_candidates, cuts_and_glues):

        nodes = [route[i] for spot in cut_candidates for i in spot]
        node_dic = {i: node for i, node in enumerate(nodes)}

        indices = [index for spot in cut_candidates for index in spot]
        index_dic = {i: index for i, index in enumerate(indices)}

        superior_routes = []

        # For efficiency (to avoid calculating the delete distance for k_opt moves redundantly)
        max_del_distance = sum(
            [graph.calculate_node_distance(node=route[spot[0]], other_node=route[spot[1]]) for spot in cut_candidates])

        for cuts_and_glues in cuts_and_glues:

            if len(cuts_and_glues[0]) == len(cut_candidates):
                del_distance = max_del_distance
            else:
                del_distance = sum(
                    [graph.calculate_node_distance(node=node_dic[cut[0]], other_node=node_dic[cut[1]]) for cut in
                     cuts_and_glues[0]])

            add_distance = sum(
                [graph.calculate_node_distance(node=node_dic[glue[0]], other_node=node_dic[glue[1]]) for glue in
                 cuts_and_glues[1]])

            if del_distance > add_distance:
                glues = [(index_dic[glue[0]], index_dic[glue[1]]) for glue in cuts_and_glues[1]]
                superior_route = RoutingOptimizer.__bld_route(route=route, glues=glues)
                superior_routes.append(superior_route)

        return superior_routes

    @staticmethod
    def __bld_route(route, glues):
        new_route = route[:glues[0][0] + 1].copy()

        for i in range(0, len(glues) - 1):
            if glues[i][1] > glues[i + 1][0]:
                new_route = new_route + list(reversed(route[glues[i + 1][0]:glues[i][1] + 1]))
            else:
                new_route = new_route + route[glues[i][1]:glues[i + 1][0] + 1]

        new_route = new_route + route[glues[-1][1]:]
        return new_route

    @staticmethod
    def __is_route_feasible(route, requests):

        for request in requests:
            p_node = request.get_pickup_node()
            d_node = request.get_delivery_node()

            p_index = next((i for i, node in enumerate(route) if p_node.id == node.id), -1)
            d_index = next((i for i, node in enumerate(route) if d_node.id == node.id), -1)

            if p_index > d_index:
                return False

        return True

    @staticmethod
    def __find_improvement(graph, org_route, requests, cut_combis, cuts_and_glues):
        route = org_route.copy()
        # random.Random(4).shuffle(cut_combis) #set seed to produce comparable results

        for cut_candidates in cut_combis:
            superior_routes = RoutingOptimizer.__get_superior_routes(graph, route, cut_candidates, cuts_and_glues)

            if superior_routes is None:
                continue

            for i, superior_route in enumerate(superior_routes):

                if RoutingOptimizer.__is_route_feasible(superior_route, requests):
                    return superior_route

        return None

    """
    ************
    ***PUBLIC***
    ************
    """

    def optimize(self, route, requests, k_opt):

        current_route = route.copy()
        graph = self.get_graph()

        cut_combis = self.get_cut_combis(len_route=len(route), k_opt=k_opt)
        cuts_and_glues = self.get_cuts_and_glues(k_opt=k_opt)

        while True:
            superior_route = self.__find_improvement(graph=graph, org_route=current_route, requests=requests,
                                                cut_combis=cut_combis, cuts_and_glues=cuts_and_glues)
            if superior_route is None:
                break
            else:
                current_route = superior_route.copy()

        return current_route

    """
    *************
    ***GETTERS***
    *************
    """

    def get_graph(self):
        return self.graph

    def get_cut_combis(self, len_route, k_opt):
        key = f"({str(len_route)}, {str(k_opt)})"
        if key not in self.cut_combis:
            self.cut_combis[key] = self.__get_cut_combis(len_route=len_route, k_opt=k_opt)

        return self.cut_combis[key]

    def get_cuts_and_glues(self, k_opt):
        if k_opt not in self.cuts_and_glues:
            self.cuts_and_glues[k_opt] = self.__get_generic_cuts_and_glues(k_opt=k_opt)

        return self.cuts_and_glues[k_opt]
