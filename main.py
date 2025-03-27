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

# Функция для создания игрового поля без начальных совпадений
def create_grid():
    grid = [[random.randint(1, 5) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    # Проверка на наличие совпадений
    def has_matches():
        # Проверка горизонтальных совпадений
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH - 2):
                if grid[row][col] != 0 and grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                    return True

        # Проверка вертикальных совпадений
        for col in range(GRID_WIDTH):
            for row in range(GRID_HEIGHT - 2):
                if grid[row][col] != 0 and grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                    return True

        return False

    # Пересоздаём поле, пока есть совпадения
    while has_matches():
        grid = [[random.randint(1, 5) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    return grid

# Создание игрового поля
grid = create_grid()

# Функция для отрисовки игрового поля
def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            tile_value = grid[row][col]
            color = None

            # Определение цвета в зависимости от значения тайла
            if tile_value == 0:  # Пустая ячейка
                color = WHITE
            elif tile_value == 1:
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

# Функция для проверки совпадений
def check_matches():
    matches = []

    # Проверка горизонтальных совпадений
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH - 2):  # Минимум три элемента подряд
            if grid[row][col] != 0 and grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                # Найдено совпадение
                match = [(row, col), (row, col + 1), (row, col + 2)]
                # Проверяем, есть ли продолжение совпадения
                for i in range(col + 3, GRID_WIDTH):
                    if grid[row][i] == grid[row][col]:
                        match.append((row, i))
                    else:
                        break
                matches.append(match)

    # Проверка вертикальных совпадений
    for col in range(GRID_WIDTH):
        for row in range(GRID_HEIGHT - 2):  # Минимум три элемента подряд
            if grid[row][col] != 0 and grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                # Найдено совпадение
                match = [(row, col), (row + 1, col), (row + 2, col)]
                # Проверяем, есть ли продолжение совпадения
                for i in range(row + 3, GRID_HEIGHT):
                    if grid[i][col] == grid[row][col]:
                        match.append((i, col))
                    else:
                        break
                matches.append(match)

    return matches

# Функция для удаления совпадений
def remove_matches(matches):
    for match in matches:
        for row, col in match:
            grid[row][col] = 0  # Удаляем элемент

# Функция для сдвига элементов вниз
def drop_tiles():
    for col in range(GRID_WIDTH):
        empty_rows = []
        for row in range(GRID_HEIGHT - 1, -1, -1):  # Проходим снизу вверх
            if grid[row][col] == 0:
                empty_rows.append(row)
            elif empty_rows:
                # Перемещаем элемент вниз
                new_row = empty_rows.pop(0)
                grid[new_row][col] = grid[row][col]
                grid[row][col] = 0
                empty_rows.append(row)

# Функция для заполнения пустых ячеек новыми элементами
def fill_empty_tiles():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col] == 0:
                grid[row][col] = random.randint(1, 5)

# Часы для контроля FPS
clock = pygame.time.Clock()
FPS = 60

# Новая переменная для управления анимацией
animation_phase = None  # Возможные значения: None, "remove", "drop", "fill"
animation_timer = 0  # Таймер для анимации
ANIMATION_DELAY = 500  # Задержка в миллисекундах (0.5 секунды)

# Переменные для хранения выбранных тайлов
selected_tile = None

# Основной игровой цикл
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка кликов мыши
        if event.type == pygame.MOUSEBUTTONDOWN and animation_phase is None:
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

                        # Проверяем совпадения после перемещения
                        matches = check_matches()
                        if matches:
                            animation_phase = "remove"  # Переходим к фазе удаления
                            animation_timer = current_time
                        else:
                            # Если совпадений нет, возвращаем тайлы на место
                            grid[prev_row][prev_col], grid[row][col] = grid[row][col], grid[prev_row][prev_col]

                    # Сбрасываем выбор
                    selected_tile = None

    # Логика анимации
    if animation_phase == "remove":
        if current_time - animation_timer >= ANIMATION_DELAY:
            remove_matches(matches)
            animation_phase = "drop"
            animation_timer = current_time

    elif animation_phase == "drop":
        if current_time - animation_timer >= ANIMATION_DELAY:
            drop_tiles()
            animation_phase = "fill"
            animation_timer = current_time

    elif animation_phase == "fill":
        if current_time - animation_timer >= ANIMATION_DELAY:
            fill_empty_tiles()
            animation_phase = None  # Завершаем анимацию

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