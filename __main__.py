from Core.Utils.Data import create_Environment
from Core.Agent import Agent

if __name__ == "__main__":
    path = r"./Dataset/a_example.txt"
    env = create_Environment(path)
    #env.draw()
    boomer = Agent(env)
    #boomer.environment.show()
    boomer.deploy_arm()
    #boomer.running_workers[0].my_description()
    boomer.run_assembly()
