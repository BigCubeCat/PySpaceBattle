from GameObjects import *
from random import randint, choice
import pygame
import sys
from time import sleep as time_pause

pygame.init()

pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=2 ** 12)
GRAVITY = 0.2
BLAST_SOUND = pygame.mixer.Sound('audio_data/blast.wav')
HIT_SOUND = pygame.mixer.Sound('audio_data/hit.wav')
CHANNELS = [pygame.mixer.Channel(i) for i in range(6)]
SOUND = True
size = width, height = 600, 600
screen_rect = (0, 0, width, height)
pygame.display.set_caption('PySpaceBattle', 'icon.png')
screen = pygame.display.set_mode(size)


def terminate():
    """
    exit from game
    """
    pygame.quit()
    sys.exit()


def clicked(rect, pos):
    """
    Check what position in rectangle
    :param rect: Rectangle (left, top, width, height)
    :param pos: position (x, y)
    :return: True if position in rectangle and False if position not in rectangle
    """
    return rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]


def draw_start_screen():
    """
     drawing main game screen
    """
    intro_text = ["PySpaceBattle", "",
                  "Shoot to survive!"]

    fon = pygame.transform.scale(load_image('bg1.png'), (1024, 4096))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(255, 100, 100))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    rects = [(50, 150, 200, 50), (50, 220, 200, 50), (50, 290, 200, 50),
             (50, 360, 200, 50), (50, 430, 200, 50)]

    pygame.draw.rect(screen, pygame.Color(75, 75, 75), (60, 150 + 10, 200, 50))
    pygame.draw.rect(screen, pygame.Color(200, 200, 200), (50, 150, 200, 50))
    pygame.draw.rect(screen, pygame.Color('black'), (50, 150, 200, 50), 5)
    string_rendered = font.render('easy', 1, pygame.Color(55, 55, 55))
    screen.blit(string_rendered, (70, 160, 200, 50))

    pygame.draw.rect(screen, pygame.Color(75, 75, 75), (60, 220 + 10, 200, 50))
    pygame.draw.rect(screen, pygame.Color(200, 200, 255), (50, 220, 200, 50))
    pygame.draw.rect(screen, pygame.Color('black'), (50, 220, 200, 50), 5)
    string_rendered = font.render('normal', 1, pygame.Color(55, 55, 0))
    screen.blit(string_rendered, (70, 230, 200, 50))

    pygame.draw.rect(screen, pygame.Color(75, 75, 75), (60, 290 + 10, 200, 50))
    pygame.draw.rect(screen, pygame.Color(200, 200, 145), (50, 290, 200, 50))
    pygame.draw.rect(screen, pygame.Color('black'), (50, 290, 200, 50), 5)
    string_rendered = font.render('hard', 1, pygame.Color(55, 55, 0))
    screen.blit(string_rendered, (70, 300, 200, 50))

    pygame.draw.rect(screen, pygame.Color(75, 75, 75), (60, 360 + 10, 200, 50))
    pygame.draw.rect(screen, pygame.Color(145, 200, 145), (50, 360, 200, 50))
    pygame.draw.rect(screen, pygame.Color('black'), (50, 360, 200, 50), 5)
    string_rendered = font.render('ultra hard', 1, pygame.Color(0, 55, 0))
    screen.blit(string_rendered, (70, 370, 200, 50))

    pygame.draw.rect(screen, pygame.Color(75, 75, 75), (60, 430 + 10, 200, 50))
    pygame.draw.rect(screen, pygame.Color(200, 145, 145), (50, 430, 200, 50))
    pygame.draw.rect(screen, pygame.Color('black'), (50, 430, 200, 50), 5)
    string_rendered = font.render('hell', 1, pygame.Color(55, 0, 0))
    screen.blit(string_rendered, (70, 440, 200, 50))
    font = pygame.font.Font(None, 25)
    pygame.draw.rect(screen, pygame.Color(200, 200, 200), (width - 64, 0, 64, 40))
    pygame.draw.rect(screen, pygame.Color('black'), (width - 64, 0, 64, 40), 5)
    string_rendered = font.render('sound:', 1, pygame.Color('black'))
    screen.blit(string_rendered, (width - 60, 0, 64, 11))

    image = pygame.transform.scale(load_image('green_btn.png', -1), (200, 200))
    screen.blit(image, (350, 350))

    font = pygame.font.Font(None, 50)
    string_rendered = font.render('Shop', 1, pygame.Color(0, 55, 0))
    screen.blit(string_rendered, (410, 430, 150, 150))
    shop_button = (350, 400, 200, 200)

    return rects, shop_button


