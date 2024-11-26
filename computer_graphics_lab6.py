
# 3D

import pygame
import numpy as np

pygame.init()

text_colour = (230, 0, 100)
white = (255, 255, 255)
colour = (240, 30, 50)
colour2 = (140, 240, 30)
bg_colour = (0, 0, 0)

font_object = pygame.font.Font("freesansbold.ttf", 30)
display_text = ["", "Cohen-Sutherland 3D", "Cyrus-Beck 3D", "Liang-Barsky 3D"]

text = font_object.render(display_text[0], False, text_colour)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

def reset_screen() :
    screen.fill(bg_colour)

##########  Cohen Sutherland ###########

INSIDE = 0
LEFT = 1  
RIGHT = 2 
BOTTOM = 4
TOP = 8   
NEAR = 16 
FAR = 32

def compute_outcode(x, y, z, xmin, xmax, ymin, ymax, zmin, zmax):
    outcode = INSIDE
    if x < xmin:
        outcode |= LEFT
    elif x > xmax:
        outcode |= RIGHT
    if y < ymin:
        outcode |= BOTTOM
    elif y > ymax:
        outcode |= TOP
    if z < zmin:
        outcode |= NEAR
    elif z > zmax:
        outcode |= FAR

    return outcode

def cohen_sutherland_clip_3d(x1, y1, z1, x2, y2, z2, xmin, xmax, ymin, ymax, zmin, zmax):
    outcode1 = compute_outcode(x1, y1, z1, xmin, xmax, ymin, ymax, zmin, zmax)
    outcode2 = compute_outcode(x2, y2, z2, xmin, xmax, ymin, ymax, zmin, zmax)
    
    accept = False
    
    while True:
        if outcode1 == 0 and outcode2 == 0:
            accept = True
            break
        elif (outcode1 & outcode2) != 0:
            break
        else:
            if outcode1 != 0:
                outcode_out = outcode1
            else:
                outcode_out = outcode2

            if outcode_out & LEFT:
                x = xmin
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                z = z1 + (z2 - z1) * (xmin - x1) / (x2 - x1)
            elif outcode_out & RIGHT:
                x = xmax
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                z = z1 + (z2 - z1) * (xmax - x1) / (x2 - x1)
            elif outcode_out & BOTTOM:
                y = ymin
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                z = z1 + (z2 - z1) * (ymin - y1) / (y2 - y1)
            elif outcode_out & TOP:
                y = ymax
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                z = z1 + (z2 - z1) * (ymax - y1) / (y2 - y1)
            elif outcode_out & NEAR:
                z = zmin
                x = x1 + (x2 - x1) * (zmin - z1) / (z2 - z1)
                y = y1 + (y2 - y1) * (zmin - z1) / (z2 - z1)
            elif outcode_out & FAR:
                z = zmax
                x = x1 + (x2 - x1) * (zmax - z1) / (z2 - z1)
                y = y1 + (y2 - y1) * (zmax - z1) / (z2 - z1)
            
            if outcode_out == outcode1:
                x1, y1, z1 = x, y, z
                outcode1 = compute_outcode(x1, y1, z1, xmin, xmax, ymin, ymax, zmin, zmax)
            else:
                x2, y2, z2 = x, y, z
                outcode2 = compute_outcode(x2, y2, z2, xmin, xmax, ymin, ymax, zmin, zmax)
    
    print("Cohen-Sutherland 3D : ")
    if accept:
        print(f"Line accepted from ({x1}, {y1}, {z1}) to ({x2}, {y2}, {z2})")
        return ((x1, y1, z1), (x2, y2, z2))
    else:
        print("Line rejected")
        return None
    
##########  Cohen-Sutherland ###########


#############  Cyrus-Beck ##############

def dot(v1, v2):
    return np.dot(v1, v2)

def cyrus_beck_clip_3d(p1, p2, poly_faces):
    d = np.subtract(p2, p1)
    t_in = 0
    t_out = 1
    
    for face in poly_faces:
        p_face = face['point']
        n_face = face['normal']
        p_face_minus_p1 = np.subtract(p_face, p1)
        num = dot(n_face, p_face_minus_p1)
        den = dot(n_face, d)

        if den != 0:
            t = num / den
            if den < 0:  # Line is entering
                t_in = max(t_in, t)
            else:  # Line is leaving
                t_out = min(t_out, t)
    
    print("Cyrus-Beck 3D : ")
    if t_in <= t_out:
        clipped_p1 = p1 + t_in * d
        clipped_p2 = p1 + t_out * d
        print(f"Line accepted from {clipped_p1} to {clipped_p2}")
        return clipped_p1, clipped_p2
    else:
        print("Line rejected")
        return None
    
#############  Cyrus-Beck ##############


############# Liang-Barsky #############

