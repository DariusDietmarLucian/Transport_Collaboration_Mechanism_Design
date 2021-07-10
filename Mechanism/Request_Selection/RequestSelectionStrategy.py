import enum


class RequestSelectionStrategy(enum.Enum):
    MIN_PROFIT = 1
    CLUSTER = 2
    COMBO = 3
    COMBO_NEIGH = 4