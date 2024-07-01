import pygame
import sys
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minmax.algorithm import minimax
from checkers.board import Board

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
        
        # Define button rectangles
        new_game_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//3, button_width, button_height)
        leaderboard_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2, button_width, button_height)
        exit_button = pygame.Rect(WIDTH//2 - button_width//2, 2*HEIGHT//3, button_width, button_height)
        
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
        
        draw_text(WIN, 'Checkers', font, (255, 255, 255), pygame.Rect(WIDTH//2 - 100, HEIGHT//6, 200, 50))
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
                    difficulty_menu()  # Call difficulty menu
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

def difficulty_menu():
    menu = True
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 50)
    
    button_width = 300
    button_height = 60

    while menu:
        WIN.fill((0, 0, 0))
        
        # Define button rectangles
        easy_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//3, button_width, button_height)
        medium_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2, button_width, button_height)
        hard_button = pygame.Rect(WIDTH//2 - button_width//2, 2*HEIGHT//3, button_width, button_height)
        
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
                    main(3)  # Start game with easy difficulty
                elif medium_button.collidepoint(event.pos):
                    pygame.draw.rect(WIN, (255, 255, 255), medium_button)  # Set button to white when clicked
                    draw_text(WIN, 'Medium', font_small, (0, 200, 0), medium_button)  # Green text
                    pygame.display.flip()
                    pygame.time.wait(200)  # Wait for a short duration to show the effect
                    menu = False
                    main(4)  # Start game with medium difficulty
                elif hard_button.collidepoint(event.pos):
                    pygame.draw.rect(WIN, (255, 255, 255), hard_button)  # Set button to white when clicked
                    draw_text(WIN, 'Hard', font_small, (0, 200, 0), hard_button)  # Green text
                    pygame.display.flip()
                    pygame.time.wait(200)  # Wait for a short duration to show the effect
                    menu = False
                    main(5)  # Start game with hard difficulty

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def display_moves(game, font):
    move_surface.fill((50, 50, 50))  # Background color for move count section
    player_moves_text = f"Player Moves: {game.player_moves}"
    ai_moves_text = f"AI Moves: {game.ai_moves}"
    player_moves_surface = font.render(player_moves_text, True, (255, 255, 255))
    ai_moves_surface = font.render(ai_moves_text, True, (255, 255, 255))
    move_surface.blit(player_moves_surface, (20, 50))
    move_surface.blit(ai_moves_surface, (20, 100))

def main(difficulty=3):
    run = True
    clock = pygame.time.Clock()
    board = Board()
    game = Game(game_surface)
    
    # Font for the move count section
    font = pygame.font.Font(None, 36)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), difficulty, float('-inf'), float('inf'), True, game)
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
                if pos[0] < WIDTH:  # Ensure clicks are within the game board area
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

        game.update()
        display_moves(game, font)
        
        # Blit the game surface and move count surface onto the main window
        WIN.blit(game_surface, (0, 0))
        WIN.blit(move_surface, (WIDTH, 0))
        pygame.display.flip()
    
    pygame.quit()

main_menu()
