# POS State
EMPTY=0
PLAYER_X=1
PLAYER_O=-1
MARKS={PLAYER_X:"X",PLAYER_O:"O",EMPTY:" "}
DRAW=2

class TTTBoard:
    
    def __init__(self,board=None):
        if board==None:
            self.board = []
            for i in range(9):self.board.append(EMPTY)
        else:
            self.board=board
        self.winner=None
    
    def get_possible_pos(self):
        pos=[]
        for i in range(9):
            if self.board[i]==EMPTY:
                pos.append(i)
        return pos
    
    def print_board(self):
        tempboard=[]
        for i in self.board:
            tempboard.append(MARKS[i])
        row = ' {} | {} | {} '
        hr = '\n-----------\n'
        print((row + hr + row + hr + row).format(*tempboard))
               

                    
    def check_winner(self):
        win_cond = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))
        for each in win_cond:
            if self.board[each[0]-1] == self.board[each[1]-1]  == self.board[each[2]-1]:
                if self.board[each[0]-1]!=EMPTY:
                    self.winner=self.board[each[0]-1]
                    return self.winner
        return None
    
    def check_draw(self):
        if len(self.get_possible_pos())==0 and self.winner is None:
            self.winner=DRAW
            return DRAW
        return None
    
    def move(self,pos,player):
        if self.board[pos]== EMPTY:
            self.board[pos]=player
        else:
            self.winner=-1*player
        self.check_winner()
        self.check_draw()
    
    def clone(self):
        return TTTBoard(self.board.copy())
    
    def switch_player(self):
        if self.player_turn == self.player_x:
            self.player_turn=self.player_o
        else:
            self.player_turn=self.player_x

class TTT_GameOrganizer:

    act_turn=0
    winner=None
    
    def __init__(self,px,po,nplay=1,showBoard=True,showResult=True,stat=100):
        self.player_x=px
        self.player_o=po
        self.nwon={px.myturn:0,po.myturn:0,DRAW:0}
        self.nplay=nplay
        self.players=(self.player_x,self.player_o)
        self.board=None
        self.disp=showBoard
        self.showResult=showResult
        self.player_turn=self.players[random.randrange(2)]
        self.nplayed=0
        self.stat=stat
    
    def progress(self):
        while self.nplayed<self.nplay:
            self.board=TTTBoard()
            while self.board.winner==None:
                if self.disp:print("Turn is "+self.player_turn.name)
                act=self.player_turn.act(self.board)
                self.board.move(act,self.player_turn.myturn)
                if self.disp:self.board.print_board()
               
                if self.board.winner != None:
                    # notice every player that game ends
                    for i in self.players:
                        i.getGameResult(self.board) 
                    if self.board.winner == DRAW:
                        if self.showResult:print ("Draw Game")
                    elif self.board.winner == self.player_turn.myturn:
                        out = "Winner : " + self.player_turn.name
                        if self.showResult: print(out)
                    else:
                        print ("Invalid Move!")
                    self.nwon[self.board.winner]+=1
                else:
                    self.switch_player()
                    #Notice other player that the game is going
                    self.player_turn.getGameResult(self.board)

            self.nplayed+=1
            if self.nplayed%self.stat==0 or self.nplayed==self.nplay:
                print(self.player_x.name+":"+str(self.nwon[self.player_x.myturn])+","+self.player_o.name+":"+str(self.nwon[self.player_o.myturn])
             +",DRAW:"+str(self.nwon[DRAW]))

            
    def switch_player(self):
        if self.player_turn == self.player_x:
            self.player_turn=self.player_o
        else:
            self.player_turn=self.player_x

import random
             

class PlayerRandom:
    def __init__(self,turn):
        self.name="Random"
        self.myturn=turn
        
    def act(self,board):
        acts=board.get_possible_pos()
        i=random.randrange(len(acts))
        return acts[i]
    
    
    def getGameResult(self,board):
        pass

    
class PlayerHuman:
    def __init__(self,turn):
        self.name="Human"
        self.myturn=turn
        
    def act(self,board):
        valid = False
        while not valid:
            try:
                act = input("Where would you like to place " + str(self.myturn) + " (1-9)? ")
                act = int(act)
                #if act >= 1 and act <= 9 and board.board[act-1]==EMPTY:
                if act >= 1 and act <= 9:
                    valid=True
                    return act-1
                else:
                    print ("That is not a valid move! Please try again.")
            except Exception as e:
                    print (act +  "is not a valid move! Please try again.")
        return act
    
    def getGameResult(self,board):
        if board.winner is not None and board.winner!=self.myturn and board.winner!=DRAW:
            print("I lost...")

