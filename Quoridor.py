# Author: Roy Kim
# Date: 8/12/2021
# Description: A two-player board game called Quoridor.

class QuoridorGame:
    def __init__(self):
        """ initializes the board with the fences (four edges) and pawns(P1 and P2) placed in the correct positions """
        self._rows = [i for i in range(9)]
        self._columns = [j for j in range(9)]
        self._positions = []

        for x in self._rows:
            for y in self._columns:
                self._positions.append((x, y))

        self._board = {coord: None for coord in self._positions}
        self._board[(4, 0)] = "P1"
        self._board[(4, 8)] = "P2"

        self._board_edge = []

        for coord in self._positions:
            if 0 in coord or 8 in coord:
                self._board_edge.append(coord)

        self._p1_edge = []
        self._p2_edge = []

        for coord in self._positions:
            if coord[1] == 0:
                self._p1_edge.append(coord)
        for coord in self._positions:
            if coord[1] == 8:
                self._p2_edge.append(coord)

        self._player = [1, 2]
        self._p1_fence_count = 10
        self._p2_fence_count = 10
        self._used_fences = {'v': [], 'h': []}
        self._new_fence = []

        self._p1_current = (4, 0)
        self._p2_current = (4, 8)

        self._turn_counter = 1

    def move_pawn(self, player, to_location):
        """ moves pawn according to given coord. makes sure the move is not forbidden or the game has not already been
        won. if so, returns False. otherwise returns True """
        if self.is_winner(1) is True or self.is_winner(2) is True:
            return False
        if player == self._turn_counter:
            if player == 1:
                if self.p1_move_check(to_location) is True and self.p1_wall_check(to_location) is True:
                    self._board[self._p1_current] = None
                    self._board[to_location] = "P1"
                    self._p1_current = to_location
                    self._turn_counter += 1
                    return True

            if player == 2:
                if self.p2_move_check(to_location) is True and self.p2_wall_check(to_location) is True:
                    self._board[self._p2_current] = None
                    self._board[to_location] = "P2"
                    self._p2_current = to_location
                    self._turn_counter -= 1
                    return True

        return False

    def place_fence(self, player, v_or_h, pos):
        """ places a fence vertically or horizontally according to given position/coord. makes sure that the player has
        remaining fences, the fence is within the boundaries, that there is no fence already there, that the new fence
        will no overlap or intersect with an existing fence, and that the game has not already been won yet. if so,
        return False. otherwise, return True. """
        if player == self._turn_counter:
            if player == 1:
                if self.p1_fence_check(v_or_h, pos) is True:
                    for coord in self._new_fence:
                        self._used_fences['v'].append(coord)
                        self._p1_fence_count -= 1
                        self._turn_counter += 1
                        return True

            if player == 2:
                if self.p2_fence_check(v_or_h, pos) is True:
                    for coord in self._new_fence:
                        self._used_fences['v'].append(coord)
                        self._p2_fence_count -= 1
                        self._turn_counter -= 1
                        return True

        return False

    def is_winner(self, player):
        """ takes a single integer representing the player number as a parameter and returns True if that player
        has won, and False if that player has not won """
        if player == 1:
            if self._p1_current in self._p2_edge:
                return True
        elif player == 2:
            if self._p2_current in self._p1_edge:
                return True

        return False

    def print_board(self):
        """ prints the board to the screen """
        print(self._board)

    def p1_move_check(self, to_location):
        """ checks whether a pawn move made by player 1 is a valid move """
        if self.is_winner(1) is True or self.is_winner(2) is True:
            return False
        if to_location not in self._board:
            return False

        if self._board[to_location] == "P2":
            return False

        if to_location[0] == self._p1_current[0] + 1 or to_location[0] == self._p1_current[0] - 1:
            if to_location[1] == self._p1_current[1]:
                return True
        elif to_location[1] == self._p1_current[1] + 1 or to_location[1] == self._p1_current[1] - 1:
            if to_location[0] == self._p1_current[0]:
                return True

        elif self._p1_current[0] - to_location[0] == 2 and self._p1_current[1] - to_location[1] == 0:
            if self._p2_current == (to_location[0]+1, to_location[1]):
                return True
        elif self._p1_current[0] - to_location[0] == -2 and self._p1_current[1] - to_location[1] == 0:
            if self._p2_current == (to_location[0]-1, to_location[1]):
                return True
        elif self._p1_current[0] - to_location[0] == 0 and self._p1_current[1] - to_location[1] == 2:
            if self._p2_current == (to_location[0], to_location[1]+1):
                return True
        elif self._p1_current[0] - to_location[0] == 0 and self._p1_current[1] - to_location[1] == -2:
            if self._p2_current == (to_location[0], to_location[1]-1):
                return True

        elif to_location == (self._p1_current[0]+1, self._p1_current[1]-1):
            if self._p1_current not in self._used_fences and self._p2_current == (self._p1_current[0],
                                                                                  self._p1_current[1]-1):
                return True
        elif to_location == (self._p1_current[0]-1, self._p1_current[1]-1):
            if (self._p1_current[0]-1, self._p1_current[1]) not in self._used_fences and self._p2_current ==\
                    (self._p1_current[0], self._p1_current[1]-1):
                return True
        elif to_location == (self._p1_current[0]-1, self._p1_current[1]+1):
            if to_location not in self._used_fences and self._p2_current == (self._p1_current[0],
                                                                             self._p1_current[1]+1):
                return True
        elif to_location == (self._p1_current[0]+1, self._p1_current[1]+1):
            if (self._p1_current[0], self._p1_current[1]+1) not in self._used_fences and self._p2_current ==\
                    (self._p1_current[0], self._p1_current[1]+1):
                return True

        return False

    def p2_move_check(self, to_location):
        """ checks whether a pawn move made by player 2 is a valid move """
        if self.is_winner(1) is True or self.is_winner(2) is True:
            return False
        if to_location not in self._board:
            return False

        if self._board[to_location] == "P1":
            return False

        if to_location[0] == self._p2_current[0] + 1 or to_location[0] == self._p2_current[0] - 1:
            if to_location[1] == self._p2_current[1]:
                return True
        elif to_location[1] == self._p2_current[1] + 1 or to_location[1] == self._p2_current[1] - 1:
            if to_location[0] == self._p2_current[0]:
                return True

        elif self._p2_current[0] - to_location[0] == 2 and self._p2_current[1] - to_location[1] == 0:
            if self._p1_current == (to_location[0]+1, to_location[1]):
                return True
        elif self._p2_current[0] - to_location[0] == -2 and self._p2_current[1] - to_location[1] == 0:
            if self._p1_current == (to_location[0]-1, to_location[1]):
                return True
        elif self._p2_current[0] - to_location[0] == 0 and self._p2_current[1] - to_location[1] == 2:
            if self._p1_current == (to_location[0], to_location[1]+1):
                return True
        elif self._p2_current[0] - to_location[0] == 0 and self._p2_current[1] - to_location[1] == -2:
            if self._p1_current == (to_location[0], to_location[1]-1):
                return True

        elif to_location == (self._p2_current[0]+1, self._p2_current[1]-1):
            if self._p2_current not in self._used_fences and self._p1_current == (self._p2_current[0],
                                                                                  self._p2_current[1]-1):
                return True
        elif to_location == (self._p2_current[0]-1, self._p2_current[1]-1):
            if (self._p2_current[0]-1, self._p2_current[1]) not in self._used_fences and self._p1_current == \
                    (self._p2_current[0], self._p2_current[1]-1):
                return True
        elif to_location == (self._p2_current[0]-1, self._p2_current[1]+1):
            if to_location not in self._used_fences and self._p1_current == (self._p2_current[0],
                                                                             self._p2_current[1]+1):
                return True
        elif to_location == (self._p2_current[0]+1, self._p2_current[1]+1):
            if (self._p2_current[0], self._p2_current[1]+1) not in self._used_fences and self._p1_current == \
                    (self._p2_current[0], self._p2_current[1]+1):
                return True

        return False

    def p1_wall_check(self, to_location):
        """ checks whether a pawn move by player 1 is blocked by a fence """
        if self._p1_current[0] - to_location[0] == 1 and self._p1_current[1] - to_location[1] == 0:
            if to_location not in self._used_fences['v'] or (
                    to_location[0], to_location[1]+1) not in self._used_fences['v']:
                return True
        if self._p1_current[0] - to_location[0] == -1 and self._p1_current[1] - to_location[1] == 0:
            if self._p1_current not in self._used_fences['v'] or (
                    self._p1_current[0], self._p1_current[1]+1) not in self._used_fences['v']:
                return True
        if self._p1_current[1] - to_location[1] == 1 and self._p1_current[0] - to_location[0] == 0:
            if (self._p1_current[0]-1, self._p1_current[1]) not in self._used_fences['h'] or \
                    self._p1_current not in self._used_fences['h']:
                return True
        if self._p1_current[1] - to_location[1] == -1 and self._p1_current[0] - to_location[0] == 0:
            if to_location not in self._used_fences['h'] or (
                    to_location[0]-1, to_location[1]) not in self._used_fences['h']:
                return True

        if self._p1_current[0] - to_location[0] == 2 and self._p1_current[1] - to_location[1] == 0:
            if to_location not in self._used_fences['v'] or (to_location[0], to_location[1]+1) not in\
                    self._used_fences['v'] or (to_location[0]+1, to_location[1]) not in self._used_fences['v'] or \
                    (to_location[0]+1, to_location[1]+1) not in self._used_fences['v']:
                return True
        if self._p1_current[0] - to_location[0] == -2 and self._p1_current[1] - to_location[1] == 0:
            if self._p1_current not in self._used_fences['v'] or (self._p1_current[0], self._p1_current[1]+1) not in\
                    self._used_fences['v'] or (self._p1_current[0]+1, self._p1_current[1]) not in self._used_fences or \
                    (self._p1_current[0]+1, self._p1_current[1]+1) not in self._used_fences:
                return True
        if self._p1_current[1] - to_location[1] == 2 and self._p1_current[0] - to_location[0] == 0:
            if (self._p1_current[0] - 1, self._p1_current[1]) not in self._used_fences['h'] or self._p1_current not in\
                    self._used_fences['h'] or (self._p1_current[0], self._p1_current[1]+1) not in self._used_fences or \
                    (self._p1_current[0]+1, self._p1_current[1]+1) not in self._used_fences:
                return True
        if self._p1_current[1] - to_location[1] == -2 and self._p1_current[0] - to_location[0] == 0:
            if to_location not in self._used_fences['h'] or (to_location[0]-1, to_location[1]) not in\
                    self._used_fences['h'] or (to_location[0], to_location[1]-1) not in self._used_fences or \
                    (to_location[0]-1, to_location[1]-1) not in self._used_fences:
                return True

        return False

    def p2_wall_check(self, to_location):
        """ checks whether a pawn move by player 2 is blocked by a fence """
        if self._p2_current[0] - to_location[0] == 1 and self._p2_current[1] - to_location[1] == 0:
            if to_location not in self._used_fences['v'] or (
                    to_location[0], to_location[1]+1) not in self._used_fences['v']:
                return True
        if self._p2_current[0] - to_location[0] == -1 and self._p2_current[1] - to_location[1] == 0:
            if self._p2_current not in self._used_fences['v'] or (
                    self._p2_current[0], self._p2_current[1]+1) not in self._used_fences['v']:
                return True
        if self._p2_current[1] - to_location[1] == 1 and self._p2_current[0] - to_location[0] == 0:
            if (self._p2_current[0]-1, self._p2_current[1]) not in self._used_fences['h'] or \
                    self._p2_current not in self._used_fences['h']:
                return True
        if self._p2_current[1] - to_location[1] == -1 and self._p2_current[0] - to_location[0] == 0:
            if to_location not in self._used_fences['h'] or (
                    to_location[0]-1, to_location[1]) not in self._used_fences['h']:
                return True

        if self._p2_current[0] - to_location[0] == 2 and self._p2_current[1] - to_location[1] == 0:
            if to_location not in self._used_fences['v'] or (to_location[0], to_location[1]+1) not in \
                    self._used_fences['v'] or (to_location[0]+1, to_location[1]) not in self._used_fences['v'] or \
                    (to_location[0]+1, to_location[1]+1) not in self._used_fences['v']:
                return True
        if self._p2_current[0] - to_location[0] == -2 and self._p2_current[1] - to_location[1] == 0:
            if self._p2_current not in self._used_fences['v'] or (self._p2_current[0], self._p2_current[1]+1) not in \
                    self._used_fences['v'] or (self._p2_current[0]+1, self._p2_current[1]) not in self._used_fences or \
                    (self._p2_current[0]+1, self._p2_current[1]+1) not in self._used_fences:
                return True
        if self._p2_current[1] - to_location[1] == 2 and self._p2_current[0] - to_location[0] == 0:
            if (self._p2_current[0] - 1, self._p2_current[1]) not in self._used_fences['h'] or self._p2_current not in \
                    self._used_fences['h'] or (self._p2_current[0], self._p2_current[1]+1) not in self._used_fences or \
                    (self._p2_current[0]+1, self._p2_current[1]+1) not in self._used_fences:
                return True
        if self._p2_current[1] - to_location[1] == -2 and self._p2_current[0] - to_location[0] == 0:
            if to_location not in self._used_fences['h'] or (to_location[0]-1, to_location[1]) not in \
                    self._used_fences['h'] or (to_location[0], to_location[1]-1) not in self._used_fences or \
                    (to_location[0]-1, to_location[1]-1) not in self._used_fences:
                return True

        return False

    def p1_fence_check(self, v_or_h, pos):
        """ checks whether a fence placement by player 1 is valid """
        if self.is_winner(1) is True or self.is_winner(2) is True:
            return False
        if self._p1_fence_count == 0:
            return False
        for coord in self._board_edge:
            if coord[0] != 8 or coord[1] != 0:
                if v_or_h == 'v':
                    self._new_fence = [pos, (pos[0], pos[1] + 1)]
                    for fence in self._used_fences['v']:
                        if self._new_fence[0] not in fence and self._new_fence[1] not in fence:
                            return True
                    if pos not in self._used_fences['h']:
                        return True
                if v_or_h == 'h':
                    self._new_fence = [pos, (pos[0] + 1, pos[1])]
                    for fence in self._used_fences['h']:
                        if self._new_fence[0] not in fence and self._new_fence[1] not in fence:
                            return True
                    if pos not in self._used_fences['v']:
                        return True

        return False

    def p2_fence_check(self, v_or_h, pos):
        """ checks whether a fence placement by player 2 is valid """
        if self.is_winner(1) is True or self.is_winner(2) is True:
            return False
        if self._p2_fence_count == 0:
            return False
        for coord in self._board_edge:
            if coord[0] != 8 or coord[1] != 0:
                if v_or_h == 'v':
                    self._new_fence = [pos, (pos[0], pos[1] + 1)]
                    for fence in self._used_fences['v']:
                        if self._new_fence[0] not in fence and self._new_fence[1] not in fence:
                            return True
                    if pos not in self._used_fences['h']:
                        return True
                if v_or_h == 'h':
                    self._new_fence = [pos, (pos[0] + 1, pos[1])]
                    for fence in self._used_fences['h']:
                        if self._new_fence[0] not in fence and self._new_fence[1] not in fence:
                            return True
                    if pos not in self._used_fences['v']:
                        return True

        return False
