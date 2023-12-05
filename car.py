import math
import pygame as pg
from pygameUtils import rotate, calc_sides
import pickle
import neat
import os

CAR_HEIGHT = 100
CAR_WIDTH = 100
RADAR_COLOR = (0, 0, 255)
WHITE_COLOR = (255, 255, 255, 255)

def load_neural_network(path):
    with open(path, 'rb') as f:
        winner = pickle.load(f)

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    return neat.nn.FeedForwardNetwork.create(winner, config)


class Car(object):

    def __init__(self, game_map, neural_network=None):
        self.game_map = game_map
        self.surface = pg.image.load('car.png')
        self.surface = pg.transform.scale(
            self.surface, (CAR_WIDTH, CAR_HEIGHT)
        )
        self.rotate_surface = self.surface
        self.x_pos = 700
        self.y_pos = 650
        self.angle = 0
        self.speed = 4
        self.distance = 0
        self.collided = False
        self.collision_points = []
        self.radars = []
        self.center = [
            self.x_pos + 50, self.y_pos + 50
        ]
        self.neural_network = neural_network

    def draw(self, screen):
        screen.blit(self.rotate_surface, [self.x_pos, self.y_pos])
        self.draw_radar(screen)

    def update(self):

        self.distance += self.speed
        self.x_pos += math.cos(math.radians(360-self.angle)) * self.speed
        self.y_pos += math.sin(math.radians(360-self.angle)) * self.speed
        self.center = [int(self.x_pos + 50), int(self.y_pos + 50)]
        self.rotate_surface = rotate(self.surface, self.angle)

        self.update_collision_points()
        self.check_collision()
        self.radars.clear()

        sensoresList = list(range(-90, 120, 45))

        for degree in sensoresList:
            self.update_radar(degree)

    def update_radar(self, degree):
        length = 0

        x_len = int(
            self.center[0] + math.cos(
                math.radians(360 - (self.angle + degree))
            ) * length
        )
        y_len = int(
            self.center[1] + math.sin(
                math.radians(360 - (self.angle + degree))
            ) * length
        )

        try:
            pixel = self.game_map.get_at((x_len, y_len))
        except IndexError:
            pixel = WHITE_COLOR

        while pixel != WHITE_COLOR and length < 300:

            try:
                pixel = self.game_map.get_at((x_len, y_len))
            except IndexError:
                pixel = WHITE_COLOR
            else:
                length = length + 1

            x_len = int(
                self.center[0] + math.cos(
                    math.radians(360 - (self.angle + degree))
                ) * length
            )

            y_len = int(
                self.center[1] + math.sin(
                    math.radians(360 - (self.angle + degree))
                ) * length
            )

        horizontal = math.pow(x_len - self.center[0], 2)
        vertical = math.pow(y_len - self.center[1], 2)

        distance = int(math.sqrt(horizontal + vertical))
        self.radars.append([(x_len, y_len), distance])

    def draw_radar(self, screen):
        self.get_data()
        for radar in self.radars:
            position, _ = radar
            pg.draw.line(screen, RADAR_COLOR, self.center, position, 1)
            pg.draw.circle(screen, RADAR_COLOR, position, 2)

    def update_collision_points(self):
        self.collision_points = calc_sides(self.center, self.angle)

    def check_collision(self):

        self.collided = False

        for point in self.collision_points:

            try:
                if self.game_map.get_at((
                    int(point[0]), int(point[1])
                )) == WHITE_COLOR:
                    self.collided = True
                    break
            except:
                self.collided = True

    def get_collided(self):
        return self.collided

    def get_reward(self):
        return self.distance/50.0

    def get_data(self):

        inputLayer = []
        for i in range(5):
            inputLayer.append(0)

        for i, radar in enumerate(self.radars):
            inputLayer[i] = int(radar[1]/30)
        return inputLayer