'''This is where some classes are stored. Both the board and the pieces themselves should have a copy of their location
TODO: Create more pieces'''

def format(coords, form="coordinates"):
    coords = list(coords)
    coords[0],coords[1] = str(coords[0]), str(coords[1])
    if len(coords) == 2:
        for i in range(len(coords)):
            if int(coords[i]) <= 7 and int(coords[i]) >= 0:
                pass
            else: raise Exception("No inputs outside of 01234567")
    else: raise Exception("Input must be 2 characters")

    coords[0] = int(coords[0])
    coords[1] = int(coords[1])
    # optional second parameter allows you to make the output have +1 or -1 coordinates. Might be useful somewhere.
    if form=="-1":
        coords[0] -= 1
        coords[1] -= 1
    elif form=="+1":
        coords[0] += 1
        coords[1] += 1
    elif form=="notation":
        coords[0] = "abcdefgh"[coords[0]]
        coords[1] += 1
    return coords

class position:
    def __init__(self):
        self.notation = None
        self.coordinates = None
    def change(self, newPosition):
        newPosition = format(newPosition)
        bobject.squares[newPosition[0]][newPosition[1]] = self
        bobject.squares[self.coordinates[0]][self.coordinates[1]] = None
        self.coordinates = newPosition
        self.notation = "abcdefgh"[self.coordinates[0]] + str(self.coordinates[1]+1)
        # this function should also add scoreboard points to the capturing team

# this is the parent class for pieces
class piece:
    def __init__(self, color, startSquare):
        self.color = color
        self.position = position()
        self.position.coordinates = format(startSquare)
        self.materialPoints = 0
        self.moves = []


class knight(piece):
    def __init__(self, color, startSquare):
        super().__init__(color, startSquare)
        self.materialPoints = 3
        bobject.squares[startSquare[0]][startSquare[1]] = self
    # all pieces need findMoves() to and a moves list. findMoves() will be different for every piece
    def findMoves(self):
        self.moves = []
        relativeCoords = [2,1]
        currentCoords = self.position.coordinates
        moveAttempt = []
        for _ in range(2):
            for _ in range(2):
                for _ in range(2):
                    moveAttempt = [currentCoords[0] + relativeCoords[0], currentCoords[1] + relativeCoords[1]]
                    if bobject.occupationCheck(moveAttempt) != self.color and bobject.occupationCheck(moveAttempt) != "Out of bounds":
                        self.moves.append(moveAttempt)
                    relativeCoords[0] *= -1
                relativeCoords[1] *= -1
            relativeCoords.reverse()

class bishop(piece):
    def __init__(self, color, startSquare):
        super().__init__(color, startSquare)
        self.materialPoints = 3
        bobject.squares[startSquare[0]][startSquare[1]] = self
    def findMoves(self):
        self.moves = []
        relativeCoords = [1,1]
        currentCoords = self.position.coordinates
        moveAttempt = []
        for _ in range(2):
            for i in range(2):
                # invert the direction of move attempts only if we are in the right part of the cycle
                if i == 1:
                    relativeCoords[0] *= -1
                moveAttempt = [currentCoords[0] + relativeCoords[0], currentCoords[1] + relativeCoords[1]]
                while bobject.occupationCheck(moveAttempt) != self.color:
                    if bobject.occupationCheck(moveAttempt) == "Out of bounds":
                        break
                    # store a copy of moveAttempt in self.moves
                    self.moves.append(moveAttempt[:])
                    if bobject.occupationCheck(moveAttempt) != "Empty":
                        break
                    # change the moveAttempt to the next square
                    moveAttempt[0] += relativeCoords[0]
                    moveAttempt[1] += relativeCoords[1]
            relativeCoords.reverse()

class board:
    def __init__(self):
        self.squares = []
        for i in range(8):
            self.squares.append([])
            for o in range(8):
                self.squares[i].append(None)
    def occupationCheck(self, target):
        try:
            target = format(target)
        except Exception as e:
            if str(e) == ("No inputs outside of 01234567"):
                return "Out of bounds"
        if self.squares[target[0]][target[1]] == None:
            return "Empty"
        else:
            return self.squares[target[0]][target[1]].color

# I have referenced the board object as "bobject" everywhere in the code. If the name needs to change, the references should also change
bobject = board()
bis = bishop("white", [5, 6])
kn = knight("white", [4,4])
k2 = knight("black", [2,3])

print(format(bis.position.coordinates, "notation"),"\n")
bis.findMoves()
for i in bis.moves:
    print(format(i, "notation"))
print("\n\n")
kn.findMoves()
for i in kn.moves:
    print(format(i, "notation"))