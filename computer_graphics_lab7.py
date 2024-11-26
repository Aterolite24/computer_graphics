import pygame
import numpy as np

pygame.init()

width = 600
height = 500
method_type = 0
running = True
text_colour = (230, 0, 100)
colour = (255, 255, 255)
colour2 = (140, 240, 30)
bg_colour = (0, 0, 0)
display_text = ["", "Bezier Curve", "Hermite Curve"]

screen = pygame.display.set_mode((width, height))
font_object = pygame.font.Font("freesansbold.ttf", 30)


def reset_screen() :
    screen.fill(bg_colour)
    
def put_pixel(x, y):
    screen.set_at((x, height - y), colour)
    
def bezier(u, p0, p1, p2, p3):
    U = np.array([[1, u, u**2, u**3]])
    B = np.array([[1, 0, 0, 0],
                  [-3, 3, 0, 0],
                  [3, -6, 3, 0],
                  [1, 3, -3, 1]])
    P = np.array([p0, p1, p2, p3])
    return tuple(np.dot(np.dot(U, B), P)[0].astype(np.int64))
    
def hermite(u, p0, p1, p2, p3):
    U = np.array([[1, u, u**2, u**3]])
    B = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [-3, -2, 3, -1],
                  [2, 1, -2, 1]])
    P = np.array([p0, p1, p2, p3])
    return tuple(np.dot(np.dot(U, B), P)[0].astype(np.int64))


while running:
    
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                method_type = 1
                reset_screen()
                p0, p1, p2, p3 = (100, 200), (50, 30), (300, 100), (0, 0)
                screen.set_at((100, height - 200), colour)
                screen.set_at((50, height - 30), colour)
                screen.set_at((300, height - 100), colour)
                screen.set_at((0, height - 0), colour)
                u_array = np.linspace(0, 1, 2000)
                for u in u_array:
                    x, y = bezier(u, p0=p0, p1=p1, p2=p2, p3=p3)
                    put_pixel(x, y)
            elif event.key == pygame.K_2:
                method_type = 2
                reset_screen()
                p0, p1, p2, p3 = (200, 300), (100, 300), (300, 100), (0, 0)
                u_array = np.linspace(0, 1, 2000)
                screen.set_at((200, height - 300), colour)
                screen.set_at((100, height - 300), colour)
                screen.set_at((300, height - 100), colour)
                screen.set_at((0, height - 0), colour)
                for u in u_array:
                    x, y = hermite(u, p0=p0, p1=p1, p2=p2, p3=p3)
                    put_pixel(x, y)
                
    text = font_object.render(display_text[method_type], False, text_colour)
    screen.blit(text, (5, 20))
    pygame.display.update()