def start_screen():
    """
    Main screen of game
    """
    global SOUND
    font = pygame.font.Font(None, 30)
    group = pygame.sprite.Group()
    while True:
        rects, shop_button = draw_start_screen()
        sound_button = (width - 64, 0, 64, 64)
        dic_sound_instance = {True: 'ON', False: "OFF"}
        string_rendered = font.render(f'{dic_sound_instance[SOUND]}', 1,
                                      pygame.Color(255, 100, 100))
        screen.blit(string_rendered, (width - 60, 20, 64, 10))
        group.draw(screen)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            for i, el in enumerate(data):
                if el == 2:
                    return i + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if clicked(sound_button, pos):
                    SOUND = not SOUND
                    string_rendered = font.render(f'{dic_sound_instance[SOUND]}', 1,
                                                  pygame.Color('red'))
                    screen.blit(string_rendered, (width - 64, 20, 64, 10))
                for i in range(len(rects)):
                    if clicked(rects[i], pos):
                        return i + 1
                if clicked(shop_button, pos):
                    shop()
                    print(data)
                    draw_start_screen()
        pygame.display.flip()
        clock.tick(10)


def shop():
    """Scene shop with player skins"""
    screen.fill((0, 0, 30))
    rects = [(0, i * 120, width, 120) for i in range(5)]
    sales = [0, 5, 10, 50, 70]
    skins = ['player.png', 'player.png', 'player2.png', 'player1.png', 'player3.png']
    count_shell = [1, 2, 2, 2, 2]
    group = pygame.sprite.Group()
    for i, element in enumerate(skins):
        im = pygame.sprite.Sprite(group)
        im.image = load_image(element)
        im.rect = im.image.get_rect()
        im.rect.center = 120, i * 120 + 60
        if data[i] == 0:
            font = pygame.font.Font(None, 25)
            btn_im = pygame.transform.scale(load_image('red_btn.png', -1), (64, 64))
            screen.blit(btn_im, (300, i * 120 + 30))
            string = font.render(str(sales[i]), 1, pygame.Color(0, 0, 0))
            screen.blit(string, (325, i * 120 + 55))
        elif data[i] == 2:
            im = pygame.transform.scale(load_image('green_btn.png', -1), (64, 64))
            screen.blit(im, (300, i * 120 + 30))
        elif data[i] == 1:
            im = pygame.transform.scale(load_image('blue_btn.png', -1), (64, 64))
            screen.blit(im, (300, i * 120 + 30))
        for k in range(count_shell[i]):
            im = pygame.transform.scale(load_image(f'shell{i + 1}.png', -1), (22, 32))
            screen.blit(im, (200 + 30 * k, i * 120 + 30))
    while True:
        group.draw(screen)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for i in range(len(rects)):
                    if clicked(rects[i], pos):
                        if data[i] == 1:
                            for j in range(5):
                                if data[j] == 2:
                                    data[j] = 1
                            data[i] = 2
                        elif data[i] == 0:
                            if data['coins'] >= sales[i]:
                                data['coins'] -= sales[i]
                                for j in range(5):
                                    if data[j] == 2:
                                        data[j] = 1
                                data[i] = 2
                                return
                        else:
                            return
        pygame.display.flip()
        clock.tick(10)


def create_particles(position, image_name='star1.png'):
    """
    :param position: position particles
    :param image_name: particles image
    """
    particle_count = randint(4, 7)
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(particles, position, choice(numbers), choice(numbers), GRAVITY, screen_rect,
                 image_name=image_name)


def check_keys(player, keys):
    """
    check keys and set movement vector for player
    :param player: player
    :param keys: list keyboard keys
    """
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.set_move('v', -1)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.set_move('v', 1)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.set_move('h', 1)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.set_move('h', -1)


class FullingObject(GameObject):
    """
    This is fulling object. When this object collide with player, player take damage
    """
    def __init__(self, group, HP, image_name, pos, speed=0,
                 screen_size=(600, 600)):
        super().__init__(group, HP, image_name, pos, speed=speed,
                         screen_size=screen_size)
        self.x_speed = randint(-1, 1) * self.speed * 0.25

    def die(self):
        """
        killing me with set damage to player
        """
        player.set_damage(self.HP)
        super().die()

    def update(self, *args):
        if pygame.sprite.collide_mask(self, player):
            self.die()
        elif self.rect.y >= self.screen_size[1]:
            self.group.remove(self)
        self.velocity[1] += self.speed
        self.velocity[0] += self.x_speed
        if pygame.sprite.collide_mask(self, player):
            self.die()
        if self.rect.x < 0:
            self.rect.x = width - 32
        elif self.rect.x > width:
            self.rect.x = 32
        if self.rect.y > height:
            self.kill()
        super().update()
        if pygame.sprite.collide_mask(self, player):
            self.die()
        if pygame.sprite.spritecollideany(self, shells):
            self.kill()


