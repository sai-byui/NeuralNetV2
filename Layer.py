from Neuron import Neuron

import random

class Layer:

   staticID = 0
   DEFAULT_WEIGHT = 1

   def __init__(self, neurons: list, networkID = -1):

      for n in neurons:
         n.layerID = Layer.staticID

      self.ID = Layer.staticID
      self.neurons = neurons
      self.size = len(neurons)
      self.networkID = networkID
      Layer.staticID += 1

   def getCopy(self):
      neurons = []
      temp = Neuron.staticID
      Neuron.staticID = 0
      for n in self.neurons:
         neurons.append(n.getCopy())
      output = Layer(neurons)
      Neuron.staticID = temp
      return output

   # Connect one layer to another.
   def connectTo(self, layer, randomizeWeights: bool = False):
      for n in self.neurons:
         n.connectTo(layer.neurons, randomizeWeights)

   def display(self):
      print("======================= Layer %d =======================" % (self.ID))
      for n in self.neurons:
         n.display()
         print("----------------                       ----------------")
      print()

   # Calls each neuron's calulate function
   def calculate(self):
      for n in self.neurons:
         n.calculate()

   def setValues(self, values: list):
      for i in range(len(values)):
         self.neurons[i].value = values[i]

   def getValues(self):
      output = []
      for n in self.neurons:
         output.append(n.value)
      return output

   def randomizeWeights(self):
      for n in self.neurons:
         n.randomizeWeights()

   def normalize(self):
      largest = self.getLargest().value
      if abs(largest) > 1:
         for n in self.neurons:
            n.value = n.value/largest

   def getLargest(self):
      large = self.neurons[0]
      for n in self.neurons:
         if abs(n.value) > abs(large.value):
            large = n
      return large

   def getSmallest(self):
      small = self.neurons[0]
      for n in self.neurons:
         if abs(n.value) < abs(small.value):
            small = n
      return small

   def getNeuronById(self, Id):
      for n in self.neurons:
         if n.ID == Id:
            return n
      return None

   @staticmethod
   def create(size):
      neurons = []
      temp = Neuron.staticID
      Neuron.staticID = 0
      Neuron.DEFAULT_WEIGHT = Layer.DEFAULT_WEIGHT
      for i in range(0,size):
         neurons.append(Neuron())
      output = Layer(neurons)
      for n in output.neurons:
         n.layerID = output.ID
      Neuron.staticID = temp
      return output
      