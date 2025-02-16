'''
Ask for clarifying questions
Found out following points
1. Played player vs player
2. Board can be of variable dimensions
3. Game can be of connecting 'n' discs in a row (horizontally, vertically or diagonally)
4. Score tracking system for players


######## Future Scope ##########
1. Connect it with Postgresql database to store scores for players
'''

'''

### High level design

1. Board class
2. Player class
3. Game class
4. Game class manages state of the board and turn of players
'''

from enum import Enum

class Piece(Enum):
    EMPTY = 0
    YELLOW = 1
    RED = 2

class Board:
    def __init__(self, rows : int, cols : int, n : int):
        self._rows = rows
        self._cols = cols
        self._grid = self.init_grid()
        self._n = n

    def init_grid(self):
        return [[Piece.EMPTY for _ in range(self._cols)] for _ in range(self._rows)]

    '''
    Why does place_piece belong to Board class?
    1. It cannot be placed in Player class as placing piece will be done by both players on a common grid
    2. It can be placed in Game class but makes more sense to keep and change state of board in Board class itself.
    '''
    def place_piece(self, col : int, piece : Piece) -> int:   #returns the row in which the pice was placed
        if col < 0 or col >= self._cols:
            raise ValueError("Tried to place piece in an invalid place")
        for row in range(self._rows -1, -1, -1):
            if(self._grid[row][col] == Piece.EMPTY):
                self._grid[row][col] = piece
                return row #Piece placed successfully
        return -1  #Column is full
    
    def check_win(self, row: int, col: int, piece: Piece) -> bool:
        def count_consecutive(dx, dy):
            count = 0
            r, c = row, col
            while 0 <= r < self._rows and 0 <= c < self._cols and self._grid[r][c] == piece:
                count += 1
                r += dx
                c += dy
            return count

        # Check all directions
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal (↘, ↙)
        for dx, dy in directions:
            if count_consecutive(dx, dy) + count_consecutive(-dx, -dy) - 1 >= self._n:
                return True
        return False

    

class Player:
    def __init__(self, name : str, piece : Piece):
        self.piece = piece
        self.name = name
        self.score = 0

class Game:
    def __init__(self, rows : int, cols : int, target_score : int, player1 : Player, player2 : Player, n : int) :
        self._grid = Board(rows, cols, n)
        self._target_score = target_score 
        self._player1 = player1
        self._player2 = player2
        self.curr_player = player1

    def play_move(self) -> bool:
        while True:
            col = int(input(f"{self.curr_player.name}'s turn: Enter column number to place a piece: "))
            row = self._grid.place_piece(col, self.curr_player.piece)   #place the piece in specified column
            if row == -1:
                print("Column is full, try again!")
                continue
            break
        is_win = self.check_win(row, col, self.curr_player)

        if is_win:
            return is_win
        
        #Chage current player
        if(self.curr_player.name == self._player1.name):
            self.curr_player = self._player2
        else:
            self.curr_player = self._player1

        return is_win


    def _play_round(self) -> Player : # private method: returns the player that wins the round
        #implementation pending
        moves_count = 0
        while True:
            is_win = self.play_move()
            moves_count += 1

            if is_win:
                print(f"{self.curr_player.name} wins this round!")
                self.curr_player.score += 1
                return self.curr_player

            if moves_count == self._grid._rows * self._grid._cols:
                is_win = False
                return None
        

    def play_game(self)-> Player : # public method : returns the player that wins the game
        #implementation pending
        while self._player1.score < self._target_score and self._player2.score < self._target_score:
            winner = self._play_round()
            if winner is not None:
                print(f"{winner.name} won the round !!!")
                print(f"Status of scores : {self._player1.name} : {self._player1.score} and {self._player2.name} : {self._player2.score}")
                self.curr_player = self._player1
            else:
                print(f"The round ended in draw!")

            if self._player1.score == self._target_score:
                return self._player1
            elif self._player2.score == self._target_score:
                return self._player2

    def check_win(self, row : int, col : int, player : Player) -> bool:
        return self._grid.check_win(row, col, player.piece)
    

class GameController:
    @classmethod
    def play(cls):
        player2 = Player("Suresh", Piece.RED)
        player1 = Player("Ramesh", Piece.YELLOW)

        if player1.piece == player2.piece:
            raise ValueError("Both players cannot play the same piece !!!")
        
        game = Game(6 , 7, 3, player1, player2, 4)
        winner = game.play_game()
        print(f"{winner.name} is the winner!")


GameController.play()