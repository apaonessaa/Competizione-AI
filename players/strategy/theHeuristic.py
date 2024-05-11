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
            return -1 if player == 'X' else +1
        # backward per X ma forward per O
        # x             X forward
        # y             O backward
        return +1 if player == 'X' else -1
    
    def possibileMove(x,y):
        def minDistance(x,y,z):
            if distance(y,z)<distance(x,z):
                return y
            return x
        
        d=direction(x,y)
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
            
    def boardEval(x):
        if board[x] == board.off: return 0
        squares = possiblesquares(x)
        density = 0
        for square in squares:
            if board[square] == board.off and (x==myKing or x==opponentKing):
                density+=0
            elif board[square] == board.empty and x==opponentKing:
                density+=symbols[board[opponentKing]] if direction(x,square)>0 else symbols[board[myKing]]
            elif board[square] == board.empty and x==myKing:
                density+=symbols[board[square]] if direction(x,square)>0 else symbols[board[myKing]]
            elif x==myKing or x==opponentKing:
                density+= symbols[board[square]] if symbols[board[x]] == symbols[board[square]] else 9*symbols[board[square]]
            else:
                density+=symbols[board[square]] if direction(x,square)>0 else 0
        if square == opponentKing:   
            return density/distance(square,opponentGoal) if density!=0 else +8/distance(square,opponentGoal) 
        if square == myKing:
            if density==0:
               for pos in possiblesquares(square):
                   if symbols[board[pos]] != 0: return -16/distance(square,myGoal) 
               return +1/distance(square,myGoal) 
            return density/distance(square,myGoal)
        distances=distance(square,myKing)*distance(square,opponentKing)
        if possibileMove(square,myKing)+possibileMove(square,opponentKing)==0:
            return 0 if symbols[board[x]]==symbols[board[myKing]] else +1
        return density/distances if density!=0 else symbols[board[square]]/distances

    if player=='X':
        myGoal=(14,7)
        opponentGoal=(0,7)
        symbols={'o':-1,'Q':-1,'x':1,'K':1,'#':0,' ':0}
    else:
        myGoal=(0,7)
        opponentGoal=(14,7)
        symbols={'o':1,'Q':1,'x':-1,'K':-1,'#':0,' ':0}

    boarddensity=0
    myKing=(-1,-1)
    opponentKing=(-1,-1)
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
        boarddensity+=symbols[board[(r,c)]] if (r,c)!=myKing or (r,c)!=opponentKing else 16*symbols[board[(r,c)]]

    defensive=boardEval(myKing)
    (r,c)=myKing
    ddefensive=0
    for i in range(1,3):
        if player=='O':
            ddefensive+=boardEval((r-i,c-i)) if board[(r-i,c-i)] != symbols[board[myKing]] else 0
            ddefensive+=boardEval((r-i,c+i)) if board[(r-i,c+i)] != symbols[board[myKing]] else 0
            ddefensive+=boardEval((r-2*i,c)) if board[(r-2*i,c)] != symbols[board[myKing]] else 0
        else:
            ddefensive+=boardEval((r+i,c-i)) if board[(r+i,c-i)] != symbols[board[myKing]] else 0
            ddefensive+=boardEval((r+i,c+i)) if board[(r+i,c+i)] != symbols[board[myKing]] else 0
            ddefensive+=boardEval((r+2*i,c)) if board[(r+2*i,c)] != symbols[board[myKing]] else 0
        ddefensive+=boardEval((r,c-2*i)) if board[(r,c-2*i)] != symbols[board[myKing]] else 0
        ddefensive+=boardEval((r,c+2*i)) if board[(r,c+2*i)] != symbols[board[myKing]] else 0

    offensive=boardEval(opponentKing)
    (r,c)=opponentKing
    ooffensive=0
    for i in range(1,3):
        if player=='X':
            ooffensive+=boardEval((r-2*i,c)) #if board[(r-2*i,c)] != symbols[board[opponentKing]] else 0
            ooffensive+=boardEval((r-i,c-i)) #if board[(r-i,c-i)] != symbols[board[opponentKing]] else 0
            ooffensive+=boardEval((r-i,c+i)) #if board[(r-i,c+i)] != symbols[board[opponentKing]] else 0
        else:
            ooffensive+=boardEval((r+2*i,c)) #if board[(r+2*i,c)] != symbols[board[opponentKing]] else 0
            ooffensive+=boardEval((r+i,c-i)) #if board[(r+i,c-i)] != symbols[board[opponentKing]] else 0
            ooffensive+=boardEval((r+i,c+i)) #if board[(r+i,c+i)] != symbols[board[opponentKing]] else 0
        ooffensive+=boardEval((r,c-2*i)) #if board[(r,c-2*i)] != symbols[board[opponentKing]] else 0
        ooffensive+=boardEval((r,c+2*i)) #if board[(r,c+2*i)] != symbols[board[opponentKing]] else 0

    w1=50
    w2=75
    w3=45
    w4=35
    w5=80
    res=f(w1*offensive+w2*defensive+w5*boarddensity+w3*ddefensive+w4*ooffensive)
    return res

def possiblesquares(x):
    return [(x[0]-1,x[1]-1),(x[0]-1,x[1]+1),(x[0]-2,x[1]),(x[0]+2,x[1]),(x[0]+1,x[1]+1),(x[0]+1,x[1]-1),(x[0],x[1]-2),(x[0],x[1]+2)]

def distance(x,y):
    return euclideanDistance(x,y)

def manhattanDistance(x, y):
    return abs(x[0]-y[0]) + abs(x[1]-y[1])

def euclideanDistance(x, y):
    return math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)

def f(x):
    return x/10000

