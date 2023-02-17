import enum
from pickle import TRUE
import random

import pygame
from pygame import mixer

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Define screen sizes
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

# Define button
BUTTON_SIZE = (400, 175)
BUTTON_POSITION = (SCREEN_WIDTH / 2 - 195, SCREEN_HEIGHT / 2 + 90)

# Define position
MISS_POS = (350, 25)
HIT_POS = (125, 25)
TIME_POS = (1500, 25)
SCORE_POS = (690, 460)

# Define FPS
FPS = 60


# Define button state
class ButtonState(enum.Enum):
    IDLE = 0
    HOVER = 1


# Define ZombieState
class ZombieState(enum.Enum):
    APPEAR = 0
    DISAPPEAR = 1


# Define HammerState
class HammerState(enum.Enum):
    IDLE = 0
    SMASH = 1


# Define random position
RAND_POSITION = [(80, 280), (690, 280), (1250, 280), (80, 580), (690, 580), (1250, 580)]

# Define mouse offset
MOUSE_OFFSET = (100, 100)


# Define a base screen class
class Screen:
    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


# Define a screen for the main menu
class MainMenuScreen(Screen):
    def __init__(self):
        self.background = pygame.image.load('Game Arts/Begin2.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.button_idle = pygame.image.load('Game Arts/Play1.png')
        self.button_idle = pygame.transform.scale(self.button_idle, BUTTON_SIZE)
        self.button_hover = pygame.image.load('Game Arts/Play2.png')
        self.button_hover = pygame.transform.scale(self.button_hover, BUTTON_SIZE)
        self.button_rect = pygame.Rect(BUTTON_POSITION[0], BUTTON_POSITION[1], BUTTON_SIZE[0], BUTTON_SIZE[1])
        self.button_state = ButtonState.IDLE
        mixer.music.load("BGM/bgm.mp3")
        mixer.music.play(-1)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                if self.button_rect.collidepoint(event.pos):
                    self.button_state = ButtonState.HOVER
                else:
                    self.button_state = ButtonState.IDLE
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    game_screen.active = True
                    main_menu_screen.active = False

    def draw(self, screen):
        # Draw the background
        screen.blit(self.background, (0, 0))

        # Draw the button
        if self.button_state == ButtonState.IDLE:
            screen.blit(self.button_idle, BUTTON_POSITION)
        elif self.button_state == ButtonState.HOVER:
            screen.blit(self.button_hover, BUTTON_POSITION)


# Define a screen for the game
class GameScreen(Screen):
    def __init__(self):
        self.background = pygame.image.load('Game Arts/Background1.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.zombie = pygame.image.load('Game Arts/Zombie.png')
        self.zombie = pygame.transform.scale(self.zombie, (self.zombie.get_width()*0.8, self.zombie.get_height()*0.8))
        self.zombie_collider = self.zombie.get_rect().inflate(-125, -85)
        
        # Zombie dies
        self.zombie_dies = pygame.image.load('Game Arts/Zombie_Die.png')
        self.zombie_dies = pygame.transform.scale(self.zombie_dies, (self.zombie_dies.get_width()*0.8, self.zombie_dies.get_height()*0.8))
        self.zombie_dies_collider = self.zombie_dies.get_rect().inflate(-125, -85)
        # End Zombie dies
        
        self.mouse_idle = pygame.image.load('Game Arts/Hammer0.png')
        self.mouse_idle = pygame.transform.scale(self.mouse_idle, (self.mouse_idle.get_width() * 0.7, self.mouse_idle.get_height() * 0.7))
        self.mouse_smash = pygame.image.load('Game Arts/Hammer1.png')
        self.mouse_smash = pygame.transform.scale(self.mouse_smash, (self.mouse_smash.get_width() * 0.7, self.mouse_smash.get_height() * 0.7))
        self.mouse_collider = self.mouse_smash.get_rect().inflate(-125, -75)
        
        self.hammer_state = HammerState.IDLE
        self.zombie_state = ZombieState.APPEAR
        
        self.disappear_time = 1
        self.appear_time = 1
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.rand_position = random.choice(RAND_POSITION)
        self.mouse_pos = pygame.mouse.get_pos()

        self.hit_count = 0
        self.miss_count = 0
        self.got_hit = False
        
        self.time_countdown = 15
        self.font_name = pygame.font.Font('Fonts/SairaSemiCondensed-SemiBold.ttf', 50)
        
        self.hammerSound = mixer.Sound("BGM/hammer.mp3")
        self.zombieDieSound = mixer.Sound("BGM/zombie-death.mp3")

        self.particleSystem = []

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.hammer_state = HammerState.SMASH
                self.hammerSound.play()
                # Define Miss Event
                self.mouse_collider.x = self.mouse_pos[0] - 20
                self.mouse_collider.y = self.mouse_pos[1]
                if (self.zombie_collider.colliderect(self.mouse_collider)) & (self.zombie_state == ZombieState.APPEAR):
                    self.hit_count += 1
                    self.got_hit = True
                    if self.appear_time > 0.5:
                        self.appear_time -= 5/FPS
                        self.disappear_time -= 5/FPS
                else:
                    self.miss_count += 1
            else:
                self.hammer_state = HammerState.IDLE

    def update(self):
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.time_countdown -= 1/FPS
        if self.time_countdown <= 0:
            end_game_screen.active = True
            game_screen.active = False
            end_game_screen.score = self.hit_count * 5 - self.miss_count
            self.disappear_time = 1
            self.appear_time = 1
            self.time_countdown = 15
            self.miss_count = 0
            self.hit_count = 0
        m_pos = pygame.mouse.get_pos()
        self.mouse_pos = (m_pos[0] - MOUSE_OFFSET[0], m_pos[1] - MOUSE_OFFSET[1])
        if (self.elapsed_time < self.disappear_time) & (self.zombie_state == ZombieState.APPEAR):
            self.zombie_state = ZombieState.DISAPPEAR
            self.got_hit = False
            
        elif (self.elapsed_time < self.appear_time + self.disappear_time) & (self.elapsed_time >= self.disappear_time) & (self.zombie_state == ZombieState.DISAPPEAR):
            self.rand_position = random.choice(RAND_POSITION)
            self.zombie_state = ZombieState.APPEAR
        elif self.elapsed_time >= self.appear_time + self.disappear_time:
            self.start_time = pygame.time.get_ticks()

        #for particle in self.particleSystem:
         #   particle.Play()

    def draw(self, screen):
        # Draw the background
        screen.blit(self.background, (0, 0))
        # Fix here
        if self.zombie_state == ZombieState.APPEAR:
            self.zombie_collider.x = self.rand_position[0] + 65
            self.zombie_collider.y = self.rand_position[1] + 25
            
            if self.got_hit:
                newParticle = ParticleSystem(self.zombie_collider.x + 25, self.zombie_collider.y + 25, screen)
                newParticle.Reset()
                self.particleSystem.append(newParticle)

                self.zombieDieSound.play()
                screen.blit(self.zombie_dies, self.rand_position)
            else: 
                screen.blit(self.zombie, self.rand_position)

        if self.hammer_state == HammerState.IDLE:
            screen.blit(self.mouse_idle, self.mouse_pos)
        else:
            screen.blit(self.mouse_smash, self.mouse_pos)

        # Draw Miss click
        screen.blit(self.font_name.render(str(self.miss_count), 1, BLACK), MISS_POS)

        # Draw Hit click
        screen.blit(self.font_name.render(str(self.hit_count), 1, BLACK), HIT_POS)

        # Draw time countdown
        screen.blit(self.font_name.render(str(int(self.time_countdown)), 1, BLACK), TIME_POS)

        for particle in self.particleSystem:
            particle.Play()


class EndGameScreen(Screen):
    def __init__(self):
        self.background = pygame.image.load('Game Arts/Finish.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.button_idle = pygame.image.load('Game Arts/TryAgain1.png')
        self.button_idle = pygame.transform.scale(self.button_idle, BUTTON_SIZE)
        self.button_hover = pygame.image.load('Game Arts/TryAgain2.png')
        self.button_hover = pygame.transform.scale(self.button_hover, BUTTON_SIZE)
        self.button_rect = pygame.Rect(BUTTON_POSITION[0], BUTTON_POSITION[1], BUTTON_SIZE[0], BUTTON_SIZE[1])
        self.button_state = ButtonState.IDLE
        self.font_name = pygame.font.Font('Fonts/SairaSemiCondensed-SemiBold.ttf', 50)
        self.score = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                if self.button_rect.collidepoint(event.pos):
                    self.button_state = ButtonState.HOVER
                else:
                    self.button_state = ButtonState.IDLE
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    game_screen.active = True
                    end_game_screen.active = False
            
    def draw(self, screen):
        # Draw the background
        screen.blit(self.background, (0, 0))

        screen.blit(self.font_name.render('SCORE: ' + str(int(self.score)), 1, BLACK), SCORE_POS)

        # Draw the button
        if self.button_state == ButtonState.IDLE:
            screen.blit(self.button_idle, BUTTON_POSITION)
        elif self.button_state == ButtonState.HOVER:
            screen.blit(self.button_hover, BUTTON_POSITION)


class ZombieGame:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Zombie Game - Z Team")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Update the active screen
            if main_menu_screen.active:
                main_menu_screen.handle_events(events)
                main_menu_screen.update()
                main_menu_screen.draw(self.screen)
            elif game_screen.active:
                game_screen.handle_events(events)
                game_screen.update()
                game_screen.draw(self.screen)
            elif end_game_screen.active:
                end_game_screen.handle_events(events)
                end_game_screen.update()
                end_game_screen.draw(self.screen)

            # Update the display
            pygame.display.update()

            self.clock.tick(FPS)

class ParticleSystem:
    def __init__(self, x = 0, y = 0, screen = None):
        self.particles = []
        self.x = x
        self.y = y
        self.screen = screen
        self.num = 0

    def Play(self):
        if(self.particles):
            for particle in self.particles:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                particle[1][1] += 0.1
                particle[2] -= 15 / FPS
                pygame.draw.circle(self.screen, (255, 50, 50), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
                if(particle[2] <= 0):
                    self.particles.remove(particle)


    def Reset(self):
        self.particles = []
        self.num = random.randint(3, 10)
        for i in range (0, self.num + 1):
            self.particles.append([[self.x, self.y], [random.randint(0, 30) / 10 - 1, random.randint(-3, 3)], random.randint(5, 10)])
        

if __name__ == "__main__":

    zombie_game = ZombieGame()

    # Create the screens
    main_menu_screen = MainMenuScreen()
    game_screen = GameScreen()
    end_game_screen = EndGameScreen()

    # Set the active screen to the main menu
    main_menu_screen.active = True

    zombie_game.run()
