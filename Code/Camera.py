import pygame
from pygame import Rect
from settings import screen_height, screen_width

class Camera(object):

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0,0,width,height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def simple_cam(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+(screen_width/2), -t+(screen_height/2), w, h)


def complex_camera(camera, target_rect):
    # we want to center target_rect
    x = -target_rect.centerx + screen_width / 2
    y = -target_rect.centery + screen_height / 2
    camera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera.topleft)) * 0.15 #smoothing factor

    return camera