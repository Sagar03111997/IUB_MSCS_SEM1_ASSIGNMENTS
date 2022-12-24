# sdsahu-rbhagcha-dwamanne

## Part 1: Birds, heuristics, and A* 

Here, the challenge is to use the A* search algorithm to quickly sort the unsorted set of five birds into an order of 1 to N.

Implementation
The A* search algorithm can be used to find a goal state where each bird is in the order 1 to N in order to solve this challenge. Exactly one bird can swap places with a neighboring bird in each of our successor states. The objective is to locate the goal state within 10 seconds and in the fewest possible steps.

A* search : We need to define an admissible heuristic function h(s) and the g(s) which is the cost for the best path found till each state and apply Best First Search.

State space: Exactly one bird switches places with exactly one of its neighbors in each step.
For instance, if the initial state is [1, 3, 4, 2, 5], the succeeding states are:
[3, 1, 4, 2, 5]
[1, 4, 3, 2, 5]
[1, 3, 2, 4, 5]
[1, 3, 4, 5, 2]

Successor function: In the provided code, which is shown below, we already have a predefined successor function.
[ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]

Goal state : Goal state is the state where all the birds are arranged in the order of 1 to N.
Heuristic function : Here, the heuristic function h(s) is basically the number of misplaced birds.
g(s) : It is the cost of best path found so far to s.

Working of Algorithm:
Define fringe using a Priority Queue. In this way, we can pop the most promising state from the fringe first so that we can reach the goal with minimum cost that is with less number of steps from the initial state to goal state through all the successor states.
Insert the initial state to the Fringe.
while Fringe is not empty pop the most promising state from the Fringe 
If the state is the goal state then return the path Else get the successor state from the present state
insert every successor state and its cost into the Fringe
If the fringe is empty then return nothing in the path
For Example: From state [1, 3, 4, 2, 5] found goal state by taking path: [[1, 3, 4, 2, 5], [1, 3, 2, 4, 5], [1, 2, 3, 4, 5]]

The successor state for depth 1:
[3, 1, 4, 2, 5]
[1, 4, 3, 2, 5]
[1, 3, 2, 4, 5]
[1, 3, 4, 5, 2]

The successor state for depth 2:
[3, 1, 2, 4, 5]
[1, 2, 3, 4, 5]
[1, 3, 4, 2, 5]
[1, 3, 2, 5, 4]

The state with minimum cost is popped at each level and the goal is reached in 3 steps.



## Part 2: The 2022 Puzzle
 
Here goal is to find a short sequence of moves that restores the canonical configuration

State space - Any number of ways of changing the board by sliding and rotating rows and columns of board
Initial state - Any board in which numbers are randomly placed
Goal state - Restore the canonical configuration of the board

A* search f(s) = g(s) + h(s)
g(s) = cost from start to s, here we calculated by pow(cost, 2)/2 (squared and halved the cost)
h(s) = cost of reaching the goal from s, which is manhattan distance here

Successor function - This changes the board by sliding and rotating the rows and columns and give us the new state 
along with the move taken

1) Branching factor of search tree:
    Sliding rows left : 5
    Sliding rows right: 5
    Sliding columns up : 5
    Sliding columns down : 5
    Rotating outer clockwise : 1
    Rotating inner clockwise : 1
    Rotating outer counterclockwise : 1
    Rotating inner counterclockwise : 1
    Total branches is 24 
2) Breadth first search go through all the states in level 1 and goes on
    In this case as each state will have 24 branches and each will again have 24, for a search to reach 7
    moves it takes 24 + 24^2 + 24^3 + ..... 24^7 which is around 4.5 * 10^9 ( around 4.5 Billion)

Implementation:
1) Started with writing code for the successors which is sliding the rows left and right, sliding the columns up and 
down and rotating clockwise and counterclockwise.
2) Initially implemented the heuristic function with misplaced tiles which worked for board0 but board1 was going 
into loop
3) Later changed the heuristic to manhattan and the issue was still persisting.
4) Based on the robot navigation taught in class tried adding the cost by squaring and halved it to reduce the penalty 
caused by proceeding in a wrong path and used heapq to sort the states based on f(s)
5) Kept on modifying the cost function to reach the goal in 11 moves and within 15 minutes for board 1

Algorithm:
1) Defined a fringe and used Heap Queue as it has sorts all the elements based on the first value, here we have f(s) as
the first value which helps in giving minimum number of moves
2) Check if any fringe is available if so pop it out and add it to the visited state and check if goal state is achieved
3) If goal is not reached, find the successors of the state and add the new state and move in the heapq along with
f(s) and h(s) and continue till goal is reached
4) If no fringes are present return empty path

## PART 3: Road  trip!
State Space: Travel from one city to another city
Initial State: Source city
Goal State: Destination\end city
Cost Function: Here the cost function is selected based on segments, distance, time and delivery. 
- For segment cost function a counter is set up for each city visited.  
- Shortest distance between cities are calculated in cost function distance using euclidean distance formula.
- For time cost function, based on the speed limit cost function value is calculated and return the optimal value while calculating euclidean distance between cities.
- Delivery cost function use the speed limit should be less than 50 else performa an operation for certain driver while calculating euclidean distance between cities.

Working:
Code runs in the following manner:
- Initially define fringe to store the cost function with the source city with all the cost function value.
- Iterate over the fringe until it becomes empty.
- Find the attached cities to the selected city add that to the fringe.
- Find the cost function for the selected city and select the city with the optimal cost value of the selected cost function.
- If reach the destination return the cost function sum value. 

For example: 1. Reach to Union_Center,Indiana from Bloomington,Indiana using cost function time
- Total segments: 16
- Total miles: 198.000
- Total hours: 3.835
- Total hours for delivery: 4.523

2. Reach to Union_Center,Indiana from Bloomington,Indiana using cost function segments
- Total segments: 9
- Total miles: 182.000
- Total hours: 4.046
- Total hours for delivery: 4.201

3. Reach to Union_Center,Indiana from Bloomington,Indiana using cost function delivery
- Total segments: 14
- Total miles: 188.000
- Total hours: 3.867
- Total hours for delivery: 4.069
