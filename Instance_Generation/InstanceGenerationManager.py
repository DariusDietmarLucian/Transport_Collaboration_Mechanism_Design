from Instance_Generation.BB_Instance_Generation.BBGenerator import BBGenerator
from Instance_Generation.GH_Instance_Generation.GHGenerator import GHGenerator
from Instance_Generation.Custom_Instance_Generation.CustomGenerator import CustomGenerator
from Instance_Generation.GenerationStrategy import GenerationStrategy
from File_Management.InputFileManager import InputFileManager

from Models.Node import Node
from Models.Request import Request
from Models.Graph import Graph

import random


class InstanceGenerationManager:

    def __init__(self, parent_directory, configuration):
        self.parent_directory = parent_directory
        self.configuration = configuration

        self.node_id = -1
        self.bb_graph = None
        self.file_manager = None

    """
    *************
    ***PRIVATE***
    *************
    """

    def __generate_node_id(self):
        self.node_id = self.node_id + 1
        return self.node_id

    def __make_new_depots_requests_instances(self):

        depots, requests = self.__generate_depots_requests_instances(num_instances=1000)

        filemanager = self.get_file_manager()
        if filemanager is not None:
            filemanager.write(depots_all_rounds=depots, requests_all_rounds=requests,
                              competition_level=self.configuration.competition_level,
                              generation_strategy=self.configuration.strategy,
                              num_carriers=self.configuration.num_carriers)

        depots = depots[:self.configuration.num_runs]
        requests = requests[:self.configuration.num_runs]

        return depots, requests

    def __rand_requests(self, customer_sites, num_requests):
        random.shuffle(customer_sites)
        requests = []

        for i in range(0, num_requests * 2, 2):
            from_node = Node(id=self.__generate_node_id(), site=customer_sites[i])
            to_node = Node(id=self.__generate_node_id(), site=customer_sites[i + 1])
            request = Request(p_node=from_node, d_node=to_node)
            requests.append(request)

        return requests

    def __make_depots_requests(self, depot_sites, customer_sites, num_carrier_requests):

        depots = []
        requests = []

        for i in range(len(depot_sites)):
            d_site = [ds for ds in depot_sites if ds.area_id == i][0]
            node = Node(id=self.__generate_node_id(), site=d_site)
            depots.append(node)

            c_sites = [cs for cs in customer_sites if cs.area_id == i]
            requests.append(self.__rand_requests(customer_sites=c_sites, num_requests=num_carrier_requests))

        return depots, requests

    def __generate_depots_requests_instances(self, num_instances):
        all_depots = []
        all_requests = []

        for i in range(num_instances):
            self.node_id = -1

            if self.configuration.strategy == GenerationStrategy.BB:
                generator = BBGenerator()
                depot_sites, customer_sites = generator.create_sites(
                    competition_level=self.configuration.competition_level)

            elif self.configuration.strategy == GenerationStrategy.GH:
                generator = GHGenerator()
                depot_sites, customer_sites = generator.create_sites(
                    competition_level=self.configuration.competition_level,
                    num_carrier_requests=self.configuration.num_carrier_requests)

            elif self.configuration.strategy == GenerationStrategy.Custom:
                generator = CustomGenerator(num_carriers=self.configuration.num_carriers)
                depot_sites, customer_sites = generator.create_sites(
                    competition_level=self.configuration.competition_level,
                    num_carrier_requests=self.configuration.num_carrier_requests)

            depots, requests = self.__make_depots_requests(depot_sites=depot_sites, customer_sites=customer_sites,
                                                           num_carrier_requests=self.configuration.num_carrier_requests)
            all_depots.append(depots)
            all_requests.append(requests)

        return all_depots, all_requests

    # for Berger and Bierwirth (BB) 2009 always the same locations are used (distance graph stays the same)
    def __get_bb_graph(self):
        if self.bb_graph is None:
            bb_filereader = BBGenerator()
            locations = bb_filereader.get_locations()
            self.bb_graph = Graph(locations=locations)

        return self.bb_graph

    def __get_new_graph(self, depots, requests):
        depot_sites = [depot.get_site() for depot in depots]
        requests = [request for carrier_requests in requests for request in carrier_requests]
        customer_nodes = [node for request in requests for node in
                          [request.get_pickup_node(), request.get_delivery_node()]]
        customer_sites = [node.get_site() for node in customer_nodes]
        sites = (depot_sites + customer_sites)
        locations = list(set([site.get_location() for site in sites]))

        return Graph(locations=locations)

    def __make_graphs(self, depots_instances, requests_instances):
        graph_instances = []

        if self.configuration.strategy == GenerationStrategy.GH or self.configuration.strategy == GenerationStrategy.Custom:
            for i in range(len(depots_instances)):
                graph = self.__get_new_graph(depots=depots_instances[i], requests=requests_instances[i])
                graph_instances.append(graph)

        elif self.configuration.strategy == GenerationStrategy.BB:
            for i in range(len(depots_instances)):
                graph = self.__get_bb_graph()
                graph_instances.append(graph)

        return graph_instances

    """
    ************
    ***PUBLIC***
    ************
    """

    def get_instances(self):
        filemanager = self.get_file_manager()

        if filemanager is not None:
            depots_instances, requests_instances = filemanager.read(num_runs=self.configuration.num_runs,
                                                                num_requests=self.configuration.num_carrier_requests,
                                                                competition_level=self.configuration.competition_level,
                                                                generation_strategy=self.configuration.strategy,
                                                                num_carriers=self.configuration.num_carriers)

            if depots_instances is None or requests_instances is None:
                depots_instances, requests_instances = self.__make_new_depots_requests_instances()
        else:
            depots_instances, requests_instances = self.__make_new_depots_requests_instances()

        graph_instances = self.__make_graphs(depots_instances=depots_instances, requests_instances=requests_instances)

        return depots_instances, requests_instances, graph_instances

    """
    ************
    ***GETTERS***
    ************
    """

    def get_parent_directory(self):
        return self.parent_directory

    def get_file_manager(self):
        if self.file_manager is None:
            parent_directory = self.get_parent_directory()
            if parent_directory is None:
                return None
            self.file_manager = InputFileManager(parent_directory=parent_directory)

        return self.file_manager
