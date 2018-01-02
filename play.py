
# coding: utf-8

# In[138]:


import chess
import pandas as pd
import numpy as np
import time
import re
import chess.uci
from yaml import load, dump
from yaml import CLoader as Loader, CDumper as Dumper
import yaml
currentDir="/home/mike_heward/AnacondaProjects/chessproject/chessTestFramework/"
configfile = open(currentDir + 'config.yaml', 'r')
config=yaml.load(configfile)

def setupEngine(board,name='stockfish'):
    
    engine = chess.uci.popen_engine(config['engines'][name]['location']+config['engines'][name]['name'])
    engine.uci()
    info_handler = chess.uci.InfoHandler()
    engine.info_handlers.append(info_handler)
    engine.ucinewgame()
    engine.position(board)
    return engine,info_handler

def playGame(gameFEN= chess.STARTING_FEN,engine1Name='sunfish',engine2Name='stockfish'):  
    board=chess.Board()
    moveCount=1
    gamePlaying=True
    movetime_eng1=config['engines'][engine1Name]['movetime']
    movetime_eng2=config['engines'][engine2Name]['movetime']
    engine1,info1=setupEngine(board,engine1Name)
    engine1Move=engine1.go(movetime=movetime_eng1)
    engine2,info2=setupEngine(board,engine2Name)
    print ("Game between {} and {} ".format(engine1.name,engine2.name))
    while  gamePlaying:    
        engine1.position(board)
        engine1Move=engine1.go(movetime=movetime_eng1)
        board.push(engine1Move.bestmove)
        if not board.is_game_over():
            engine2.position(board)
            engine2Move=engine2.go(movetime=movetime_eng2)
            board.push(engine2Move.bestmove) 
        moveCount+=1
        gamePlaying=not board.is_game_over()
        print ("   {} {} {} {} {}".format(moveCount,engine1Move.bestmove,info1.info["score"],engine2Move.bestmove,info2.info["score"][1]))     
    engine1.quit()
    engine2.quit()
    return board
playGame(engine1Name="stockfish",engine2Name='sunfish')
print("game over")