def liang_barsky_clip_3d(x1, y1, z1, x2, y2, z2, xmin, xmax, ymin, ymax, zmin, zmax):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    t_min = 0.0
    t_max = 1.0
    
    for p, q in [
        (-dx, x1 - xmin), (dx, xmax - x1),  # x clipping
        (-dy, y1 - ymin), (dy, ymax - y1),  # y clipping
        (-dz, z1 - zmin), (dz, zmax - z1)   # z clipping
    ]:
        if p == 0:  # Parallel to the plane
            if q < 0:
                # Line is outside
                print("Line rejected (parallel and outside clipping region)")
                return None
        else:
            t = q / p
            if p < 0:
                t_min = max(t_min, t)  # Line is entering
            else:
                t_max = min(t_max, t)  # Line is leaving

    print("Liang-Barsky 3D : ")
    if t_min <= t_max:
        clipped_x1 = x1 + t_min * dx
        clipped_y1 = y1 + t_min * dy
        clipped_z1 = z1 + t_min * dz
        clipped_x2 = x1 + t_max * dx
        clipped_y2 = y1 + t_max * dy
        clipped_z2 = z1 + t_max * dz
        
        print(f"Line accepted from ({clipped_x1}, {clipped_y1}, {clipped_z1}) to ({clipped_x2}, {clipped_y2}, {clipped_z2})")
        return ((clipped_x1, clipped_y1, clipped_z1), (clipped_x2, clipped_y2, clipped_z2))
    else:
        print("Line rejected")
        return None
    
############# Liang-Barsky #############


############ Projection ###############

camera = (0, 0, 0)
focal_length = 20

def project_3d_to_2d(point_3d):
    x, y, z = point_3d
    cx, cy, cz = camera

    if z - cz != 0:
        x_2d = focal_length * (x - cx) / (z - cz) + screen_width / 2
        y_2d = focal_length * (y - cy) / (z - cz) + screen_height / 2
    else:
        x_2d, y_2d = screen_width / 2, screen_height / 2

    return (int(x_2d), int(y_2d))

############ Projection ###############


method_type = 0

running = True
while running:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                method_type = 1
                reset_screen()
                xmin, xmax = -10, 10
                ymin, ymax = -10, 10
                zmin, zmax = -10, 10
                x1, y1, z1 = -15, 5, 5
                x2, y2, z2 = 5, 5, 5
                full_line_2D_1, full_line_2D_2 = project_3d_to_2d([x1, y1, z1]), project_3d_to_2d([x2, y2, z2])
                pygame.draw.line(screen, colour, full_line_2D_1, full_line_2D_2)
                clipped_line_3D_1, clipped_line_3D_2 = cohen_sutherland_clip_3d(x1, y1, z1, x2, y2, z2, xmin, xmax, ymin, ymax, zmin, zmax)
                clipped_line_2D_1, clipped_line_2D_2 = project_3d_to_2d(clipped_line_3D_1), project_3d_to_2d(clipped_line_3D_2)
                pygame.draw.line(screen, colour2, clipped_line_2D_1, clipped_line_2D_2)

            elif event.key == pygame.K_2:
                method_type = 2
                reset_screen()
                polyhedron_faces = [
                    {'point': np.array([1, 0, 0]), 'normal': np.array([1, 0, 0])},
                    {'point': np.array([0, 0, 0]), 'normal': np.array([-1, 0, 0])},
                    {'point': np.array([0, 1, 0]), 'normal': np.array([0, 1, 0])},
                    {'point': np.array([0, 0, 0]), 'normal': np.array([0, -1, 0])},
                    {'point': np.array([0, 0, 1]), 'normal': np.array([0, 0, 1])},
                    {'point': np.array([0, 0, 0]), 'normal': np.array([0, 0, -1])}
                ]
                p1 = np.array([-1, 0.5, 0.5])
                p2 = np.array([2, 0.5, 0.5])
                full_line_2D_1, full_line_2D_2 = project_3d_to_2d([p1[0], p1[1], p1[2]]), project_3d_to_2d([p2[0], p2[1], p2[2]])
                pygame.draw.line(screen, colour, full_line_2D_1, full_line_2D_2)
                clipped_line_3D_1, clipped_line_3D_2 = cyrus_beck_clip_3d(p1, p2, polyhedron_faces)
                clipped_line_2D_1, clipped_line_2D_2 = project_3d_to_2d(clipped_line_3D_1), project_3d_to_2d(clipped_line_3D_2)
                pygame.draw.line(screen, colour2, clipped_line_2D_1, clipped_line_2D_2)

            elif event.key == pygame.K_3:
                method_type = 3
                reset_screen()
                xmin, xmax = -10, 10
                ymin, ymax = -10, 10
                zmin, zmax = -10, 10
                x1, y1, z1 = -15, 5, 20
                x2, y2, z2 = 10, 5, 5
                full_line_2D_1, full_line_2D_2 = project_3d_to_2d([x1, y1, z1]), project_3d_to_2d([x2, y2, z2])
                pygame.draw.line(screen, colour, full_line_2D_1, full_line_2D_2)
                clipped_line_3D_1, clipped_line_3D_2 = liang_barsky_clip_3d(x1, y1, z1, x2, y2, z2, xmin, xmax, ymin, ymax, zmin, zmax)
                clipped_line_2D_1, clipped_line_2D_2 = project_3d_to_2d(clipped_line_3D_1), project_3d_to_2d(clipped_line_3D_2)
                pygame.draw.line(screen, colour2, clipped_line_2D_1, clipped_line_2D_2)

    text = font_object.render(display_text[method_type], False, text_colour)
    screen.blit(text, (5, 20))
    pygame.display.update()