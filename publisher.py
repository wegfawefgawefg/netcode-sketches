from pickle import dumps as dehydrate
from pickle import loads as hydrate

import pygame
from pygame import Vector2
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def set_position(position):
    r.publish('room1', dehydrate({'op': 'MOVE', 'vector': position}))

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # quit when i press escape
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

            # get mouse position
            if event.type == pygame.MOUSEMOTION:
                pos = Vector2(event.pos)
                set_position(pos)

        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)

main()