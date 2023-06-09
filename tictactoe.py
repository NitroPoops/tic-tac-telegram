class TicTacToe:
    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def move(self, mark, pos):
        x = pos // 3
        y = pos % 3
        if self.board[x][y] != " ":
            return False
        else:
            self.board[x][y] = mark
            return True

    def getempty(self):
        empty = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    empty.append(str(i * 3 + j))
        return empty

    def checkwin(self):
        # check diagonals
        if self.board[0][0] != " ":
            found = True
            for i in range(3):
                if self.board[0][0] != self.board[i][i]:
                    found = False
            if found:
                return True
        if self.board[0][2] != " ":
            found = True
            for i in range(3):
                if self.board[0][2] != self.board[i][2 - i]:
                    found = False
            if found:
                return True

        # check rows and columns
        for i in range(3):
            if self.board[i][0] != " ":
                found = True
                for j in range(3):
                    if self.board[i][0] != self.board[i][j]:
                        found = False
                if found:
                    return True
            if self.board[0][i] != " ":
                found = True
                for j in range(3):
                    if self.board[0][i] != self.board[j][i]:
                        found = False
                if found:
                    return True

        # no matching lines were found, so no winner
        return False
