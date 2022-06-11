import pygame
import pygame.freetype
import sys
import time
import random

pygame.init()

# Global settings
screen_width = 500
screen_height = 500
pygame.display.set_caption("Classic Snake Game")
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

segment_width = 20
segement_height = 20
segment_seperation = 3

font = pygame.freetype.SysFont('timesnewroman',  24, bold = True)


class segment(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        self.direction_x = 0
        self.direction_y = 0

        self.image = pygame.Surface([segment_width,segement_height])

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y


class point(pygame.sprite.Sprite):
    def __init__(self,timer):
        super().__init__()

        self.image = pygame.Surface([15, 15])
        self.rect = self.image.get_rect()
        self.timer = timer
        self.timer_orig = self.timer
        self.rect.x, self.rect.y = random.randint(0, 750), random.randint(0, 750)

    def update(self):
        if self.timer > 0:
            self.timer -= 1

        else:
            x = random.randint(30, screen_width-45)
            y = random.randint(30, screen_height-45)
            self.rect.x, self.rect.y = x,y
            self.timer = self.timer_orig


point = point(60)
all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(point)
snake_segments = []
snake_segments.append(segment(300,300))

def length(score):
    for i in range(1,score):
        x = 300 - (segment_width + segment_seperation) * i
        y = 300
        segments = segment(x, y)
        snake_segments.append(segments)
        all_sprites_list.add(segments)


def main():
    score = 0
    x_direction = (segment_width + segment_seperation)
    y_direction = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                print("GAME OVER")

            elif event.type == pygame.KEYDOWN:

                # Controls Snake Direction using Arrow Keys or WASD
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and x_direction == 0:
                    x_direction = (segment_width + segment_seperation)*1
                    y_direction = 0


                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and x_direction == 0:
                    x_direction = (segment_width + segment_seperation) * -1
                    y_direction = 0


                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and y_direction == 0:
                    x_direction = 0
                    y_direction = (segment_width + segment_seperation) * 1


                if (event.key == pygame.K_UP or event.key == pygame.K_w) and y_direction == 0:
                    x_direction = 0
                    y_direction = (segment_width + segment_seperation) * -1


        #Snake movement
        x = snake_segments[0].rect.x + x_direction
        y = snake_segments[0].rect.y + y_direction
        new_segment = segment(x,y)

        last_segment = snake_segments.pop()
        all_sprites_list.remove(last_segment)

        snake_segments.insert(0,new_segment)
        all_sprites_list.add(new_segment)

        # Updates Point and Snake position, draws them at new position then clears the screen for the next set of drawings
        point.update()
        screen.fill((255,255,255),[15,15,screen_width-30,screen_height-30])
        all_sprites_list.draw(screen)
        font.render_to(screen, (screen_width-50,screen_height-50), f"{score}", (0, 0, 0))
        pygame.display.flip()

        # Checks for Snake collision with point
        if pygame.sprite.collide_rect(point,snake_segments[0]):
            point.timer = 0
            score += 1
            length(2)

        # Checks for Snake collision with itself
        for n in range(1,score):
            if pygame.sprite.collide_rect(snake_segments[0],snake_segments[n]):
                sys.exit()

        # Checks for Snake collision with the border
        if snake_segments[0].rect.x <= 15 or snake_segments[0].rect.x >= screen_width-30:
            sys.exit()


        if snake_segments[0].rect.y <= 15 or snake_segments[0].rect.y >= screen_height-30:
            sys.exit()

        clock.tick(15)  # Sets game to 15 fps

main()
