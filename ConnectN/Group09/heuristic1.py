import math


def heuristic1(aba, brd):
    value = 0
    for i in range(brd.h):
        for j in range(brd.w):
            value += check_line(aba, brd, i, j, 1, 0)
            value += check_line(aba, brd, i, j, 1, 1)
            value += check_line(aba, brd, i, j, 0, 1)
            value += check_line(aba, brd, i, j, 1, -1)
    return value


def check_line(aba, brd, i, j, dx, dy):
    count = 0
    player = brd.board[i][j]
    other = False
    for c in range(0, brd.n):
        if not other:
            cx = j + c * dx
            cy = i + c * dy
            # dump out of this line check we went out of bounds
            if cx < 0 or cx >= brd.w or cy < 0 or cy >= brd.h:
                other = True
                count = 0
            # Same piece or we haven't seen any pieces
            elif brd.board[cy][cx] == player or player == 0:
                if player == 0:
                    player = brd.board[cy][cx]
                if player != 0 and brd.board[cy][cx] == player:
                    count += 1
            # Dump out of this line check we found a different piece
            elif brd.board[cy][cx] != player and brd.board[cy][cx] != 0:
                other = True
                count = 0
    if player != 0:
        # count will be 0,1,3,9,27,81... for count = 0,1,2,3,4,5...
        count = math.floor(3 ** (count - 1))
        # if the count was done on the opponent negate it
        if player != aba.player:
            count *= -1
    else:
        count = 0
    return count
