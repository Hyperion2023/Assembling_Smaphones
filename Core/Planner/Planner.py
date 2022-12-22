from Core.Utils.Dijkstra import *
import Core
class Planner:

    def __init__(self,environment: Core.Environment.Environment):
        self.environment = environment
        create_graph_from_district(self.environment)

    # def generate_path_to_first_point(self,agent):
    #     for worker in agent.running_workers:
    #








