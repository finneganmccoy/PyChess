
class RendererBase:

    def __init__(self):
        pass

    def drawWhitePieces(self, board):
        raise NotImplementedError("Subclasses should implement this method.")

    def drawBlackPieces(self, board):
        raise NotImplementedError("Subclasses should implement this method.")