from copyreg import constructor
import threading
import os
import random

#easy
#blankGrid = [[1, 9, 6, 0, 5, 3, 0, 0, 0],
#             [7, 0, 0, 2, 1, 0, 3, 0, 0],
#             [0, 3, 0, 0, 0, 6, 0, 0, 7],
#             [0, 7, 0, 0, 0, 2, 4, 1, 0],
#             [5, 6, 1, 3, 7, 4, 0, 0, 0],
#             [4, 0, 0, 0, 0, 0, 7, 0, 0],
#             [6, 1, 0, 0, 2, 0, 5, 0, 9],
#             [2, 0, 0, 6, 0, 0, 8, 3, 0],
#             [0, 8, 0, 5, 3, 0, 0, 7, 2]]

#expert
blankGridExpert = [[3, 7, 9, 0, 0, 0, 0, 0, 0],
             [8, 0, 0, 4, 2, 0, 0, 0, 0],
             [2, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 5, 0, 0, 0, 0, 0, 2, 0],
             [0, 0, 7, 0, 0, 0, 0, 0, 8],
             [0, 0, 0, 0, 6, 5, 0, 0, 4],
             [0, 0, 0, 9, 0, 0, 0, 0, 0],
             [0, 8, 0, 3, 0, 0, 7, 0, 0],
             [0, 0, 0, 0, 0, 2, 3, 9, 0]]

blankGridEvil = [[3, 0, 0, 0, 0, 0, 0, 2, 0],
             [4, 0, 0, 0, 9, 0, 0, 0, 0],
             [0, 9, 2, 6, 0, 0, 8, 0, 0],
             [9, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 5, 1, 0, 6, 0, 0, 4, 0],
             [0, 0, 0, 8, 0, 0, 0, 0, 7],
             [0, 0, 0, 0, 0, 1, 4, 0, 0],
             [0, 0, 3, 0, 0, 0, 0, 0, 0],
             [0, 2, 6, 0, 5, 0, 0, 1, 0]]

#crazy
blankGridHardest = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 3, 6, 0, 0, 0, 0, 0],
             [0, 7, 0, 0, 9, 0, 2, 0, 0],
             [0, 5, 0, 0, 0, 7, 0, 0, 0],
             [0, 0, 0, 0, 4, 5, 7, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 3, 0],
             [0, 0, 1, 0, 0, 0, 0, 6, 8],
             [0, 0, 8, 5, 0, 0, 0, 1, 0],
             [0, 9, 0, 0, 0, 0, 4, 0, 0]]

blankGridImpossible = [[0, 4, 0, 0, 0, 0, 0, 0, 0],
                    [7, 0, 0, 0, 0, 0, 0, 0, 9],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 2, 4, 5, 0, 0, 8, 0, 0],
                    [0, 0, 9, 0, 0, 0, 3, 0, 0],
                    [0, 0, 1, 3, 7, 0, 0, 5, 6],
                    [0, 0, 0, 0, 6, 1, 0, 0, 0],
                    [2, 0, 0, 0, 3, 0, 0, 7, 4],
                    [1, 3, 0, 0, 8, 0, 0, 2, 0]]


def createGrid():
    rows = []
    for y in range(0,9):
        row = []
        for x in range(0, 9):
            row.append(0)
        rows.append(row)
    return rows

def printGrid(grid):
    for row in grid:
        print(row)

def printResult(grid, original):
    for row in range(0,9):
        print(original[row],"  --->  ",grid[row])

iterations = 0
firstPositionX = None
firstPositionY = None
refreshCount = 0
originalGrid = None
def solve(grid, positionX, positionY):
    if verifyPosition(grid, positionY, positionX) == False:
        return False

    global originalGrid
    global iterations
    global refreshCount

    if originalGrid == None:
        originalGrid = [row[:] for row in grid]
    iterations += 1
    if grid[positionY][positionX] != 0:
        if positionX == 8:
            if positionY == 8:
                cleanPrint(originalGrid, grid)
                print("Iterations: "+str(iterations))
                return True
            else:
                return solve(grid, 0, positionY+1)
        else:
            return solve(grid, positionX+1, positionY)
    else:
        global firstPositionY, firstPositionX
        if firstPositionY == None:
            firstPositionY = positionY
            firstPositionX = positionX
        startPosition = getFirstAvailableNumber(grid, positionY, positionX)
        if startPosition < 0:
            return False
        for value in range (startPosition, 10):
            grid[positionY][positionX] = value
            
            solveResult = solve(grid, positionX, positionY)
            if solveResult == False and value == 9:
                grid[positionY][positionX] = 0
                #if positionY == firstPositionY and positionX == firstPositionX:
                #    print("No solution found :(")
                return False
            if solveResult:
                return True

        

def getFirstAvailableNumber(grid, positionY, positionX):
    available = [True] * 9
    for number in range(0,9):
        if grid[positionY][number] != 0:
            available[grid[positionY][number]-1] = False
    for number in range(0,9):
        if grid[number][positionX] != 0:
            available[grid[number][positionX]-1] = False
    
    if True in available:
        first_index = available.index(True)
        return first_index + 1
    else:
        return -1

def checkHorizontal(grid):
    for row in grid:
        rowPopulated = [False] * 9
        for column in row:
            if column != 0:
                if rowPopulated[column-1]:
                    return False
                else:
                    rowPopulated[column-1] = True
    return True

