"""
s'occupe de la validité des moves, les enregistres et stocke les infos 
"""

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves}
        
        self.whiteToMove = True
        self.movelog = []
    '''
    récup le coup comme un paramètre et l'éxécute'''
    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove #tour
    
    
    def undoMove(self):
        if len(self.movelog) != 0: #permet de s'assurer que il y a un coup à annuler
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    '''
    tous les coups sont vérifs
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    '''
    tous les coups sans aucune vérifs
    '''
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #nb de lignes
            for c in range(len(self.board[r])): #nb de colones
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #pions blancs
            if self.board[r-1][c] == "--": #1 carré
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 carré
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: #capture à gauche
                if self.board[r-1][c-1][0] == 'b': 
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:#capture à droite
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:#pion noir
            if self.board[r + 1][c] == "--":
                moves.append(Move((r,c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r,c), (r + 2, c), self.board))

            if c - 1 >= 0: #capture à gauche
                if self.board[r+1][c-1][0] == 'w': 
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:#capture à droite
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))



    def getRookMoves(self, r, c, moves):
        directions = ((-1 , 0), (0 , -1), (1 , 0), (0 , 1))
        ennemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == ennemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2 , -1), (-2 , 1), (-1 , -2), (-1 , 2), (1 , -2), (1 , 2), (2 , -1), (2 , 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol <8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))



    def getBishopMoves(self, r, c, moves):
        directions = ((-1 , -1), (-1 , 1), (1 , -1), (1 , 1))
        ennemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == ennemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break



    def getKingMoves(self, r, c, moves):
        kingMove = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMove[i][0]
            endCol = c + kingMove[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)





class Move():
    ranksToRow = {"1" : 7, "2" : 6, "3" : 5, "4" : 4,
                  "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowToRanks = {v: k for k, v in ranksToRow.items()}
    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3,
                   "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFiles(self.startRow, self.startCol) + self.getRankFiles(self.endRow, self.endCol)


    def getRankFiles(self, r, c):
        return self.colsToFiles[c] + self.rowToRanks[r]