class PlayerAlphaRandom:
    
    
    def __init__(self,turn,name="AlphaRandom"):
        self.name=name
        self.myturn=turn
        
    def getGameResult(self,winner):
        pass
        
    def act(self,board):
        acts=board.get_possible_pos()
        #see only next winnable act
        for act in acts:
            tempboard=board.clone()
            tempboard.move(act,self.myturn)
            # check if win
            if tempboard.winner==self.myturn:
                #print ("Check mate")
                return act
        i=random.randrange(len(acts))
        return acts[i]

class PlayerMC:
    def __init__(self,turn,name="MC"):
        self.name=name
        self.myturn=turn
    
    def getGameResult(self,winner):
        pass
        
    def win_or_rand(self,board,turn):
        acts=board.get_possible_pos()
        #see only next winnable act
        for act in acts:
            tempboard=board.clone()
            tempboard.move(act,turn)
            # check if win
            if tempboard.winner==turn:
                return act
        i=random.randrange(len(acts))
        return acts[i]
           
    def trial(self,score,board,act):
        tempboard=board.clone()
        tempboard.move(act,self.myturn)
        tempturn=self.myturn
        while tempboard.winner is None:
            tempturn=tempturn*-1
            tempboard.move(self.win_or_rand(tempboard,tempturn),tempturn)
        
        if tempboard.winner==self.myturn:
            score[act]+=1
        elif tempboard.winner==DRAW:
            pass
        else:
            score[act]-=1

        
    def getGameResult(self,board):
        pass
        
    
    def act(self,board):
        acts=board.get_possible_pos()
        scores={}
        n=50
        for act in acts:
            scores[act]=0
            for i in range(n):
                #print("Try"+str(i))
                self.trial(scores,board,act)
            
            #print(scores)
            scores[act]/=n
        
        max_score=max(scores.values())
        for act, v in scores.items():
            if v == max_score:
                #print(str(act)+"="+str(v))
                return act


