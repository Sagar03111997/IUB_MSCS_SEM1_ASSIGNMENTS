Part 1 Navigation 

Initial State: Here in this problem the initial state is the location of Pichu which is indicated by the letter 'p'. 
Successor State: We need to put the Pichu('p')on the next node where there is no wall('X') and the next node should be present inside the map i.e it should be a valid move. ('.'). [We used a valid index function and moves function for this.]
Cost Function: For each move of the Pichu the cost function is 1.
Goal State: The goal state is the final position or the goal position for Pichu and it is indicated by '@' on the map.

We need to find the shortest path from the initial position to the goal position.

Approach: BFS

1. When I tried to run the given program, I found out that the program was ending in an infinite loop. To check this I printed the fringe value and I found that Pichu was going from one node to another node and then again it was coming back to the same node. This was happening because there was no logic present to store the visited nodes.
2. So, I created a list to store the visited nodes. Then I appended the current moves into that list. If the next move is not present on the visited list then I have added it to the fringe.
3. After this step, I was able to get the shortest distance from the initial node to the goal node but the direction of Pichu traversing was not printing.
4. To find the direction for the shortest path I created a get_direction function which takes a current move, move, and capture_move as a parameter and returns the direction as Up, Down, Left, and Right as the output.
5. I append all the returned directions in a string and was able to get the correct pichu traversing from the initial node to the goal node.

Part 2 Hide and Seek

In this problem, we have to put k pichus on a map in such a way that two pichus cannot see each other.
This problem is similar to the n-queens problem but here the wall is an extra element on the map. If there is a wall between two pichus then we can place them in the same row.
The basic skeleton of the code was provided by the professor. We only needed to create a function that checks for rows, columns, and diagonals considering the wall factor.
To place the pichus according to the above condition I created and called the verify_path function inside the successor method.
This verify path function takes the house map, row, and column as input. Inside this function, I have declared and checked certain conditions. Such as:
It checks the top of the Pichu.
It checks the left and right of the Pichu.
It checks diagonally i.e in the right and left diagonal of the Pichu.
From the above mentioned conditions I get the position to place the next Pichu on the map and returns back to the successor function which in turns return to the add pichu function and places the next pichu on the map.
We can keep adding agents and the function verify path will find the best possible destination for the placing the next pichu. When max pichus i.e agents are met, and if the argument passes more agents then the function returns False
