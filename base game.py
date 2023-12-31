import pygame
import os
import random
from pygame import mixer
import time
main_time=time.time()

def health_bar(surf, x, y, pct):
    '''Draw a health bar for the player'''
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (255, 0, 0), fill_rect)

def stamina_bar(surf, x, y, stamina):
    '''Draw a stamina bar for the player'''
    if stamina < 0:
        stamina = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (stamina / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0, 255, 0), fill_rect)

def resize_image(image):
    width = image.get_width() * 2
    height = image.get_height() * 2
    resized_image = pygame.transform.scale(image, (width, height))
    return resized_image

def unpack_assprite_files(path):
    images = []
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            image = resize_image(pygame.image.load(os.path.join(path, filename)))
            images.append(image)
    return images

run_frames = unpack_assprite_files(path="ASSEST\Run")
# for i in range(5):
#     run_frames=run_frames+run_frames

walk_frames =  unpack_assprite_files(path="ASSEST\Run") 
shoot_frames = unpack_assprite_files(path="ASSEST\ATTACK") 
idle_frame =  resize_image(pygame.image.load(r"ASSEST\PNGExports\PNGExports\Idle.png"))

class Player():
    def __init__(self, pos, run_frames, walk_frames, shoot_frames, idle_frame):
        super(Player, self).__init__()
        self.image = idle_frame
        self.rect = self.image.get_rect(topleft=pos)

        self.run_frames = run_frames
        self.walk_frames = walk_frames
        self.shoot_frames = shoot_frames
        self.idle_frame = idle_frame

        self.current_frame = 0
        self.current_frame_shoot = 0

        self.animation_speed = 10
        self.animation_delay = 0

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5

        self.is_shooting = False
        self.flipped = False
        self.health=100
        self.ismoving=True
        self.stamina=100
        self.canmove=True

    def update(self):
        if self.canmove:self.is_shooting==True
        player.handle_input()
        self.animate()
        self.move()
        self.ismoving=False
        self.check_stamina()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.ismoving=True
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.ismoving=True


        else:
            self.direction.y = 0

            

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.flipped = True
            self.ismoving=True

        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.flipped = False
            self.ismoving=True
                        
        else:
            self.direction.x = 0

        self.is_shooting = pygame.mouse.get_pressed()[0]
        if self.is_shooting == False:
            self.handle_mouse_release()
            self.speed=5
        else:
            self.speed=0
        
    def flip_image(self, image):
        return pygame.transform.flip(image, True, False)

    def animate(self):
        self.animation_delay += 1
        #print(self.direction.magnitude())

        if self.ismoving:
            # Handle shooting animation
            if self.current_frame < len(self.walk_frames):
                self.image = self.flip_image(self.walk_frames[self.current_frame]) if self.flipped else self.walk_frames[self.current_frame]
                self.current_frame =self.current_frame +1 
            else:
                self.current_frame=0
            # else:
            #     self.is_shooting = False
            #     self.current_frame = 0
        elif self.is_shooting and self.stamina >0:
        #     # Handle shooting animation
             if self.current_frame_shoot < len(self.shoot_frames):
                 self.image = self.flip_image(self.shoot_frames[self.current_frame_shoot]) if self.flipped else self.shoot_frames[self.current_frame_shoot]
                 self.current_frame_shoot += 1
             else:
                self.is_shooting = False
                self.current_frame_shootw = 0

        # elif self.ismoving=False:
        #     # Handle movement animation
        #         if self.current_frame < len(self.walk_frames):
        #             self.image = self.flip_image(self.walk_frames[self.current_frame]) if self.flipped else self.walk_frames[self.current_frame]
        #             self.current_frame += 1
        #         else:
        #             self.ismoving = False
        #             self.current_frame = 0
                
                # Update frame and reset delay when threshold reached
                # if self.animation_delay >= self.animation_speed:
                #     self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                #     self.image = self.flip_image(self.run_frames[self.current_frame]) if self.flipped else self.run_frames[self.current_frame]
                #     self.animation_delay = 0  # Reset the delay
        else:
                 # Set idle frame and reset delay for smooth transition
                 self.image = self.idle_frame
                 self.animation_delay = 0  # Reset the delay

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        #self.direction.x

    def handle_mouse_release(self):
        self.is_shooting = False
        self.current_frame_shoot = 0
        
    
    def check_damage(self,is_damaged):
        if is_damaged:
            self.health=self.health-20
        if self.health<=0:
              print("you are dead")
              pygame.quit()
              quit()
              
              
    def check_stamina(self):
        if player.is_shooting==True:
            
            self.stamina=self.stamina -1     
        
        if self.stamina <=0:
            self.canmove=False
        else:
            self.canmove= True

        

# ...

# Sample usage
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()



background = pygame.image.load(r"_53d0c924-3d11-4b95-89bb-584fa270efd5.png")
# Load player animation frames
##resize background
background = pygame.transform.scale(background, (800, 600))

player = Player((100, 100), run_frames, walk_frames, shoot_frames, idle_frame)


