import pygame
#from pygame.sprite import _Group

# Initialize pygame
pygame.init()

# Set up the display 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Game window
pygame.display.set_caption("Shooter") # Title

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define player action variables
moving_left = False
moving_right = False

# Define colors
BG = (144, 201, 120)

def draw_bg():
    screen.fill(BG)


class Soldier(pygame.sprite.Sprite): # Class Soldier inherits from pygame.sprite.Sprite. Soldier gains all the functionality of the Sprite class 
    def __init__(self, char_type, x, y, scale, speed): # Constructor method.
        pygame.sprite.Sprite.__init__(self) # Inherits sprite. self: A reference to the current(particular) instance of the class.
        self.char_type = char_type #    Player/Enemy
        self.speed = speed
        self.direction = 1 # Moving left(1)  or right(-1)
        self.flip = False # Flip player

        img = pygame.image.load(f'img/{self.char_type}/Idle/0.png') # Loads player image
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) # Scales image
        self.rect = self.image.get_rect() # it gives you a Rect object with the same width and height as the surface.
        self.rect.center = (x, y) # Centers it


    def move(self, moving_left, moving_right):

        # Reset movement variables (for the rect)
        dx = 0
        dy = 0

        # Assign movement variable if moving left or right
        if moving_left: # If its true..
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self): # Creates a method that draws the image (img) at the location (rect)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) 


# Player coordinates
player = Soldier('player', 200, 200, 3, 5) # Creates instance named player
enemy = Soldier('enemy', 400, 200, 3, 5) # Creates instance named player



# Main game loop
run = True
while run:

    clock.tick(FPS) # Controls framerate & ensures game runs at a consistent speed

    draw_bg()

    player.draw()
    enemy.draw()

    player.move(moving_left, moving_right)

    # Event Handler
    for event in pygame.event.get():  # Listening for an event to quit game
        # Quit Game
        if event.type == pygame.QUIT: 
            run = False
        # Keyboard clicks
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE: # escape to quit game
                run = False
        
        # Keyboard button releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update() # Recent changes are updated

# Quit pygame
pygame.quit()