#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pygame


# In[1]:


import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set up the display
width = 800
height = 600
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game by Nilanjan')

# Define the clock
clock = pygame.time.Clock()
snake_block = 20  # Increased size for better visibility

# Font styles
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.circle(dis, black, [int(x[0] + snake_block / 2), int(x[1] + snake_block / 2)], int(snake_block / 2))

def draw_food(foodx, foody, size):
    pygame.draw.circle(dis, green, [int(foodx + size / 2), int(foody + size / 2)], int(size / 2))

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(width / 2, height / 2 + y_offset))
    dis.blit(mesg, mesg_rect)

def draw_score(score, highscore):
    score_text = score_font.render(f"Score: {score}", True, white)
    highscore_text = score_font.render(f"Highscore: {highscore}", True, white)
    dis.blit(score_text, [10, 10])
    dis.blit(highscore_text, [width - highscore_text.get_width() - 10, 10])

def select_difficulty():
    difficulty = None
    while difficulty not in ['E', 'N', 'H']:
        dis.fill(blue)
        message("Select Difficulty: E - Easy, N - Normal, H - Hard", white)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    difficulty = 'E'
                elif event.key == pygame.K_n:
                    difficulty = 'N'
                elif event.key == pygame.K_h:
                    difficulty = 'H'
    return difficulty

def pause_menu():
    paused = True
    while paused:
        dis.fill(blue)
        message("Paused", white, -100)
        message("Press R - Resume", white, -50)
        message("Press Q - Quit", white, 0)
        message("Press C - Restart", white, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    return 'restart'
    return 'resume'

def splash_screen():
    splash_running = True
    while splash_running:
        dis.fill(blue)
        # Display ASCII art and text
        ascii_art = [
            " ",
            " ",
            "SNAKE GAME",
            " ",
            " ",
            " ",
            "Developed by Nilanjan Das",
            " ",
            "Press Enter to Start"
        ]

        for i, line in enumerate(ascii_art):
            message(line, white, i * 30 - 150)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    splash_running = False

def gameLoop(highscore):
    game_over = False
    game_close = False
    score = 0

    # Difficulty selection
    difficulty = select_difficulty()
    if difficulty == 'E':
        snake_speed = 5
    elif difficulty == 'N':
        snake_speed = 8
    elif difficulty == 'H':
        snake_speed = 12

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message(f"You Lost! Final Score: {score}", red, -50)
            message("Press Q-Quit or C-Play Again", red, 10)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(highscore)  # Pass highscore to retain it

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_ESCAPE:
                    action = pause_menu()
                    if action == 'restart':
                        gameLoop(highscore)  # Pass highscore to retain it
                        return
                    elif action == 'resume':
                        continue
                    elif action == 'quit':
                        game_over = True

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        draw_food(foodx, foody, snake_block)
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        draw_score(score, highscore)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            score += 10
            if score > highscore:
                highscore = score

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Main execution
splash_screen()
gameLoop(0)  # Start with a highscore of 0


# In[ ]:




