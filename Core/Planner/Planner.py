from Core.Utils.Dijkstra import *
from Core import Environment
class Planner:

    def __init__(self, environment:Environment):
        self.environment = environment
        create_graph_from_district(self.environment)

    # def generate_path_to_first_point(self,agent):
    #     for worker in agent.running_workers:
    #








