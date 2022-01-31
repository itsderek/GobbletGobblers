
from enum import unique
import random
from pprint import pprint
from copy import deepcopy
import pickle




class FTTT:
    def __init__(self, players) -> None:
        self.name = "Fancy TicTacToe"
        self.turn_counter = 0
        self.players = [players[0], players[1]]

        random.shuffle(self.players)
        self.initPlayers(self.players)

        self.state = {
            'top-left': [None],
            'top-center': [None],
            'top-right': [None],
            'middle-left': [None],
            'middle-center': [None],
            'middle-right': [None],
            'bottom-left': [None],
            'bottom-center': [None],
            'bottom-right': [None]
        }

    def initPlayers(self, players):
        self.active_player = players[0]
        self.players = {
            players[0]: ('X', ['SX1', 'SX2', 'MX1', 'MX2', 'LX1', 'LX2']),
            players[1]: ('O', ['SO1', 'SO2', 'MO1', 'MO2', 'LO1', 'LO2'])
        }

    def resetGame(self):
        self.state = {
            'top-left': [None],
            'top-center': [None],
            'top-right': [None],
            'middle-left': [None],
            'middle-center': [None],
            'middle-right': [None],
            'bottom-left': [None],
            'bottom-center': [None],
            'bottom-right': [None]
        }
        self.turn_counter = 0
        p_list = list(self.players.keys())
        random.shuffle(p_list)
        self.initPlayers(p_list)

    def startGame(self):
        self.resetGame()
        #gross workaround
        self.changePlayers()
        while(True):
            self.changePlayers()
            for p in self.players:
                p.getState(self.state, self.active_player)

            outcome = self.checkForWin(self.state, self.turn_counter)
            if(outcome != 0):
                #self.displayState()
                #print("Game over!")
                #pprint(self.state)
                break

            player_move = self.active_player.makeDecision(self.state, self.availableMoves(self.state, self.active_player))
            self.placePiece(self.active_player, player_move[1], player_move[0])
            self.turn_counter += 1
            
            #self.displayState()

        for p in list(self.players.keys()):
            p.train(outcome, self.active_player.name)



    def changePlayers(self):
        if(self.active_player == list(self.players.keys())[0]):
            self.active_player = list(self.players.keys())[1]
        else:
            self.active_player = list(self.players.keys())[0]

    def displayState(self):
        print(f"{self.turn_counter} - {self.active_player.name}'s Turn:")
        print(f"\n{'   ' if self.state['top-left'][0] is None else self.state['top-left'][0]}|" + \
              f"{'   ' if self.state['top-center'][0] is None else self.state['top-center'][0]}|" + \
              f"{'   ' if self.state['top-right'][0] is None else self.state['top-right'][0]}" + \
              f"\n-----------\n" + \
              f"{'   ' if self.state['middle-left'][0] is None else self.state['middle-left'][0]}|" + \
              f"{'   ' if self.state['middle-center'][0] is None else self.state['middle-center'][0]}|" + \
              f"{'   ' if self.state['middle-right'][0] is None else self.state['middle-right'][0]}" + \
              f"\n-----------\n" + \
              f"{'   ' if self.state['bottom-left'][0] is None else self.state['bottom-left'][0]}|" + \
              f"{'   ' if self.state['bottom-center'][0] is None else self.state['bottom-center'][0]}|" + \
              f"{'   ' if self.state['bottom-right'][0] is None else self.state['bottom-right'][0]}\n")

    def placePiece(self, player, piece, location):
        #print(f"player: {player.name}\tpiece: {piece}\tlocation: {location}\nplayer pieces:{self.getHeldPieces(player)}")
        if(piece in self.getHeldPieces(player)):
            self.players[player][1].remove(piece)

        on_board, location2 = self._isPieceOnBoard(piece)
        if(on_board):
            self.state[location2].remove(piece)
        
        self.state[location].insert(0, piece)


    def _isPieceOnBoard(self, piece):
        for key in self.state.keys():
            if(self.state[key][0] == piece):
                return (True, key)
        return (False, None)

    def checkForWin(self, state, turn_count):
        if(self._checkForWinHelper(state['top-left'][0],state['top-center'][0],state['top-right'][0])
        or self._checkForWinHelper(state['middle-left'][0],state['middle-center'][0],state['middle-right'][0])
        or self._checkForWinHelper(state['bottom-left'][0],state['bottom-center'][0],state['bottom-right'][0])
        or self._checkForWinHelper(state['top-left'][0],state['middle-left'][0],state['bottom-left'][0])
        or self._checkForWinHelper(state['top-center'][0],state['middle-center'][0],state['bottom-center'][0])
        or self._checkForWinHelper(state['top-right'][0],state['middle-right'][0],state['bottom-right'][0])
        or self._checkForWinHelper(state['top-left'][0],state['middle-center'][0],state['bottom-right'][0])
        or self._checkForWinHelper(state['top-right'][0],state['middle-center'][0],state['bottom-left'][0])):
            return 1
        
        if(turn_count > 30):
            return 2
        
        return 0
    
    def _checkForWinHelper(self, sq1, sq2, sq3):
        if(sq1 is None or sq2 is None or sq3 is None):
            return False
        elif(sq1[1] == sq2[1] and sq2[1] == sq3[1]):
            return True
        else:
            return False
    
    def getHeldPieces(self, player):
        return self.players[player][1]

    def availableMoves(self, state, player):
        valid_moves = {}
        held_pieces = self.getHeldPieces(player)

        i = 0
        for k, v in state.items():
            for hp in held_pieces:
                if(self._availableMovesHelper(v[0], hp)):
                    i += 1
                    valid_moves[i] = (k, hp)
        
        for v in state.values():
            piece = v[0]
            if(piece is not None and piece[1] == self.players[player][0]):
                for k in state.keys():
                    if(self._availableMovesHelper(state[k][0], piece)):
                        i += 1
                        valid_moves[i] = (k, piece)

        return valid_moves


    def _availableMovesHelper(self, square, piece):
        if(square is None):
            return True
        elif(square[0] == 'S' and piece[0] == 'M'):
            return True
        elif(square[0] == 'S' and piece[0] == 'L'):
            return True
        elif(square[0] == 'M' and piece[0] == 'L'):
            return True
        else:
            return False




