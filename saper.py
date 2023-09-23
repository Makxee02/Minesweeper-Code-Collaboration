import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Размер и параметры игрового поля (уменьшаем на 20%)
WIDTH, HEIGHT = 640, 640
GRID_SIZE = 40
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
NUM_MINES = 80

# Цвета
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Зеленый цвет
NUM_COLORS = [(0, 0, 255), (0, 128, 0), (255, 0, 0), (0, 0, 128), (128, 0, 0), (0, 128, 128), (0, 0, 0), (128, 128, 128)]

# Создание окна
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сапер PIVOVAROV")  # Изменение названия игры

def initialize_game():
    global grid, revealed, game_over, start_time
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    revealed = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Расставляем мины на поле
    mines = [(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) for _ in range(NUM_MINES)]
    for x, y in mines:
        grid[y][x] = -1

    # Вычисляем количество мин вокруг каждой ячейки
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[y][x] != -1:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT and grid[y + dy][x + dx] == -1:
                            grid[y][x] += 1

    game_over = False
    start_time = None

initialize_game()

# Функция для открытия ячейки
def open_cell(x, y):
    global start_time, game_over
    if start_time is None:
        start_time = time.time()

    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and not revealed[y][x]:
        revealed[y][x] = True
        if grid[y][x] == 0:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    open_cell(x + dx, y + dy)
        elif grid[y][x] == -1:
            game_over = True
            start_time = None

# Основной игровой цикл
running = True
game_over = False
start_time = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            x //= GRID_SIZE
            y //= GRID_SIZE
            open_cell(x, y)

        if game_over and event.type == pygame.KEYDOWN:
            initialize_game()
            game_over = False
            start_time = None

    window.fill(WHITE)

    # Отображение таймера
    if start_time is not None and not game_over:
        current_time = int(time.time() - start_time)
    else:
        current_time = 0

    font = pygame.font.Font(None, 36)
    time_text = font.render(f"Время: {current_time // 60:02}:{current_time % 60:02}", True, GREEN)
    time_rect = time_text.get_rect(topleft=(10, 10))
    window.blit(time_text, time_rect)

    # Отрисовка разделителей и ячеек поля
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cell_rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(window, WHITE, cell_rect)
            pygame.draw.rect(window, GRAY, cell_rect, 1)

            if revealed[y][x] and grid[y][x] == 0:
                pygame.draw.rect(window, GRAY, cell_rect)

            if revealed[y][x]:
                if grid[y][x] == -1:
                    mine_img = pygame.image.load('mine.png')
                    mine_img = pygame.transform.scale(mine_img, (GRID_SIZE, GRID_SIZE))
                    window.blit(mine_img, cell_rect)
                elif grid[y][x] > 0:
                    font = pygame.font.Font(None, 28)
                    text = font.render(str(grid[y][x]), True, NUM_COLORS[grid[y][x]])
                    text_rect = text.get_rect(center=(x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2))
                    pygame.draw.rect(window, GRAY, cell_rect)
                    window.blit(text, text_rect)

    # Если игра завершена (проиграна или выиграна), выводим соответствующее сообщение
    if game_over:
        font = pygame.font.Font(None, 36)
        if any(not revealed[y][x] and grid[y][x] == -1 for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)):
            message = "Неудачник, ты проиграл."
        else:
            message = "Поздравляю! Ты выиграл."

        end_time = time.time()
        if start_time is not None:
            elapsed_time = int(end_time - start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            time_message = f"Потратив всего {minutes:02}:{seconds:02}."
        else:
            time_message = ""

        final_message = message + " " + time_message
        text = font.render(final_message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(text, text_rect)

    pygame.display.flip()

# Завершение Pygame
pygame.quit()
