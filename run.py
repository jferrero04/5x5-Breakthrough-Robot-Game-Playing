from Game import *
from Robot373 import *

#
#
#  Define all the basic game functions
#
# 
left,right=Motors("ab")

def forward():
    left.power=17
    right.power=17

def stop():
    left.power=0
    right.power=0

def reverse():
    left.power=-17
    right.power=-17

def degrees(position):
    return position*1.0

def distance_traveled(position):
    wheel_diameter_cm=7.62
    pi=3.141592653589793235
    return pi*wheel_diameter_cm*degrees(position)/360

def forward1():
    forward()
    Wait(1)
    stop()

#
#
#  MOVEMENT FUNCTIONS
#
#
def go_forward_squares_yellow(number_cols_to_move):  # THIS FUNCTION GETS TO FIRST YELLOW
    print("Yellow function started")
    distance_per_yellow_cm1=(7.56*2.54)*number_cols_to_move
    total_distance_cm1=distance_per_yellow_cm1
    left.reset_position()
    forward()
    print("Motor power set:",left.power,right.power)
    print("Starting forward movement")
    while distance_traveled(left.position)<total_distance_cm1:
        Wait(0.01)

def rot90():
    print("Rotate 90 started")
    left.reset_position()
    left.power=17
    right.power=-17
    axis_length_cm=16.5  # 6.69in axle to axle converted to 17 cm
    pi=3.14159
    distance_needed=(axis_length_cm/2)*2*pi/4  # need a quarter turn of the robot
    while distance_traveled(left.position)<distance_needed:
        Wait(0.01)

def go_forward_squares_blue(number_rows_to_move):   # THIS FUNCTION MOVES TO 1 SQUARE. Implement AFTER rot90() function
    print("Blue function started")
    distance_per_yellow_cm2=(5.75*2.54)*number_rows_to_move
    total_distance_cm2=distance_per_yellow_cm2
    left.reset_position()
    forward()
    print("Motor power set:",left.power,right.power)
    print("Starting forward movement")
    while distance_traveled(left.position)<total_distance_cm2:
        Wait(0.01)
    stop()

def initial_state():
    state=Board(5,5)
    
    row=0
    for col in range(5):
        state[row, col] = 1
        
    row=4
    for col in range(5):
        state[row, col] = 2
    
    return state


# In[3]:
def valid_moves(state, player):
    moves=[]
    player1Column1down=[0,5,10,15]
    player2Column1up=[5,10,15,20]
    player1Column5down=[4,9,14,19]
    player2Column5up=[9,14,19,24]

    # Player 1 valid forward moves
    if player==1:
        for location in range(20):
            if state[location]==1:
                newLocation=location+5
                if newLocation<len(state) and state[newLocation]==0:
                    moves.append((location,newLocation))

    # Player 2 valid forward moves
    if player==2:
        for location in range(5, 25):
            if state[location]==2:
                newLocation=location-5
                if newLocation>=0 and state[newLocation]==0:
                    moves.append((location,newLocation))
                
    # Player 1 valid diagonal moves right
    if player==1:
        for location in range(20):
            if state[location]==1:
                if location%5==4:
                    continue
                newLocation=location+6
                if newLocation<len(state) and state[newLocation]==2:
                    moves.append((location,newLocation))
                
    # Player 1 valid diagonal moves left
    if player==1:
        for location in range(5,25):
            if state[location]==1:
                if location%5==0:
                    continue
                newLocation=location+4
                if newLocation<len(state) and state[newLocation]==2:
                    moves.append((location,newLocation))
                    
    # Player 1 valid diagonal moves down column 1 (0 index)
    if player==1:
        for location in player1Column1down:
            if state[location]==1:
                newLocation=location+6
                if newLocation<len(state) and state[newLocation]==2:
                    moves.append((location,newLocation))
                    
    # Player 1 valid diagonal moves down column 5 (4 index)
    if player==1:
        for location in player1Column5down:
            if state[location]==1:
                newLocation=location+4
                if newLocation<len(state) and state[newLocation]==2:
                    moves.append((location,newLocation))
                
    # Player 2 valid diagonal moves right
    if player==2:
        for location in range(20):
            if state[location]==2:
                if location%5==4:
                    continue
                newLocation=location-6
                if newLocation>=0 and state[newLocation]==1:
                    moves.append((location,newLocation))
                
    # Player 2 valid diagonal moves left
    if player==2:
        for location in range(20):
            if state[location]==2:
                if location%5==0:
                    continue
                newLocation=location-4
                if newLocation>=0 and state[newLocation]==1:
                    moves.append((location,newLocation))
                    
    # Player 2 valid diagonal moves up column 1 (0 index)
    if player==2:
        for location in player2Column1up:
            if state[location]==2:
                newLocation=location-4
                if newLocation<len(state) and state[newLocation]==1:
                    moves.append((location,newLocation))
                    
    # Player 2 valid diagonal moves up column 5 (4 index)
    if player==2:
        for location in player2Column5up:
            if state[location]==2:
                newLocation=location-6
                if newLocation<len(state) and state[newLocation]==1:
                    moves.append((location,newLocation))

                    
    moves=[ [start,end] for start,end in moves]
                    
    return moves       


