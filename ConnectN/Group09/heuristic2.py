def checkState(aba, x, y, dx, dy):
    state = aba.board[y][x]
    if state == 0:
        for i in range(aba.n):
            nY = y + (dy * i)
            nX = x + (dx * i)
            if aba.board[nY][nX] != 0:
                state = aba.board[nY][nX]
                break
    if state == 0:
        return
    cnt = 0
    for i in range(aba.n):
        nY = y + (dy * i)
        nX = x + (dx * i)
        if (nY >= 0 and nX >= 0):
            if aba.board[nY][nX] == state:
                cnt += 1
            elif aba.board[nY][nX] == 0:
                continue
            else:
                return
        else:
            return
    if cnt == aba.n:
        aba.scoreBrd[state] = aba.scoreBrd[state] + 5
    else:
        aba.scoreBrd[state] = aba.scoreBrd[state] + cnt / aba.n


def checkDirection(aba, x, y, dx, dy):
    try:
        aba.board[y + (dy * (aba.n - 1))][x + (dx * (aba.n - 1))]
    except:
        return
    checkState(aba, x, y, dx, dy)


def checkAllDirections(aba, x, y):
    checkDirection(aba, x, y, 1, 0)
    checkDirection(aba, x, y, 1, 1)
    checkDirection(aba, x, y, 0, 1)
    checkDirection(aba, x, y, 1, -1)


# Calculates the heuristic of the brd
#
# Returns the heuristic value
def heuristic2(aba, brd):
    """Calculate the heuristic of the board"""
    aba.board = brd.board
    aba.n = brd.n
    aba.scoreBrd = {1: 0, 2: 0}
    for y in range(brd.h):
        for x in range(brd.w):
            checkAllDirections(aba, x, y)
    if aba.player == 1:
        return aba.scoreBrd[1] - aba.scoreBrd[2]
    else:
        return aba.scoreBrd[2] - aba.scoreBrd[1]
