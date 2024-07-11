from Piece import Piece

class Bishop(Piece):
    def findValidMoves(self):
        '''
        Calculates the valid moves of the bishop piece before regarding
        any checks or pins. Overrides the method in the Piece class.
        '''
        self.validMoves = [] # Reset valid moves

        # Down right diagonal
        for i in range(1, 8):
            if 0 <= self.rank + i <= 7 and 0 <= self.column + i <= 7:
                piece = self.board.board[self.rank + i][self.column + i].piece
                if not piece or (piece and piece.color != self.color):
                    self.validMoves.append((self.rank + i, self.column + i))
                if piece: # Stop searching past the found piece
                    break
        
        # Down left diagonal
        for i in range(1, 8):
            if 0 <= self.rank + i <= 7 and 0 <= self.column - i <= 7:
                piece = self.board.board[self.rank + i][self.column - i].piece
                if not piece or (piece and piece.color != self.color):
                    self.validMoves.append((self.rank + i, self.column - i))
                if piece: # Stop searching past the found piece
                    break
        
        # Up left diagonal
        for i in range(1, 8):
            if 0 <= self.rank - i <= 7 and 0 <= self.column - i <= 7:
                piece = self.board.board[self.rank - i][self.column - i].piece
                if not piece or (piece and piece.color != self.color):
                    self.validMoves.append((self.rank - i, self.column - i))
                if piece: # Stop searching past the found piece
                    break

        # Up right diagonal
        for i in range(1, 8):
            if 0 <= self.rank - i <= 7 and 0 <= self.column + i <= 7:
                piece = self.board.board[self.rank - i][self.column + i].piece
                if not piece or (piece and piece.color != self.color):
                    self.validMoves.append((self.rank - i, self.column + i))
                if piece: # Stop searching past the found piece
                    break