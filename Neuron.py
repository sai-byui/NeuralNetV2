class Neuron:
    def __init__(self):
        # Initialize weights, inputs, and output to none
        # Initialize various backpropagation variables
        pass

    def enqueue(self, input_amt):
        # Append the input to the inputs list
        pass

    def calc_output(self):
        # set total = 0
        # add each input to the total, keeping track of the number of inputs
        # clear self.inputs
        # Calculate the output
        # set self.num_runs += 1, keep track of how many times the neuron has been run
        # Set self.total_output += self.output, keep track of the total amount of output the neuron has given
        # Set self.average_output, needed for backprop calculus
        # set self.average_input, also needed
        pass

    def reset_backprop_vars(self):
        """Reset the various backprop vars, for a fresh training run."""
        pass

    def request_delta(self, delta):
        """Requested from the network that this neuron change its output by a certain amount.
                Requests are averaged, calculus is applied outside this function, etc."""
        # Set self.total_requested_delta += delta
        # Set self.num_requests += 1
        # Set self.average_requested_delta
