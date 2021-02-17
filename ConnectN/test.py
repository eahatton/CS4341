# import board 
# import alpha_beta_agent as aba

# b1 = [[1,1,0],[2,1,0],[0,0,0]]
# board1 = board.Board(b1, 3, 3, 3)
# aba1 = aba.AlphaBetaAgent("aba1",3)


# brd = board1.board
# winNum = 3 
# scoreBrd = {1: 0,
#             2: 0}
# def isLineAtR(moves, cnt, x,y,dx,dy, player):
#     print("cnt: {}".format(cnt))
#     print("moves: {}".format(moves))
#     print(player)
#     if  cnt == winNum-1:
#         scoreBrd[player] = scoreBrd[player] + 10
#         return
#     elif moves == winNum-1:
#         print("left at moves == winNum")
#         scoreBrd[player] = scoreBrd[player] + cnt/winNum
#         return
#     curr = brd[y][x]
#     if curr == player:
#         cnt +=1
#     # print("curr: {}".format(curr))
#     nX = x+dx
#     nY = y+dy
#     try:
#         brd[nY][nX]
#     except:
#         print("left at no next block")
#         if cnt > 1:
#             scoreBrd[player] = scoreBrd[player] + cnt/winNum
#         return

#     if curr == 0:
#         moves+=1
#         return isLineAtR(moves, cnt,nX,nY,dx,dy, player)
#     elif curr != player:
#         return
#     else:
#         moves +=1
#         return isLineAtR(moves, cnt,nX,nY,dx,dy, player)

# def isLineAt(y,x,dx,dy):
#     try:
#         brd[y+(dx*(winNum-1))][x+(dx*(winNum-1))]
#     except:
#         return
#     if brd[y][x] != 0:
#         return isLineAtR(0, 0, x,y,dx,dy, brd[y][x])

# def isAnyLineAt(y,x):
#     isLineAt(y,x,1,0)
#     isLineAt(y,x,1,1)
#     isLineAt(y,x,1,-1) 
#     isLineAt(y,x,0,1)

# # for y in range(board1.h):
# #     for x in range(board1.w):
# #         print(brd[y][x])
# #         isAnyLineAt(y,x)
# #         print(scoreBrd)

# # print(scoreBrd)

# # isLineAt(0,1,1,0)
# # print(scoreBrd)

# # for y in range(board1.h):
# #     print()
# #     for x in range(board1.w):
# #         print(brd[y][x], end='')



# def checkState(x,y,dx,dy):
#     state = brd[y][x]
#     if state == 0:
#         return
#     # print("Starting at X:{0} Y:{1}".format(dx,dy))
#     cnt = 0
#     for i in range(winNum):
#         # print("x: {0} y:{1}".format(x+(dx*i),y+(dy*i)))
#         nY = y +(dy*i)
#         nX = x +(dx*i)
#         if(nY >= 0 and nX >= 0):
#             if brd[nY][nX] == state:
#                 cnt += 1
#             elif brd[nY][nX] == 0:
#                 continue
#             else:
#                 return
#         else:
#             return
#     if cnt == winNum-1:
#         scoreBrd[state] = scoreBrd[state] + 10
#     else:
#         scoreBrd[state] = scoreBrd[state] + cnt/winNum

# def checkDirection(x,y,dx,dy):
#     try:
#         brd[y + (dy*(winNum-1))][x + (dx*(winNum-1))]
#     except:
#         # print("couldn't get there")
#         return
#     checkState(x,y,dx,dy)    

# def checkAllDirections(x,y):
#     checkDirection(x,y,1,0)
#     checkDirection(x,y,1,1)
#     checkDirection(x,y,0,1)
#     checkDirection(x,y,1,-1)


# # checkAllDirections(0,0)
# # print(scoreBrd)

# for y in range(board1.h):
#     for x in range(board1.w):
#         #print(brd[y][x])
#         checkAllDirections(y,x)
#         #print(scoreBrd)

# print(scoreBrd)