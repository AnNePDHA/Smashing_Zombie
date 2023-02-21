import enum
import random

import pygame
from pygame import mixer
from Zombie import ZombieObject, HitMissMgr

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
HITTED_POS = (610, 760)
MISSED_POS = (840, 760)

# Define FPS
FPS = 60

# Define interval
INTERVAL = 10


# Define button state
class ButtonState(enum.Enum):
    IDLE = 0
    HOVER = 1


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

        self.zlist = []
        self.zlist.append(ZombieObject('Game Arts/Zombie.png', 'Game Arts/Zombie_Die.png', 1, 1))
        self.zlist.append(ZombieObject('Game Arts/Zombie1.png', 'Game Arts/Zombie_Die1.png', 1, 1))

        self.z_cur_list = []
        HitMissMgr.update_znum()
        self.z_cur_list.append(random.choice(self.zlist))
        self.zlist.remove(self.z_cur_list[-1])

        self.mouse_idle = pygame.image.load('Game Arts/Hammer0.png')
        self.mouse_idle = pygame.transform.scale(self.mouse_idle, (self.mouse_idle.get_width() * 0.7, self.mouse_idle.get_height() * 0.7))
        self.mouse_smash = pygame.image.load('Game Arts/Hammer1.png')
        self.mouse_smash = pygame.transform.scale(self.mouse_smash, (self.mouse_smash.get_width() * 0.7, self.mouse_smash.get_height() * 0.7))
        self.mouse_collider = self.mouse_smash.get_rect().inflate(-125, -75)
        
        self.hammer_state = HammerState.IDLE
        self.mouse_pos = pygame.mouse.get_pos()
        self.font_name = pygame.font.Font('Fonts/SairaSemiCondensed-SemiBold.ttf', 50)
        self.hammerSound = mixer.Sound("BGM/hammer.mp3")
        self.time_countdown = 30
        self.interval = INTERVAL
        self.reloadHammerStateTime = 100
        self.hammerSmashTime = 0
        self.allowChangeHammerState = True

        self.got_hit = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.hammerSmashTime = pygame.time.get_ticks()
                self.allowChangeHammerState = False
                self.hammer_state = HammerState.SMASH
                self.hammerSound.play()
                # Define Miss Event
                self.mouse_collider.x = self.mouse_pos[0] - 20
                self.mouse_collider.y = self.mouse_pos[1]
                self.got_hit = False
                for z in self.z_cur_list:
                    z.handle_events(self.mouse_collider)
                    if not self.got_hit:
                        self.got_hit = z.got_hit
                if not self.got_hit:
                    HitMissMgr.update_miss()
            else:
                if self.allowChangeHammerState:
                    self.hammer_state = HammerState.IDLE

    def update(self):
        self.time_countdown -= 1/FPS
        self.interval -= 1/FPS
        if self.time_countdown <= 0:
            self.zlist.clear()
            self.z_cur_list.clear()
            end_game_screen.active = True
            game_screen.active = False
            self.time_countdown = 15
            mixer.music.fadeout(3000)
        m_pos = pygame.mouse.get_pos()
        self.mouse_pos = (m_pos[0] - MOUSE_OFFSET[0], m_pos[1] - MOUSE_OFFSET[1])
        for z in self.z_cur_list:
            z.update()
        if (self.interval <= 0) and (len(self.z_cur_list) < 4):
            if len(self.zlist) <= 0:
                self.zlist.append(ZombieObject('Game Arts/Zombie.png', 'Game Arts/Zombie_Die.png', 1, 1))
                self.zlist.append(ZombieObject('Game Arts/Zombie1.png', 'Game Arts/Zombie_Die1.png', 1, 1))
            HitMissMgr.update_znum()
            self.z_cur_list.append(random.choice(self.zlist))
            self.zlist.remove(self.z_cur_list[-1])
            self.interval = INTERVAL
        if pygame.time.get_ticks() - self.hammerSmashTime >= self.reloadHammerStateTime:
            self.allowChangeHammerState = True
            self.hammer_state = HammerState.IDLE

    def draw(self, screen):
        # Draw the background
        screen.blit(self.background, (0, 0))

        for z in self.z_cur_list:
            z.draw(screen)

        if self.hammer_state == HammerState.IDLE:
            screen.blit(self.mouse_idle, self.mouse_pos)
        else:
            screen.blit(self.mouse_smash, self.mouse_pos)

        # Draw Miss click
        screen.blit(self.font_name.render(str(HitMissMgr.get_miss()), 1, BLACK), MISS_POS)

        # Draw Hit click
        screen.blit(self.font_name.render(str(HitMissMgr.get_hit()), 1, BLACK), HIT_POS)

        # Draw time countdown
        screen.blit(self.font_name.render(str(int(self.time_countdown)), 1, BLACK), TIME_POS)


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
        self.hit_score = 0
        self.miss_score = 0

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
                    HitMissMgr.reset()
                    mixer.music.play(-1)
                    game_screen.active = True
                    game_screen.__init__()
                    end_game_screen.active = False

    def draw(self, screen):
        # Draw the background
        screen.blit(self.background, (0, 0))

        self.hit_score = HitMissMgr.get_hit()
        self.miss_score = HitMissMgr.get_miss()

        self.score = self.hit_score * 5 - self.miss_score
        screen.blit(self.font_name.render('SCORE: ' + str(int(self.score)), 1, BLACK), SCORE_POS)
        screen.blit(self.font_name.render('HIT: ' + str(int(self.hit_score)), 1, WHITE), HITTED_POS)
        screen.blit(self.font_name.render('MISS: ' + str(int(self.miss_score)), 1, RED), MISSED_POS)

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


if __name__ == "__main__":
    zombie_game = ZombieGame()

    # Create the screens
    main_menu_screen = MainMenuScreen()
    game_screen = GameScreen()
    end_game_screen = EndGameScreen()

    # Set the active screen to the main menu
    main_menu_screen.active = True

    zombie_game.run()
