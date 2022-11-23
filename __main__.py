from Core.Utils.Data import create_Environment
from Core.Agent import Agent
from Core.Astar.State import State

if __name__ == "__main__":
    path = r"./Dataset/b_single_arm.txt"

    # state = State(None, 4)
    # state.get_children()

    env = create_Environment(path)
    #env.draw()
    boomer = Agent(env)
    #boomer.environment.show()
    boomer.deploy_arm()
    #boomer.running_workers[0].my_description()
    boomer.run_assembly()
