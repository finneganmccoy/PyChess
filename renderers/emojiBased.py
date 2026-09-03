import os
emojis = {
    "Bking": "♔",
    "Wking": "♚",
    "Bqueen": "♕",
    "Wqueen": "♛",
    "Bknight": "♘",
    "Wknight": "♞",
    "Bbishop": "♗",
    "Wbishop": "♝",
    "Brook": "♖",
    "Wrook": "♜",
    "Bpawn": "♙",
    "Wpawn": "♟",
}

def draw(board, orientation="white"):
    # this line clears terminal
    # not sure why vscode says its deprecated
    # you can change it if you want
    os.system("cls" if os.name == "nt" else "clear")
    for y in range(8):
            if orientation == "black": y = 7-y #this line is all that is required to flip board. very happy with it
            xline = []
            for x in range(8):
                if board.squares[x][7-y] != None:
                    xline.append(board.squares[x][7-y].color[0].upper()  +  type(board.squares[x][7-y]).__name__.lower())
                else:
                    xline.append("None")
            for i in range(len(xline)):
                if xline[i] != "None":
                    xline[i] = emojis[xline[i]]
                else:
                    xline[i] = " "
            print(8-y, xline, '\n')
    xline = ""
    for i in "abcdefgh":
         xline = xline+ "    " + i
    print(xline)
    for i in ["white","black"]:
        print(f"Score {i}:", board.scores[i])