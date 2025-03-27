import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 400, 600  # Ширина и высота окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Три в ряд")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройки игрового поля
GRID_WIDTH, GRID_HEIGHT = 8, 12  # Размер сетки (столбцы x строки)
TILE_SIZE = 50  # Размер одной ячейки

# Создание игрового поля
grid = [[random.randint(1, 5) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Функция для отрисовки игрового поля
def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            tile_value = grid[row][col]
            color = None

            # Определение цвета в зависимости от значения тайла
            if tile_value == 1:
                color = (255, 0, 0)  # Красный
            elif tile_value == 2:
                color = (0, 255, 0)  # Зелёный
            elif tile_value == 3:
                color = (0, 0, 255)  # Синий
            elif tile_value == 4:
                color = (255, 255, 0)  # Жёлтый
            elif tile_value == 5:
                color = (255, 0, 255)  # Фиолетовый

            # Отрисовка тайла
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

# Функция для получения координат тайла по позиции мыши
def get_tile_position(mouse_x, mouse_y):
    col = mouse_x // TILE_SIZE
    row = mouse_y // TILE_SIZE
    return row, col

# Часы для контроля FPS
clock = pygame.time.Clock()
FPS = 60

# Переменные для хранения выбранных тайлов
selected_tile = None

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка кликов мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            row, col = get_tile_position(mouse_x, mouse_y)

            # Проверяем, что клик был внутри игрового поля
            if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
                if selected_tile is None:
                    # Выбираем первый тайл
                    selected_tile = (row, col)
                else:
                    # Выбираем второй тайл и проверяем соседство
                    prev_row, prev_col = selected_tile
                    if (abs(row - prev_row) + abs(col - prev_col)) == 1:  # Проверка соседства
                        # Меняем местами значения тайлов
                        grid[prev_row][prev_col], grid[row][col] = grid[row][col], grid[prev_row][prev_col]
                    # Сбрасываем выбор
                    selected_tile = None

    # Отрисовка фона
    screen.fill(WHITE)

    # Отрисовка игрового поля
    draw_grid()

    # Подсветка выбранного тайла
    if selected_tile is not None:
        row, col = selected_tile
        pygame.draw.rect(screen, (255, 255, 255), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 4)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()