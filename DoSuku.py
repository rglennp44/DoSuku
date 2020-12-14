from calculate import checkSolved, findNeeds, findCellOptions, resolveChanges, whichBox
from puzzlein import testPuzzle
from userInterface import displayPuzzle, printDebug

# Import Data and Display Unsolved Puzzle
data = testPuzzle()
print("\nInitial Puzzle: \n")
displayPuzzle(data)

# Generate Needs Array for Puzzle
printDebug("Calling findNeeds(data)")
needs = findNeeds(data)

# Build Change Array and Cell Options from Needs Data
printDebug("Calling findCellOptions(data, needs)")
[options, changes] = findCellOptions(data, needs)

# Resolve outstanding changes while adding new changes from puzzle as they are generated
printDebug("Calling resolveChanges(data, changes, options)")
[data, options] = resolveChanges(data, changes, options)

checkSolved(data)
