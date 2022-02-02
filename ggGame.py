
import random

class FTTT:
    def __init__(self, players, real_game=False) -> None:
        self.name = "Fancy TicTacToe"
        self.turn_counter = 0
        self.players = [players[0], players[1]]

        self.real_game = real_game

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
                if(self.real_game):
                    self.displayState()
                    self.changePlayers()
                    print(f"Game over! {self.active_player.name} is the winner!")
                break

            if(self.real_game):
                self.displayState()

            player_move = self.active_player.makeDecision(self.state, self.availableMoves(self.state, self.active_player))
            self.placePiece(self.active_player, player_move[1], player_move[0])
            self.turn_counter += 1

        if(not self.real_game):
            for p in list(self.players.keys()):
                p.train(outcome, self.active_player.name)


    def runGames(self, conn, num_games):
        for i in range(num_games):
            self.startGame()
        
        if(list(self.players.keys())[0].num_wins > list(self.players.keys())[1].num_wins):
            conn.send(list(self.players.keys())[0].LTM)
            conn.close()
        else:
            conn.send(list(self.players.keys())[1].LTM)
            conn.close()


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