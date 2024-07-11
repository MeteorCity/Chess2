# import pygame
from Board import Board

'''
pygame.init()

# Set up the display
width, height = 800, 800
square_size = width // 8
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")

# Load piece images
piece_images = {}
def load_images():
    pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['white', 'black']
    for piece in pieces:
        for color in colors:
            image_path = f'icons/{color}-{piece}.svg'
            piece_images[f'{color}-{piece}'] = pygame.transform.scale(pygame.image.load(image_path), (square_size, square_size))

load_images()

# Draw the board
def draw_board(window, board):
    colors = [pygame.Color(235, 236, 208), pygame.Color(119, 149, 86)]
    for i in range(8):
        for j in range(8):
            color = colors[(i + j) % 2]
            pygame.draw.rect(window, color, pygame.Rect(j * square_size, i * square_size, square_size, square_size))
            piece = board.board[i][j].piece
            if piece:
                piece_type = type(piece).__name__.lower()
                piece_color = piece.color
                window.blit(piece_images[f'{piece_color}-{piece_type}'], (j * square_size, i * square_size))

# Handle user input
def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    x, y = mouse_pos[0] // square_size, mouse_pos[1] // square_size
    return y, x

def handle_click(board, selected_square, valid_moves):
    if pygame.mouse.get_pressed()[0]:
        rank, column = get_square_under_mouse()
        piece = board.board[rank][column].piece
        if selected_square is None:
            if piece and piece.color == current_turn:
                selected_square = (rank, column)
                valid_moves = piece.validMoves
        else:
            if (rank, column) in valid_moves:
                board.board[selected_square[0]][selected_square[1]].piece.move(rank, column)
                selected_square = None
                valid_moves = []
                switch_turn()
            else:
                selected_square = None
                valid_moves = []
    return selected_square, valid_moves

def switch_turn():
    global current_turn
    current_turn = "black" if current_turn == "white" else "white"

board = Board()
selected_square = None
valid_moves = []
global current_turn
current_turn = "white"

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    selected_square, valid_moves = handle_click(board, selected_square, valid_moves)

    draw_board(window, board)
    pygame.display.flip()

pygame.quit()
'''


board = Board()


board.board[6][4].piece.move(4, 4) # e4
board.board[1][2].piece.move(3, 2) # c5
board.board[4][4].piece.move(3, 4) # e5
board.board[1][3].piece.move(2, 3) # d6
board.board[3][4].piece.move(2, 3) # exd6
board.board[0][1].piece.move(2, 2) # Nc6
board.board[6][3].piece.move(4, 3) # d5
board.board[2][2].piece.move(4, 3) # Nxd5
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

#board.board[6][5].piece.move(4, 5) # f4
#board.board[1][4].piece.move(3, 4) # e5
#board.board[6][6].piece.move(4, 6) # g4
#board.board[0][3].piece.move(4, 7) # Qh4#

board.printBoard()