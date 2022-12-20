# Assembling_Smartphones
Project for the final assesment of the course *Aritificial Intelligence Fundamentals* of the accademic year 2022/2023. 

## Problem Introduction
In this problem statement, we will explore the idea of operating an automated assembly line for smartphones.
Building a smartphone is a complex process that involves assembling numerous components, including the screen, multiple cameras, microphones, speakers, a
processing unit, and a storage unit.
In order to automate the building of a smartphone, we will be using robotic arms that can move around the assembly workspace performing all necessary tasks.

You are given a description of robotic arms and possible mount points, as well as the locations the arms need to visit during the assembly of a smartphone. Create a plan that uses the robotic arms to build a smartphone, completing as many tasks as possible.

## Problem Visualization
![image](https://user-images.githubusercontent.com/36853239/200181155-de8f4a38-c69c-41b7-bc40-27a41a4222cc.png)
Robotic arms can move the gripper and expand to one of the four neighbouring cells (up/down/right/le - not diagonally). Robotic arms can expand as far as needed inside the assembly workspace. Robotic arms can also retract, moving the gripper back into the previous cell occupied by the robotic arm, and toward the direction of the mount point. Robotic arms can also wait in place without moving (for example, waiting to expand until a neighboring cell becomes free).

## Assembly points and tasks
You are given a list of T tasks that should be completed by the robotic arms. Each task has a score awarded for completing it. Each task can only be completed once, but you do not need to complete all tasks. Each task consists of one or more assembly points that need to be visited in the given
order by a single robotic arm. The same assembly point may appear in the description of multiple tasks, and may appear multiple times in the description of a single task. An assembly point will never be in the same cell as a mount point. Each robotic arm can only work on one task at a time (i.e. it cannot sta a new task before nishing the current task).

## Input data set
File format
Each input data set is provided in a plain text file. The le contains only ASCII characters with lines ending with a single '\n' character (also called “UNIX-style” line endings). When multiple numbers are given in one line, they are separated by a single space between each two numbers.
The first line of the data set contains:
- an integer W (1 ≤ W ≤ $10^3$) – the width of the assembly workspace (number of columns),
- an integer H (1 ≤ H ≤ $10^3$) – the height of the assembly workspace (number of rows),
- an integer R (1 ≤ R ≤ $10^2$) – the number of robotic arms available,
- an integer M (R ≤ M ≤ $10^3$) – the number of mount points,
- an integer T (1 ≤ T ≤ $10^3$) – the number of tasks available, and
- an integer L (1 ≤ L ≤ $10^4$) – the number of total steps for the assembly process.

This is followed by M lines describing the mount points. Each such line contains integers x (0 ≤ x < W) and y (0 ≤ y < H) describing the coordinates of the mount points. A cell can have at most one mount point.
This is followed by T sections describing the tasks. Each task is described in two lines.
The rst line describing each task contains:
- an integer S (1 ≤ S ≤ $10^6$) – the score awarded for finishing the task,
- an integer P (1 ≤ P ≤ $10^3$) – the number of assembly points of this task.
The second line describing the task contains 2·P integers $x_0$, $y_0$, $x_1$, $y_1$, ..., $x_{P-1}$, $y_{P-1}$ (0 ≤ $x_i$ < W, 0 ≤ $y_i$ < H ) – the coordinates of the assembly points in order, the first assembly point having the coordinates [ $x_0$, $y_0$ ] and the last assembly point having the coordinates [ $x_{P-1}$, $y_{P-1}$ ]. 

# Scoring
Your score is the sum of all scores of the tasks finished.
In order for your submission to be valid, you must ensure that:
- the arms are never instructed to expand beyond the workspace, to a mount point (regardless of whether any arm is mounted there – but note that an arm is always allowed to retract to its own mount point) or to a cell occupied in the same step by some robotic arm, and
- each task is assigned to at most one arm, and
- each arm completes all tasks assigned to it.

Note that the robotic arms can be in any con guration after finishing a task and don't need to be retracted to the initial position. You don't need to finish all tasks to receive points for your submission.