class Meteor(FullingObject):
    def kill(self):
        """
        Create some particles and kill object
        """
        create_particles(self.rect.center, image_name='stone.png')
        player.plus_score(1)
        super().kill()


class Bomb(FullingObject):
    def kill(self):
        """Create some particles and kill object"""
        game_controller.play_sound(BLAST_SOUND, 3)
        create_particles(self.rect.center, image_name='blast.png')
        super().kill()


class GameController:
    """
    Class for control game and Game events
    """
    def __init__(self, speed, hard_level, wave_delay=5,
                 meteor_prefab=FullingObject, FPS=5, delay=10):
        self.speed = speed
        self.FPS, self.delay = FPS, delay
        self.meteor_prefab = meteor_prefab
        self.hard_level = hard_level
        self.timer = 0
        self.wave_delay = wave_delay
        self.wave = 0
        self.wave_delay_ten = self.wave_delay * 3
        self.channel_index = 0
        self.boss_time = self.wave_delay_ten * 5 // self.hard_level
        self.is_boss = False
        self.boss = None

    def play_sound(self, sound, index=4):
        """
        Play sound on different channels. First 4 channels for hitting sound
        :param sound: Sound for playing (pygame.mixer.Sound)
        :param index: Chanel index
        """
        if SOUND:
            if index == -1:  # -1 for shooting sound
                CHANNELS[self.channel_index].play(sound)
                self.channel_index = (self.channel_index + 1) % 4
            else:
                CHANNELS[index].play(sound)

    def make_meteor(self):
        """
        Create Meteor in top screen
        """
        pos = (randint(0, width - 64), randint(-128, 0))
        Meteor(enemy_group, 10, 'm', pos, 1, screen_size=size)

    def make_rockets(self):
        """
        Create some rockets in top screen
        """
        old_positions = []
        for i in range(randint(1, int(1.2 * self.hard_level))):
            x = randint(0, width)
            while any([x <= i <= x + 64 for i in old_positions]):
                x = randint(0, width)
            Rocket(f"shell{randint(1, 4)}", enemy_group, randint(self.hard_level,
                                                                 int(1.5 * self.hard_level)),
                   (x, -64), speed=self.speed)
            old_positions.append(x)

    def update(self):
        if not self.is_boss:
            self.timer += 1
            if self.timer % self.delay == 0:
                for _ in range(randint(1, self.hard_level)):
                    self.make_meteor()
            if self.timer % self.wave_delay == 0:
                self.wave = (self.wave + 1) % self.wave_delay
                self.make_rockets()
                if randint(0, 2) == 0:
                    if randint(0, 1) == 0:
                        Star(particles, (randint(0, width), 0), speed=self.speed)
                    else:
                        Diamond(particles, (randint(0, width), 0), speed=self.speed)
                    Coin(particles, (randint(0, width), 0), speed=self.speed)
            if self.timer % self.wave_delay_ten == 0:
                Planet(planets, image_name=f'earth{randint(1, 4)}',
                       pos=(randint(-64, width + 64), -128))
            if self.timer % self.boss_time == 0:
                self.is_boss = True
                self.boss = Boss()
        else:
            if len(boss_group) == 0:
                self.is_boss = False


