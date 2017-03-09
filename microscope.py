#!/usr/bin/env python

# 

import argparse, csv, collections, pprint
# from copy import deepcopy
import copy
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--board_size', type=int, default=7, help=' ')
parser.add_argument('--search_depth', type=int, default=3, help=' ')
args = parser.parse_args()

class Game:
    size = args.board_size
    turn = 'B'
    board = []
    search_depth = args.search_depth

    def __init__(self):
        pass

    def setup_new_game(self):
        for i in range(self.size):
            self.board.append(['.'] * self.size)
        self.board[0][0] = 'B'
        self.board[0][self.size - 1] = 'G'
        self.board[self.size - 1][0] = 'G'
        self.board[self.size - 1][self.size - 1] = 'B'

    def __str__(self):
        retval = 'Turn: ' + self.turn + '\n';
        retval += 'Value: ' + str(self.value(0)) + '\n';
        for row in self.board:
            retval += (''.join(row) + '\n')
        return retval
    def within1(self, i, j):
        """ Read this as: if there is a |self.turn| piece within 1 of board[i][j]"""
        if i > 0 and j > 0 and self.board[i-1][j-1] == self.turn:
            return True
        elif i > 0 and self.board[i-1][j] == self.turn:
            return True
        elif i > 0 and j < self.size-1 and self.board[i-1][j+1] == self.turn:
            return True
        elif j > 0 and self.board[i][j-1] == self.turn:
            return True
        elif j < self.size-1 and self.board[i][j+1] == self.turn:
            return True
        elif i < self.size-1 and j > 0 and self.board[i+1][j-1] == self.turn:
            return True
        elif i < self.size-1 and self.board[i+1][j] == self.turn:
            return True
        elif i < self.size-1 and j < self.size-1 and self.board[i+1][j+1] == self.turn:
            return True
        return False

    def within2(self, i, j):
        """ Read this as: return all squares that have a |self.turn| piece
        that can jump to board[i][j]"""
        squares = []
        if i > 1 and j > 1 and self.board[i-2][j-2] == self.turn:
            squares.append((i-2, j-2))
        if i > 1 and j > 0 and self.board[i-2][j-1] == self.turn:
            squares.append((i-2, j-1))
        if i > 1 and self.board[i-2][j] == self.turn:
            squares.append((i-2, j))
        if i > 1 and j < self.size-1 and self.board[i-2][j+1] == self.turn:
            squares.append((i-2, j+1))
        if i > 1 and j < self.size-2 and self.board[i-2][j+2] == self.turn:
            squares.append((i-2, j+2))
        if i > 0 and j > 1 and self.board[i-1][j-2] == self.turn:
            squares.append((i-1, j-2))
        if i > 0 and j < self.size-2 and self.board[i-1][j+2] == self.turn:
            squares.append((i-1, j+2))
        if j > 1 and self.board[i][j-2] == self.turn:
            squares.append((i, j-2))
        if j < self.size-2 and self.board[i][j+2] == self.turn:
            squares.append((i, j+2))
        if i < self.size-1 and j > 1 and self.board[i+1][j-2] == self.turn:
            squares.append((i+1, j-2))
        if i < self.size-1 and j < self.size-2 and self.board[i+1][j+2] == self.turn:
            squares.append((i+1, j+2))
        if i < self.size-2 and j > 1 and self.board[i+2][j-2] == self.turn:
            squares.append((i+2, j-2))
        if i < self.size-2 and j > 0 and self.board[i+2][j-1] == self.turn:
            squares.append((i+2, j-1))
        if i < self.size-2 and self.board[i+2][j] == self.turn:
            squares.append((i+2, j))
        if i < self.size-2 and j < self.size-1 and self.board[i+2][j+1] == self.turn:
            squares.append((i+2, j+1))
        if i < self.size-2 and j < self.size-2 and self.board[i+2][j+2] == self.turn:
            squares.append((i+2, j+2))
        
        return squares

    def get_moves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == '.':
                    if self.within1(i, j):
                        moves.append(('expand', i, j))
                    for (move_i, move_j) in self.within2(i, j):
                        moves.append(('jump', i, j, move_i, move_j))
        return moves

    def boardcopy(self):
        newboard = []
        for row in self.board:
            newboard.append(copy.copy(row))
        return newboard

    def apply_move(self, move):
        """ Returns a new game, same as the old one, but with one move applied.
        A move will either be 'extend', target_i, target_j, or:
        'jump', target_i, target_j, source_i, source_j"""

        newboard = self.boardcopy()
        target_i = move[1]
        target_j = move[2]
        newboard[target_i][target_j] = self.turn
        if target_i > 0 and target_j > 0 and self.board[target_i-1][target_j-1] != '.':
            newboard[target_i-1][target_j-1] = self.turn
        if target_i > 0 and self.board[target_i-1][target_j] != '.':
            newboard[target_i-1][target_j] = self.turn
        if target_i > 0 and target_j < self.size-1 and self.board[target_i-1][target_j+1] != '.':
            newboard[target_i-1][target_j+1] = self.turn
        if target_j > 0 and self.board[target_i][target_j-1] != '.':
            newboard[target_i][target_j-1] = self.turn
        if target_j < self.size-1 and self.board[target_i][target_j+1] != '.':
            newboard[target_i][target_j+1] = self.turn
        if target_i < self.size-1 and target_j > 0 and self.board[target_i+1][target_j-1] != '.':
            newboard[target_i+1][target_j-1] = self.turn
        if target_i < self.size-1 and self.board[target_i+1][target_j] != '.':
            newboard[target_i+1][target_j] = self.turn
        if target_i < self.size-1 and target_j < self.size-1 and self.board[target_i+1][target_j+1] != '.':
            newboard[target_i+1][target_j+1] = self.turn

        if move[0] == 'jump':
            newboard[move[3]][move[4]] = '.'
        
        if self.turn == 'B':
            newturn = 'G'
        elif self.turn == 'G':
            newturn = 'B'

        newgame = Game()
        newgame.turn = newturn
        newgame.board = newboard
        return newgame

    def simple_value(self):
        """ Value taking no future turns into account; just: how good is this
        board right now."""
        num_bs = num_gs = 0
        for row in self.board:
            for char in row:
                if char == 'B':
                    num_bs += 1
                elif char == 'G':
                    num_gs += 1
        if num_bs == 0:
            return -10000
        elif num_gs == 0:
            return 10000
        else:
            return num_bs - num_gs

    def value(self, depth):
        """ Returns the value of the current board state."""
        if depth == 0:
            return self.simple_value()
        else:
            all_moves = self.get_moves()
            if len(all_moves) == 0:
                return 10000 if self.turn == 'G' else -10000
            moves_scores = {}
            for move in all_moves:
                moves_scores[move] = self.apply_move(move).value(depth-1)
            if self.turn == 'B':
                best_move_score = max(moves_scores.items(), key=lambda x: x[1])
                return best_move_score[1]
            elif self.turn == 'G':
                worst_move_score = min(moves_scores.items(), key=lambda x: x[1])
                return worst_move_score[1]

    def next_move(self): 
        all_moves = self.get_moves()
        if len(all_moves) == 0:
            return None
            # return [] if self.turn == 'G' else 
        moves_scores = {}
        for move in all_moves:
            moves_scores[move] = self.apply_move(move).value(self.search_depth)
        if self.turn == 'B':
            best_move_score = max(moves_scores.items(), key=lambda x: x[1])
            best_move = best_move_score[0]
            return best_move
            # return self.apply_move(best_move)
        elif self.turn == 'G':
            worst_move_score = min(moves_scores.items(), key=lambda x: x[1])
            return worst_move_score[0]
            # return self.apply_move(worst_move_score[0])

a = Game()
a.setup_new_game()

print a

for i in range(100):
    move = a.next_move()
    print a.turn, move
    a = a.apply_move(move)
    print a

