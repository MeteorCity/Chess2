from Piece import Piece

class Rook(Piece):
    def __init__(self, color, rank, column, board):
        super().__init__(color, rank, column, board)
        self.has_moved = False

    def findValidMoves(self):
        '''
        Calculates the valid moves of the rook piece before regarding
        any checks or pins. Overrides the method in the Piece class.
        '''
        self.validMoves = [] # Reset valid moves

        # Down
        for i in range(1, 8):
            if 0 <= self.rank + i <= 7:
                piece = self.board.board[self.rank + i][self.column].piece
                if not piece or (piece and piece.color != self.color):
                    self.validMoves.append((self.rank + i, self.column))
                if piece: # Stop searching past the found piece
                    break
        
        # Up
        for i in range(1, 8):
            if 0 <= self.rank - i <= 7:
                piece = self.board.board[self.rank - i][self.column].piece
                if not piece or (piece and piece.color != self.color):
                    self.validMoves.append((self.rank - i, self.column))
                if piece: # Stop searching past the found piece
                    break

        # Right
        for j in range(1, 8):
            if 0 <= self.column + j <= 7:
                piece = self.board.board[self.rank][self.column + j].piece
                if not piece or (piece and piece.color != self.color):
                    self.validMoves.append((self.rank, self.column + j))
                if piece: # Stop searching past the found piece
                    break

        # Left
        for j in range(1, 8):
            if 0 <= self.column - j <= 7:
                piece = self.board.board[self.rank][self.column - j].piece
                if not piece or (piece and piece.color != self.color):
                    self.validMoves.append((self.rank, self.column - j))
                if piece: # Stop searching past the found piece
                    break
    
    def move(self, moveRank, moveColumn):
        super().move(moveRank, moveColumn)
        self.has_moved = True