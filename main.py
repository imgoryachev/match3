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

# Часы для контроля FPS
clock = pygame.time.Clock()
FPS = 60

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Отрисовка фона
    screen.fill(WHITE)

    # Отрисовка игрового поля
    draw_grid()

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()