class Agent:
    def __init__(self, name, training=True, e_thresh=0.75) -> None:
        self.name = name
        self.STM = []
        self.LTM = {}
        self.e_thresh = max(min(e_thresh, 1.0), 0.0)
        self.training = training
        self.num_wins = 0
    
    def save(self):
        with open(f"trainedLTM{self.name}.pickle", 'wb') as f:
            pickle.dump(self.LTM, f)

    def load(self, file):
        with open(file, 'rb') as f:
            self.LTM = pickle.load(f)

    def getState(self, state, player):
        self.STM.append((self.stateToText(state), player))
    
    def stateToText(self, state):
        return f"<{state['top-left']},{state['top-center']},{state['top-right']}," + \
               f"{state['middle-left']},{state['middle-center']},{state['middle-right']}," + \
               f"{state['bottom-left']},{state['bottom-center']},{state['bottom-right']}>"

    def placePiece(self, state, piece, location):
        #if(state[location][0] is None):
        #    state[location] = [piece]
        #else:
        state[location].insert(0, piece)

    def makeDecision(self, state, av_states):
        randomnum = random.random()
        #print(f"randomnum: {randomnum}\te_thresh: {self.e_thresh}")
        if(self.training and randomnum > self.e_thresh):
            return av_states[random.choice(list(av_states.keys()))]

        moves_info = {}
        for move_num in av_states:
            k, v = av_states[move_num]
            new_state = deepcopy(state)
            self.placePiece(new_state, v, k)

            new_state_text = self.stateToText(new_state)
            if(new_state_text in self.LTM):
                moves_info[move_num] = self.LTM[new_state_text][0] / self.LTM[new_state_text][1]
            else:
                moves_info[move_num] = 0.0

        #pprint(av_states)
        return av_states[max(moves_info, key=moves_info.get)]

    def getReward(self, outcome, winner):
        if(outcome == 1 and self.name == winner):
            return 1
        elif(outcome == 2):
            return 0.2
        else:
            return  0
        

    def train(self, outcome, winner):
        if(self.name == winner):
            self.num_wins += 1
        
        unique_STM = []
        for i in self.STM:
            if(i not in unique_STM):
                unique_STM.append(i)

        for state, player in unique_STM:
            if state in self.LTM:
                weight, hits = self.LTM[state]
                weight += self.getReward(outcome, player.name)
                hits += 1
                self.LTM[state] = [weight, hits]
            else:
                self.LTM[state] = [self.getReward(outcome, player.name), 1]

        self.STM = []

