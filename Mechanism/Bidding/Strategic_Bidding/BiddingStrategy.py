import enum

class BiddingStrategy(enum.Enum):
    TRUTHFUL = 1
    INPUT_MANIPULATION = 2
    HIGH_ABS = 3
    BID_MANIPULATION_REL = 4
    CONSPIRING = 5
    HIGH_ABS_ISO = 6
