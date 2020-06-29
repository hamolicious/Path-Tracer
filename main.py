from vector_class import Vector2D, Vector3D
import pygame
from time import time, gmtime, sleep
from threading import Thread, active_count
import settings
from os import system ; system('cls')
from math import tan
from random import randint
import playsound

#region initialise variables
print('[!] Loading...')
print('[!] Creating Variables')

focal_length = (0.5 * settings.rendering_canvas_size[0]) * tan(settings.fov / 2)
rendering_canvas = pygame.Surface(settings.rendering_canvas_size) ; rendering_canvas.fill(settings.sky_colour)

report = [0 for _ in range(settings.threads_to_open)]
#endregion

#region Functions
print('[!] Creating Functions')

clear = lambda : system('cls')

def pretty_time(gm_time):
    hr = str(gm_time.tm_hour)
    mi = str(gm_time.tm_min)
    se = str(gm_time.tm_sec)

    if len(hr) == 1 : hr = '0' + hr
    if len(mi) == 1 : mi = '0' + mi
    if len(se) == 1 : se = '0' + se

    return f'{hr}:{mi}:{se}'

def map_to_range(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def draw_pixel_to_canvas(pos, colour):
    rendering_canvas.set_at(pos, colour)

def chunk_renderer(id, pixels):
    global report

    done = 0 ; total = len(pixels)

    while len(pixels) > 0:
        temp = []
        for pixel in pixels:
            if pixel.step():
                done += 1
            else:
                temp.append(pixel)

        pixels = temp
        report[id-1] = map_to_range(done, 0, total, 0, 100)

def await_finish():
    system('cls')
    start_time = time()
    while (active_threads := active_count()) > 1:
        system('cls')

        print(f'Complete: {round(sum(report) / len(report), 3)}%')
        print(f'Active Threads: {active_threads-1}/{settings.threads_to_open}')

        elapsed = time() - start_time
        print('Elapsed: ' + pretty_time(gmtime(elapsed)))

        seconds_per_percent = round(sum(report) / len(report), 3) / elapsed
        eta_in_seconds = 100 * seconds_per_percent
        print('Average ETA: ' + pretty_time(gmtime(eta_in_seconds)))

        sleep(0.8)

    print(f'Complete: {sum(report) / len(report)}%')
    end_time = gmtime(time() - start_time)
    system('cls')
    print('Elapsed: ' + pretty_time(end_time))

#endregion

#region shapes
print('[!] Creating Shapes')

class Sphere():
    def __init__(self, x, y, z, r, colour=[255, 255, 255]):
        self.pos = Vector3D(x, y, z)
        self.r = r
        self.colour = colour
    
    def collide_point(self, point):
        return self.pos.dist(point) <= self.r

class Box():
    def __init__(self, x, y, z, w, h, d, colour=[255, 255, 255]):
        self.pos = Vector3D(x, y, z)
        self.size = Vector3D(w, h, d)
        self.colour = colour
    
    def collide_point(self, point):
            return  point.x >= self.pos.x - self.size.x/2 and point.x <= self.pos.x + self.size.x/2 and\
                    point.y >= self.pos.y - self.size.y/2 and point.y <= self.pos.y + self.size.y/2 and\
                    point.z >= self.pos.z - self.size.z/2 and point.z <= self.pos.z + self.size.z/2

#endregion

#region path tracing classes
print('[!] Creating Classes')

class Light():
    def __init__(self, x, y, z):
        self.pos = Vector3D(x, y, z)

class Ray():
    def __init__(self, x, y, z):
        self.pos = Vector3D(x, y, z)
        self.bounces = 0

        self.heading = self.pos - Vector3D(settings.rendering_canvas_size[0]/2, settings.rendering_canvas_size[1]/2, -focal_length)
        self.heading.normalise()

class Pixel():
    def __init__(self, x, y):
        self.pos = Vector2D(x, y)
        self.colour = [0, 0, 0] ; self.colour_additions = 0

        self.raw_colour_ray = Ray(x, y, 0) ; self.raw_ray_finished = False
        self.light_rays = [] ; self.light_ray_finished = False
    
    def check_shape_collisions(self, ray):
        for shape in shapes:
            if shape.collide_point(ray.pos):
                return shape
        
        return False

    def add_colour(self, colour):
        self.colour[0] += colour[0]
        self.colour[1] += colour[1]
        self.colour[2] += colour[2]

        self.colour_additions += 1

    def get_colour(self):
        if sum(self.colour) == 0:
            return settings.sky_colour
        
        if self.colour_additions == 0:
            return self.colour
        
        if self.colour[0] < 0 : self.colour[0] = 0
        if self.colour[1] < 0 : self.colour[1] = 0
        if self.colour[2] < 0 : self.colour[2] = 0

        return [self.colour[0] / self.colour_additions, self.colour[1] / self.colour_additions, self.colour[2] / self.colour_additions]

    def deflect_ray_from_shape(self, ray, shape):
        ray.heading = (ray.pos - shape.pos) + ray.heading
        ray.bounces += 1

    def advance_raw_ray(self):
        if self.raw_ray_finished:
            return

        # move ray
        self.raw_colour_ray.pos.add(self.raw_colour_ray.heading)

        # out of render distance
        if self.raw_colour_ray.pos.dist([self.pos.x, self.pos.y, 0]) >= settings.render_distance:
            self.raw_ray_finished = True

        # check for collisions
        if (result := self.check_shape_collisions(self.raw_colour_ray)) != False:
            self.add_colour(result.colour)

            # save last collision
            light_ray = Ray(self.raw_colour_ray.pos.x, self.raw_colour_ray.pos.y, self.raw_colour_ray.pos.z)
            light_ray.heading = light.pos - self.raw_colour_ray.pos
            light_ray.heading.normalise()
            distance_from_light = light_ray.pos.dist(light.pos)
            self.light_rays.append([light_ray, False, distance_from_light])

            if self.raw_colour_ray.bounces >= settings.ray_reflections:
                self.raw_ray_finished = True
            else:
                self.deflect_ray_from_shape(self.raw_colour_ray, result)

    def advance_light_ray(self):
        temp = []
        for ray in self.light_rays:
            ray[0].pos.add(ray[0].heading)

            for shape in shapes:
                if shape.collide_point(ray[0].pos):
                    ray[1] = True
                    break

            if ray[0].pos.dist(light.pos) < 5:
                ray[1] = True

            if ray[1]:
                val = map_to_range(ray[0].pos.dist(light.pos), 0, ray[2], settings.light_strength, -settings.light_strength/2)
                self.add_colour([val, val, val])
            else:
                temp.append(ray)
        
        self.light_rays = temp
        if len(self.light_rays) == 0:
            self.light_ray_finished = True

    def step(self):
        if not self.raw_ray_finished:
            self.advance_raw_ray()
        elif len(self.light_rays) > 0:
            self.advance_light_ray()
        else:
            self.light_ray_finished = True

        if self.raw_ray_finished and self.light_ray_finished:
            draw_pixel_to_canvas(self.pos.get(), self.get_colour())
            return True
        else:
            return False
#endregion

#region path trace

#load and create shapes
print('[!] Loading Shapes')

shapes = []
for i in settings.shapes:
    name = i.split(' ')[0]

    if name.lower() == 'sphere':
        _, x, y, z, rad, r, g, b = i.split(' ')
        if r == g == b == 'r' : r = randint(0, 150) ; g = randint(0, 150) ; b = randint(0, 150)

        shapes.append(Sphere(float(x), float(y), float(z), float(rad), colour=[float(r), float(g), float(b)]))
    elif name.lower() == 'box':
        _, x, y, z, w, h, d, r, g, b = i.split(' ')
        if r == g == b == 'r' : r = randint(0, 150) ; g = randint(0, 150) ; b = randint(0, 150)

        shapes.append(Box(float(x), float(y), float(z), float(w), float(h), float(d), colour=[float(r), float(g), float(b)]))

# load and create lights
print('[!] Loading Light')
x, y, z = settings.light.split(' ')
light = Light(float(x), float(y), float(z))

# create pixel threads
print('[!] Creating Threads')
pixels = []
id = 1
for y in range(settings.rendering_canvas_size[0]):
    for x in range(settings.rendering_canvas_size[1]):
        pixels.append(Pixel(x, y))

        if len(pixels) == int((settings.rendering_canvas_size[0] * settings.rendering_canvas_size[1]) / settings.threads_to_open):
            thread = Thread(target=chunk_renderer, args=(id, pixels))
            thread.start()
            pixels = []

            print(f' |___ Created {id}/{settings.threads_to_open} Threads')            
            id += 1
if len(pixels) != 0:
    thread = Thread(target=chunk_renderer, args=(id+1, pixels))
    thread.start()

print(f'[!] Started {active_count()-1} Threads')

clear()
print('[!] Loading Done...')
await_finish()

if settings.play_sound_when_done:
    playsound.playsound('Data/done_sound.mp3', block=False)

#endregion

#region pygame
pygame.init()
screen = pygame.display.set_mode(settings.screen_size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 60

rendering_canvas = pygame.transform.scale(rendering_canvas, settings.screen_size)
pygame.image.save(rendering_canvas, 'render_result.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.blit(rendering_canvas, (0, 0))

    pygame.display.update()
    clock.tick(fps)
#endregion



