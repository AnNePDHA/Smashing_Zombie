import enum

import pygame
from pygame import mixer
pygame.font.init()
clock = pygame.time.Clock()

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define screen sizes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#  Define font text
FONT= pygame.font.SysFont('comicsans',30)


# Define position
MISS_POS = (280,25)
HIT_POS = (100,25)
TIME_POS = (1215,25)
ZOM_POS = [(100,100)]

# Define button state
class ButtonState(enum.Enum):
    IDLE = 0
    HOVER = 1


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
        self.background = pygame.image.load('Game Arts/Begin.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.button_idle = pygame.image.load('Game Arts/Play1.png')
        self.button_idle = pygame.transform.scale(self.button_idle, (325, 140))
        self.button_hover = pygame.image.load('Game Arts/Play2.png')
        self.button_hover = pygame.transform.scale(self.button_hover, (325, 140))
        self.button_rect = pygame.Rect(SCREEN_WIDTH / 2 - 175, SCREEN_HEIGHT / 2 + 77, 325, 140)
        self.button_state = ButtonState.IDLE
        mixer.music.load("BGM/Bgm (friendly spookier version).mp3")
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
                game_screen.active = True
                main_menu_screen.active = False

    def draw(self, screen):
        # Draw the background
        screen.blit(self.background, (0, 0))

        # Draw the button
        if self.button_state == ButtonState.IDLE:
            screen.blit(self.button_idle, (SCREEN_WIDTH / 2 - 175, SCREEN_HEIGHT / 2 + 77))
        elif self.button_state == ButtonState.HOVER:
            screen.blit(self.button_hover, (SCREEN_WIDTH / 2 - 175, SCREEN_HEIGHT / 2 + 77))


# Define a screen for the game
class GameScreen(Screen):
    def __init__(self):
        self.background = pygame.image.load('Game Arts/Background1.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.hammerSound = mixer.Sound("BGM/hammer.mp3")
        self.hit_count = 0
        self.miss_count = 0
        self.time_countdown = 60
        

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.hammerSound.play()
                x_pos , y_pos = pygame.mouse.get_pos()
                x_pos, y_pos = int(x_pos), int(y_pos)
                #Define Miss Event
                if (x_pos,y_pos) not in ZOM_POS:
                    self.miss_count+=1
                else:
                    self.hit_count+=1


    def draw(self, screen):
        # Draw the background
        screen.blit(self.background, (0, 0))

        # Draw Miss click
        screen.blit(FONT.render(str(self.miss_count),1,BLACK),MISS_POS)

        # Draw Hit click
        screen.blit(FONT.render(str(self.hit_count),1,BLACK),HIT_POS)

        # Draw time countdown
        screen.blit(FONT.render(str(self.time_countdown),1,BLACK),TIME_POS)

        # Draw position mouse
        x_pos , y_pos = pygame.mouse.get_pos()
        x_pos, y_pos = int(x_pos), int(y_pos)
        pos_text = FONT.render("X: "+ str(x_pos) + "- Y: "+ str(y_pos),1, WHITE)
        screen.blit(pos_text,(0,0))


class EndGameScreen(Screen):
    def __init__(self):
        self.background = pygame.image.load('Game Arts/Finish.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def handle_events(self, events):
        pass

    def draw(self, screen):
        # Draw the background
        screen.blit(self.background, (0, 0))


class ZombieGame:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Zombie Game - Z Team")

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

            # Update the display
            pygame.display.update()


if __name__ == "__main__":
    
    zombie_game = ZombieGame()

    # Create the screens
    main_menu_screen = MainMenuScreen()
    game_screen = GameScreen()
    end_game_screen = EndGameScreen()

    # Set the active screen to the main menu
    main_menu_screen.active = True

    zombie_game.run()
