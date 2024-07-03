import pygame
import sys
import numpy as np
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minmax.algorithm import minimax
from checkers.board import Board
from genetic.genetic_algo import genetic_algorithm_move  # Import the genetic algorithm function

FPS = 60

# Initialize Pygame and its font module
pygame.init()
pygame.font.init()

# Define dimensions for the move count section
MOVE_WIDTH = 300  # Increase the width for the move count section
TOTAL_WIDTH = WIDTH + MOVE_WIDTH

# Create the main window with additional width for the move count section
WIN = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
pygame.display.set_caption('Checker Board')

# Create surfaces for the game and move count sections
game_surface = pygame.Surface((WIDTH, HEIGHT))
move_surface = pygame.Surface((MOVE_WIDTH, HEIGHT))

def draw_text(surface, text, font, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def main_menu():
    menu = True
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 50)
    
    button_width = 300
    button_height = 60

    while menu:
        WIN.fill((0, 0, 0))
        
        # Define button rectangles with centered x-coordinate
        new_game_button = pygame.Rect(TOTAL_WIDTH // 2 - button_width // 2, HEIGHT // 3, button_width, button_height)
        leaderboard_button = pygame.Rect(TOTAL_WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
        exit_button = pygame.Rect(TOTAL_WIDTH // 2 - button_width // 2, 2 * HEIGHT // 3, button_width, button_height)
        
        # Check if mouse is over a button
        mouse_pos = pygame.mouse.get_pos()
        if new_game_button.collidepoint(mouse_pos):
            new_game_color = (255, 255, 255)  # White background
            new_game_text_color = (0, 200, 0)  # Green text
        else:
            new_game_color = (0, 200, 0)  # Green background
            new_game_text_color = (255, 255, 255)  # White text
        
        if leaderboard_button.collidepoint(mouse_pos):
            leaderboard_color = (255, 255, 255)  # White background
            leaderboard_text_color = (0, 200, 0)  # Green text
        else:
            leaderboard_color = (0, 200, 0)  # Green background
            leaderboard_text_color = (255, 255, 255)  # White text
        
        if exit_button.collidepoint(mouse_pos):
            exit_color = (255, 255, 255)  # White background
            exit_text_color = (0, 200, 0)  # Green text
        else:
            exit_color = (0, 200, 0)  # Green background
            exit_text_color = (255, 255, 255)  # White text
        
        # Draw buttons with appropriate colors
        pygame.draw.rect(WIN, new_game_color, new_game_button)
        pygame.draw.rect(WIN, leaderboard_color, leaderboard_button)
        pygame.draw.rect(WIN, exit_color, exit_button)
        
        # Center the title text
        draw_text(WIN, 'Checkers', font, (255, 255, 255), pygame.Rect(TOTAL_WIDTH // 2 - 100, HEIGHT // 6, 200, 50))
        # Center the button text
        draw_text(WIN, 'New Game', font_small, new_game_text_color, new_game_button)
        draw_text(WIN, 'Leaderboard', font_small, leaderboard_text_color, leaderboard_button)
        draw_text(WIN, 'Exit', font_small, exit_text_color, exit_button)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    pygame.draw.rect(WIN, (255, 255, 255), new_game_button)  # Set button to white when clicked
                    draw_text(WIN, 'New Game', font_small, (0, 200, 0), new_game_button)  # Green text
                    pygame.display.flip()
                    pygame.time.wait(200)  # Wait for a short duration to show the effect
                    method_menu()  # Call method menu
                    menu = False
                elif leaderboard_button.collidepoint(event.pos):
                    pygame.draw.rect(WIN, (255, 255, 255), leaderboard_button)  # Set button to white when clicked
                    draw_text(WIN, 'Leaderboard', font_small, (0, 200, 0), leaderboard_button)  # Green text
                    pygame.display.flip()
                    pygame.time.wait(200)  # Wait for a short duration to show the effect
                    pass  # Implement leaderboard functionality here
                elif exit_button.collidepoint(event.pos):
                    pygame.draw.rect(WIN, (255, 255, 255), exit_button)  # Set button to white when clicked
                    draw_text(WIN, 'Exit', font_small, (0, 200, 0), exit_button)  # Green text
                    pygame.display.flip()
                    pygame.time.wait(200)  # Wait for a short duration to show the effect
                    pygame.quit()
                    sys.exit()

def method_menu():
    menu = True
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 50)
    font_medium = pygame.font.Font(None, 60)
    
    button_width = 300
    button_height = 60

    while menu:
        WIN.fill((0, 0, 0))
        
        # Define the prompt text rectangle
        prompt_text_rect = pygame.Rect(TOTAL_WIDTH // 2 - 200, HEIGHT // 6, 400, 50)
        
        # Define button rectangles with centered x-coordinate
        alpha_minimax_button = pygame.Rect(TOTAL_WIDTH // 2 - button_width // 2, HEIGHT // 3, button_width, button_height)
        genetic_button = pygame.Rect(TOTAL_WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
        
        # Check if mouse is over a button
        mouse_pos = pygame.mouse.get_pos()
        if alpha_minimax_button.collidepoint(mouse_pos):
            alpha_minimax_color = (255, 255, 255)  # White background
            alpha_minimax_text_color = (0, 200, 0)  # Green text
        else:
            alpha_minimax_color = (0, 200, 0)  # Green background
            alpha_minimax_text_color = (255, 255, 255)  # White text
        
        if genetic_button.collidepoint(mouse_pos):
            genetic_color = (255, 255, 255)  # White background
            genetic_text_color = (0, 200, 0)  # Green text
        else:
            genetic_color = (0, 200, 0)  # Green background
            genetic_text_color = (255, 255, 255)  # White text
        
        # Draw the prompt text
        draw_text(WIN, 'Which method to use?', font_medium, (255, 255, 255), prompt_text_rect)
        
        # Draw buttons with appropriate colors
        pygame.draw.rect(WIN, alpha_minimax_color, alpha_minimax_button)
        pygame.draw.rect(WIN, genetic_color, genetic_button)
        
        draw_text(WIN, 'AlphaMnMx', font_small, alpha_minimax_text_color, alpha_minimax_button)
        draw_text(WIN, 'Genetic', font_small, genetic_text_color, genetic_button)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if alpha_minimax_button.collidepoint(event.pos):
                    pygame.draw.rect(WIN, (255, 255, 255), alpha_minimax_button)  # Set button to white when clicked
                    draw_text(WIN, 'AlphaMnMx', font_small, (0, 200, 0), alpha_minimax_button)  # Green text
                    pygame.display.flip()
                    pygame.time.wait(200)  # Wait for a short duration to show the effect
                    menu = False
                    difficulty_menu('alpha_minimax')  # Call difficulty menu for AlphaMinimax
                elif genetic_button.collidepoint(event.pos):
                    pygame.draw.rect(WIN, (255, 255, 255), genetic_button)  # Set button to white when clicked
                    draw_text(WIN, 'Genetic', font_small, (0, 200, 0), genetic_button)  # Green text
                    pygame.display.flip()
                    pygame.time.wait(200)  # Wait for a short duration to show the effect
                    menu = False
                    main(0, 'genetic')  # Directly start the game with genetic algorithm

def difficulty_menu(selected_algorithm):
    menu = True
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 50)
    
    button_width = 300
    button_height = 60

    while menu:
        WIN.fill((0, 0, 0))
        
        # Define button rectangles with centered x-coordinate
        easy_button = pygame.Rect(TOTAL_WIDTH // 2 - button_width // 2, HEIGHT // 3, button_width, button_height)
        medium_button = pygame.Rect(TOTAL_WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
        hard_button = pygame.Rect(TOTAL_WIDTH // 2 - button_width // 2, 2 * HEIGHT // 3, button_width, button_height)
        
        # Check if mouse is over a button
        mouse_pos = pygame.mouse.get_pos()
        if easy_button.collidepoint(mouse_pos):
            easy_color = (255, 255, 255)  # White background
            easy_text_color = (0, 200, 0)  # Green text
        else:
            easy_color = (0, 200, 0)  # Green background
            easy_text_color = (255, 255, 255)  # White text
        
        if medium_button.collidepoint(mouse_pos):
            medium_color = (255, 255, 255)  # White background
            medium_text_color = (0, 200, 0)  # Green text
        else:
            medium_color = (0, 200, 0)  # Green background
            medium_text_color = (255, 255, 255)  # White text
        
        if hard_button.collidepoint(mouse_pos):
            hard_color = (255, 255, 255)  # White background
            hard_text_color = (0, 200, 0)  # Green text
        else:
            hard_color = (0, 200, 0)  # Green background
            hard_text_color = (255, 255, 255)  # White text
        
        # Draw buttons with appropriate colors
        pygame.draw.rect(WIN, easy_color, easy_button)
        pygame.draw.rect(WIN, medium_color, medium_button)
        pygame.draw.rect(WIN, hard_color, hard_button)
        
        draw_text(WIN, 'Easy', font_small, easy_text_color, easy_button)
        draw_text(WIN, 'Medium', font_small, medium_text_color, medium_button)
        draw_text(WIN, 'Hard', font_small, hard_text_color, hard_button)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    pygame.draw.rect(WIN, (255, 255, 255), easy_button)  # Set button to white when clicked
                    draw_text(WIN, 'Easy', font_small, (0, 200, 0), easy_button)  # Green text
                    pygame.display.flip()
                    pygame.time.wait(200)  # Wait for a short duration to show the effect
                    menu = False
                    main(3, selected_algorithm)  # Start game with easy difficulty
                elif medium_button.collidepoint(event.pos):
                    pygame.draw.rect(WIN, (255, 255, 255), medium_button)  # Set button to white when clicked
                    draw_text(WIN, 'Medium', font_small, (0, 200, 0), medium_button)  # Green text
                    pygame.display.flip()
                    pygame.time.wait(200)  # Wait for a short duration to show the effect
                    menu = False
                    main(4, selected_algorithm)  # Start game with medium difficulty
                elif hard_button.collidepoint(event.pos):
                    pygame.draw.rect(WIN, (255, 255, 255), hard_button)  # Set button to white when clicked
                    draw_text(WIN, 'Hard', font_small, (0, 200, 0), hard_button)  # Green text
                    pygame.display.flip()
                    pygame.time.wait(200)  # Wait for a short duration to show the effect
                    menu = False
                    main(5, selected_algorithm)  # Start game with hard difficulty

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def display_moves(game, font, font_small):
    move_surface.fill((50, 50, 50))  # Background color for move count section
    player_moves_text = f"Player Moves: {game.player_moves}"
    ai_moves_text = f"AI Moves: {game.ai_moves}"
    player_moves_surface = font.render(player_moves_text, True, (255, 255, 255))
    ai_moves_surface = font.render(ai_moves_text, True, (255, 255, 255))
    move_surface.blit(player_moves_surface, (20, 50))
    move_surface.blit(ai_moves_surface, (20, 100))
    
    # Define button dimensions and positions
    button_width = 200
    button_height = 60
    return_button = pygame.Rect(50, HEIGHT - 150, button_width, button_height)
    restart_button = pygame.Rect(50, HEIGHT - 70, button_width, button_height)
    
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    
    # Check if mouse is over the return button
    if return_button.collidepoint(mouse_pos):
        return_button_color = (255, 255, 255)  # White background
        return_text_color = (255, 0, 0)  # Red text
    else:
        return_button_color = (255, 255, 255)  # White background
        return_text_color = (0, 0, 0)  # Black text
    
    # Check if mouse is over the restart button
    if restart_button.collidepoint(mouse_pos):
        restart_button_color = (255, 255, 255)  # White background
        restart_text_color = (255, 0, 0)  # Red text
    else:
        restart_button_color = (255, 255, 255)  # White background
        restart_text_color = (0, 0, 0)  # Black text
    
    # Draw buttons
    pygame.draw.rect(move_surface, return_button_color, return_button)  # Return button
    pygame.draw.rect(move_surface, restart_button_color, restart_button)  # Restart button

    draw_text(move_surface, 'Return', font_small, return_text_color, return_button)  # Return button text
    draw_text(move_surface, 'Restart', font_small, restart_text_color, restart_button)  # Restart button text

def main(difficulty=3, algorithm='alpha_minimax'):
    run = True
    clock = pygame.time.Clock()
    board = Board()
    game = Game(game_surface)
    
    # Font for the move count section and buttons
    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 50)
    
    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            if algorithm == 'alpha_minimax':
                value, new_board = minimax(game.get_board(), difficulty, float('-inf'), float('inf'), True, game)
            elif algorithm == 'genetic':
                board_array = game.get_board().to_array()  # Assuming you have a to_array method in Board
                best_move = genetic_algorithm_move(board_array)
                new_board = Board()  # Assuming you have a method to create a Board from an array
                new_board.from_array(best_move[2])  # Update the board with the best move
            game.ai_move(new_board)

        winner = game.winner()
        if winner is not None:
            print(winner)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Define button dimensions and positions
                button_width = 200
                button_height = 60
                return_button = pygame.Rect(WIDTH + 50, HEIGHT - 150, button_width, button_height)
                restart_button = pygame.Rect(WIDTH + 50, HEIGHT - 70, button_width, button_height)
                if return_button.collidepoint(pos):
                    main_menu()  # Call the main menu
                    return
                if restart_button.collidepoint(pos):
                    game.reset()
                if pos[0] < WIDTH:  # Ensure clicks are within the game board area
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

        game.update()
        display_moves(game, font, font_small)
        
        # Blit the game surface and move count surface onto the main window
        WIN.blit(game_surface, (0, 0))
        WIN.blit(move_surface, (WIDTH, 0))
        pygame.display.flip()
    
    pygame.quit()

main_menu()
