from random import choice
import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTION = [UP, DOWN, LEFT, RIGHT]

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()


class GameObject:
    PAUSED = False

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def random_position(self, snake_positions: list[tuple[int, int]]) -> None:
        while True:
            random_x = choice(range(0, SCREEN_WIDTH, GRID_SIZE))
            random_y = choice(range(0, SCREEN_HEIGHT, GRID_SIZE))
            position = (random_x, random_y)

            if position not in snake_positions:
                self.position = position
                return None


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [self.position]
        self.direction = choice(DIRECTION)
        self.last = None
        self.length = 0
        self.next_direction = None

    def draw(self):
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        position_x, position_y = self.position
        next_position_x, next_position_y = self.direction
        self.position = (
            (position_x + (next_position_x * GRID_SIZE)) % SCREEN_WIDTH,
            (position_y + (next_position_y * GRID_SIZE)) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, self.position)
        if len(self.positions) - 1 > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction


def handle_keys(game_object: Snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        if not snake.PAUSED:
            snake.move()
        snake.update_direction()

        if apple.position in snake.positions:
            snake.length += 1
            apple.random_position(snake.positions)

        pygame.display.update()


if __name__ == "__main__":
    main()
