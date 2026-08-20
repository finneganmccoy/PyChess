from RendererBase import RendererBase

class TestRenderer(RendererBase):
    def __init__(self):
        super().__init__()

    def drawWhitePieces(self, board):
        # Implementation for drawing white pieces
        # comment to Micheal: this would have to print board.squares to achieve the affect your are looking for here
        print(board)

    def drawBlackPieces(self, board):
        # Implementation for drawing black pieces
        pass