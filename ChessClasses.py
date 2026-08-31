'''This is where some classes are stored. Both the board and the pieces themselves should have a copy of their location
TODO: redo format() to make it useful (and be able to input "a1" notation)'''

"""
FYI, it's convention to name classes with a capital letter at the start of each word, like this: "MyClass".
"""

def format(coords: list, form="coordinates") -> list[int]:
    coords = list(coords)
    hasLetters = False
    for i in range(len(coords)):
        if type(coords[i]).__name__ == "str":
            try: coords[i] = int(coords[i])
            except ValueError:
                coords[i] = "abcdefgh".index(coords[i])+1
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
    form = "coordinates"
    return coords

class Position:
    def __init__(self, parent, startSquare, board):
        self.board = board
        self.coordinates = startSquare
        self.parentPiece = parent
    def change(self, newPosition):
        oldPosition = [self.coordinates[0], self.coordinates[1]]
        wasInSquare = self.board.squares[newPosition[0]][newPosition[1]]
        if not(newPosition in self.parentPiece.moves):
            return "Failure not in moves"
        self.coordinates = newPosition
        self.board.squares[oldPosition[0]][oldPosition[1]] = None
        self.board.squares[newPosition[0]][newPosition[1]] = self.parentPiece
        self.board.updateAll()
        for i in self.board.kings:
            if i.is_in_check == True and i.color == self.parentPiece.color:
                self.board.squares[newPosition[0]][newPosition[1]] = wasInSquare
                self.board.squares[oldPosition[0]][oldPosition[1]] = self.parentPiece
                self.coordinates = oldPosition
                self.board.updateAll()
                return "Failure is in check"
        self.parentPiece.hasMoved = True
        self.board.updateAll()
        return "Success"
        # this function should also add scoreboard points to the capturing team

# this is the parent class for pieces
class Piece:
    def __init__(self, color, startSquare, board):
        self.color = color
        self.board = board
        self.hasMoved = False
        self.position = Position(self, startSquare, self.board)
        self.materialPoints = 0
        self.moves = []

class Knight(Piece):
    def __init__(self, color, startSquare, board):
        super().__init__(color, startSquare, board)
        self.materialPoints = 3
        self.board.squares[startSquare[0]][startSquare[1]] = self
        self.board.squares[startSquare[0]][startSquare[1]] = self
    # all pieces need findMoves() to and a moves list. findMoves() will be different for every piece
    def findMoves(self):
        moves = []
        relativeCoords = [2,1]
        currentCoords = self.position.coordinates
        moveAttempt = []
        for _ in range(2):
            for _ in range(2):
                for _ in range(2):
                    moveAttempt = [currentCoords[0] + relativeCoords[0], currentCoords[1] + relativeCoords[1]]
                    if self.board.colorCheck(moveAttempt) != self.color and self.board.colorCheck(moveAttempt) != "Out of bounds":
                        moves.append(moveAttempt)
                    relativeCoords[0] *= -1
                relativeCoords[1] *= -1
            relativeCoords.reverse()
        return moves

class Bishop(Piece):
    def __init__(self, color, startSquare, board):
        super().__init__(color, startSquare, board)
        self.materialPoints = 3
        self.board.squares[startSquare[0]][startSquare[1]] = self
    def findMoves(self):
        moves = []
        relativeCoords = [1,1]
        currentCoords = self.position.coordinates
        moveAttempt = []
        for _ in range(2):
            for i in range(2):
                # invert the direction of move attempts only if we are in the second iteration
                if i == 1:
                    relativeCoords[0] *= -1
                moveAttempt = [currentCoords[0] + relativeCoords[0], currentCoords[1] + relativeCoords[1]]
                while self.board.colorCheck(moveAttempt) != self.color:
                    if self.board.colorCheck(moveAttempt) == "Out of bounds":
                        break
                    # store a copy of moveAttempt in self.moves
                    moves.append(moveAttempt[:])
                    if self.board.colorCheck(moveAttempt) != "Empty":
                        break
                    # change the moveAttempt to the next square
                    moveAttempt[0] += relativeCoords[0]
                    moveAttempt[1] += relativeCoords[1]
            relativeCoords.reverse()
        return moves

class Rook(Piece):
    def __init__(self, color, startSquare, board):
        super().__init__(color, startSquare, board)
        self.materialPoints = 5
        self.board.squares[startSquare[0]][startSquare[1]] = self
    def findMoves(self):
        moves = []
        relativeCoords = [1,0]
        currentCoords = self.position.coordinates
        moveAttempt = []
        for _ in range(2):
            for _ in range(2):
                moveAttempt = [currentCoords[0] + relativeCoords[0], currentCoords[1] + relativeCoords[1]]
                while self.board.colorCheck(moveAttempt) != self.color:
                    if self.board.colorCheck(moveAttempt) == "Out of bounds":
                        break
                    moves.append(moveAttempt[:])
                    if self.board.colorCheck(moveAttempt) != "Empty":
                        break
                    moveAttempt[0] += relativeCoords[0]
                    moveAttempt[1] += relativeCoords[1]
                relativeCoords[0] *= -1
                relativeCoords[1] *= -1
            relativeCoords.reverse()
        return moves

class Queen(Piece):
    def __init__(self, color, startSquare, board):
        super().__init__(color, startSquare, board)
        self.materialPoints = 5
        self.board.squares[startSquare[0]][startSquare[1]] = self
    def findMoves(self):
        moves = Bishop.findMoves(self)
        for i in Rook.findMoves(self):
            moves.append(i)
        return moves

