from Core.Worker import Worker


class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.unmoved_arms = self.environment.n_robotic_arms
        self.running_workers = []

    def update_step(self):
        self.environment.update_time()
        self.unmoved_arms = self.environment.n_robotic_arms

    def update_moved_arms(self):
        self.unmoved_arms -= 1

    def all_arms_moved_in_current_step(self):
        if self.unmoved_arms == 0:
            return True
        else:
            return False

    def deploy_arm(self):
        # TODO: implement distance deployment strat

        for row in self.environment.districts:
            for district in row:
                district.sort_tasks()
                for mounting_point_index, mouting_point in enumerate(district.mounting_points):
                    #print(district.ordered_tasks[mounting_point_index])
                    if not district.ordered_tasks[mounting_point_index]:  # if there are no task in district
                        continue
                    self.running_workers.append(
                       Worker(self.environment.add_robotic_arm(mouting_point), district.ordered_tasks[mounting_point_index].pop(0)))

    def worker_move_arm(self,worker,x_y_distances,retraction=False):
        arm_moved=False
        if not worker.action_taken:
            ##Check su o giu
            if x_y_distances[1]!=0:
                
                if x_y_distances[1]>0 :
                    arm_moved=self.environment.move_robotic_arm(worker.arm,"U")
                    print("[MOVE]: U")
                else:
                    arm_moved=self.environment.move_robotic_arm(worker.arm,"D")
                    print("[MOVE]: D")
           # print("ARM MOVED: \t\t"+str(arm_moved))

            if arm_moved:
                worker.take_action()
        if not worker.action_taken:
            if x_y_distances[0]!=0:
                if x_y_distances[0]>0 :
                    arm_moved=self.environment.move_robotic_arm(worker.arm,"R")
                    print("[MOVE]: R")
                else:
                    arm_moved=self.environment.move_robotic_arm(worker.arm,"L")
                    print("[MOVE]: L")
            if arm_moved:
                worker.take_action()
           # print("ARM MOVED: "+str(arm_moved))
        if not worker.action_taken:
            arm_moved=self.environment.move_robotic_arm(worker.arm,"W")     
            print("[MOVE]: W")               
        worker.reset_action_taken()


    def get_to_task_point(self,worker):
        x_y_distances=worker.task.get_distance_to_first_point(worker.arm.get_position())
        # print("[ARM position]: "+str(worker.arm.get_position())) 
        # print("[TASK position]: "+str(worker.task.get_position()))
        # print("DISTANCES: "+str(x_y_distances[0])+" "+str(x_y_distances[1]))
      
        # TODO: ottimizzare scelta passi, per ora prima su e giu poi dx e sx
        self.worker_move_arm(worker,x_y_distances)
        print("New [ARM position]: "+str(worker.arm.get_position())) 
        print("New [TASK position]: "+str(worker.task.get_position()))
        if worker.arm.get_position() ==worker.task.get_position():
            worker.task.task_target_update()

    def worker_retract_arm(self,worker):
        retract,newPos=worker.retract()
        
        x_y_distances=worker.task.x_y_distance(worker.arm.get_position(),newPos)
        print(x_y_distances)
        if retract:
            self.worker_move_arm(worker,x_y_distances)
        elif newPos!=(0,0):
            pass #TODO: implement descheduling sleep or task reassignment



    def run_assembly(self):
        self.environment.n_steps=4
        for current_step in range(self.environment.n_steps):
            print("[STEP]: " + str(current_step))
            for worker in self.running_workers:
                
                if not worker.task.task_completed() and not worker.arm.collision_check:
                    self.get_to_task_point(worker)
                else:
                    print("RETRACTING")
                    self.worker_retract_arm(worker)
                print("PATH:")
                print(worker.arm.path)
            self.environment.update_time()
        print("#######################")
        for worker in self.running_workers:
            print(worker.arm.moves)
