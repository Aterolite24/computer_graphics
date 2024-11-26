import pygame
import numpy as np
import math

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

light_position = np.array([10, -8, -8])
camera_position = np.array([0, 0, -7])

ambient_color = np.array([0.1, 0.1, 0.1])
diffuse_color = np.array([0.7, 0.1, 0.3])
specular_color = np.array([1.0, 1.0, 1.0])
shininess = 10

sphere_radius = 2
sphere_center = np.array([0, 0, 0])

ambient_intensity = 0.3
light_intensity = 1.0

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def phong_shading(point, normal):
    ambient = ambient_intensity * ambient_color
    light_dir = normalize(light_position - point)
    diffuse = light_intensity * diffuse_color * max(np.dot(normal, light_dir), 0)
    view_dir = normalize(camera_position - point)
    reflect_dir = normalize(2 * np.dot(normal, light_dir) * normal - light_dir)
    specular = light_intensity * specular_color * (max(np.dot(view_dir, reflect_dir), 0) ** shininess)

    return ambient + diffuse + specular

def project_to_2d(point_3d):
    x, y, z = point_3d
    fov = 500
    if z == 0:
        z = 0.001
    x_2d = int(screen_width / 2 + (fov * x) / (z + 5))
    y_2d = int(screen_height / 2 - (fov * y) / (z + 5))
    return x_2d, y_2d

def plot_point(point):
    view_dir = view_dir = normalize(camera_position - point)
    normal = normalize(point - sphere_center)
    if(np.dot(view_dir, normal) > 0):
        color = phong_shading(point, normal)
        color = np.clip(color * 255, 0, 255).astype(int)
        x_2d, y_2d = project_to_2d(point)
        pygame.draw.circle(screen, color, (x_2d, y_2d), 2)

def render_sphere():
    for i in np.arange(-sphere_radius, sphere_radius, 0.01):
        y = i + sphere_center[1]
        circle_radius = math.sqrt(max(sphere_radius**2 - i**2, 0))
        for j in np.arange(-circle_radius, circle_radius, 0.01):
            x = j + sphere_center[0]
            k = math.sqrt(max(sphere_radius**2 - j**2 - i**2, 0))

            z = k + sphere_center[2]
            point = np.array([x, y, z])

            plot_point(point)

            z = sphere_center[2] - k
            point = np.array([x, y, z])

            plot_point(point)

            
running = True

screen.fill((0, 0, 0))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                render_sphere()

    pygame.display.update()
