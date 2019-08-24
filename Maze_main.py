#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 10:40:28 2018

@author: user
"""

import sys
import pygame as py
import pygame.locals as p
import random
import time

#Classes ----------------------------------------------------------------------

class Block:
    def __init__(self, pos, dim):
        self.pos = pos
        self.rect = py.Rect(pos, dim)

    def display(self, surface):
        py.draw.rect(surface, (0, 0, 0), self.rect) 

class Maze:
    
    def __init__(self):

        self.length = 10
        self.width = 8
        self.blocksize = 22 #pixels
        self.maze_matrix = [[1,1,1,1,1,1,1,1,1,1],
                            [1,0,0,0,0,0,0,0,0,1],
                            [1,0,0,0,0,0,0,0,0,1],
                            [1,0,1,1,1,1,1,1,0,1],
                            [1,0,1,0,0,0,0,0,0,1],
                            [1,0,1,0,1,1,1,1,0,1],
                            [1,0,0,0,0,0,0,0,0,1],
                            [1,1,1,1,1,1,1,1,1,1]]


    #Read Csv file and turn it into a maze matrix

    def maze_blocks(self):
        
        self.blocks = []
        
        for by in range(self.width):

            for bx in range(self.length):

                if self.maze_matrix[by][bx] == '1':
                #if self.maze_matrix[bx][by] == 1 and (((player1.x - 1) <= bx <= (player1.x + 1) and (player1.y - 1) <= by <= (player1.y + 1)) or \
                #((player2.x - 1) <= bx <= (player2.x + 1) and (player2.y - 1) <= by <= (player2.y + 1))):
                    
                    #Make blocks and display hitbox
                    newblock = Block((bx * self.blocksize, by * self.blocksize), (self.blocksize, self.blocksize))
                    newblock.display(surface)
                    self.blocks.append(newblock)

        return self.blocks
    
    def reader(self, csv_file):
        
        csv = open(csv_file)

        self.maze_matrix = []
        count = 0

        for line in csv:
            row = line.strip().split(',')

            count += 1

            self.maze_matrix.append(row)
            self.length = len(row)

        self.width = count


    def draw(self, surface, block_surf, player1, player2):

        blocks = []

        for by in range(self.width):

            for bx in range(self.length):

                #if self.maze_matrix[by][bx] == '1' and (templist in player1_vision or templist in player2_vision):
                if self.maze_matrix[by][bx] == '1' and (((player1.x - player1.radius) <= bx <= (player1.x + player1.radius) and (player1.y - player1.radius) <= by <= (player1.y + player1.radius)) or \
                ((player2.x - player2.radius) <= bx <= (player2.x + player2.radius) and (player2.y - player2.radius) <= by <= (player2.y + player2.radius))):
                    
                    #display image on top of blocks
                    surface.blit(block_surf,( bx * self.blocksize , by * self.blocksize))
                    
                    #display Players
                    player1.display()
                    player2.display()

        return blocks

class Player():

    def __init__ (self, Maze, surface, image, pos):
        self.x = pos[0]
        self.y = pos[1]

        self.Pixel_pos_x = self.x * Maze.blocksize
        self.Pixel_pos_y = self.y * Maze.blocksize

        self.sprite = py.Rect((self.Pixel_pos_x, self.Pixel_pos_y), (Maze.blocksize, Maze.blocksize))
        self.transition = 22
        
        self.radius = 1
        self.vision = None
        
        self.surface = surface
        self.image = image

    def display(self):
        py.draw.rect(self.surface, (0, 0, 0), self.sprite)
        self.surface.blit(self.image, self.sprite)



    def right(self, blocks):
        self.Pixel_pos_x += self.transition
        self.x += 1
        self.sprite.move_ip(self.transition, 0)
        
        for block in blocks:
            if self.sprite.colliderect(block):
                self.Pixel_pos_x -= self.transition
                self.x -= 1
                self.sprite.move_ip(-self.transition, 0)

    def left(self, blocks):
        self.Pixel_pos_x -= self.transition
        self.x -= 1
        self.sprite.move_ip(-self.transition, 0)
        
        for block in blocks:
            if self.sprite.colliderect(block):
                self.Pixel_pos_x += self.transition
                self.x += 1
                self.sprite.move_ip(self.transition, 0)

    def up(self, blocks):

        self.Pixel_pos_y -= self.transition
        self.y -= 1
        self.sprite.move_ip(0, -self.transition)
        
        for block in blocks:
            if self.sprite.colliderect(block):
                self.Pixel_pos_y += self.transition
                self.y += 1
                self.sprite.move_ip(0, self.transition)
                
    def down(self, blocks):
        self.Pixel_pos_y += self.transition
        self.y += 1
        self.sprite.move_ip(0, self.transition)
        
        for block in blocks:
            if self.sprite.colliderect(block):
                self.Pixel_pos_y -= self.transition
                self.y -= 1
                self.sprite.move_ip(0, -self.transition)

class Power():
	def __init__(self, chart, pow_type):
		# Place in empty initial position
		# Assuming object of class Maze is called chart and chart.maze is the list of lists
		self.x1 = 0
		self.y1 = 0
		while (chart.maze_matrix[self.y1][self.x1] == '1'):

			self.x1 = random.randint(0, chart.length - 1)
			self.y1 = random.randint(0, chart.width - 1)

		self.x2 = self.x1 * chart.blocksize
		self.y2 = self.y1 * chart.blocksize

		self.sprite = py.Rect((self.x2, self.y2), (chart.blocksize,chart.blocksize))
		self.pow_type = pow_type

	def display(self, surface):
		py.draw.rect(surface, (0, 0, 0), self.sprite)
        
#		if self.pow_type == 'speed':
#			speedimg = py.image.load('speed.png').convert_alpha()
#			surface.blit(speedimg, self.sprite)
            
		if self.pow_type == 'attack':
			attackimg = py.image.load('attack.png').convert_alpha()
			surface.blit(attackimg, self.sprite)
            
		if self.pow_type == 'radius':
			radiusimg = py.image.load('radius.png').convert_alpha()
			surface.blit(radiusimg, self.sprite)
            
	def power_up(self, player1, player2):
        
		plist = [player1, player2]
        
		#detecting who received the power
		for player in plist:
			if player.sprite.colliderect(self.sprite):
				p1 = player
			else:
				p2 = player
                
#		if self.pow_type == 'speed':
#			p1.transition += 22
#			sfnt = pwrfont.render('Increased speed!', True, (255, 255, 255))
#			surface.blit(sfnt, self.sprite)

		if self.pow_type == 'attack' and (p2.radius >=1 ):
			#I need to know how to keep this.
			p2.radius -= 1
			

		if self.pow_type == 'radius':
			p1.radius += 1
#Winning condition
class ExitBlock():
	def __init__(self, maze):
		self.img = py.image.load('exit.png').convert()
		self.x = 23
		self.y = 30
		self.x1 = self.x * maze.blocksize
		self.y1 = self.y * maze.blocksize
		self.sprite = py.Rect((self.x1, self.y1), (maze.blocksize, maze.blocksize))
        
	def display(self, surface):
		py.draw.rect(surface, (0, 0, 0), self.sprite)
		surface.blit(self.img, self.sprite)
			

#Classes ----------------------------------------------------------------------

py.init()
surface = py.display.set_mode((990, 682))
py.display.set_caption('Super Maze')

#Images
player1_surf = py.image.load("Player.png").convert()
player2_surf = py.image.load("Player2.png").convert()
block_surf = py.image.load("Block1.png").convert()

#Maze_csv_file
csv_file = "maze-1.csv"

#Maze
maze = Maze()
maze.reader(csv_file)
blocks = maze.maze_blocks()


#Players
player1 = Player(maze, surface, player1_surf, (1, 1))
player2 = Player(maze, surface, player2_surf, (43, 1))
players = [player1, player2]

#Powers
pwrfont = py.font.SysFont('smalle', 14)
pwrlist = []
pwrtype = ['attack', 'radius']
py.time.set_timer(p.USEREVENT, 30000)
attack_pickup_t = 0
attacker = 0
power_grabbed = False
pow_g = ''

#For the first page and the instructions
gametitle = py.image.load('gametitle.png').convert()
instructions = py.image.load('instructions.png').convert()

#The exit
ex = ExitBlock(maze)
ex_t = 0
game_over = False
winner = 0
winfont = py.font.SysFont('smalle', 50)

#First Page Display
while True:
    
	proceed = False
	py.event.pump()
	keys = py.key.get_pressed()
	for event in py.event.get():
		if event.type == py.QUIT:
			py.display.quit()
			sys.exit()
		if event.type == py.KEYDOWN:
			if (keys[py.K_RETURN]):
				proceed = True
	if proceed:
		break
	surface.fill((0, 0, 0))
	surface.blit(gametitle, (0,0))
	py.display.update()

#Instructions display

while True:
    
    proceed = False
    py.event.pump()
    keys = py.key.get_pressed()
    for  event in py.event.get():
        if event.type == py.QUIT:
            py.display.quit()
        if event.type == py.KEYDOWN:
            if keys[py.K_RETURN]:
                proceed = True
    if proceed:
        break
    surface.fill((0, 0, 0))
    surface.blit(instructions, (0,0))
    py.display.update()

#Loop
py.mixer.init()
song = py.mixer.Sound('Mario.wav')
while True:
    #Is the time over yet?
    py.mixer.Sound.play(song, -1)
    timer = int(py.time.get_ticks())
    if attacker and timer - attack_pickup_t >= 10000:
        attack_pickup_t = 0
        if attacker == 1:
            player2.radius += 1
        elif attacker == 2:
            player1.radius += 1
        attacker = 0

    #Keys Pressed
    py.event.pump()
    keys = py.key.get_pressed()

    surface.fill((0, 0, 0))
    maze.draw(surface, block_surf, player1, player2)
    
    for event in py.event.get():

        # Quit game
        if event.type == py.QUIT:
            py.mixer.Sound.stop(song)
            py.display.quit()
            sys.exit()

        #Power spawning
        if event.type == p.USEREVENT:
            ptyp = pwrtype[random.randint(0, 1)]
            power = Power(maze, ptyp)
            pwrlist.append(power)

        #Move player
        if event.type == py.KEYDOWN:
            if (keys[py.K_RIGHT]):
                player1.right(blocks)

            if (keys[py.K_LEFT]):
                player1.left(blocks)

            if (keys[py.K_UP]):
                player1.up(blocks)

            if (keys[py.K_DOWN]):
                player1.down(blocks)

            if (keys[py.K_d]):
                player2.right(blocks)

            if (keys[py.K_a]):
                player2.left(blocks)

            if (keys[py.K_w]):
                player2.up(blocks)

            if (keys[py.K_s]):
                player2.down(blocks)

            if (keys[py.K_ESCAPE]):
                py.mixer.Sound.stop(song)
                py.display.quit()
                sys.exit()

	#Checking if anyone collided with the power
    
    for plyr in range(len(players)):
        
        for pwr in pwrlist:
            
            pwr.display(surface)
            
            if players[plyr].sprite.colliderect(pwr.sprite):
                pwr.power_up(player1, player2)
                fnt_display_t = py.time.get_ticks()
                power_grabbed = True
                pow_g = pwr
                fnt_display_t = int(py.time.get_ticks())
                if pwr.pow_type == 'attack':
                    attack_pickup_t = int(py.time.get_ticks())
                    attacker = plyr + 1
                #image display
                pwrlist.remove(pwr)
                
    #Displaying what the power does
    if power_grabbed:
    	if pow_g.pow_type == 'attack':
    		afnt = pwrfont.render('Radius of oponent decreased!', True, (255, 255, 255))
    		surface.blit(afnt, pow_g.sprite)
    	if pow_g.pow_type == 'radius':
    		rfnt = pwrfont.render('Increased radius of vision!', True, (255, 255, 255))
    		surface.blit(rfnt, pow_g.sprite)
    	current_t = int(py.time.get_ticks())

    	if current_t - fnt_display_t >= 3000:
    		power_grabbed = False
    		pow_g = ''
    #Displaying the exit
    ex.display(surface)
    
    #Checking if anyone has won
    for plyr in range(len(players)):
    	if players[plyr].sprite.colliderect(ex.sprite):
    		ex_t = py.time.get_ticks()
    		winner = plyr + 1
    		game_over = True
            
    #Has anybody won yet
    
    py.display.update()
    
    if game_over:
        py.mixer.Sound.stop(song)
        break
    
winf = winfont.render('Player {0} won!'.format(str(winner)), False, (255, 255, 255))
winpos = py.Rect((445, 330), (300, 50))
        
start = time.time()     
while True:
    
    timer = time.time()
    print(timer, start)
    if (timer - start) > 5:
        py.display.quit()
        sys.exit()
        break
    
    else:
        surface.blit(winf, winpos)
        py.display.update()