class Boss(GameObject):
    """
    This is Boss. He comming very rare and very strong.
    """
    def __init__(self):
        super().__init__(boss_group, 300 * game_controller.hard_level, 'boss', (width // 2, -128),
                         speed=game_controller.speed,
                         screen_size=size)
        enemy_group = pygame.sprite.Group()  # delete all enemys
        self.left_border = (self.rect.width - self.HP / 10) // 2
        self.timer = 0

    def update(self, *args):
        self.timer += 1
        screen.fill(pygame.Color(10, 200, 10), (
            self.rect.x + self.left_border, self.rect.y - 15, self.HP / 10, 5
        ))
        if self.rect.y < 0:
            self.velocity[1] = self.speed
        elif self.timer % 10 == 0:
            if self.timer % 20 == 0:
                self.velocity = [self.speed, self.speed]
            else:
                self.velocity = [-self.speed, -self.speed]
        if self.timer % 50 == 0:
            self.hit()
        if pygame.sprite.spritecollideany(self, shells):
            self.HP -= player.power
        super().update()

    def kill(self):
        """
        creating many particles and kill boss
        """
        game_controller.play_sound(BLAST_SOUND)
        for __ in range(5):
            create_particles(self.rect.center, image_name='blast.png')
        super().kill()

    def hit(self):
        """Drop bomb"""
        Bomb(enemy_group, 10, 'mine', (self.rect.center[0], self.rect.bottom + 32),
             speed=1, screen_size=size)


class Player(GameObject):
    player_types = {
        # id: ('sprite name', count shells, speed, power)
        0: ('player', 1, 1, 1),
        1: ('player', 2, 1, 1),
        2: ('player2', 2, 1.1, 2),
        3: ('player1', 2, 1.3, 3),
        4: ('player3', 2, 1.15, 5),
    }

    def __init__(self, group, HP, pos, player_type=None, speed=0, screen_size=(600, 600), coins=0):
        self.score = 0
        self.speed_shell = 5
        self.index = 0
        for i in range(5):
            if player_type[i] == 2:
                self.player_type = self.player_types[i]
                self.index = i
                break
        self.shell_name = self.index + 1
        self.count_coins = coins
        super().__init__(group, HP, self.player_type[0], pos, speed=speed,
                         screen_size=screen_size)
        self.power = self.player_type[-1]
        self.speed *= self.player_type[2]

    def plus_score(self, score):
        """added score"""
        self.score += score

    def set_damage(self, damage):
        """setting damage for player"""
        self.HP -= damage

    def update(self, *args):
        super().update(*args)
        self.velocity = [0, 0]  # Nullify player movement vector

    def set_move(self, axis, way):
        """Set movement Vector"""
        if axis == 'v':
            self.velocity[1] = way * self.speed
        elif axis == 'h':
            self.velocity[0] = way * self.speed

    def hit(self):
        """Fire a shot"""
        if self.index == 0:
            Shell(shells, self.speed * self.speed_shell, (self.rect.x + 21, self.rect.y - 40), True,
                  shell_name=f'shell{self.shell_name}')
        elif 1 <= self.index <= 3:
            Shell(shells, self.speed * self.speed_shell, (self.rect.x + 2, self.rect.y - 40), True,
                  shell_name=f'shell{self.shell_name}')
            Shell(shells, self.speed * self.speed_shell, (self.rect.x + 38, self.rect.y - 40), True,
                  shell_name=f'shell{self.shell_name}')
        elif self.index == 4:
            Shell(shells, self.speed * self.speed_shell, (self.rect.x + 2, self.rect.y - 20), True,
                  shell_name=f'shell{self.shell_name}')
            Shell(shells, self.speed * self.speed_shell, (self.rect.x + 38, self.rect.y - 20), True,
                  shell_name=f'shell{self.shell_name}')

    def move_on_vector(self):
        """
        Moving object on vector.
        Player can not move out screen on Y Axis and
        moves on other side on X Axis if player out screen
        """
        self.rect.x += self.velocity[0]
        new_y = self.rect.y + self.velocity[1]
        if 0 <= new_y and new_y + self.rect.height - self.speed <= self.screen_size[1]:
            self.rect.y = new_y
        if self.rect.x < 0:
            self.rect.x = self.screen_size[0] - self.rect.width
        if self.rect.x > self.screen_size[0] - self.rect.width:
            self.rect.x = 0


class Star(pygame.sprite.Sprite):
    """This is shooting star. On Collide with player add 100 score """
    def __init__(self, group, pos, speed=10, image_name='falling-star.png'):
        super().__init__(group)
        self.speed = speed
        self.image = load_image(image_name, -1)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, *args):
        self.rect.y += self.speed
        if pygame.sprite.collide_mask(self, player) or self.rect.y > height:
            self.die()
        super().update(*args)
        if not self.rect.colliderect(screen_rect):
            self.kill()

    def die(self):
        """Call when player take star. Add 100 score to player"""
        player.plus_score(100)
        create_particles(self.rect.center)
        self.kill()


class Diamond(Star):
    """HP-bonus for player"""
    def __init__(self, group, pos, speed=10):
        super().__init__(group, pos, speed=speed, image_name='diamond.png')

    def die(self):
        """Add health for player and killing me"""
        player.HP += 10
        if player.HP > 100:
            player.HP = 100
        self.kill()


