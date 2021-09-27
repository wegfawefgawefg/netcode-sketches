import pygame
import redis
import time
from pickle import dumps as dehydrate
from pickle import loads as hydrate
from pygame import Vector2
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.subscribe('player1')
pygame.init()
class Message:
    def __init__(self, message):
        self.type = message['type']
        self.pattern = message['pattern']
        self.channel = message['channel']
        data = message['data']
        if isinstance(data, bytes):
            data = hydrate(data)
        self.data = data
screen_size = Vector2(240, 240)
scr = pygame.Surface(screen_size)
clock = pygame.time.Clock()
pos = Vector2(screen_size/2)
while 1:
    dt = clock.tick(60)*.001
    message = p.get_message()
    if message:
        message = Message(message)
        if isinstance(message.data, dict):
            if message.data['op'] == 'MOVE':
                pos = message.data['vector'] * 10
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_ESCAPE)):
            pygame.quit()
            quit()
    scr.fill((30,20,30))
    pygame.draw.circle(scr, (200,200,0), pos, 3)
    r.publish('player1', dehydrate({'op': 'DISPLAY', 'buffer': scr.get_buffer().raw}))