import pygame
import random
from podesavanja import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.speed = self.set_speed()
        self.starting_pos = [pos.x, pos.y]

    def update(self):
        self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            self.move()

        # podesavanje pozicije grida u odnosu na poziciju pixela
        self.grid_pos[0] = (self.pix_pos[
                                0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[
                                1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1

    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour, (int(self.pix_pos.x),int(self.pix_pos.y)), self.radius)

    def set_speed(self):
        if self.personality in ["brzo","uplaseno"]:
            speed = 2
        else:
            speed =1
        return  speed

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "brzo":
            self.direction = self.get_random_direction()
        if self.personality == "sporo":
            self.direction = self.get_random_direction()
        if self.personality == "uplaseno":
            self.direction = self.get_random_direction()

    def get_random_direction(self):
        while True:
            number = random.randint(-2,1)
            if number == -2:
                x_dir, y_dir = 1,0
            elif number == -1:
                x_dir, y_dir = 0,1
            elif number == 0:
                x_dir, y_dir = -1,0
            else:
                x_dir, y_dir = 0,-1
            next_pos = vec(self.grid_pos.x + x_dir,self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir,y_dir)

    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)
        print(self.grid_pos, self.pix_pos)

    def set_colour(self):
        if self.number == 0:
            return (43, 78, 203)
        if self.number == 1:
            return (197, 200, 27)
        if self.number == 2:
            return (189, 29, 29)
        if self.number == 3:
            return (215, 159, 33)

    def set_personality(self):
        if self.number == 0:
            return "brzo"
        elif self.number == 1:
            return "sporo"
        elif self.number == 2:
            return "random"
        else:
            return "uplaseno"