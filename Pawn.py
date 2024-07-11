from Piece import Piece

class Pawn(Piece):
    def findValidMoves(self):
        '''
        Calculates the valid moves of the pawn piece before regarding
        any checks or pins. Overrides the method in the Piece class.

        TODO Add en-passant
        '''
        self.validMoves = [] # Reset valid moves
        i, j = self.rank, self.column

        # White pawns
        if self.color == "white":
            # Move forward
            if self.board.board[i - 1][j].piece is None:
                self.validMoves.append((i - 1, j))
                if i == 6 and self.board.board[i - 2][j].piece is None:
                    self.validMoves.append((i - 2, j))

            # Capture left diagonally
            if j - 1 >= 0 and (piece := self.board.board[i - 1][j - 1].piece) and piece.color == "black":
                self.validMoves.append((i - 1, j - 1))

            # Capture right diagonally
            if j + 1 < 8 and (piece := self.board.board[i - 1][j + 1].piece) and piece.color == "black":
                self.validMoves.append((i - 1, j + 1))
        
        # Black pawns
        else:
            # Move forward (from black's point of view)
            if self.board.board[i + 1][j].piece is None:
                self.validMoves.append((i + 1, j))
                if i == 1 and self.board.board[i + 2][j].piece is None:
                    self.validMoves.append((i + 2, j))

            # Capture left diagonally (from white's point of view)
            if j - 1 >= 0 and (piece := self.board.board[i + 1][j - 1].piece) and piece.color == "white":
                self.validMoves.append((i + 1, j - 1))

            # Capture right diagonally (from white's point of view)
            if j + 1 < 8 and (piece := self.board.board[i + 1][j + 1].piece) and piece.color == "white":
                self.validMoves.append((i + 1, j + 1))

    def promote():
        pass