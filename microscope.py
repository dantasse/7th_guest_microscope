#!/usr/bin/env python

# 

import argparse, csv, collections, pprint
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# parser.add_argument(arg, help=' ')
args = parser.parse_args()

# class Move:
#     def __init__(self)

class Game:
    size = 7
    turn = 'B'
    board = []#[['.'] * size] * size
    def __init__(self):
        for i in range(self.size):
            self.board.append(['.'] * self.size)
        self.board[0][0] = 'B'
        self.board[0][self.size - 1] = 'G'
        self.board[self.size - 1][0] = 'G'
        self.board[self.size - 1][self.size - 1] = 'B'

    def __str__(self):
        retval = 'Turn: ' + self.turn + '\n';
        retval += 'Value: ' + str(self.value()) + '\n';
        for row in self.board:
            retval += (''.join(row) + '\n')
        return retval

    def value(self):
        val = 0
        for row in self.board:
            for char in row:
                if char == 'B':
                    val += 1
                elif char == 'G':
                    val -= 1
        return val

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

    def apply_move(self, move):
        """ a move will either be 'extend', target_i, target_j, or:
        'jump', target_i, target_j, source_i, source_j"""
        target_i = move[1]
        target_j = move[2]
        self.board[target_i][target_j] = self.turn
        if target_i > 0 and target_j > 0 and self.board[target_i-1][target_j-1] != '.':
            self.board[target_i-1][target_j-1] = self.turn
        if target_i > 0 and self.board[target_i-1][target_j] != '.':
            self.board[target_i-1][target_j] = self.turn
        if target_i > 0 and target_j < self.size-1 and self.board[target_i-1][target_j+1] != '.':
            self.board[target_i-1][target_j+1] = self.turn
        if target_j > 0 and self.board[target_i][target_j-1] != '.':
            self.board[target_i][target_j-1] = self.turn
        if target_j < self.size-1 and self.board[target_i][target_j+1] != '.':
            self.board[target_i][target_j+1] = self.turn
        if target_i < self.size-1 and target_j > 0 and self.board[target_i+1][target_j-1] != '.':
            self.board[target_i+1][target_j-1] = self.turn
        if target_i < self.size-1 and self.board[target_i+1][target_j] != '.':
            self.board[target_i+1][target_j] = self.turn
        if target_i < self.size-1 and target_j < self.size-1 and self.board[target_i+1][target_j+1] != '.':
            self.board[target_i+1][target_j+1] = self.turn

        if move[0] == 'jump':
            self.board[move[3]][move[4]] = '.'
        
        if self.turn == 'B':
            self.turn = 'G'
        elif self.turn == 'G':
            self.turn = 'B'


a = Game()
print a
moves = a.get_moves()
print a.get_moves()
a.apply_move(moves[2])
print a
moves = a.get_moves()
print moves
a.apply_move(moves[0])
print a
