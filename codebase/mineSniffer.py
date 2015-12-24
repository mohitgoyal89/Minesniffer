import copy
import itertools

class MineSniffer():
    def __init__(self):
        self.minesniffer = [[], []]
        self.row = 0
        self.col = 0

# read the initial game state from the input file
    def readGameState(self, filePath):

        fileHandle = open(filePath, 'r')

        gameAttr = fileHandle.readline().rstrip('\n').split(' ')

        self.row = int(gameAttr[0])
        self.col = int(gameAttr[1])

        self.minesniffer = [[0 for x in range(self.col)] for x in range(self.row)]

        gameRawState = [line.rstrip('\n').split(',') for line in open(filePath)]
        gameRawState.remove(gameRawState[0])

        if len(gameRawState) != self.row:
            print "Wrong gameState given, check txt file"
            exit(0)
        else:
            for i in range(self.row):
                if len(gameRawState[i]) != self.col:
                    print "Wrong gameState given, check txt file"
                    exit(0)

        # storing the game state into list
        for i in range(self.row):
            for j in range(self.col):
                if gameRawState[i][j] == 'X':
                    self.minesniffer[i][j] = -1
                else:
                    self.minesniffer[i][j] = int(gameRawState[i][j])

        self.minesniffer.reverse()

        return self.minesniffer

    def getGameDimen(self, ):
        return [self.row, self.col]

# returning the hints set
def mineHints(game, row, col):
    hints = set()

    for i in xrange(0, row):
        for j in xrange(0, col):
            if game[i][j] != -1:
                pos = (i, j)
                hints.add(pos)

    return list(hints)

# Checking for neighbours on all the eight sides for possible mines
def checkNeighbours(game, pos, row, col):
    x, y = pos
    neighbours = []

    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if i >= 0 and j >= 0 and i < row and j < col and game[i][j] < 0:
                neighbours.append(-1*game[i][j])

    return neighbours

# convert game into cnf form
def convert2CNF(game, row, col):
    cnf = []

    hintsPos = mineHints(game, row, col)

    varName = 0
    for i in xrange(0, row):
        for j in xrange(0, col):
            if game[i][j] == -1:
                varName = varName + 1
                game[i][j] = -varName
            else:
                game[i][j] = game[i][j]


    for pos in hintsPos:
        neighbours = checkNeighbours(game, pos, row, col)

        n = len(neighbours)
        k = game[pos[0]][pos[1]]

        tempCnf = []

        if n >= 1:
            # checking if the value of hints is 0
            if k == 0:
                for elem in range(n):
                    tempCnf.append([neighbours[elem]])

            # check if the value of hints is number of mines
            if k == n:
                for elem in range(n):
                    tempCnf.append([-1*neighbours[elem]])

            # check for the rest of the cases
            if k > 0 and k+1 <= n:
                # calculating at least mines
                atleastMines = list(itertools.combinations(neighbours, n-k+1))

                for elem in range(len(atleastMines)):
                    tmpNeighbours = copy.deepcopy(neighbours)
                    tmpNeighbours[:] = [-1 * elem for elem in list(atleastMines[elem])]
                    tempCnf.append(tmpNeighbours)

                # calculating at most mines
                atmostMines = list(itertools.combinations(neighbours, k+1))

                for elem in range(len(atmostMines)):
                    tempNeighbours = copy.deepcopy(neighbours)
                    tempNeighbours[:] = [elem for elem in list(atmostMines[elem])]
                    tempCnf.append(tempNeighbours)

            # appending all the possible cnf
            for elem in range(0, len(tempCnf)):
                if tempCnf[elem] not in cnf:
                    cnf.append(tempCnf[elem])

    '''
    # DEBUG
    print varName
    print cnf
    '''

    return [varName, cnf]