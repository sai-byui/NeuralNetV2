from Layer import Layer

from math import e
import random
import sys, pygame

def sigmoid(x):
   return 1 / (1 + e ** (-x))

class Network:

   staticID = 0
   DEFAULT_WEIGHT = 1

   def __init__(self,layers: list):

      for l in layers:
         l.networkID = Network.staticID

      self.layers = layers
      self.size = len(layers)
      self.inputs = layers[0]
      self.outputs = layers[len(layers) - 1]
      self.error = 10
      self.ID = Network.staticID
      Network.staticID += 1

   def getCopy(self):
      layers = []
      temp = Layer.staticID
      Layer.staticID = 0
      for i in range(len(self.layers)):
         layers.append(self.layers[i].getCopy())
         if i > 0: 
            # Connect the previous layers and set the weights so that they match
            # layers[i].connectTo(layers[i-1])
            Network.connectLayerExternal(layers,i)
            for n in range(len(self.layers[i].neurons)):
               layers[i].neurons[n].copyWeights(self.layers[i].neurons[n])

      output = Network(layers)
      output.error = self.error
      Layer.staticID = temp
      return output

   def set_weights_and_biases_from_swarm_particle_position(self, position):
      pos_index = 0
      for l_i,l in enumerate(self.layers):
         for n_i,n in enumerate(l.neurons):
            n.setBias(position[pos_index])
            pos_index += 1
            for c_i in range(n.inputCount):
               n.setWeight(c_i,position[pos_index])
               pos_index += 1

   def get_weights_and_biases_for_swarm_particle_position(self):
      position = []
      for l_i,l in enumerate(self.layers):
         for n_i,n in enumerate(l.neurons):
            position.append(n.getBias())
            for c_i in range(n.inputCount):
               position.append(n.getWeight(c_i))
      return position

   def get_dimension_count(self):
      count = 0
      for l_i,l in enumerate(self.layers):
         for n_i,n in enumerate(l.neurons):
            count += 1
            for c_i in range(n.inputCount):
               count += 1
      return count

   def update(self):
      for l in self.layers:
         l.calculate()
      # self.normalize()

   def setInputs(self, values: list):
      self.inputs.setValues(values)
      # self.inputs.normalize()

   def getOutputs(self):
      return outputs.getValues()

   def randomizeWeights(self):
      for i,l in enumerate(self.layers):
         if i > 0:
            l.randomizeWeights()

   def randomizBias(self):
      for i,l in enumerate(self.layers):
         if i > 0:
            for n in l.neurons:
               n.bias = random.uniform(-1,1)

   def randomize(self):
      for i,l in enumerate(self.layers):
         if i > 0:
            l.randomizeWeights()
            for n in l.neurons:
               n.bias = random.uniform(-1,1)

   # Returns: [reference_to_neuron, weight_index, original_weight] 
   #  in case you need to revert
   def adjustRandomWeight(self, modifier = 1):
      random.seed(random.random())
      l = self.layers[random.randint(1,len(self.layers)-1)]
      n = l.neurons[random.randint(0,len(l.neurons)-1)]
      w_index = random.randint(0,n.inputCount-1)
      temp = [n,w_index,n.getWeight(w_index)]
      n.adjustWeight(w_index, random.uniform(-modifier,modifier))
      return temp

   def adjustRandomBias(self, modifier = 1):
      random.seed(random.random())
      l = self.layers[random.randint(1,len(self.layers)-1)]
      n = l.neurons[random.randint(0,len(l.neurons)-1)]
      w_index = random.randint(0,n.inputCount-1)
      temp = [n,n.bias]
      n.adjustBias(random.uniform(-modifier,modifier))
      return temp

   def changeRandomWeight(self, modifier = 1):
      random.seed(random.random())
      l = self.layers[random.randint(1,len(self.layers)-1)]
      n = l.neurons[random.randint(0,len(l.neurons)-1)]
      w_index = random.randint(0,n.inputCount-1)
      temp = [n,w_index,n.getWeight(w_index)]
      n.setWeight(w_index, random.uniform(-modifier,modifier))
      return temp

   def changeRandomBias(self, modifier = 1):
      random.seed(random.random())
      l = self.layers[random.randint(1,len(self.layers)-1)]
      n = l.neurons[random.randint(0,len(l.neurons)-1)]
      w_index = random.randint(0,n.inputCount-1)
      temp = [n,n.bias]
      n.setBias(random.uniform(-modifier,modifier))
      return temp

   # Input is based on the output of changeRandomWeight()
   def revertWeight(self, revertList):
      revertList[0].setWeight(revertList[1],revertList[2])

   def revertBias(self, revertList):
      revertList[0].setBias(revertList[1])

   def display(self):
      print("#################### Network %d ####################\n" % self.ID)
      for l in self.layers:
         l.display()
      print("####################################################\n")

   def normalize(self):
      largest = self.layers[0].neurons[0].value
      for l in self.layers:
         for n in l.neurons:
            if(abs(n.value) > abs(largest)):
               largest = n.value
      if abs(largest) > 1:
         for l in self.layers:
            for n in l.neurons:
               n.value /= largest

   def getLargestLayer(self):
      largest = self.layers[0]
      for l in self.layers:
         if(l.size > largest.size):
            largest = l
      return largest

   def getLayerByID(self, ID):
      for l in self.layers:
         if l.ID == ID:
            return l
      return None

   def connectLayer(self, layerNumber, randomWeights = False):
      if layerNumber > 0:
         self.layers[layerNumber].connectTo(self.layers[layerNumber - 1],randomWeights)
         # for j in range(layerNumber ,0,-1):
         #    ## Debug
         #    # print("%d i: %d j: %d" % ((i-j),i,j))
         #    self.layers[layerNumber].connectTo(self.layers[layerNumber-j], randomWeights)

   def connectLayerExternal(layerList, layerNumber, randomWeights = False):
      if layerNumber > 0:
         # layerList[layerNumber].connectTo(layerList[layerNumber - 1],randomWeights)
         for j in range(layerNumber ,0,-1):
            ## Debug
            # print("%d i: %d j: %d" % ((i-j),i,j))
            layerList[layerNumber].connectTo(layerList[layerNumber-j], randomWeights)

   def connectLayers(self, randomWeights = False):
      for i in range(len(self.layers)):
         self.connectLayer(i,randomWeights)

   def create(layerSizes: list, randomWeights = False):
      layers = []
      temp = Layer.staticID # We'll store the global ID and set it back later
      Layer.staticID = 0    # so we can set a local ID within a Network
      Layer.DEFAULT_WEIGHT = Network.DEFAULT_WEIGHT
      for i in range(len(layerSizes)):
         layers.append(Layer.create(layerSizes[i]))
         Network.connectLayerExternal(layers,i,randomWeights)
         # if(i > 0):
         #    layers[i].connectTo(layers[i-1], randomWeights)
      output = Network(layers)
      for l in output.layers:
         l.networkID = output.ID
      Layer.staticID = temp
      return output

   def getGraphic(self):
      r = 10 # Draw radius of a neuron. Everything is scaled to this value
      buff = r + 10 # Give the sides some space
      largest = self.getLargestLayer()

      # Set the surface size to be just big enough for the network
      size = width, height = int((self.size-1)*(8*r)) + buff*2, int((largest.size-1)*(2.5*r) + buff*2)
      surface = pygame.Surface(size,pygame.SRCALPHA) #<== note: the pygame.SRCALPHA allows for alpha drawing

      # Need to store the starting y-position of current and previous layers... for connections
      offset = 0
      offset2 = 0

      for x in range(len(self.layers)):
         diff = largest.size - self.layers[x].size # Size difference between the current layer and the largest one
         offset = diff/2                        # Offset for the smaller layers to center them

         for y in range(len(self.layers[x].neurons)):
            # Big long positional maths relating x and y to r
            pos = [int(x*(8*r) + buff),int((y+offset)*(2.5*r) + buff)]

            n = self.layers[x].neurons[y]

            for i in range(len(self.layers[x].neurons[y].inputConnections)):
               if x > 0:
                  weight = n.getWeight(i)
                  n2 = n.getConnectedNeuron(i)
                  n2_size = self.layers[n2.layerID].size
                  offset2 = (largest.size - n2_size) / 2

                  cval = int(sigmoid(weight * 2)*255)
                  alpha = int(abs(2*sigmoid(weight * 2) - 1) * 255)
                  color = pygame.Color(cval,cval,cval)

                  pos2 = [int(n2.layerID*(8*r) + buff),int(((i % n2_size)+offset2)*(2.5*r) + buff)]

                  pygame.draw.line(surface,color,pos,pos2,1)


      for x in range(len(self.layers)):
         diff = largest.size - self.layers[x].size # Size difference between the current layer and the largest one
         offset = diff/2                        # Offset for the smaller layers to center them

         for y in range(len(self.layers[x].neurons)):
            # Big long positional maths relating x and y to r
            pos = [int(x*(8*r) + buff),int((y+offset)*(2.5*r) + buff)]
            n = self.layers[x].neurons[y]

            cval = int(sigmoid(n.value * 2) * 255)
            color = (cval,cval,cval,int(abs(2 * sigmoid(n.value * 2) - 1)*255))
            pygame.draw.circle(surface,color,pos,r)
            pygame.draw.circle(surface,(0,0,0),pos,r,2)
      return surface