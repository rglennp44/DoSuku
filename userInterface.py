import time


animatePuzzle = True
debug = True


def printDebug(message):
    if debug:
        print(message)


def displayPuzzle(data):
    # Print Top Line
    print("\n")
    print("+", end="")
    for i in range(9):
        print("---+", end="")
    print("")
    # Print Puzzle
    for y in range(len(data)):
        print("|", end="")
        for x in range(len(data)):
            symbol = "[" if x == 2 or x == 5 else "|"
            if data[x][y] == None:
                print("  ", end=f" {symbol}")
            else:
                print(f" {data[x][y]}", end=f" {symbol}")

        print("")
        # Determine whether to print a thin line or thick one
        if y == 2 or y == 5:
            print("#", end="")
            for x in range(9):
                print("===+", end="")
        else:
            print("+", end="")
            for x in range(9):
                print("---+", end="")
        print("")
    print("\n")


def puzzleDisplayStep(data):
    if animatePuzzle:
        displayPuzzle(data)
        time.sleep(.1)
