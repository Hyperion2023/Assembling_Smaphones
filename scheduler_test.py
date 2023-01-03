from Core import Agent, Worker, District, RoboticArm, MountingPoint


agent = Agent(None)
agent.districts = [District((0, 0), 5, 5), District((3, 0), 8, 3), District((7, 1), 6, 6)]
arm1 = RoboticArm()
arm2 = RoboticArm()
arm3 = RoboticArm()
arm1.mount(MountingPoint(1, 3))
arm2.mount(MountingPoint(6, 0))
arm3.mount(MountingPoint(8, 4))
agent.running_workers.append(Worker(arm1, None, None, agent.districts[0]))
agent.running_workers.append(Worker(arm2, None, None, agent.districts[1]))
agent.running_workers.append(Worker(arm3, None, None, agent.districts[2]))
agent.running_workers.append(Worker(arm1, None, None, agent.districts[0]))
agent.running_workers[0].plan = ["R", "R", "R", "D", "D", "L", "R", "U", "U", "L", "L", "L"]
agent.running_workers[1].plan = ["L", "L", "R", "R", "R", "U", "R", "D", "R", "L", "U", "L", "D", "L"]
agent.running_workers[2].plan = ["R", "R", "R", "D", "D", "D", "L", "L", "R", "R", "U", "U", "U", "L", "L", "L"]
agent.running_workers[3].plan = ["R", "R", "R", "L", "L", "L"]
solution = agent.schedule_plans()
print(solution)
