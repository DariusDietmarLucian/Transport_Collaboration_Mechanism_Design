"""
Generation based on:
Berger, S. and Bierwirth, C., 2010. Solutions to the request reassignment problem in collaborative carrier networks.
Transportation Research Part E: Logistics and Transportation Review, 46(5), pp.627-638.
"""

from Instance_Generation.CompetitionLevel import CompetitionLevel
from Instance_Generation.BB_Instance_Generation.BBFileReader import BBFileReader

from Models.Site import Site

import config
import sys

class BBGenerator:

    def __init__(self):
        self.locations = None

    """
     *************
     ***PRIVATE***
     *************
     """

    @staticmethod
    def __cat(depot_loc_indices, locations):
        depot_locations = []
        customer_locations = []

        for loc in locations:
            if loc.id in depot_loc_indices:
                depot_locations.append(loc)
            else:
                customer_locations.append(loc)

        return depot_locations, customer_locations

    @staticmethod
    def __selected_assignment(locations, areas, overlap_area=None):
        customer_sites = []

        for loc in locations:

            if overlap_area and loc.get_id() in overlap_area:
                customer_sites.extend(
                    [Site(location=loc, area_id=i) for i in range(len(areas))])
                continue

            area_index = next(i for i, area in enumerate(areas) for v in area if v == loc.get_id())
            customer_sites.append(Site(location=loc, area_id=area_index))

        return customer_sites

    @staticmethod
    def __identical_assignment(locations, areas):
        customer_sites = []

        for loc in locations:
            customer_sites.extend([Site(location=loc, area_id=i) for i in range(len(areas))])

        return customer_sites

    def create_sites(self, competition_level):
        locations = self.get_locations()

        depot_locations, customer_locations = self.__cat(depot_loc_indices=self.DEPOT_INDICES, locations=locations)

        depot_sites = []
        for index, loc in enumerate(depot_locations):
            depot_sites.append(Site(location=loc, area_id=index))

        if competition_level == CompetitionLevel.LOW:
            customer_sites = self.__selected_assignment(locations=customer_locations,
                                                        areas=self.AREAS)
        elif competition_level == CompetitionLevel.MEDIUM:
            customer_sites = self.__selected_assignment(locations=customer_locations,
                                                        areas=self.AREAS, overlap_area=self.OVRLP_AREA)
        elif competition_level == CompetitionLevel.HIGH:
            customer_sites = self.__identical_assignment(locations=customer_locations,
                                                         areas=self.AREAS)

        return depot_sites, customer_sites

    """
    ************
    ***GETTERS***
    ************
    """

    def get_locations(self):
        if self.locations is None:
            if config.r101_filepath is None:
                print("ERROR: you have to store the values from r101 (http://w.cba.neu.edu/~msolomon/problems.htm)"
                      "in a clean format ({index} {x_location} {y_location})"
                      "and then submit the path to the file in the config file")
                sys.exit()

            file_reader = BBFileReader(r101_filename=config.r101_filepath)
            self.locations = file_reader.get_locations()

        return self.locations

    """
    ***************
    ***Constants***
    ***************
    """

    """
    Constants similar to Berger and Bierwirth 2010
    Warning: depot_loc_indices' and areas' order should not be changed because the indices should match
    """
    DEPOT_INDICES = [10, 54, 93]
    AREAS = [
        [36, 49, 64, 19, 11, 63, 62, 90, 32, 70, 30, 20, 66, 51, 81, 9, 71, 35, 65, 47, 48, 7, 88, 52, 31, 27, 69, 1,
         50, 33],
        [34, 78, 79, 3, 77, 29, 68, 80, 12, 24, 26, 40, 55, 21, 4, 25, 73, 72, 2, 74, 56, 39, 75, 22, 41, 23, 67, 76,
         28, 0, 53, 58],
        [46, 8, 45, 83, 60, 17, 84, 5, 96, 99, 61, 59, 95, 85, 98, 92, 97, 37, 16, 86, 91, 100, 87, 44, 42, 57, 14,
         38, 43, 15, 82, 18, 89, 6, 94, 13]
    ]
    OVRLP_AREA = [82, 18, 89, 6, 94, 13, 76, 28, 0, 53, 58, 47, 48, 7, 88, 52, 31, 27, 69, 1, 50, 33]
