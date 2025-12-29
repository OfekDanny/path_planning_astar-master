
# header files
from utils import *
import sys


startCol = int(input("Enter the x-coordinate for start node : "))
startRow = int(input("Enter the y-coordinate for start node : "))
goalCol = int(input("Enter the x-coordinate for goal node : "))
goalRow = int(input("Enter the y-coordinate for goal node : "))
radius = int(input("Enter the radius for the robot : "))
clearance = int(input("Enter the clearance for the robot : "))
stepSize = int(input("Enter the step size : "))

# take start and goal node as input
start = (startRow, startCol)
goal = (goalRow, goalCol)
astar = AStar(start, goal, clearance, radius, stepSize)

if(astar.IsValid(start[0], start[1])):
    if(astar.IsValid(goal[0], goal[1])):
        if(astar.IsObstacle(start[0],start[1]) == False):
            if(astar.IsObstacle(goal[0], goal[1]) == False):
                (exploredStates, backtrackStates, distanceFromStartToGoal) = astar.search()
                astar.animate(exploredStates, backtrackStates, "./astar_rigid.avi")

                # print optimal path found or not
                if(distanceFromStartToGoal == float('inf')):
                    print("\nNo optimal path found.")
                else:
                    print("\nOptimal path found. Distance is " + str(distanceFromStartToGoal))
            else:
                print("The entered goal node is an obstacle ")
                print("Please check README.md file for running astar.py file.")
        else:
            print("The entered start node is an obstacle ")
            print("Please check README.md file for running astar.py file.")
    else:
        print("The entered goal node outside the map ")
        print("Please check README.md file for running astar.py file.")
else:
    print("The entered start node is outside the map ")
    print("Please check README.md file for running astar.py file.")
