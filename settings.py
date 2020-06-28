
render_distance = 200
fov = 90

ray_reflections = 5

sky_colour = [210, 200, 200]

screen_size = (600, 600)
rendering_canvas_size = (600, 600)

threads_to_open = 20

shapes = [
    f'Sphere {rendering_canvas_size[0]/4} {rendering_canvas_size[1]/4} 150 {rendering_canvas_size[0]/4} 150 150 34',
    f'Sphere {rendering_canvas_size[0]/1.5} {rendering_canvas_size[1]/1.5} 100 {rendering_canvas_size[0]/4} 10 150 150',
    f'Box -100 {rendering_canvas_size[1] * 0.9} -200 {rendering_canvas_size[0] * 10} 10 {render_distance*10} 60 30 0'
]






