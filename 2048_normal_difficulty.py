import pygame
import random

# Constants
GRID_SIZE = 5
CELL_SIZE = 128
WINDOW_SIZE = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Game state
grid = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)


def draw_cell(x, y, value):
    color = CELL_COLORS[value]
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    if value != 0:
        font = pygame.font.Font(None, 64)
        text = font.render(str(value), True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            draw_cell(x, y, grid[y][x])

def add_new_tile():
    empty_cells = [(x, y) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if grid[y][x] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        grid[y][x] = 2

#restarts game
def restart_game():
    global grid
    grid = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    add_new_tile()
    add_new_tile()

def merge_tiles(row):
    merged_row = [value for value in row if value != 0]
    for i in range(len(merged_row) - 1):
        if merged_row[i] == merged_row[i + 1]:
            merged_row[i] *= 2
            merged_row[i + 1] = 0
    merged_row = [value for value in merged_row if value != 0]


    return merged_row + [0] * (GRID_SIZE - len(merged_row))


def merge_left():
    global grid
    new_grid = []
    for row in grid:
        new_row = merge_tiles(row)
        new_grid.append(new_row)
    if new_grid != grid:
        grid = new_grid
        add_new_tile()


def merge_right():
    global grid
    new_grid = []
    for row in grid:
        new_row = merge_tiles(row[::-1])[::-1]
        new_grid.append(new_row)
    if new_grid != grid:
        grid = new_grid
        add_new_tile()

def is_game_over():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == 0:
                return False
            if x < GRID_SIZE - 1 and grid[y][x] == grid[y][x+1]:
                return False
            if y < GRID_SIZE - 1 and grid[y][x] == grid[y+1][x]:
                return False
    return True


def merge_up():
    global grid
    new_grid = [[] for _ in range(GRID_SIZE)]
    for x in range(GRID_SIZE):
        column = [grid[y][x] for y in range(GRID_SIZE)]
        new_column = merge_tiles(column)
        for y in range(GRID_SIZE):
            new_grid[y].append(new_column[y])
    if new_grid != grid:
        grid = new_grid
        add_new_tile()


def merge_down():
    global grid
    new_grid = [[] for _ in range(GRID_SIZE)]
    for x in range(GRID_SIZE):
        column = [grid[y][x] for y in range(GRID_SIZE)][::-1]
        new_column = merge_tiles(column)[::-1]
        for y in range(GRID_SIZE):
            new_grid[y].append(new_column[y])
    if new_grid != grid:
        grid = new_grid
        add_new_tile()

# Define bot function

def bot_play():
    direction = random.choice(['left', 'right', 'up', 'down'])
    if direction == 'left':
        merge_left()
    elif direction == 'right':
        merge_right()
    elif direction == 'up':
        merge_up()
    elif direction == 'down':
        merge_down()

# Game loop
restart_game()  # Call the function once at the beginning of the game
highest_score = 0
current_score = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                merge_left()
            elif event.key == pygame.K_RIGHT:
                merge_right()
            elif event.key == pygame.K_UP:
                merge_up()
            elif event.key == pygame.K_DOWN:
                merge_down()
            elif event.key == pygame.K_r:
                restart_game()  # Call the function when the user presses 'r'

            # Update highest score if current score is higher
            current_score = max(map(max, grid))
            if current_score > highest_score:
                highest_score = current_score

            if is_game_over():
                font = pygame.font.Font(None, 64)
                text = font.render("Game Over", True, (255, 0, 0))
                text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
                screen.blit(text, text_rect)


                # Display highest score
                font = pygame.font.Font(None, 32)
                text = font.render("Highest Score: {}".format(highest_score), True, (255, 255, 255))
                text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 50))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(2000)  # Pause for 2 secondst



    screen.fill(BACKGROUND_COLOR)
    draw_grid()



    # Display current score and highest score
    font = pygame.font.Font(None, 32)
    text = font.render("Score: {}".format(current_score), True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, 25))
    screen.blit(text, text_rect)

    text = font.render("Highest Score: {}".format(highest_score), True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, 50))
    screen.blit(text, text_rect)

    # Have the bot play every 10 game loops
    '''
    if pygame.time.get_ticks() % 10 == 0:
        bot_play()
        current_score = max(map(max, grid))
        if current_score > highest_score:
            highest_score = current_score
    elif is_game_over():
        font = pygame.font.Font(None, 64)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
        screen.blit(text, text_rect)


        font = pygame.font.Font(None, 32)
        text = font.render("Highest Score: {}".format(highest_score), True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 50))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 secondst
    '''

    pygame.display.flip()
pygame.quit()
