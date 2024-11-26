import pygame
import math
import numpy as np
from collections import deque

pygame.init()


colour = (150, 230, 200)
fill_colour = (255, 100, 0)
bg_colour = (0, 0, 0)
points = [(200, 150), (400, 300), (600, 200), (500, 500), (300, 400)]
points2 = [(200, 150), (400, 300), (600, 500), (400, 200), (300, 200), (400, 350)]

font_object = pygame.font.Font("freesansbold.ttf", 30)
text1,  text2, text3, text4, text5, text6 = "Ellipse - Parametric", "Ellipse - Polynomial", "Ellipse - Bresenham", "Ellipse - Mid Point", "Polygon - Scan Line", "Polygon - Seed Fill"
display_text = text1
text = font_object.render(display_text, True, colour)

screen = pygame.display.set_mode((800, 600))

xc = 400
yc = 300


def reset_screen() :
    screen.fill(bg_colour)

def plot_four_points(x, y) :
    screen.set_at([xc + x, yc + y], colour)
    screen.set_at([xc - x, yc + y], colour)
    screen.set_at([xc + x, yc - y], colour)
    screen.set_at([xc - x, yc - y], colour)

def parametric_ellipse() :
    rx = 250
    ry = 130
    for theta in np.linspace(0, (math.pi)/2, 450) :
        plot_four_points(round(rx*math.cos(theta)), round(ry*math.sin(theta)))
    
def polynomial_ellipse() :
    rx = 220
    ry = 150
    x, y = 0, 0
    for y in range(0, ry + 1) :
        plot_four_points(round(((rx*rx)*(1 - (y*y)/(ry*ry)))**0.5), y)
    for x in range(0, rx + 1) :
        plot_four_points(x, round(((ry*ry)*(1 - (x*x)/(rx*rx)))**0.5))

def bresenham_ellipse() :
    rx = 300
    ry = 100
    r = max(rx, ry)
    x = 0
    y = r
    d = r
    e = 1.0*ry/r
    f = 1.0*rx/r

    while y >= x:
        plot_four_points(round(f*x), round(e*y))
        plot_four_points(round(f*y), round(e*x))
        x += 1
        if d < 0 :
            y -= 1
            d -= 2*(x - y)
        else :
            d = d - 2*x


def midpoint_ellipse() :
    rx = 200
    ry = 130
    x = 0
    y = ry

    d1 = ((ry*ry) - (rx*rx*ry) + (0.25*rx*rx));
    dx = 2*ry*ry*x
    dy = 2*rx*rx*y

    while dx < dy :
        plot_four_points(x, y)
        if (d1 < 0):
            x += 1
            dx += (2*ry*ry)
            d1 += dx + (ry*ry)
        else :
            x += 1
            y -= 1
            dx += 2*ry*ry
            dy -= (2*rx*rx)
            d1 += dx - dy + (ry*ry)

        d2 = (((ry * ry) * ((x + 0.5) * (x + 0.5))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry))
    
    while y >= 0 :
        plot_four_points(x, y)
        
        if d2 > 0 :
            y -= 1
            dy -= (2*rx*rx)
            d2 += rx*rx - dy
        else :
            y -= 1
            x += 1
            dx += 2*ry*ry
            dy -= (2*rx*rx)
            d2 += dx - dy + rx*rx

def scan_line_fill() :
    
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)
    
    for y in range(min_y, max_y + 1) :

        intersections = []
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            if p1[1] == p2[1]:
                continue
            if min(p1[1], p2[1]) <= y < max(p1[1], p2[1]):
                x = int(p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]))
                intersections.append(x)

        intersections.sort()
        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                pygame.draw.line(screen, fill_colour, (intersections[i], y), (intersections[i+1], y))

def seed_fill(x, y):

    try:
        queue = deque()
        queue.append((x, y))
        while queue:
            x, y = queue.popleft()

            if screen.get_at((x, y))[:3] != colour and screen.get_at((x, y))[:3] != fill_colour:
                screen.set_at((x, y), fill_colour)

                if x > 0:
                    queue.append((x - 1, y))
                if x < 800:
                    queue.append((x + 1, y))
                if y > 0:
                    queue.append((x, y - 1))
                if y < 600:
                    queue.append((x, y + 1))
    except :
        print("seed fill used ouside")

# parametric_ellipse()

running = True
while running:

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
    
        if event.type == pygame.MOUSEBUTTONDOWN :
            x, y = pygame.mouse.get_pos()
            seed_fill(x, y)

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_1 :
                display_text = text1
                reset_screen()
                parametric_ellipse()
            elif event.key == pygame.K_2 :
                display_text = text2
                reset_screen()
                polynomial_ellipse()
            elif event.key == pygame.K_3 :
                display_text = text3
                reset_screen()
                bresenham_ellipse()
            elif event.key == pygame.K_4 :
                display_text = text4
                reset_screen()
                midpoint_ellipse()
            elif event.key == pygame.K_5 :
                display_text = text5
                reset_screen()
                pygame.draw.polygon(screen, colour, points, 1)
                scan_line_fill()
            elif event.key == pygame.K_6 :
                display_text = text6
                reset_screen()
                pygame.draw.polygon(screen, colour, points2, 1)

    text = font_object.render(display_text, False, colour)
    screen.blit(text, (5, 20))
    pygame.display.update()
