def draw(board):
    for y in range(8):
            xline = []
            for x in range(8):
                if board.squares[x][7-y] != None:
                    xline.append(board.squares[x][7-y].color[0].upper()  +  type(board.squares[x][7-y]).__name__[0:3].lower())
                else:
                     xline.append(" N  ")
            print(xline,"\n")