import numpy as np
from Python_Extensions.TranslatorDict import TranslatorDict


class GoogleRoutingTranslator:

    def __init__(self, depot, requests, graph):
        self.depot = depot
        self.requests = requests
        self.graph = graph

        self.nodes = None
        self.translation_matrix = None
        self.translation_dictionary = None

    """
    *************
    ***PRIVATE***
    *************
    """

    """
    Function: __bloat_and_cut_matrix(self, dist_matrix, nodes):
    -> Bloat the matrix, i.e. copy the matrix rows and columns for node duplicates 
    -> Translate each iteration to a node because the iteration index will correspond to the node's position in the cut matrix
    -> Cut the matrix, i.e. delete the matrix rows and columns of nodes that aren't included
     
    """

    @staticmethod
    def __bloat_and_cut_matrix(dist_matrix, nodes):
        # Assumption: location_ids correspond to the positions in the dist_matrix
        sorted_nodes = sorted(nodes, key=lambda node: node.get_location_id())

        bloated_matrix = dist_matrix
        bloated_indices = []
        translator_dic = TranslatorDict()

        previous_id = -1
        number_of_bloats = 0

        for index, node in enumerate(sorted_nodes):
            if node.get_location_id() == previous_id:
                number_of_bloats += 1
                bloated_index = node.get_location_id() + number_of_bloats
                bloated_matrix = np.insert(bloated_matrix, bloated_index, bloated_matrix[:, bloated_index - 1], axis=1)
                bloated_matrix = np.insert(bloated_matrix, bloated_index, bloated_matrix[bloated_index - 1, :], axis=0)
                bloated_indices.append(bloated_index)
            else:
                bloated_index = node.get_location_id() + number_of_bloats
                bloated_indices.append(bloated_index)

            translator_dic[index] = node
            previous_id = node.get_location_id()

        cut_matrix = bloated_matrix[bloated_indices, :][:, bloated_indices]

        return cut_matrix, translator_dic

    @staticmethod
    def __get_transl_requests(transl_dic, requests):
        return [(transl_dic[request.p_node], transl_dic[request.d_node]) for request in requests]

    @staticmethod
    def __get_transl_depot(transl_dic, depot):
        return transl_dic[depot]

    """
    ************
    ***Public***
    ************
    """

    def translate_matrix_depot_requests(self):
        transl_dic = self.get_translation_dictionary()
        depot = self.get_depot()
        requests = self.get_requests()

        return (self.get_translation_matrix(),
                self.__get_transl_depot(transl_dic=transl_dic, depot=depot),
                self.__get_transl_requests(transl_dic=transl_dic, requests=requests))

    def translate_route_from_google(self, route):
        node_route = []
        transl_dic = self.get_translation_dictionary()

        for index in route:
            node_route.append(transl_dic[index])

        node_route.append(transl_dic[route[0]])

        return node_route

    def translate_route_to_google(self, route):
        shortened_route = route[1:-1].copy()
        index_route = []
        transl_dic = self.get_translation_dictionary()

        for node in shortened_route:
            index_route.append(transl_dic[node])

        return index_route

    """
    *************
    ***GETTERS***
    *************
    """

    def get_depot(self):
        return self.depot

    def get_requests(self):
        return self.requests

    def get_graph(self):
        return self.graph

    def get_nodes(self):
        if self.nodes is None:
            self.nodes = [node for nodes_pair in [[request.p_node, request.d_node] for request in self.get_requests()]
                          for node in nodes_pair]

            self.nodes.append(self.get_depot())

        return self.nodes

    def get_translation_matrix(self):
        if self.translation_matrix is None:
            graph = self.get_graph()
            nodes = self.get_nodes()
            self.translation_matrix, self.translation_dictionary = self.__bloat_and_cut_matrix(
                graph.get_distance_matrix(), nodes)

        return self.translation_matrix

    def get_translation_dictionary(self):
        if self.translation_dictionary is None:
            graph = self.get_graph()
            nodes = self.get_nodes()
            self.translation_matrix, self.translation_dictionary = self.__bloat_and_cut_matrix(
                graph.get_distance_matrix(), nodes)

        return self.translation_dictionary
