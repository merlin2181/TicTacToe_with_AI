# write your code here

def print_cells(cell_list):
    """
    Outputs the current board to the screen
    """
    board = f"---------\n" \
            f"| {cell_list[2][0]} {cell_list[2][1]} {cell_list[2][2]} |\n" \
            f"| {cell_list[1][0]} {cell_list[1][1]} {cell_list[1][2]} |\n" \
            f"| {cell_list[0][0]} {cell_list[0][1]} {cell_list[0][2]} |\n" \
            f"---------"
    print(board)


def check_coordinates(numbers, board):
    """
    Function that checks whether the coordinates entered by the user are "legal".
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
    if board[numbers[1] - 1][numbers[0] - 1] != " ":
        return 'This cell is occupied! Choose another one!'
    return True


def check_winner(board):
    """
    Function that determines if the game is finished or not and
    whether X or O has one the game.
    """
    col = check_columns(board)
    row = check_rows(board)
    diag = check_diagonal(board)
    exes = ['X', 'X', 'X']
    oohs = ['O', 'O', 'O']
    winner = [col, row, diag]
    for item in winner:
        for i in range(len(item)):
            if item[i] == exes or item[i] == oohs:
                winning_move = item[i][0]
                return winning_move
    for item in winner:
        for i in range(len(item)):
            if ' ' in item[i]:
                return "Game not finished"
    return "Draw"


def check_columns(board):
    """
    Gathers all the entries in each column going from left to right
    """
    check_col = [[], [], []]
    for i in range(3):
        for j in range(3):
            check_col[i].append(board[j][i])
    return check_col


def check_rows(board):
    """
    Gathers all the entries in each row going from bottom to top
    """
    check_row = [[], [], []]
    for i in range(3):
        for j in range(3):
            check_row[i].append(board[i][j])
    return check_row


def check_diagonal(board):
    """
    Gathers all the entries in each diagonal starting from bottom left to top right
    and then from bottom right to top left
    """
    check_diag = [[], []]
    for i in range(3):
        check_diag[0].append(board[i][i])
    j = 2
    for i in range(3):
        check_diag[1].append(board[i][j])
        j -= 1
    return check_diag


starting_moves = input('Enter cells: ')
starting_moves = [char if char != "_" else " " for char in starting_moves]

# Determines if it's X's move or O's move
if starting_moves.count('X') == starting_moves.count('O'):
    move = 0
else:
    move = 1

# Formats the input into the game board
layout = [[], [], []]
for i in range(3):
    for _ in range(3):
        layout[i].append(starting_moves.pop())
for i in range(3):
    layout[i].reverse()
print_cells(layout)

# Loop to asking the user for the correct coordinates
flag = True
while flag:
    nums = input('Enter the coordinates: ').split()
    check = check_coordinates(nums, layout)
    if type(check) == str:
        print(check)
    else:
        flag = False

# Main part of the game
nums = [(int(num) - 1) for num in nums]
if move % 2 == 0:
    layout[nums[1]][nums[0]] = 'X'
    move += 1
else:
    layout[nums[1]][nums[0]] = 'O'
    move -= 1
print_cells(layout)
outcome = check_winner(layout)
if len(outcome) == 1:
    print(f'{outcome} wins')
else:
    print(outcome)
