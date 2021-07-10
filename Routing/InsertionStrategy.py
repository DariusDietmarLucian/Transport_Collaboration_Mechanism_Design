import enum


class InsertionStrategy(enum.Enum):
    NEW_ROUTE = 1

    DOUBLE_INSERTION_NO_OPT = 2
    DOUBLE_INSERTION_2_OPT = 3
    DOUBLE_INSERTION_3_OPT = 4

    CHEAP_INSERTION_NO_OPT = 5
    CHEAP_INSERTION_2_OPT = 6
    CHEAP_INSERTION_3_OPT = 7

    CHEAP_INSERTION_GOOGLE_PATH_CHEAPEST_ARC = 8
    CHEAP_INSERTION_GOOGLE_LOCAL_CHEAPEST_ARC = 9
    CHEAP_INSERTION_GOOGLE_PARALLEL_CHEAPEST_INSERTION = 10

    def uses_double_insertion(self):
        return self.value in [2, 3, 4]

    def uses_cheap_insertion(self):
        return self.value in [5, 6, 7, 8, 9, 10]

    def uses_google_opt(self):
        return self.value in [8, 9, 10]

    def uses_two_opt(self):
        return self.value in [3, 6]

    def uses_three_opt(self):
        return self.value in [4, 7]