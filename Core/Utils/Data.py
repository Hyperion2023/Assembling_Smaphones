from Core import Environment


def create_Environment(file_path: str) -> Environment:
    """
    Read the input file and create the environment. Generate several districts based on district_size.
    :param file_path: Path to the input file.
    :param district_size: Size of the districts.
    :return: Complete environment.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

        width = int((lines[0].split(" "))[0])
        height = int((lines[0].split(" "))[1])
        number_of_arms = int((lines[0].split(" "))[2])

        number_of_mouting_points = int((lines[0].split(" "))[3])
        number_of_total_steps = int((lines[0].split(" "))[5])
        environment = Environment(width, height, number_of_total_steps, number_of_arms)
        mouting_points = [(int((s.split(" "))[0]), int((s.split(" "))[1])) for s in lines[1:number_of_mouting_points+1]]
        environment.add_mounting_points(mouting_points)

        tasks = lines[number_of_mouting_points+1::2]
        tasks_positions = lines[number_of_mouting_points+2::2]
        environment.add_tasks(tasks, tasks_positions)
        return environment


