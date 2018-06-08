class Network:
    def __init__(self):
        if self.get_type == NetworkType.Network:
            raise("ERROR: Cannot directly instantiate class Network!")

    def run_network(self, inputs):
        raise("ERROR: Networks of type " + str(self.get_type()) + " have not implemented run_network.")

    def train_network_gen_alg(self, inputs, expected):
        raise ("ERROR: Networks of type " + str(self.get_type()) + " have not implemented train_network_gen_alg.")

    def train_network_backprop(self, inputs, expected):
        raise ("ERROR: Networks of type " + str(self.get_type()) + " have not implemented train_network_backprop.")

    def train_network_adversarial(self, fitness_callback):
        raise ("ERROR: Networks of type " + str(self.get_type()) + " have not implemented train_network_adversarial.")