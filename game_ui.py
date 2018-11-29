from game_mechanics import GAME

def print_board(board:list):
    '''takes current board prints board'''
    for rows in range(len(board[0])):
        print('|', end = '')
        for columns in range(len(board)):
            print(board[columns][rows], end = '')
        print('|')
    print(' ', end = '')
    for columns in range(len(board)):
        print('---', end = '')
    print(' ',end = '')
    print()
    
def input_size(identifier:str) -> int:
    '''returns valid input for rows/columns'''
    while True:
        num = input().strip()
        '''identifier determines the minimum based on if it was rows or columns'''
        if identifier == 'rows':
            minimum = 4
        else:
            minimum = 3
        try:
            if int(num) >= minimum:
                break
            else:
                print('Invalid')
        except (TypeError, ValueError):
            print('Invalid Input')
    return int(num)

def input_field(game:object, rows:int, columns:int):
    '''Checks Empty or Contents before doing actions'''
    while True:
        field = input().strip().upper()
        if field == 'EMPTY':
            break
        elif field == 'CONTENTS':
            game.board_custom(input_contents(rows, columns))
            game.board_dropall()
            break
        else:
            print('Input must be EMPTY or CONTENTS')
            pass

def input_contents(rows:int, columns:int) -> str:
    '''validates inputted content, returning string of the field'''
    content = ''
    valid_input = ['S','T','V','W','X','Y','Z',' ']
    for row in range(rows):
        while True:
            invalid_input = 0
            line = input().upper()
            if len(line) == columns:
                for character in line:
                    if character in valid_input:
                        pass
                    else:
                        invalid_input = 1
                        print('Try again for Row ' + str(row + 1))
                        break
                if invalid_input == 0:
                    content += (line + '\n')
                    break
            else:
                print('Try again for Row ' + str(row + 1))
    return content[:-1]

def input_faller(move: str, columns:int) -> bool:
    valid_input = ['S','T','V','W','X','Y','Z']
    move = move[2:].split()
    if len(move) == 4:
        if move[0].isdigit():
            if 1 <= int(move[0]) <= columns:
                for letter in range(1, len(move)):
                    if move[letter] not in valid_input:
                        return False
                    else:
                        return True

def run(game:object, rows:int, columns:int):
    while True:
        '''If the Board matches, match it, print it, then erase, else just print'''
        if game.board_match():
            print_board(game.board)
            game.board_erase()
        else:
            print_board(game.board)
        '''Checks Game Over, breaks and exits if it is'''
        if game.board_game_over():
            print('GAME OVER')
            break
        '''Commands/Actions'''
        move = input().strip().upper()
        if move[:1] == 'F':
            if not game.faller_exists():
                if input_faller(move,columns):
                    game.faller_create(move[2:].split())
        else:
            move = move.strip()
            if move == 'Q':
                break
            elif move == 'R':
                if game.faller_exists():
                    game.faller_rotate()
            elif move == '<':
                if game.faller_exists():
                    game.faller_move(-1)
            elif move == '>':
                if game.faller_exists():
                    game.faller_move(1)
            elif move == '':
                if game.faller_exists():
                    game.board_tick()
            else:
                pass
        
if __name__ == '__main__':
    rows = input_size('rows')
    columns = input_size('columns')
    game = GAME(rows, columns)
    input_field(game,rows,columns)
    run(game,rows,columns)
    











        
    
        

