from math import e
import random

def sigmoid(x):
   if x > 1000:
      x = 1000
   elif x < -1000:
      x = -1000
   return (e ** (3*x)) / (1 + e ** (3*x))

def reLU(x):
   if x < 0:
      return 0
   else:
      return x

class Neuron:

   staticID = 0
   DEFAULT_WEIGHT = 1

   def __init__(self, value = 0, bias = 0, layerID = -1):
      self.value = value
      self.bias = bias
      self.inputConnections = [] #[[Neuron_0,weight_0], [Neuron_1, weight_1], ...]
      self.inputCount = 0
      self.layerID = layerID
      self.ID = Neuron.staticID
      Neuron.staticID += 1

   def getCopy(self):
      output = Neuron(self.value,self.bias)
      return output

   def copyWeights(self, otherNeuron):
      for c in range(len(self.inputConnections)):
         self.setWeight(c,otherNeuron.getWeight(c))

   def calculate(self):
      if(len(self.inputConnections) > 0):
         self.value = 0
         for c in self.inputConnections:
            self.value += c[0].value * c[1]
         self.value += self.bias
         self.value = reLU(self.value/2)
         # self.value = sigmoid(self.value)
      return self.value

   def setWeight(self, connectionID, newWeight):
      self.inputConnections[connectionID][1] = newWeight

   def setWeights(self, weights: list):
      for i in range(len(weights)):
         self.setWeight(i,weights[i])

   def initWeights(self, value = DEFAULT_WEIGHT):
      for c in self.inputConnections:
         c[1] = value

   def adjustWeight(self, connectionID, amount):
      self.setWeight(connectionID,self.getWeight(connectionID) + amount)

   def adjustWeights(self, weights: list):
      for i in range(0,len(weights)):
         self.adjustWeight(i,weights[i])

   def getWeight(self, connectionID):
      return self.inputConnections[connectionID][1]

   def getWeights(self):
      output = []
      for c in self.inputConnections:
         output.append(c[1])
      return output

   def getConnectedNeuron(self, connectionID):
      return self.inputConnections[connectionID][0]

   def randomizeWeights(self, seed = 0):
      for c in self.inputConnections:
         c[1] = random.uniform(-1,1)

   def getBias(self):
      return self.bias

   def setBias(self, newBias):
      self.bias = newBias
      if(self.bias < -1):
         self.bias = -1
      elif(self.bias > 1):
         self.bias = 1

   def adjustBias(self, amount):
      self.setBias(self.bias + amount)

   # Toggle-able randomized weights is mostly a debug feature. Could be useful though
   def connectTo(self, neurons: list, randomWeights: bool = False):
      for n in neurons:
         if randomWeights:
            self.inputConnections.append([n,random.uniform(-1,1)])
         else:
            self.inputConnections.append([n,Neuron.DEFAULT_WEIGHT])
         self.inputCount += 1

   def display(self):
      print("=> ID: %3d   Value: %.5f   Bias: %.3f" % (self.ID, self.value, self.bias))
      for i in range(0,len(self.inputConnections)):
         c = self.inputConnections[i]
         print("ID: %3d   Weight: %.5f   Value: %.5f   Bias: %.3f" % \
            (c[0].ID, c[1], c[0].value, c[0].bias))