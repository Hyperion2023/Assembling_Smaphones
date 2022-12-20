from Core.Worker import Worker
import random

drawFlag = True
import time
sec_time = 10


class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.n_total_arms = self.environment.n_robotic_arms
        self.running_workers = []
        self.deployed_arms = 0

    def update_step(self):
        self.environment.update_time()
        self.n_total_arms = self.environment.n_robotic_arms

    def update_moved_arms(self):
        self.n_total_arms -= 1

    def all_arms_moved_in_current_step(self):
        if self.n_total_arms == 0:
            return True
        else:
            return False

    def deploy_arm(self):
        # TODO: implement distance deployment strat

        for row in self.environment.districts:
            for district in row:
                district.mounting_points.reverse()
                district.sort_tasks()
                for mounting_point_index, mouting_point in enumerate(district.mounting_points):
                    # print(district.ordered_tasks[mounting_point_index])
                    if not district.ordered_tasks[mounting_point_index]:  # if there are no task in district
                        continue
                    selectedTask = district.ordered_tasks[mounting_point_index][0]
                    if self.deployed_arms < self.n_total_arms:
                        self.deployed_arms += 1
                        self.running_workers.append(
                            Worker(self.environment.add_robotic_arm(mouting_point), selectedTask,self.environment))
                        for ot in district.ordered_tasks:
                            ot.remove(selectedTask)
                        self.environment.tasks.remove(selectedTask)
        self.environment.draw(agent=self)

        # input()
        # time.sleep(sec_time)



    def random_deploy(self):
        randomMoutingPoints = random.sample(self.environment.mounting_points, self.environment.n_robotic_arms)
        for row in self.environment.districts:
            for district in row:
                district.sort_tasks()
        for mountingpoint in randomMoutingPoints:
            currentDistrict = self.environment.calculate_district(mountingpoint.x, mountingpoint.y)
            mounting_point_index = currentDistrict.mounting_points.index(mountingpoint)
            selectedTask = currentDistrict.ordered_tasks[mounting_point_index][0]
            self.running_workers.append(
                Worker(self.environment.add_robotic_arm(mountingpoint), selectedTask,self.environment))
            for ot in currentDistrict.ordered_tasks:
                ot.remove(selectedTask)
            self.environment.tasks.remove(selectedTask)
        self.deployed_arms = self.n_total_arms
        self.environment.draw(agent=self)

    def worker_move_arm(self, worker, x_y_distances, retraction=False):
        print("MOVE ARM")
        arm_moved = False
        if not worker.action_taken:
            ##Check su o giu
            if x_y_distances[1] != 0:

                if x_y_distances[1] > 0:
                    arm_moved = self.environment.move_robotic_arm(worker.arm, "U")
                    print("[MOVE]: U")
                else:
                    arm_moved = self.environment.move_robotic_arm(worker.arm, "D")
                    print("[MOVE]: D")
            # print("ARM MOVED: \t\t"+str(arm_moved))

            if arm_moved:
                worker.take_action()
        if not worker.action_taken:
            if x_y_distances[0] != 0:
                if x_y_distances[0] > 0:
                    arm_moved = self.environment.move_robotic_arm(worker.arm, "R")
                    print("[MOVE]: R")
                else:
                    arm_moved = self.environment.move_robotic_arm(worker.arm, "L")
                    print("[MOVE]: L")
            if arm_moved:
                worker.take_action()
        # print("ARM MOVED: "+str(arm_moved))
        if not worker.action_taken:
            print("HERE W in workers")
            arm_moved = self.environment.move_robotic_arm(worker.arm, "W")
            print("[MOVE]: W")
        worker.reset_action_taken()

    def get_to_task_point(self, worker):
        x_y_distances = worker.task.get_distance_to_first_point(worker.arm.get_position)
        # print("[ARM position]: "+str(worker.arm.get_position())) 
        # print("[TASK position]: "+str(worker.task.get_position()))
        # print("DISTANCES: "+str(x_y_distances[0])+" "+str(x_y_distances[1]))

        # TODO: ottimizzare scelta passi, per ora prima su e giu poi dx e sx
        self.worker_move_arm(worker, x_y_distances)
        # print("New [ARM position]: "+str(worker.arm.get_position()))
        # print("New [TASK position]: "+str(worker.task.get_position()))
        if worker.arm.get_position == worker.task.get_position:
            worker.task.task_target_update()

    def worker_retract_arm(self, worker):

        retract, newPos = worker.retract()
        print("NEWPOS: ", str(newPos))
        x_y_distances = worker.task.x_y_distance(worker.arm.get_position, newPos)
        print(x_y_distances)
        if retract:
            self.worker_move_arm(worker, x_y_distances)
        elif newPos != (0, 0):
            pass  # TODO: implement descheduling sleep or task reassignment

    def run_assembly(self):

        for current_step in range(self.environment.n_steps):
            print("[STEP]: " + str(current_step))

            for worker in self.running_workers:
                if current_step == 0:
                    district = self.environment.calculate_district(worker.arm.mounting_point.x,
                                                                   worker.arm.mounting_point.y)
                    for ot in district.ordered_tasks:
                        print(ot)

                isTaskCompleted = worker.task.task_completed()
                if isTaskCompleted and len(worker.arm.path) == 1:

                    district = self.environment.calculate_district(worker.arm.mounting_point.x,
                                                                   worker.arm.mounting_point.y)
                    newTask = district.ordered_tasks[district.mounting_points.index(worker.arm.mounting_point)][0]
                    for ot in district.ordered_tasks:
                        ot.remove(newTask)
                    self.environment.tasks.remove(newTask)
                    worker.task = newTask

                if not isTaskCompleted and not worker.arm.collision_check:
                    self.get_to_task_point(worker)
                else:
                    print("RETRACTING")
                    self.worker_retract_arm(worker)
            self.environment.update_time()
            if drawFlag:
                self.environment.draw(agent=self)
        print("#######################")

        for worker in self.running_workers:
            print(worker.arm.moves)


    def run_plan(self, planned_workers):
        for worker in planned_workers:
            print(worker.arm.moves)
        for current_step in range(self.environment.n_steps):
            print("[STEP]: " + str(current_step))
            for worker, planned_worker in zip(self.running_workers, planned_workers):
                try:
                    self.environment.move_robotic_arm(worker.arm, planned_worker.arm.moves.pop(0))
                except IndexError:
                    return
            self.environment.update_time()
            if drawFlag:
                self.environment.draw(agent=self)
        print("#######################")

        for worker in self.running_workers:
            print(worker.arm.moves)