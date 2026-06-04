import pygame
import os
import random
import sys


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def get_save_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

pygame.init()
try:
    pygame.mixer.init()
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, 'imgs')
HIGH_SCORE_FILE = get_save_path('highscore.txt')
MENU_MUSIC_FILE = resource_path('backgroundmusicforvideos-gaming-game-minecraft-background-music-372242.mp3')
GAME_MUSIC_FILE = resource_path('tatamusic-game-gaming-minecraft-background-music-377647.mp3')

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(resource_path(os.path.join('imgs', 'pipe.png'))))
GROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(resource_path(os.path.join('imgs', 'base.png'))))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(resource_path(os.path.join('imgs', 'bg.png'))))
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(resource_path(os.path.join('imgs', 'bird1.png')))),
    pygame.transform.scale2x(pygame.image.load(resource_path(os.path.join('imgs', 'bird2.png')))),
    pygame.transform.scale2x(pygame.image.load(resource_path(os.path.join('imgs', 'bird3.png')))),
]

pygame.font.init()
SCORE_FONT = pygame.font.SysFont('arial', 50)
MENU_FONT = pygame.font.SysFont('arial', 40)


class Bird:
    IMGS = BIRD_IMAGES
    # rotation animation
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.height = self.y
        self.time = 0
        self.image_count = 0
        self.image = self.IMGS[0]

    def jump(self):
        self.velocity = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        # calculate displacement
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.velocity * self.time

        # restrict displacement
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # the bird's angle
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_VELOCITY

    def draw(self, screen):
        # select the bird image for animation
        self.image_count += 1

        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_count < self.ANIMATION_TIME * 2:
            self.image = self.IMGS[1]
        elif self.image_count < self.ANIMATION_TIME * 3:
            self.image = self.IMGS[2]
        elif self.image_count < self.ANIMATION_TIME * 4:
            self.image = self.IMGS[1]
        elif self.image_count >= self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMGS[0]
            self.image_count = 0

        # if the bird is falling, don't flap wings
        if self.angle <= -80:
            self.image = self.IMGS[1]
            self.image_count = self.ANIMATION_TIME * 2

        # draw the bird image
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        image_center = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center=image_center)
        screen.blit(rotated_image, rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Pipe:
    DISTANCE = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_pos = 0
        self.bottom_pos = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top_pos = self.height - self.PIPE_TOP.get_height()
        self.bottom_pos = self.height + self.DISTANCE

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.top_pos))
        screen.blit(self.PIPE_BOTTOM, (self.x, self.bottom_pos))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top_pos - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom_pos - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_offset)
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)

        return top_point or bottom_point


class Ground:
    VELOCITY = 5
    WIDTH = GROUND_IMAGE.get_width()
    IMAGE = GROUND_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))


def draw_screen(screen, birds, pipes, ground, score):
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    score_text = SCORE_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - 10 - score_text.get_width(), 10))
    ground.draw(screen)
    pygame.display.update()


def load_highscore():
    try:
        with open(HIGH_SCORE_FILE, 'r', encoding='utf-8') as file:
            return int(file.read().strip() or 0)
    except Exception:
        return 0


def save_highscore(score, highscore):
    if score > highscore:
        with open(HIGH_SCORE_FILE, 'w', encoding='utf-8') as file:
            file.write(str(score))
        return score
    return highscore


def play_music(music_file, volume=0.5):
    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
    except Exception:
        pass


def main_menu(screen, clock, highscore):
    play_music(MENU_MUSIC_FILE)
    options = ["Play", "Options", "Exit"]
    selected = 0

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[selected]

        screen.blit(BACKGROUND_IMAGE, (0, 0))
        title = SCORE_FONT.render("Flappy Bird", 1, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            text = MENU_FONT.render(option, 1, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250 + i * 60))

        highscore_text = MENU_FONT.render(f"High Score: {highscore}", 1, (255, 255, 255))
        screen.blit(highscore_text, (SCREEN_WIDTH // 2 - highscore_text.get_width() // 2, 180))

        instructions = MENU_FONT.render("Use ↑ ↓ and Enter", 1, (255, 255, 255))
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 520))

        pygame.display.update()


def options_menu(screen, clock, sound_enabled):
    play_music(MENU_MUSIC_FILE)
    options = ["Sound", "Back"]
    selected = 0

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT) and selected == 0:
                    sound_enabled = not sound_enabled
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected == 0:
                        sound_enabled = not sound_enabled
                    else:
                        return sound_enabled
                elif event.key == pygame.K_ESCAPE:
                    return sound_enabled

        screen.blit(BACKGROUND_IMAGE, (0, 0))
        title = SCORE_FONT.render("Options", 1, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        sound_status = "On" if sound_enabled else "Off"
        options_text = [f"Sound: {sound_status}", "Back"]

        for i, option in enumerate(options_text):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            text = MENU_FONT.render(option, 1, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250 + i * 60))

        instructions = MENU_FONT.render("Use ← → to toggle", 1, (255, 255, 255))
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 520))

        pygame.display.update()


def play_game(screen, clock):
    play_music(GAME_MUSIC_FILE)
    birds = [Bird(230, 350)]
    ground = Ground(730)
    pipes = [Pipe(700)]
    score = 0

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        for bird in birds:
            bird.move()
        ground.move()

        add_pipe = False
        remove_pipes = []
        remove_birds = []
        for pipe in pipes:
            for bird in birds:
                if pipe.collide(bird):
                    remove_birds.append(bird)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move()
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipes.append(pipe)

        for bird in remove_birds:
            if bird in birds:
                birds.remove(bird)

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        for pipe in remove_pipes:
            pipes.remove(pipe)

        for bird in birds[:]:
            if (bird.y + bird.image.get_height()) > ground.y or bird.y < 0:
                birds.remove(bird)

        if not birds:
            return score

        draw_screen(screen, birds, pipes, ground, score)


def game_over(screen, clock, score, highscore):
    play_music(MENU_MUSIC_FILE)
    options = ["Play again", "Menu"]
    selected = 0

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[selected]
                elif event.key == pygame.K_ESCAPE:
                    return "Menu"

        screen.blit(BACKGROUND_IMAGE, (0, 0))
        title = SCORE_FONT.render("Game Over", 1, (255, 0, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        score_text = MENU_FONT.render(f"Final score: {score}", 1, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))

        highscore_text = MENU_FONT.render(f"High Score: {highscore}", 1, (255, 255, 255))
        screen.blit(highscore_text, (SCREEN_WIDTH // 2 - highscore_text.get_width() // 2, 240))

        if score >= highscore:
            new_record = MENU_FONT.render("New high score!", 1, (255, 255, 0))
            screen.blit(new_record, (SCREEN_WIDTH // 2 - new_record.get_width() // 2, 280))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            text = MENU_FONT.render(option, 1, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 340 + i * 60))

        instructions = MENU_FONT.render("Use ↑ ↓ and Enter", 1, (255, 255, 255))
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 520))

        pygame.display.update()


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')
    clock = pygame.time.Clock()
    sound_enabled = True

    highscore = load_highscore()

    while True:
        choice = main_menu(screen, clock, highscore)
        if choice == "Play":
            while True:
                score = play_game(screen, clock)
                highscore = save_highscore(score, highscore)
                result = game_over(screen, clock, score, highscore)
                if result == "Play again":
                    continue
                break
        elif choice == "Options":
            sound_enabled = options_menu(screen, clock, sound_enabled)
        else:
            break

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