class PlayerQL:
    def __init__(self,turn,name="QL",e=0.2,alpha=0.3):
        self.name=name
        self.myturn=turn
        self.q={} #set of s,a
        self.e=e
        self.alpha=alpha
        self.gamma=0.9
        self.last_move=None
        self.last_board=None
        self.totalgamecount=0
        
    
    def policy(self,board):
        self.last_board=board.clone()
        acts=board.get_possible_pos()
        #Explore sometimes
        if random.random() < (self.e/(self.totalgamecount//10000+1)):
                i=random.randrange(len(acts))
                return acts[i]
        qs = [self.getQ(tuple(self.last_board.board),act) for act in acts]
        maxQ= max(qs)

        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(acts)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        self.last_move = acts[i]
        return acts[i]
    
    def getQ(self, state, act):
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q.get((state, act)) is None:
            self.q[(state, act)] = 1
        return self.q.get((state, act))
    
    def getGameResult(self,board):
        r=0
        if self.last_move is not None:
            if board.winner is None:
                self.learn(self.last_board,self.last_move, 0, board)
                pass
            else:
                if board.winner == self.myturn:
                    self.learn(self.last_board,self.last_move, 1, board)
                elif board.winner !=DRAW:
                    self.learn(self.last_board,self.last_move, -1, board)
                else:
                    self.learn(self.last_board,self.last_move, 0, board)
                self.totalgamecount+=1
                self.last_move=None
                self.last_board=None

    def learn(self,s,a,r,fs):
        pQ=self.getQ(tuple(s.board),a)
        if fs.winner is not None:
            maxQnew=0
        else:
            maxQnew=max([self.getQ(tuple(fs.board),act) for act in fs.get_possible_pos()])
        self.q[(tuple(s.board),a)]=pQ+self.alpha*((r+self.gamma*maxQnew)-pQ)
        #print (str(s.board)+"with "+str(a)+" is updated from "+str(pQ)+" refs MAXQ="+str(maxQnew)+":"+str(r))
        #print(self.q)

    
    def act(self,board):
        return self.policy(board)


import chainer

from chainer import Function, gradient_check, Variable, optimizers, serializers, utils
import chainer.functions as F
import chainer.links as L
import numpy as np
from chainer import computational_graph as c

# Network definition
class MLP(chainer.Chain):

    def __init__(self, n_in, n_units, n_out):
        super(MLP, self).__init__(
            l1=L.Linear(n_in, n_units),  # first layer
            l2=L.Linear(n_units, n_units),  # second layer
            l3=L.Linear(n_units, n_units),  # Third layer
            l4=L.Linear(n_units, n_out),  # output layer
        )

    def __call__(self, x, t=None, train=False):
        h = F.leaky_relu(self.l1(x))
        h = F.leaky_relu(self.l2(h))
        h = F.leaky_relu(self.l3(h))
        h = self.l4(h)

        if train:
            return F.mean_squared_error(h,t)
        else:
            return h

    def get(self,x):
        # input x as float, output float
        return self.predict(Variable(np.array([x]).astype(np.float32).reshape(1,1))).data[0][0]


class DQNPlayer:
    def __init__(self, turn,name="DQN",e=1,dispPred=False):
        self.name=name
        self.myturn=turn
        self.model = MLP(9, 162,9)
        self.optimizer = optimizers.SGD()
        self.optimizer.setup(self.model)
        self.e=e
        self.gamma=0.95
        self.dispPred=dispPred
        self.last_move=None
        self.last_board=None
        self.last_pred=None
        self.totalgamecount=0
        self.rwin,self.rlose,self.rdraw,self.rmiss=1,-1,0,-1.5
        
    
    def act(self,board):
        
        self.last_board=board.clone()
        x=np.array([board.board],dtype=np.float32).astype(np.float32)
        
        pred=self.model(x)
        if self.dispPred:print(pred.data)
        self.last_pred=pred.data[0,:]
        act=np.argmax(pred.data,axis=1)
        if self.e > 0.2: #decrement epsilon over time
            self.e -= 1/(20000)
        if random.random() < self.e:
            acts=board.get_possible_pos()
            i=random.randrange(len(acts))
            act=acts[i]
        i=0
        while board.board[act]!=EMPTY:
            #print("Wrong Act "+str(board.board)+" with "+str(act))
            self.learn(self.last_board,act, -1, self.last_board)
            x=np.array([board.board],dtype=np.float32).astype(np.float32)
            pred=self.model(x)
            #print(pred.data)
            act=np.argmax(pred.data,axis=1)
            i+=1
            if i>10:
                print("Exceed Pos Find"+str(board.board)+" with "+str(act))
                acts=self.last_board.get_possible_pos()
                act=acts[random.randrange(len(acts))]
            
        self.last_move=act
        #self.last_pred=pred.data[0,:]
        return act
    
    def getGameResult(self,board):
        r=0
        if self.last_move is not None:
            if board.winner is None:
                self.learn(self.last_board,self.last_move, 0, board)
                pass
            else:
                if board.board== self.last_board.board:            
                    self.learn(self.last_board,self.last_move, self.rmiss, board)
                elif board.winner == self.myturn:
                    self.learn(self.last_board,self.last_move, self.rwin, board)
                elif board.winner !=DRAW:
                    self.learn(self.last_board,self.last_move, self.rlose, board)
                else:                    #DRAW
                    self.learn(self.last_board,self.last_move, self.rdraw, board)
                self.totalgamecount+=1
                self.last_move=None
                self.last_board=None
                self.last_pred=None

    def learn(self,s,a,r,fs):
        if fs.winner is not None:
            maxQnew=0
        else:
            x=np.array([fs.board],dtype=np.float32).astype(np.float32)
            maxQnew=np.max(self.model(x).data[0])
        update=r+self.gamma*maxQnew
        #print(('Prev Board:{} ,ACT:{}, Next Board:{}, Get Reward {}, Update {}').format(s.board,a,fs.board,r,update))
        #print(('PREV:{}').format(self.last_pred))
        self.last_pred[a]=update
        
        x=np.array([s.board],dtype=np.float32).astype(np.float32)
        t=np.array([self.last_pred],dtype=np.float32).astype(np.float32)
        self.model.zerograds()
        loss=self.model(x,t,train=True)
        loss.backward()
        self.optimizer.update()
        #print(('Updated:{}').format(self.model(x).data))
        #print (str(s.board)+"with "+str(a)+" is updated from "+str(pQ)+" refs MAXQ="+str(maxQnew)+":"+str(r))
        #print(self.q)

pQ=PlayerQL(PLAYER_O,"QL1")
p2=PlayerQL(PLAYER_X,"QL2")
game=TTT_GameOrganizer(pQ,p2,100000,False,False,10000)
game.progress()
