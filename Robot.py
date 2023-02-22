from Colors import *


class Robot:
    def __init__(self, pygame, window):
        self.pygame = pygame
        self.window = window

        self.color = RED
        self.radius = 10
        self.thickness = 0

        self.x = 950
        self.y = 600

    def draw(self):
        self.pygame.draw.circle(self.window, self.color, [self.x, self.y], self.radius, self.thickness)
