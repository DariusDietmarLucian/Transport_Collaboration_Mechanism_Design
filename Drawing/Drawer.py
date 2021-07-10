import numpy as np
import matplotlib.pyplot as plt


class Drawer:
    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __get_coordinates(locations):
        xs = np.array([loc.get_x() for loc in locations])
        ys = np.array([loc.get_y() for loc in locations])
        return xs, ys

    def __add_indices(self, ax, locations, xs, ys):
        n = np.array([loc.get_id() for loc in locations])
        for i, txt in enumerate(n):
            ax.annotate(txt, (xs[i], ys[i]))

    """
    ************
    ***PUBLIC***
    ************
    """

    def add_edges(self, ax, edges, color):
        for edge in edges:
            start_node = edge[0]
            end_node = edge[1]
            start_pos = start_node.get_coordinates()
            end_pos = end_node.get_coordinates()

            ax.annotate("", xy=end_pos, xytext=start_pos,
                        arrowprops=dict(arrowstyle='->', color=color))

    def add_nodes(self, ax, nodes, color, show_indices):
        locations = [node.get_location() for node in nodes]

        xs, ys = self.__get_coordinates(locations=locations)
        ax.scatter(x=xs, y=ys, color=color)

        if show_indices:
            self.__add_indices(ax=ax, locations=locations, xs=xs, ys=ys)

    def draw_locations(self, locations):
        fig, ax = plt.subplots()
        xs, ys = self.__get_coordinates(locations=locations)
        ax.scatter(x=xs, y=ys, color='blue')

        self.__add_indices(ax=ax, locations=locations, xs=xs, ys=ys)
        plt.show()
