from Core.Utils.Data import create_Environment


if __name__ == "__main__":
    path = r"./Dataset/b_single_arm.txt"
    env = create_Environment(path)
    env.show()
