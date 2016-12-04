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
            for i in range(64):self.board.append(EMPTY)
        else:
            self.board=board
        self.winner=None
    
    def get_possible_pos(self):
        pos=[]
        for i in range(64):
            if self.board[i]==EMPTY:
                pos.append(i)
        return pos
    
    def print_board(self):
        tempboard=[]
        for i in self.board:
            tempboard.append(MARKS[i])
        row = ' {} | {} | {} | {} | {} | {} | {} | {} '
        hr = '\n----------------\n'
        print((row + hr + row + hr + row + hr + row  + hr + row + hr + row + hr + row + hr + row).format(*tempboard))
               
    def check_winner(self, player):
        p1_cnt=0
        for place in self.board:
            if place == player:
                p1_cnt+=1
        if p1_cnt > 32:
            self.winner = player # player1
        elif p1_cnt == 32:
            self.winner = DRAW
        else:
            self.winner = -1*player # player2

    def conv_pos_xy_to_num(self,x, y):
        return y*8 + x;
        
    def conv_pos_num_to_xy(self,num):
        return  num % 8, int(num / 8)
        
    
    def check_hasami(self,check_pos, player, xv, yv):
        cur_x, cur_y = self.conv_pos_num_to_xy(check_pos)
#        print("check_hasami cur_pos:" + str(check_pos) + " x,y:" + str(cur_x) + "," + str(cur_y))
        if cur_x < 0 or cur_x > 7 or cur_y < 0 or cur_y > 7:
            return False

        if self.board[check_pos] == EMPTY:
            return False
        
        if self.board[check_pos] == player:
            return True

        check_x = cur_x + xv
        check_y = cur_y + yv
        if check_x < 0 or check_x > 7 or check_y < 0 or check_y > 7:
            return False
        
        ret = self.check_hasami(self.conv_pos_xy_to_num(check_x, check_y), player, xv, yv) 
        if ret == True:
            self.board[check_pos] = player;

        return ret
        
    def move(self,pos,player):
        if self.board[pos]== EMPTY:
            self.board[pos]=player
            cur_x, cur_y = self.conv_pos_num_to_xy(pos)
            xv = 0
            yv = 1
            self.check_hasami(self.conv_pos_xy_to_num(cur_x+xv, cur_y+yv), player, xv, yv)
            xv = 0
            yv = -1
            self.check_hasami(self.conv_pos_xy_to_num(cur_x+xv, cur_y+yv), player, xv, yv)
            xv = 1
            yv = 0
            self.check_hasami(self.conv_pos_xy_to_num(cur_x+xv, cur_y+yv), player, xv, yv)            
            xv = -1
            yv = 0
            self.check_hasami(self.conv_pos_xy_to_num(cur_x+xv, cur_y+yv), player, xv, yv)
            xv = -1
            yv = -1
            self.check_hasami(self.conv_pos_xy_to_num(cur_x+xv, cur_y+yv), player, xv, yv)
            xv = 1
            yv = 1
            self.check_hasami(self.conv_pos_xy_to_num(cur_x+xv, cur_y+yv), player, xv, yv)            
            xv = 1
            yv = -1
            self.check_hasami(self.conv_pos_xy_to_num(cur_x+xv, cur_y+yv), player, xv, yv)
            xv = -1
            yv = 1
            self.check_hasami(self.conv_pos_xy_to_num(cur_x+xv, cur_y+yv), player, xv, yv)                        
        else:
            print("wrong placement! " + str(pos))
            self.winner=-1*player
        if(len(self.get_possible_pos())==0):
            self.check_winner(player)
    
    def clone(self):
        return TTTBoard(list(self.board))
    
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
#                    print("myturn:" + str(self.player_turn.myturn) + " self.board.winner:" + str(self.board.winner))
                    if self.board.winner == DRAW:
                        if self.showResult:print ("Draw Game")
                    else:
                        if self.showResult: print("Winner " + str(self.board.winner))
                    # elif self.board.winner == self.player_turn.myturn:
                    #     out = "Winner : " + self.player_turn.name
                    #     if self.showResult: print(out)
                    # else:
                    #     print(self.board.winner)
                    #     print ("Invalid Move!")
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
                act = input("Where would you like to place " + str(self.myturn) + " (1-32)? ")
                act = int(act)
                #if act >= 1 and act <= 9 and board.board[act-1]==EMPTY:
                if act >= 1 and act <= 64:
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


