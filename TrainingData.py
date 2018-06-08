class TrainingData:
    """TrainingData class, used to enable easier input of training and testing data for a neural network"""
    def __init__(self):
        self.data_points_list = []
        self.size = 0

    def append(self, data_point):
        """Adds a DataPoint to the list."""
        if isinstance(data_point, DataPoint):
            self.data_points_list.append(data_point)
            self.size += 1
        else:
            raise Exception("Can only append objects of type DataPoint to TrainingData.")

    def get_inputs(self):
        """Returns only the inputs from each data point."""
        data_inputs = []
        for data_point in self.data_points_list:
            data_inputs.append(data_point.inputs)
        return data_inputs

    def get_expected(self):
        """Returns only the expected output values from each data point."""
        data_expected = []
        for data_point in self.data_points_list:
            data_expected.append(data_point.expected)
        return data_expected

    def getCopy(self):
        output = TrainingData()
        for d in self.data_points_list:
            output.append(d)
        return output


class DataPoint:
    """Simple structure to hold the inputs and associated expected outputs of a single piece of data."""
    def __init__(self, inputs, expected_outputs):
        self.inputs = inputs
        self.expected = expected_outputs

    def getCopy(self):
        inputs = []
        expected = []
        for i in self.inputs:
            inputs.append(i)
        for e in self.expected:
            expected.append(e)
        output = DataPoint(inputs,expected)