import sys
import pygame
import random
#Defining the classes and what they do
class Power():
	def __init__(self, chart, pow_type):
		# Place in empty initial position
		# Assuming object of class Maze is called chart and chart.maze is the list of lists
		self.x1  = 0
		self.y1  = 0
		while (chart.maze[self.x1][self.y1] == 1):
			self.x1  = random.randint(0, chart.M-1)
			self.y1  = random.randint(0, chart.N-1)
		self.x2 = self.x1 * chart.blocksize
		self.y2 = self.x1 * chart.blocksize
		self.sprite = pygame.Rect((self.x2, self.y2), (chart.block_size,chart.block_size))
		self.pow_type = pow_type
	def display(self):
		#pygame.draw.rect(surface, (255, 255, 255), self.sprite, 0)
		if self.pow_type == 'speed':
			speedimg = pygame.image.load('speed.png').convert_alpha()
			surface.blit(speedimg, self.x2, self.y2)
		if self.pow_type == 'attack':
			attackimg = pygame.image.load('attack.png').convert_alpha()
			surface.blit(attackimg, self.x2, self.y2)
		if self.pow_type == 'radius':
			radiusimg = pygame.image.load('radius.png').convert_alpha()
			surface.blit(radiusimg, self.x2, self.y2)
	def power_up(self, player1, player2):
		plist = [player1, player2]
		#detecting who received the power
		for i in plist:
			if self.sprite.colliderect(i.rect):
				p1 = i
			else:
				p2 = i
		if self.pow_type == 'speed':
			p1.velocity += 1
			sfnt = pwrfont.render('Increased speed!', True, (255, 255, 255))
			surface.blit(sfnt, (2, 2))
		if self.pow_type == 'attack':
			#I need to know how to keep this.
			p2.radius -= 5
			afnt = pwrfont.render('Radius of oponent decreased!', True, (255, 255, 255))
			surface.blit(afnt, (2, 2))
		if self.pow_type == 'radius':
			p1.radius += 2
			rfnt = pwrfont.render('Increased radius of vision!', True, (255, 255, 255))
			surface.blit(rfnt, (2, 2))
#Main body of the game
#Pre-loop
pygame.init()
surface = pygame.display.set_mode(990, 660)
pwrfont = pygame.font.Sysfont('smalle', 14)
pwrlist = []
pwrtype = ['speed', 'attack', 'radius']
pygame.time.set_timer(USEREVENT+1, 30000)
plyr1 = Player()
plyr2 = Player()
plyrlst = [plyr1, plyr2]
mz = Maze()
#Loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
		if event.type == USEREVENT+1:
			p = random.randint(0, 2)
			ptyp = pwrtype[p]
			pwr = Power(mz, ptyp)
			pwrlist.append(pwr)
	#Checking if anyone collided with the power
	for i in len(range(pwrlist)):
		for j in plyrlst:
			if pwrlist[i].sprite.colliderect(j.sprite):
				pwrlist[i].power_up(plyr1, plyr2)
				pwrlist.pop(i)
		#displaying the image
		pwrlist[i].display()
	pygame.display.update()