import tensorflow as tf
import numpy as np

# Network definition
class MLP():

    def __init__(self, n_in, n_units, n_out):
        self.sess = tf.Session()
        x = tf.placeholder("float", [None, n_in])
        y_ = tf.placeholder("float", [None, n_units])

        weights1 = tf.Variable(tf.truncated_normal([n_in, n_units], stddev=0.0001))
        biases1 = tf.Variable(tf.ones([n_units]))

        weights2 = tf.Variable(tf.truncated_normal([n_units, n_units], stddev=0.0001))
        biases2 = tf.Variable(tf.ones([n_units]))

        weights3 = tf.Variable(tf.truncated_normal([n_units, n_out], stddev=0.0001))
        biases3 = tf.Variable(tf.ones([n_out]))

        # This time we introduce a single hidden layer into our model...
        hidden_layer_1 = tf.nn.relu(tf.matmul(x, weights1) + biases1)
        hidden_layer_2 = tf.nn.relu(tf.matmul(hidden_layer_1, weights2) + biases2)
        self.model = tf.nn.softmax(tf.matmul(hidden_layer_2, weights3) + biases3)

        cost = -tf.reduce_sum(y_*tf.log(model))

        self.training_step = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost)

        init = tf.initialize_all_variables()
        
        sess.run(init)

    def pred(self, x):
        return sess.run(self.model,feed_dict(x: [x]))

    def learn(x, y):
        self.sess.run(self.training_step, feed_dict={x: [x], y_: [y]})

    

class DQNPlayer:
    def __init__(self, turn,name="DQN",e=1,dispPred=False):
        self.name=name
        self.myturn=turn
        self.model = MLP(64, 256, 64)
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
        x = board.board
        
        pred=self.model.pred(x)
        if self.dispPred:print(pred)
        self.last_pred=pred
        act=np.argmax(pred)
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
            pred=self.model.pred(x)
            #print(pred.data)
            act=np.argmax(pred.data,axis=1)
            i+=1
            if i>10:
#                print("Exceed Pos Find"+str(board.board)+" with "+str(act))
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
            x= fs.board
            maxQnew=np.max(self.model.pred(x)[0])
            
        update=r+self.gamma*maxQnew

        self.last_pred[a]=update
        
        x=s.board
        y=self.last_pred
        self.model.learn(x,y)
        

pQ=DQNPlayer(PLAYER_O,"QL1")
p2=PlayerRandom(PLAYER_X)
game=TTT_GameOrganizer(pQ,p2,250000,False,False,10)
game.progress()

# pQ=PlayerQL(PLAYER_O,"QL1")
# p2=PlayerRandom(PLAYER_X)
# game=TTT_GameOrganizer(pQ,p2,200000,False,False,1000)
# game.progress()

# import pickle
# with open("./QL_player.pickle","wb") as f:
#     pickle.dump(pQ, f)

# import pickle
# with open('./QL_player.pickle', 'rb') as f:
#     pQ = pickle.load(f)
pQ.e=0
p2=PlayerRandom(PLAYER_X)
game=TTT_GameOrganizer(pQ,p2,2000,False,False,100)
game.progress()


p2=PlayerHuman(PLAYER_X)
game=TTT_GameOrganizer(pQ,p2,20)
game.progress()

# pQ=PlayerHuman(PLAYER_X)
# p2=PlayerRandom(PLAYER_O)
# game=TTT_GameOrganizer(pQ,p2)
# game.progress()
