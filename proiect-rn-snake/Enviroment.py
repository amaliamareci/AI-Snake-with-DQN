from Player import Player
import numpy as np
import pygame
import random

BLACK = (0,0,0)
GREEN = (102,205,0)
RED = (220,20,60)
ORANGE = (210,105,30)

FPS = 400
CUBE_SIZE = 25

def cube(position,color):
    cube = pygame.sprite.Sprite()
    cube.position = position
    cube.image = pygame.Surface((CUBE_SIZE, CUBE_SIZE))
    cube.rect = cube.image.get_rect()
    cube.rect.topleft = tuple(np.array(cube.position) * CUBE_SIZE)
    cube.image.fill(color)
    return cube

class Enviroment():
    food = (0, 0)
    game_started = False


    def __init__(self,size):
        self.size = size


    def reset(self):
        self.player = Player((6, 6), 2,self.size)
        self.place_food(self.player.body)
        return self.state()


    def state(self):
        position = self.player.body[0]
        up = 0
        if (position[1] == 0 or list(position) + [0,-1] in self.player.body):
            up = 1

        right = 0
        if (position[0] == self.size - 1 or list(position) + [1, 0] in self.player.body):
            right = 1

        down = 0
        if (position[1] == self.size - 1 or list(position) + [0, 1] in self.player.body):
            down = 1

        left = 0
        if (position[0] == 0 or list(position) + [-1, 0] in self.player.body):
            left = 1

        state = np.array([up, right, down, left])
        state = np.roll(state, -1 * self.player.action + 1)
        state = np.delete(state, 2)  # remove down

        up = 0
        if (position[1] > self.food[1]):
            up = 1

        right = 0
        if (position[0] < self.food[0]):
            right = 1

        down = 0
        if (position[1] < self.food[1]):
            down = 1

        left = 0
        if (position[0] > self.food[0]):
            left = 1

        food = np.array([up, right, down, left])
        food = np.roll(food, -1 * self.player.action + 1)
        food = np.delete(food, 2)  # remove down
        return np.array([state, food]).reshape(6)


    def step(self, action: int):
        self.player.move(action)
        reward = self.player.update(self)
        done = not self.player.alive
        return self.state(), reward, done


    def render(self):
        if (self.game_started == False):
            pygame.init()
            pygame.mixer.init()
            self.screen = pygame.display.set_mode((self.size * CUBE_SIZE, self.size * CUBE_SIZE))
            pygame.display.set_caption("Snake")
            self.clock = pygame.time.Clock()
            self.game_started = True

        self.screen.fill(BLACK)
        pygame.event.get()
        self.clock.tick(FPS)

        sprites = pygame.sprite.Group()
        if (self.player.alive):
            color = GREEN
        else:
            color = ORANGE

        for position in self.player.body:
            cube1 = cube(position, color)
            sprites.add(cube1)

        sprites.add(cube(self.food, RED))

        sprites.draw(self.screen)
        pygame.display.update()
        pygame.time.delay(50)


    def place_food(self, body):
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)

        if ((x, y) in body):
            return self.place_food(body)
        else:
            self.food = (x, y)