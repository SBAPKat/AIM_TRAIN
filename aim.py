import os, pygame
import time
from pygame.locals import *
from random import randrange

def image_load(name):
    arbo = os.path.join("data", name) + ".bmp"
    image = pygame.image.load(arbo).convert()
    colorkey = image.get_at((1, 0))
    image.set_colorkey(colorkey)
    return image

class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dict = {}
        for i in range(0, 5):
            self.dict["crosshair" + str(i)] = image_load("crosshair_" + str(i))
        self.image = self.dict.get("crosshair0")
        self.rect = self.image.get_rect()
        self.rect.center = (234, 30)
        self.shooting = 0
        self.animation_count = 0
        self.hitbox = self.rect

    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.rect.center = self.pos
        self.hitbox = self.rect
        if self.shooting and self.animation_count != 4:
            self.animation_count = self.animation_count + 1
        elif self.animation_count == 4:
            self.shooting = 0
            self.animation_count = 0
        self.image = self.dict.get("crosshair" + str(self.animation_count))


    def shoot(self, shot):
        if not self.shooting:
            self.shooting = 1
            return self.hitbox.colliderect(shot.rect)

class Timer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frames = 0
        self.counter_s = 0
        self.pol = pygame.font.Font(os.path.join('data', 'sans.ttf'), 20)
        self.image = self.pol.render('Time:' + str(self.counter_s), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topright = (1000, 0)

    def update(self):
        self.frames += 1
        if self.frames >= 60:
            self.counter_s += 1
            self.image = self.pol.render('Time:' + str(self.counter_s), True, (0, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.topright = (1000, 0)
            self.frames = 0



class Target(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = image_load('target')
        self.rect = self.image.get_rect()
        self.rect.center = (234, 30)
        self.frames = 0

    def move(self):
        self.rect.center = (randrange(0, 950), randrange(0, 550))
        self.frames = 0

    def update(self):
        self.frames += 1



class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pol = pygame.font.Font(os.path.join('data', 'sans.ttf'), 20)
        self.score = 0
        self.image = self.pol.render('score:' + str(self.score), True, (0, 0, 0))
        self.rect = self.image.get_rect()

    def update(self):
        self.image = self.pol.render('score:' + str(self.score), True, (0, 0, 0))

    def add(self):
        self.score += 1 


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption('Shooting')
    pygame.mouse.set_visible(0)

    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare Game Objects
    clock = pygame.time.Clock()
    crosshair = Crosshair()
    target = Target()
    timer = Timer()
    score = Score()
    allsprites = pygame.sprite.RenderPlain((crosshair, score, timer, target))

    # Main Loop
    run = True
    while run:
        clock.tick((60))

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                    if crosshair.shoot(target) == 1:
                        target.move()
                        score.add()

            elif event.type == MOUSEBUTTONUP:
                pass

        if target.frames == 120/(score.score*0.5 + 1):
            target.move()

        allsprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
