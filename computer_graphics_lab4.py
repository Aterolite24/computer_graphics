import pygame
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

pygame.init()

text_colour = (230, 0, 200)
colour = (0, 30, 250)
colour2 = (140, 240, 30)
fill_colour = (255, 0, 0)
white = (255, 255, 255)
bg_colour = (0, 0, 0)
width = 800
height = 600

x_minw, x_maxw = 100, 736
y_minw, y_maxw = 40, 560
x_minv, x_maxv = 250, 736
y_minv, y_maxv = 90, 450

font_object = pygame.font.Font("freesansbold.ttf", 30)
display_text = ["Triangle ", "Translation", "Scaling", "Rotation", "Shearing", "Reflection about y=mx+c", "Rotation and scaling about point", "Window", "Viewport"]
image_path = os.getenv('PATH_OF_IMAGE')
print(f"Image path from .env: {image_path}")

# Load the image
try:
    img = pygame.image.load(image_path)
    img = pygame.surfarray.array3d(img)  # Convert to NumPy array
except pygame.error as e:
    print(f"Failed to load image: {e}")
    pygame.quit()
    exit()

# Get the dimensions of the image
height, width = img.shape[:2]
print(height, width)

screen = pygame.display.set_mode((width, height))

triangle_points = np.array(((10, 70, 100), (20, 120, 20), (1, 1, 1)))

def reset_screen() :
    screen.fill(bg_colour)

def draw(figure, colour):
    tmp_fig = np.array(figure.T[:, :2])
    tmp_fig[:, 1] = height - tmp_fig[:, 1]
    pygame.draw.polygon(screen, colour, tmp_fig, 1)

def translation(dx, dy, points = triangle_points):
    mat = np.array(((1, 0, dx),
                    (0, 1, dy), 
                    (0, 0, 1)))
    return np.matmul(mat, points)

def scaling(sx, sy, points = triangle_points):
    mat = np.array(((sx, 0, 0),
                    (0, sy, 0),
                    (0, 0, 1)))
    return np.matmul(mat, points)

def rotation(theta, points = triangle_points):
    mat = np.array(((np.cos(theta), -np.sin(theta), 0),
                    (np.sin(theta), np.cos(theta), 0),
                    (0, 0, 1)))
    return np.matmul(mat, points)

def shearing(shx, shy, points = triangle_points):
    mat = np.array(((1, shy, 0),
                    (shx, 1, 0),
                    (0, 0, 1)))
    return np.matmul(mat, points)

def reflection(m, c, points = triangle_points):
    mat = np.array((((1-m**2)/(m**2+1), (2*m)/(m**2+1), -(2*m*c)/(m**2+1)),
                    ((2*m)/(m**2+1), (m**2-1)/(m**2+1), (2*c)/(m**2+1)),
                    (0, 0, 1)))
    return np.matmul(mat, points)

def rotation_and_scaling(x0, y0, theta, sx, sy, points = triangle_points):
    temp_points1 = translation(-x0, -y0, points)
    temp_points2 = np.array(rotation(theta, temp_points1))
    temp_points3 = np.array(scaling(sx, sy, temp_points2))
    temp_points4 = np.array(translation(x0, y0, temp_points3))
    return temp_points4

def window(image_path):
    imp = pygame.image.load(image_path).convert()
    screen.blit(imp, (0, 0))
    pygame.draw.line(screen, white, [x_minw, 0], [x_minw, 600])
    pygame.draw.line(screen, white, [x_maxw, 0], [x_maxw, 600])
    pygame.draw.line(screen, white, [0, y_minw], [800, y_minw])
    pygame.draw.line(screen, white, [0, y_maxw], [800, y_maxw])

def viewport(image_path):
    img = pygame.surfarray.array3d(pygame.image.load(image_path).convert())
    
    # Get the dimensions of the image
    height, width = img.shape[:2]
    
    sx = (x_maxv - x_minv) / (x_maxw - x_minw)
    sy = (y_maxv - y_minv) / (y_maxw - y_minw)
    
    for x in range(x_minw, x_maxw + 1):
        for y in range(y_minw, y_maxw + 1):
            # Ensure x and y are within image bounds before accessing img[x][y]
            if 0 <= x < width and 0 <= y < height:
                xv = round(x_minv + (x - x_minw) * sx)
                yv = round(y_minv + (y - y_minw) * sy)
                
                # Ensure the viewport coordinates are within the screen bounds
                if 0 <= xv < width and 0 <= yv < height:
                    screen.set_at([xv, yv], img[x, y])


method_type = 0
draw(triangle_points, colour)
running = True
while running:

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                method_type = 0
                reset_screen()
                draw(triangle_points, colour)
            elif event.key == pygame.K_1:
                method_type = 1
                reset_screen()
                draw(triangle_points, colour)
                mod_points = translation(40, 100)
                draw(mod_points, colour2)
            elif event.key == pygame.K_2:
                method_type = 2
                reset_screen()
                draw(triangle_points, colour)
                mod_points = scaling(1.2, 1.7)
                draw(mod_points, colour2)
            elif event.key == pygame.K_3:
                method_type = 3
                reset_screen()
                draw(triangle_points, colour)
                mod_points = rotation(0.5)
                draw(mod_points, colour2)
            elif event.key == pygame.K_4:
                method_type = 4
                reset_screen()
                draw(triangle_points, colour)
                mod_points = shearing(0.1, 1.5)
                draw(mod_points, colour2)
            elif event.key == pygame.K_5:
                method_type = 5
                reset_screen()
                draw(triangle_points, colour)
                m, c = 2, 35
                mod_points = reflection(m, c)
                line = np.array(((0, width), (m*0+c, m*width+c), (1, 1)))
                draw(line, white)
                draw(mod_points, colour2)
            elif event.key == pygame.K_6:
                method_type = 6
                reset_screen()
                draw(triangle_points, colour)
                mod_points = rotation_and_scaling(-10, -10, 0.1, 4, 4)
                draw(mod_points, colour2)
            elif event.key == pygame.K_7:
                method_type = 7
                reset_screen()
                window(image_path)
            elif event.key == pygame.K_8:
                method_type = 8
                reset_screen()
                viewport(image_path)

    text = font_object.render(display_text[method_type], False, text_colour)
    screen.blit(text, (5, 20))
    pygame.display.update()