# Create Players
p1 = Agent('Derek')
p2 = Agent('Mason', e_thresh=0.2)
players = [p1, p2]

#p1.LTM['<[\'SX1\'],[None],[None],[None],[None],[None],[None],[None],[None]>'] = [10, 100]

# Tests about players
assert len(players) == 2

assert p1.getReward(1, "Mason") == 0
assert p1.getReward(2, "Derek") == 0.2
assert p1.getReward(1, "Derek") == 1
assert p2.getReward(1, "Mason") == 1
assert p2.getReward(1, "Derek") == 0
assert p2.getReward(2, "Derek") == 0.2


# Creating the Game
game = FTTT(players)

# Tests about the Game
assert game._checkForWinHelper('SX1', 'MX2', 'LX1') == 1
assert game._checkForWinHelper('SO1', 'MX2', 'LX1') == 0
assert game._checkForWinHelper('SX1', 'MX2', 'LO1') == 0
assert game._checkForWinHelper('SO2', 'MO1', 'LO1') == 1
assert game._checkForWinHelper(None, 'MO1', 'LO1') == 0

s1 = {
         'top-left': [None],
         'top-center': [None],
         'top-right': [None],
         'middle-left': [None],
         'middle-center': [None],
         'middle-right': [None],
         'bottom-left': [None],
         'bottom-center': [None],
         'bottom-right': [None]
     }
assert game.checkForWin(s1, 0) == 0

s2 = {
         'top-left': ['SX1'],
         'top-center': [None],
         'top-right': [None],
         'middle-left': [None],
         'middle-center': [None],
         'middle-right': [None],
         'bottom-left': [None],
         'bottom-center': [None],
         'bottom-right': [None]
     }
assert game.checkForWin(s2, 1) == 0

s3 = {
         'top-left': ['SX1'],
         'top-center': [None],
         'top-right': [None],
         'middle-left': [None],
         'middle-center': [None],
         'middle-right': [None],
         'bottom-left': [None],
         'bottom-center': [None],
         'bottom-right': [None]
     }
assert game.checkForWin(s3, 31) == 2

s4 = {
         'top-left': ['SX1'],
         'top-center': [None],
         'top-right': [None],
         'middle-left': ['MX2'],
         'middle-center': [None],
         'middle-right': [None],
         'bottom-left': ['SX2'],
         'bottom-center': [None],
         'bottom-right': [None]
     }
assert game.checkForWin(s4, 20) == 1

s5 = {
         'top-left': ['SO1'],
         'top-center': [None],
         'top-right': [None],
         'middle-left': ['MO2'],
         'middle-center': [None],
         'middle-right': [None],
         'bottom-left': ['SO2'],
         'bottom-center': [None],
         'bottom-right': [None]
     }
assert game.checkForWin(s5, 35) == 1

s6 = {
         'top-left': ['MO1'],
         'top-center': [None],
         'top-right': ['SX1'],
         'middle-left': ['MX2', 'SO1'],
         'middle-center': [None],
         'middle-right': [None],
         'bottom-left': ['SO2'],
         'bottom-center': [None],
         'bottom-right': ['LX1']
     }
assert game.checkForWin(s6, 15) == 0

s7 = {
         'top-left': ['MO1'],
         'top-center': [None],
         'top-right': ['SX1'],
         'middle-left': ['LO2', 'MX2', 'SO1'],
         'middle-center': [None],
         'middle-right': [None],
         'bottom-left': ['SO2'],
         'bottom-center': [None],
         'bottom-right': ['LX1']
     }
assert game.checkForWin(s7, 15) == 1

assert game._availableMovesHelper(None, 'S01') == True
assert game._availableMovesHelper('SX1', 'S01') == False
assert game._availableMovesHelper('MX1', 'S01') == False
assert game._availableMovesHelper('MX1', 'LO2') == True
assert game._availableMovesHelper('SX1', 'MX1') == True


for i in range(10000):
    game.startGame()

p1.save()

print(f"p1.num_wins: {p1.num_wins}\tp2.num_wins: {p2.num_wins}")