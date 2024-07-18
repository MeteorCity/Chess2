from collections import defaultdict

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
        self.findAllLegalMoves()
        self.positions = defaultdict(int)
        self.fiftyMoveCounter = 0
    
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
                
                squareColor = "white" if (i + j) % 2 == 0 else "black"
                square = Square(piece, i, j, squareColor)
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
    
    def findAllLegalMoves(self):
        '''
        Finds all the valid moves for every piece. Called after finding all
        the valid moves.
        '''
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].piece
                if piece is not None:
                    piece.findLegalMoves()
    
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
        Returns True or False based on whether the king of the passed
        in color is in check or not.
        '''
        oppAttacks = []
        king = None

        for i in range(8):
            for j in range(8):
                if (piece := self.board[i][j].piece) and piece.color != color:
                    oppAttacks.extend(piece.validMoves)
                elif piece and piece.color == color and type(piece).__name__ == "King":
                    king = piece
        
        assert king is not None, "King is missing from the board"
        return (king.rank, king.column) in oppAttacks
    
    def isKingInCheckmate(self, color):
        '''
        Returns True or False based on whether the king of the passed
        in color is in checkmate or not.
        '''
        if not self.isKingInCheck(color):
            return False

        for i in range(8):
            for j in range(8):
                if (piece := self.board[i][j].piece) and piece.color == color:
                    if piece.legalMoves: # There are legal moves
                        return False

        return True
    
    def isKingInStalemate(self, color):
        '''
        Returns True or False based on whether the king of the passed
        in color is in stalemate or not.
        '''
        if self.isKingInCheck(color):
            return False

        for i in range(8):
            for j in range(8):
                if (piece := self.board[i][j].piece) and piece.color == color:
                    if piece.legalMoves: # There are legal moves
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
        # TODO might have to change this to avoid error None object doesn't contain attribute __name__
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
        
        # Calculate opponent attacks
        oppAttacks = []
        for i in range(8):
            for j in range(8):
                if (piece := self.board[i][j].piece) and piece.color != color:
                    oppAttacks.extend(piece.validMoves)

        # If there are pieces in the way or the king will castle into
        # or through check, return False
        for i in range(1, 3):
            offset = i if side == "kingside" else -i
            if (self.board[rank][4 + offset].piece is not None or
                (rank, 4 + offset) in oppAttacks):
                return False
        
        return True
    
    def posToFEN(self, board):
        '''
        Takes in a 2d array representing the board and returns a FEN string
        of the corresponding position.
        Currently only piece placement will be implemented but, if necessary,
        more fields will be introduced in the future for active color, castling
        rights, etc.
        '''
        fen = ["" for _ in range(8)]
        spaceCounter = 0

        for i in range(8):
            for j in range(8):
                if (piece := board[i][j].piece):
                    name = type(piece).__name__
                    letter = ""
                    if name == "Knight":
                        letter = name[1].upper() if piece.color == "white" else name[1]
                    else:
                        letter = name[0].lower() if piece.color == "black" else name[0]
                    
                    if spaceCounter == 0:
                        fen[i] += letter
                    else:
                        fen[i] += str(spaceCounter) + letter
                    spaceCounter = 0
                else:
                    spaceCounter += 1

            if spaceCounter != 0:
                fen[i] += str(spaceCounter)
            spaceCounter = 0
            fen[i] += "/"
        
        return "".join(fen)[:-1]

    def hasInsufMaterial(self, color):
        '''
        Returns True or Falsed based on whether the given color has
        insufficient mating material.
        '''
        pieces = []
        for i in range(8):
            for j in range(8):
                if (piece := self.board[i][j].piece) and piece.color == color:
                    pieces.append(type(piece).__name__)
        
        pieces.remove("King")
        if (pieces == [] or pieces == ["Bishop"] or pieces == ["Knight"] or
            pieces == ["Knight", "Knight"]):
            return True
        
        return False
    
    def checkEndings(self, piece, moveToPiece):
        '''
        Checks if the conditions for a game to end have been met. Checks
        for checkmate, stalemate, 3-move position repeat, and 50-move rule
        draw.
        '''
        oppositeColor = "white" if piece.color == "black" else "black"

        # Checkmate
        if self.isKingInCheckmate(oppositeColor):
            print(f"{oppositeColor} is in checkmate!")
            return True

        # Stalemate
        if self.isKingInStalemate(oppositeColor):
            print(f"{oppositeColor} is in stalemate!")
            return True
        
        # 3-move repetition
        fenString = self.posToFEN(self.board)
        self.positions[fenString] += 1
        if self.positions[fenString] == 3:
            print("Game is a draw by 3-time position repeat.")
            return True

        # 50-move draw
        if moveToPiece is not None or type(piece).__name__ == "Pawn":
            self.fiftyMoveCounter = 0
        else:
            self.fiftyMoveCounter += 0.5
        if self.fiftyMoveCounter == 50:
            print("Game is a draw by 50-move rule.")
            return True

        # Insufficient material
        if self.hasInsufMaterial("white") and self.hasInsufMaterial("black"):
            print("Game is a draw due to insufficient mating material")
            return True