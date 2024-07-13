from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color, rank, column, board):
        self.color = color # Must be "white" or "black"
        self.rank = rank
        self.column = column
        self.board = board # The piece's Board instance

        # A list of valid moves before taking into account checks or pins
        self.validMoves = []
    
    def printAttr(self):
        '''
        A method to print the attributes of the piece for debugging purposes.
        '''
        print(f"The piece is a {self.color} {type(self).__name__} on rank {self.rank}, column {self.column}")

    def move(self, moveRank, moveColumn):
        # self.board.printBoard()
        if self.isLegal(moveRank, moveColumn):
            oppositeColor = "white" if self.color == "black" else "black"
            if self.board.isKingInCheckmate(oppositeColor): # Checkmate
                print(f"{oppositeColor} is in checkmate!")
            if self.board.isKingInStalemate(oppositeColor): # Stalemate
                print(f"{oppositeColor} is in stalemate!")
            fenString = self.board.posToFEN(self.board.board) # 3-move rep
            self.board.positions[fenString] += 1
            if self.board.positions[fenString] >= 3:
                print("Game is a draw by 3-time position repeat.")
        else:
            print(f"Illegal move: {type(self).__name__} {self.rank, self.column} to {moveRank, moveColumn}")
    
    def isLegal(self, moveRank, moveColumn, movePiecesBack=False, ignoreValidity=False):
        '''
        Given the move coordinates, this function returns whether the move
        is legal or not. If the move is legal, it plays the move and returns
        True. Otherwise, it returns False.
        If the movePiecesBack flag is set to True, then the board will be reset
        no matter if the move is legal or not.
        If the ignoreValidity flag is set to True, then it doesn't matter if 
        the given move is in validMoves or not.
        '''
        assert moveRank > -1 and moveRank < 8 and moveColumn > -1 and moveColumn < 8, "move out of bounds"

        if not ignoreValidity and (moveRank, moveColumn) not in self.validMoves:
            return False

        # Store the piece on the square we're moving to
        moveToPiece = self.board.board[moveRank][moveColumn].piece
        oldRank = self.rank
        oldColumn = self.column

        # Make the move
        self.board.updateBoard(self.rank, self.column, moveRank, moveColumn)
        self.rank = moveRank
        self.column = moveColumn
        self.board.findAllValidMoves()

        # Check if after the move our king is in check
        inCheck = self.board.isKingInCheck(self.color)

        # Reset board to position before move if illegal move or flag was used
        if inCheck or movePiecesBack:
            self.rank = oldRank
            self.column = oldColumn
            self.board.board[self.rank][self.column].piece = self
            self.board.board[moveRank][moveColumn].piece = moveToPiece
        
        # Reset the valid moves
        self.board.findAllValidMoves()

        return not inCheck
    
    @abstractmethod
    def findValidMoves(self):
        '''
        Abstract method to be implemented by child classes.
        Calculates the valid moves of the piece before regarding any checks or pins.
        '''
        pass