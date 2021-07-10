import config


class InstanceGenerationManagerConfiguration:

    def __init__(self, competition_level=None, num_carrier_requests=None, num_carriers=None, num_runs=None, strategy=None):
        self.competition_level = competition_level if competition_level is not None else config.instance_generation_configuration[
            "competition_level"]
        self.num_carrier_requests = num_carrier_requests if num_carrier_requests is not None else config.instance_generation_configuration[
            "num_carrier_requests"]
        self.num_carriers = num_carriers if num_carriers is not None else config.instance_generation_configuration[
            "num_carriers"]
        self.num_runs = num_runs if num_runs is not None else config.instance_generation_configuration[
            "num_runs"]
        self.strategy = strategy if strategy is not None else config.instance_generation_configuration[
            "strategy"]


    def get_dictionary(self):
        dic = {}

        dic["competition level"] = str(self.competition_level)
        dic["number of requests per carrier"] = self.num_carrier_requests
        dic["number of carriers"] = self.num_carriers
        dic["number of runs"] = self.num_runs
        dic["generation strategy"] = str(self.strategy)

        return dic

