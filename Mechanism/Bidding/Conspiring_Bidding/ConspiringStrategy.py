import enum

class ConspiringStrategy(enum.Enum):
    AUTO_COMBO = 1
    INPUT_MAX = 2
    INPUT_ENTER = 3
    BID_KICKOUT = 4
    DESTROY_WEIGHT = 5
    WIN_LOW = 6