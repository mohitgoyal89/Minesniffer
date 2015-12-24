import sys
import mineSniffer
from mineSniffer import MineSniffer

# TEAM MEMBERS
# MOHIT GOYAL (110349552)
# DEEPAK GOYAL (110347387)

# Reference: https://www.cs.berkeley.edu/~daw/teaching/cs70-s05/Notes/lecture09.pdf

def parse_file(filepath):
    # read the layout file to the board array
    board = [[], []]

    mSniffer = MineSniffer()
    board = mSniffer.readGameState(filepath)
    row, col =mSniffer.getGameDimen()

    return [board, row, col]

def convert2CNF(board, output):
    # interpret the number constraints

    game = board[0]
    row = board[1]
    col = board[2]

    '''
    # DEBUG
    print "game" + str(game)
    print "row" + str(row)
    print "col" + str(col)
    '''

    # calling minesniffer's method to convert game into CNF
    cnf = mineSniffer.convert2CNF(game, row, col)

    no_of_var = cnf[0]
    no_of_clauses = len(cnf[1])

    # writing CNF to output file
    fileHandle = open(output, 'w')
    fileHandle.write('c ' + "Homework-2 Mine Sniffer Game" + '\n')
    fileHandle.write('p cnf %d %d\n' % (no_of_var, no_of_clauses))

    for elem in cnf[1]:
        fileHandle.write(' '.join(str(v) for v in elem) + ' 0\n')

    fileHandle.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board = parse_file(sys.argv[1])
    convert2CNF(board, sys.argv[2])