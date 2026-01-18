from enum import Enum

class Symbol(Enum):
    X = 1
    O = -1
    EMPTY = 0

class Player:
    def __init__(self, name: str, symbol: Symbol):
        self.name = name
        self.symbol = symbol

class TicTacToe:
    def __init__(self, n: int):
        self.n = n
        # Instead of a full grid check, we track sums for each row/col
        self.rows = [0] * n
        self.cols = [0] * n
        self.diag = 0
        self.anti_diag = 0
        # We still keep a board to prevent playing on the same spot
        self.board = [[0] * n for _ in range(n)]

    def make_move(self, row: int, col: int, player: Player) -> bool:
        # Basic validation
        if not (0 <= row < self.n and 0 <= col < self.n) or self.board[row][col] != 0:
            return False

        # Mark board and get point value (1 or -1)
        val = player.symbol.value
        self.board[row][col] = val

        # Update counters
        self.rows[row] += val
        self.cols[col] += val
        
        if row == col:
            self.diag += val
        if row + col == self.n - 1:
            self.anti_diag += val

        # Simple check: did any counter reach the board size (n)?
        # Using abs() handles both +n (Player X) and -n (Player O)
        # Check if the absolute sum of any line equals N
        if abs(self.rows[row]) == self.n: 
            return True
        if abs(self.cols[col]) == self.n:
            return True
        if abs(self.diag) == self.n: 
            return True
        if abs(self.anti_diag) == self.n: 
            return True

        return False

# --- Main Method ---
if __name__ == "__main__":
    p1 = Player("Alice", Symbol.X)
    p2 = Player("Bob", Symbol.O)
    
    n = 3
    game = TicTacToe(n)
    players = [p1, p2]
    turn = 0

    while turn < n * n:
        current_p = players[turn % 2]
        print(f"Turn {turn + 1}: {current_p.name}'s move")
        
        try:
            r, c = map(int, input("Enter row and col: ").split())
            if game.make_move(r, c, current_p):
                print(f"*** {current_p.name} WINS! ***")
                break
            turn += 1
        except ValueError:
            print("Invalid input.")
    else:
        print("It's a draw!")