import math 

def h(board, player):
    def direction(x,y):
        # direzione : forward o backward 
        # x->y
        if x[0] == y[0]:
            return 1
        if x[0] > y[0]:
            # forward per X ma backward per O
            # y             X backward
            # x             O forward
            return -1 if board[x]=='x' or board[x]=='K' else +1
        # backward per X ma forward per O
        # x             X forward
        # y             O backward
        return +1 if board[x]=='x' or board[x]=='K' else -1
    
    def possibleMove(x,y):
        def minDistance(x,y,z):
            return y if distance(y,z)<distance(x,z) else x
        
        d=direction(x,y)
        # print(x,y,d)
        if x == myKing or x == opponentKing:
            return 1
        else:
            if d > 0 and x[0] == y[0]:
                (r,c)=x
                s=symbols[board[minDistance((r,c-2),(r,c+2),y)]]
                if abs(s)>0 and s != symbols[board[x]]:
                    return 1
            elif d > 0:
                # forward
                return 1
            else:
                # backward
                (r,c)=x
                if board[x] == 'x':
                    # direzioni (r-1,c-1),(r-1,c+1),(r-2,c)
                    tmp=minDistance((r-1,c-1),(r-1,c+1),y)
                    s=symbols[board[minDistance(tmp,(r-2,c),y)]]
                    if abs(s)>0 and s != symbols[board[x]]:
                        return 1
                else:
                    # direzioni (r+2,c),(r+1,c+1),(r+1,c-1)
                    tmp=minDistance((r+2,c),(r+1,c+1),y)
                    s=symbols[board[minDistance(tmp,(r+1,c-1),y)]]
                    if abs(s)>0 and s != symbols[board[x]]:
                        return 1
        return 0
            
    def eval(x):
        if board[x] == board.off: return 0
        squares = possiblesquares(x)
        density = 0
        zeros=0
        for square in squares:
            zeros+=1 if symbols[board[square]]==0 else 0

            if board[square] == board.empty:
                if x==opponentKing:
                    density+=symbols[board[opponentKing]] if possibleMove(opponentKing,square)>0 else symbols[board[myKing]]
                elif x==myKing:
                    density+=symbols[board[square]] if possibleMove(myKing,square)>0 else symbols[board[myKing]]
            else:
                if x==myKing or x==opponentKing:
                    if symbols[board[x]] == symbols[board[square]]:
                        # behind myKing
                        density+= 0 if direction(square,x)>0 else symbols[board[square]]
                    else:
                        density+= 8*symbols[board[square]]
                else:
                    density+=symbols[board[square]]
        
        if x == opponentKing:  
            # distanceOppKingtoGoal == distance(x,opponentGoal)
            if density==0:
                return -1/distanceOppKingtoGoal if zeros==8 else +5/distanceOppKingtoGoal
            return density/distanceOppKingtoGoal
        
        if x == myKing:
            # distanceMyKingtoGoal == distance(x,myGoal)
            if density==0:
                return +1/distanceMyKingtoGoal if zeros==8 else -8/distanceMyKingtoGoal
            return density/distanceMyKingtoGoal
        
        if density==0 and zeros==8:
            if symbols[board[x]] == symbols[board[myKing]]:
                return symbols[board[x]] if direction(x,opponentKing)>0 else 0
            else:
                return symbols[board[x]] if direction(x,myKing)>0 else symbols[board[myKing]]
        
        distances=distance(x,myKing)*distance(x,opponentKing)
        return density/distances if density!=0 else symbols[board[x]]/distances

    def compareDistance():
        if distanceMyKingtoGoal < distanceOppKingtoGoal:
            return +1/distanceMyKingtoGoal
        if distanceMyKingtoGoal > distanceOppKingtoGoal: 
            return -1/distanceOppKingtoGoal
        return 0
    
    if player=='X':
        myGoal=(14,7) 
        opponentGoal=(0,7)
        symbols={'o':-1,'Q':-1,'x':1,'K':1,'#':0,' ':0}
    else:
        myGoal=(0,7)
        opponentGoal=(14,7)
        symbols={'o':1,'Q':1,'x':-1,'K':-1,'#':0,' ':0}

    def distance(x,y):
        return euclideanDistance(x,y) if x!=y else 0.00001
    
    myKing=(-1,-1)
    opponentKing=(-1,-1)

    globalDensity=0
    for (r,c) in board:
        if board[(r,c)] == 'K':
            if player == 'X':
                myKing=(r,c)
            else:
                opponentKing=(r,c)
        elif board[(r,c)] == 'Q': 
            if player == 'X':
                opponentKing=(r,c)
            else:
                myKing=(r,c)
        globalDensity+=symbols[board[(r,c)]] if (r,c)!=myKing or (r,c)!=opponentKing else 16*symbols[board[(r,c)]]

    distanceMyKingtoGoal=distance(myKing,myGoal)
    distanceOppKingtoGoal=distance(opponentKing,opponentGoal)

    defensive=0
    (r,c)=myKing
    for i in range(1,3):
        if player=='O':
            defensive+=eval((r-i,c-i)) if board[(r-i,c-i)] != symbols[board[myKing]] else 0
            defensive+=eval((r-i,c+i)) if board[(r-i,c+i)] != symbols[board[myKing]] else 0
            defensive+=eval((r-2*i,c)) if board[(r-2*i,c)] != symbols[board[myKing]] else 0
        else:
            defensive+=eval((r+i,c-i)) if board[(r+i,c-i)] != symbols[board[myKing]] else 0
            defensive+=eval((r+i,c+i)) if board[(r+i,c+i)] != symbols[board[myKing]] else 0
            defensive+=eval((r+2*i,c)) if board[(r+2*i,c)] != symbols[board[myKing]] else 0
        defensive+=eval((r,c-2*i)) if board[(r,c-2*i)] != symbols[board[myKing]] else 0
        defensive+=eval((r,c+2*i)) if board[(r,c+2*i)] != symbols[board[myKing]] else 0

    offensive=0
    (r,c)=opponentKing
    for i in range(1,3):
        if player=='X':
            offensive+=eval((r-2*i,c)) #if board[(r-2*i,c)] != symbols[board[opponentKing]] else 0
            offensive+=eval((r-i,c-i)) #if board[(r-i,c-i)] != symbols[board[opponentKing]] else 0
            offensive+=eval((r-i,c+i)) #if board[(r-i,c+i)] != symbols[board[opponentKing]] else 0
        else:
            offensive+=eval((r+2*i,c)) #if board[(r+2*i,c)] != symbols[board[opponentKing]] else 0
            offensive+=eval((r+i,c-i)) #if board[(r+i,c-i)] != symbols[board[opponentKing]] else 0
            offensive+=eval((r+i,c+i)) #if board[(r+i,c+i)] != symbols[board[opponentKing]] else 0
        offensive+=eval((r,c-2*i)) #if board[(r,c-2*i)] != symbols[board[opponentKing]] else 0
        offensive+=eval((r,c+2*i)) #if board[(r,c+2*i)] != symbols[board[opponentKing]] else 0

    w1=50
    # eval(opponentKing)
    w2=75
    # eval(myKing)
    w3=45
    # defensive
    w4=35
    # offensive
    w5=80
    # globalDensity
    w6=100
    # compareDistance()

    f = lambda x : x/10000

    return f(w1*eval(opponentKing)+w2*eval(myKing)+w3*defensive+w4*offensive+w5*globalDensity+w6*compareDistance())

def possiblesquares(x):
    return [(x[0]-1,x[1]-1),(x[0]-1,x[1]+1),(x[0]-2,x[1]),(x[0]+2,x[1]),(x[0]+1,x[1]+1),(x[0]+1,x[1]-1),(x[0],x[1]-2),(x[0],x[1]+2)]

def manhattanDistance(x, y):
    return abs(x[0]-y[0]) + abs(x[1]-y[1])

def euclideanDistance(x, y):
    return math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)





