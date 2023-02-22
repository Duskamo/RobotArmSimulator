import time
import pygame

from Config import *
from Colors import *
from Box import Box
from Robot import Robot


class Main:
    def main(self):
        # Initialize PyGame and Window
        pygame.init()
        window = pygame.display.set_mode((1100, 700))
        window.fill(WHITE)

        # Define Event Handlers

        # Define Text Objects
        font = pygame.font.SysFont(None, 50)
        img = font.render('OUTPUT ENV', True, BLACK)
        img2 = font.render('INPUT ENV', True, BLACK)

        # Define Game Objects
        self.robots = []
        for i in range(ROBOT_COUNT):
            self.robots.append(Robot(pygame, window))

        self.blocks = []
        for i in range(100, 300, 25):
            for j in range(600, 1000, 25):
                self.blocks.append(Box(pygame, window, j, i, 0, BLUE))

        self.outputBlocks = []
        for i in range(100,500,25):
            for j in range(100, 500, 25):
                self.outputBlocks.append(Box(pygame, window, j, i, 1, BLACK))

        # Read Map File and append to targetBlock list
        f = open("Map.txt", "r")
        file = f.read()
        file = file.replace('\n', '')

        self.targetBlocks = []
        for i in range(len(file)):
            if file[i] == '*':
                self.targetBlocks.append(self.outputBlocks[i])

        # Set Game Clock and other variables
        clock = pygame.time.Clock()
        self.blockSelection = [0, len(self.targetBlocks) - 1]
        self.overBlock = [False, False]
        self.pickupBlock = [True, True]
        self.running = True

        # Game Loop
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False

            window.fill(WHITE)

            # Draw Output Environment
            pygame.draw.rect(window, BLACK, (100, 100, 400, 400), 2)
            window.blit(img, (100, 60))
            for block in self.outputBlocks:
                block.draw()

            # Draw Input Environment
            pygame.draw.rect(window, BLACK, (600, 100, 400, 400), 2)
            window.blit(img2, (600, 60))
            for block in self.blocks:
                block.draw()

            # Default Arm Box
            pygame.draw.rect(window, BLACK, (900, 550, 100, 100), 2)
            for robot in self.robots:
                robot.draw()

            # Main Algorithm
            for robotNum in range(ROBOT_COUNT):
                self.move(robotNum, self.blockSelection[robotNum])

            # Update everything
            pygame.display.update()
            clock.tick(CLOCK_SPEED)

    def move(self, robotNum, blockSelection):
        self.moveArmToBlock(self.robots[robotNum], self.blocks[blockSelection], robotNum)
        self.moveBlockToDest(self.robots[robotNum], self.blocks[blockSelection], self.targetBlocks[blockSelection], robotNum)
        if RETURN_ARM_TO_START:
            self.returnArmtoStart(self.robots[robotNum], robotNum)
        if self.ifLastBlockIsPlaced():
            self.running = False
            # self.returnArmtoStart(self.robots[0], 0)
            # self.returnArmtoStart(self.robots[1], 1)

    def moveArmToBlock(self, robot, block, boolVal):
        if not self.overBlock[boolVal] and self.pickupBlock[boolVal]:
            if robot.x > block.center[0]:
                robot.x = robot.x - SPEED
            elif robot.x < block.center[0]:
                robot.x = robot.x + SPEED

            if robot.x == block.center[0] and robot.y > block.center[1]:
                robot.y = robot.y - SPEED
            elif robot.x == block.center[0] and robot.y < block.center[1]:
                robot.y = robot.y + SPEED

            if robot.x == block.center[0] and robot.y == block.center[1]:
                self.overBlock[boolVal] = True
                # time.sleep(1)

    def moveBlockToDest(self, robot, block, targetBlock, boolVal):
        if self.overBlock[boolVal]:
            if robot.x > targetBlock.center[0]:
                robot.x = robot.x - SPEED
                block.x = block.x - SPEED
            elif robot.x < targetBlock.center[0]:
                robot.x = robot.x + SPEED
                block.x = block.x + SPEED

            if robot.x == targetBlock.center[0] and robot.y > targetBlock.center[1]:
                robot.y = robot.y - SPEED
                block.y = block.y - SPEED
            elif robot.x == targetBlock.center[0] and robot.y < targetBlock.center[1]:
                robot.y = robot.y + SPEED
                block.y = block.y + SPEED

            if robot.x == targetBlock.center[0] and robot.y == targetBlock.center[1]:
                block.inUse = True
                self.overBlock[boolVal] = False
                if RETURN_ARM_TO_START:
                    self.pickupBlock[boolVal] = False
                else:
                    self.pickupBlock[boolVal] = True
                    if boolVal == 0:
                        self.blockSelection[0] = self.blockSelection[0] + 1
                    elif boolVal == 1:
                        self.blockSelection[1] = self.blockSelection[1] - 1

    def returnArmtoStart(self, robot, boolVal):
        if not self.pickupBlock[boolVal]:
            if robot.y < 600:
                robot.y = robot.y + SPEED

            if robot.y == 600 and robot.x < 950:
                robot.x = robot.x + SPEED

            if robot.y == 600 and robot.x == 950:
                self.pickupBlock[boolVal] = True
                if boolVal == 0:
                    self.blockSelection[0] = self.blockSelection[0] + 1
                elif boolVal == 1:
                    self.blockSelection[1] = self.blockSelection[1] - 1

            # if self.blocks[0].x < 500 and self.blocks[1].x < 500 and self.blocks[2].x < 500 and self.robot.x == 950 and self.robot.y == 600:
            #     self.running = False

    def ifLastBlockIsPlaced(self):
        blockInUseCount = 0
        for block in self.blocks:
            if block.inUse == True:
                blockInUseCount = blockInUseCount + 1

        if blockInUseCount == len(self.targetBlocks):
            return True
        else:
            return False


if __name__ == "__main__":
    Main().main()
    time.sleep(5)
    pygame.quit()