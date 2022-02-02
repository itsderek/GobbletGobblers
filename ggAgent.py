
import pickle
import random
from copy import deepcopy

class Agent:
    def __init__(self, name, training=True, e_thresh=0.75) -> None:
        self.name = name
        self.STM = []
        self.LTM = {}
        self.e_thresh = max(min(e_thresh, 1.0), 0.0)
        self.training = training
        self.num_wins = 0
    
    def save(self):
        file_name = f"trainedLTM{self.name}.pickle"
        with open(file_name, 'wb') as f:
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
        state[location].insert(0, piece)

    def makeDecision(self, state, av_states):
        randomnum = random.random()
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

        return av_states[max(moves_info, key=moves_info.get)]

    def getReward(self, outcome, winner):
        if(outcome == 1 and self.name == winner):
            return 1
        elif(outcome == 2):
            return 0.1
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

class Player:
    def __init__(self, name) -> None:
        self.name = name
    
    def getState(self, state, player):
        pass

    def makeDecision(self, state, av_states):
        
        i = -1
        display_string = 'Move\tPiece->Square\n'
        for k, v in av_states.items():
            i += 1
            if(i == 4):
                display_string += '\n'
                i = 0
            
            display_string += f"{k}: {v[1]}->{v[0]}\t\t"

        display_string += "\n"

        player_choice = input(display_string)
        return av_states[int(player_choice)]


from ggGame import FTTT

p1 = Agent('Robo', training=False)
p2 = Player("Derek")

p1.load("trainedLTMBest.pickle")

game = FTTT([p1, p2], real_game=True)
game.startGame()