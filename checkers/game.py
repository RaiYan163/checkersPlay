import pygame
import numpy as np
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board
from collections import defaultdict

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.player_moves = 0
        self.ai_moves = 0
        self.moves_without_capture = 0  # Counter for moves without capture
        self.move_history = []  # List to store move history for threefold repetition

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.player_moves = 0
        self.ai_moves = 0
        self.moves_without_capture = 0  # Reset the counter
        self.move_history = []  # Reset move history

    def winner(self):
        # Check for all pieces captured
        if self.board.red_left <= 0:
            return WHITE
        elif self.board.white_left <= 0:
            return RED

        # Check for no more moves
        if not self.board.has_legal_moves(RED):
            return WHITE
        if not self.board.has_legal_moves(WHITE):
            return RED

        # Check for threefold repetition
        position_counts = defaultdict(int)
        for pos in self.move_history:
            position_counts[pos] += 1
            if position_counts[pos] >= 3:
                return "Draw due to threefold repetition"
        
        # Check for the 10-move rule
        if self.moves_without_capture >= 30:
            return "Draw due to 30-move rule"
        
        return None

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
                self.moves_without_capture = 0  # Reset counter if a piece is captured
            else:
                self.moves_without_capture += 1  # Increment counter if no capture

            # Increment move counts before changing the turn
            if self.turn == RED:
                self.player_moves += 1
            else:
                self.ai_moves += 1
            
            # Save board state to move history for threefold repetition
            self.move_history.append(self.board_to_string())
            
            # Print the current board state after the player's move
            self.print_board_as_array()
            
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        self.turn = WHITE if self.turn == RED else RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.ai_moves += 1  # Increment AI moves
        self.move_history.append(self.board_to_string())  # Save board state to move history
    
        # Increment or reset move counter based on whether a capture occurred
        if self.board.move_count_without_capture >= 30:
            self.board.move_count_without_capture = 0  # Reset counter if a piece is captured
        else:
            self.board.move_count_without_capture += 1  # Increment counter if no capture

        self.change_turn()

    def board_to_string(self):
        # Convert the board state to a string representation
        board_string = ''
        for row in self.board.board:
            for piece in row:
                if piece == 0:
                    board_string += '0'
                elif piece.color == RED:
                    board_string += 'r' if not piece.king else 'R'
                elif piece.color == WHITE:
                    board_string += 'w' if not piece.king else 'W'
        return board_string

    def print_board_as_array(self):
        board_array = np.zeros((8, 8), dtype=int)
        for i, row in enumerate(self.board.board):
            for j, piece in enumerate(row):
                if piece == 0:
                    board_array[i, j] = 0
                elif piece.color == RED:
                    board_array[i, j] = -1 if not piece.king else -2
                elif piece.color == WHITE:
                    board_array[i, j] = 1 if not piece.king else 2
        print(board_array)
