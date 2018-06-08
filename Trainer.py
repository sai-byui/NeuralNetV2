from Network import Network
from TrainingData import TrainingData, DataPoint

import random
from math import sqrt

class Trainer:
   def __init__(self, network, training_data, testing_data = TrainingData()):
      self.network = network
      self.training_data = training_data
      self.testing_data = testing_data
      self.iteration_count = 0
      self.error = 10

   def getCopy(self):
      output = Trainer(self.network.getCopy(),self.training_data.getCopy(),self.testing_data.getCopy())
      output.error = self.error
      output.iteration_count = self.iteration_count
      return output

   def calculate_error(self, testing = False):
      error = 0
      if testing:
         data = self.testing_data
      else:
         data = self.training_data
      for testCase in range(data.size):
         data_point = data.data_points_list[testCase]

         # If the input or output sizes of the network and data don't match up
         if len(data_point.expected) != self.network.outputs.size \
         or len(data_point.inputs) != self.network.inputs.size:
            raise Exception("Incompatible DataPoint/Network pair.")

         self.network.setInputs(data_point.inputs)
         self.network.update()
         for i, output in enumerate(self.network.outputs.getValues()):
            error += (output - data_point.expected[i]) ** 2
      return sqrt(error)

   def reset(self):
      self.iteration_count = 0
      self.network.randomize()
      self.error = 10

   def step(self):
      self.iteration_count += 1



class Particle_Swarm(Trainer):
   def __init__(self, particle_count, network, training_data, testing_data = TrainingData()):
      super(Particle_Swarm,self).__init__(network,training_data,testing_data)
      self.num_dimensions = self.network.get_dimension_count()
      self.group = []
      self.group_best = []

      for i in range(particle_count):
         self.group.append(Particle(self.num_dimensions))

      for i in range(self.num_dimensions):
         self.group_best.append(self.group[0].best_position[i])

   def cost_func(self, position):
      self.network.set_weights_and_biases_from_swarm_particle_position(position)
      return self.calculate_error()

   def reset(self):
      super(Particle_Swarm,self).reset()
      for p in self.group:
         p.reset()
      self.group_best = list(self.group[0].position)

   def step(self):
      super(Particle_Swarm,self).step()
      for p in self.group:
         p.error = self.cost_func(p.position)
         p.update(self.group_best)
         if p.best_error < self.error:
            self.group_best = list(p.best_position)
            self.error = p.best_error
      Particle.T += 0.1

class Particle:

   I = 0.6   # Inertial constant
   C_COG = 1 # Cognitive constant
   C_SOC = 2 # Social constant
   T = 1
   V_INIT = 1

   def __init__(self, dimension_count):
      self.num_dimensions = dimension_count
      self.position = []
      self.velocity = []
      self.best_position = []
      self.error = -1
      self.best_error = -1

      for i in range(dimension_count):
         self.velocity.append(random.uniform(-Particle.V_INIT,Particle.V_INIT))
         self.position.append(random.uniform(-10,10))
         self.best_position.append(self.position[i])

   def reset(self):
      self.error = -1
      self.best_error = -1
      for i in range(self.num_dimensions):
         self.velocity[i]=random.uniform(-Particle.V_INIT,Particle.V_INIT)
         self.position[i]=random.uniform(-10,10)
         self.best_position[i]=self.position[i]

   def update(self, group_best):
      self.update_velocity(group_best)
      self.update_position()

      if self.error < self.best_error or self.best_error == -1:
         self.best_position = list(self.position)
         self.best_error = self.error      

   def update_position(self):
      for i in range(self.num_dimensions):
         self.position[i] += self.velocity[i]

   def update_velocity(self, group_best):
      for i in range(self.num_dimensions):
         r_cog = random.uniform(0,1)
         r_soc = random.uniform(0,1)

         vel_cog = Particle.C_COG * r_cog * (self.best_position[i] - self.position[i])
         vel_soc = Particle.C_SOC * r_soc * (group_best[i] - self.position[i])

         self.velocity[i] = (self.I * self.velocity[i] + vel_cog + vel_soc)/Particle.T


class GeneticTrainer(Trainer):
   def __init__(self, network, training_data, testing_data = TrainingData()):
      super(GeneticTrainer,self).__init__(network,training_data,testing_data)

   # Randomizes a random weight. If it doesn't decrease the error, reverts is and
   # and randomizes a random bias. If that doesn't work, it reverts
   def step(self):
      modifier = max(self.error,1)

      self.error = self.calculate_error()
      success = False
      revert1 = self.network.changeRandomWeight(modifier)
      error2 = self.calculate_error()
      if error2 <= self.error:
         success = True
      else:
         self.network.revertWeight(revert1)

      self.error = self.calculate_error()
      revert2 = self.network.changeRandomBias(modifier)
      error2 = self.calculate_error()
      if error2 <= self.error:
         success = True
      else:
         self.network.revertBias(revert2)

      self.error = self.calculate_error()
      revert1 = self.network.adjustRandomWeight(modifier)
      error2 = self.calculate_error()
      if error2 <= self.error:
         success = True
      else:
         self.network.revertWeight(revert1)

      self.error = self.calculate_error()
      revert2 = self.network.adjustRandomBias(modifier)
      error2 = self.calculate_error()
      if error2 <= self.error:
         success = True
      else:
         self.network.revertBias(revert2)
      
      if success:
         self.iteration_count += 1
      return success