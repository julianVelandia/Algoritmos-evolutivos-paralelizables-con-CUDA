import pygame as pg
import math


def rotate(image, angle):

    origin = image.get_rect()

    image_rotation = pg.transform.rotate(image, angle)

    rect_rotation = origin.copy()
    rect_rotation.center = image_rotation.get_rect().center

    image_rotation = image_rotation.subsurface(rect_rotation).copy()

    return image_rotation


def calc_sides(coords, angle):
    length = 50
    top_left = [
        coords[0] + math.cos(math.radians(360 - (angle + 30))) * length,
        coords[1] + math.sin(math.radians(360 - (angle + 30))) * length
    ]
    top_right = [
        coords[0] + math.cos(math.radians(360 - (angle + 150))) * length,
        coords[1] + math.sin(math.radians(360 - (angle + 150))) * length
    ]
    bottom_left = [
        coords[0] + math.cos(math.radians(360 - (angle + 210))) * length,
        coords[1] + math.sin(math.radians(360 - (angle + 210))) * length
    ]
    bottom_right = [
        coords[0] + math.cos(math.radians(360 - (angle + 330))) * length,
        coords[1] + math.sin(math.radians(360 - (angle + 330))) * length
    ]

    return [top_left, top_right, bottom_left, bottom_right]