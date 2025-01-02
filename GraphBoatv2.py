import pandas as pd
import pygame
import os
import math

#Parameters
file_name = r'C:\Users\rage3\OneDrive\Documents\BoatGraphProgram\sailboat_data.txt'
data_file_path = r'C:\Users\rage3\OneDrive\Documents\BoatGraphProgram\sailboat_data.txt'
img_dir = r'C:\Users\rage3\OneDrive\Documents\BoatGraphProgram'
inputDelay = 50
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
windDialPos = (SCREEN_WIDTH/2+120, 120)
rudderDist = 80
CSVskiprows = 5

#Constants
inputTimer = 0
timestamp = 0

#Defining Colors
white = [255, 255, 255]
black = [0, 0, 0]
brown = [100, 42, 42]

#FUNCTIONS:
#Load csv
def load_csv(file_name):
    df = pd.read_csv(file_name, skiprows = CSVskiprows)
    return df

#Timestamp forward
def timestamp_update(data, timestamp):
    hullCenter = (SCREEN_WIDTH*3/4, SCREEN_HEIGHT/2)
    hullRotation = -data.iloc[timestamp, 6]
    boatHull = pygame.transform.rotate(boatHull_orig, hullRotation)
    boatHull_rect = boatHull.get_rect(center = hullCenter)
    boatSail = pygame.transform.rotate(boatSail_orig, -data.iloc[timestamp, 8])
    boatSail_rect = boatSail.get_rect(center = (SCREEN_WIDTH*3/4, SCREEN_HEIGHT/2))
    windArrow = pygame.transform.rotate(windArrow_orig, -data.iloc[timestamp, 7])
    windArrow_rect = windArrow.get_rect(center = hullCenter)
    wpDirectionArrow = pygame.transform.rotate(wpDirectionArrow_orig, -data.iloc[timestamp, 11])
    wpDirectionArrow_rect = wpDirectionArrow.get_rect(center = (SCREEN_WIDTH*3/4, SCREEN_HEIGHT/2))    
    
    directionVector = (rudderDist,  math.radians(data.iloc[timestamp, 6]+90))
    rudderCenterX = int(hullCenter[0] + directionVector[0] * math.cos(directionVector[1]))
    rudderCenterY = int(hullCenter[1] + directionVector[0] * math.sin(directionVector[1]))
    rudderCenter = (rudderCenterX, rudderCenterY)
    rudderRotation = hullRotation + (data.iloc[timestamp, 10] - 180)
    boatRudder = pygame.transform.rotate(boatRudder_orig, rudderRotation)
    boatRudder_rect = boatRudder.get_rect(center = rudderCenter)
    return boatHull, boatHull_rect, boatSail, boatSail_rect, boatRudder, boatRudder_rect, windArrow, windArrow_rect, wpDirectionArrow, wpDirectionArrow_rect
    
    
#Timestamp backward
def timestamp_backward(data, timestamp):
    boatHull = pygame.transform.rotate(boatHull_orig, data.iloc[timestamp, 6])
    boatHull_rect = boatHull.get_rect(center = (500, SCREEN_HEIGHT/2-100))
    return boatHull, boatHull_rect

#Load csv
data = load_csv(data_file_path)

#Pygame window initialization
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Alef', 30)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Fancy Boat Display")

#Objects
middleLine = pygame.Rect(SCREEN_WIDTH/2, 0, 1, 600)

global boatHull
global boatSail
global boatRudder

boatHull_orig = pygame.transform.smoothscale(
    pygame.transform.rotate(
        pygame.image.load(os.path.join(img_dir, 'boatScaled.png')),
        0),
    (200, 200))

boatSail_orig = pygame.transform.smoothscale(
    pygame.transform.rotate(
        pygame.image.load(os.path.join(img_dir, 'sailScaled.png')),
        90),
    (200, 200))

boatRudder_orig = pygame.transform.smoothscale(
    pygame.transform.rotate(
        pygame.image.load(os.path.join(img_dir, 'rudder2Scaled.png')),
        0),
    (200, 200))

windDial_orig = pygame.transform.smoothscale(
    pygame.transform.rotate(
        pygame.image.load(os.path.join(img_dir, 'windDial.png')),
        0),
    (200, 200))

windArrow_orig = pygame.transform.smoothscale(
    pygame.transform.rotate(
        pygame.image.load(os.path.join(img_dir, 'windArrow2.png')),
        0),
    (400, 400))

wpDirectionArrow_orig = pygame.transform.smoothscale(
    pygame.transform.rotate(
        pygame.image.load(os.path.join(img_dir, 'WPDirectionArrow.png')),
        0),
    (400, 400))

boatHull, boatHull_rect, boatSail, boatSail_rect, boatRudder, boatRudder_rect, windArrow, windArrow_rect, wpDirectionArrow, wpDirectionArrow_rect = timestamp_update(data, timestamp)
windDial_rect = windArrow.get_rect(center = windDialPos)

#Main Loop
run = True
while run:
    screen.fill(white)
    
    #Draw objects:
    text = my_font.render('Timestamp:' + str(timestamp), True, black)
    text_rect = text.get_rect(center=(SCREEN_WIDTH*3/4, 15))
    screen.blit(text, text_rect)
    
    text = my_font.render('Boat angle:' + str(data.iloc[timestamp, 6]), True, black)
    text_rect = text.get_rect(center=(SCREEN_WIDTH*3/4, 50))
    screen.blit(text, text_rect)

    text = my_font.render('Sail angle:' + str(data.iloc[timestamp, 8]), True, black)
    text_rect = text.get_rect(center=(SCREEN_WIDTH*3/4, 85))
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, black, middleLine)
    screen.blit(wpDirectionArrow, wpDirectionArrow_rect)
    screen.blit(windArrow, windArrow_rect)
    screen.blit(boatHull, boatHull_rect)
    screen.blit(boatSail, boatSail_rect)
    screen.blit(boatRudder, boatRudder_rect)
    #screen.blit(windDial_orig, windDial_rect)
    
    #Move through timestamps
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and timestamp < len(data)-1 and inputTimer == 0:
        timestamp += 1
        boatHull, boatHull_rect, boatSail, boatSail_rect, boatRudder, boatRudder_rect, windArrow, windArrow_rect, wpDirectionArrow, wpDirectionArrow_rect = timestamp_update(data, timestamp)
        inputTimer += inputDelay
    elif keys[pygame.K_LEFT] and timestamp > 0 and inputTimer == 0:
        timestamp -= 1
        boatHull, boatHull_rect, boatSail, boatSail_rect, boatRudder, boatRudder_rect, windArrow, windArrow_rect, wpDirectionArrow, wpDirectionArrow_rect = timestamp_update(data, timestamp)
        inputTimer += inputDelay
        
    if inputTimer > 0: #Decrease input delay timer
        inputTimer -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
    
pygame.quit()
