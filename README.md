# Maze Generator And Solver
Program Purpose: Generates a maze that then solves itself

Language: Python and Pygame

Algorithm: Randomized DFS / Floodfill / Recursive Backtracking

[Link to Project](https://replit.com/@joshualiu555/Pixel-Art-Maker)

[Wikipedia Algorithm Pseudocode](https://en.wikipedia.org/wiki/Maze_generation_algorithm)

[Inspired by The Coding Train](https://www.youtube.com/watch?v=HyK_Q5rrcr4rl)

[Demo](https://user-images.githubusercontent.com/53412192/120880638-39779480-c591-11eb-914e-c4ae03ddb413.mov)


## How the program works
###### Generation
1) Maintain a matrix that keeps track of visited cells
2) Maintain a stack that keeps track of cells on the current path
3) Start at the top left cell
4) Randomly choose one of the available neighbor cells
5) If there are none, go to previous cell in the stack
6) Color visited cells blue, current cell blue, and remove the white wall
7) Will eventually return to the top left cell and guarantees a maze
###### Solving
1) Maintain a matrix that keeps track of visited cells
2) Maintain a stack that keeps track of cells on the current path
3) Start at the top left cell
4) Randomly choose one of the available neighbor cells without a wall
5) If there are none, go to previous cell in the stack
6) Color visited cells green and current cell red
7) Will eventually reach the bottom right cell, at which point the program restarts

## Code Overview
1) A matrix of cell classes: each cell instance maintains properties such as a wall array, visited / current booleans, and methods to draw to the screen
2) Simulation Function 
   1) Generation - Find next cell, check if it is inbounds and unvisited, remove the wall, move to that cell 
   2) Solving - Find next cell, check if it is inbounds and unvisited, move to that cell

## Install as executable file
Open the terminal / command line

`pip install pyinstaller`

Put `maze.py` inside of a folder called `main` (or whatever name you want)

Open up a terminal / command line inside the folder

`pyinstaller --onefile -w maze.py`

Go to `dist` and select `main.exe`
