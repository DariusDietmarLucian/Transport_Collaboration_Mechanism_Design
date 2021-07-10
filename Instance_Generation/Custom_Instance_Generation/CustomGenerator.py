import random
import math

from Instance_Generation.CompetitionLevel import CompetitionLevel
from Models.Site import Site
from Models.Location import Location


class CustomGenerator:

    def __init__(self, num_carriers):
        self.num_carriers = num_carriers

        self.location_id = -1

    """
    *************
    ***PRIVATE***
    *************
    """

    def __generate_location_id(self):
        self.location_id = self.location_id + 1
        return self.location_id

    def __create_depots(self, num_carriers):

        if num_carriers < 2:
            return None

        degree = 360 / num_carriers

        depot_sites = []

        for i in range(num_carriers):
            current_degree = degree * i
            x = round(math.cos(math.radians(current_degree)) * 115)
            y = round(math.sin(math.radians(current_degree)) * 115)
            site = Site(Location(id=self.__generate_location_id(), x=x, y=y), area_id=i)
            depot_sites.append(site)

        return depot_sites

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
        num_carriers = self.get_num_carriers()

        depot_sites = self.__create_depots(num_carriers=num_carriers)

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

    """
    *************
    ***GETTERS***
    *************
    """

    def get_num_carriers(self):
        return self.num_carriers
