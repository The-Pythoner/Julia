import numpy as np
import matplotlib.pyplot as plt
import pygame as pg
pg.init()

filename = "julia-0.75.png"
f1 = lambda x: x**2-0.75

zoom_center = [0, 0]
zoom_scale = 4
zoom = 0

def f2(x, n):
	for i in range(n):
		x = f1(x)

		if x.real > 256 or x.imag > 256:
			return i

	return -1

def julia(zoom_center, zoom_scale):
	image = np.zeros((600, 1200, 4))

	for i in range(1200):
		for j in range(600):
			y = f2(i*zoom_scale/1200+zoom_center[0]-zoom_scale/2
			+(j*zoom_scale/1200+zoom_center[1]-zoom_scale/4)*1j, int(32*2**zoom))

			if y == -1:
				image[j, i] = [0, 0, 0, 1]

			else:
				image[j, i] = [y/64/2**zoom, y/64/2**zoom, y/32/2**zoom, 1]

	plt.imsave(filename, image)

	return pg.image.load(filename)

image = julia(zoom_center, zoom_scale)

win = pg.display.set_mode((1200, 600))
pg.display.set_caption("Julia x^2"+filename[5:-4])

run = True

while run:
	win.blit(image, (0, 0))
	pg.display.flip()

	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False

		if event.type == pg.MOUSEBUTTONUP:
			x, y = event.pos

			x /= 1200
			y /= 1200

			x -= 0.5
			y -= 0.25

			x *= zoom_scale
			y *= zoom_scale

			zoom_center = [zoom_center[0]+x, zoom_center[1]+y]

			zoom_scale /= 8
			zoom += 1

			image = julia(zoom_center, zoom_scale)

pg.quit()