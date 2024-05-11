from players.strategy.playingStrategies import h_alphabeta_search 
from players.strategy.playingStrategies import cutoff_depth 

turno=0
def playerStrategy(game,state):
    global turno
    turno+=1
    cutOff=2
    if turno>90: cutOff=3
    if turno>150: cutOff=4
    value,move,depth = h_alphabeta_search(game,state,cutoff_depth(cutOff))
    return move