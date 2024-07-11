from Piece import Piece

class Knight(Piece):
    def findValidMoves(self):
        '''
        Calculates the valid moves of the knight piece before regarding
        any checks or pins. Overrides the method in the Piece class.
        '''
        self.validMoves = [] # Reset valid moves
        i, j = self.rank, self.column

        # Lower right
        if 0 <= i + 2 <= 7 and 0 <= j + 1 <= 7:
            piece = self.board.board[i + 2][j + 1].piece
            if not piece or piece.color != self.color:
                self.validMoves.append((i + 2, j + 1))

        # Lower left
        if 0 <= i + 2 <= 7 and 0 <= j - 1 <= 7:
            piece = self.board.board[i + 2][j - 1].piece
            if not piece or piece.color != self.color:
                self.validMoves.append((i + 2, j - 1))

        # Left lower
        if 0 <= i + 1 <= 7 and 0 <= j - 2 <= 7:
            piece = self.board.board[i + 1][j - 2].piece
            if not piece or piece.color != self.color:
                self.validMoves.append((i + 1, j - 2))
        
        # Left upper
        if 0 <= i - 1 <= 7 and 0 <= j - 2 <= 7:
            piece = self.board.board[i - 1][j - 2].piece
            if not piece or piece.color != self.color:
                self.validMoves.append((i - 1, j - 2))
        
        # Upper left
        if 0 <= i - 2 <= 7 and 0 <= j - 1 <= 7:
            piece = self.board.board[i - 2][j - 1].piece
            if not piece or piece.color != self.color:
                self.validMoves.append((i - 2, j - 1))

        # Upper right
        if 0 <= i - 2 <= 7 and 0 <= j + 1 <= 7:
            piece = self.board.board[i - 2][j + 1].piece
            if not piece or piece.color != self.color:
                self.validMoves.append((i - 2, j + 1))

        # Right upper
        if 0 <= i - 1 <= 7 and 0 <= j + 2 <= 7:
            piece = self.board.board[i - 1][j + 2].piece
            if not piece or piece.color != self.color:
                self.validMoves.append((i - 1, j + 2))

        # Right lower
        if 0 <= i + 1 <= 7 and 0 <= j + 2 <= 7:
            piece = self.board.board[i + 1][j + 2].piece
            if not piece or piece.color != self.color:
                self.validMoves.append((i + 1, j + 2))