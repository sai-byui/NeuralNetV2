#! /usr/bin/env python3
from Layer import Layer
from Network import Network
from TrainingData import TrainingData, DataPoint
from Trainer import Particle_Swarm, GeneticTrainer
import DataSets
from View import getGraphic

import random
import sys, pygame
import time


VERBOSE_ERROR = True

random.seed(time.time())

##############################################
# Network Setup #
#===============#

Network.DEFAULT_WEIGHT = 0

learnDecode = Network.create([1,6,6,11,11])
learnDecode.update()

learnTruth = Network.create([4,8,8,4])
learnTruth.update()

learnAdd = Network.create([2,4,4,4,4,1])
learnAdd.update()

# network2 = network1.getReverse()
# network2.display()

#============================================#


##############################################
# Training Data #
#===============#

# Broke out DataSets into a different file to allow easy swapping of data sets

truth_table, truth_table_testing = DataSets.and_or_nand_xor()

decoder, decoder_testing = DataSets.decoder()

adder, adder_testing = DataSets.adding()

# trainer = Particle_Swarm(10, learnTruth, truth_table,truth_table_testing)
trainer = GeneticTrainer(learnTruth,truth_table,truth_table_testing)

#=============================================#

##############################################
# Pygame Graphics :D #
#====================#


# Initialize
#=============
pygame.init()

graphic = getGraphic(trainer.network)
size = width, height = graphic.get_width(), graphic.get_height()

background_img = pygame.image.load("Recources/61581d98e54acca.jpg")
back_surface = pygame.Surface(size)

#-------------------------------------------------------------------------------
# Tile the background image so it will always be there ... watching... waiting |
# ... no matter how big you make your window.                                  |
#-------------------------------------------------------------------------------
i = 0
while background_img.get_height() * i < height:
   j = 0
   while background_img.get_width() * j < width:
      back_surface.blit(background_img,[0,i*background_img.get_height()])
      j += 1
   i += 1
#-------------------------------------------

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

t = 0

input_toggle = True
untrained_toggle = False
tCase = 0

done = False

# Loop
#==============================================
while 1:
   for event in pygame.event.get():
      if event.type == pygame.QUIT: 
         sys.exit()
      elif event.type == pygame.KEYDOWN:
         if event.key == pygame.K_i:
            tCase += 1
         elif event.key == pygame.K_d:
            trainer.network.display()
         elif event.key == pygame.K_t:
            untrained_toggle = not untrained_toggle
            if untrained_toggle:
               print("Testing untrained data...")
               print(trainer.calculate_error(True))
            else:
               print("No longer testing untrained data")
         elif event.key == pygame.K_r:
            trainer.reset()
         elif event.key == pygame.K_SPACE:
            input_toggle = not input_toggle

   clock.tick(120)
   t += 1

   if untrained_toggle and trainer.testing_data.size > 0:
      network_in = trainer.testing_data.get_inputs()[tCase % trainer.testing_data.size]
   elif trainer.training_data.size > 0:
      network_in = trainer.training_data.get_inputs()[tCase % trainer.training_data.size]
   else:
      if untrained_toggle:
         raise Exception("testing_data is size zero")
      else:
         raise Exception("training_data is size zero")

   if input_toggle:
      trainer.network.setInputs(network_in)
      trainer.network.update()
      graphic = getGraphic(trainer.network)
   else: # Let's just see what it's up to
      graphic = getGraphic(trainer.network)

   screen.blit(back_surface,[0,0])
   screen.blit(graphic,[0,0])
   pygame.display.flip()

   if trainer.error >= 0.0001: 

      if VERBOSE_ERROR:
         if not(t % 80) and not untrained_toggle :
            print()
            print(str(trainer.network.ID) + ":" + str(trainer.error))
         sys.stdout.write('.')
         sys.stdout.flush()

      trainer.step()

   elif not done:
      print(trainer.iteration_count)
      done = True