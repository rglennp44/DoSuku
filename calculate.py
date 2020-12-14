from userInterface import printDebug, puzzleDisplayStep


# Tracking Stat Variables
trackingSquaresSolved = 0


def checkSolved(data):
    for y in range(9):
        for x in range(9):
            if data[x][y] == None:
                print(
                    f"Puzzle Failed to complete. Please verify that puzzle is solvable.")
                return(False)
    print(
        f"\nSolved {trackingSquaresSolved} Squares in TODO Seconds, \nPuzzle Complete!!!")
    print("To Do: Build Verification that puzzle results fit the requirements of a solved sudoku")
    return(True)


def updateData(data, changeBuffer):
    for change in range(len(changeBuffer)):
        row = changeBuffer[change][0]
        col = changeBuffer[change][1]
        val = changeBuffer[change][2]
        data[col][row] = val
    return(data)


# data format data[col][row]
# changeBuffer format: [row, col, value]
def updateNeeds(changeBuffer, rowNeeds, colNeeds, boxNeeds):
    while len(changeBuffer) != 0:
        # Collect Data from Change Buffer
        row = changeBuffer[0][0]
        col = changeBuffer[0][1]
        box = whichBox(row, col)-1
        val = changeBuffer[0][2]
        # Update Row Needs
        try:
            printDebug(f"Needs for Row {row}: {rowNeeds[row]}")
            rowNeeds[row].remove(val)
            if len(rowNeeds[row]) == 1:
                print("TEST INSTANCE ROW")
            printDebug(f"Removed {val} from row {row+1}")
            printDebug(f"Needs for Row {row}: {rowNeeds[row]}")
        except:
            print(
                f"Error: Tried to remove {val} from Row {row+1} needs index, but the value was already absent")

        # Update Col Needs
        try:
            printDebug(f"Needs for Col {col}: {colNeeds[col]}")
            colNeeds[col].remove(val)
            if len(colNeeds[col]) == 1:
                print("TEST INSTANCE COL")
            printDebug(f"Removed {val} from col {col+1}")
            printDebug(f"Needs for Col {col}: {colNeeds[col]}")
        except:
            print(
                f"Error: Tried to remove {val} from col {col+1} needs index, but the value was already absent")

        # Update Box Needs
        try:
            printDebug(f"Needs for Box {box}: {boxNeeds[box]}")
            boxNeeds[box].remove(val)
            if len(boxNeeds[box]) == 1:
                print("TEST INSTANCE BOX")
            printDebug(f"Removed {val} from box {box+1}")
            printDebug(f"Needs for Box {box}: {boxNeeds[box]}")
        except:
            print(
                f"Error: Tried to remove {val} from box {box} needs index, but the value was already absent")

        # Remove Entry from Change Array
        printDebug(f"Removing {changeBuffer[0]} from Changes Array")
        del changeBuffer[0]
    return(rowNeeds, colNeeds, boxNeeds)


