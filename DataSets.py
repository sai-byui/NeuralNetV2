from TrainingData import TrainingData, DataPoint
import time
import random



def adding():
	# Adds two random numbers together

	random.seed(time.time())

	adder = TrainingData()
	adder_testing = TrainingData()

	for i in range(100):
		a = random.random()
		b = random.random()
		adder.append(DataPoint([a, b], [a + b]))

		a = random.random()
		b = random.random()
		adder_testing.append(DataPoint([a, b], [a + b]))

	# return a tuple of the training data and testing data
	return adder, adder_testing



def subtract():
	# Subtracts two random numbers

	random.seed(time.time())

	subtract_train = TrainingData()
	subtract_test = TrainingData()

	for i in range(100):
		a = random.random()
		b = random.random()
		subtract_train.append(DataPoint([a, b], [a - b]))

		a = random.random()
		b = random.random()
		subtract_test.append(DataPoint([a, b], [a - b]))

	# return a tuple of the training data and testing data
	return subtract_train, subtract_test



def power():
	# Raises one number to the power of another number

	random.seed(time.time())

	power_train = TrainingData()
	power_test = TrainingData()
	
	for i in range(100):
		a = random.random()
		b = random.random()
		power_train.append(DataPoint([a, b], [a ** b]))

		a = random.random()
		b = random.random()
		power_test.append(DataPoint([a, b], [a ** b]))
		
	return power_train, power_test



def average():
	# Raises one number to the power of another number

	random.seed(time.time())

	power_train = TrainingData()
	power_test = TrainingData()

	for i in range(100):
		a = random.random()
		b = random.random()
		power_train.append(DataPoint([a, b], [(a + b) / 2 ]))

		a = random.random()
		b = random.random()
		power_test.append(DataPoint([a, b], [(a + b) / 2]))

	return power_train, power_test



def decoder():
	# Makes a binary decoder of size size

	decoder_training = TrainingData()
	decoder_testing = TrainingData()

	decoder_training.append(DataPoint([0.0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
	decoder_training.append(DataPoint([0.1], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
	decoder_training.append(DataPoint([0.2], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]))
	decoder_training.append(DataPoint([0.3], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]))
	decoder_training.append(DataPoint([0.4], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]))
	decoder_training.append(DataPoint([0.5], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]))
	decoder_training.append(DataPoint([0.6], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]))
	decoder_training.append(DataPoint([0.7], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]))
	decoder_training.append(DataPoint([0.8], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]))
	decoder_training.append(DataPoint([0.9], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]))
	decoder_training.append(DataPoint([1.0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]))

	return decoder_training, decoder_testing



def and_or_nand_xor():
	truth_table = TrainingData()
	truth_table_testing = TrainingData()
	##Inputs: 0 and 1  Expected outputs:and, or, nand, xor
	truth_table.append(DataPoint([0, 0, 0, 0], [0, 0, 1, 0]))
	truth_table.append(DataPoint([0, 0, 0, 1], [0, 1, 1, 1]))
	truth_table.append(DataPoint([0, 0, 1, 0], [0, 1, 1, 1]))
	truth_table.append(DataPoint([0, 0, 1, 1], [0, 1, 1, 0]))
	truth_table.append(DataPoint([0, 1, 0, 0], [0, 1, 1, 1]))
	truth_table.append(DataPoint([0, 1, 0, 1], [0, 1, 1, 0]))
	truth_table.append(DataPoint([0, 1, 1, 0], [0, 1, 1, 0]))
	truth_table.append(DataPoint([0, 1, 1, 1], [0, 1, 1, 1]))
	truth_table.append(DataPoint([1, 0, 0, 0], [0, 1, 1, 1]))
	truth_table.append(DataPoint([1, 0, 0, 1], [0, 1, 1, 0]))
	truth_table.append(DataPoint([1, 0, 1, 0], [0, 1, 1, 0]))
	truth_table.append(DataPoint([1, 0, 1, 1], [0, 1, 1, 1]))
	truth_table.append(DataPoint([1, 1, 0, 0], [0, 1, 1, 0]))
	truth_table.append(DataPoint([1, 1, 0, 1], [0, 1, 1, 1]))
	truth_table.append(DataPoint([1, 1, 1, 0], [0, 1, 1, 1]))
	truth_table.append(DataPoint([1, 1, 1, 1], [1, 1, 0, 0]))

	return truth_table, truth_table_testing

