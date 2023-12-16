from typing import Any, SupportsFloat
import gymnasium as gym
import numpy as np
import pygame
pygame.init()


pygame.font.init()

# Rest of your code...



import time
import os

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
walk_frames =  unpack_assprite_files(path="ASSEST\Run") 
shoot_frames = unpack_assprite_files(path="ASSEST\ATTACK") 
idle_frame =  resize_image(pygame.image.load(r"ASSEST\PNGExports\PNGExports\Idle.png"))






class Player(pygame.sprite.Sprite):
    def __init__(self, pos, walk_frames=walk_frames, shoot_frames=shoot_frames, idle_frame=idle_frame):
        super(Player, self).__init__()

        self.image = idle_frame
        self.rect = self.image.get_rect(topleft=pos)

        #self.run_frames = run_frames
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
        self.ISDEAD=False

    def update(self,action):
        if self.canmove:self.is_shooting==True
        self.check_stamina()

        self.handle_input(action)
        self.animate()
        self.move()
        self.ismoving=False

    def handle_input(self,action):

        if action==0: #W
            self.direction.y = -1
            self.ismoving=True
        elif action == 1: #s
            self.direction.y = 1
            self.ismoving=True
        else:
            self.direction.y = 0

        if action ==2: #a
            self.direction.x = -1
            self.flipped = True
            self.ismoving=True

        elif action ==3: # D
            self.direction.x = 1
            self.flipped = False
            self.ismoving=True
                        
        else:
            self.direction.x = 0

        self.is_shooting = True  if action==4 and self.canmove==True else False
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
            self.health=self.health-50
        if self.health<=0:
            self.ISDEAD=True     
            
        """ DO THIS OUTSIDE THE CODE, SINCE THE MAIN GAME WILL NOT USE PYGAME WHILE TRAINING, ONLY ON RENDER""" 
            
            #   print("you are dead")
            #   pygame.quit()
            #   quit()
              
              
    def check_stamina(self):
        if self.is_shooting==True:
            
            self.stamina=self.stamina -10     
        
        if self.stamina <=0:
            self.canmove=False
            self.is_shooting=False
        else:
            self.canmove= True


dead_frame=unpack_assprite_files(path=r"ASSEST\64x64 Pixel Art Character and zombie by RgsDev\Zombie\Dead")
run_frames_zombie=unpack_assprite_files(path=r"ASSEST\64x64 Pixel Art Character and zombie by RgsDev\Zombie\Walk")


class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos, run_frames=run_frames_zombie, dead_frame=dead_frame):
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
        self.dead_frame=dead_frame
        self.run_frames_zombie=run_frames_zombie



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
            


def set_fps( observation,Reward,terminated,truncated,info,fps=60 ):
    """ the following code will be used in the step method and will return the obs and etc after a fixed time """
    times=time.time()
    while True:
        if time.time()  > times+ 1/fps:
            return observation,Reward,terminated,truncated,info
            
    



            