def checkVertical(grid):
    for column in range(0, 9):
        columnPopulated = [False] * 9
        for row in grid:
            if row[column] != 0:
                if columnPopulated[row[column]-1]:
                    return False
                else:
                    columnPopulated[row[column]-1] = True
    return True

def checkRegion(grid):
    for region in range(0, 9):
        regionPopulated = [False] * 9
        offsetX = (region % 3) * 3
        offsetY = (region // 3) * 3

        for column in range(offsetY+0, offsetY+3):
            roowStr = ""
            for row in range(offsetX+0, offsetX+3):
                value = grid[column][row]
                roowStr = roowStr + " " + str(value)
                if value != 0:
                    if regionPopulated[value-1]:
                        return False
                    else:
                        regionPopulated[value-1] = True
    return True

def checkGrid(grid):
    return checkHorizontal(grid) and checkVertical(grid) and checkRegion(grid)

def verifyPosition(grid, positionY, positionX):
    input = grid[positionY][positionX]
    if input == 0:
        return True
    for number in range(0,9):
        if number == positionX:
            continue
        if grid[positionY][number] == input:
            return False
    for number in range(0,9):
        if number == positionY:
            continue
        if grid[number][positionX] == input:
            return False

    regionXOffset = (positionX // 3) * 3
    regionYOffset = (positionY // 3) * 3
    for y in range(0, 3):
        for x in range(0, 3):
            if y+regionYOffset == positionY and x+regionXOffset == positionX :
                continue
            if grid[y+regionYOffset][x+regionXOffset] == input:
                return False
    return True


def createGame(desiredClueCount):
    count = 0
    while count != desiredClueCount:
        gameBoard = [[0]*9 for i in range(9)]
        count = 0
        for column in range(0,9):
            for row in range(0,9):
                number = random.randint(1,9)
                chance = random.randint(1,9)
                if chance < 3:
                    gameBoard[column][row] = number
                    count += 1
                    while verifyPosition(gameBoard, column, row) == False:
                        number = random.randint(0,9)
                        gameBoard[column][row] = number
    #printGrid(gameBoard)
    #print("clue count: {}".format(count))
    return gameBoard

def createAndPlay():
    gameCount = 0
    while gameCount < 10:
        game = generateGame()
        global originalGrid
        global iterations
        originalGrid = None
        iterations = 0
        print()
        result = solve(game, 0 ,0)
        if result:
            gameCount += 1
        print(result)

def generateGame():
    base  = 3
    side  = base*base

    # pattern for a baseline valid solution
    def pattern(r,c): return (base*(r%base)+r//base+c)%side

    # randomize rows, columns and numbers (of valid base pattern)
    from random import sample
    def shuffle(s): return sample(s,len(s)) 
    rBase = range(base) 
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

    #for line in board: print(line)
    squares = side*side
    empties = squares * 3//4
    for p in sample(range(squares),empties):
        board[p//side][p%side] = 0

    numSize = len(str(side))
    #for line in board: print("["+"  ".join(f"{n or '0':{numSize}}" for n in line)+"]")
    return board

def cleanPrint(board):
    base = 3
    side = 9
    def expandLine(line):
        return line[0]+line[5:9].join([line[1:5]*(base-1)]*base)+line[9:13]
    line0  = expandLine("╔═══╤═══╦═══╗")
    line1  = expandLine("║ . │ . ║ . ║")
    line2  = expandLine("╟───┼───╫───╢")
    line3  = expandLine("╠═══╪═══╬═══╣")
    line4  = expandLine("╚═══╧═══╩═══╝")

    symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums   = [ [""]+[symbol[n] for n in row] for row in board ]
    print(line0)
    for r in range(1,side+1):
        print( "".join(n+s for n,s in zip(nums[r-1],line1.split("."))) )
        print([line2,line3,line4][(r%side==0)+(r%base==0)])

def cleanPrint(board, solved):
    base = 3
    side = 9
    def expandLine(line):
        return line[0]+line[5:9].join([line[1:5]*(base-1)]*base)+line[9:13]
    line0  = expandLine("╔═══╤═══╦═══╗")
    line1  = expandLine("║ . │ . ║ . ║")
    line2  = expandLine("╟───┼───╫───╢")
    line3  = expandLine("╠═══╪═══╬═══╣")
    line4  = expandLine("╚═══╧═══╩═══╝")

    symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums   = [ [""]+[symbol[n] for n in row] for row in board ]
    nums2   = [ [""]+[symbol[n] for n in row] for row in solved ]
    print(line0, "   --->   ",line0)
    for r in range(1,side+1):
        print( "".join(n+s for n,s in zip(nums[r-1],line1.split("."))), "   --->   ", "".join(n+s for n,s in zip(nums2[r-1],line1.split("."))))
        print([line2,line3,line4][(r%side==0)+(r%base==0)], "   --->   ", [line2,line3,line4][(r%side==0)+(r%base==0)])

print(solve(blankGridEvil, 0, 0))
#print(getFirstAvailableNumber(blankGrid, 0, 4))
#print(checkGrid(testSolve))
#36 / 41 / 28
#createAndPlay()
#generateGame()