from pygame import *
font.init()
mixer.init()
from random import randint
import pyautogui

myScreenshot = pyautogui.screenshot()
myScreenshot.save(r'phase_2_background.png')
window = display.set_mode((0, 0), RESIZABLE)
display.set_caption("Space_cleaner")
display.update()
background = transform.scale(image.load('phase_2_background.png'), (1928, 1080))

is_playing = True
phase_1 = True
clock = time.Clock()
FPS = 30
main_score = 0
trashes_file = ['Trash_1.png', 'Trash_2.png', 'Trash_3.png', 'Trash_4.png', 'Trash_5.png', 'Trash_6.png', 'Trash_7.png', 'Trash_8.png']


class GameSprite(sprite.Sprite):
	def __init__(self, x, y, image_name, speed, width, height):
		super().__init__()
		self.width = width
		self.height = height
		self.image = transform.scale(image.load(image_name), (self.width, self.height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.speed = speed

	def show_sprite(self):
		window.blit(self.image, (self.rect.x, self.rect.y))


close_window_symbol = GameSprite(1373, 405, 'krest 1.png', 0, 32, 32)
font = font.Font(None, 35)
fake_window = GameSprite(420, 400, 'phase_1_background.png', 0, 1000, 300)


class Player(GameSprite):
	def __init__(self, x, y, image_name, speed, width, height, fuel):
		super().__init__(x, y, image_name, speed, width, height)
		self.width = width
		self.height = height
		self.image = transform.scale(image.load(image_name), (self.width, self.height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.speed = speed
		self.fuel = fuel
	def update(self):
		keys_pressed = key.get_pressed()
		if is_playing:
			if phase_1:
				if keys_pressed[K_UP] and self.rect.y > 440:
					self.rect.y -= self.speed
					self.fuel -= 0.001
				if keys_pressed[K_DOWN] and self.rect.y < 660:
					self.rect.y += self.speed
					self.fuel -= 0.001
				if keys_pressed[K_LEFT] and self.rect.x > 430:
					self.rect.x -= self.speed
					self.fuel -= 0.001
				if keys_pressed[K_RIGHT] and self.rect.x < 1370:
					self.rect.x += self.speed
					self.fuel -= 0.001
			else:
				if keys_pressed[K_UP] and self.rect.y > 0:
					self.rect.y -= self.speed
					self.fuel -= 0.001
				if keys_pressed[K_DOWN] and self.rect.y < 1080:
					self.rect.y += self.speed
					self.fuel -= 0.001
				if keys_pressed[K_LEFT] and self.rect.x > 0:
					self.rect.x -= self.speed
					self.fuel -= 0.001
				if keys_pressed[K_RIGHT] and self.rect.x < 1928:
					self.rect.x += self.speed
					self.fuel -= 0.001
		self.show_sprite()


class Trash(GameSprite):
	def update(self, player):
		global main_score, is_playing, phase_1, trashes_file
		if self.rect.colliderect(player):
			main_score += 1
			if ship.fuel <= 1:
				ship.fuel += 0.1
			self.speed = randint(2, 10)
			if phase_1:
				self.rect.x = 420
			else:
				self.rect.x = randint(-150, 0)
			self.image = transform.scale(image.load(trashes_file[randint(0, 7)]), (self.width, self.height))
			if phase_1:
				self.rect.y = randint(440, 660)
			else:
				self.rect.y = randint(0, 800)
		self.show_sprite()
		if phase_1:
			if self.rect.x >= 1000:
				player.fuel -= 10
				self.rect.x = 420
				self.rect.y = randint(470, 660)
		else:
			if self.rect.x >= 1920:
				player.fuel -= 0.5
				self.rect.x = randint(-100, 0)
				self.rect.y = randint(0, 800)
		self.rect.x += self.speed


class Meteor(GameSprite):
	def update(self, player):
		global is_playing
		self.show_sprite()
		reset = False
		if self.rect.colliderect(player):
			ship.fuel -= 0.3
			reset = True
		if phase_1:
			if self.rect.x >= 1420 or reset:
				self.rect.x = 420
				self.rect.y = randint(470, 660)
		else:
			if self.rect.x >= 1920 or reset:
				self.rect.x = randint(-100, 0)
				self.rect.y = randint(0, 800)
		self.rect.x += self.speed


ship = Player(900, 570, 'Ship.png', 12, 80, 40, 1)

fuel_bar_indicator = GameSprite(1290, 660, 'fuel_bar.png', 0, 124, 20)
fuel_bar = GameSprite(1310, 662, 'green_fuel.png', 0, 100 * ship.fuel, 15)

rubbish = sprite.Group()
for i in range(4):
	trash = Trash(420, randint(400, 660), trashes_file[randint(0, 5)], randint(2, 7), 120, 60)
	rubbish.add(trash)

meteor = Meteor(420, randint(400, 660), 'Meteorit.png', randint(2, 10), 50, 50)
asteroids_phase_2 = sprite.Group()
for i in range(5):
	meteor_2 = Meteor(randint(-150, 0), randint(0, 1080), 'Meteorit.png', randint(4, 10), 50, 50)
	asteroids_phase_2.add(meteor_2)

def Phase_2():
	global window, background, phase_1, ship
	window.blit(background, (0, 0))
	display.update()
	myScreenshot = pyautogui.screenshot()
	myScreenshot.save(r'phase_2_background.png')
	window = display.set_mode((0, 0), RESIZABLE)
	background = transform.scale(image.load('phase_2_background.png'), (1920, 1080))
	phase_1 = False
	ship.speed = 16

while is_playing:
	if main_score < 20:
		score = font.render(('Score:' + str(main_score)), True, (255, 255, 255))
	elif main_score < 50:
		score = font.render(('Score:' + str(main_score)), True, (255, 100, 100))
	elif main_score < 100:
		score = font.render(('SCORE:' + str(main_score)), True, (255, 50, 50))
	else:
		score = font.render(('SCORE:' + str(main_score)), True, (255, 0, 0))


	for e in event.get():
		if e.type == QUIT or (mouse.get_pressed()[0] and close_window_symbol.rect.collidepoint(mouse.get_pos())) or ship.fuel <= 0:
			is_playing = False
	window.blit(background, (0, 0))
	if phase_1 and main_score > 15:
		Phase_2()
	fake_window.show_sprite()
	window.blit(score, (420, 440))

	fuel_bar = GameSprite(1310, 662, 'green_fuel.png', 0, 100 * ship.fuel, 15)
	fuel_bar.show_sprite()
	fuel_bar_indicator.show_sprite()

	rubbish.update(ship)
	meteor.update(ship)

	if not phase_1:
		asteroids_phase_2.update(ship)
		if ship.speed < 20:
			ship.speed = main_score
	ship.update()
	clock.tick(FPS)
	display.update()
