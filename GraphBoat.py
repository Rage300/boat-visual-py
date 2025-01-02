import pandas as pd
import pygame
import os

#Parameters
file_name = r'C:\Users\rage3\OneDrive\Documents\BoatGraphProgram\sailboat_data.txt'
inputDelay = 200

#FUNCTIONS:
#Load csv
def load_csv(file_name):
    df = pd.read_csv(file_name, skiprows=4)
    return df

#Timestamp forward
def timestamp_forward(data, timestamp, boatHull):
    pygame.transform.rotate(boatHull, data.iloc[timestamp, 6])
    boatHull_rect = boatHull.get_rect(center = (500, SCREEN_HEIGHT/2-100))
    #print(data.iloc[timestamp, 6])
    
#Timestamp backward
def timestamp_backward(data, timestamp, boatHull):
    data = data

#Load csv
data = load_csv(r'C:\Users\rage3\OneDrive\Documents\BoatGraphProgram\sailboat_data.txt')
timestamp = 0

#Pygame initialization
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Courier', 30)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
inputTimer = 0
pygame.display.set_caption("Fancy Boat Display")

#Colors
white = [255, 255, 255]
black = [0, 0, 0]
brown = [100, 42, 42]

#Objects
middleLine = pygame.Rect(SCREEN_WIDTH/2, 0, 1, 600)

global boatHull
global boatSail
global boatRudder

hullImage = pygame.image.load(r'C:\Users\rage3\OneDrive\Documents\BoatGraphProgram\boatScaled.png')
sailImage = pygame.image.load(r'C:\Users\rage3\OneDrive\Documents\BoatGraphProgram\sailScaled.png')
rudderImage = pygame.image.load(r'C:\Users\rage3\OneDrive\Documents\BoatGraphProgram\rudder.png')
hullImageRotate = pygame.transform.rotate(hullImage, data.iloc[0, 6])
sailImageRotate = pygame.transform.rotate(sailImage, data.iloc[0, 6])
rudderImageRotate = pygame.transform.rotate(rudderImage, data.iloc[0, 6])
boatHull_orig = pygame.transform.scale(hullImageRotate, (200, 200))
boatSail = pygame.transform.scale(sailImageRotate, (200, 200))
boatRudder = pygame.transform.scale(rudderImageRotate, (200, 200))

boatHull = boatHull_orig
boatHull_rect = boatHull.get_rect(center = (500, SCREEN_HEIGHT/2-100))
#Main Loop
run = True
while run:
    screen.fill(white)
    
    
    
    #Timestamp counter
    text = my_font.render(str(timestamp), True, black)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2+15, 15))
    screen.blit(text, text_rect)
    
    #Move through timestamps
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and timestamp < len(data) and inputTimer == 0:
        timestamp_forward(data, timestamp, boatHull)
        timestamp += 1
        boatHull = pygame.transform.rotate(boatHull_orig, -10)
        boatHull_rect = boatHull.get_rect(center = (500, SCREEN_HEIGHT/2-100))
        inputTimer += inputDelay
    elif keys[pygame.K_LEFT] and timestamp > 0 and inputTimer == 0:
        timestamp_backward(data, timestamp, boatHull)
        timestamp -= 1
        boatHull = pygame.transform.rotate(boatHull_orig, 10)
        boatHull_rect = boatHull.get_rect(center = (500, SCREEN_HEIGHT/2-100))
        inputTimer += inputDelay

    pygame.draw.rect(screen, black, middleLine)
    screen.blit(boatHull, boatHull_rect)
    screen.blit(boatSail, (500, SCREEN_HEIGHT/2-100))
    screen.blit(boatRudder, (500, SCREEN_HEIGHT/2-100))
        
    if inputTimer > 0:
        inputTimer -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
    
pygame.quit()