# In[4]:
def update_state(state,player,move):
    start,end=move
    newState=state
    newState[start]=0
    newState[end]=player
    
    return newState


# In[5]:
def win_status(state,player):
    # Win by reaching opposing players start row
    for col in range(5):
        if state[4, col]==1:
            return "win"
            
    for col in range(5):
        if state[0, col]==2:
            return "win"

    # Win by blocking and win by eliminating all opposing players' pieces
    if player==1 and not valid_moves(state,2):
        return "win"
    
    if player==2 and not valid_moves(state,1):
        return "win"

    return None


# In[6]:
def show_state(state,player):
    print(state)


# In[8]:
def monkey_move(state,player):
    return random.choice(valid_moves(state,player))
monkey_agent=Agent(monkey_move)
random_move=monkey_move


def read_state_from_file(filename):
    text = open(filename).read()
    text = text.strip()
    lines = [line.strip() for line in text.split('\n')]  # get rid of \n
    
    row = lines[0].split()
    R, C = len(lines), len(row)
    print(f"{R}x{C} board")
    state = Board(R, C)
    state.board = [int(val) for val in text.split()]
    print(state)
    return state

import ijson   # install with pip install ijson on both laptop and robot
from Game.tables import make_immutable,str2table

class SmallTable(object):

    def __init__(self,filename):
        self.filename=filename

    def __getitem__(self, key):
        key=make_immutable(key)
        with open(self.filename, "rb") as f:
            for record in ijson.items(f, str(key)):
                return str2table(record)

        raise KeyError

    def __contains__(self, key):
        keyi=make_immutable(key)
        try:
            value=self[keyi]
            return True
        except KeyError:
            print(key)
            print(keyi.__repr__())
            return False


def get_move(state,player):
    if player==2:
        Q=SmallTable("small_breakthrough_skittles2.json")
    else:
        Q=SmallTable("small_breakthrough_skittles1.json")

    if state not in Q:
        print("State not in the table: ",state)
        move=random_move(state,player)
    else:
        move=top_choice(Q[state])

    return move

read_state=read_state_from_file
    
# In[58]:
def make_move(move):
    start,end=move
    row,col=state.row(start),state.col(start)

    # depends on where the robot starts
    number_cols_to_move=1+col
    number_rows_to_move=5-row


    go_forward_squares_yellow(number_cols_to_move)
    rot90()
    forward1()
    go_forward_squares_blue(number_rows_to_move)

    #  0  1  2  3  4
    #  5  6  7  8  9
    #  10 11 12 13 14
    #  15 16 17 18 19
    #  20 21 22 23 24
    
    #if start-end==3:
        #do_right_diag()
    #elif start-end==5:
        #do_left_diag()
    #elif start-end==4:
        #do_forward_move()
    #else:
        #raise ValueError("You can't get there from here")
    print("Making move ",move)


# In[52]:
player=2 # or player=2 depending on which you want
state=read_state("board-JF.txt") # read the pieces, and construct the state
move=get_move(state,player) # replace with minimax,skitles, Q, etc...
make_move(state,player,move) # actually move the pieces

