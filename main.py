import pygame
from time import time, sleep, gmtime
from threading import Thread, Lock, active_count
from vector_class import Vector3D as Vec
from math import sqrt, tan
import settings
from os import system

#region shapes
class Sphere():
    def __init__(self, x, y, z, r, colour=[255, 255, 255]):
        self.pos = Vec(x, y, z)
        self.r = r
        self.colour = colour
    
    def collide_point(self, point):
        return self.pos.dist(point) <= self.r

class Box():
    def __init__(self, x, y, z, w, h, d, colour=[255, 255, 255]):
        self.pos = Vec(x, y, z)
        self.size = Vec(w, h, d)
        self.colour = colour
    
    def collide_point(self, point):
            return  point.x >= self.pos.x and point.x <= self.pos.x + self.size.x and\
                    point.y >= self.pos.y and point.y <= self.pos.y + self.size.y and\
                    point.z >= self.pos.z and point.z <= self.pos.z + self.size.z

#endregion

#region path tracing

class Ray():
    def __init__(self, x, y, z):
        self.pos = Vec(x, y, z)
        self.colour = [0, 0, 0]
        self.bounces = 0
        self.pixel = (x, y)

        self.heading = self.pos - Vec(settings.rendering_canvas_size[0]/2, settings.rendering_canvas_size[1]/2, -focal_length)
        self.heading.normalise()

    def get_colour(self):
        r, g, b = self.colour

        r /= self.bounces ; g /= self.bounces ; b /= self.bounces

        if r > 255 : r = 255
        if g > 255 : g = 255
        if b > 255 : b = 255

        return [r, g, b]

    def add_colour(self, colour):
        r, g, b = colour

        self.colour[0] += r ; self.colour[1] += g ; self.colour[2] += b
        self.bounces += 1

#load and create shapes
shapes = []
for i in settings.shapes:
    name = i.split(' ')[0]

    if name.lower() == 'sphere':
        _, x, y, z, rad, r, g, b = i.split(' ')
        shapes.append(Sphere(float(x), float(y), float(z), float(rad), colour=[float(r), float(g), float(b)]))
    elif name.lower() == 'box':
        _, x, y, z, w, h, d, r, g, b = i.split(' ')
        shapes.append(Box(float(x), float(y), float(z), float(w), float(h), float(d), colour=[float(r), float(g), float(b)]))

rendering_canvas = pygame.Surface(settings.rendering_canvas_size)

report = ['[Thread 0 - ?/? | ?%' for _ in range(settings.threads_to_open)]

def map_to_range(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def chunk_renderer(id, rays):
    total_rays_at_start = len(rays)

    while len(rays) > 0:
        temp_ray_holder = []

        for ray in rays:
            ray.pos.add(ray.heading)

            next_iter = True

            if ray.pos.dist([ray.pixel[0], ray.pixel[1], 0]) > settings.render_distance:

                if ray.bounces == 0:
                    ray.add_colour(settings.sky_colour)

                rendering_canvas.set_at(ray.pixel, ray.get_colour())

                next_iter = False
        
            for shape in shapes:
                if shape.collide_point(ray.pos):
                    ray.add_colour(shape.colour)

                    if ray.bounces == settings.ray_reflections + 1:
                        rendering_canvas.set_at(ray.pixel, ray.get_colour())
                        next_iter = False
                        break
                    else:
                        ray.heading = ray.pos - shape.pos
                        ray.heading.normalise()
        
            if next_iter:
                temp_ray_holder.append(ray)
        
        rays = temp_ray_holder
        current_total_rays = len(rays)

        report[id-1] = f'[Thread {id} - {current_total_rays}/{total_rays_at_start} | {int(map_to_range(current_total_rays, 0, total_rays_at_start, 100, 0))}%'

focal_length = (0.5 * settings.rendering_canvas_size[0]) * tan(settings.fov / 2)
rays = []
id = 1
for y in range(settings.rendering_canvas_size[0]):
    for x in range(settings.rendering_canvas_size[1]):
        rays.append(Ray(x, y, 0))

        if len(rays) == int((settings.rendering_canvas_size[0] * settings.rendering_canvas_size[1]) / settings.threads_to_open):
            thread = Thread(target=chunk_renderer, args=(id, rays))
            thread.start()
            rays = []
            id += 1

if len(rays) != 0:
    thread = Thread(target=chunk_renderer, args=(id+1, rays))
    thread.start()
#endregion

def pretty_time(gm_time):
    hr = str(gm_time.tm_hour)
    mi = str(gm_time.tm_min)
    se = str(gm_time.tm_sec)

    if len(hr) == 1 : hr = '0' + hr
    if len(mi) == 1 : mi = '0' + mi
    if len(se) == 1 : se = '0' + se

    print(f'Time Elapsed: {hr}:{mi}:{se}')

system('cls')
start_time = time()
while active_count() > 1:
    system('cls')

    for rep in sorted(report, key=lambda elem : int(elem.split(' ')[1])):
        print(rep)

    elapsed = gmtime(time() - start_time)
    pretty_time(elapsed)

    sleep(0.5)
end_time = gmtime(time() - start_time)
system('cls')
pretty_time(end_time)

#region pygame
pygame.init()
screen = pygame.display.set_mode(settings.screen_size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 60

rendering_canvas = pygame.transform.scale(rendering_canvas, settings.screen_size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            quit()

    screen.blit(rendering_canvas, (0, 0))

    pygame.display.update()
    clock.tick(fps)
#endregion
