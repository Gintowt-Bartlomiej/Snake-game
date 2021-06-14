#!/usr/bin/env python
import pygame
from pygame.locals import *
import time
import random
import pygame_menu


SIZE = 40

#-------------------------
# Snake class
#-------------------------
class Snake:
    #initiation of snake class
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen

        #loading blocks (snake body) images
        self.image_head_down = pygame.image.load("head down.jpg").convert()
        self.image_head_up = pygame.image.load("head up.jpg").convert()
        self.image_head_left = pygame.image.load("head left.jpg").convert()
        self.image_head_right = pygame.image.load("head right.jpg").convert()
        self.image_body = pygame.image.load("block.jpg").convert()
        self.direction = 'down'

        #starting apple position
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

    def walk(self):
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

        self.draw()

    #drawing snake
    def draw(self):
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

#-------------------------
# Apple class
#-------------------------
class Apple:
    #initiation of apple class
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        #loading apple image
        self.image = pygame.image.load("apple.jpg").convert()
        self.x = 120
        self.y = 120

    #drawing appel on screen
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    #apple position on screen
    def move(self):
        self.x = random.randint(1,19)*SIZE
        self.y = random.randint(1,14)*SIZE

#-------------------------
# Game class
#-------------------------
class Game:
    #initiation of game class
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake game")

        #music initiation
        pygame.mixer.init()
        self.play_background_music()

        #game window size
        self.surface = pygame.display.set_mode((800, 600))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    #loading background music
    def play_background_music(self):
        pygame.mixer.music.load('bg_music.mp3')
        pygame.mixer.music.play(-1, 0)

    #loading events music
    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("crash.mp3")
        elif sound_name == "eat":
            sound = pygame.mixer.Sound("eat.mp3")

        pygame.mixer.Sound.play(sound)

    #reseting
    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    #snake collision
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    #setting background graphic
    def render_background(self):
        bg = pygame.image.load("background.jpg")
        self.surface.blit(bg, (0,0))


    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        self.high_score()
        pygame.display.flip()

        #snake eating apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("eat")
            self.snake.increase_length()
            self.apple.move()

        #snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

        #snake colliding with the bounderies of the window
        if not (0 <= self.snake.x[0] <= 760 and 0 <= self.snake.y[0] <= 560):
            self.play_sound('crash')
            raise "Hit the boundry error"

    #score function
    def display_score(self):
        font = pygame.font.SysFont('times new roman',30)
        score = font.render(f"Score: {self.snake.length}",True,(255,255,255))
        self.surface.blit(score,(650,10))
        
    #hight score function
    def high_score(self):
        font = pygame.font.SysFont('times new roman',30)
        score = font.render(f"High score: {40}",True,(255,255,255))
        self.surface.blit(score,(35,10))

    #game over function, ending screen
    def show_game_over(self):
        self.render_background()
        self.image3 = pygame.image.load("snake dead.jpg").convert()
        self.surface.blit(self.image3, (500, 150))
        font = pygame.font.SysFont('times new roman', 30)
        line1 = font.render(f"You died!", True, (255, 0, 0))
        self.surface.blit(line1, (130, 190))
        line2 = font.render(f"Your score is: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line2, (130, 230))
        line3 = font.render("To play again press Enter.", True, (255, 255, 255))
        self.surface.blit(line3, (130, 270))
        line4 = font.render("To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line4, (130, 310))
        pygame.mixer.music.pause()
        pygame.display.flip()

    #event checking
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #exit and play again events
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    #snake controls
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            #showing game over screen
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.25)

if __name__ == '__main__':
    #running the game
    game = Game()
    game.run()
