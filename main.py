import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')


font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)

#Variables
scroll_del_suelo = 0
velocidad_scroll = 4
volar = False
game_over = False
tuberias = 150
frecuencia_de_tube = 1500 #milisegundos (1,5seg)
last_pipe = pygame.time.get_ticks() - frecuencia_de_tube
score = 0
siguiente_tube = False

#cargando las imagenes
fondo = pygame.image.load('imagenes/bg.png')
suelo_img = pygame.image.load('imagenes/suelo.jpg')
button_img = pygame.image.load('imagenes/restart.png')

# La letra del contador
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
#reinicio del juego
def reset_game():
	mov_tuberias.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(screen_height / 2)
	score = 0
	return score
#El pajaro
class Pajaro(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for num in range (1, 4):
			img = pygame.image.load(f"imagenes/pajaro/bird{num}.png")
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.velocidad = 0
		self.clicked = False
	#Movimiento
	def update(self):

		if volar == True:
			#Creo Gravedad
			self.velocidad += 0.5
			if self.velocidad > 8:
				self.velocidad = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.velocidad)

		if game_over == False:
			#Los Saltos
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.velocidad = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False
			
			flap_cooldown = 5
			self.counter += 1
			
			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
				self.image = self.images[self.index]

			#El movimiento de cabesa del pajaro
			self.image = pygame.transform.rotate(self.images[self.index], self.velocidad * -2)
		else:
			self.image = pygame.transform.rotate(self.images[self.index], -90)

#Creo las tuberias
class Tuberias(pygame.sprite.Sprite):

	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("imagenes/tuberia.png")
		self.rect = self.image.get_rect()
		# 1 es arriba
		# -1 es abajo
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(tuberias / 2)]
		elif position == -1:
			self.rect.topleft = [x, y + int(tuberias / 2)]
		#Si choco muero
	def update(self):
		self.rect.x -= velocidad_scroll
		if self.rect.right < 0:
			self.kill()
#El boton para reiniciar
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):
		action = False
		#posicion del mouse
		pos = pygame.mouse.get_pos()
		#Para clikear el boton reinicia el juego
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True
		#La apricion del Boton
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action
#Los sprites
mov_tuberias = pygame.sprite.Group()
mov_pajaro = pygame.sprite.Group()

flappy = Pajaro(100, int(screen_height / 2))

mov_pajaro.add(flappy)
#creo el reset del boton
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

iniciar = True
while iniciar:
	clock.tick(fps)
	#aparece el fondo
	screen.blit(fondo, (0,0))

	mov_tuberias.draw(screen)
	mov_pajaro.draw(screen)
	mov_pajaro.update()

	#aparece el suelo
	screen.blit(suelo_img, (scroll_del_suelo, 768))

	#actualizacion del puntaje 0,1,2,etc
	if len(mov_tuberias) > 0:
		if mov_pajaro.sprites()[0].rect.left > mov_tuberias.sprites()[0].rect.left\
			and mov_pajaro.sprites()[0].rect.right < mov_tuberias.sprites()[0].rect.right\
			and siguiente_tube == False:
			siguiente_tube = True
		if siguiente_tube == True:
			if mov_pajaro.sprites()[0].rect.left > mov_tuberias.sprites()[0].rect.right:
				score += 1
				siguiente_tube = False
	draw_text(str(score), font, white, int(screen_width / 2), 20)

	#las coliciones
	if pygame.sprite.groupcollide(mov_pajaro, mov_tuberias, False, False) or flappy.rect.top < 0:
		game_over = True

	if flappy.rect.bottom >= 768:
		game_over = True
		volar = False


	if volar == True and game_over == False:
		#generacion de nuevas tuberias
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe > frecuencia_de_tube:
			tuberia_height = random.randint(-100, 100)
			btm_pipe = Tuberias(screen_width, int(screen_height / 2) + tuberia_height, -1)
			top_tuberia = Tuberias(screen_width, int(screen_height / 2) + tuberia_height, 1)
			mov_tuberias.add(btm_pipe)
			mov_tuberias.add(top_tuberia)
			last_pipe = time_now

		mov_tuberias.update()

		scroll_del_suelo -= velocidad_scroll
		if abs(scroll_del_suelo) > 35:
			scroll_del_suelo = 0
	
	#Verificacion si perdiste y para reiniciar
	if game_over == True:
		if button.draw():
			game_over = False
			score = reset_game()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			iniciar = False
		if event.type == pygame.MOUSEBUTTONDOWN and volar == False and game_over == False:
			volar = True

	pygame.display.update()

pygame.quit()
