import pygame as pg
from pygame.locals import *
import sys
import chess
import chess.svg
import io

from Board import Board

# Initialize pygame
pg.init()

# Constants
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE_COLOR = (240, 217, 181)
DARK_SQUARE_COLOR = (181, 136, 99)

# Images
img_dict = {
    "w_Rook": pg.image.load('icons/white-rook.png'),
    "w_Knight": pg.image.load('icons/white-knight.png'),
    "w_Bishop": pg.image.load('icons/white-bishop.png'),
    "w_Queen": pg.image.load('icons/white-queen.png'),
    "w_King": pg.image.load('icons/white-king.png'),
    "w_Pawn": pg.image.load('icons/white-pawn.png'),
    "b_Rook": pg.image.load('icons/black-rook.png'),
    "b_Knight": pg.image.load('icons/black-knight.png'),
    "b_Bishop": pg.image.load('icons/black-bishop.png'),
    "b_Queen": pg.image.load('icons/black-queen.png'),
    "b_King": pg.image.load('icons/black-king.png'),
    "b_Pawn": pg.image.load('icons/black-pawn.png'),
}

# Create the display window
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Chess Board')

# Function to draw the chessboard
def draw_board(board):
    colors = [LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR]
    for i in range(8):
        for j in range(8):
            color = colors[(i + j) % 2]
            pg.draw.rect(screen, color, (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board.board[i][j].piece
            piece_image = None
            if piece is not None:
                piece_name = f"{piece.color[0]}_{type(piece).__name__}"
                piece_image = pg.transform.smoothscale(img_dict[piece_name], (SQUARE_SIZE, SQUARE_SIZE))
            if piece_image is not None and type(piece).__name__ == "Pawn":
                screen.blit(piece_image, (j * SQUARE_SIZE - 2, i * SQUARE_SIZE))
            elif piece_image is not None and type(piece).__name__ != "Pawn":
                screen.blit(piece_image, (j * SQUARE_SIZE, i * SQUARE_SIZE))

def main():
    # Main loop
    board = Board()
    running = True
    selected = ()
    clicks = [] # Will contain both of the user's clicks

    while running:
        for event in pg.event.get():
            # User exits the game
            if event.type == QUIT:
                running = False
            
            # User clicks
            elif event.type == MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE

                # The same square was clicked twice in a row
                if (row, col) == selected:
                    selected = () # Deselect the square
                    clicks = []
                elif (selected == () and board.board[row][col].piece is not None) or selected != ():
                    selected = (row, col)
                    clicks.append(selected)

                # We attempt to move to the newly selected square
                if len(clicks) == 2:
                    prevRow, prevCol = clicks[0]
                    newRow, newCol = clicks[1]
                    board.board[prevRow][prevCol].piece.move(newRow, newCol)
                    selected = ()
                    clicks = []

        screen.fill(WHITE)  # Fill the background with white
        draw_board(board)  # Draw the chessboard
        
        pg.display.flip()

main()

# Quit pygame
pg.quit()


# board = Board()

'''
board.board[6][4].piece.move(4, 4) # e4
board.board[1][2].piece.move(3, 2) # c5
board.board[4][4].piece.move(3, 4) # e5
board.board[1][3].piece.move(2, 3) # d6
board.board[3][4].piece.move(2, 3) # exd6
board.board[0][1].piece.move(2, 2) # Nc6
board.board[6][3].piece.move(4, 3) # d4
board.board[2][2].piece.move(4, 3) # Nxd4
board.board[7][4].piece.move(6, 3) # Kd2
board.board[0][2].piece.move(3, 5) # Bf5
board.board[7][5].piece.move(2, 0) # Ba6
board.board[0][0].piece.move(0, 2) # Rc8
board.board[7][3].piece.move(3, 7) # Qh5
board.board[1][5].piece.move(2, 5) # f6 (Illegal move)
board.board[1][7].piece.move(2, 7) # h6
board.board[3][7].piece.move(1, 5) # Qxf7+
board.board[0][4].piece.move(1, 3) # Kd7
board.board[1][5].piece.move(3, 5) # Qxf5+
board.board[4][3].piece.move(3, 5) # Nxf5
'''

'''
board.board[6][5].piece.move(4, 5) # f4
board.board[1][4].piece.move(3, 4) # e5
board.board[6][6].piece.move(4, 6) # g4
board.board[0][3].piece.move(4, 7) # Qh4#
'''

'''
board.board[6][4].piece.move(4, 4) # e4
board.board[1][3].piece.move(3, 3) # d5
board.board[7][5].piece.move(2, 0) # Ba6
board.board[0][1].piece.move(2, 0) # Nxa6
board.board[7][6].piece.move(5, 5) # Nf3
board.board[0][2].piece.move(4, 6) # Bg4
board.board[7][4].piece.move(7, 6) # 0-0
board.board[0][3].piece.move(2, 3) # Qd6
board.board[7][5].piece.move(7, 4) # Re1
board.board[0][4].piece.move(0, 2) # 0-0-0
'''

'''
board.board[6][4].piece.move(5, 4) # e3
board.board[1][0].piece.move(3, 0) # a5
board.board[7][3].piece.move(3, 7) # Qh5
board.board[0][0].piece.move(2, 0) # Ra6
board.board[3][7].piece.move(3, 0) # Qxa5
board.board[1][7].piece.move(3, 7) # h5
board.board[6][7].piece.move(4, 7) # h4
board.board[2][0].piece.move(2, 7) # Rah6
board.board[3][0].piece.move(1, 2) # Qxc7
board.board[1][5].piece.move(2, 5) # f6
board.board[1][2].piece.move(1, 3) # Qxd7+
board.board[0][4].piece.move(1, 5) # Kf7
board.board[1][3].piece.move(1, 1) # Qxb7
board.board[0][3].piece.move(5, 3) # Qd3
board.board[1][1].piece.move(0, 1) # Qxb8
board.board[5][3].piece.move(1, 7) # Qh7
board.board[0][1].piece.move(0, 2) # Qxc8
board.board[1][5].piece.move(2, 6) # Kg6
board.board[0][2].piece.move(2, 4) # Qe6
'''

'''
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
board.board[5][2].piece.move(7, 1) # Nb1
board.board[2][2].piece.move(0, 1) # Nb8
board.board[7][1].piece.move(5, 2) # Nc3
board.board[0][1].piece.move(2, 2) # Nc6
'''

# board.printBoard()