class ZombieEnv(gym.Env):
    metadata = {
        'render_modes': ['human', 'rgb_array'],
        'render_fps': 60
    }
    
    def __init__(self,render_mode=None) :

        self.size=(800,800)
        self.run_frames = unpack_assprite_files(path="ASSEST\Run")
        
        #pygame
        self.success=False
        self.dead_last_time=False




        self.walk_frames =  unpack_assprite_files(path="ASSEST\Run") 
        self.shoot_frames = unpack_assprite_files(path="ASSEST\ATTACK") 
        self.idle_frame =  resize_image(pygame.image.load(r"ASSEST\PNGExports\PNGExports\Idle.png"))
        
        self.background=pygame.image.load(r"_53d0c924-3d11-4b95-89bb-584fa270efd5.png")
        
        self.action_space=gym.spaces.Discrete(5)
        #pygame.init()

   

        self.reward_last=0
        
        assert render_mode is None or render_mode in self.metadata['render_modes']
        self.render_mode = render_mode
        
   
        num_zombies = 7
        self.observation_space = gym.spaces.Dict({
            "player": gym.spaces.Box(low=np.array([0, 0]), high=np.array([800, 800]), dtype=np.int32),
            "zombies": gym.spaces.Box(low=np.zeros(num_zombies * 2), high=np.full(num_zombies * 2, 800), dtype=np.int32)
        })


    
    def _get_obs(self):
        zombie_positions = np.array([zombie.rect.center for zombie in self.zombies]).flatten()
        return {
            "player": np.array(self.player.rect.center),
            "zombies": zombie_positions
        }
        
        
            
    def reset(self,seed=None,options=None):
     
        self.player=Player(pos=(100, 100))
        info={'health':self.player.health}
        self.zombies=[]
        pos = np.random.random_integers(0, 800), np.random.random_integers(0, 800)
        self.zombie1=Zombie(pos=pos)
        pos = np.random.random_integers(0, 800), np.random.random_integers(0, 800)
        self.zombie2=Zombie(pos=pos)
        pos = np.random.random_integers(0, 800), np.random.random_integers(0, 800)
        self.zombie3=Zombie(pos=pos)
        pos = np.random.random_integers(0, 800), np.random.random_integers(0, 800)
        self.zombie4=Zombie(pos=pos)
        pos = np.random.random_integers(0, 800), np.random.random_integers(0, 800)
        self.zombie5=Zombie(pos=pos)
        pos = np.random.random_integers(0, 800), np.random.random_integers(0, 800)
        self.zombie6=Zombie(pos=pos)
        pos = np.random.random_integers(0, 800), np.random.random_integers(0, 800)
        self.zombie7=Zombie(pos=pos)
        
        self.zombies.append(self.zombie1)
        self.zombies.append(self.zombie2)
        self.zombies.append(self.zombie3)
        self.zombies.append(self.zombie4)
        self.zombies.append(self.zombie5)
        self.zombies.append(self.zombie6)
        self.zombies.append(self.zombie7)
        self.reward=0

        self.screen = pygame.display.set_mode((800, 600),pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        
        self.done=False
        self.dead_zombies=[]
        
     
        
        
        
        return self._get_obs() ,{}
    
    def step(self,action):
        self.player.update(action)
        
        for zombie in self.zombies:
            zombie.update(self.player.rect.center)
            zombie.check_death(self.player.rect.center,self.player.is_shooting)
            #self.player.check_damage(zombie.rect.center)
            self.player.check_damage(zombie.check_damage(self.player.rect.center))
            if zombie.is_dead and zombie  not in self.dead_zombies:
                self.dead_zombies.append(zombie)
                
                self.reward+=2
                
        if self.player.ISDEAD:
            self.reward=self.reward-10
            self.dead_last_time=True
            self.success=False
                
        observation=self._get_obs()
        #print(self.reward)
        if self.reward >13:
            self.success=True
            self.dead_last_time=False
        
        if self.player.ISDEAD or self.reward>13 :
            self.done=True
            #pygame.display.quit()
        
        # or len(self.zombies)==0
        terminated=self.done
        
        
        """test"""
        #terminated =False
        
        
        info={'health':self.player.health}
        truncated=False
        # pygame.time.Clock().tick(60)
        fps=60 #if self.render_mode=='human' else 700

        #if self.render_mode:
            
        
        
        #print(self.player.health)
        self.render_dick()
            
        
        #print('fuck')
        self.reward_last=self.reward
        return observation,self.reward,terminated,truncated,{}
     
    
    # 
        #return self._get_obs(),self.player.health,self.player.ISDEAD,{}
    # # def render(self, mode='human'):4
    
    # def render(self ):
    #     if self.render_mode == 'human':
    #        # pygame.display.init()
    #         screen = pygame.display.set_mode((800, 600))

    #         #self.clock = pygame.time.Clock()
    #         screen.fill((255, 255, 255))
    #         #self.clock.tick(60)
            
    #         # Render player
    #         # self.player.render(self.screen)
            
    #         # # Render zombies
    #         # for zombie in self.zombies:
    #         #     zombie.render(self.screen)
            
    #         pygame.display.flip()
    #     elif self.render_mode == 'rgb_array':
    #         # Implement rendering to RGB array here
    #         pass
    #     else:
    #         raise ValueError("Invalid render mode. Supported modes are 'human' and 'rgb_array'.")
    def render(self):pass
        #if self.render_mode=="human":
        #@self.window.event
        #def on_draw():
            # Clear the window with a green color
    #     pyglet.gl.glClearColor(0, 1, 0, 1)
    #     self.window.clear()

    #     # player_sprite = pyglet.sprite.Sprite(self.player.image, x=self.player.rect.center[0], y=self.player.rect.center[1])
    #     # player_sprite.draw()
    #     # def update(dt):
    #     #     player_sprite.set_position(self.player.rect.center[0], self.player.rect.center[1])

    # # Schedule the update function to be called every 1/60th of a second
    #     #pyglet.clock.schedule_interval(on_draw, 1/60.0)


    #     # Process all the events currently in the queue
    #     pyglet.app.run()

        # Redraw the window
        # self.window.flip()
    def render_dick(self):
        
        for event in pygame.event.get():
            pass
        
        
        
        self.screen.fill((0,0,0))
        #self.screen.blit(self.background,(0,0))
        
        
        self.screen.blit(self.player.image,self.player.rect)
        for zombies in self.zombies:
            self.screen.blit(zombies.image,zombies.rect)
            # if zombies.is_dead:
            #     self.zombies.remove(zombies)
        
            
        if self.dead_last_time:
            font = pygame.font.Font(None, 36)
            text = font.render(f"You died last time  {self.reward_last}" , True, (255, 0, 0))
            self.screen.blit(text, (700, 10))
        
        if self.success:
            font = pygame.font.Font(None, 36)
            text = font.render(f"Success! {self.reward_last}", True, (0, 0, 255))
            self.screen.blit(text, (700, 10))
            
        health_bar(self.screen, 10, 10, self.player.health)
        stamina_bar(self.screen, 300, 10, self.player.stamina)

        
        
        
        
        self.clock.tick(30)
        pygame.display.flip()
        #print('dick')
        

