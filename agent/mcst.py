import STcpClient_1 as STcpClient
import numpy as np
import random
import copy




def getLegalSteps(mapStat):
    freeRegion = [(i, j) for i in range(12) for j in range(12) if mapStat[i][j] == 0]
    steps = [[pos,1,1] for pos in freeRegion]
    for (x,y) in freeRegion:
        for d in range(1,7):
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



# The UCT algorithm balances exploration and exploitation in the tree search
def UCT(node):
    if node.n == 0:
        return float('inf')
    return node.w / node.n + 1.414 * np.sqrt(np.log(node.parent.n) / node.n)

class Node:
    def __init__(self,mapStat,player = 1,parent = None, step = None):
        self.mapStat = mapStat
        self.parent = parent
        self.player = player
        self.step = step
        self.children = []
        self.n = 0
        self.w = 0
    
    def game_over(self,mapStat):
        if len(getLegalSteps(mapStat))==0:
            return True
        else:
            return False

    def expand(self,mapStat):
        if self.game_over(mapStat):
            return
        steps = getLegalSteps(mapStat)
        for move in steps:
            mapStatCopy = copy.deepcopy(mapStat)
            child_mapStat = applyStep(mapStatCopy, move)
            chlid_node = Node(child_mapStat,3-self.player,self,move)
            self.children.append(chlid_node)

    def select(self):
        node = self
        while node.children:
            # Select the best child node based on the UCT formula
            node = max(node.children, key=UCT)
        # Otherwise, return the best child based on the UCT formula
        return node
    
    def update(self, result):
        self.n += 1
        self.w += result

    def rollout(self,mapStat,player):
        if self.game_over(mapStat):
            return
        mapStatCopy = copy.deepcopy(mapStat)
        steps = getLegalSteps(mapStatCopy)
        if len(getLegalSteps(mapStatCopy))==1:
            if player == 1:
                return False
            elif player == 2:
                return True
        step = random.choice(steps)
        mapStatCopy = applyStep(mapStatCopy,step)
        result = self.rollout(mapStatCopy,3-player)
        return result

    def backpropagate(self,result):
        node = self
        node.update(result)
        if node.parent:
            node.parent.backpropagate(result)


    def simulate(self,timelimit):
        self.expand(self.mapStat)
        for i in range(timelimit-1):
            node = self.select()
            if node.n == 0:
                result = self.rollout(self.mapStat,self.player)
                if result ==None:
                    break
                node.backpropagate(result)
            else:
                check = self.expand(self.mapStat)
                if check == None:
                    break


        best_node = max(self.children, key=UCT)
        return best_node.step



        

    


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
    
    # step, _score = minimax(mapStat,3,float('-inf'),float('inf'),True)
    mapStatCopy = copy.deepcopy(mapStat)
    root = Node(mapStat = mapStatCopy, player = 1, parent= None ,step= None)
    step = root.simulate(100000000)
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
# mapStat[5][6] = 0
# mapStat[6][5] = 0

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
