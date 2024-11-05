import pygame
import os

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

# dEfine game variables
GRAVITY = 0.75

# Define player action variables
moving_left = False
moving_right = False

# Define colors
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


class Soldier(pygame.sprite.Sprite): # Class Soldier inherits from pygame.sprite.Sprite. Soldier gains all the functionality of the Sprite class 
    def __init__(self, char_type, x, y, scale, speed): # Constructor method.
        pygame.sprite.Sprite.__init__(self) # Inherits sprite. self: A reference to the current(particular) instance of the class.
        self.alive = True
        self.char_type = char_type #    Player/Enemy
        self.speed = speed
        self.vel_y = 0 # y velocity for jump
        self.jump = False
        self.in_air = True
        self.direction = 1 # Moving left(1)  or right(-1)
        self.flip = False # Flip player
        self.animation_list = [] # List of animations; idle, jump..
        self.frame_index = 0 # Index
        self.action = 0 # Index used to loop thru animation_list 
        self.update_time = pygame.time.get_ticks() # Timestamp when instance is created

        # Load all images for the players
        animation_types = ['Idle', 'Run', 'Jump']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = [] # Empty list
            # count no of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames): 
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png') # Loads character image one by one
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) # Scales image
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
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

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # Update animation
        ANIMATION_COOLDOWN = 100
        # Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks() # Resets timer
            self.frame_index += 1 # Moves to next index - (image)
        # If animation has run out, then reset back to start
        if self.frame_index  >= len(self.animation_list[self.action]):
            self.frame_index = 0


    def update_action(self, new_action):   # Update action. Action represent change in animation state
        # check if new action is diff frm prev action
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks() # reset cooldown time



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

    player.update_animation()
    player.draw()
    enemy.draw()
 
    # update player actions
    if player.alive:
        if player.in_air:
            player.update_action(2) # 2: JUMP
        elif moving_left or moving_right:
            player.update_action(1) # 1: RUN
        else:
            player.update_action(0) # 0: IDLE
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
            if event.key == pygame.K_w and player.alive:
                player.jump = True
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