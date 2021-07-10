import config

class GABundleGeneratorConfiguration:

    def __init__(self, population_size=None, number_bundles=None, elite_share=None, rounds=None, cross_over_prob=None, mutate_prob=None):
        self.population_size = population_size if population_size is not None else config.ga_bundling_generator_configuration["population_size"]
        self.number_bundles = number_bundles if number_bundles is not None else config.ga_bundling_generator_configuration["number_bundles"]
        self.elite_share = elite_share if elite_share is not None else config.ga_bundling_generator_configuration["elite_share"]
        self.rounds = rounds if rounds is not None else config.ga_bundling_generator_configuration["rounds"]
        self.cross_over_prob = cross_over_prob if cross_over_prob is not None else config.ga_bundling_generator_configuration["cross_over_prob"]
        self.mutate_prob = mutate_prob if mutate_prob is not None else config.ga_bundling_generator_configuration["mutate_prob"]

    def get_dictionary(self):
        dic = {}

        dic["population size"] = self.population_size
        dic["number of bundles"] = self.number_bundles
        dic["elite share"] = self.elite_share
        dic["number of rounds"] = self.rounds
        dic["cross-over probability"] = self.cross_over_prob
        dic["mutation probability"] = self.mutate_prob

        return dic