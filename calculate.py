from userInterface import printDebug


def checkSolved(data):
    for y in range(9):
        for x in range(9):
            if data[x][y] == None:
                return(False)
    return(True)


# index = Column # 1-9
def findColNeeds(data, index):
    needs = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for y in range(9):
        if data[index][y] != None:
            needs.remove(data[index][y])
        printDebug(f"Column {index+1} Needs: {needs}")
    return(needs)


# index = Row # 1-9
def findRowNeeds(data, index):
    needs = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for x in range(9):
        if data[x][index] != None:
            needs.remove(data[x][index])
    printDebug(f"Row {index+1} Needs: {needs}")
    return(needs)


# index = Box # 1-9
def findBoxNeeds(data, index):
    needs = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    yOffset = (index // 3) * 3
    xOffset = (index % 3) * 3

    # if debug():
    #     print(f"X Offset: {xOffset}")
    #     print(f"Y Offset: {yOffset}")

    for x in range(3):
        for y in range(3):
            if data[x+xOffset][y+yOffset] != None:
                needs.remove(data[x+xOffset][y+yOffset])
    printDebug(f"Box {index+1} Needs: {needs}")
    return(needs)


def findCellOptions(rowNeeds, colNeeds, boxNeeds):
    options = []
    for val in range(1, 10):
        if val in rowNeeds and val in colNeeds and val in boxNeeds:
            options.append(val)
    return options


def findSingleOptions(data, rowNeeds, colNeeds, boxNeeds, cellOptions):
    changeBuffer = []
    for row in range(9):
        for col in range(9):
            if data[col][row] == None:
                box = whichBox(row, col)
                index = 9 * row + col
                printDebug(f"({row+1},{col+1}), Box: {box}")
                options = findCellOptions(
                    rowNeeds[row], colNeeds[col], boxNeeds[box-1])
                printDebug(f"Cell Options for ({row+1},{col+1}): {options}")
                if len(options) == 1:
                    print(
                        f"Discovered Solution {options[0]} at ({row+1}, {col+1})\n")
                    changeBuffer.append([row, col, options[0]])
                printDebug(f"inserting {options} into index: {index}")
                cellOptions[index] = options
    printDebug(f"Cell Options Array Length: {len(cellOptions)}\n")
    printDebug(f"Cell Options Array: {cellOptions}\n")
    printDebug(f"Change Buffer Array Length: {len(changeBuffer)}\n")
    printDebug(f"Change Buffer Array: {changeBuffer}\n")
    return cellOptions, changeBuffer


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
        changeBuffer.remove(changeBuffer[0])
    return(rowNeeds, colNeeds, boxNeeds)


def whichBox(row, col):
    box = 0
    if row < 3:
        if col < 3:
            box = 1
        elif 3 <= col < 6:
            box = 2
        elif 6 <= col:
            box = 3
    elif 3 <= row < 6:
        if col < 3:
            box = 4
        elif 3 <= col < 6:
            box = 5
        elif 6 <= col:
            box = 6
    elif 6 <= row:
        if col < 3:
            box = 7
        elif 3 <= col < 6:
            box = 8
        elif 6 <= col:
            box = 9
    if box == 0:
        print("Error: whichBox Function in DoSuku.py failed")
    return box
