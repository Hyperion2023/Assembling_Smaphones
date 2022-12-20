from Core.Utils.Data import create_Environment
from Core.Agent import Agent
from Core.Astar.State import State
from Core.Astar.Astar import a_star
from Core.Astar.heuristic import *
from Core.Utils.Dijkstra import *

if __name__ == "__main__":
    path = r"./Dataset/a_example.txt"

    # state = State(None, 4)
    # state.get_children()

    env = create_Environment(path, district_size=4)
    # env.draw()
    boomer = Agent(env)
    # boomer.environment.show()
    boomer.deploy_arm()

    g=Graph()
    g.create_graph_from_mat(boomer.environment.matrix)
    # print("Graph data:")
    # for v in g:
    #     for w in v.get_connections():
    #         vid = v.get_id()
    #         wid = w.get_id()
    #         print(vid, wid, v.get_weight(w))
    import time

    start = time.time()
    dijkstra(g, g.get_vertex(2), g.get_vertex(504)) 
    end = time.time()
    print(end - start)
    target = g.get_vertex(504)
    path = [target.get_id()]
    start = time.time()
    shortest(target, path)
    end = time.time()
    print(end - start)
    print ("The shortest path : %s",(path[::-1]))

    #boomer.running_workers[0].
    #starting_state = State(env.matrix, boomer.running_workers)

    #final_state = a_star(starting_state, goal_test, g, h)
    #boomer.run_plan(final_state.workers)
    # boomer.running_workers[0].my_description()
    # boomer.run_assembly()