class Coin(Star):
    """It is Coin - money"""
    def __init__(self, group, pos, speed=10):
        super().__init__(group, pos, speed=speed, image_name='coin.png')

    def die(self):
        """Add coin for player"""
        player.count_coins += game_controller.hard_level
        self.kill()


class Rocket(GameObject):
    """This is enemy-rocket. Shooting anf killing"""
    sprites = ['spaceship', 'spaceship1']

    def __init__(self, shell_name, g, HP, pos, speed=0):
        sprite = choice(self.sprites)
        super().__init__(g, HP, sprite, pos, speed=speed,
                         screen_size=size)
        self.shell_name = shell_name
        self.delay = game_controller.delay * 2
        self.timer = 0
        self.left_border = (self.rect.width - self.HP * 10) // 2
        if sprite == 'spaceship1':
            self.double_hit = True
            self.speed *= 1.2
            self.delay *= 0.8
        else:
            self.double_hit = False

    def die(self):
        player.plus_score(20)
        super().die()

    def kill(self):
        create_particles(self.rect.center, image_name='blast.png')
        game_controller.play_sound(BLAST_SOUND, index=3)
        super().kill()

    def update(self, *args):
        self.timer = (self.timer + 1) % self.delay
        if self.timer == 0:
            self.hit()
        self.velocity[1] = self.speed
        if player.rect.x < self.rect.x:
            self.velocity[0] = -self.speed * 0.2
        elif player.rect.x > self.rect.x:
            self.velocity[0] = self.speed * 0.2
        super().update()
        if pygame.sprite.spritecollideany(self, shells):
            self.HP -= player.power
            if self.HP <= 0:
                self.die()
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.HP = 0
        if self.HP == 0 or self.rect.y > height:
            self.kill()
        screen.fill(pygame.Color(10, 200, 10), (
            self.rect.x + self.left_border, self.rect.y - 15, self.HP * 10, 5
        ))

    def hit(self):
        if not self.double_hit:
            pos = (self.rect.x + 21, self.rect.y + 64)
            Shell(enemy_group, self.speed * -3, pos, False, shell_name=self.shell_name)
        else:
            pos = (self.rect.left + 5, self.rect.y + 64)
            pos1 = (self.rect.right - 30, self.rect.y + 64)
            Shell(enemy_group, self.speed * -3, pos, False, shell_name=self.shell_name)
            Shell(enemy_group, self.speed * -3, pos1, False, shell_name=self.shell_name)


class Satellite(Rocket):
    sprites = ['satellite1', 'satellite1']

    def hit(self):
        pos = (self.rect.x + 21, self.rect.y + 64)
        Shell(enemy_group, game_controller.speed * -4, pos, False, shell_name=self.shell_name)


