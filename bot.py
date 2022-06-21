#from main import Game
import random
from game import *

class Bot():
    def __init__(self, game):
        self.game = game
        # self.black_list = {
        #     game.current: [],
        #     game.enemy: []
        #     #TODO: change it knows what is the player(enemy) and what is the bot(me)
        # }
        self.black_list = []


    def reset_bot(self):
        """resets the black list of the bot"""
        #TODO: make this bot a class and black list an attrebute not global var
        self.black_list = []


    def best_column(game):
        pass

    def column_to_win(self, game, player):
        """:arg Game game, String player :return: the column index to place piece and win, if there is none returns -1"""

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
            if three_in_one_column and there_is_space:
                print("win with column")
                return column_index

        # win in row
        for i in range(NUMBER_OF_ROWS):
            row_index = NUMBER_OF_ROWS - (i + 1)
            for column_index in range(NUMBER_OF_COLUMNS - 3):
                # print('win in row: current column checking: ', column_index)
                if self.__can_win_in_row(game.board[row_index][column_index : column_index + 4], player):
                    empty_cell_column = column_index + game.board[row_index][column_index : column_index + 4].index(EMPTY_SLOT)
                    print("can win in column: " , empty_cell_column, "row:", row_index)
                    if game.can_place_piece(row_index, empty_cell_column):
                        return empty_cell_column
                    else:
                        first_empty_row = game.available_slot(empty_cell_column)
                        print('first_empty_row', first_empty_row)
                        one_below = first_empty_row  - row_index == 1
                        # TODO: make the append black list method like the sequence method
                        if one_below and not (first_empty_row, empty_cell_column) in self.black_list:
                            self.black_list.append((first_empty_row, empty_cell_column))

        # win in sequence
        for i in range(NUMBER_OF_ROWS - 3):
            row_index = NUMBER_OF_ROWS - (i + 1)
            print("checking winner on sequence, row: ", row_index)
            for j in range(NUMBER_OF_COLUMNS):
                if game.legal_index(row_index - 3, j + 3):
                    up_right_sequence = game.get_sequence(row_index, j, -1, 1)
                    up_right = self.__can_win_in_row(up_right_sequence, player)
                    if up_right:
                        final_row_index = row_index - up_right_sequence.index(EMPTY_SLOT)
                        final_column_index = j + up_right_sequence.index(EMPTY_SLOT)
                        print("uR final row index:", final_row_index, "final column index", final_column_index)
                        if game.can_place_piece(final_row_index, final_column_index):
                            return final_column_index
                        else:
                            not_in_BL = not (final_row_index + 1, final_column_index) in self.black_list
                            if game.legal_index(final_row_index + 1, final_column_index) and not_in_BL:
                                self.black_list.append((final_row_index + 1, final_column_index))
                                print("black list :", (final_row_index + 1, final_column_index))
                if game.legal_index(row_index - 3, j - 3):
                    up_left_sequence = game.get_sequence(row_index, j, -1, -1)
                    up_left = self.__can_win_in_row(up_left_sequence, player)
                    if up_left:
                        final_row_index = row_index - up_left_sequence.index(EMPTY_SLOT)
                        final_column_index = j - up_left_sequence.index(EMPTY_SLOT)
                        print("uL final row index:", final_row_index, "final column index", final_column_index)
                        if game.can_place_piece(final_row_index, final_column_index):
                            return final_column_index
                        else:
                            not_in_BL = not (final_row_index + 1, final_column_index) in self.black_list
                            if game.legal_index(final_row_index + 1, final_column_index) and not_in_BL:
                                self.black_list.append((final_row_index + 1, final_column_index))
                                print("black list :", (final_row_index + 1, final_column_index))
        return -1

    @staticmethod
    def __can_win_in_row(row, player):
        """get a row and player, returns True if there is a spot for given player to place piece and win.
        if cant win returns False.
        note that the row must be 4 cells long.
        """
        pieces_count = 0
        for i in range(4):
            if row[i] == player:
                pieces_count += 1
            elif row[i] != EMPTY_SLOT: #found enemy piece
                return False
        three_pieces_one_empty = pieces_count == 3 # [x, x, " ", x] for example, can win
        return three_pieces_one_empty


    def column_index_for_trap(game, player):
        for i in range(NUMBER_OF_ROWS):
            row_index = NUMBER_OF_ROWS - (i + 1)
            pieces_count = 0
            for column_index in range(NUMBER_OF_COLUMNS - 4): # checks for each piece the four pieces ahead of him
                pass


    # def trap_in_row(row, player):
    #   tow_together = False
    #   empty_slots = []
    #    for i in range(5):
    #        if row[i] == EMPTY_SLOT:
    #            emp


class EasyBot(Bot):

    def __init__(self, game):
        super().__init__(game)

    def do_turn(self, game, gui):
        print("check if i can win:")
        # I can win
        best_column = self.column_to_win(game, game.player)
        if best_column != -1:  # there is a column to win
            row = game.available_slot(best_column)
            print("best column: ", best_column, "row:", row)
            game.place(game.player, row, best_column, gui)
            return None

        print("""-----------------------------------------------
        check if enemy can win:""")
        # enemy can win
        enemy_best_column = self.column_to_win(game, game.enemy)
        if enemy_best_column != -1:  # there is a column for enemy to win
            row = game.available_slot(enemy_best_column)
            print("enemy best column: ", enemy_best_column, "row:", row)
            game.place(game.player, row, enemy_best_column, gui)
            return None

        print("black list:", self.black_list)

        # check if i can trap

        column = random.randint(0, 6)
        print('column', column)
        row = game.available_slot(column)
        in_black_list = (row, column) in self.black_list
        while row == None or in_black_list:
            column = random.randint(0, 6)
            print('column', column)
            row = game.available_slot(column)
            print('black list', self.black_list)
            in_black_list = (row, column) in self.black_list

        print(f'row: {row} column: {column}')
        game.place(game.player, row, column, gui)
