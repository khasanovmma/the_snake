from random import choice
import pygame as pg
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Константы направлений
UP: tuple[int, int] = (0, -1)
DOWN: tuple[int, int] = (0, 1)
LEFT: tuple[int, int] = (-1, 0)
RIGHT: tuple[int, int] = (1, 0)
DIRECTIONS: tuple[tuple[int, int]] = (UP, DOWN, LEFT, RIGHT)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# Инициализация Pygame
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption("Змейка")
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов, таких как яблоко и змея."""

    def __init__(
        self,
        body_color: tuple,
        position: tuple[int, int] = None,
    ) -> None:
        """
        Инициализация базового игрового объекта с заданным положением и цветом
        тела.

        :param body_color: Цвет тела объекта в формате RGB.
        :param position: Начальное положение объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position: tuple) -> None:
        """
        Отображает ячейку на экране по заданной позиции с цветом объекта.

        :param position: Координаты ячейки для отображения.
        """
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self) -> None:
        """
        Метод для отображения объекта. Должен быть реализован в

        дочерних классах.
        """
        raise NotImplementedError(
            "Метод draw() должен быть реализован в дочерних классах."
        )


class Apple(GameObject):
    """Класс, представляющий яблоко на экране."""

    def __init__(
        self,
        body_color: tuple,
        position: tuple[int, int] = None,
        occupied_positions=(SCREEN_CENTER,),
    ) -> None:
        """Инициализация яблока с заданным начальным положением и цветом."""
        super().__init__(body_color, position)

    def draw(self) -> None:
        """Рисует яблоко на экране в заданной позиции."""
        self.draw_cell(self.position)

    def randomize_position(self, snake_positions: list[tuple[int, int]]):
        """Генерирует случайную позицию для яблока, избегая позиций змеи."""
        while True:
            random_x = choice(range(0, SCREEN_WIDTH, GRID_SIZE))
            random_y = choice(range(0, SCREEN_HEIGHT, GRID_SIZE))
            self.position = (random_x, random_y)

            if self.position not in snake_positions:
                break


class Snake(GameObject):
    """Класс, представляющий змею и управляющий её движением и положением."""

    SPEED = 5

    def __init__(
        self,
        body_color: tuple,
        position: tuple[int, int] = None,
    ) -> None:
        """Инициализация змеи с начальным положением, направлением и длиной."""
        super().__init__(body_color, position=position)
        self.positions = [self.position]
        self.direction = choice(DIRECTIONS)
        self.last_position = None
        self.length = 0
        self.next_direction = None
        self.paused: bool = False

    def draw(self) -> None:
        """Рисует тело змеи и её голову на экране."""
        # Рисуем тело змеи
        for position in self.positions[:-1]:
            self.draw_cell(position)

        # Рисуем голову змеи
        self.draw_cell(self.get_head_position())

        # Очистка последней позиции хвоста
        if self.last_position:
            last_rect = pg.Rect(self.last_position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    def move(self) -> None:
        """Перемещает змею в текущем направлении и обновляет её позиции."""
        position_x, position_y = self.get_head_position()
        next_position_x, next_position_y = self.direction
        self.position = (
            (position_x + (next_position_x * GRID_SIZE)) % SCREEN_WIDTH,
            (position_y + (next_position_y * GRID_SIZE)) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, self.position)
        if len(self.positions) - 1 > self.length:
            self.last_position = self.positions.pop()
        else:
            self.last_position = None

    def update_direction(self) -> None:
        """
        Обновляет направление движения змеи, если
        задано новое направление.
        """
        if self.next_direction:
            self.direction = self.next_direction

    def randomize_position(self) -> tuple[int, int]:
        """Возвращает случайное положение для размещения змеи на экране."""
        random_x = choice(range(0, SCREEN_WIDTH, GRID_SIZE))
        random_y = choice(range(0, SCREEN_HEIGHT, GRID_SIZE))
        return random_x, random_y

    def reset(self) -> None:
        """Сбрасывает параметры змеи к начальному состоянию."""
        self.positions = [self.randomize_position()]
        self.direction = choice(DIRECTIONS)
        self.last_position = None
        self.length = 0
        self.SPEED = 5


def handle_keys(snake: Snake) -> None:
    """Обрабатывает нажатия клавиш и изменяет направление движения змеи."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == pg.K_RETURN:
                snake.paused = False
                screen.fill(BLACK_COLOR)


def main() -> None:
    """
    Запускает главный игровой цикл, создаёт
    объекты змеи и яблока и обновляет экран.
    """
    pg.init()
    apple = Apple(body_color=APPLE_COLOR)
    snake = Snake(body_color=SNAKE_COLOR)
    while True:
        clock.tick(snake.SPEED)
        handle_keys(snake)

        if not snake.PAUSED:
            apple.draw()
            snake.draw()
            snake.move()
            snake.update_direction()

        if apple.position in snake.positions:
            snake.length += 1
            snake.SPEED += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.PAUSED = True
            font = pg.font.Font(None, 74)
            text = font.render("Game Over", True, WHITE_COLOR)
            score_text = pg.font.Font(None, 36).render(
                f"Your score: {snake.length}", True, WHITE_COLOR
            )
            instruction_text = pg.font.Font(None, 36).render(
                "Press ENTER to continue or ESC to exit", True, WHITE_COLOR
            )
            screen.blit(
                text,
                (
                    SCREEN_WIDTH // 2 - text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - text.get_height() // 2,
                ),
            )
            screen.blit(
                score_text,
                (
                    SCREEN_WIDTH // 2 - instruction_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 + 50,
                ),
            )
            screen.blit(
                instruction_text,
                (
                    SCREEN_WIDTH // 2 - instruction_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 + 80,
                ),
            )
            pg.display.flip()
            snake.reset()

        pg.display.update()


if __name__ == "__main__":
    main()
