import pygame
import random
import time

# Create a blank Sudoku board
def create_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    return board

# Check if a number can be placed in the given position
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

# Fill the Sudoku board with valid numbers
def fill_board(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if fill_board(board):
                            return True
                        board[i][j] = 0
                return False
    return True

# Remove elements to create a playable puzzle
def remove_elements(board, num_holes=40):
    count = 0
    while count < num_holes:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            count += 1

# Initialize Pygame and set up the game window
pygame.init()
size = width, height = 640, 640  # Increased width for scoreboard
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sudoku")

# Draw the Sudoku grid and numbers
def draw_grid(screen, board):
    block_size = (width - 100) // 9  # Adjusted for scoreboard space
    for i in range(10):
        line_color = (0, 0, 0) if i % 3 == 0 else (200, 200, 200)
        pygame.draw.line(screen, line_color, (100, i * block_size), (width, i * block_size))
        pygame.draw.line(screen, line_color, (i * block_size + 100, 0), (i * block_size + 100, height - 100))
    
    font = pygame.font.Font(None, 36)
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                num_text = font.render(str(board[i][j]), True, (0, 0, 0))
                screen.blit(num_text, (j * block_size + 115, i * block_size + 10))

# Draw the board with user input
def draw_board_with_input(board, screen, selected):
    block_size = (width - 100) // 9  # Adjusted for scoreboard space
    font = pygame.font.Font(None, 36)
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                num_text = font.render(str(board[i][j]), True, (0, 0, 0))
                screen.blit(num_text, (j * block_size + 115, i * block_size + 10))
            if selected and selected == (i, j):
                pygame.draw.rect(screen, (0, 255, 0), (j * block_size + 100, i * block_size, block_size, block_size), 3)

# Draw the buttons and scoreboard
def draw_buttons_and_score(screen, score):
    pygame.draw.rect(screen, (0, 128, 0), (60, height - 80, 150, 50))  # Start button
    pygame.draw.rect(screen, (128, 0, 0), (330, height - 80, 150, 50))  # Exit button
    font = pygame.font.Font(None, 36)
    start_text = font.render("Start", True, (255, 255, 255))
    exit_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(start_text, (90, height - 70))
    screen.blit(exit_text, (370, height - 70))
    
    # Draw the scoreboard
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

# Draw the timer
def draw_timer(screen, start_time):
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(0, 600 - elapsed_time)  # 10 minutes = 600 seconds
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    timer_text = f"{minutes:02}:{seconds:02}"
    font = pygame.font.Font(None, 36)
    timer_surf = font.render(timer_text, True, (0, 0, 0))
    screen.blit(timer_surf, (width // 2 - 30, height - 70))  # Position the timer at the bottom center

# Main game loop
def main():
    board = create_board()
    fill_board(board)
    remove_elements(board)
    
    selected = None
    running = True
    game_started = False
    start_time = 0
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 60 <= x <= 210 and height - 80 <= y <= height - 30:  # Start button
                    game_started = True
                    start_time = time.time()
                elif 330 <= x <= 480 and height - 80 <= y <= height - 30:  # Exit button
                    running = False
                else:
                    selected = ((y // ((height - 100) // 9)), ((x - 100) // ((width - 100) // 9)))
            elif event.type == pygame.KEYDOWN and game_started:
                if selected:
                    row, col = selected
                    if event.key == pygame.K_1:
                        board[row][col] = 1
                    elif event.key == pygame.K_2:
                        board[row][col] = 2
                    elif event.key == pygame.K_3:
                        board[row][col] = 3
                    elif event.key == pygame.K_4:
                        board[row][col] = 4
                    elif event.key == pygame.K_5:
                        board[row][col] = 5
                    elif event.key == pygame.K_6:
                        board[row][col] = 6
                    elif event.key == pygame.K_7:
                        board[row][col] = 7
                    elif event.key == pygame.K_8:
                        board[row][col] = 8
                    elif event.key == pygame.K_9:
                        board[row][col] = 9
                    score += 10  # Increase score for each valid entry

        screen.fill((255, 255, 255))
        draw_grid(screen, board)
        draw_board_with_input(board, screen, selected)
        draw_buttons_and_score(screen, score)  # Draw the buttons and scoreboard
        
        if game_started:
            draw_timer(screen, start_time)  # Draw the timer
        
        pygame.display.update()  # Update the display

if __name__ == "__main__":
    main()
