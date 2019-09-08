from src.board import Board
from src.chess_pieces import *
import pygame

PIECEDIR = 'src/Pieces/'
IMAGES = {
    Pawn: "p",
    Rook: "r",
    Bishop: "b",
    Knight: "n",
    Queen: "q",
    King: "k"
}


class ChessGame:
    def __init__ (self, window, width, height, checkersize):
        self.window = window
        self.width = width
        self.height =  height
        self.checkersize = checkersize
        self.board = Board()
    
    def redrawWindow(self):
        self.draw_checkerboard()
        self.draw_pieces()
        
    def draw_checkerboard(self):
        for row, y in zip (self.board.game_board, range (0, self.height, self.height // 8)):
            for square, x in zip (row, range (0, self.width, self.width // 8)):
                square.coords = (x,y)  # Important to know where to blit the images to
                self.draw_chessrect((x,y), square.color)

    def draw_chessrect(self, coords: tuple, color: tuple):
        pygame.draw.rect(self.window, color, (coords, self.checkersize))
    
    def draw_pieces(self):
        blitsequence = []
        for row in self.board.game_board:
            for square in row:
                imgtuples = self.get_imgtuples(square)
                if imgtuples is not None: blitsequence.append(imgtuples)
        self.window.blits(tuple(blitsequence))
                
    def get_imgtuples(self, square):
        if type(square.piece) is NonePiece: return

        pimage = self.get_image_surf(square.piece)
        coords = (square.coords [0] + 6.25, square.coords [1] + 6.25)
        size = (self.checkersize [0] - 14, self.checkersize [1] - 14)
        pimage = pygame.transform.scale(pimage, size)
        return pimage, coords
        
    def get_image_surf(self, piece):
        letter = IMAGES [type (piece)]
        color = "white" if piece.color == WHITE else "black"
        return pygame.image.load(f'{PIECEDIR}{color}_{letter}.png')
    
        
class Button:
    def __init__ (self, colors, x, y, width, height, text='', toggle=False):
        # colors is tuple consisting of a initial rgb tuple, and a mouseover rgb tuple which is the toggle tuple if toggle is True
        self.colors = colors
        # The color the Button is currently drawn in
        self.color = colors[0]
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        # If the button can be toggled, and the current toggle state
        self.toggle = toggle
        self.toggled = False
    
    def draw(self, win, outline = None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
    
    def check(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over(pos):
                if self.toggle:
                    if self.toggled:
                        self.color = self.colors[0]
                        self.toggled = False
                    else:
                        self.color = self.colors[1]
                        self.toggled = True
                    return self.toggled
                else:
                    return True

        if event.type == pygame.MOUSEMOTION:
            if not self.toggle:
                if self.is_over(pos):
                    self.color = self.colors[1]
                else:
                    self.color = self.colors[0]

