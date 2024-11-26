import pygame
import numpy as np

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

bg_colour = (0, 0, 0)

surfaces = np.array([[[100, 400, 40], [300, 100, 90], [700, 300, 50]],
                      [[300, 100, 90], [700, 300, 50], [500, 475, 100]]])

colour_surfaces = np.array([[255, 0, 0], [0, 0, 255]])

# 0 - transparent, 1 - opaque
opacities = [0.9, 0.5]

def calc_surface_vector(surface):
    v1 = surface[1] - surface[0]
    v2 = surface[2] - surface[0]

    normal_vector = np.cross(v1, v2)
    a, b, c = normal_vector

    d = -np.dot(normal_vector, surface[0])

    return a, b, c, d    

def get_intersection(j, x0, y0, x1, y1):
    m = (y1 - y0) / (x1 - x0)
    x_intersection = x0 + (j - y0) / m

    return round(x_intersection)


def z_buffer():
    depth_buffer = np.full((screen_width, screen_height), -1)
    for k in range(len(surfaces)):
        surface = surfaces[k]
        colour = colour_surfaces[k]
        sorted_surface = sorted(surface, key=lambda point: point[1])
        a, b, c, d = calc_surface_vector(sorted_surface)

        for j in range(sorted_surface[0][1], sorted_surface[2][1] + 1):
            if j < sorted_surface[1][1]:
                intersection1 = get_intersection(j, sorted_surface[0][0], sorted_surface[0][1], sorted_surface[1][0], sorted_surface[1][1])
                intersection2 = get_intersection(j, sorted_surface[0][0], sorted_surface[0][1], sorted_surface[2][0], sorted_surface[2][1])
            else :
                intersection1 = get_intersection(j, sorted_surface[2][0], sorted_surface[2][1], sorted_surface[1][0], sorted_surface[1][1])
                intersection2 = get_intersection(j, sorted_surface[2][0], sorted_surface[2][1], sorted_surface[0][0], sorted_surface[0][1])
            x0 = min(intersection1, intersection2)
            x1 = max(intersection1, intersection2)
            z = -a*x0 - b*j - d
            z = z/c
            if depth_buffer[x0][j] == -1 or depth_buffer[x0][j] > z:
                depth_buffer[x0][j] = z
                screen.set_at((x0, j), colour)
            for i in range(x0 + 1, x1 + 1):
                z = z - a/c
                if depth_buffer[i][j] == -1 or depth_buffer[i][j] > z:
                    depth_buffer[i][j] = z
                    screen.set_at((i, j), colour)

def a_buffer_function():
    a_buffer = [[[] for _ in range(screen_height)] for _ in range(screen_width)]
    for k in range(len(surfaces)):
        surface = surfaces[k]
        colour = colour_surfaces[k]
        sorted_surface = sorted(surface, key=lambda point: point[1])
        a, b, c, d = calc_surface_vector(sorted_surface)

        for j in range(sorted_surface[0][1], sorted_surface[2][1] + 1):
            if j < sorted_surface[1][1]:
                intersection1 = get_intersection(j, sorted_surface[0][0], sorted_surface[0][1], sorted_surface[1][0], sorted_surface[1][1])
                intersection2 = get_intersection(j, sorted_surface[0][0], sorted_surface[0][1], sorted_surface[2][0], sorted_surface[2][1])
            else :
                intersection1 = get_intersection(j, sorted_surface[2][0], sorted_surface[2][1], sorted_surface[1][0], sorted_surface[1][1])
                intersection2 = get_intersection(j, sorted_surface[2][0], sorted_surface[2][1], sorted_surface[0][0], sorted_surface[0][1])
            x0 = min(intersection1, intersection2)
            x1 = max(intersection1, intersection2)
            z = -a*x0 - b*j - d
            z = z/c
            a_buffer[x0][j].append((z, colour, opacities[k]))
            for i in range(x0 + 1, x1 + 1):
                z = z - a/c
                a_buffer[i][j].append((z, colour, opacities[k]))

    for i in range(screen_width):
        for j in range(screen_height):
            if len(a_buffer[i][j]) == 0:
                continue            
            temp_colour = np.array([0, 0, 0])
            temp_opacity = 0
            for z, colour, opacity in sorted(a_buffer[i][j], reverse=True, key=lambda point: point[0]):
                colour = np.array(colour)
                temp_colour = (temp_colour * temp_opacity + colour * opacity * (1 - temp_opacity)) / (temp_opacity + opacity*(1 - temp_opacity))
                temp_opacity = temp_opacity + opacity * (1 - temp_opacity)
            screen.set_at((i, j), temp_colour*temp_opacity)


running = True

screen.fill((0, 0, 0))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                screen.fill((0, 0, 0))
                z_buffer()
            if event.key == pygame.K_2:
                screen.fill((0, 0, 0))
                a_buffer_function()

    pygame.display.update()