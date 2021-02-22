import math
import os
import sys
import pygame
import requests


class Map(object):
    def __init__(self):
        self.lat = 56.346846
        self.lon = 43.847955
        self.zoom = 16
        self.type = 'map'

    def ll(self):
        return str(self.lon) + ',' + str(self.lat)

    def update(self, event):
        my_step = 0.008
        if event.key == pygame.K_PAGEDOWN and self.zoom < 19:
            self.zoom += 1
        elif event.key == pygame.K_PAGEUP and self.zoom > 2:
            self.zoom -= 1
        elif event.key == pygame.K_LEFT:
            self.lon -= my_step * math.pow(2, 15 - self.zoom)
        elif event.key == pygame.K_RIGHT:
            self.lon += my_step * math.pow(2, 15 - self.zoom)
        elif event.key == pygame.K_UP and self.lat < 85:
            self.lat += my_step * math.pow(2, 15 - self.zoom)
        elif event.key == pygame.K_DOWN and self.lat > -85:
            self.lat -= my_step * math.pow(2, 15 - self.zoom)


def load_map(map):
    request = 'http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}'.format(ll=map.ll(), z=map.zoom, type=map.type)
    response = requests.get(request)
    if not response:
        print('Ошибка выполнения запроса:')
        print(request)
        print('Http статус:', response.status_code, '(', response.reason, ')')
        sys.exit(1)

    map_file = 'map.png'
    with open(map_file, 'wb') as file:
        file.write(response.content)
    return map_file


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    map = Map()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYUP:
            map.update(event)
        map_file = load_map(map)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()