class King(Piece):
    def __init__(self, color, startSquare, board):
        super().__init__(color, startSquare, board)
        self.materialPoints = 1
        self.board.squares[startSquare[0]][startSquare[1]] = self
        self.is_in_check = False
    def findMoves(self):
        moves = []
        currentCoords = self.position.coordinates
        relativeCoords = [1,0]
        for _ in range(2):
            for _ in range(2):
                moveAttempt = [currentCoords[0] + relativeCoords[0], currentCoords[1] + relativeCoords[1]]
                if self.board.colorCheck(moveAttempt) != self.color and self.board.colorCheck(moveAttempt) != "Out of bounds":
                    moves.append(moveAttempt[:])
                moveAttempt[0] += relativeCoords[0]
                moveAttempt[1] += relativeCoords[1]
                relativeCoords[0] *= -1
                relativeCoords[1] *= -1
            relativeCoords.reverse()

        relativeCoords = [1,1]
        for _ in range(2):
            for i in range(2):
                if i == 1:
                    relativeCoords[0] *= -1
                moveAttempt = [currentCoords[0] + relativeCoords[0], currentCoords[1] + relativeCoords[1]]
                if self.board.colorCheck(moveAttempt) != self.color and self.board.colorCheck(moveAttempt) != "Out of bounds":
                    moves.append(moveAttempt[:])
                moveAttempt[0] += relativeCoords[0]
                moveAttempt[1] += relativeCoords[1]
            relativeCoords.reverse()

        return moves

class Pawn(Piece):
    def __init__(self, color, startSquare, board):
        super().__init__(color, startSquare, board)
        self.materialPoints = 1
        self.board.squares[startSquare[0]][startSquare[1]] = self
    def findMoves(self):
        moves = []
        currentCoords = self.position.coordinates

        if self.color == "white":
            moveAttempt = [currentCoords[0], currentCoords[1]+1]
        else:
            moveAttempt = [currentCoords[0], currentCoords[1]-1]
        # check forward squares
        if self.board.colorCheck(moveAttempt) == "Empty" and self.board.colorCheck(moveAttempt) != "Out of bounds":
            moves.append(moveAttempt[:])

            if self.color == "white":
                moveAttempt = [currentCoords[0], currentCoords[1]+2]
            else:moveAttempt = [currentCoords[0], currentCoords[1]-2]
            if self.board.colorCheck(moveAttempt) == "Empty" and self.hasMoved == False and self.board.colorCheck(moveAttempt) != "Out of bounds":
                moves.append(moveAttempt[:])


        if self.color == "white":
            moveAttempt[1] = currentCoords[1]+1
        else:
            moveAttempt[1] = currentCoords[1]-1
        # check diagonal squares
        moveAttempt[0] = currentCoords[0]+1
        if self.board.colorCheck(moveAttempt) != "Empty" and self.board.colorCheck(moveAttempt) != self.color and self.board.colorCheck(moveAttempt) != "Out of bounds":
            moves.append(moveAttempt[:])

        moveAttempt[0] = currentCoords[0]-1
        if self.board.colorCheck(moveAttempt) != "Empty" and self.board.colorCheck(moveAttempt) != self.color and self.board.colorCheck(moveAttempt) != "Out of Bounds":
            moves.append(moveAttempt[:])
        
        return moves
        

class Board:
    def __init__(self):
        self.squares = []
        for i in range(8):
            self.squares.append([])
            for o in range(8):
                self.squares[i].append(None)
        self.kings = []
    def updateAll(self):
        self.kings = []
        for column in range(len(self.squares)):
            for square in self.squares[column]:
                if square != None:
                    square.moves = square.findMoves()
                    if type(square).__name__ == "King":
                        self.kings.append(square)

        for king in self.kings:
            king.is_in_check = False

        for column in range(len(self.squares)):
            for square in self.squares[column]:
                if square != None:
                    for king in self.kings:
                        if king.position.coordinates in square.moves:
                            if king.color != square.color:
                                king.is_in_check =True
    def colorCheck(self, target):
        for i in target:
            if not(str(i) in "01234567"):
                return "Out of bounds"
        if self.squares[target[0]][target[1]] == None:
            return "Empty"
        else:
            return self.squares[target[0]][target[1]].color
    def typeCheck(self, target):
        for i in target:
            if not(str(i) in "01234567"):
                return "Out of bounds"
        if self.squares[target[0]][target[1]] != None:
            return type(self.squares[target[0]][target[1]]).__name__
        else:
            return "Empty"

    def boardSetup(self):
        self.__init__()
        # setup white
        for i in range(8):
            Pawn("white", [i,1], self)
        Rook("white", [0,0], self)
        Knight("white", [1,0], self)
        Bishop("white", [2,0], self)
        Queen("white", [3,0], self)
        King("white", [4,0], self)
        Bishop("white", [5,0], self)
        Knight("white", [6,0], self)
        Rook("white", [7,0], self)

        # setup black
        for i in range(8):
            Pawn("black", [i,6], self)
        Rook("black", [0,7], self)
        Knight("black", [1,7], self)
        Bishop("black", [2,7], self)
        Queen("black", [3,7], self)
        King("black", [4,7], self)
        Bishop("black", [5,7], self)
        Knight("black", [6,7], self)
        Rook("black", [7,7], self)
        self.updateAll()
