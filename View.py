#! /usr/bin/env python3
import pygame
from Network import sigmoid
import sys


def getGraphic(network):
	r = 20  # Draw radius of a neuron. Everything is scaled to this value
	buff = r + 10  # Give the sides some space
	largest = network.getLargestLayer()

	# Set the surface size to be just big enough for the network
	size = width, height = int((network.size - 1) * (8 * r)) + buff * 2, int((largest.size - 1) * (2.5 * r) + buff * 2)
	surface = pygame.Surface(size, pygame.SRCALPHA)  # <== note: the pygame.SRCALPHA allows for alpha drawing

	# Need to store the starting y-position of current and previous layers... for connections
	offset = 0
	offset2 = 0

	for x in range(len(network.layers)):
		diff = largest.size - network.layers[x].size  # Size difference between the current layer and the largest one
		offset = diff / 2  # Offset for the smaller layers to center them

		for y in range(len(network.layers[x].neurons)):
			# Big long positional maths relating x and y to r
			pos = [int(x * (8 * r) + buff), int((y + offset) * (2.5 * r) + buff)]

			n = network.layers[x].neurons[y]

			for i in range(len(network.layers[x].neurons[y].inputConnections)):
				if x > 0:
					weight = n.getWeight(i)
					n2 = n.getConnectedNeuron(i)
					n2_size = network.layers[n2.layerID].size
					offset2 = (largest.size - n2_size) / 2

					cval = int(sigmoid(weight * 2) * 255)
					alpha = int(abs(2 * sigmoid(weight * 2) - 1) * 255)
					color = pygame.Color(cval, cval, cval)

					pos2 = [int(n2.layerID * (8 * r) + buff), int(((i % n2_size) + offset2) * (2.5 * r) + buff)]

					pygame.draw.line(surface, color, pos, pos2, 1)

	for x in range(len(network.layers)):
		diff = largest.size - network.layers[x].size  # Size difference between the current layer and the largest one
		offset = diff / 2  # Offset for the smaller layers to center them

		for y in range(len(network.layers[x].neurons)):
			# Big long positional maths relating x and y to r
			pos = [int(x * (8 * r) + buff), int((y + offset) * (2.5 * r) + buff)]
			n = network.layers[x].neurons[y]

			cval = int(sigmoid(n.value * 2) * 255)
			color = (cval, cval, cval, int(abs(2 * sigmoid(n.value * 2) - 1) * 255))
			pygame.draw.circle(surface, color, pos, r)
			pygame.draw.circle(surface, (0, 0, 0), pos, r, 2)
	return surface