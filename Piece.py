from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color, rank, column, board):
        self.color = color # Must be "white" or "black"
        self.rank = rank
        self.column = column
        self.board = board # The piece's Board instance
        self.validMoves = [] # The piece's valid moves before accounting for checks or pins
        self.legalMoves = [] # The piece's actual legal moves
    
    def printAttr(self):
        '''
        A method to print the attributes of the piece for debugging purposes.
        '''
        print(f"The piece is a {self.color} {type(self).__name__} on rank {self.rank}, column {self.column}")

    def move(self, moveRank, moveColumn):
        moveToPiece = self.board.board[moveRank][moveColumn].piece
        # self.board.printBoard()
        if (moveRank, moveColumn) in self.legalMoves:
            # Make the move
            self.board.updateBoard(self.rank, self.column, moveRank, moveColumn)
            self.rank = moveRank
            self.column = moveColumn

            # Set the has_moved flag to true for the king and rook if either moved
            if type(self).__name__ == "King" or type(self).__name__ == "Rook":
                self.has_moved = True

            # Refind the valid and legal moves after the move is made
            self.board.findAllValidMoves()
            self.board.findAllLegalMoves()

            # Check for any possible endings (checkmate, 3-move rep, etc)
            self.board.checkEndings(self, moveToPiece)
        else:
            print(f"Illegal move: {type(self).__name__} {self.rank, self.column} to {moveRank, moveColumn}")
    
    def isLegal(self, moveRank, moveColumn):
        '''
        Given the move coordinates, this function returns whether the move
        is legal or not.
        '''
        assert moveRank > -1 and moveRank < 8 and moveColumn > -1 and moveColumn < 8, "move out of bounds"

        # Store the piece on the square we're moving to
        moveToPiece = self.board.board[moveRank][moveColumn].piece
        oldRank = self.rank
        oldColumn = self.column

        # Make the move
        self.board.updateBoard(self.rank, self.column, moveRank, moveColumn)
        self.rank = moveRank
        self.column = moveColumn

        # Find the valid moves of the new position
        self.board.findAllValidMoves()

        # Check if after the move our king is in check
        inCheck = self.board.isKingInCheck(self.color)

        # Reset old position
        self.rank = oldRank
        self.column = oldColumn
        self.board.board[self.rank][self.column].piece = self
        self.board.board[moveRank][moveColumn].piece = moveToPiece
        
        # Reset valid moves
        self.board.findAllValidMoves()

        return not inCheck

    def findLegalMoves(self):
        self.legalMoves = [] # Reset legal moves
        for validMove in self.validMoves:
            if self.isLegal(validMove[0], validMove[1]):
                self.legalMoves.append(validMove)
    
    @abstractmethod
    def findValidMoves(self):
        '''
        Abstract method to be implemented by child classes.
        Calculates the valid moves of the piece before regarding any checks or pins.
        '''
        pass