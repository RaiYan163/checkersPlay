import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece
from collections import defaultdict
import numpy as np

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
        self.move_count_without_capture = 0
        self.previous_positions = []

    def winner(self):
        # Check for all pieces captured
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        # Check for no more moves
        if not self.has_legal_moves(RED):
            return WHITE
        if not self.has_legal_moves(WHITE):
            return RED

        # Check for stalemate (threefold repetition)
        if self.is_stalemate():
            return "Draw due to threefold repetition"
        
        # Check for the 10-move rule
        if self.move_count_without_capture >= 30:
            return "Draw due to 30-move rule"
        
        return None

    def has_legal_moves(self, color):
        for piece in self.get_all_pieces(color):
            if self.get_valid_moves(piece):
                return True
        return False

    def is_stalemate(self):
        current_position = self.board_to_string()
        self.previous_positions.append(current_position)
        if self.previous_positions.count(current_position) >= 3:
            return True
        return False

    def board_to_string(self):
        board_string = ''
        for row in self.board:
            for piece in row:
                if piece == 0:
                    board_string += '0'
                elif piece.color == RED:
                    board_string += 'r' if not piece.king else 'R'
                elif piece.color == WHITE:
                    board_string += 'w' if not piece.king else 'W'
        return board_string

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    row = max(r - 3, 0) if step == -1 else min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    row = max(r - 3, 0) if step == -1 else min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    def print_board_array(self):
        board_array = []
        for row in self.board:
            row_array = []
            for piece in row:
                if piece == 0:
                    row_array.append(0)
                else:
                    row_array.append(1 if piece.color == WHITE else -1)  # 1 for WHITE, -1 for RED
            board_array.append(row_array)
        for row in board_array:
            print(row)
        print("\n")

    def to_array(self):
        board_array = []
        for row in self.board:
            row_array = []
            for piece in row:
                if piece == 0:
                    row_array.append(0)
                else:
                    if piece.color == WHITE:
                        row_array.append(2 if piece.king else 1)
                    else:
                        row_array.append(-2 if piece.king else -1)
            board_array.append(row_array)
        return np.array(board_array)

    def from_array(self, array):
        for i in range(ROWS):
            for j in range(COLS):
                value = array[i][j]
                if value == 0:
                    self.board[i][j] = 0
                else:
                    color = WHITE if value > 0 else RED
                    king = abs(value) == 2
                    self.board[i][j] = Piece(i, j, color)
                    if king:
                        self.board[i][j].make_king()
