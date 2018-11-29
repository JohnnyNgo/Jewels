
class GAME:
    
    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self.board = self._board_new()
        self._faller = [] #[faller_col_num,top,middle,bottom,faller_row_num]
        self._temp = []

    def _board_new(self) -> [[str]]:
        '''Creates new board using rows and columns'''
        board = []
        for col in range(self._columns):
            board.append([])
            for row in range(self._rows):
                board[-1].append('   ')
        return board

    def _board_copy(self, board: [[str]]) -> [[str]]:
        '''Copies the given game board'''
        board_copy = []

        for col in range(self._columns):
            board_copy.append([])
            for row in range(self._rows):
                board_copy[-1].append(board[col][row])     
        return board_copy
        
    def board_custom(self, custom_board:str):
        '''Creates a Board according to your input'''
        custom_board = custom_board.split('\n')
        for columns in range(self._columns):
            for rows in range(self._rows):
                self.board[columns][rows] = " " + custom_board[rows][columns] + " "

    def board_dropall(self):
        '''Drops all the pieces to it's lowest position via recursion.
        If count is 0, there are no more pieces to dropped'''
        for column in range(self._columns):
            for row in range(self._rows - 1, 0, -1):
                if self.board[column][row] == '   ':
                    if self.board[column][row - 1] != '   ':
                        self.board[column][row] = self.board[column][row - 1]
                        self.board[column][row - 1] = '   '
                        self.board_dropall()
                        break

    def board_tick(self):
        '''Passage of Time'''
        start_row = self._find_bottom_empty_row_in_column(self._faller[0])
        faller_row = self._faller[4]
        '''Checks if there is a space between the Faller and the Frozen Blocks / Floor'''
        if self._faller_active() < 3 and start_row == -1:
            if len(self._temp) != 4:
                self.board_postpone_check()
        elif faller_row < start_row:
            self._faller_tick()
            self._faller_check_landed()
        else:
            self._faller_change(' ')
            
    def board_postpone_check(self) -> bool:
        '''Creates a new board showing the Hidden Faller and Freezes It'''
        new_board = self._board_copy(self.board)
        original_board = self._board_copy(self.board)
        faller_copy = self._faller
        for i in range(self._faller_active(), 3):
            for col in range(self._columns):
                new_board[col].insert(0, '   ')
            new_board[self._faller[0]][0] = self._faller[3 - i]
        '''Stores information into self._temp to check for match'''
        self._faller_change(' ')
        self._temp = [new_board, len(new_board[0]), self._rows, self._faller_active()]
        
    def board_match(self):
        '''Matches board, changing all the matched letters to *'''
        '''If the match is outside, expand the board and match it'''
        if len(self._temp) == 4:
            original_board = self.board
            self.board = self._temp[0]
            self._rows = self._temp[1]
            self._faller_change(' ')
        '''This checks and replaces anything that matches to *LETTER*'''
        new_board = self._board_copy(self.board)
        new_board = self._board_match_change(new_board,1,0,0)
        new_board = self._board_match_change(new_board,0,1,0)
        new_board = self._board_match_change(new_board,1,1,0)
        new_board = self._board_match_change(new_board,1,1,2)
        '''If the board does not match, return False (and revert the expanded board)'''
        if self.board == new_board:
            if len(self._temp) == 4:
                self.board = original_board
                self._rows = self._temp[2]
                self._faller = [0,'   ','   ','   ',0]
            return False
        '''If it did match, set it equal to the matched board'''
        self.board = new_board
        '''and If it was expanded, store the expanded version into the temp and revert the board, returning True'''
        if len(self._temp) == 4:
            self._temp[0] = self._board_copy(new_board)
            for row in range(self._temp[3], 3):
                for col in range(self._columns):
                    del self.board[col][0]
            self._rows = self._temp[2]
        return True
        
    def _board_match_change(self, board:[[str]], col_del: int,row_del: int, reverse: int) -> [[str]]:
        '''Cases for Diag/Vertical/Horizontal matching'''
        new_board = self._board_copy(board)
        for col in range(col_del, self._columns - col_del):
            for row in range(row_del, self._rows - row_del):
                if (self.board[col][row] == self.board[col - col_del][row - row_del + reverse] and
                    self.board[col][row] == self.board[col + col_del][row + row_del - reverse] and
                    self.board[col][row] != '   ' and
                    '[' not in self.board[col][row] and
                    '|' not in self.board[col][row]):
                    new_board[col][row] = "*" + self.board[col][row][1] + "*"
                    new_board[col - col_del][row - row_del + reverse] = "*" + self.board[col][row][1] + "*"
                    new_board[col + col_del][row + row_del - reverse] = "*" + self.board[col][row][1] + "*"
        return new_board
    
    def board_erase(self):
        '''Erases all Letters with *_* and drops all'''
        '''If the board was expanded, use self._temp board instead'''
        if len(self._temp) == 4:
            self._rows = self._temp[1]
            self.board = self._board_copy(self._temp[0])
        new_board = self._board_copy(self.board)
        for col in range(self._columns):
            for row in range(self._rows):
                if '*' in self.board[col][row]:
                    new_board[col][row] = '   '
        '''Board with Holes are dropped here'''
        self.board = new_board
        self.board_dropall()
        '''If expanded, revert back to original board and clear self._temp'''
        if len(self._temp) == 4:
            repeat = 0
            for row in range(0, 3 - self._temp[3]):
                for col in range(self._columns):
                    if self.board[col][row] != '   ':
                        repeat = 1
            if repeat == 1:
                self._temp[0] = self._board_copy(self.board)
            for row in range(self._temp[3], 3):
                for col in range(self._columns):
                    del self.board[col][0]
            self._rows = self._temp[2]
            if repeat == 0:
                self._faller = []
                self._temp = []
    def board_game_over(self) -> bool:
        '''If Board is Filled or Faller is still not present after matching, Game Ends'''
        if self.faller_exists():
            if self._faller[3] == '   ':
                return True
            if len(self._temp) == 4:
                return False
            start_row = self._find_bottom_empty_row_in_column(self._faller[0])
            if self._faller_active() < 3 and start_row == -1:
                if ' ' in self.board[self._faller[0]][self._faller[4]]:
                    return True
        for col in range(self._columns):
            if (self.board[col][0] == '   ' or
                '[' in self.board[col][0] or
                '|' in self.board[col][0]):
                return False
        return True

    def faller_create(self, faller:list):
        '''Creates the Faller'''
        self._faller = [      (int(faller[0])-1)     ,
                        '[' + faller[1].upper() + ']',
                        '[' + faller[2].upper() + ']',
                        '[' + faller[3].upper() + ']',
                        0
                       ]
        empty_row = self._find_bottom_empty_row_in_column(self._faller[0])
        if empty_row == -1:
            self._faller[4] = -1
            self.board_postpone_check()
        else:
            self.board[self._faller[0]][0] = self._faller[3]
            self._faller_check_landed()

    def faller_rotate(self):
        '''Determines how many faller blocks are on the board and rotates it'''
        faller_copy = [self._faller[0], self._faller[3],self._faller[1],self._faller[2],self._faller[4]]
        faller_present = self._faller_active()
        for i in range(faller_present):
                self.board[self._faller[0]][self._faller[4] - i] = faller_copy[3 - i]
        self._faller = faller_copy
        self._faller_check_landed()

    def faller_move(self, direction:int):
        '''Validates if faller can move in the specified direction and moves it if True'''
        if self._is_valid_column_number(self._faller[0] + direction):
            empty_neighbor_row = self._find_bottom_empty_row_in_column(self._faller[0] + direction)
            if empty_neighbor_row >= self._faller[4]:
                for i in range(self._faller_active()):
                    self.board[self._faller[0] + direction][self._faller[4] - i] = self._faller[3 - i]
                    self.board[self._faller[0]][self._faller[4] - i] = '   '
                self._faller[0] += direction
        self._faller_check_landed()

    def _faller_tick(self):
        '''Moves Faller down one space'''
        for i in range(self._faller_active()):
            self.board[self._faller[0]][self._faller[4] - i + 1] = self._faller[3 - i]
            self.board[self._faller[0]][self._faller[4] - i] = '   '
        '''If not all three Faller blocks are present on the board, then create the upcoming block'''
        if self._faller_active() < 3:
            for i in range(self._faller_active()):
                self.board[self._faller[0]][self._faller[4] - i] = self._faller[2 - i]
        '''Faller Row moves down by 1'''
        self._faller[4] += 1

    def _faller_change(self, x:str):
        '''Lands/Freezes the Faller depending on what x is'''
        '''Copies the given game board and resets Faller'''
        new_board = self._board_copy(self.board)
        for col in range(self._columns):
            for row in range(self._rows):
                if '[' in self.board[col][row] or '|' in self.board[col][row]:
                    letter = x + self.board[col][row][1] + x
                    new_board[col][row] = letter
        self.board = new_board
        if x == ' ':
            '''If Frozen and Present, delete current Faller'''
            if self._faller_active() == 3 and self._faller[4] >= 0:
                self._faller = []

    def faller_exists(self) -> bool:
        '''Checks if there is a Faller created and not yet Frozen'''
        for column in range(self._columns):
            for row in range(self._rows):
                if len(self._faller) == 5:
                    '''If there is a Faller, return True'''
                    return True
        return False
            
    def _faller_active(self) -> int:
        '''Returns the number of Faller blocks that are currently in the board'''
        faller_present = 0
        if self._faller[4] == 0:
            faller_present = 1
        elif self._faller[4] == 1:
            faller_present = 2
        elif self._faller[4] > 1:
            faller_present = 3
        return faller_present

    def _faller_check_landed(self):
        if self._faller[4] >= self._find_bottom_empty_row_in_column(self._faller[0]):
            self._faller_change('|')
    
    def _find_bottom_empty_row_in_column(self, column_number: int) -> int:
        '''Determines the bottommost empty row within a given column.
        If the entire column in filled with pieces, this function returns -1'''
        for i in range(self._rows - 1, -1, -1):
            if self.board[column_number][i] == '   ':
                return i
        return -1

    def _is_valid_column_number(self, column_number: int) -> bool:
        '''Returns True if the given column number is valid; returns False otherwise'''
        return 0 <= column_number < self._columns
