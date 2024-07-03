import numpy as np
import random

# Function to generate all possible moves for the AI pieces, including captures
def generate_possible_moves(board_state, ai_piece=1, opponent_piece=-1):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Possible move directions
    capture_directions = [(2 * d[0], 2 * d[1]) for d in directions]  # Capture move directions

    def is_within_bounds(x, y):
        return 0 <= x < board_state.shape[0] and 0 <= y < board_state.shape[1]

    possible_moves = []

    for i in range(board_state.shape[0]):
        for j in range(board_state.shape[1]):
            if board_state[i, j] == ai_piece:
                # Check for normal moves
                for direction in directions:
                    new_i, new_j = i + direction[0], j + direction[1]
                    if is_within_bounds(new_i, new_j) and board_state[new_i, new_j] == 0:
                        new_board = board_state.copy()
                        new_board[i, j] = 0
                        new_board[new_i, new_j] = ai_piece
                        move = ((i, j), (new_i, new_j), new_board)
                        possible_moves.append(move)
                # Check for capture moves
                for capture_direction in capture_directions:
                    mid_i, mid_j = i + capture_direction[0] // 2, j + capture_direction[1] // 2
                    new_i, new_j = i + capture_direction[0], j + capture_direction[1]
                    if (
                        is_within_bounds(mid_i, mid_j) and is_within_bounds(new_i, new_j) and
                        board_state[mid_i, mid_j] == opponent_piece and board_state[new_i, new_j] == 0
                    ):
                        new_board = board_state.copy()
                        new_board[i, j] = 0
                        new_board[mid_i, mid_j] = 0
                        new_board[new_i, new_j] = ai_piece
                        move = ((i, j), (new_i, new_j), new_board)
                        possible_moves.append(move)

    return possible_moves

# Function to calculate fitness of a move
def calculate_fitness(board, original_board):
    ai_piece = 1
    opponent_piece = -1
    fitness = 0

    # 1. Capturing Opponent Pieces
    original_opponent_pieces = np.sum(original_board == opponent_piece)
    new_opponent_pieces = np.sum(board == opponent_piece)
    captured_pieces = original_opponent_pieces - new_opponent_pieces
    fitness += captured_pieces * 10

    # 2. Improving Position
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] == ai_piece:
                # Moving closer to becoming a king
                fitness += (board.shape[0] - i) * 1
                # Control the center
                if 2 <= i <= 5 and 2 <= j <= 5:
                    fitness += 2

    # 3. Avoiding Capture
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] == ai_piece:
                for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    if 0 <= i + di < board.shape[0] and 0 <= j + dj < board.shape[1]:
                        if board[i + di, j + dj] == opponent_piece:
                            if 0 <= i - di < board.shape[0] and 0 <= j - dj < board.shape[1] and board[i - di, j - dj] == 0:
                                fitness -= 5

    # 4. Mobility
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] == ai_piece:
                for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    if 0 <= i + di < board.shape[0] and 0 <= j + dj < board.shape[1]:
                        if board[i + di, j + dj] == 0:
                            fitness += 1

    return fitness

# Rank Selection
def rank_selection(moves_with_fitness, num_selections):
    # Sort moves based on fitness
    sorted_moves = sorted(moves_with_fitness, key=lambda x: x[1], reverse=True)
    total_rank = sum(range(1, len(sorted_moves) + 1))
    rank_probabilities = [(rank + 1) / total_rank for rank in range(len(sorted_moves))]
    
    # Create cumulative probability distribution
    cumulative_probabilities = np.cumsum(rank_probabilities)

    # Select moves based on rank probabilities
    selected_moves = []
    for _ in range(num_selections):
        r = random.random()
        for i, cumulative_probability in enumerate(cumulative_probabilities):
            if r <= cumulative_probability:
                selected_moves.append(sorted_moves[i][0])
                break

    return selected_moves

# Function to perform crossover between two binary strings
def crossover_binary(bin1, bin2):
    crossover_point = random.randint(1, len(bin1) - 1)
    offspring1 = bin1[:crossover_point] + bin2[crossover_point:]
    offspring2 = bin2[:crossover_point] + bin1[crossover_point:]
    return offspring1, offspring2

# Function to perform mutation on a binary string
def mutate_binary(bin_str, mutation_rate=0.01):
    bin_list = list(bin_str)
    for i in range(len(bin_list)):
        if random.random() < mutation_rate:
            bin_list[i] = '1' if bin_list[i] == '0' else '0'
    return ''.join(bin_list)

# Main genetic algorithm function
def genetic_algorithm_move(board_state):
    best_move = None
    best_fitness = float('-inf')

    iterations = 0
    max_iterations = 20

    while iterations < max_iterations:
        iterations += 1

        # Generate possible moves
        possible_moves = generate_possible_moves(board_state)

        # Check if there are no possible moves
        if not possible_moves:
            print("No possible moves available. Terminating.")
            break

        # Check if there is only one possible move
        if len(possible_moves) == 1:
            best_move = possible_moves[0]
            best_fitness = calculate_fitness(best_move[2], board_state)
            print("Only one possible move available. Terminating.")
            break

        # Calculate fitness for all possible moves
        fitness_array = []
        moves_with_fitness = []

        for move in possible_moves:
            fitness = calculate_fitness(move[2], board_state)
            fitness_array.append(fitness)
            moves_with_fitness.append((move, fitness))

        # Select 2 moves with the highest fitness using rank selection
        selected_population_1 = rank_selection(moves_with_fitness, 2)

        # Extract indices of the selected moves
        selected_indices = []
        for move in selected_population_1:
            index = possible_moves.index(move)
            selected_indices.append(index)

        # Convert indices to binary
        max_index = len(possible_moves) - 1
        bit_length = len(bin(max_index)[2:])  # Determine the number of bits needed
        binary_indices = [bin(index)[2:].zfill(bit_length) for index in selected_indices]

        # Perform crossover and mutation
        while True:
            offspring1, offspring2 = crossover_binary(binary_indices[0], binary_indices[1])
            offspring1 = mutate_binary(offspring1)
            offspring2 = mutate_binary(offspring2)

            offspring_indices = [int(offspring1, 2), int(offspring2, 2)]
            if all(index <= max_index for index in offspring_indices):
                break

        # Generate offspring moves from indices
        offspring_moves = [possible_moves[index] for index in offspring_indices]

        # Evaluate the fitness of the offspring
        for move in offspring_moves:
            fitness = calculate_fitness(move[2], board_state)
            if fitness > best_fitness:
                best_fitness = fitness
                best_move = move

    return best_move
