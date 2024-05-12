import math 

def eval(board,player,symbols,myKing,opponentKing,myGoal,opponentGoal,x):
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
            if distance(y,z)<distance(x,z):
                return y
            return x
        
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
                    if possibleMove(x,square)>0:
                        density+= symbols[board[square]] if possibleMove(x,square)>0 else 0
                else:
                    density+= 8*symbols[board[square]] 
            else:
                density+=symbols[board[square]]
                
    if x == opponentKing:  
        if density==0:
            return +1/distance(x,opponentGoal) if zeros==8 else -1/distance(x,opponentGoal) 
        return density/distance(x,opponentGoal)
    
    if x == myKing:
        if density==0:
            return +1/distance(x,myGoal) if zeros==8 else -8/distance(x,myGoal) 
        return density/distance(x,myGoal)
    
    distances=distance(x,myKing)*distance(x,opponentKing)

    if density==0 and zeros==8:
        if symbols[board[x]] == symbols[board[myKing]]:
            return symbols[board[x]] if possibleMove(x,opponentKing)>0 else 0
        else:
            return symbols[board[x]] if possibleMove(x,myKing)>0 else symbols[board[myKing]]
    if density==0 and board[x]==board.empty:
        if symbols[board[x]] == symbols[board[myKing]]:
            return symbols[board[myKing]]/distances 
        else:
            return symbols[board[opponentKing]]/distances

    return density/distances if density!=0 else symbols[board[x]]/distances

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

def compareDistance(myKing,myGoal,opponentKing,opponentGoal):
    if distance(myKing,myGoal) < distance(opponentKing,opponentGoal):
        return +1/distance(myKing,myGoal)
    if distance(myKing,myGoal) > distance(opponentKing,opponentGoal): 
        return -1/distance(opponentKing,opponentGoal)
    return 0


