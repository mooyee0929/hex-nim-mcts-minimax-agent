import STcpClient_1 as STcpClient
import numpy as np
import random
import copy


def minimax(mapStat, depth, alpha, beta, maximizingPlayer):
    if len(checkRemainMove(mapStat))==1:
        if maximizingPlayer :
            return getLegalSteps(mapStat)[0], float('-inf')
        else:
            return getLegalSteps(mapStat)[0], float('inf')
    if depth == 0:
        if maximizingPlayer :
            return random.choice(getLegalSteps(mapStat)), 0
        else:
            return random.choice(getLegalSteps(mapStat)), 0
    if maximizingPlayer:
        bestScore = float('-inf')
        steplist = getLegalSteps(mapStat)
        bestStep = steplist[0]
        for step in steplist:
            mapStatCopy = copy.deepcopy(mapStat)
            mapStatCopy = applyStep(mapStatCopy, step)
            _, score = minimax(mapStatCopy, depth - 1, alpha, beta, False)
            if score > bestScore:
                bestScore = score
                bestStep = step
            alpha = max(alpha, bestScore)
            if alpha >= beta:
                break
        return bestStep, bestScore
    else:
        bestScore = float('inf')
        steplist = getLegalSteps(mapStat)
        bestStep = steplist[0]
        for step in steplist:
            mapStatCopy = copy.deepcopy(mapStat)
            mapStatCopy = applyStep(mapStatCopy, step)
            _, score = minimax(mapStatCopy, depth - 1, alpha, beta, True)
            if score < bestScore:
                bestScore = score
                bestStep = step
            beta = min(beta, bestScore)
            if alpha >= beta:
                break
        return bestStep, bestScore

def getLegalSteps(mapStat):
    freeRegion = [(i, j) for i in range(12) for j in range(12) if mapStat[i][j] == 0]
    steps = [[pos,1,1] for pos in freeRegion]
    for (x,y) in freeRegion:
        for d in range(1,4):
            next_x,next_y = x,y
            for l in range(2,4):
                [next_x,next_y] = Next_Node(next_x,next_y,d)
                if(next_x >= 0 and next_x < 12 and next_y >= 0 and next_y < 12 and mapStat[next_x][next_y]==0):
                    steps.append(([x,y],l,d))
                else:
                    break
    return steps

def applyStep(mapStat, step):
    pos, l, d = step
    x, y = pos
    mapStat[x][y] = 1
    for i in range(l-1):
        x, y = Next_Node(x, y, d)
        mapStat[x][y] = 1
    return mapStat

def evaluate(mapStat):
    # Here you can define your evaluation function
    score = 0
    queue = []
    seen = set()
    count = 0
    for i in range(12):
        for j in range(12):
            w = (i,j)
            if mapStat[i][j] == 0 and w not in seen:
                queue.append(w)
                seen.add(w)
            while(len(queue)>0):
                for d in range(1,7):
                    x,y = Next_Node(queue[0][0],queue[0][1],d)
                    if  mapStat[x][y] == 0 and (x,y) not in seen:
                        queue.append((x,y))
                        seen.add((x,y))
                queue.pop()
            count+=1

    score += (1000000/count)

    if(len(checkRemainMove(mapStat))%4==1):
        score += len(checkRemainMove(mapStat))

    return score



'''
    input position (x,y) and direction
    output next node position on this direction
'''
def Next_Node(pos_x,pos_y,direction):
    if pos_y%2==1:
        if direction==1:
            return pos_x,pos_y-1
        elif direction==2:
            return pos_x+1,pos_y-1
        elif direction==3:
            return pos_x-1,pos_y
        elif direction==4:
            return pos_x+1,pos_y
        elif direction==5:
            return pos_x,pos_y+1
        elif direction==6:
            return pos_x+1,pos_y+1
    else:
        if direction==1:
            return pos_x-1,pos_y-1
        elif direction==2:
            return pos_x,pos_y-1
        elif direction==3:
            return pos_x-1,pos_y
        elif direction==4:
            return pos_x+1,pos_y
        elif direction==5:
            return pos_x-1,pos_y+1
        elif direction==6:
            return pos_x,pos_y+1


def checkRemainMove(mapStat):
    free_region = (mapStat == 0)
    temp = []
    for i in range(len(free_region)):
        for j in range(len(free_region[0])):
            if(free_region[i][j] == True):
                temp.append([i,j])
    return temp


'''
    輪到此程式移動棋子
    mapStat : 棋盤狀態(list of list), 為 12*12矩陣, 0=可移動區域, -1=障礙, 1~2為玩家1~2佔領區域
    gameStat : 棋盤歷史順序
    return Step
    Step : 3 elements, [(x,y), l, dir]
            x, y 表示要畫線起始座標
            l = 線條長度(1~3)
            dir = 方向(1~6),對應方向如下圖所示
              1  2
            3  x  4
              5  6
'''
def Getstep(mapStat, gameStat):
    #Please write your code here
    
    step, _score = minimax(mapStat,6,float('-inf'),float('inf'),True)
    #Please write your code here
    return step
    


# mapStat = np.array([[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
#                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
#                     ])
# mapStat[5][5] = 0


# s = Getstep(mapStat,1)
# print(s)

# start game
print('start game')
while (True):

    (end_program, id_package, mapStat, gameStat) = STcpClient.GetBoard()
    if end_program:
        STcpClient._StopConnect()
        break
    
    decision_step = Getstep(mapStat, gameStat)
    
    STcpClient.SendStep(id_package, decision_step)
