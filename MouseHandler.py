import turtle

screen = turtle.Screen()

"""
Mouse Handler
"""
# don't worry about this, I haven't found anything to use it for
# Honestly this is just a useful tkinter mouse handler.
class MouseHandler:
    # Make  the variables to be referenced
    x, y = 0, 0
    
    def _updatePos(self, event):
        # Get coordinates relative to the window
        eventX, eventY = event.x, event.y
    
        # Convert window coordinates to Turtle coordinates
        # (Subtract half the width/height to center the origin)
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.x = eventX - width / 2
        self.y = height / 2 - eventY
    
    # The constructor allows this to be applied to specific screens 
    def __init__ (self, canvas):
        self.canvas = canvas
        self.canvas.bind("<Motion>", self._updatePos)

def printClick(x,y):
    print("CLICKED",x,y)

def printPos():
    print(mickey.x,mickey.y)
    screen.ontimer(printPos, 100)

mickey = MouseHandler(screen.getcanvas())

screen.onclick(printClick)
printPos()
screen.mainloop()
