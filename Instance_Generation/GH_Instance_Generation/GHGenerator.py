"""
Generation based on:
Gansterer, M. and Hartl, R.F., 2016. Request evaluation strategies for carriers in auction-based collaborations.
OR spectrum, 38(1), pp.3-23.
"""

import random
import math

from Instance_Generation.CompetitionLevel import CompetitionLevel
from Models.Site import Site
from Models.Location import Location


class GHGenerator:

    def __init__(self):
        self.location_id = -1

    """
    *************
    ***PRIVATE***
    *************
    """

    def __generate_location_id(self):
        self.location_id = self.location_id + 1
        return self.location_id

    def __random_customer_sites(self, depot, radius, num_points):

        sites = []

        for i in range(num_points):
            r = radius * math.sqrt(random.random())
            theta = random.random() * 2 * math.pi

            x = int(depot.get_location_x() + r * math.cos(theta))
            y = int(depot.get_location_y() + r * math.sin(theta))
            location = Location(id=self.__generate_location_id(), x=x, y=y)
            sites.append(Site(location=location, area_id=depot.area_id))

        return sites

    """
    ************
    ***PUBLIC***
    ************
    """

    def create_sites(self, competition_level, num_carrier_requests):
        self.location_id = -1

        # equidistant points with length of ~200 between them (see G&H 2016)
        depot_sites = [
            Site(Location(id=self.__generate_location_id(), x=100, y=173), area_id=0),
            Site(Location(id=self.__generate_location_id(), x=-100, y=173), area_id=1),
            Site(Location(id=self.__generate_location_id(), x=0, y=0), area_id=2),
            ]

        customer_sites = []
        for depot in depot_sites:

            if competition_level == CompetitionLevel.LOW:
                sites = self.__random_customer_sites(depot=depot, radius=150, num_points=num_carrier_requests * 2)
            elif competition_level == CompetitionLevel.MEDIUM:
                sites = self.__random_customer_sites(depot=depot, radius=200, num_points=num_carrier_requests * 2)
            elif competition_level == CompetitionLevel.HIGH:
                sites = self.__random_customer_sites(depot=depot, radius=300, num_points=num_carrier_requests * 2)

            customer_sites.extend(sites)

        return depot_sites, customer_sites
