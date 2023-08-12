import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

Ancho = 864
Alto = 936           #tamaño de la pantalla
Pantalla = pygame.display.set_mode((Ancho, Alto))
pygame.display.set_caption('Flappy Bird')               
fuente = pygame.font.SysFont('Bauhaus 93', 60)

white = (255, 255, 255) #Defino color

croll_del_suelo = 0                          
velocidad_del_scroll = 4  
volar = False                              #Variables
game_over = False 
tuberias= 150 
freuencia_tube = 1500 #milisegundos
final_del_tube= pygame.time.get_ticks() - freuencia_tube
score = 0
pasar_tube = False 


#cargar images
fondo = pygame.image.load('imagenes/bg.png') 
suelo_img = pygame.image.load('imagenes/suelo.jpg')
boton_img = pygame.image.load('imagenes/restart.png')


def mostrar_text(text, fuente, text_col, x, y):
	img = fuente.render(text, True, text_col)
	Pantalla.blit(img, (x, y))


def reinicio_de_juego():
	tuberias.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(Alto / 2)
	score = 0
	return score



class Pajaro(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.imagenes = []
		self.index = 0
		self.counter = 0
		for num in range(1, 4):
			img = pygame.image.load(f'imagenes/pajaro/bird{num}.png')
			self.imagenes.append(img)
		self.imagen = self.imagenes[self.index]
		self.rect = self.imagen.get_rect()
		self.rect.center = [x, y]
		self.velocidad = 0
		self.clikeado = False

	def Actualizar(self):

		if volar == True:                                 
			self.velocidad += 0.5 
			if self.velocidad > 8:   #gravedad
				self.velo = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.velocidad)

		if game_over == False:
			if pygame.mouse.get_pressed()[0] == 1 and self.clikeado == False:
				self.clikeado = True
				self.velocidad = -10                  # salto
			if pygame.mouse.get_pressed()[0] == 0:
				self.clikeado = False
			self.contador += 1
			flap_cooldown = 5         #contador

			if self.contador > flap_cooldown:
				self.contador = 0
				self.index += 1
				if self.index >= len(self.imagenes):
					self.index = 0
			self.imagen = self.imagenes[self.index]

			self.imagen = pygame.transform.rotate(self.imagenes[self.index], self.velocidad * -2)
		else:                                                       #movimineto del pajaro
			self.image = pygame.transform.rotate(self.imagenes[self.index], -90)

class Tuberias(pygame.sprite.Sprite):
	def __init__(self, x, y, posicion):
		pygame.sprite.Sprite.__init__(self)
		self.imagen = pygame.image.load('img/pipe.png')
		self.rect = self.imagen.get_rect()
		if posicion == 1:                    #posicion 1 es desde arriba
			self.imagen = pygame.transform.flip(self.imagen, False, True)
			self.rect.bottomleft = [x, y - int(tuberias / 2)]
		if posicion == -1:                    #posicion -1 es desde abajo
			self.rect.topleft = [x, y + int(tuberias / 2)]

	def actualizacipn(self):
		self.rect.x -= velocidad_del_scroll
		if self.rect.right < 0:
			self.kill()


class Boton():
	def __init__(self, x, y, imagen):
		self.imagen = imagen
		self.rect = self.imagen.get_rect()
		self.rect.topleft = (x, y)

	def mostrar(self):

		action = False
		mouse = pygame.mouse.get_pos()        #posicion del mouse
		if self.rect.collidepoint(mouse):
			if pygame.mouse.get_pressed()[0] == 1:    #si el mouse esta sobre el boton
				action = True
		Pantalla.blit(self.imagen, (self.rect.x, self.rect.y))

		return action

grupo_del_pajaro = pygame.sprite.Group()
grupo_de_tuberias = pygame.sprite.Group()

flappy = Pajaro(100, int(Alto / 2))

grupo_del_pajaro.add(flappy)

boton = Boton(Ancho // 2 - 50, Alto // 2 - 100, boton_img)

iniciar = True
while iniciar:

	clock.tick(fps)

	Pantalla.blit(fondo, (0,0))
                 
	grupo_del_pajaro.draw(Pantalla)
	grupo_del_pajaro.update()
	grupo_de_tuberias(Pantalla)
	Pantalla.blit(suelo_img, (croll_del_suelo, 768))

	if len(grupo_de_tuberias) > 0:
		if grupo_del_pajaro.sprites()[0].rect.left > grupo_de_tuberias.sprites()[0].rect.left\
			and grupo_del_pajaro.sprites()[0].rect.right < grupo_de_tuberias.sprites()[0].rect.right\
			and pasar_tube == False:             #comprobar puntuacion 0,1,2,etc
			pasar_tube = True
		if pasar_tube == True:
			if grupo_del_pajaro.sprites()[0].rect.left > grupo_de_tuberias.sprites()[0].rect.right:
				score += 1
				pasar_tube = False


	mostrar_text(str(score), fuente, white, int(Ancho / 2), 20)
	if pygame.sprite.groupcollide(grupo_del_pajaro, grupo_de_tuberias, False, False) or flappy.rect.top < 0:
		game_over = True                      #coliciones

	if flappy.rect.bottom >= 768:
		game_over = True               #si toca el suelo
		volar = False


	if game_over == False and volar == True:

		time_now = pygame.time.get_ticks()
		if time_now - final_del_tube > freuencia_tube:
			pipe_height = random.randint(-100, 100)
			btm_pipe = Tuberias(Ancho, int(Alto / 2) + pipe_height, -1)
			top_pipe = Tuberias(Ancho, int(Alto / 2) + pipe_height, 1) #generar nuevas tuberias
			grupo_de_tuberias.add(btm_pipe)
			grupo_de_tuberias.add(top_pipe)
			final_del_tube = time_now

		croll_del_suelo -= velocidad_del_scroll
		if abs(croll_del_suelo) > 35:  #aparicion y movimiento del suelo
			croll_del_suelo = 0

		grupo_de_tuberias.update()

	if game_over == True:
		if boton.draw() == True:
			game_over = False            #verificar si perdiste y reiniciar
			score = reinicio_de_juego()



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			iniciar = False
		if event.type == pygame.MOUSEBUTTONDOWN and volar == False and game_over == False:
			volar = True

	pygame.display.update()

pygame.quit()