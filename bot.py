#from main import Game
import random
from game import *

black_list = []

def do_turn(game, gui) :

    print("black list:", black_list)
    # I can win
    best_column = column_to_win(game, game.player)
    if best_column != -1: #there is a column to win
        row = game.available_slot(best_column)
        print("best column: ", best_column, "row:", row)
        game.place(game.player, row, best_column, gui)
        return None

    # enemy can win
    enemy_best_column = column_to_win(game, game.enemy)
    if enemy_best_column != -1:  # there is a column for enemy to win
        row = game.available_slot(enemy_best_column)
        print("enemy best column: ", enemy_best_column, "row:", row)
        game.place(game.player, row, enemy_best_column, gui)
        return None

    column = random.randint(0, 6)
    print('column', column)
    row = game.available_slot(column)
    in_black_list = (row, column) in black_list
    while row == None or in_black_list:
        column = random.randint(0, 6)
        print('column', column)
        row = game.available_slot(column)
        print('black list', black_list)
        in_black_list = (row, column) in black_list

    print(f'row: {row} column: {column}')
    game.place(game.player, row, column, gui)

def best_column(game):
    pass

def column_to_win(game, player):
    """:arg Game game :return: the column index to place piece and win, if there is none returns -1"""
    # win in column
    for column_index in range(NUMBER_OF_COLUMNS):
        pieces_count = 0
        for j in range(NUMBER_OF_ROWS):
            row_index = NUMBER_OF_ROWS - (j + 1)  # the check goes from bottom to top
            if game.board[row_index][column_index] == player:
                pieces_count += 1
            elif game.board[row_index][column_index] != EMPTY_SLOT: # enemy piece
                pieces_count = 0
            else: #empty slot
                break
        three_in_one_column = pieces_count == 3
        there_is_space = game.board[0][column_index] == EMPTY_SLOT
        if  three_in_one_column and there_is_space:
            print("win with column")
            return column_index

    # win in row
    for i in range(NUMBER_OF_ROWS):
        row_index = NUMBER_OF_ROWS - (i + 1)
        # pieces_count = 0
        # column_index = 0
        for column_index in range(NUMBER_OF_COLUMNS - 3):
            # print('win in row: current column checking: ', column_index)
            if __can_win_in_row(game.board[row_index][column_index : column_index + 4], player):
                empty_cell_column = column_index + game.board[row_index][column_index : column_index + 4].index(EMPTY_SLOT)
                print("can win in column: " , empty_cell_column, "row:", row_index)
                if game.can_place_piece(row_index, empty_cell_column):
                    return empty_cell_column
                else:
                    #TODO: make this black list thing work!
                    first_empty_row = game.available_slot(empty_cell_column)
                    print('first_empty_row', first_empty_row)
                    one_below = first_empty_row  - row_index == 1
                    if one_below and not (first_empty_row, empty_cell_column) in black_list:
                        black_list.append((first_empty_row, empty_cell_column))
        #     if game.board[row_index][column_index] == player:
        #         pieces_count += 1
        #     elif game.board[row_index][column_index] != EMPTY_SLOT:  # enemy piece
        #         pieces_count = 0
        #     if pieces_count == 3:  # can win
        #         break
        # print('column index:', column_index)
        # if pieces_count == 3:
        #     column_option1 =  column_index + 1
        #     column_option2 = column_index - 3
        #     if game.can_place_piece(row_index, column_option1):
        #         print("win with row")
        #         return column_option1
        #     if game.can_place_piece(row_index, column_option2):
        #         print("win with row")
        #         return column_option2

    #
    """
    for i in range(NUMBER_OF_ROWS):
        for j in range(NUMBER_OF_COLUMNS):
            up_left = game.legal_index(i - 3, j - 3) and __can_win_in_row(game.get_sequence(i, j, -1, -1), player)
            if up_left:
                
            up_right = False
            down_left = False
            down_right = False
            if

    """
    return -1
# def __can_win_in_sequence(game, player, row_direction, column_direction):
#     if not game.legal_index()
#     for i in range(1, 4):


def __can_win_in_row(row, player):
    """get a row and player, returns True if there is a spot for given player to place piece and win.
    note that the row has to be 4 cells long.
    if cant win returns False"""
    pieces_count = 0
    for i in range(4):
        if row[i] == player:
            pieces_count += 1
        elif row[i] != EMPTY_SLOT: #found enemy piece
            return False
    three_pieces_one_empty = pieces_count == 3 # [x, x, " ", x] for example, can win
    return three_pieces_one_empty