import gui
#final variables
EMPTY_SLOT = ' '
NUMBER_OF_ROWS = 6
NUMBER_OF_COLUMNS= 7
ROW_LENGTH = 7
COLUMN_LENGTH = 6
EMPTY_LINE = [EMPTY_SLOT, EMPTY_SLOT, EMPTY_SLOT, EMPTY_SLOT, EMPTY_SLOT, EMPTY_SLOT, EMPTY_SLOT]



class Game:
    #general checking functions

    def __init__(self):
        self.board = []
        self.player = 'red'
        self.enemy = 'yellow'
        for number in range(NUMBER_OF_ROWS):
            self.board.append(EMPTY_LINE.copy())

    def legal_index(self, x, y):
        """returns true if two given integers are in index range"""
        try:
            self.board[x][y]
        except:
            return False
        return True

    def can_place_piece(self, row, column):
        """gets row index and column index. returns if can place a piece there
        (also checks if it is legal index)"""
        if (not self.legal_index(row, column)):
            return False
        if self.board[row][column] != EMPTY_SLOT:
            return False
        if row != NUMBER_OF_ROWS - 1: # not the bottom row
            has_piece_below = self.board[row + 1][column] != EMPTY_SLOT
            if (not has_piece_below):
                return  False
        return True

    @staticmethod
    def is_number(value):
        """
        get a value and return true if the value is a int or can be convert into a int:
        """
        try:
            int(value)
        except ValueError:
            return False
        return True


    # general functions
    def available_slot(self, column_index):
        """
        gets a column index (int) and returns the row index of the first empty slot in this column
        if theres no empty slot, returns None
        """
        for i in range(NUMBER_OF_ROWS):
            row_index = NUMBER_OF_ROWS - 1 - i # returns first the bottom slot. that's how the game works
            if self.board[row_index][column_index] == EMPTY_SLOT:
                return row_index


    def place(self, piece, row, column, gui):
        """gets str piece, int row, int column and place it on the board"""
        self.board[row][column] = piece
        gui.draw_piece(self.player, column , row)


    def switch_players(self):
        """switches the players """
        if self.player == 'red':
            self.player = 'yellow'
            self.enemy = 'red'
        elif self.player == 'yellow':
            self.player = 'red'
            self.enemy = 'yellow'


    def print_board(self):
        """prints the board"""
        for i in range(NUMBER_OF_ROWS): # running in the rows
            for y in range(NUMBER_OF_COLUMNS):# running in the columns
                if y != ROW_LENGTH - 1: # checks it isn't the last piece in the row
                    print(self.board[i][y][0], end = '|')
                else:
                    print(self.board[i][y][0])

    def reset_board(self):
        """rests the board to have only empty spaces"""
        for row in self.board:
            for index in range(ROW_LENGTH):
                row[index] = EMPTY_SLOT



    # win checking functions
    def who_won(self):
        """returns the winner. if theres no winner returns None"""

        # this for checks all the rows for winner
        for row in self.board:
            winner = self.__four_in_list(row)
            if winner:
                return winner

        # this for checks all the columns for winner
        for number in range(len(self.board[0])): # take a normal length of a column
            current_column = []
            for row in self.board:
                current_column.append(row[number])
            winner = self.__four_in_list(current_column)
            if winner:
                return winner

        #this for checks all the possible sequence for winner
        for row_index in range(NUMBER_OF_ROWS):
            for column_index in range(NUMBER_OF_COLUMNS): #  the length of the row
                if self.__is_winner_on_sequence(row_index, column_index):
                    # print('test 3')
                    return self.board[row_index][column_index]
        return False


    def __four_in_list(self, li):
        """gets a list. if theres four equal values in a row then returns the value. """
        count = 1 # counts himself
        for i in range(len(li) - 1): # -1 because this checks if the current slot is the same as next slot. so theres no need to check the last slot
            if li[i] != EMPTY_SLOT and li[i] == li[i + 1]:
                count += 1
                if count == 4:
                    # print('test test')
                    return li[i]
            else:
                count = 1

    def __is_winner_on_sequence(self, row_index, column_index):
        #FIXME: there is a bug. says win when no
        right_sequence = True
        left_sequence = True
        if self.board[row_index][column_index] == EMPTY_SLOT:
            return False
        for i in range(1,4):
            if right_sequence:
                if not self.legal_index(row_index + i, column_index + i) or self.board[row_index + i][column_index + i] != self.board[row_index][column_index]:
                    right_sequence = False
                print('current: ' , self.board[row_index][column_index], "next one + 1: ",  self.board[row_index][column_index])

            if left_sequence:
                if not self.legal_index(row_index + i, column_index - i) or self.board[row_index + i][column_index - i] != self.board[row_index][column_index]:
                    left_sequence = False
        if right_sequence or left_sequence:
            return True
        return False

    def get_sequence(self, row, column, row_dir, column_dir):
        """gets row index, column index, row direction, column direction"""
        sequence = [self.board[row][column]]
        for i in range(1, 4):
            sequence.append(self.board[row + i * row_dir][column + i * column_dir])
        # print('sequence:', sequence)
        return sequence

    def tie_check(self):
        """ checks for a tie. returns true if its a tie. otherwise else"""
        for row in self.board:
            for piece in row:
                if piece == EMPTY_SLOT:
                    return False
        return True
