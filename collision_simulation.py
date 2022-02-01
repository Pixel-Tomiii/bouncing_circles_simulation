import pygame
import time
import math
import random

CIRCLE_COLOR = (255, 0, 0)
BG_COLOR = (0, 0, 0)
FPS = 60
RADIUS = 40
MIN_SPEED = 4
MAX_SPEED = 30
MAX_CIRCLES = 200
RESISTANCE = 0.85


def to_velocity(angle, speed):
    """Convert an angle in radians to a velocity vector""" 
    x = math.cos(angle) * speed
    y = math.sin(angle) * speed
    return x, y


def get_difference(vect1, vect2):
    """Gets the difference between two vectors"""
    x_diff = vect1[0] - vect2[0]
    y_diff = vect1[1] - vect2[1]
    return (x_diff, y_diff)


def add_vector(vect1, vect2):
    """Adds two vectors together"""
    return (vect1[0] + vect2[0], vect1[1] + vect2[1])


class Circle():
    def __init__(self, position):
        self.position = position
        self.speed = random.randint(MIN_SPEED, MAX_SPEED)
        self.velocity = to_velocity(math.pi * (random.random() + random.random()), self.speed)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
##        self.color = (255, 255, 255)
        
    def get_center(self):
        """Returns a tuple representing the coordinates of the centre of
        the circle."""
        return (self.position[0] + RADIUS, self.position[1] + RADIUS)

    def flip_x(self):
        """Flips the x velocity of the circle"""
        self.velocity = (self.velocity[0] * -1, self.velocity[1])

    def flip_y(self):
        """Flips the y velocity of the circle"""
        self.velocity = (self.velocity[0], self.velocity[1] * -1)

    def slow(self):
        """Reduces the magnitude of the velocity of the circle based on
        the resistance modifier."""
        mag = math.sqrt((self.velocity[0]**2) + (self.velocity[1]**2)) * RESISTANCE
        angle = math.atan2(self.velocity[1], self.velocity[0])
        self.velocity = to_velocity(angle, mag)

    
# Initialise screen.
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

width = screen.get_width()
height = screen.get_height()

# Update control.
running = True
paused = True
next_frame = time.time()
interval = 1 / FPS

circles = [Circle((random.randint(0, width-1-(RADIUS*2)), random.randint(0, height-1-(RADIUS*2)))) for _ in range(MAX_CIRCLES)]



# Update loop.
while running:

    # Event handling.
    for event in pygame.event.get():
        # Quit event.
        if event.type == pygame.QUIT:
            running = False
            break

        # Quit on escape pressed.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

            if event.key == pygame.K_SPACE:
                paused = not paused
    
    # Check for a frame update.
    current = time.time()
    if current < next_frame:
        continue
    
    next_frame += interval
    
    screen.fill(BG_COLOR)
    
    # Render all the circles.
    for circle in circles:
        pygame.draw.circle(screen, circle.color, circle.get_center(), RADIUS)

    pygame.display.update()

    # Skip updating if paused.
    if paused:
        continue

    # Update the position of all the circles.
    for circle in circles:
        v_x, v_y = circle.velocity
        p_x, p_y = circle.position

        # Check bounds.
        if 0 <= p_x + v_x <= width - 1 - RADIUS*2:
            p_x += v_x
        # Bound off side.
        else:
            circle.flip_x()
            circle.slow()       # Slow down after hitting a wall.
            if p_x + v_x < 0:
                p_x = -v_x - p_x
            else:
                p_x = width - 1 - v_x - (width - p_x - 1)
            
        if 0 <= p_y + v_y <= height - 1 - RADIUS*2:
            p_y += v_y
        # Bound off top/bottom.
        else:
            circle.flip_y()
            circle.slow()       # Slow down after hitting a wall.
            if p_y + v_y < 0:
                p_y = -v_y - p_y
            else:
                p_y = width - 1 - v_y - (width - p_y - 1)

        circle.position = (p_x, p_y)
##        circle.slow()
    

pygame.quit()
        
