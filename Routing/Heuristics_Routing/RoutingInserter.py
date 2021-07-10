import random


class RoutingInserter:

    def __init__(self, graph):
        self.graph = graph

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __calc_insert_request_dist(graph, request, index, route):

        start_dist = graph.calculate_node_distance(node=route[index], other_node=request.get_pickup_node())
        dir_dist = request.get_distance()
        end_dist = graph.calculate_node_distance(node=request.get_delivery_node(), other_node=route[index + 1])

        old_distance = graph.calculate_node_distance(node=route[index], other_node=route[index + 1])

        return start_dist + dir_dist + end_dist - old_distance

    @staticmethod
    def __calc_insert_node_dist(graph, node, index, route):

        start_dist = graph.calculate_node_distance(node=route[index], other_node=node)
        end_dist = graph.calculate_node_distance(node=node, other_node=route[index + 1])

        old_distance = graph.calculate_node_distance(node=route[index], other_node=route[index + 1])

        return start_dist + end_dist - old_distance

    @staticmethod
    def __calc_min_insrt(graph, route, node):
        min_distance = None

        for i in range(len(route) - 1):
            distance = RoutingInserter.__calc_insert_node_dist(graph=graph, node=node, index=i, route=route)

            if min_distance is None or distance < min_distance:
                min_distance = distance
                insert_index = i + 1

        return min_distance, insert_index

    @staticmethod
    def __calc_min_consq_insrt(graph, route, request):
        min_distance = None

        for i in range(len(route) - 1):
            distance = RoutingInserter.__calc_insert_request_dist(graph=graph, request=request, index=i, route=route)

            if min_distance is None or distance < min_distance:
                min_distance = distance
                insert_pickup_index = i + 1
                insert_delivery_index = i + 2

        return min_distance, insert_pickup_index, insert_delivery_index

    @staticmethod
    def __calc_min_non_consq_insrt(graph, route, request):
        min_distance = None

        for i in range(len(route) - 2):
            p_node = request.get_pickup_node()
            pickup_distance = RoutingInserter.__calc_insert_node_dist(graph=graph, node=p_node, index=i, route=route)

            for j in range(i + 1, len(route) - 1):
                d_node = request.get_delivery_node()
                delivery_distance = RoutingInserter.__calc_insert_node_dist(graph=graph, node=d_node, index=j,
                                                                            route=route)
                distance = pickup_distance + delivery_distance

                if min_distance is None or distance < min_distance:
                    min_distance = distance
                    insert_pickup_index = i + 1
                    insert_delivery_index = j + 2

        return min_distance, insert_pickup_index, insert_delivery_index

    """
    ************
    ***PUBLIC***
    ************
    """

    """
    cheap insert (sequential approach -> faster):
    
    1) insert pickup-node at cheapest position
    2) insert delivery-node at cheapest position
    """

    def calculate_cheap_insert_single(self, route, request):
        graph = self.get_graph()

        # Case if the route is empty (besides of the depot node which is always at the end and beginning)
        if len(route) == 2:
            return [route[0], request.get_pickup_node(), request.get_delivery_node(), route[1]]

        new_route = route.copy()

        p_node = request.get_pickup_node()
        pickup_insert_distance, insert_pickup_index = self.__calc_min_insrt(graph=graph, route=route, node=p_node)
        new_route.insert(insert_pickup_index, request.get_pickup_node())

        remaining_route = new_route[insert_pickup_index:]
        d_node = request.get_delivery_node()
        delivery_insert_distance, insert_delivery_index = self.__calc_min_insrt(graph=graph, route=remaining_route,
                                                                                node=d_node)
        new_route.insert(insert_pickup_index + insert_delivery_index, request.get_delivery_node())

        return new_route

    def calculate_cheap_insert_multiple(self, route, requests, random_sequence=False):

        if random_sequence:
            random.shuffle(requests)

        new_route = route.copy()

        for request in requests:
            new_route = self.calculate_cheap_insert_single(route=new_route, request=request)

        return new_route

    """
    double insert (simultaneous approach -> more accurate):

    1) insert pickup-node and delivery-node at their cheapest position
    """

    def calculate_double_insert_single(self, route, request):

        graph = self.get_graph()

        # Case if the route is empty (besides of the depot node which is always at the end and beginning)
        if len(route) == 2:
            return [route[0], request.get_pickup_node(), request.get_delivery_node(), route[1]]

        new_route = route.copy()

        min_conseq_dist, p_id_c, d_id_c = self.__calc_min_consq_insrt(graph=graph, route=route, request=request)
        min_non_conseq_dist, p_id_nc, d_id_nc = self.__calc_min_non_consq_insrt(graph=graph, route=route,
                                                                                request=request)

        if min_conseq_dist < min_non_conseq_dist:
            new_route.insert(p_id_c, request.get_pickup_node())
            new_route.insert(d_id_c, request.get_delivery_node())
            return new_route
        else:
            new_route.insert(p_id_nc, request.get_pickup_node())
            new_route.insert(d_id_nc, request.get_delivery_node())
            return new_route

    def calculate_double_insert_multiple(self, route, requests, random_sequence=False):

        if random_sequence:
            random.shuffle(requests)

        new_route = route.copy()

        for request in requests:
            new_route = self.calculate_double_insert_single(route=new_route, request=request)

        return new_route

    """
    *************
    ***GETTERS***
    *************
    """

    def get_graph(self):
        return self.graph
