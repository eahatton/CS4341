import board
import alpha_beta_agent

b1 = [[1,1,1],[0,0,0],[0,0,0]]
board1 = board.Board(b1, 3, 3, 3)
aba = alpha_beta_agent.AlphaBetaAgent("aba1",6)

board1.print_it()
print("should have a heuristic of 0 and is ", aba.heuristic(board1))

b2 = [
    [1,0,1,1,2,2,1],
    [0,0,1,2,1,2,0],
    [0,0,0,0,2,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
]
board2 = board.Board(b2,7,6,4)
board2.print_it()
print("Should have a heuristic of 0.9 and is ", aba.heuristic(board2))

print(aba.go(board2))

b3 = [[0] * 7 for i in range(6)]
b3[0][3] = 2
board3 = board.Board(b3,7,6,4)
board3.print_it()
print(aba.go(board3))
