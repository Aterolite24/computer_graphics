import pygame as py

py.init()

length = 800
screen = py.display.set_mode((length,length))

for i in range(length):
    for j in range(length):
        col = (255,i*255/800,j*255/800)
        screen.set_at((i,j),col)

movie = py.font.Font("freesansbold.ttf",50)

running = True

color = (255,255,255)
while running:

    for event in py.event.get():

        if event.type == py.QUIT:
            running = False

    text = movie.render(" La La Land ", False , color)
    screen.blit(text,(250,250))
    py.draw.circle(screen,color,(29,18),4)
    py.draw.rect(screen,color,py.Rect(25,30,10,10))
    py.draw.rect(screen,color,py.Rect(25,50,20,20))
    py.draw.rect(screen,color,py.Rect(25,80,30,30))
    py.display.update()
