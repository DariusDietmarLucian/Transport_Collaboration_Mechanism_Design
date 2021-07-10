import config
from Mechanism.Bundle_Generation.BundleGeneratorStrategy import BundleGeneratorStrategy
from Mechanism.Bundle_Generation.Genetic_Algorithm_Bundle_Generation.GABundleGeneratorConfiguration import GABundleGeneratorConfiguration


class BundleGeneratorConfiguration:

    def __init__(self, strategy=None, ga_bundle_generator_configuration=None):
        self.strategy = strategy if strategy is not None else config.bundle_generator_configuration["strategy"]

        self.ga_bundle_generator_configuration = \
            ga_bundle_generator_configuration if ga_bundle_generator_configuration is not None \
                else GABundleGeneratorConfiguration()

    def get_dictionary(self):
        dic = {}

        dic["composition strategy"] = str(self.strategy)

        if self.strategy == BundleGeneratorStrategy.BEST_GA_BUNDLES:
            dic["genetic algorithm parameters"] = self.ga_bundle_generator_configuration.get_dictionary()

        return dic
