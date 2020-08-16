"""
A more involved game of Tic Tac Toe that offers the ability to play against the computer using
two different difficulties: easy and hard

To play: type "start" followed by either user, easy or medium.
Example: 'start easy user' ==> start the game, player1 is easy computer, player2 is the user
Example: 'start medium medium' ==> start the game, player1 and player2 are both medium
          difficulty computer players
"""
import random
import sys


class TicTacToe:

    def __init__(self):
        self.move = 0
        self.player1 = None
        self.player2 = None
        self.board = {(i, j): " " for i in range(1, 4) for j in range(1, 4)}
        self.winner = None
        self.draw = None

    def pick_player(self):
        """
        Method that starts the game by having the user choose to play against computer,
        another user or have the computer play itself
        """
        player_choice = ['user', 'easy', 'medium']
        while True:
            choice = input('Input Command: ').split()
            if choice[0] == 'exit':
                sys.exit()
            elif choice[0] == 'start' and len(choice) == 3:
                if choice[1] in player_choice and choice[2] in player_choice:
                    self.player1 = [choice[1], 'X']
                    self.player2 = [choice[2], 'O']
                    self.print_gameboard()
                    self.run_game()
                else:
                    print('Bad parameters!')
            else:
                print('Bad parameters!')

    def run_game(self):
        """
        Method that runs the real code of the game. It has the player choose a position and
        checks whether the game is won or a draw.
        """
        while True:
            if self.move == 0:
                self.choose_player(self.player1)
                self.move += 1
            else:
                self.choose_player(self.player2)
                self.move -= 1
            self.print_gameboard()
            self.check_winner()
            if self.winner is None and self.draw is None:
                continue
            elif self.winner is not None:
                print(f'{self.winner} wins')
                self.reset_game()
                break
            elif self.draw is not None:
                print('Draw')
                self.reset_game()
                break
        self.pick_player()

    def print_gameboard(self):
        """
        Outputs the current board to the screen
        """
        board_output = f"---------\n" \
                       f"| {self.board[(3, 1)]} {self.board[(3, 2)]} {self.board[(3, 3)]} |\n" \
                       f"| {self.board[(2, 1)]} {self.board[(2, 2)]} {self.board[(2, 3)]} |\n" \
                       f"| {self.board[(1, 1)]} {self.board[(1, 2)]} {self.board[(1, 3)]} |\n" \
                       f"---------"
        print(board_output)

    def choose_player(self, player):
        """
        Method that decides whether the computer is playing or the user
        """
        if player[0] == 'user':
            return self.user_move(player[1])
        elif player[0] == 'easy':
            return self.computer_move_easy(player[1])
        elif player[0] == 'medium':
            return self.computer_move_medium(player[1])

    def user_move(self, char):
        """
        method that lets the user choose a move
        """
        flag = True
        while flag:
            nums = input('Enter the coordinates: ').split()
            check = self.check_coordinates(nums)
            if type(check) == str:
                print(check)
            else:
                flag = False
        self.board[(nums[0], nums[1])] = char

    def computer_move_easy(self, char, level='easy'):
        """
        method that lets the computer choose a move by creating a list of empty cells and
        randomly choosing a cell from that list
        """
        random.seed()  # reseed everytime to get as random a result as possible
        print(f'Making move level "{level}"')
        comp_move = []
        for key, value in self.board.items():
            if value == ' ':
                comp_move.append(key)
        self.board[random.choice(comp_move)] = char

    def computer_move_medium(self, char):
        """
        Method that increases the difficulty of playing against the computer.  This method
        actively looks for offensive and defensive moves.
        """
        if char == 'X':
            opp_char = 'O'
        else:
            opp_char = 'X'
        space = 0
        items = list(self.board.items())
        for item in items:
            if item[1] == ' ':
                space += 1
        if space > 6:
            self.computer_move_easy(char, 'medium')
        else:
            offense_move = self.potential_move(items, char)
            if offense_move is None:
                defense_move = self.potential_move(items, opp_char)
                if defense_move is None:
                    self.computer_move_easy(char, 'medium')
                else:
                    print('Making move level "medium"')
                    self.board[defense_move] = char
            else:
                print('Making move level "medium"')
                self.board[offense_move] = char

    def potential_move(self, item, char):
        """
        Method that goes through every column, row and diagonal to determine an offensive or
        defensive move.
        """
        for i in range(3):
            check_board = [item[i], item[i + 3], item[i + 6]]
            pos = self._analyze_board(check_board, char)
            if pos:
                return pos
        for i in range(0, 8, 3):
            check_board = [item[i], item[i + 1], item[i + 2]]
            pos = self._analyze_board(check_board, char)
            if pos:
                return pos
        check_board = [item[0], item[4], item[8]]
        pos = self._analyze_board(check_board, char)
        if pos:
            return pos
        check_board = [item[2], item[4], item[6]]
        pos = self._analyze_board(check_board, char)
        if pos:
            return pos
        return None

    def check_coordinates(self, numbers):
        """
        Method that checks whether the coordinates entered by the user are "legal".
        Returns an error message or True
        """
        if len(numbers) != 2:
            return 'You should enter numbers!'
        num_list = [1, 2, 3]
        try:
            numbers[0], numbers[1] = int(numbers[0]), int(numbers[1])
        except ValueError:
            return 'You should enter numbers!'
        if numbers[0] not in num_list or numbers[1] not in num_list:
            return 'Coordinates should be from 1 to 3!'
        if self.board[(numbers[0], numbers[1])] != " ":
            return 'This cell is occupied! Choose another one!'
        return True

    def check_winner(self):
        """
        Method that determines if the game is finished or not and
        whether X or O has won the game or it is a draw.
        """
        items = list(self.board.items())
        moves = ['X', 'O']
        for move in moves:
            # Checks columns
            for i in range(3):
                if items[i][1] == move and items[i][1] == items[i + 3][1] == items[i + 6][1]:
                    self.winner = items[i][1]
            # Checks rows
            for i in range(0, 8, 3):
                if items[i][1] == move and items[i][1] == items[i + 1][1] == items[i + 2][1]:
                    self.winner = items[i][1]
            # Checks diagonals
            if items[0][1] == move and items[0][1] == items[4][1] == items[8][1]:
                self.winner = items[0][1]
            elif items[2][1] == move and items[2][1] == items[4][1] == items[6][1]:
                self.winner = items[2][1]
        # If there is still no winner, it checks for draw
        if self.winner is None:
            self.check_draw()

    def check_draw(self):
        """
        Totals all the Xs and Os on the board. If there are 9 total without a winner, then
        this sets self.draw to True
        """
        exs = 0
        ohs = 0
        for value in self.board.values():
            if value == 'X':
                exs += 1
            elif value == 'O':
                ohs += 1
        if exs + ohs == 9:
            self.draw = True

    def reset_game(self):
        """
        Method that resets the following variables to begin a new game
        """
        self.move = 0
        self.board = {(i, j): " " for i in range(1, 4) for j in range(1, 4)}
        self.draw = None
        self.winner = None

    @staticmethod
    def _analyze_board(segment, char):
        """
        Static method that analyzes the given segment list and checks whether a move can complete
        three Xs or three Os and returns where to put that character in the board.
        """
        temp_hold = [segment[i][1] for i in range(3)]
        if temp_hold.count(char) == 2 and ' ' in temp_hold:
            pos = segment[temp_hold.index(' ')][0]
            if pos:
                return pos
        return None


if __name__ == '__main__':
    ttt = TicTacToe()
    ttt.pick_player()
