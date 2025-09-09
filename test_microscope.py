#!/usr/bin/env python

import unittest
import sys
import os

# Add the current directory to the path so we can import microscope
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Game class from microscope module
from microscope import Game


class TestGame(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = Game()
        
    def test_setup_new_game(self):
        """Test that setup_new_game creates the correct initial board state."""
        self.game.setup_new_game()
        
        # Check board size
        self.assertEqual(len(self.game.board), 7)
        self.assertEqual(len(self.game.board[0]), 7)
        
        # Check corner pieces
        self.assertEqual(self.game.board[0][0], 'B')  # Top-left
        self.assertEqual(self.game.board[0][6], 'G')  # Top-right
        self.assertEqual(self.game.board[6][0], 'G')  # Bottom-left
        self.assertEqual(self.game.board[6][6], 'B')  # Bottom-right
        
        # Check that all other squares are empty
        empty_count = 0
        for i in range(7):
            for j in range(7):
                if self.game.board[i][j] == '.':
                    empty_count += 1
        self.assertEqual(empty_count, 45)  # 49 total - 4 corner pieces
        
    def test_boardcopy(self):
        """Test that boardcopy creates an independent copy of the board."""
        self.game.setup_new_game()
        original_board = self.game.board
        copied_board = self.game.boardcopy()
        
        # Check that the copy is equal but not the same object
        self.assertEqual(original_board, copied_board)
        self.assertIsNot(original_board, copied_board)
        
        # Modify the copy and ensure original is unchanged
        copied_board[0][0] = 'X'
        self.assertNotEqual(original_board[0][0], copied_board[0][0])
        
    def test_within1_basic(self):
        """Test within1 method with basic scenarios."""
        self.game.setup_new_game()
        self.game.turn = 'B'
        
        # Test adjacent to corner B piece at (0,0)
        self.assertTrue(self.game.within1(0, 1))  # Right
        self.assertTrue(self.game.within1(1, 0))  # Down
        self.assertTrue(self.game.within1(1, 1))  # Diagonal
        
        # Test not adjacent
        self.assertFalse(self.game.within1(0, 2))  # Two squares away
        self.assertFalse(self.game.within1(2, 2))  # Center of board
        
    def test_within1_edge_cases(self):
        """Test within1 method with edge cases."""
        self.game.setup_new_game()
        self.game.turn = 'B'
        
        # Test corners and edges don't cause index errors
        self.assertFalse(self.game.within1(0, 0))  # Corner with B piece
        self.assertFalse(self.game.within1(3, 3))  # Center with no adjacent pieces
        
    def test_within2_basic(self):
        """Test within2 method returns correct jump positions."""
        self.game.setup_new_game()
        self.game.turn = 'B'
        
        # Test jump positions from corner B piece at (0,0)
        jump_positions = self.game.within2(0, 2)  # Two squares right
        self.assertIn((0, 0), jump_positions)
        
        jump_positions = self.game.within2(2, 0)  # Two squares down
        self.assertIn((0, 0), jump_positions)
        
        jump_positions = self.game.within2(2, 2)  # Two squares diagonal
        self.assertIn((0, 0), jump_positions)
        
    def test_within2_empty_result(self):
        """Test within2 returns empty list when no jumps possible."""
        self.game.setup_new_game()
        self.game.turn = 'B'
        
        # Test position with no possible jumps
        jump_positions = self.game.within2(3, 3)  # Center of board
        self.assertEqual(len(jump_positions), 0)
        
    def test_get_moves_initial_state(self):
        """Test get_moves returns correct moves for initial game state."""
        self.game.setup_new_game()
        self.game.turn = 'B'
        
        moves = self.game.get_moves()
        
        # Should have expand moves adjacent to B pieces and jump moves
        expand_moves = [move for move in moves if move[0] == 'expand']
        jump_moves = [move for move in moves if move[0] == 'jump']
        
        self.assertTrue(len(expand_moves) > 0)
        self.assertTrue(len(jump_moves) > 0)
        
        # Check some specific expected moves
        self.assertIn(('expand', 0, 1), moves)  # Adjacent to (0,0)
        self.assertIn(('expand', 1, 0), moves)  # Adjacent to (0,0)
        
    def test_apply_move_expand(self):
        """Test apply_move correctly handles expand moves."""
        self.game.setup_new_game()
        self.game.turn = 'B'
        
        # Apply an expand move
        new_game = self.game.apply_move(('expand', 1, 1))
        
        # Check that the new position has the piece
        self.assertEqual(new_game.board[1][1], 'B')
        
        # Check that adjacent pieces are converted
        self.assertEqual(new_game.board[0][0], 'B')  # Should remain B
        
        # Check that turn switched
        self.assertEqual(new_game.turn, 'G')
        
    def test_apply_move_jump(self):
        """Test apply_move correctly handles jump moves."""
        self.game.setup_new_game()
        self.game.turn = 'B'
        
        # Apply a jump move
        new_game = self.game.apply_move(('jump', 2, 2, 0, 0))
        
        # Check that the new position has the piece
        self.assertEqual(new_game.board[2][2], 'B')
        
        # Check that the source position is now empty
        self.assertEqual(new_game.board[0][0], '.')
        
        # Check that turn switched
        self.assertEqual(new_game.turn, 'G')
        
    def test_simple_value_basic(self):
        """Test simple_value calculation."""
        self.game.setup_new_game()
        
        # Initial state: 2 B pieces, 2 G pieces
        value = self.game.simple_value()
        self.assertEqual(value, 0)  # 2 - 2 = 0
        
        # Add more B pieces
        self.game.board[1][1] = 'B'
        self.game.board[1][2] = 'B'
        value = self.game.simple_value()
        self.assertEqual(value, 2)  # 4 - 2 = 2
        
    def test_simple_value_edge_cases(self):
        """Test simple_value with edge cases."""
        # Test when B has no pieces
        self.game.board = [['G', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
        value = self.game.simple_value()
        self.assertEqual(value, -10000)
        
        # Test when G has no pieces
        self.game.board = [['B', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
        value = self.game.simple_value()
        self.assertEqual(value, 10000)
        
    def test_value_depth_zero(self):
        """Test value method with depth 0 (should equal simple_value)."""
        self.game.setup_new_game()
        
        simple_val = self.game.simple_value()
        depth_zero_val = self.game.value(0)
        
        self.assertEqual(simple_val, depth_zero_val)
        
    def test_new_board(self):
        """Test new_board method sets board from string."""
        board_string = "BG.....\nGB.....\n......."
        self.game.new_board(board_string)
        
        expected_board = [['B', 'G', '.', '.', '.', '.', '.'], 
                         ['G', 'B', '.', '.', '.', '.', '.'], 
                         ['.', '.', '.', '.', '.', '.', '.']]
        self.assertEqual(self.game.board, expected_board)
        
    def test_next_move_returns_valid_move(self):
        """Test that next_move returns a valid move."""
        self.game.setup_new_game()
        self.game.turn = 'B'
        
        move = self.game.next_move()
        
        # Should return a valid move tuple
        self.assertIsNotNone(move)
        self.assertIn(move[0], ['expand', 'jump'])
        
        # Should be in the list of available moves
        available_moves = self.game.get_moves()
        self.assertIn(move, available_moves)
        
    def test_next_move_no_moves_available(self):
        """Test next_move when no moves are available."""
        # Create a board state with no moves for current player
        self.game.board = [['G'] * 7 for _ in range(7)]
        self.game.turn = 'B'
        
        move = self.game.next_move()
        self.assertIsNone(move)
        
    def test_game_state_consistency(self):
        """Test that game state remains consistent after moves."""
        self.game.setup_new_game()
        original_turn = self.game.turn
        
        # Apply a move and check consistency
        moves = self.game.get_moves()
        if moves:
            new_game = self.game.apply_move(moves[0])
            
            # Turn should have switched
            self.assertNotEqual(original_turn, new_game.turn)
            
            # Board should be different
            self.assertNotEqual(self.game.board, new_game.board)
            
            # Original game should be unchanged
            self.assertEqual(self.game.turn, original_turn)
            
    def test_piece_conversion_on_move(self):
        """Test that pieces are correctly converted when making moves."""
        # Set up a specific board state using the full 7x7 board
        self.game.setup_new_game()
        # Place a G piece adjacent to where we'll move
        self.game.board[0][1] = 'G'
        self.game.turn = 'B'
        
        # Make a move that should convert the G piece
        new_game = self.game.apply_move(('expand', 0, 2))
        
        # Check that the G piece at (0,1) was converted to B
        self.assertEqual(new_game.board[0][1], 'B')
        self.assertEqual(new_game.board[0][2], 'B')


class TestGameIntegration(unittest.TestCase):
    """Integration tests for the Game class."""
    
    def test_full_game_simulation(self):
        """Test a short game simulation to ensure everything works together."""
        game = Game()
        game.setup_new_game()
        game.search_depth = 1  # Use shallow search to avoid long computation
        
        # Play a few moves
        for _ in range(3):
            move = game.next_move()
            if move is None:
                break
            game = game.apply_move(move)
            
            # Ensure game state is valid
            self.assertIn(game.turn, ['B', 'G'])
            self.assertIsInstance(game.board, list)
            self.assertEqual(len(game.board), 7)
            
    def test_board_string_representation(self):
        """Test that the string representation works correctly."""
        game = Game()
        game.setup_new_game()
        
        str_repr = str(game)
        
        # Should contain turn information
        self.assertIn('Turn:', str_repr)
        self.assertIn('Value:', str_repr)
        
        # Should contain board representation
        self.assertIn('B', str_repr)
        self.assertIn('G', str_repr)
        self.assertIn('.', str_repr)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)