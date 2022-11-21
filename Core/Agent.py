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
                    print(district.ordered_tasks[mounting_point_index])
                    if not district.ordered_tasks[mounting_point_index]:  # if there are no task in district
                        continue
                    self.running_workers.append(
                       Worker(self.environment.add_robotic_arm(mouting_point), district.ordered_tasks[mounting_point_index].pop(0)))
