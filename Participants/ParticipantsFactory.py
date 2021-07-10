from Participants.Carrier.Carrier import Carrier
from Participants.Mechanism_Manager.MechanismManager import MechanismManager
from Participants.Mechanism_Manager.MechanismManagerConfiguration import MechanismManagerConfiguration
from Participants.Carrier.CarrierConfiguration import CarrierConfiguration

from Instance_Generation.InstanceGenerationManager import InstanceGenerationManager
from Instance_Generation.InstanceGenerationManagerConfiguration import InstanceGenerationManagerConfiguration

import config


class ParticipantsFactory:

    def __init__(self, instance_generation_config=None, mechanism_manager_config=None, carrier_config=None,
                 other_carriers_config=None):

        self.instance_generation_config = instance_generation_config if instance_generation_config is not None else InstanceGenerationManagerConfiguration()
        self.mechanism_manager_config = mechanism_manager_config if mechanism_manager_config is not None else MechanismManagerConfiguration()
        self.carrier_config = carrier_config if carrier_config is not None else CarrierConfiguration()
        self.other_carriers_config = other_carriers_config if other_carriers_config is not None else CarrierConfiguration()

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __create_participants(depots, requests, graph, mm_config, c_config, oc_config):
        carriers = []

        for index in range(len(depots)):
            carrier_id = index
            other_carrier_ids = [i for i in range(len(depots)) if i != carrier_id]
            depot = depots[carrier_id]
            other_depots = [depots[j] for j in range(len(depots)) if j != carrier_id]
            player_requests = requests[carrier_id]

            # player with index = 0 should be separated from other players to test bidding strategies for that player
            if carrier_id == 0:
                carrier = Carrier(id=carrier_id, other_player_ids=other_carrier_ids, depot=depot,
                                  other_depots=other_depots, requests=player_requests,
                                  graph=graph, configuration=c_config)
            else:
                carrier = Carrier(id=carrier_id, other_player_ids=other_carrier_ids, depot=depot,
                                  other_depots=other_depots, requests=player_requests,
                                  graph=graph, configuration=oc_config)

            carriers.append(carrier)

        mechanism_manager = MechanismManager(carriers=carriers, graph=graph, configuration=mm_config)

        return carriers, mechanism_manager

    """
    ************
    ***PUBLIC***
    ************
    """

    def create_all_participants(self):

        i_config = self.get_instance_generation_configuration()
        mm_config = self.get_mechanism_manager_configuration()
        c_config = self.get_carrier_configuration()
        oc_config = self.get_other_carriers_configuration()

        instance_manager = InstanceGenerationManager(parent_directory=config.parent_directory, configuration=i_config)
        depot_instances, request_instances, graph_instances = instance_manager.get_instances()

        all_participants = []

        for i in range(len(depot_instances)):
            carriers, mechanism_manager = self.__create_participants(depots=depot_instances[i],
                                                                     requests=request_instances[i],
                                                                     graph=graph_instances[i],
                                                                     mm_config=mm_config,
                                                                     c_config=c_config,
                                                                     oc_config=oc_config)
            all_participants.append((mechanism_manager, carriers))

        return all_participants

    """
    *************
    ***GETTERS***
    *************
    """

    def get_instance_generation_configuration(self):
        return self.instance_generation_config

    def get_mechanism_manager_configuration(self):
        return self.mechanism_manager_config

    def get_carrier_configuration(self):
        return self.carrier_config

    def get_other_carriers_configuration(self):
        return self.other_carriers_config
