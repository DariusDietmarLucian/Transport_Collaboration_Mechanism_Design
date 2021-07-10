import enum


class SolutionStrategy(enum.Enum):
    DOUBLE_INSERTION = 1

    GOOGLE_PATH_CHEAPEST_ARC = 2
    GOOGLE_LOCAL_CHEAPEST_INSERTION = 3
    GOOGLE_PARALLEL_CHEAPEST_INSERTION = 4

    def uses_google(self):
        return self.value in [2, 3, 4]
