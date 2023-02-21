import pygame
import random
import enum
from pygame import mixer

# Define random position
RAND_POSITION = [(80, 280), (690, 280), (1250, 280), (80, 580), (690, 580), (1250, 580)]

# Define FPS
FPS = 60


# Define ZombieState
class ZombieState(enum.Enum):
    APPEAR = 0
    DISAPPEAR = 1


zombie_num = 0
random_pos_list = []
hit_count = 0
miss_count = 0


class HitMissMgr:
    @staticmethod
    def update_hit():
        global hit_count
        hit_count += 1

    @staticmethod
    def update_miss():
        global miss_count
        miss_count += 1

    @staticmethod
    def update_znum():
        global zombie_num
        zombie_num += 1

    @staticmethod
    def cache_pos(pos):
        global random_pos_list
        if pos not in random_pos_list:
            for p in RAND_POSITION:
                random_pos_list.append(p)
        random_pos_list.remove(pos)

    @staticmethod
    def get_rand_pos():
        global random_pos_list
        if len(random_pos_list) <= 0:
            for p in RAND_POSITION:
                random_pos_list.append(p)
        return random.choice(random_pos_list)

    @staticmethod
    def get_hit():
        global hit_count
        return hit_count

    @staticmethod
    def get_miss():
        global miss_count
        return miss_count

    @staticmethod
    def reset():
        global hit_count
        global miss_count
        global zombie_num
        global random_pos_list
        hit_count = 0
        miss_count = 0
        zombie_num = 0
        random_pos_list.clear()


class ZombieObject:
    def __init__(self, path, d_path, appear, disappear):
        self.zombie = pygame.image.load(path)
        self.zombie = pygame.transform.scale(self.zombie, (self.zombie.get_width() * 0.8, self.zombie.get_height() * 0.8))
        self.zombie_collider = self.zombie.get_rect().inflate(-125, -85)

        self.zombie_dies = pygame.image.load(d_path)
        self.zombie_dies = pygame.transform.scale(self.zombie_dies, (self.zombie_dies.get_width()*0.8, self.zombie_dies.get_height()*0.8))
        self.zombie_dies_collider = self.zombie_dies.get_rect().inflate(-125, -85)

        self.particleSystem = []
        self.zombie_state = ZombieState.APPEAR
        self.appear_time = appear
        self.disappear_time = disappear
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.rand_position = HitMissMgr.get_rand_pos()
        HitMissMgr.cache_pos(self.rand_position)
        self.got_hit = False

        self.zombieDieSound = mixer.Sound("BGM/zombie-death.mp3")

    def handle_events(self, mouse_collider):
        if (self.zombie_collider.colliderect(mouse_collider)) & (self.zombie_state == ZombieState.APPEAR):
            HitMissMgr.update_hit()
            self.got_hit = True
            if self.appear_time > 0.75:
                self.appear_time -= 1 / FPS
                self.disappear_time -= 1 / FPS

    def update(self):
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        if (self.elapsed_time < self.disappear_time) & (self.zombie_state == ZombieState.APPEAR):
            self.zombie_state = ZombieState.DISAPPEAR
            self.got_hit = False
        elif (self.elapsed_time < self.appear_time + self.disappear_time) and (self.elapsed_time >= self.disappear_time) & (self.zombie_state == ZombieState.DISAPPEAR):
            self.rand_position = HitMissMgr.get_rand_pos()
            HitMissMgr.cache_pos(self.rand_position)
            self.zombie_state = ZombieState.APPEAR
        elif self.elapsed_time >= self.appear_time + self.disappear_time:
            self.start_time = pygame.time.get_ticks()

    def draw(self, screen):
        if self.zombie_state == ZombieState.APPEAR:
            self.zombie_collider.x = self.rand_position[0] + 65
            self.zombie_collider.y = self.rand_position[1] + 25

            if self.got_hit:
                new_particle = ParticleSystem(self.zombie_collider.x + random.randint(25, 45), self.zombie_collider.y + random.randint(25, 45), screen)
                new_particle.Reset()
                self.particleSystem.append(new_particle)
                self.zombieDieSound.play()
                screen.blit(self.zombie_dies, self.rand_position)
            else:
                screen.blit(self.zombie, self.rand_position)

        for particle in self.particleSystem:
            particle.Play()


class ParticleSystem:
    def __init__(self, x = 0, y = 0, screen = None):
        self.particles = []
        self.x = x
        self.y = y
        self.screen = screen
        self.num = 0

    def Play(self):
        if self.particles:
            for particle in self.particles:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                particle[1][1] += 0.1
                particle[2] -= 15 / FPS
                pygame.draw.circle(self.screen, (255, 50, 50), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
                if particle[2] <= 0:
                    self.particles.remove(particle)

    def Reset(self):
        self.particles = []
        self.num = random.randint(5, 10)
        for i in range (0, self.num + 1):
            self.particles.append([[self.x, self.y], [random.randint(-30, 50) / 10 - 1, random.randint(-4, 4)], random.randint(5, 12)])
