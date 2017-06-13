def create_board():
    # place mines
    # count adjacent mines
    pass

def get_input():
    # get column and row number
    pass

def update_board(move):
    # if coordinates are a mine, game over
    # elif number, reveal that square only
    # elif blank, reveal adjacent area up to numbers
        # if blank, go out one step in each direction (recursive)
        # if number, clear that space and stop
    pass

def print_board(board):
    # print board with column and row numbers
    # distinguish between revealed and non-revealed squares
    pass

if __name__ == "__main__":
    board = create_board()

    while gameplay == True:
        print_board(board)
        move = get_input()
        board = update_board(move)
