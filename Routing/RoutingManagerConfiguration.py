import config


class RoutingManagerConfiguration:

    def __init__(self, solution_strategy=None, insertion_strategy=None, removal_strategy=None):
        self.solution_strategy = solution_strategy if solution_strategy is not None else config.routing_manager_configuration[
            "solution_strategy"]
        self.insertion_strategy = insertion_strategy if insertion_strategy is not None else config.routing_manager_configuration[
            "insertion_strategy"]
        self.removal_strategy = removal_strategy if removal_strategy is not None else config.routing_manager_configuration[
            "removal_strategy"]

    def get_dictionary(self):
        dic = {}

        dic["solution strategy"] = str(self.solution_strategy)
        dic["insertion strategy"] = str(self.insertion_strategy)
        dic["removal strategy"] = str(self.removal_strategy)

        return dic

