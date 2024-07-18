from Piece import Piece

class King(Piece):
    def __init__(self, color, rank, column, board):
        super().__init__(color, rank, column, board)
        self.has_moved = False

    def findValidMoves(self):
        '''
        Calculates the valid moves of the king piece before regarding
        any checks or pins. Overrides the method in the Piece class.

        TODO Add castling
        '''
        self.validMoves = [] # Reset valid moves

        # Add regular king moves
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Exclude king's starting square
                if i == 0 and j == 0:
                    continue

                if 0 <= self.rank + i <= 7 and 0 <= self.column + j <= 7:
                    piece = self.board.board[self.rank + i][self.column + j].piece
                    if not piece or piece.color != self.color:
                        self.validMoves.append((self.rank + i, self.column + j))
        
        # Add castling moves
        rank = 0 if self.color == "black" else 7
        if self.board.canCastle(f"{self.color}", "queenside"):
            self.validMoves.append((rank, 2))
        if self.board.canCastle(f"{self.color}", "kingside"):
            self.validMoves.append((rank, 6))
        
    def move(self, moveRank, moveColumn):
        '''
        Overrides the move function of the piece class such that castling
        can be implemented.
        '''
        # Queenside castle
        if (moveRank, moveColumn) in self.legalMoves and self.column - moveColumn == 2:
            # Update king's position
            self.board.updateBoard(self.rank, self.column, moveRank, moveColumn)
            self.column = moveColumn

            # Update rook's position
            rook = self.board.board[self.rank][0].piece
            self.board.updateBoard(rook.rank, rook.column, self.rank, 3)
            rook.column = 3
            
            # Find new valid and legal moves
            self.board.findAllValidMoves()
            self.board.findAllLegalMoves()
        
        # Kingside Castle
        elif (moveRank, moveColumn) in self.legalMoves and self.column - moveColumn == -2:
            # Update king's position
            self.board.updateBoard(self.rank, self.column, moveRank, moveColumn)
            self.column = moveColumn

            # Update rook's position
            rook = self.board.board[self.rank][7].piece
            self.board.updateBoard(rook.rank, rook.column, self.rank, 5)
            rook.column = 5

            # Find new valid moves
            self.board.findAllValidMoves()
            self.board.findAllLegalMoves()

        # Non-castle move
        else:
            super().move(moveRank, moveColumn)