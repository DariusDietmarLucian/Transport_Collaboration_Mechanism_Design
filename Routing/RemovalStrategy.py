import enum


class RemovalStrategy(enum.Enum):
    NEW_ROUTE = 1

    SIMPLE_REMOVAL_NO_OPT = 2
    SIMPLE_REMOVAL_2_OPT = 3
    SIMPLE_REMOVAL_3_OPT = 4

    def uses_two_opt(self):
        return self.value in [2]

    def uses_three_opt(self):
        return self.value in [4]