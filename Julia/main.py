import numpy as np
import matplotlib.pyplot as plt
import pygame as pg
pg.init()

c = -3/4

def to_str(n):
	if str(n)[0] == "-":
		return str(n)

	else:
		return "+"+str(n)

f1 = lambda x: x**2+c
filename = "julia"+to_str(c)+".jpg"

center = [0, 0]
zoom = 1
n = 32

def f(x, n):
	result = np.zeros(x.shape)

	for i in range(n):
		x = f1(x)

		result[abs(x) > 256] = i
		x[abs(x) > 256] = 0

	return result

def color(array, n):
	result = np.zeros((array.shape[0], array.shape[1], 4))

	for i in range(array.shape[0]):
		for j in range(array.shape[1]):
			result[i, j, 0] = array[i, j]/n/2
			result[i, j, 1] = array[i, j]/n/2
			result[i, j, 2] = array[i, j]/n
			result[i, j, 3] = 1

	return result

def julia(center, zoom, n):
	array_real = np.concatenate((np.linspace(-1/zoom*2+center[0], 1/zoom*2+center[0], 1200).reshape((1200, 1)), np.ones((1200, 1))), axis=1)
	array_imag = np.concatenate((np.ones((600, 1)), np.linspace(-1/zoom+center[1], 1/zoom+center[1], 600, dtype=np.complex64).reshape((600, 1))*1j), axis=1)

	array = np.dot(array_imag, array_real.T)
	array_out = f(array, n)

	result = color(array_out, n)
	plt.imsave(filename, result)
	image = pg.image.load(filename)

	return image

screen = pg.display.set_mode((1200, 600))
pg.display.set_caption("Julia f(x)=x^2"+to_str(c))

image = julia(center, zoom, n)

run = True

while run:
	screen.blit(image, (0, 0))
	pg.display.flip()

	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False

		elif event.type == pg.MOUSEBUTTONUP:
			center = [(event.pos[0]-600)/300/zoom+center[0], (event.pos[1]-300)/300/zoom+center[1]]
			zoom *= 4
			n += 4

			image = julia(center, zoom, n)

pg.quit()