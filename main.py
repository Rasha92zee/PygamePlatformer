import pygame
#from pygame.sprite import _Group

# Initialize pygame
pygame.init()

# Set up the display 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Game window
pygame.display.set_caption("Shooter") # Title

class Soldier(pygame.sprite.Sprite): # Class Soldier inherits from pygame.sprite.Sprite. Soldier gains all the functionality of the Sprite class 
    def __init__(self, x, y, scale): # Constructor method.
        pygame.sprite.Sprite.__init__(self) # Inherits sprite. self: A reference to the current(particular) instance of the class.
        img = pygame.image.load('img/player/Idle/0.png') # Loads player image
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) # Scales image
        self.rect = self.image.get_rect() # it gives you a Rect object with the same width and height as the surface.
        self.rect.center = (x, y) # Centers it

    def draw(self): # Creates a method that draws the image (img) at the location (rect)
        screen.blit(self.image, self.rect) 


# Player coordinates
player = Soldier(200, 200, 3) # Creates instance named player
player2 = Soldier(400, 200, 3) 



# Main game loop
run = True
while run:


    player.draw()
    player2.draw()

    # Event Handler
    for event in pygame.event.get():  # Listening for an event to quit game
        if event.type == pygame.QUIT: # Keyboard clicks
            run = False

    pygame.display.update() # Recent changes are updated

# Quit pygame
pygame.quit()