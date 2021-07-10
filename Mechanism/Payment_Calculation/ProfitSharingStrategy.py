import enum


class ProfitSharingStrategy(enum.Enum):
    EGALITARIAN = 1
    PURCHASE_SALE_WEIGHT = 2
    MODIFIED_EGALITARIAN = 3
    CRITICAL_WEIGHT = 4
    CRITICAL_WEIGHT_SQUARED = 5
    CRITICAL_WEIGHT_CUBIC = 6
    SHAPLEY_VALUE = 7

    def requires_contribution(self):
        return self.value in [3]

    def based_on_egalitarian(self):
        return self.value in [1, 3]

    def based_on_purchase_sale_weight(self):
        return self.value in [2]

    def based_on_critical_weight(self):
        return self.value in [4, 5, 6]

    def based_on_shapley_value(self):
        return self.value in [7]
