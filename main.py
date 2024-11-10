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
shoot = False
grenade = False
grenade_thrown = False

# Load images
# bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
#grenade
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()

# Define colors
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


class Soldier(pygame.sprite.Sprite): # Class Soldier inherits from pygame.sprite.Sprite. Soldier gains all the functionality of the Sprite class 
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades): # Constructor method.
        pygame.sprite.Sprite.__init__(self) # Inherits sprite. self: A reference to the current(particular) instance of the class.
        # Variables
        self.alive = True
        self.char_type = char_type #    Player/Enemy
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0 # limit firing quickly
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.vel_y = 0 # y velocity for jump
        self.jump = False
        self.in_air = True
        self.direction = 1 # Moving left(-1)  or right(1)
        self.flip = False # Flip player
        self.animation_list = [] # List of animations; idle, jump..
        self.frame_index = 0 # Index
        self.action = 0 # Index used to loop thru animation_list 
        self.update_time = pygame.time.get_ticks() # Timestamp when instance is created

        # Load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = [] # Empty list
            # count no of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames): 
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha() # Loads character image one by one
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) # Scales image
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect() # it gives you a Rect object with the same width and height as the surface.
        self.rect.center = (x, y) # Centers it

    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


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

    def shoot(self):
        if self.shoot_cooldown == 0  and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction) #center bullet by adding player width * 0.6
            bullet_group.add(bullet) # Add bullet to bullet_group
            # reduce ammo
            self.ammo -= 1

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
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0


    def update_action(self, new_action):   # Update action. Action represent change in animation state
        # check if new action is diff frm prev action
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks() # reset cooldown time


    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)



    def draw(self): # Creates a method that draws the image (img) at the location (rect)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 25
                self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100 # fuse timer
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):          # grenade trajectory
        self.vel_y += GRAVITY
        dx = self.direction * self.speed   #change in x coordinate of the grenade = speed*direction
        dy = self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

        #check collision with walls
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1 # flip grenade direction
            dx = self.direction * self.speed

        # upgrade grenade position
        self.rect.x += dx
        self.rect.y += dy
            

# Create sprite groups
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
        


# Player coordinates
player = Soldier('player', 200, 200, 3, 5, 20, 5) # Creates instance named player
enemy = Soldier('enemy', 400, 200, 3, 5, 20, 0) # Creates instance named player



# Main game loop
run = True
while run:

    clock.tick(FPS) # Controls framerate & ensures game runs at a consistent speed

    draw_bg()

    player.update()
    player.draw()

    enemy.update()
    enemy.draw()

    #update and draw groups
    bullet_group.update()
    grenade_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)
 
    # update player actions
    if player.alive:
        #shoots bullets
        if shoot:
            player.shoot()
        # throw grenade
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
            player.rect.top, player.direction)
            grenade_group.add(grenade)
            # reduce grenades
            player.grenades -= 1
            grenade_thrown = True
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
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:  
                grenade = True # Trigger grenade throw
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
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

    pygame.display.update() # Recent changes are updated

# Quit pygame
pygame.quit()