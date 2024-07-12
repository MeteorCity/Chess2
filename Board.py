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
    
    def kingHelper(self, color):
        '''
        A helper function for the inCheck, inCheckmate, and inStalemate
        functions. Returns the squares the opponent is attacking and the
        King object of the given color.
        '''
        assert color == "white" or color == "black", "color must be white or black"

        oppAttacks = []
        king = None

        for i in range(8):
            for j in range(8):
                if (piece := self.board[i][j].piece) and piece.color != color:
                    # Prevent forward pawn squares from being added to oppAttacks
                    if type(piece).__name__ == "Pawn":
                        attackMoves = list(filter(lambda x: x[1] != piece.column, piece.validMoves))
                        oppAttacks.extend(attackMoves)
                    else:
                        oppAttacks.extend(piece.validMoves)
                elif piece and piece.color == color and type(piece).__name__ == "King":
                    king = piece
        
        assert king is not None, "King is missing from the board"
        return oppAttacks, king
    
    def isKingInCheck(self, color):
        '''
        Returns True or False based on whether the king of the passed
        in color is in check or not.
        '''
        oppAttacks, king = self.kingHelper(color)
        return (king.rank, king.column) in oppAttacks
    
    def isKingInCheckmate(self, color):
        '''
        Returns True or False based on whether the king of the passed
        in color is in checkmate or not.
        '''
        oppAttacks, king = self.kingHelper(color)
        
        # King in check
        if (king.rank, king.column) in oppAttacks:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # Exclude king's starting square
                    if i == 0 and j == 0:
                        continue
                    
                    if (0 <= king.rank + i <= 7 and 0 <= king.column + j <= 7 and
                    king.isLegal(king.rank + i, king.column + j, True)):
                        return False
        else:
            return False

        return True
    
    def canCastle(self, color, side):
        '''
        Returns True or False based on whether the king of the passed
        in color can castle on the passed in side.
        '''
        assert side == "kingside" or side == "queenside", "side must be kingside or queenside"

        rookCol = 7 if side == "kingside" else 0
        rank = 0 if color == "black" else 7

        # If the king or the rook aren't on their starting locations, return False
        if (type(self.board[rank][4].piece).__name__ != "King" or
            type(self.board[rank][rookCol].piece).__name__ != "Rook"):
            return False
        
        king = self.board[rank][4].piece
        rook = self.board[rank][rookCol].piece
        
        # If the king or rook has moved, return False
        if (king.has_moved or rook.has_moved):
            return False
        
        # If the king is currently in check, return False
        if self.isKingInCheck(color):
            return False

        # If there are pieces in the way or the king will castle into
        # or through check, return False
        for i in range(1, 3):
            offset = i if side == "kingside" else -i
            if (self.board[rank][4 + offset].piece is not None or
                not king.isLegal(rank, 4 + offset, True, True)):
                return False
        
        return True