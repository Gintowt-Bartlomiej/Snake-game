#!/usr/bin/env python
import pygame, sys, random
from pygame.locals import *
import time
import random
import pygame_menu

SIZE = 40

class SNAKE:
    #initiation of snake class
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen

        #loading blocks (snake body) images
        self.image_head_down = pygame.image.load("Graphics/head down.jpg").convert()
        self.image_head_up = pygame.image.load("Graphics/head up.jpg").convert()
        self.image_head_left = pygame.image.load("Graphics/head left.jpg").convert()
        self.image_head_right = pygame.image.load("Graphics/head right.jpg").convert()
        self.image_body = pygame.image.load("Graphics/block.jpg").convert()
        self.direction = 'down'

        #starting snake base position
        self.length = 1
        self.x = [400]
        self.y = [40]

    #directions to move snake
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_snake(self):
        #update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        #update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw_snake()

    #drawing snake
    def draw_snake(self):
        for i in range(self.length):
            if i == 0:
                #drawing snakes head in particular possitions
                if self.direction == 'left':
                    self.parent_screen.blit(self.image_head_left, (self.x[i], self.y[i]))
                if self.direction == 'right':
                    self.parent_screen.blit(self.image_head_right, (self.x[i], self.y[i]))
                if self.direction == 'up':
                    self.parent_screen.blit(self.image_head_up, (self.x[i], self.y[i]))
                if self.direction == 'down':
                    self.parent_screen.blit(self.image_head_down, (self.x[i], self.y[i]))
            else:
                #drawing snakes body
                self.parent_screen.blit(self.image_body, (self.x[i], self.y[i]))
        pygame.display.flip()

    #increasing lenght of snake
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class FRUIT:
    #initiation of fruit class
    def __init__(self, parent_screen):
        #loading fruit image
        self.parent_screen = parent_screen
        self.image = pygame.image.load("Graphics/apple.jpg").convert()
        self.x = 120
        self.y = 120

    #drawing appel on screen
    def draw_fruit(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    #fruit position on screen
    def randomize(self):
        self.x = random.randint(1,19)*SIZE
        self.y = random.randint(1,19)*SIZE


class MAIN:
    def __init__(self):
        self.surface = pygame.display.set_mode((800, 800))
        self.snake = SNAKE(self.surface)
        self.fruit = FRUIT(self.surface)
        pygame.mixer.init()
        self.play_background_music()

    #loading background music
    def play_background_music(self):
        pygame.mixer.music.load('Music/bg_music.mp3')
        pygame.mixer.music.play(-1, 0)
    
    def reset(self):
        self.snake = SNAKE(self.surface)
        self.apple = FRUIT(self.surface)

    #loading events music
    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("Music/crash.mp3")
        elif sound_name == "eat":
            sound = pygame.mixer.Sound("Music/eat.mp3")

        pygame.mixer.Sound.play(sound)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.collision_with_itself()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False


    def check_collision(self):
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.fruit.x, self.fruit.y):
            self.play_sound("eat")
            self.snake.increase_length()
            self.fruit.randomize()

    def check_fail(self):
        if not (0 <= self.snake.x[0] <= 760 and 0 <= self.snake.y[0] <= 760):
            self.play_sound('crash')
            self.game_over()

    def collision_with_itself(self):
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                self.game_over()

    def game_over(self):
        game_intro()

    def draw_score(self):
        font = pygame.font.SysFont('times new roman',30)
        score = font.render(f"Score: {self.snake.length}",True,(255,255,255))
        self.surface.blit(score,(650,10))


class Button:
    def __init__(self, color,x ,y, width, height, text: str):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw_text(self, screen, outline=None):
        pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4,self.height+4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        text = game_font.render(self.text, True, (0,0,0))
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isover(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos [1] < self.y + self.height:
                return True
        return False


class text:
    pass

pygame.init()
pygame.display.set_caption("Snake game")
PIXEL_SIZE = 40
PIXEL_NUMBER = 20
SCREEN_WIDTH =PIXEL_SIZE*PIXEL_NUMBER
SCREEN_HEIGHT = PIXEL_SIZE*PIXEL_NUMBER
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("times new roman", 25)
display = pygame.Surface((SCREEN_SIZE))
music = pygame.mixer.music.load("Music/Corona.mp3")
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
click = False

btnstart = Button((255, 255, 255), 200, 150, 400, 100, "Start")
btnrules = Button((255,255,255), 200, 300, 400, 100, "Rules")
btnhighscores = Button((255,255,255), 200, 450, 400, 100, "Highscores")
btnquit = Button((255,255,255), 200, 600, 400, 100, "Exit")
btnback = Button((255,255,255), 200, 600, 400, 100, "Back")

def edge():
    screen.fill((101,167,69))
    btnstart.draw_text(screen, (0,0,0))
    btnquit.draw_text(screen, (0,0,0))
    btnrules.draw_text(screen, (0,0,0))
    btnhighscores.draw_text(screen, (0,0,0))


def edge2():
    screen.fill((101,167,69))
    btnback.draw_text(screen, (0,0,0))


def game_intro():
    intro = True
    while intro:
        edge()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnstart.isover(pos):
                    game_loop()
                if btnquit.isover(pos):
                    exit()
                if btnrules.isover(pos):
                    rules()
                if btnhighscores.isover(pos):
                    highscores()

        pygame.display.update()
        clock.tick(60)
        screen.fill((101,167,69))


def exit():
    pygame.quit()
    sys.exit()


def rules():
    rule = True
    while rule:
        edge2()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnback.isover(pos):
                    game_intro()

        pygame.display.update()
        clock.tick(60)
        screen.fill((101,167,69))


def highscores():
    score = True
    while score:
        edge2()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnback.isover(pos):
                    game_intro()

        pygame.display.update()
        clock.tick(60)
        screen.fill((101,167,69))


def game_loop():
    main_game = MAIN()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    main_game.snake.move_left()

                if event.key == K_RIGHT:
                    main_game.snake.move_right()

                if event.key == K_UP:
                    main_game.snake.move_up()

                if event.key == K_DOWN:
                        main_game.snake.move_down()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)
        screen.fill((101,167,69))

game_intro()
