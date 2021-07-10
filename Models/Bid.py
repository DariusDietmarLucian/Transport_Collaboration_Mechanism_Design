class Bid:

    def __init__(self, bundle, valuation, carrier_id):
        self.bundle = bundle
        self.valuation = valuation
        self.carrier_id = carrier_id

    """
    *************
    ***GETTERS***
    *************
    """

    def get_bundle(self):
        return self.bundle

    def get_valuation(self):
        return self.valuation

    def get_carrier_id(self):
        return self.carrier_id

    def get_bundle_id(self):
        return self.get_bundle().get_id()

    def get_requests(self):
        return self.bundle.get_requests()

    """
    **************
    ***CONFORMS***
    **************
    """

    def __eq__(self, other):
        return self.get_bundle_id() == other.get_bundle_id() and self.get_carrier_id() == other.get_carrier_id() and self.get_valuation() == other.get_valuation()
