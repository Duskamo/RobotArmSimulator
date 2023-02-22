from Colors import *


class Box:
    def __init__(self, pygame, window, x, y, thickness, color):
        self.pygame = pygame
        self.window = window

        self.inUse = False
        self.color = color
        self.width = 25
        self.height = 25
        self.thickness = thickness

        self.x = x
        self.y = y
        self.center = (self.x + 12.5, self.y + 12.5)

    def draw(self):
        self.pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.height), self.thickness)

