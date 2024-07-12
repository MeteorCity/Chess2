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

        for i in range(-1, 2):
            for j in range(-1, 2):
                # Exclude king's starting square
                if i == 0 and j == 0:
                    continue

                if 0 <= self.rank + i <= 7 and 0 <= self.column + j <= 7:
                    piece = self.board.board[self.rank + i][self.column + j].piece
                    if not piece or piece.color != self.color:
                        self.validMoves.append((self.rank + i, self.column + j))
        
    def move(self, moveRank, moveColumn):
        # Queenside castle
        if (self.rank == moveRank and self.column - moveColumn == 2 and
        self.board.canCastle(f"{self.color}", "queenside")):
            # Update king's position
            self.board.updateBoard(self.rank, self.column, moveRank, moveColumn)
            self.column = moveColumn

            # Update rook's position
            rook = self.board.board[self.rank][0].piece
            self.board.updateBoard(rook.rank, rook.column, self.rank, 3)
            rook.column = 3
            
            # Find new valid moves
            self.board.findAllValidMoves()
        
        # Kingside Castle
        elif (self.rank == moveRank and self.column - moveColumn == -2 and
        self.board.canCastle(f"{self.color}", "kingside")):
            # Update king's position
            self.board.updateBoard(self.rank, self.column, moveRank, moveColumn)
            self.column = moveColumn

            # Update rook's position
            rook = self.board.board[self.rank][7].piece
            self.board.updateBoard(rook.rank, rook.column, self.rank, 5)
            rook.column = 5

            # Find new valid moves
            self.board.findAllValidMoves()
        else:
            super().move(moveRank, moveColumn)
        
        self.has_moved = True