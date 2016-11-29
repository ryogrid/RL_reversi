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
            for i in range(16):self.board.append(EMPTY)
        else:
            self.board=board
        self.winner=None
    
    def get_possible_pos(self):
        pos=[]
        for i in range(16):
            if self.board[i]==EMPTY:
                pos.append(i)
        return pos
    
    def print_board(self):
        tempboard=[]
        for i in self.board:
            tempboard.append(MARKS[i])
        row = ' {} | {} | {} | {} '
        hr = '\n----------------\n'
        print((row + hr + row + hr + row + hr + row).format(*tempboard))
               
    def check_winner(self):
        p1_cnt=0
        for place in board:
            if place == 1:
                p1_cnt+=1
            if p1_cnt > 8:
                self.winner = 1 # player1
            elif p1_cnt == 8:
                self.winner = DRAW
            else:
                self.winner = -1 # player2

    def conv_pos_xy_to_num(self,x, y):
        return (x-1)*4 + y;
        
    def conv_pos_num_to_xy(self,num):
        return  int((num + 3) / 4) , num % 4
        
    
    def check_hasami(self,check_pos, player, xv, yv):
        cur_x, cur_y = self.conv_pos_num_to_xy(check_pos)
        if cur_x < 1 or cur_x > 4 or cur_y < 1 or cur_y > 4:
            return False

        if self.board[check_pos] == EMPTY:
            return False
        
        if self.board[check_pos] == player:
            return True

        cur_x, cur_y = self.conv_pos_num_to_xy(check_pos)
        check_x = cur_x + xv
        check_y = cur_y + yv
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
            printf("wrong placement! " + str(pos))
            self.winner=-1*player
        if(self.get_possible_pos()==0):
            self.check_winner()
    
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
                act = input("Where would you like to place " + str(self.myturn) + " (1-16)? ")
                act = int(act)
                #if act >= 1 and act <= 9 and board.board[act-1]==EMPTY:
                if act >= 1 and act <= 16:
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

# pQ=PlayerQL(PLAYER_O,"QL1")
# p2=PlayerQL(PLAYER_X,"QL2")
# game=TTT_GameOrganizer(pQ,p2,100000,False,False,10000)
# game.progress()

pQ=PlayerRandom(PLAYER_O)
p2=PlayerHuman(PLAYER_X)
game=TTT_GameOrganizer(pQ,p2)
game.progress()
