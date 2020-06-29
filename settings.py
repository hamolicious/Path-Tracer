
# camera settings
render_distance = 100 # maximum distance a ray is allowed to travel
fov = 90 # cameras field of view
rendering_canvas_size = (400, 400) # resolution of final render
ray_reflections = 5 # amount of reflections rays are allowed to perform

# environment settings
sky_colour = [200, 200, 230] # colour of background

"""
Shapes are defined bellow

Allowed shapes and how to define:
    Sphere -> 'Sphere x_pos y_pos z_pos radius red green blue'
        if 'r' is passed in for any rgb then a random colour will be defined

    Box -> 'Box x_pos y_pos z_pos width height depth red green blue'
        if 'r' is passed in for any rgb then a random colour will be defined
"""
shapes = [
    f'Sphere 200 250 50 50 150 0 150',
    f'Sphere 200 150 50 50 0 150 150',
    f'Box {rendering_canvas_size[0]/2} {rendering_canvas_size[1]} -1000 999999999 20 9999999999 40 20 10',
]

# display screen settings
screen_size = (600, 600) # size to stretch the final render to and screen size to be used for displaying
threads_to_open = 30 # amount of threads to open to render the image
                     # each thread will be responsible for ((canvas_width * canvas_height) / threads_to_open) amount of pixels







