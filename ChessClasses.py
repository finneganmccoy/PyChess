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
    def __init__(self, parent):
        self.coordinates = None
        self.parentPiece = parent
    def change(self, newPosition):
        newPosition = format(newPosition)
        bobject.squares[self.coordinates[0]][self.coordinates[1]] = None
        bobject.squares[newPosition[0]][newPosition[1]] = self.parentPiece
        self.coordinates = newPosition
        # considering taking the following line out because of the existence of the updateAll() function
        self.parentPiece.findMoves()
        # this function should also add scoreboard points to the capturing team

# this is the parent class for pieces
class piece:
    def __init__(self, color, startSquare):
        self.color = color
        self.position = position(self)
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
                # invert the direction of move attempts only if we are in the second iteration
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

class rook(piece):
    def __init__(self, color, startSquare):
        super().__init__(color, startSquare)
        self.materialPoints = 5
        bobject.squares[startSquare[0]][startSquare[1]] = self
    def findMoves(self):
        self.moves = []
        relativeCoords = [1,0]
        currentCoords = self.position.coordinates
        moveAttempt = []
        for _ in range(2):
            for _ in range(2):
                moveAttempt = [currentCoords[0] + relativeCoords[0], currentCoords[1] + relativeCoords[1]]
                while bobject.occupationCheck(moveAttempt) != self.color:
                    if bobject.occupationCheck(moveAttempt) == "Out of bounds":
                        break
                    self.moves.append(moveAttempt[:])
                    if bobject.occupationCheck(moveAttempt) != "Empty":
                        break
                    moveAttempt[0] += relativeCoords[0]
                    moveAttempt[1] += relativeCoords[1]
                relativeCoords[0] *= -1
                relativeCoords[1] *= -1
            relativeCoords.reverse()

class queen(piece):
    def __init__(self, color, startSquare):
        super().__init__(color, startSquare)
        self.materialPoints = 5
        bobject.squares[startSquare[0]][startSquare[1]] = self
    def findMoves(self):
        self.moves = []
        relativeCoords = [1,0]
        currentCoords = self.position.coordinates
        moveAttempt = []
        for _ in range(2):
            for _ in range(2):
                moveAttempt = [currentCoords[0] + relativeCoords[0], currentCoords[1] + relativeCoords[1]]
                while bobject.occupationCheck(moveAttempt) != self.color:
                    if bobject.occupationCheck(moveAttempt) == "Out of bounds":
                        break
                    self.moves.append(moveAttempt[:])
                    if bobject.occupationCheck(moveAttempt) != "Empty":
                        break
                    moveAttempt[0] += relativeCoords[0]
                    moveAttempt[1] += relativeCoords[1]
                relativeCoords[0] *= -1
                relativeCoords[1] *= -1
            relativeCoords.reverse()

        # Bishop style move check. I used ctrl+c ctrl+v. Should it be a function? I dont know that it needs to be
        relativeCoords = [1,1]
        for _ in range(2):
            for i in range(2):
                # invert the direction of move attempts only if we are in the second iteration
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
    def updateAll(self):
        for i in range(len(self.squares)):
            for o in self.squares[i]:
                if o != None:
                    o.findMoves()

# I have referenced the board object as "bobject" everywhere in the code. If the name needs to change, the references should also change
bobject = board()

queen("white", [3,4])
knight("black", [1,2])
queen("black", [6, 4])
bishop("white", [3,7])
bobject.updateAll()

for move in bobject.squares[3][4].moves:
    print(format(move, "notation"))
print(len(bobject.squares[3][4].moves))
for move in bobject.squares[1][2].moves:
    print(format(move, "notation"))
print(len(bobject.squares[1][2].moves))