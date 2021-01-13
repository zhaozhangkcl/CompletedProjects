# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

class MDPAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"


    #Algorithm that find the best policy
    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        print "Running registerInitialState for MDPAgent!"
        print "I'm at:"
        print api.whereAmI(state)
        print type(state)
        self.makeMap(state)
        self.updateFoodInMap(state)
        self.map.display()

    def getLayoutHeight(self, corners):
        height = -1
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        return height + 1

    def getLayoutWidth(self, corners):
        width = -1
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        return width + 1



    def makeMap(self,state):
        corners = api.corners(state)
        print corners
        height = self.getLayoutHeight(corners)
        width  = self.getLayoutWidth(corners)
        self.map = Grid(width, height)
    

    # Create a map with a current picture of the food that exists.
    def updateFoodInMap(self, state):
        # First, make all grid elements that aren't walls blank.
        for i in range(self.map.getWidth()):
            for j in range(self.map.getHeight()):
                self.map.setValue(i, j, (-0.04,0))
        food = api.food(state)
        for i in range(len(food)):
            self.map.setValue(food[i][0], food[i][1], (1,0))
        
    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like the game just ended!"

    # function that updates location of ghost in the map
    def updateGhostInMap(self, state):
        # get separate list where ghosts state are displayed as well as their mode
        ghostStatesMode = api.ghostStates(state)
        for pos in ghostStatesMode:
            # check if the second element is 1
            if pos[1] == 1:
                self.map.setValue(int(pos[0][0]),int(pos[0][1]),(0.5,self.map.getValue(int(pos[0][0]),int(pos[0][1]))[1]))
            if pos[1] == 0:
                # if ghost state is 0, set reward to -1
                self.map.setValue(int(pos[0][0]),int(pos[0][1]), (-20, self.map.getValue(int(pos[0][0]), int(pos[0][1]))[1]))

    def legalMoves(self, x, y, state):
        # empty list to return
        legal = []
        # get a list of walls
        walls = api.walls(state)
        # check if neighbour is a wall
        if not ((x, y + 1) in walls):
            legal.append(Directions.NORTH)
        if not (x, y - 1) in walls:
            legal.append(Directions.SOUTH)
        if not (x + 1, y) in walls:
            legal.append(Directions.EAST)
        if not (x - 1, y) in walls:
            legal.append(Directions.WEST)
        return legal



    def value_iteration(self, state, discount, limit):
        # defines two local variables for keep track of current utility and next utility
        nextIteration = {}
        counter = 0
        while counter < limit:
            # remembers what the previous configuration was
            # iterate through for every state on the map
            for i in range(self.map.getWidth()):
                for j in range(self.map.getHeight()):
                    currentPos = (i,j)
                    legal = self.legalMoves(i,j,state)
                    action = {}
                    for move in legal:
                        # create a dictionary for the move
                        if move == Directions.NORTH:
                            actionNorth = 0.8 * self.map.getValue(currentPos[0], currentPos[1] + 1)[1] + 0.1 * \
                                          self.map.getValue(
                                              currentPos[0] - 1, currentPos[1])[1] + 0.1 * \
                                          self.map.getValue(currentPos[0] + 1, currentPos[1])[1]
                            action[move] = actionNorth
                        elif move == Directions.SOUTH:
                            actionSouth = 0.8 * self.map.getValue(currentPos[0], currentPos[1] - 1)[1] + 0.1 * \
                                          self.map.getValue(
                                              currentPos[0] - 1, currentPos[1])[1] + 0.1 * \
                                          self.map.getValue(currentPos[0] + 1, currentPos[1])[1]
                            action[move] = actionSouth
                        elif move == Directions.WEST:
                            actionWest = 0.8 * self.map.getValue(currentPos[0] - 1, currentPos[1])[1] + 0.1 * \
                                         self.map.getValue(
                                             currentPos[0], currentPos[1] + 1)[1] + 0.1 * \
                                         self.map.getValue(currentPos[0], currentPos[1] - 1)[1]
                            action[move] = actionWest
                        else:
                            actionEast = 0.8 * self.map.getValue(currentPos[0] + 1, currentPos[1])[1] + 0.1 * \
                                         self.map.getValue(
                                             currentPos[0], currentPos[1] + 1)[1] + 0.1 * \
                                         self.map.getValue(currentPos[0], currentPos[1] - 1)[1]
                            action[move] = actionEast
                    maxExpectedUtilityMove = max(action, key=action.get)
                    maxUtil = action.get(maxExpectedUtilityMove)
                    discountedMaxUtil = maxUtil * discount
                    nextIteration[currentPos] = discountedMaxUtil + self.map.getValue(currentPos[0], currentPos[1])[0]
            for i in range(self.map.getWidth()):
                for j in range(self.map.getHeight()):
                    self.map.setValue(i, j, (self.map.getValue(i, j)[0], nextIteration[(i, j)]))
            counter = counter + 1

        for i in range(self.map.getWidth()):
            for j in range(self.map.getHeight()):
                print self.map.getValue(i,j)[1]
    # For now I just move randomly
    def getAction(self, state):
        self.updateFoodInMap(state)
        self.updateGhostInMap(state)
        self.map.prettyDisplay()
        self.value_iteration(state, 0.9, 20)
        # check where pacman is
        currentPos = api.whereAmI(state)
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        action = {}
        for move in legal:
            # create a dictionary for the move
            if move == Directions.NORTH:
                actionNorth = 0.8 * self.map.getValue(currentPos[0], currentPos[1] + 1)[1] + 0.1 * self.map.getValue(
                    currentPos[0] - 1, currentPos[1])[1] + 0.1 * self.map.getValue(currentPos[0] + 1, currentPos[1])[1]
                action[move] = actionNorth
            elif move == Directions.SOUTH:
                actionSouth = 0.8 * self.map.getValue(currentPos[0], currentPos[1] - 1)[1] + 0.1 * self.map.getValue(
                    currentPos[0] - 1, currentPos[1])[1] + 0.1 * self.map.getValue(currentPos[0] + 1, currentPos[1])[1]
                action[move] = actionSouth
            elif move == Directions.WEST:
                actionWest = 0.8 * self.map.getValue(currentPos[0] - 1, currentPos[1])[1] + 0.1 * self.map.getValue(
                    currentPos[0], currentPos[1] + 1)[1] + 0.1 * self.map.getValue(currentPos[0], currentPos[1] - 1)[1]
                action[move] = actionWest
            else:
                actionEast = 0.8 * self.map.getValue(currentPos[0] + 1, currentPos[1])[1] + 0.1 * self.map.getValue(
                    currentPos[0], currentPos[1] + 1)[1] + 0.1 * self.map.getValue(currentPos[0], currentPos[1] - 1)[1]
                action[move] = actionEast
        maxExpectedUtilityMove = max(action, key=action.get)
        return api.makeMove(maxExpectedUtilityMove, legal)

class Grid:
         
    # Constructor
    #
    # Note that it creates variables:
    #
    # grid:   an array that has one position for each element in the grid.
    # width:  the width of the grid
    # height: the height of the grid
    #
    # Grid elements are not restricted, so you can place whatever you
    # like at each location. You just have to be careful how you
    # handle the elements when you use them.
    def __init__(self, width, height):
        self.width = width
        self.height = height
        subgrid = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                row.append(0)
            subgrid.append(row)

        self.grid = subgrid

    # Print the grid out.
    def display(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[i][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print

    # The display function prints the grid out upside down. This
    # prints the grid out so that it matches the view we see when we
    # look at Pacman.
    def prettyDisplay(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[self.height - (i + 1)][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print
        
    # Set and get the values of specific elements in the grid.
    # Here x and y are indices.
    def setValue(self, x, y, value):
        self.grid[y][x] = value

    def getValue(self, x, y):
        if x < 0:
            x = 0
        if x >= self.getWidth():
            x = self.getWidth()-1
        if y < 0:
            y = 0;
        if y >= self.getHeight():
            y = self.getHeight()-1
        return self.grid[y][x]

    # Return width and height to support functions that manipulate the
    # values stored in the grid.
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