# TO DO: CREATE NEEDS CLASS TO STORE DATA IN MORE READABLE FORMAT
# Find Puzzle Needs
# Takes Puzzle Data
# Returns Set Needs Array
def findNeeds(data):
    printDebug("Call Received by findNeeds()\n")
    # Declare Needs Array
    needs = [[[1, 2, 3, 4, 5, 6, 7, 8, 9]
              for x in range(9)] for y in range(3)]

    # Find Row Needs
    for row in range(9):
        printDebug(f"Scanning Row {row + 1} Needs")
        for col in range(9):
            printDebug(f"({col+1},{row+1}) = {data[col][row]}")
            if data[col][row] != None:
                needs[0][row].remove(data[col][row])
                printDebug(
                    f"Removing Value {data[col][row]} from Row {row + 1} Needs")
        printDebug(f"Row {row+1} Needs: {needs[0][row]} \n")

    # Find Column Needs
    for col in range(9):
        printDebug(f"Scanning Col {col + 1} Needs")
        for row in range(9):
            printDebug(f"({col+1},{row+1}) = {data[col][row]}")
            if data[col][row] != None:
                needs[1][col].remove(data[col][row])
                printDebug(
                    f"Removing Value {data[col][row]} from Col {col + 1} Needs")
        printDebug(f"Col {col+1} Needs: {needs[1][col]} \n")

    # Find Box Needs
    for box in range(9):
        printDebug(f"Scanning Box {box + 1} Needs")
        xOffset = (box % 3) * 3
        yOffset = (box // 3) * 3
        for y in range(3):
            for x in range(3):
                printDebug(
                    f"({x + xOffset + 1},{y + yOffset + 1}) = {data[x + xOffset][y + yOffset]}")
                if data[x + xOffset][y + yOffset] != None:
                    needs[2][box].remove(data[x + xOffset][y + yOffset])
                    printDebug(
                        f"Removing Value {data[x + xOffset][y + yOffset]} from Box {box + 1} Needs")
        printDebug(f"Box {box+1} Needs: {needs[2][box]} \n")

    printDebug(f"Returning Needs Array")
    return needs


# Build Change and Option Arrays from Needs Data
def findCellOptions(data, needs):
    printDebug("Generating Cell Options Based on Needs Array Data\n")
    options = [[[] for x in range(9)] for y in range(9)]
    changes = []
    for row in range(9):
        for col in range(9):
            if data[col][row] != None:
                continue
            box = whichBox(row, col)
            for val in range(1, 10):
                if val in needs[0][row] and val in needs[1][col] and val in needs[2][box]:
                    options[col][row].append(val)
                    # printDebug(
                    #     f"Adding {val} to Options for ({col + 1},{row + 1})")
            printDebug(
                f"Options for ({col +1},{row + 1}): {options[col][row]}")
            # If only 1 solution is possible for a given cell, append a solution to the changes array
            # Format [col, row, val]
            if len(options[col][row]) == 1:
                changes.append([col, row, options[col][row][0]])
                print(
                    f"Solution found at ({col + 1},{row + 1}) during initial scan: Inserting {options[col][row][0]} into Change Array")

    printDebug(f"\nReturning Change Array: {changes}")
    return options, changes


# Resolves Changes, updating Data and Needs Arrays
def resolveChanges(data, changes, options):
    while len(changes) != 0:
        col = changes[0][0]
        row = changes[0][1]
        val = changes[0][2]
        box = whichBox(row, col)
        global trackingSquaresSolved

        # Update Data Array with Solved Value
        data[col][row] = val
        printDebug(
            f"Inserted {val} at ({col + 1},{row + 1})")
        trackingSquaresSolved += 1
        puzzleDisplayStep(data)

        # Update Needs Array and add new changes as they are discovered
        # Row Needs:
        for x in range(9):
            if val in options[x][row]:
                options[x][row].remove(val)
                if len(options[x][row]) == 1 and data[x][row] == None:
                    changes.append([x, row, options[x][row][0]])
                    print(
                        f"Solution discovered in Row {row + 1}: adding {options[x][row][0]} to change array")
        # Column Needs:
        for y in range(9):
            if val in options[col][y]:
                options[col][y].remove(val)
                if len(options[col][y]) == 1 and data[col][y] == None:
                    changes.append([col, y, options[col][y][0]])
                    print(
                        f"Solution discovered in Col {col + 1}: adding {options[col][y][0]} to change array")
        # Box Needs:
        xOffset = (box % 3) * 3
        yOffset = (box // 3) * 3
        for x in range(3):
            for y in range(3):
                if val in options[x + xOffset][y + yOffset]:
                    options[x + xOffset][y + yOffset].remove(val)
                    if len(options[x + xOffset][y + yOffset]) == 1 and data[x + xOffset][y + yOffset] == None:
                        changes.append(
                            [x + xOffset, y + yOffset, options[x + xOffset][y + yOffset][0]])
                        print(
                            f"Solution discovered in Box {box + 1}: adding {options[x + xOffset][y + yOffset][0]} to change array")
        del changes[0]
    return data, options


# Returns 0-8 Value
def whichBox(row, col):
    box = -1
    if row < 3:
        if col < 3:
            box = 0
        elif 3 <= col < 6:
            box = 1
        elif 6 <= col:
            box = 2
    elif 3 <= row < 6:
        if col < 3:
            box = 3
        elif 3 <= col < 6:
            box = 4
        elif 6 <= col:
            box = 5
    elif 6 <= row:
        if col < 3:
            box = 6
        elif 3 <= col < 6:
            box = 7
        elif 6 <= col:
            box = 8
    if box == -1:
        print("Error: whichBox Function in DoSuku.py failed")
    # printDebug(f"({col + 1},{row + 1}) is in Box {box + 1}")
    return box
