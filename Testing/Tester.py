from Drawing.RoutingDrawer import RoutingDrawer
from File_Management.OutputFileManager import OutputFileManager
from Participants.ParticipantsFactory import ParticipantsFactory
import time
import config


class Tester:

    def __init__(self, prints_results=True, draws_results=True, saves_results=False):
        self.prints_results = prints_results
        self.draws_results = draws_results
        self.saves_results = saves_results

        self.iterations = []
        self.computation_times = []

        self.old_distances = []
        self.old_profits = []
        self.old_routes = []

        self.new_distances = []
        self.new_profits = []
        self.new_routes = []

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __calc_absolute_margins(old_values, new_values):
        matrix = []

        for i in range(len(new_values)):
            margins = []
            for j in range(len(new_values[i])):
                margins.append(new_values[i][j] - old_values[i][j])
            matrix.append(margins)

        return matrix

    @staticmethod
    def __calc_relative_margins(old_values, new_values):
        matrix = []

        for i in range(len(new_values)):
            margins = []
            for j in range(len(new_values[i])):
                margins.append(new_values[i][j] / old_values[i][j])  # old_value should usually not be 0
            matrix.append(margins)

        return matrix

    @staticmethod
    def __calc_absolute_collab_margins(old_values, new_values):
        absolute_collaboration_gains = []

        for index in range(len(new_values)):
            total_old = sum(old_values[index])
            total_new = sum(new_values[index])
            absolute_collaboration_gains.append(total_new - total_old)

        return absolute_collaboration_gains

    @staticmethod
    def __calc_relative_collab_margins(old_values, new_values):
        relative_collaboration_gains = []

        for index in range(len(new_values)):
            total_old = sum(old_values[index])
            total_new = sum(new_values[index])
            relative_collaboration_gains.append(total_new / total_old)  # total_old should usually not be 0

        return relative_collaboration_gains

    @staticmethod
    def __calc_averages(matrix):
        averages = []

        for j in range(len(matrix[0])):
            total = 0
            for i in range(len(matrix)):
                total += matrix[i][j]
            averages.append(total / len(matrix))

        return averages

    @staticmethod
    def __calc_total_relatives(old_values, new_values):
        total_relatives = []

        for j in range(len(old_values[0])):
            old_value = 0
            new_value = 0
            for i in range(len(old_values)):
                old_value += old_values[i][j]
                new_value += new_values[i][j]
            total_relatives.append(new_value / old_value)  # old_value should usually not be 0

        return total_relatives

    @staticmethod
    def __calc_total_collab_relative(old_values, new_values):
        total_old = sum([value for values in old_values for value in values])
        total_new = sum([value for values in new_values for value in values])
        return total_new / total_old

    def __run(self, all_participants):

        run_index = 0

        for i in range(len(all_participants)):
            print(f"run = {run_index}")

            mechanism_manager = all_participants[i][0]
            carriers = all_participants[i][1]

            self.__memorize_carriers_changes(carriers=carriers, before_trade=True)

            start_time = time.time()
            extra_profit, iterations = mechanism_manager.start_managing_trade()
            computation_time = time.time() - start_time

            self.__memorize_mechanism_meta(computation_time=computation_time, iterations=iterations)
            self.__memorize_carriers_changes(carriers=carriers, before_trade=False)

            run_index += 1

    """
    memorize calculated outputs
    """

    def __memorize_carriers_changes(self, carriers, before_trade):

        if before_trade:
            self.old_distances.append([carrier.get_current_route_distance() for carrier in carriers])
            self.old_profits.append([carrier.get_total_profit() for carrier in carriers])
            self.old_routes.append([carrier.get_current_route() for carrier in carriers])
        else:
            self.new_distances.append([carrier.get_current_route_distance() for carrier in carriers])
            self.new_profits.append([carrier.get_total_profit() for carrier in carriers])
            self.new_routes.append([carrier.get_current_route() for carrier in carriers])

    def __memorize_mechanism_meta(self, computation_time, iterations):
        self.computation_times.append(computation_time)
        self.iterations.append(iterations)

    """
    Output actions
    """

    def __print_results(self):
        print("--------------------------------------------------------------------")
        print(f"average computation time = {self.get_average_computation_time()}")
        print(f"average iterations = {self.get_average_iterations()}")
        print("---------------------------------------------------------------------")
        print(f"relative marginal distances = {self.get_total_relative_marginal_distances()}")
        print(f"total relative collaboration distance gain = {self.get_total_relative_collaboration_distance_gain()}")
        print("---------------------------------------------------------------------")
        print(f"relative marginal profits = {self.get_total_relative_marginal_profits()}")
        print(f"total relative collaboration profit gain = {self.get_total_relative_collaboration_profit_gain()}")
        print("---------------------------------------------------------------------")
        print(f"average absolute collaboration gain = {self.get_average_absolute_collaboration_profit_gain()}")
        print(f"average absolute distance gain = {self.get_average_absolute_collaboration_distance_gain()}")
        print(f"total distance = {sum([distance for distances in self.new_distances for distance in distances])}")

    def __draw_results(self):
        old_routes, new_routes = self.get_routes()
        drawer = RoutingDrawer()

        for i in range(len(old_routes)):
            drawer.draw_routes_before_after([old_routes[i], new_routes[i]], True)

    def __save_results(self, i_config=None, mm_config=None, c_config=None, oc_config=None):
        if config.parent_directory is None:
            print("you need to define a parent_directory to save the results")
            return

        results = self.get_results()
        output_manager = OutputFileManager(input_config=i_config, carrier_config=c_config,
                                           other_carriers_config=oc_config,
                                           mechanism_manager_config=mm_config, results=results,
                                           parent_directory=config.parent_directory)
        output_manager.save_output()

    """
    ************
    ***PUBLIC***
    ************
    """

    def test(self, i_config=None, mm_config=None, c_config=None, oc_config=None):

        mechanism_factory = ParticipantsFactory(instance_generation_config=i_config, mechanism_manager_config=mm_config,
                                                carrier_config=c_config,
                                                other_carriers_config=oc_config)
        all_participants = mechanism_factory.create_all_participants()
        self.__run(all_participants=all_participants)

        if self.get_prints_results():
            self.__print_results()

        if self.get_draws_results():
            self.__draw_results()

        if self.get_saves_results():
            self.__save_results(i_config=i_config, mm_config=mm_config, c_config=c_config, oc_config=oc_config)

    """
    *************
    ***GETTERS***
    *************
    """

    def get_prints_results(self):
        return self.prints_results

    def get_draws_results(self):
        return self.draws_results

    def get_saves_results(self):
        return self.saves_results

    def get_old_distances(self):
        return self.old_distances

    def get_new_distances(self):
        return self.new_distances

    def get_old_profits(self):
        return self.old_profits

    def get_new_profits(self):
        return self.new_profits

    def get_old_routes(self):
        return self.old_routes

    def get_new_routes(self):
        return self.new_routes

    def get_routes(self):
        return self.old_routes, self.new_routes

    """
    Absolutes
    """

    def get_iterations(self):
        return self.iterations

    def get_computation_times(self):
        return self.computation_times

    def get_absolute_marginal_distances(self):
        old_distances = self.get_old_distances()
        new_distances = self.get_new_distances()
        return self.__calc_absolute_margins(old_values=old_distances, new_values=new_distances)

    def get_absolute_marginal_profits(self):
        old_profits = self.get_old_profits()
        new_profits = self.get_new_profits()
        return self.__calc_absolute_margins(old_values=old_profits, new_values=new_profits)

    def get_absolute_collaboration_distance_gains(self):
        old_distances = self.get_old_distances()
        new_distances = self.get_new_distances()
        return self.__calc_absolute_collab_margins(old_values=old_distances, new_values=new_distances)

    def get_absolute_collaboration_profit_gains(self):
        old_profits = self.get_old_profits()
        new_profits = self.get_new_profits()
        return self.__calc_absolute_collab_margins(old_values=old_profits, new_values=new_profits)

    """
    Relatives
    """

    def get_relative_marginal_distances(self):
        old_distances = self.get_old_distances()
        new_distances = self.get_new_distances()
        return self.__calc_relative_margins(old_values=old_distances, new_values=new_distances)

    # WARNING: profits could be negative --> in that case, the relative margin doesn't make sense
    def get_relative_marginal_profits(self):
        old_profits = self.get_old_profits()
        new_profits = self.get_new_profits()
        return self.__calc_relative_margins(old_values=old_profits, new_values=new_profits)

    def get_relative_collaboration_distance_gains(self):
        old_distances = self.get_old_distances()
        new_distances = self.get_new_distances()
        return self.__calc_relative_collab_margins(old_values=old_distances, new_values=new_distances)

    # WARNING: total profit could be negative --> in that case, the relative margin doesn't make sense
    def get_relative_collaboration_profit_gains(self):
        old_profits = self.get_old_profits()
        new_profits = self.get_new_profits()
        return self.__calc_relative_collab_margins(old_values=old_profits, new_values=new_profits)

    """
    Averages
    """

    def get_average_computation_time(self):
        computation_times = self.get_computation_times()
        return sum(computation_times) / len(computation_times)

    def get_average_iterations(self):
        iterations = self.get_iterations()
        return sum(iterations) / len(iterations)

    def get_average_absolute_marginal_distances(self):
        marginal_distances = self.get_absolute_marginal_distances()
        return self.__calc_averages(matrix=marginal_distances)

    def get_average_absolute_marginal_profits(self):
        marginal_profits = self.get_absolute_marginal_profits()
        return self.__calc_averages(matrix=marginal_profits)

    def get_average_absolute_collaboration_distance_gain(self):
        absolute_distance_gains = self.get_absolute_collaboration_distance_gains()
        return sum(absolute_distance_gains) / len(absolute_distance_gains)

    def get_average_absolute_collaboration_profit_gain(self):
        absolute_profit_gains = self.get_absolute_collaboration_profit_gains()
        return sum(absolute_profit_gains) / len(absolute_profit_gains)

    # Note: Total relative marginal distances might be a better measurement
    # similar weighting of instances with potentially very different absolute values
    def get_average_relative_marginal_distances(self):
        rel_marginal_distances = self.get_relative_marginal_distances()
        return self.__calc_averages(matrix=rel_marginal_distances)

    # WARNING: if profits are negative -> relative margins don't make sense -> average relative margins might not be a good measurement
    def get_average_relative_marginal_profits(self):
        rel_marginal_profits = self.get_relative_marginal_profits()
        return self.__calc_averages(matrix=rel_marginal_profits)

    # Note: Total collaboration relative marginal distances might be a better measurement
    def get_average_relative_collaboration_distance_gain(self):
        relative_gains = self.get_relative_collaboration_distance_gains()
        return sum(relative_gains) / len(relative_gains)

    # WARNING: if total profits are negative -> relative margins don't make sense -> average relative margins might not be a good measurement
    def get_average_relative_collaboration_profit_gain(self):
        relative_gains = self.get_relative_collaboration_profit_gains()
        return sum(relative_gains) / len(relative_gains)

    """
    Totals
    """

    def get_total_relative_marginal_distances(self):
        old_distances = self.get_old_distances()
        new_distances = self.get_new_distances()
        return self.__calc_total_relatives(old_values=old_distances, new_values=new_distances)

    def get_total_relative_marginal_profits(self):
        old_profits = self.get_old_profits()
        new_profits = self.get_new_profits()
        return self.__calc_total_relatives(old_values=old_profits, new_values=new_profits)

    def get_total_relative_collaboration_distance_gain(self):
        old_distances = self.get_old_distances()
        new_distances = self.get_new_distances()
        return self.__calc_total_collab_relative(old_values=old_distances, new_values=new_distances)

    def get_total_relative_collaboration_profit_gain(self):
        old_profits = self.get_old_profits()
        new_profits = self.get_new_profits()
        return self.__calc_total_collab_relative(old_values=old_profits, new_values=new_profits)

    def get_results(self):
        results_dic = {}
        results_dic["average computation times (seconds)"] = self.get_average_computation_time()
        results_dic["average number of iterations"] = self.get_average_iterations()
        results_dic["total relative marginal distances"] = self.get_total_relative_marginal_distances()
        results_dic["total relative collaboration distance"] = self.get_total_relative_collaboration_distance_gain()
        results_dic["total relative marginal profits"] = self.get_total_relative_marginal_profits()
        results_dic["total relative collaboration profit"] = self.get_total_relative_collaboration_profit_gain()
        return results_dic
