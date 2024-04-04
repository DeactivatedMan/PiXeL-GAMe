import pygame
from pathlib import Path
from mapUnpacker import unpackAll
import subprocess

# Set the pixel dimensions
pixel_size = 16 # <---- Increase for higher resolutions, lol
pixel_width, pixel_height = 16, 16

# Set the window dimensions
window_width, window_height = pixel_width * pixel_size, pixel_height * pixel_size

if (Path.cwd() / "_internal").is_dir(): data = Path.cwd() / "_internal" / "data"
else: data = Path.cwd() / "data"
menuImg = pygame.image.load(data / "menu.png")
iconImg = pygame.image.load(data / "icon.png")
mapData = data / "mapData"

class VariablesClass:
    def __init__(self):
        self.colourDict = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
        self.mapColours = [False, False, False]  # Red, Green, Blue
        self.plrPos = [False, False]  # The player's actual position
        self.mapArray = sorted(mapData.glob('*.png'))

        self.currGame = 0
variables = VariablesClass()

def drawPixel(x, y, code):
    rgb = variables.colourDict[code]
    pygame.draw.rect(screen, rgb, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))

def unpackMap():
    screen.fill((0, 0, 0))
    mapColours = unpackAll(variables.mapArray[variables.currGame])
    variables.mapColours = mapColours

    try:
        for colour in range(3):
            for x in range(16):
                for y in range(16):
                    if mapColours[colour][x][y] == "1":
                        drawPixel(x,y,colour)
                        if colour == 1: variables.plrPos = [x,y]
    except Exception as err:
        print(err)
        pygame.quit()

def movePlr(x: int, y: int) -> None:
    mapColours = variables.mapColours; testPos = variables.plrPos[:]; plrPos = variables.plrPos
    hitWall = False; hitRed = False; isMoved = False

    while not hitWall:
            red = mapColours[0][testPos[0]][testPos[1]]
            blue = mapColours[2][testPos[0]][testPos[1]]

            if blue == "0":
                isMoved = True
                testPos[0] += x
                testPos[1] += y
            elif blue == "1":
                hitWall = True
                testPos[0] -= x
                testPos[1] -= y
            if red == "1":
                hitRed = True
                hitWall = True
    
    if isMoved:
        drawPixel(plrPos[0], plrPos[1], 3)
        variables.plrPos = testPos
        drawPixel(testPos[0], testPos[1], 1)
    if hitRed:
        variables.currGame += 1
        unpackMap()

pygame.display.set_icon(iconImg)
pygame.display.set_caption("PiXeL GAMe")
pygame.init()

screen = pygame.display.set_mode((window_width, window_height))
screen.blit(menuImg, (0, 0))
pygame.display.flip()

running = True
onMenu = True

# Load map
while onMenu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            onMenu = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            onMenu = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[1] <= 127:
                onMenu = False
                unpackMap()
            else:
                subprocess.Popen(f'explorer /open,"{mapData}"')


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_w:
                movePlr(0,-1)
            elif event.key == pygame.K_a:
                movePlr(-1,0)
            elif event.key == pygame.K_s:
                movePlr(0,1)
            elif event.key == pygame.K_d:
                movePlr(1,0)
    pygame.display.flip()

# Quit the game
pygame.quit()