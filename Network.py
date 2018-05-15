class Network:
    """Network class. Contains all the code needed to describe a simple feedforward network. 
    Layers, neurons, weights, etc. Contains functions for training the network."""

    def __init__(self, topology):
        # Set the training rate
        # Set the temperature, if we're using simulated annealing
        # Save topology as a member variable, for copying during training
        # Create and populate the the layers of the network
        # Initialize the weights (and biases) in the network
        pass

    def run_network(self, inputs):
        """This function will run the network through a SINGLE set of inputs (one DataPoint object) and return the result"""

        # Run the network LAYER BY LAYER
            # Insert the input data into the respective network inputs
            # Feed forward through the network (input -> layer 0, layer 0 -> layer 2, etc.)

        # Return the values of the output neurons
        pass

    def train_network_gen_alg(self, inputs, expected):
        """There are A LOT of options for implementing a genetic/evolutionary algorithm. Before starting, reasearch
        the following:
        Genetic algorithms. make sure you're familiar with why they are good for finding global minima.
            Also be sure you understand mutation, crossover, the difference between the two, and why both are 
            important. 
        Simulated annealing. Make sure you understand how this adds diversity, and why diversity is important.
        Do we want to include diversity in the fitness function? How do we want to do that?
        How should we handle the training rate - keep it constant, or decrease it as time goes on?
        I'm holding off on writing pseudocode for this until we can discuss these options.
        Here's (basically) how it is implemented in Version 1, if you don't want to change much:"""

        # Run the network, as-is, through each DataPoint, recording all outputs in a 2D list
        # Using this 2D list, and the expected parameter, find the errors and put them in a 2D list
        # Store the original error and original weights in variables
        # Create a population of n individuals (probably > 100)
        # Mutate the other individuals in the population
        # If any mutated individual has a lower error than the original, replace the original weights.
        # Get the new error of the system, and return that error
        pass

    def train_network_backprop(self, inputs, expected):
        """This method uses backpropagation to determine with each iteration how much to change the network's
        weights to minimize error. This will involve some calculus. Before trying to do this, watch all 
        4 videos by 3Blue1Brown at https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi
        Here's (basically) how it is implemented in Version 1, if you don't want to change anything:"""

        # ensure each neuron's backprop variables are reset
        # Initialize error list
        # Populate error list
        # Request from each output neuron that it change its output based on the error
        # perform backpropagation (more detailed pseudocode to come)
        # Get the new error of the system
        # Return that error
        pass

    def train_adversarial(self, fitness_callback):
        """Trains network using evolutionary algorithm and fitness instead of error. 
            Uses a callback so the user can determine how fitness is assigned.
            To be used when it is difficult or impractical to assign precise error
            measurements."""
        # Create new network to be an adversary
        # Make the new network's weights only slightly different from the current network
        # get the fitnesses by calling the fitness_callback with both networks as parameters
        # the fitness should have two numbers - like [2.5, 6.2] - the first for the current network's fitness,
        # the second for the new network. raise exception otherwise.
        # if the new network's fitness is higher, use its weights to replace those of the current network
