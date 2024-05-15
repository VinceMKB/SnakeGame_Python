import pygame
import pygame.freetype
from typing import Final
import random

#Screen Size Variable init
Offset: Final[float] = 75
CellCount: Final[float] = 25
CellSize: Final[float] = 30

WindowX = 2 * Offset + CellSize * CellCount
WindowY = 2 * Offset + CellSize * CellCount
BorderX = CellSize * CellCount + 10
BorderY = CellSize * CellCount + 10


# pygame setup
pygame.init()
screen = pygame.display.set_mode((WindowX, WindowY))
Game_Font = pygame.freetype.Font("\SnakeGame_Python\Graphics\Abaddon Bold.ttf", 40)
clock = pygame.time.Clock()

LightBlue = (0, 153, 255)
Black = (0, 0, 0)

image_path = "\SnakeGame_Python\Graphics\BetterFood.png"
textfile_path = "\SnakeGame_Python\HighScore.txt"

def read_highscore(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            if content:
                return int(content)
            else:
                return 0
    except FileNotFoundError:
        return 0


def write_highscore(file_path, score):
    with open(file_path, 'w') as file:
        file.write(str(score))

class Snake(object):
    def __init__(self):
        self.body = [(6, 9), (5, 9), (4, 9)]
        self.direction = (1, 0)
        self.add_segment = False
    
    def draw(self):
        for segment in self.body:
            x, y = segment
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x * CellSize + Offset, y * CellSize + Offset, CellSize, CellSize))

    def update(self):
        self.body.insert(0, (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]))
        if self.add_segment:
            self.add_segment = False
        else:
            self.body.pop()
    
    def reset(self):
        self.body = [(6, 9), (5, 9), (4, 9)]
        self.direction = (1, 0)
        self.add_segment = False

class Food(object):
    def __init__(self, snake_body):
        self.position = self.generateRandomPos(snake_body)
        self.texture = pygame.image.load(image_path)
        self.rect = self.texture.get_rect()
    
    def draw(self):
        screen.blit(self.texture, (self.position[0] * CellSize + Offset, self.position[1] * CellSize + Offset))

    @staticmethod
    def generateRandomCell():
        return (random.randint(0, CellCount -1), random.randint(0, CellCount -1))
    
    def generateRandomPos(self, snake_body):
        position = self.generateRandomCell()
        while position in snake_body:
            position = self.generateRandomCell()
        return position
    
class Game(object):
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.running = True
        self.score = 0
        self.last_updatetime = 0
        self.highscore = read_highscore(textfile_path)

    def draw(self):
        self.snake.draw()
        self.food.draw()

    def draw_score(self):
        highscore_surface, _ = Game_Font.render(f"High Score: {self.highscore}", (0, 0, 0))
        screen.blit(highscore_surface, (250, (90 + CellSize * CellCount)))       

    def update(self):
        if self.running:
            self.snake.update()
            self.checkCollisionWithEdges()
            self.checkCollisionWithFood()
            self.checkCollisionWithTail()

    def checkCollisionWithFood(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generateRandomPos(self.snake.body)
            self.snake.add_segment = True
            self.score += 10

    def checkCollisionWithEdges(self):
        if self.snake.body[0][0] == CellCount or self.snake.body[0][0] == -1:
            self.game_over()
        if self.snake.body[0][1] == CellCount or self.snake.body[0][1] == -1:
            self.game_over()

    def checkCollisionWithTail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

    def game_over(self):
        if self.score > self.highscore:
            self.highscore = self.score
            write_highscore(textfile_path, self.highscore)
        self.snake.reset()
        self.food.position = self.food.generateRandomPos(self.snake.body)
        self.score = 0
        print("GameOver!")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                    self.snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                    self.snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                    self.snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.direction = (1, 0)

    def event_triggered(self, interval):
        current_time = pygame.time.get_ticks()/1000.0
        if current_time - self.last_updatetime >= interval:
            self.last_updatetime = current_time
            return True
        return False
    
game = Game()

while game.running:
    game.handle_events()

    if game.event_triggered(0.3):
        game.update()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(LightBlue)
    text_surface, rect = Game_Font.render("~Snake Game~", (0, 0, 0))
    screen.blit(text_surface, (75, 40))
    score_text, rect = Game_Font.render(f"Score: {game.score}", (0, 0, 0))
    screen.blit(score_text, (75, (90 + CellSize * CellCount)))
    pygame.draw.rect(screen, Black, pygame.Rect(70, 70, BorderX, BorderY), 5)
    

    # RENDER YOUR GAME HERE
    game.draw()
    game.draw_score()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

