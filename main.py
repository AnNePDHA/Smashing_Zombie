import enum
import random

import pygame


# Define screen sizes
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

# Define button
BUTTON_SIZE = (400, 175)
BUTTON_POSITION = (SCREEN_WIDTH / 2 - 195, SCREEN_HEIGHT / 2 + 90)


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
        self.zombie_collider = self.zombie.get_rect().inflate(-100, -85)
        self.mouse_idle = pygame.image.load('Game Arts/Hammer0.png')
        self.mouse_idle = pygame.transform.scale(self.mouse_idle, (self.mouse_idle.get_width() * 0.7, self.mouse_idle.get_height() * 0.7))
        self.mouse_smash = pygame.image.load('Game Arts/Hammer1.png')
        self.mouse_smash = pygame.transform.scale(self.mouse_smash, (self.mouse_smash.get_width() * 0.7, self.mouse_smash.get_height() * 0.7))
        self.hammer_state = HammerState.IDLE
        self.zombie_state = ZombieState.APPEAR
        self.disappear_time = 1
        self.appear_time = 1
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.rand_position = random.choice(RAND_POSITION)
        self.mouse_pos = pygame.mouse.get_pos()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.hammer_state = HammerState.SMASH
            else:
                self.hammer_state = HammerState.IDLE

    def update(self):
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        m_pos = pygame.mouse.get_pos()
        self.mouse_pos = (m_pos[0] - MOUSE_OFFSET[0], m_pos[1] - MOUSE_OFFSET[1])
        if (self.elapsed_time < self.disappear_time) & (self.zombie_state == ZombieState.APPEAR):
            self.zombie_state = ZombieState.DISAPPEAR
        elif (self.elapsed_time < self.appear_time + self.disappear_time) & (self.elapsed_time >= self.disappear_time) & (self.zombie_state == ZombieState.DISAPPEAR):
            self.rand_position = random.choice(RAND_POSITION)
            self.zombie_state = ZombieState.APPEAR
        elif self.elapsed_time >= self.appear_time + self.disappear_time:
            self.start_time = pygame.time.get_ticks()

    def draw(self, screen):
        # Draw the background
        screen.blit(self.background, (0, 0))

        if self.zombie_state == ZombieState.APPEAR:
            self.zombie_collider.x = self.rand_position[0] + 60
            self.zombie_collider.y = self.rand_position[1] + 25
            #pygame.draw.rect(screen, (255, 0, 0), (self.zombie_collider.x, self.zombie_collider.y, self.zombie_collider.width, self.zombie_collider.height))
            screen.blit(self.zombie, self.rand_position)

        if self.hammer_state == HammerState.IDLE:
            screen.blit(self.mouse_idle, self.mouse_pos)
        else:
            screen.blit(self.mouse_smash, self.mouse_pos)


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

            # Update the display
            pygame.display.update()

            self.clock.tick(60)


if __name__ == "__main__":
    zombie_game = ZombieGame()

    # Create the screens
    main_menu_screen = MainMenuScreen()
    game_screen = GameScreen()
    end_game_screen = EndGameScreen()

    # Set the active screen to the main menu
    main_menu_screen.active = True

    zombie_game.run()
