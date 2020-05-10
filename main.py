from os import system as command
import pygame
from math import sqrt
from time import time

#region init

pygame.init()

#endregion

#region classes

class Vector():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_mag(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalise(self):
        mag = self.get_mag()

        self.x /= mag
        self.y /= mag
        self.z /= mag

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

    def __sub__(self, vector):
        return Vector(vector.x - self.x, vector.y - self.y, vector.z - self.z)

    def copy(self):
        return Vector(self.x, self.y, self.z)

class Ray():
    def __init__(self, pos, heading):
        self.live = True
        self.init_pos = pos.copy()
        self.pos = pos
        self.heading = heading
        self.heading.normalise()
        self.reflected = 0
        self.colour = [0, 0, 0]
        self.colours = 1
    
    def add_colour(self, colour):
        self.colours += 1

        r, g, b = self.colour

        r += colour[0]
        g += colour[1]
        b += colour[2]

        if r < 0 : r = 0
        if g < 0 : g = 0
        if b < 0 : b = 0
        if r > 255 : r = 255
        if g > 255 : g = 255
        if b > 255 : b = 255

        self.colour = [r, g, b]
    
    def get_initial_pos(self):
        return f'{self.init_pos.x}:{self.init_pos.y}'

    def get_colour(self):
        r, g, b = self.colour

        r /= self.colours
        g /= self.colours
        b /= self.colours

        return [r, g, b]

    def disable(self):
        self.live = False

class Sphere():
    def __init__(self, x, y, z, radius, colour=[255, 255, 255]):
        self.pos = Vector(x, y, z)
        self.radius = radius
        self.colour = colour
    
    def check_collide_point(self, point):
        distance = (point.pos.x - self.pos.x)**2 + (point.pos.y - self.pos.y)**2 + (point.pos.z - self.pos.z)**2

        if distance < self.radius**2 : return True
        else : return False

class Cube():
    def __init__(self, x, y, z, w, h, d, colour=[255, 255, 255]):
        self.pos = Vector(x, y, z)
        self.w = w
        self.h = h
        self.d = d
        self.colour = colour

    def check_collide_point(self, point):
        x = point.pos.x > self.pos.x and point.pos.x < self.pos.x + self.w
        y = point.pos.y > self.pos.y and point.pos.y < self.pos.y + self.h
        z = point.pos.z > self.pos.z and point.pos.z < self.pos.z + self.d

        return x and y and z

#endregion

#region functions

def clear():
    command('cls')

#endregion

#region global variables

objects = []

rendering_surface_w = 200
rendering_surface_h = 200

rendering_distance = 100

world_box = Cube(0, 0, -1, rendering_surface_w, rendering_surface_h, rendering_distance)

reflection_count = 1

sun_pos = Sphere((rendering_surface_w/2) + rendering_surface_w/5, 0, (rendering_distance/2) - rendering_surface_w/5, 10, [0, 0, 0])

preview_surface = pygame.Surface((500, 500))
rendering_surface = pygame.Surface((rendering_surface_w, rendering_surface_h))
rendering_surface.fill(0)

rays = []

completed_rays = 0

#endregion

# render a simple sphere, again
def output_status():
    clear()
    print('{:,}/{:,}    |   {:.2f}%'.format(completed_rays, rendering_surface_w*rendering_surface_h, (completed_rays / (rendering_surface_w*rendering_surface_h)) * 100))

def create_rays():
    """Creates an array of rays"""
    global rays

    for x in range(rendering_surface_w):
        for y in range(rendering_surface_h):
            pos = Vector(x, y, 0)
            heading = Vector(0, 0.1, 1)
            rays.append(Ray(pos, heading))

def render():
    i = 0
    for ray in rays:
        # check if ray is still in the world box
        if not world_box.check_collide_point(ray):
            x, y = ray.init_pos.x, ray.init_pos.y
            rendering_surface.set_at((x, y), ray.get_colour())

            ray.disable()

        # check if ray is completed it's life cycle
        if not ray.live:
            continue
    
        i += 1

        # move ray
        ray.pos.add(ray.heading)

        # check if ray has collided
        shape_collided_with = None
        for shape in objects:
            if shape.check_collide_point(ray):
                shape_collided_with = shape
                break

        if shape_collided_with is None:
            continue

        # add collided colour
        ray.add_colour(shape_collided_with.colour)

        # check if the ray requires reflection
        if ray.reflected < reflection_count:
            heading = shape.pos - ray.pos
            heading.normalise()
            ray.heading = heading

            ray.reflected += 1
            continue
    
        # check if can see light
        heading = ray.pos - sun_pos.pos
        heading.normalise()

        while True:
            ray.pos.add(heading)

            if sun_pos.check_collide_point(ray):
                ray.add_colour(sun_pos.colour)
                break

            finish = False
            for shape in objects:
                if shape.check_collide_point(ray):
                    r, g, b = sun_pos.colour
                    ray.add_colour([-r, -g, -b])
                    finish = True
                    break
            
            if finish : break
    
        # draw rays' colour to the screen when all reflections are done
        x, y = ray.init_pos.x, ray.init_pos.y
        rendering_surface.set_at((x, y), ray.get_colour())

        ray.disable()

    return i

def view_render():
    global rendering_surface
    size = (500, 550)

    #region init
    screen = pygame.display.set_mode(size)
    screen.fill([255, 255, 255])
    pygame.display.set_icon(screen)
    pygame.display.set_caption('')
    clock, fps = pygame.time.Clock(), 30
    #endregion

    rendering_surface = pygame.transform.scale(rendering_surface, size)

    pygame.image.save(rendering_surface, 'image.png')

    while True:
        #region events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        #endregion

        screen.blit(rendering_surface, (0, 0))

        pygame.display.update()
        clock.tick(fps)

objects = [
    Cube(-10, rendering_surface_h-2, 0, rendering_surface_w+20, 1, rendering_distance, colour=[60, 30, 0]),
    Sphere((rendering_surface_w/2)-10, rendering_surface_h/2, 75, 10, colour=[255, 0, 0]),
    Sphere((rendering_surface_w/2)+15, rendering_surface_h/2, 75, 10, colour=[0, 255, 0]),
    Sphere((rendering_surface_w/2)+7, (rendering_surface_h/2) + 10, 100, 10, colour=[0, 0, 255]),
]

create_rays()

i = 100000
mark = time()
while i != 0:
    i = render()

    clear()
    print(i)
print('Elapsed', mark - time())

view_render()






