from constraint import *

def dataNormalize (data):
    rullo_nums = [ eachPos[1] for eachPos in sorted( data['data'][0].items() ) ]
    for step in xrange(0,data['h']*data['w'],data['w']):
        print rullo_nums[step:step+data['w']]


def rullo_solve ():
    '''
        User specifies file names where puzzle matrix and constraint are located

        Stored as list of ints
    '''
    fileName_matrix = raw_input("Filepath for puzzle: ")
    if fileName_matrix.strip() == "":
        fileName_matrix = "rullo_matrix.txt"

    fileName_constraints = raw_input("Filepath for constraints: ")
    if fileName_constraints.strip() == "":
        fileName_constraints = "rullo_constraints.txt"

    # Take Data from files and store them
    puzzleMatrix = open(fileName_matrix).read()
    puzzleConstraints = open(fileName_constraints).read()

    # Split the constraint in rows and columns. 
    constraintsForColumns, constraintsForRows = puzzleConstraints.split("\n")

    puzzleList = [ int(eachNum) for eachNum in puzzleMatrix.split() ]
    constraintsForColumns = [ int(eachNum) for eachNum in constraintsForColumns.split() ]
    constraintsForRows = [ int(eachNum) for eachNum in constraintsForRows.split() ]
    
    # Quick method to find dimenstion of puzzle
    puzzleWidth = len(constraintsForColumns)
    puzzleHeight = len(constraintsForRows)
    print 'Puzzle Size: {}x{}'.format(puzzleWidth, puzzleHeight)

    # Problem instanciated
    problem = Problem( RecursiveBacktrackingSolver() )

    # Build index from dimensions
    puzzleIndex = [ (row, col) for row in range(puzzleHeight) for col in range(puzzleWidth) ]

    # Put rullo matrix into problem
    for eachIndex,eachValue in zip(puzzleIndex, puzzleList):
        problem.addVariable(eachIndex, [0, eachValue] )
        #print '{}, {}'.format(eachIndex, eachValue)

    # Constraints setting
    # Each rows and columns must add to specified constraint
    for ci in  range(0, puzzleWidth):
        columnIndexes = []
        for ri in range(0, puzzleHeight):
            columnIndexes.append((ri,ci))
        #print '{}: {}'.format(constraintsForColumns[ci], columnIndexes)
        problem.addConstraint(ExactSumConstraint(constraintsForColumns[ci]),columnIndexes)

    for ri in  range(0, puzzleHeight):
        rowIndexes = []
        for ci in range(0,puzzleWidth):
            rowIndexes.append((ri,ci))
        #print constraintsForRows[i]
        problem.addConstraint(ExactSumConstraint(constraintsForRows[ri]),rowIndexes)
    
    solution ={'w':puzzleWidth, 'h':puzzleHeight, 'data':problem.getSolutions()}
    return solution
if __name__ == '__main__':
    print "rullo output\n\n"
    dataNormalize(rullo_solve())
    raw_input("\n\nEnter any key to exit")