class Zombie():
    def __init__(self, pos, run_frames, dead_frame):
        super(Zombie, self).__init__()
        self.image = run_frames[0]
        self.rect = self.image.get_rect(center=pos)

        self.run_frames = run_frames
        self.dead_frames = dead_frame

        self.current_frame = 0
        self.animation_speed = 5
        self.animation_delay = 0

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1

        self.is_dead = False
        self.flipped = False  # Added: Initial flipped state

    def flip_image(self, image):
        return pygame.transform.flip(image, True, False)

    def update(self, player_pos):
        self.move_towards_player(player_pos)
        self.animate()

    def move_towards_player(self, player_pos):
        # Convert player position to a vector
        player_vector = pygame.math.Vector2(*player_pos)
        # Calculate direction vector
        try:
            self.direction = (player_vector - self.rect.center).normalize()
        except:
            pass
        # Update position based on direction and speed
        self.rect.center += self.direction * self.speed
        distance = (player_vector - self.rect.center).magnitude()

        if distance > 0.1:
            self.direction = (player_vector - self.rect.center).normalize()
            self.flipped = self.direction.x < 0



    # def animate(self):
    #     self.animation_delay += 1

    #     if self.is_dead:
    #         # Play dead animation sequence
    #         if self.current_frame < len(self.dead_frames):
    #             self.image = self.dead_frames[self.current_frame]
    #             self.current_frame += 1
    #         else:
    #             # Show last frame of dead animation indefinitely
    #             self.image = self.dead_frames[-1]
    #     else:
    #         # Play run animation as usual
    #         if self.animation_delay >= self.animation_speed:
    #             self.current_frame = (self.current_frame + 1) % len(self.run_frames)
    #             self.image = self.run_frames[self.current_frame]
    #             self.animation_delay = 0
    def animate(self):
        self.animation_delay += 1

        if self.is_dead:
            # Play dead animation sequence
            if self.current_frame < len(self.dead_frames):
                self.image = self.flip_image(self.dead_frames[self.current_frame]) if self.flipped else self.dead_frames[self.current_frame]
                self.current_frame += 1
            else:
                # Show last frame of dead animation indefinitely
                self.image = self.flip_image(self.dead_frames[-1]) if self.flipped else self.dead_frames[-1]
        else:
            # Play run animation with flipping
            if self.animation_delay >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                self.image = self.flip_image(self.run_frames[self.current_frame]) if self.flipped else self.run_frames[self.current_frame]
                self.animation_delay = 0


    def check_death(self, player_pos,is_shooting):
        # Convert player position to a vector
        player_vector = pygame.math.Vector2(*player_pos)
        # Calculate distance
        distance = (player_vector - self.rect.center).magnitude()
        if not self.is_dead and distance < 30 and is_shooting:
            self.is_dead = True
            
    def check_damage(self, player_pos):
        # Convert player position to a vector
        player_vector = pygame.math.Vector2(*player_pos)
        # Calculate distance
        distance = (player_vector - self.rect.center).magnitude()
        if not self.is_dead and distance < 20:
            self.is_dead = True
            return True
            



screen_width, screen_height = screen.get_size()
dead_frame=unpack_assprite_files(path=r"ASSEST\64x64 Pixel Art Character and zombie by RgsDev\Zombie\Dead")
run_frames_zombie=unpack_assprite_files(path=r"ASSEST\64x64 Pixel Art Character and zombie by RgsDev\Zombie\Walk")
zombies = []

for i in range(10):
    dead_frame=dead_frame+dead_frame

for _ in range(10):
    pos = random.randint(0, screen_width), random.randint(0, screen_height)
    zombie = Zombie(pos, run_frames_zombie, dead_frame)
    zombies.append(zombie)


dead_zombies=[]
running = True


dont_Add=False

shootingg_time = -100
while running:
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for pos in dead_zombies:
        screen.blit(dead_frame[-1], pos)
    if len(dead_zombies)>50:
        dead_zombies=dead_zombies[25:50]
    
    
    for zombie in zombies:
        zombie.update(player.rect.center)
        zombie.check_death(player.rect.center,player.is_shooting)
        player.check_damage((player.rect.center))
#zombie.check_damage
        screen.blit(zombie.image, zombie.rect)

    # ...
    
    # Check for dead zombies and spawn new ones
    for i, zombie in enumerate(zombies):
        if zombie.is_dead:
            dead_zombies.append(zombie.rect.center)

            del zombies[i]
            #zombies.append(zombie)
            break
    
    
    if round(main_time-time.time()) %2==0 and dont_Add==False  :
        for i in range(3):
            pos = random.randint(0, screen_width), random.randint(0, screen_height)

            zombie = Zombie(pos, run_frames_zombie, dead_frame)
            zombies.append(zombie)


        dont_Add=True
    if round(main_time-time.time()) %2==1:
        dont_Add=False
    

    # Draw dead zombies
    
    if player.is_shooting== True  and player.stamina >0 : 
        shootingg_time= time.time()
          
    passed_time=round(time.time()-shootingg_time)
    
    if passed_time ==4 :
        #print('pasased')
        player.stamina= 100
        shooting_time=-100
        passed_time=0
                    
    #print(player.is_shooting,passed_time,shootingg_time)
    #dprint(player.stamina , player.is_shooting)
    player.update()
    if player.stamina  <5:
        player.is_shooting=False
        
    print(player.rect.center)
    
    health_bar(screen, 10, 10, player.health)
    stamina_bar(screen, 300, 10, player.stamina)
    #print(player.health)
    screen.blit(player.image, player.rect)

    pygame.display.flip()
    clock.tick(30)
