from Square import Square
from Piece import Piece
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King
from Pawn import Pawn

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setupBoard()
        self.findAllValidMoves()
    
    def setupBoard(self):
        '''
        Sets up self.board with the chess starting position. Each element
        in the self.board array will be a Square object either containing
        a piece or not based on its location.
        '''
        for i in range(8):
            for j in range(8):
                piece = None

                if i == 0:
                    if j == 0 or j == 7:
                        piece = Rook("black", i, j, self)
                    if j == 1 or j == 6:
                        piece = Knight("black", i, j, self)
                    if j == 2 or j == 5:
                        piece = Bishop("black", i, j, self)
                    if j == 3:
                        piece = Queen("black", i, j, self)
                    if j == 4:
                        piece = King("black", i, j, self)
                if i == 1:
                    piece = Pawn("black", i, j, self)
                
                if i == 6:
                    piece = Pawn("white", i, j, self)
                if i == 7:
                    if j == 0 or j == 7:
                        piece = Rook("white", i, j, self)
                    if j == 1 or j == 6:
                        piece = Knight("white", i, j, self)
                    if j == 2 or j == 5:
                        piece = Bishop("white", i, j, self)
                    if j == 3:
                        piece = Queen("white", i, j, self)
                    if j == 4:
                        piece = King("white", i, j, self)
                
                square = Square(piece, i, j)
                self.board[i][j] = square
    
    def findAllValidMoves(self):
        '''
        Finds all the valid moves for every piece. Called after initializing
        the board and after each move.
        '''
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].piece
                if piece is not None:
                    piece.findValidMoves()
    
    def printBoard(self):
        '''
        Prints the board out for debugging purposes.
        '''
        squares = [["_" for _ in range(8)] for _ in range(8)]

        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].piece
                if piece != None:
                    name = type(piece).__name__
                    squares[i][j] = name[0] if name != "Knight" else "N"
            
            print(squares[i])
    
    def updateBoard(self, orig_rank, orig_column, new_rank, new_column):
        '''
        Updates the position of the pieces on the board after a move.
        '''
        piece = self.board[orig_rank][orig_column].piece
        self.board[orig_rank][orig_column].piece = None
        self.board[new_rank][new_column].piece = piece
    
    def isKingInCheck(self, color):
        '''
        Returns True or False based on the whether the king of the passed
        in color is in check or not.
        '''
        oppAttacks = []
        kingLocation = None

        for i in range(8):
            for j in range(8):
                if (piece := self.board[i][j].piece) and piece.color != color:
                    oppAttacks.extend(piece.validMoves)
                elif piece and piece.color == color and type(piece).__name__ == "King":
                    kingLocation = (i, j)
        
        return kingLocation in oppAttacks