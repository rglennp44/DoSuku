from calculate import checkSolved, findBoxNeeds, findColNeeds, findRowNeeds, findCellOptions, findSingleOptions, updateData, updateNeeds, whichBox
from puzzlein import testPuzzle
from userInterface import displayPuzzle, printDebug

# Import Data and Display Unsolved Puzzle
data = testPuzzle()
print("\nInitial Puzzle: \n")
displayPuzzle(data)

# Declare Needs Arrays
rowNeeds = []
colNeeds = []
boxNeeds = []
cellOptions = [None] * 81
changeBuffer = []

# Populate Needs Arrays
for row in range(9):
    rowNeeds.append(findRowNeeds(data, row))
for col in range(9):
    colNeeds.append(findColNeeds(data, col))
for box in range(9):
    boxNeeds.append(findBoxNeeds(data, box))

solved = False
while(not solved):
    # Find Possible solutions for each cell
    [cellOptions, changeBuffer] = findSingleOptions(
        data, rowNeeds, colNeeds, boxNeeds, cellOptions)

    # Update Data Array
    data = updateData(data, changeBuffer)

    # Update Needs Array
    [rowNeeds, colNeeds, boxNeeds] = updateNeeds(
        changeBuffer, rowNeeds, colNeeds, boxNeeds)

    # Display Puzzle
    displayPuzzle(data)

    # Check if Puzzle is Solved
    solved = checkSolved(data)
