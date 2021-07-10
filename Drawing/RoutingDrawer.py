import numpy as np
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt

from Drawing.Drawer import Drawer


class RoutingDrawer(Drawer):

    """
    *************
    ***PRIVATE***
    *************
    """

    def __add_depot_rqsts(self, ax, depot, requests, color):
        request_nodes = np.array([[request.p_node, request.d_node] for request in requests])

        self.add_nodes(ax=ax, nodes=np.concatenate(request_nodes), color='gray', show_indices=True)
        self.add_nodes(ax=ax, nodes=[depot], color=color, show_indices=True)
        self.add_edges(ax=ax, edges=request_nodes, color=color)

    def __add_route(self, ax, route, color, show_indices=True):
        depot_nodes = [route[0]]
        customer_nodes = route[1:-1]
        edges = []

        for index in range(len(route) - 1):
            edge = [route[index], route[index + 1]]
            edges.append(edge)
        edge = [route[-1], route[0]]
        edges.append(edge)

        self.add_nodes(ax=ax, nodes=depot_nodes, color=color, show_indices=show_indices)
        self.add_nodes(ax=ax, nodes=customer_nodes, color='gray', show_indices=show_indices)
        self.add_edges(ax=ax, edges=edges, color=color)

    """
    ************
    ***PUBLIC***
    ************
    """

    def draw_single_depot_requests(self, depot, requests):
        fig, ax = plt.subplots()
        self.__add_depot_rqsts(ax=ax, depot=depot, requests=requests, color='red')
        plt.show()

    def draw_multiple_depot_requests(self, depots, requests):
        fig, ax = plt.subplots()
        colors = cm.rainbow(np.linspace(0, 1, len(depots)))

        for i, c in enumerate(colors):
            self.__add_depot_rqsts(ax=ax, depot=depots[i], requests=requests[i], color=c)

        plt.show()

    def draw_single_route(self, route):
        fig, ax = plt.subplots()
        self.__add_route(ax=ax, route=route, color='blue')
        plt.show()

    def draw_multiple_routes_chained(self, routes):
        fig, ax_array = plt.subplots(len(routes), 1)

        for i, ax in enumerate(np.ravel(ax_array)):
            self.__add_route(ax=ax, route=routes[i], color='blue')

        plt.show()

    def draw_multiple_routes_in_one(self, routes):
        fig, ax = plt.subplots()
        colors = cm.rainbow(np.linspace(0, 1, len(routes)))

        for i, c in enumerate(colors):
            self.__add_route(ax=ax, route=routes[i], color=c)

        plt.show()

    def draw_routes_before_after(self, comparable_routes, show_indices=True):
        fig, ax_array = plt.subplots(2, 1)

        ax_array[0].title.set_text('Decentralized Routing Solution Before Exchange')
        ax_array[1].title.set_text('Decentralized Routing Solution After Exchange')

        for i in range(len(ax_array)):
            colors = cm.rainbow(np.linspace(0, 1, len(comparable_routes[i])))
            for j, c in enumerate(colors):
                self.__add_route(ax=ax_array[i], route=comparable_routes[i][j], color=c, show_indices=show_indices)

        plt.show()

    def draw_depots_requests_routes(self, depots, requests, routes):
        fig, ax_array = plt.subplots(len(routes), 2)
        colors = cm.rainbow(np.linspace(0, 1, len(routes)))

        for i in range(len(ax_array)):
            self.__add_depot_rqsts(ax=ax_array[i][0], depot=depots[i], requests=requests[i], color=colors[i])
            self.__add_route(ax=ax_array[i][1], route=routes[i], color=colors[i])

        plt.show()
