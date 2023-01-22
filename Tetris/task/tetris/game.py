# JetBrains Academy - Python Core track
# Tetris project - https://hyperskill.org/projects/147
# Submitted by Chris Freeman - Stage 4/4: I Disappear
# !! needs a major re-write to achieve this stage !!

import numpy as np


# Standard piece definitions on 4x4 grid
std_piece = {'O': [[4, 14, 15, 5], [4, 14, 15, 5], [4, 14, 15, 5], [4, 14, 15, 5]],
             'I': [[4, 14, 24, 34], [3, 4, 5, 6], [4, 14, 24, 34], [3, 4, 5, 6]],
             'S': [[5, 4, 14, 13], [4, 14, 15, 25], [5, 4, 14, 13], [4, 14, 15, 25]],
             'Z': [[4, 5, 15, 16], [5, 15, 14, 24], [4, 5, 15, 16], [5, 15, 14, 24]],
             'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
             'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
             'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]
             }
contact_left = False    # indicate left margin has been reached
contact_right = False   # right margin has been reached
lock_down = False       # piece has reached bottom of board. Freeze in place
board_x = (20, 10)      # game board dimensions - M rows, N cols
moves = ['rotate', 'left', 'right', 'down', 'exit', 'piece', 'break']  # valid moves
rot = 0             # global piece rotation: 0=quadrant-1, 1=quadrant-2 ...


def display(b: np.ndarray):
    """display the current board containing Tetris pieces"""
    for m in range(board_x[0]):
        for n in range(board_x[1] - 1):
            print(f'{b[m][n]}', end=' ')
        print(f'{b[m][n+1]}')
    print()


def place(b: np.ndarray, p: str, rotn: int, yx: tuple, bg: np.ndarray):
    """ Places the 4x10 game piece (p) into the board (b)
    at position (yx) with left-90-rotation (rotn).
    Row/Column coordinates wrap-around the board """
    global contact_left                 # define global flags
    global contact_right
    global lock_down
    m = yx[0]                           # origin row of piece in game board
    n = yx[1]                           # origin col of piece in game board
    px = std_piece[p]                   # rotational list of piece to be placed
    for p_x in range(4):                # step thru piece elements by row and col and
        row = m + (px[rotn][p_x] // 10)  # place selected rotation on board
        col = n + (px[rotn][p_x] % 10)
        b[row][col] = '0'
        if col == 0:
            contact_left = True         # flag left margin contact
        elif col == board_x[1] - 1:
            contact_right = True        # flag right margin contact
        if row == board_x[0]-1 or bg[row+1][col] == '0':
            lock_down = True            # flag bottom margin contact


def get_piece():
    """ input and return a piece name after checking that it exists """
    p = input()                         # get the Tetris piece by Letter
    if p not in std_piece.keys():
        p = 'O'
    return p


def shuffle_down(b_x, r_x):
    """ replace row r with blanks and rotate rows above down one row
    Return the modified array """
    if r_x > 0:
        for r in range(r_x - 1):
            b_x[r_x - r] = b_x[r_x - r - 1]
    for i in range(board_x[1]):
        b_x[0][i] = '-'
    return b_x


def remove_full_rows(b):
    """ find any rows that are fully occupied by parts of pieces
    and remove those rows from the board, collapsing the board down """
    for r in range(board_x[0]):
        r_full = True
        for c in range(board_x[1]):
            if b[r][c] != '0':
                r_full = False
                break
        if r_full:
            b = shuffle_down(b, r)
    return b


def check_game_over(b: np.ndarray):
    for c in range(board_x[1]):
        full_col = True
        for r in range(board_x[0]):
            if b[r, c] == '-':
                full_col = False
                break
        if full_col:
            display(b)
            print('Game Over!')
            return True
    return False


# stage 1 main
board_area = input()            # get board dimensions (20x10)
if board_area != '':
    n_xs, m_xs = board_area.strip().split()  # clean up and separate rows and sols
    m_x = int(m_xs)                     # convert to integers
    n_x = int(n_xs)
    if m_x < 4:                         # minimum rows is 4
        m_x = 4
    if n_x < 10:                        # minimum cols is 10
        n_x = 10
    board_x = (m_x, n_x)                # set new board dimensions
back_board = np.full(board_x, '-')      # build empty game board
board = back_board.copy()
display(board)                          # display the initially blank board
piece = None                            # no piece is selected yet
c_row = c_col = 0                       # set current position

while True:                             # game loop
    if lock_down:                       # lower piece contact has occurred
        back_board = board.copy()       # make it the new background game board
        piece = None                    # remove the piece from play
        c_row = c_col = 0               # reset current position
        rot = 0                         # reset piece rotation
        lock_down = False               # clear the lock_down state
    else:
        move = input().strip().lower()  # get next move
        if check_game_over(back_board):  # check for a full column
            break                       # --- game over!
        if move not in moves:
            continue                    # invalid move... ignore it !
        if piece and move == moves[0]:  # ROTATE
            rot = (rot + 1) % 4         # to next quadrant
            c_row += 1                  # drop down to next row
        elif piece and move == moves[1]:  # LEFT
            if not contact_left:
                c_col -= 1              # move column left without wrap-around
                contact_right = False
            c_row += 1                  # drop down to next row
        elif piece and move == moves[2]:  # RIGHT
            if not contact_right:
                c_col += 1              # move column right without wrap-around
                contact_left = False
            c_row += 1                  # drop down to next row
        elif piece and move == moves[3]:  # DOWN
            c_row += 1                  # drop down to next row
        elif move == moves[4]:          # EXIT
            break                       # time to Break-Out!!
        elif not piece and move == moves[5]:  # PIECE
            piece = get_piece()         # get next Tetris piece
            c_row = 0                   # set current row position at top of board
            c_col = (board_x[1] // 2) - 5  # set column of 4x10 field to board mid-point
            contact_left = contact_right = False  # clear contact flags
            place(board, piece, 0, (c_row, c_col), back_board)  # put piece on board at origin unrotated
        elif not piece and move == moves[6]:  # BREAK
            back_board = remove_full_rows(back_board)
        board = back_board.copy()       # reset game board
        if piece:
            place(board, piece, rot, (c_row, c_col), back_board)  # put piece on board position
        display(board)                  # display board with new piece position
# end - game-over or quit
