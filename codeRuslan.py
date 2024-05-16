import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки игры
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Арканоид")
clock = pygame.time.Clock()
fps = 60

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Класс для мяча
class Ball:
    def init(self, x, y, radius, color, x_speed, y_speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_speed = x_speed
        self.y_speed = y_speed

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def bounce(self, direction):
        if direction == "x":
            self.x_speed *= -1
        elif direction == "y":
            self.y_speed *= -1

# Класс для ракетки
class Paddle:
    def init(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 15  # Добавлено свойство speed для управления скоростью

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == "left":
            self.x -= self.speed  # Использование speed при движении
        elif direction == "right":
            self.x += self.speed  # Использование speed при движении

# Класс для кирпичей
class Brick:
    def init(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.alive = True

    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def is_hit(self, ball):
        if self.alive:
            if ball.x + ball.radius >= self.x and ball.x - ball.radius <= self.x + self.width:
                if ball.y + ball.radius >= self.y and ball.y - ball.radius <= self.y + self.height:
                    self.alive = False
                    return True
        return False

# Создание мяча
ball = Ball(width // 2, height // 2, 10, white, 5, 5)

# Создание ракетки
paddle = Paddle(width // 2 - 100, height - 20, 200, 10, green)

# Создание кирпичей
bricks = []
for i in range(5):
    for j in range(10):
        brick = Brick(i * 80 + 20, j * 30 + 50, 60, 20, red)
        bricks.append(brick)

# Основной цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle.move("left")
            if event.key == pygame.K_RIGHT:
                paddle.move("right")

    # Движение мяча
    ball.move()

    # Отскок от стенок
    if ball.x + ball.radius >= width or ball.x - ball.radius <= 0:
        ball.bounce("x")
    if ball.y - ball.radius <= 0:
        ball.bounce("y")

    # Отскок от ракетки
    if ball.y + ball.radius >= paddle.y and ball.x >= paddle.x and ball.x <= paddle.x + paddle.width:
        ball.bounce("y")

    # Проверка столкновения с кирпичами
    for brick in bricks:
        if brick.is_hit(ball):
            ball.bounce("y")

    # Проигрыш
    if ball.y + ball.radius >= height:
        print("Игра окончена!")
        running = False

    # Очистка экрана
    screen.fill(black)

    # Отрисовка элементов
    ball.draw()
    paddle.draw()
    for brick in bricks:
        brick.draw()

    # Обновление экрана
    pygame.display.flip()

    # Установка частоты кадров
    clock.tick(fps)
