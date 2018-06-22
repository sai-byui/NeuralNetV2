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


   # Particle swarm compatibilty code
   # -------------------------------------------------------------------
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
   #----------------------------------------------------------------------

   # Calls each layer's calculate function
   def update(self):
      for l in self.layers:
         l.calculate()

   def setInputs(self, values: list):
      self.inputs.setValues(values)

   def getOutputs(self):
      return self.outputs.getValues()

   def randomizeWeights(self):
      for i,l in enumerate(self.layers):
         if i > 0:
            l.randomizeWeights()

   def randomizeBias(self):
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
   # --------------------------------------------------------------
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
   # --------------------------------------------------------

   # Input is based on the output of changeRandomWeight()
   @staticmethod
   def revertWeight(revertList):
      revertList[0].setWeight(revertList[1],revertList[2])

   # Input is based on the output of changeRandomBias()
   @staticmethod
   def revertBias(revertList):
      revertList[0].setBias(revertList[1])

   #---------------------------------------------------------

   def display(self):
      print("#################### Network %d ####################\n" % self.ID)
      for l in self.layers:
         l.display()
      print("####################################################\n")

   def normalize(self):
      largest = self.layers[0].neurons[0].value
      for l in self.layers:
         for n in l.neurons:
            if abs(n.value) > abs(largest):
               largest = n.value
      if abs(largest) > 1:
         for l in self.layers:
            for n in l.neurons:
               n.value /= largest

   def getLargestLayer(self):
      largest = self.layers[0]
      for l in self.layers:
         if l.size > largest.size:
            largest = l
      return largest

   def getLayerByID(self, ID):
      for l in self.layers:
         if l.ID == ID:
            return l
      return None
   # Layer connection code. Some changes may be needed to smooth changing layer connection archetectures
   # ----------------------------------------------------------------------------------------------------
   def connectLayer(self, layerNumber, randomWeights = False):
      if layerNumber > 0:
         # self.layers[layerNumber].connectTo(self.layers[layerNumber - 1],randomWeights)
         for j in range(layerNumber ,0,-1):
            ## Debug
            # print("%d i: %d j: %d" % ((i-j),i,j))
            self.layers[layerNumber].connectTo(self.layers[layerNumber-j], randomWeights)

   @staticmethod
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

   # -----------------------------------------------------------------------------------------------------
   # Returns a fresh network from a list of layer sizes.
   # This is different from the constructor since the constructor takes 
   # -------------------------------------------------
   @staticmethod
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