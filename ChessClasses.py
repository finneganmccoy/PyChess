'''This is where some classes are stored. Both the board and the pieces themselves should have a copy of their location
TODO: Create more pieces'''

def format(coords, form="coordinates"):
    # The following lines just format the input into coordinate form. Feel free to change the structure; this may not be optimal
    coords = list(coords)
    coords[0],coords[1] = str(coords[0]), str(coords[1])
    if len(coords) == 2:
        for i in range(len(coords)):
            try:
                if int(coords[i]) <= 7 and int(coords[i]) >= 0:
                    pass
                else: raise Exception("No inputs outside of 01234567")
            except ValueError:
                if coords[i] in "abcdefgh":
                    coords = list(str("abcdefgh".index(coords[i])) + coords[1-i])
                else: raise Exception("No inputs outside of abcdefgh")
    else: raise Exception("Input must be 2 characters")

    coords[0] = int(coords[0])
    coords[1] = int(coords[1])
    if form=="-1":
        coords[0] -= 1
        coords[1] -= 1
    elif form=="+1":
        coords[0] += 1
        coords[1] += 1
    return coords

class position:
    def __init__(self):
        self.notation = None
        self.coordinates = None
    def change(self, newPosition):
        newPosition = format(newPosition)
        bobject.squares[newPosition[0]][newPosition[1]] = bobject.squares[self.coordinates[0]][self.coordinates[1]]
        bobject.squares[self.coordinates[0]][self.coordinates[1]] = None
        self.coordinates = newPosition
        self.notation = "abcdefgh"[self.coordinates[0]] + str(self.coordinates[1]+1)
        '''
        if bobject.squares[newPosition[0]][newPosition[1]].color != self.color:
            scoreboard.add(bobject.squares[newPosition[0]][newPosition[0]].materialPoints, self.color)
        '''

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
        bobject.squares[startSquare[0]][startSquare[0]] = self
    def findMoves(self):
        self.moves = []
        relativeCoords = [2,1]
        currentCoords = self.position.coordinates
        moveAttempt = []
        for i in range(2):
            for i in range(2):
                for i in range(2):
                    moveAttempt = [currentCoords[0] + relativeCoords[0], currentCoords[1] + relativeCoords[1]]
                    if bobject.occupationCheck(moveAttempt) != self.color and bobject.occupationCheck(moveAttempt) != "Out of bounds":
                        self.moves.append(moveAttempt)
                    relativeCoords[0] *= -1
                relativeCoords[1] *= -1
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
            if str(e) == ("No inputs outside of abcdefgh"):
                return "Out of bounds"
        if self.squares[target[0]][target[1]] == None:
            return "Empty"
        else:
            return self.squares[target[0]][target[1]].color

bobject = board()

kn = knight("white", [1,1])
print(kn.position.coordinates, kn.position.notation,"\n")
print(bobject.squares, "\n")
kn.position.change([2,4])

print(kn.position.coordinates, kn.position.notation, "\n")
print(bobject.squares,"\n")

kn.findMoves()
print(kn.moves)