class Planet(pygame.sprite.Sprite):
    """Background object with satellite"""
    def __init__(self, group,
                 image_name, pos=(-64, -128), speed=1):
        super().__init__(group)
        self.image_name = image_name
        self.speed = speed
        self.image = load_image(f'{image_name}.png')
        self.rect = self.image.get_rect()
        self.rect.center = pos
        for i in range(game_controller.hard_level // 2):
            self.make_satellite()

    def make_satellite(self):
        old_positions = []
        for i in range(randint(1, int(1.5 * game_controller.hard_level))):
            pos = randint(self.rect.x, self.rect.right), randint(self.rect.y, self.rect.bottom)
            Satellite(f"shell{randint(1, 4)}", enemy_group,
                      randint(game_controller.hard_level,
                              int(1.5 * game_controller.hard_level)),
                      pos, speed=1)
            old_positions.append(pos)

    def update(self, *args):
        self.rect.bottom += self.speed
        if self.rect.y == 0:
            self.rect.y += self.speed
        if self.rect.y > 512:
            self.kill()


class Shell(pygame.sprite.Sprite):
    """It is laser bullet"""
    def __init__(self, group, speed, pos, from_player=True, shell_name=f'shell{randint(1, 4)}'):
        super().__init__(group)
        self.image = load_image(f'{shell_name}.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = speed
        self.from_player = from_player
        if self.from_player:
            game_controller.play_sound(HIT_SOUND, index=-1)
        else:
            game_controller.play_sound(HIT_SOUND, index=5)

    def update(self, *args):
        self.rect.y -= self.speed
        if not self.rect.colliderect(screen_rect):
            self.kill()
        if self.from_player:
            if (pygame.sprite.spritecollideany(self, all_sprites) or
                    pygame.sprite.spritecollideany(self, enemy_group)):
                self.kill()
            if self.rect.y <= -32:
                self.kill()
            elif game_controller.is_boss:
                if pygame.sprite.collide_mask(self, game_controller.boss):
                    self.kill()
        else:
            if pygame.sprite.collide_mask(self, player):
                player.set_damage(10)
                self.kill()
            elif self.rect.y > height:
                self.kill()


def read_data():
    """
    reading data from files
    """
    with open('best_score.txt', 'r') as f:
        score = eval(f.read())
    with open('data.txt', 'r', encoding='utf-8') as f:
        data = eval(f.read())
    return data, score


def save_data(score):
    """
    saving data to flies
    """
    with open('best_score.txt', 'w', encoding='utf-8') as f:
        f.write(score.__str__())
    with open('data.txt', 'w', encoding='utf-8') as f:
        f.write(data.__str__())


def drawing():
    """
    drawing UI elements in Game Scene
    """
    font = pygame.font.Font(None, 20)
    screen.fill(pygame.Color(200, 45, 45), (10, 110 - player.HP, 10, player.HP))
    screen.fill(pygame.Color(200, 200, 200), (0, 120, 100, 90))
    string_rendered = font.render('score:', 1, pygame.Color(75, 75, 75))
    screen.blit(string_rendered, (20, 120, 50, 30))
    string_rendered = font.render(str(player.score), 1, pygame.Color(75, 75, 75))
    screen.blit(string_rendered, (20, 135, 50, 30))
    string_rendered = font.render('best score:', 1,
                                  pygame.Color(75, 75, 75))
    screen.blit(string_rendered, (20, 150, 50, 30))
    string_rendered = font.render(str(best_score[hard_level]), 1,
                                  pygame.Color(75, 75, 75))
    screen.blit(string_rendered, (20, 165, 50, 30))
    string_rendered = font.render('count money:', 1,
                                  pygame.Color(75, 75, 75))
    screen.blit(string_rendered, (20, 180, 50, 30))
    string_rendered = font.render(str(player.count_coins), 1,
                                  pygame.Color(75, 75, 75))
    screen.blit(string_rendered, (20, 195, 50, 30))

    screen.blit(pygame.transform.scale(load_image("star1.png"), (16, 16)), (0, 120, 16, 16))
    screen.blit(pygame.transform.scale(load_image("star.png"), (16, 16)), (0, 150, 16, 16))
    screen.blit(pygame.transform.scale(load_image("coin.png"), (16, 16)), (0, 180, 16, 16))
    screen.blit(pygame.transform.scale(load_image("diamond.png"), (16, 16)), (6, 100, 20, 20))


def drawing_and_update():
    """
    update and drawing all groups
    """
    bg.update()
    bg.draw(screen)
    planets.update()
    planets.draw(screen)
    particles.draw(screen)
    particles.update()
    all_sprites.draw(screen)
    all_sprites.update()
    boss_group.update()
    boss_group.draw(screen)
    shells.draw(screen)
    enemy_group.update()
    enemy_group.draw(screen)
    shells.update()


while True:
    data, best_score = read_data()
    clock = pygame.time.Clock()
    running = True
    enemy_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    shells = pygame.sprite.Group()
    planets = pygame.sprite.Group()
    bg = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()

    hard_level = start_screen()
    game_controller = GameController(10, hard_level, FPS=25,
                                     wave_delay=200)

    BG(bg, f'bg{hard_level}', top=True, screen_size=size)
    BG(bg, f'bg{hard_level}', top=False, screen_size=size)
    player = Player(all_sprites, player_type=data, HP=100,
                    pos=(width // 2, height // 2),
                    speed=game_controller.speed,
                    screen_size=size, coins=data['coins'])
    PLAYER_HIT = 30
    pygame.time.set_timer(PLAYER_HIT, 175)
    while running:
        if player.HP <= 0:
            if player.score > best_score[hard_level]:
                best_score[hard_level] = player.score
            data['coins'] = player.count_coins
            save_data(best_score)
            time_pause(0.3)
            break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            break
        check_keys(player, keys)
        game_controller.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == PLAYER_HIT:
                player.hit()
        drawing_and_update()
        drawing()
        clock.tick(game_controller.FPS)
        pygame.display.flip()
        player.plus_score(1)
