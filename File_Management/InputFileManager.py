import json
import os
from Instance_Generation.GenerationStrategy import GenerationStrategy
from Instance_Generation.CompetitionLevel import CompetitionLevel

from Models.Node import Node
from Models.Request import Request


class InputFileManager:

    def __init__(self, parent_directory):
        self.parent_directory = parent_directory

    """
    *************
    ***PRIVATE***
    *************
    """

    def __get_input_directory(self):
        parent_directory = self.get_parent_directory()
        return os.path.join(parent_directory, "Input")

    def __get_path(self, num_requests, competition_level, generation_strategy, num_carriers):
        input_directory = self.__get_input_directory()
        directory = InputFileManager.translate_instance_type(num_requests=num_requests,
                                                             competition_level=competition_level,
                                                             generation_strategy=generation_strategy,
                                                             num_carriers=num_carriers)
        return os.path.join(input_directory, directory)

    @staticmethod
    def __decode(data_dic):
        depots = []
        requests = []

        for player_dic in data_dic:
            problem_dic = player_dic["problem"]
            depot_dic = problem_dic["depot"]
            player_depot = Node.decode(node_dic=depot_dic)
            depots.append(player_depot)

            player_requests = []
            requests_dic = problem_dic["requests"]
            for request_dic in requests_dic:
                request = Request.decode(request_dic=request_dic)
                player_requests.append(request)
            requests.append(player_requests)

        return depots, requests

    """
    ************
    ***PUBLIC***
    ************
    """

    @staticmethod
    def translate_instance_type(num_requests, competition_level, generation_strategy, num_carriers):

        if generation_strategy == GenerationStrategy.BB:

            if competition_level == CompetitionLevel.LOW:
                return f"BB-LOW_{num_requests}"
            elif competition_level == CompetitionLevel.MEDIUM:
                return f"BB-MEDIUM_{num_requests}"
            elif competition_level == CompetitionLevel.HIGH:
                return f"BB-HIGH_{num_requests}"

        elif generation_strategy == GenerationStrategy.GH:

            if competition_level == CompetitionLevel.LOW:
                return f"GH-LOW_{num_requests}"
            elif competition_level == CompetitionLevel.MEDIUM:
                return f"GH-MEDIUM_{num_requests}"
            elif competition_level == CompetitionLevel.HIGH:
                return f"GH-HIGH_{num_requests}"

        elif generation_strategy == GenerationStrategy.Custom:

            if competition_level == CompetitionLevel.LOW:
                return f"LOW_{num_requests}_{num_carriers}"
            elif competition_level == CompetitionLevel.MEDIUM:
                return f"MEDIUM_{num_requests}_{num_carriers}"
            elif competition_level == CompetitionLevel.HIGH:
                return f"HIGH_{num_requests}_{num_carriers}"

    # in all_rounds each row holds the instances for a round
    # the instances in a row consist of the depots/requests for each carrier
    def write(self, depots_all_rounds, requests_all_rounds, competition_level, generation_strategy, num_carriers):

        input_directory = self.__get_input_directory()

        if not os.path.isdir(input_directory):
            os.mkdir(input_directory)

        num_requests = len(requests_all_rounds[0][0])
        num_rounds = len(requests_all_rounds)

        path = self.__get_path(num_requests=num_requests, competition_level=competition_level,
                               generation_strategy=generation_strategy, num_carriers=num_carriers)

        if os.path.isdir(path):
            return
        else:
            os.mkdir(path)

        for i in range(num_rounds):
            instance_dic = []
            file_object = open(f"{path}/instance_{i}.json", "w+")

            for j in range(len(requests_all_rounds[i])):
                carrier_dic = {"carrier": j}

                problem_dic = {}
                problem_dic["depot"] = depots_all_rounds[i][j].encode()

                player_requests = []
                for request in requests_all_rounds[i][j]:
                    player_requests.append(request.encode())
                problem_dic["requests"] = player_requests

                carrier_dic["problem"] = problem_dic
                instance_dic.append(carrier_dic)

            json.dump(instance_dic, file_object, indent=4)

        file_object.close()

    def read(self, num_runs, num_requests, competition_level, generation_strategy, num_carriers):

        path = self.__get_path(num_requests=num_requests, competition_level=competition_level,
                               generation_strategy=generation_strategy, num_carriers=num_carriers)

        if not os.path.isdir(path):
            return None, None

        all_depots = []
        all_requests = []

        for i in range(num_runs):
            file_object = open(f"{path}/instance_{i}.json", "r")
            data_dic = json.load(file_object)
            depots, requests = self.__decode(data_dic=data_dic)
            all_depots.append(depots)
            all_requests.append(requests)

        return all_depots, all_requests

    """
    *************
    ***GETTERS***
    *************
    """

    def get_parent_directory(self):
        return self.parent_directory
