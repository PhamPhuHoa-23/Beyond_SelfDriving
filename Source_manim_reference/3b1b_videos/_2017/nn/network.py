import os
import pickle
import random
import numpy as np
from PIL import Image
from nn.mnist_loader import load_data_wrapper
NN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
PRETRAINED_DATA_FILE = os.path.join(NN_DIRECTORY, 'pretrained_weights_and_biases')
IMAGE_MAP_DATA_FILE = os.path.join(NN_DIRECTORY, 'image_map')
DEFAULT_LAYER_SIZES = [28 ** 2, 16, 16, 10]
try:
    xrange
except NameError:
    xrange = range

class Network(object):

    def __init__(self, sizes, non_linearity='sigmoid'):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        if non_linearity == 'sigmoid':
            self.non_linearity = sigmoid
            self.d_non_linearity = sigmoid_prime
        elif non_linearity == 'ReLU':
            self.non_linearity = ReLU
            self.d_non_linearity = ReLU_prime
        else:
            raise Exception('Invalid non_linearity')

    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = self.non_linearity(np.dot(w, a) + b)
        return a

    def get_activation_of_all_layers(self, input_a, n_layers=None):
        if n_layers is None:
            n_layers = self.num_layers
        activations = [input_a.reshape((input_a.size, 1))]
        for bias, weight in zip(self.biases, self.weights)[:n_layers]:
            last_a = activations[-1]
            new_a = self.non_linearity(np.dot(weight, last_a) + bias)
            new_a = new_a.reshape((new_a.size, 1))
            activations.append(new_a)
        return activations

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        if test_data:
            n_test = len(test_data)
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k:k + mini_batch_size] for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print('Epoch {0}: {1} / {2}'.format(j, self.evaluate(test_data), n_test))
            else:
                print('Epoch {0} complete'.format(j))

    def update_mini_batch(self, mini_batch, eta):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w - eta / len(mini_batch) * nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - eta / len(mini_batch) * nb for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = self.non_linearity(z)
            activations.append(activation)
        delta = self.cost_derivative(activations[-1], y) * self.d_non_linearity(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = self.d_non_linearity(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedforward(x)), y) for x, y in test_data]
        return sum((int(x == y) for x, y in test_results))

    def cost_derivative(self, output_activations, y):
        return output_activations - y

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))

def sigmoid_inverse(z):
    assert np.max(z) <= 1.0 and np.min(z) >= 0.0
    z = 0.998 * z + 0.001
    return np.log(np.true_divide(1.0, np.true_divide(1.0, z) - 1))

def ReLU(z):
    result = np.array(z)
    result[result < 0] = 0
    return result

def ReLU_prime(z):
    return (np.array(z) > 0).astype('int')

def get_pretrained_network():
    data_file = open(PRETRAINED_DATA_FILE, 'rb')
    weights, biases = pickle.load(data_file, encoding='latin1')
    sizes = [w.shape[1] for w in weights]
    sizes.append(weights[-1].shape[0])
    network = Network(sizes)
    network.weights = weights
    network.biases = biases
    return network

def save_pretrained_network(epochs=30, mini_batch_size=10, eta=3.0):
    network = Network(sizes=DEFAULT_LAYER_SIZES)
    training_data, validation_data, test_data = load_data_wrapper()
    network.SGD(training_data, epochs, mini_batch_size, eta)
    weights_and_biases = (network.weights, network.biases)
    data_file = open(PRETRAINED_DATA_FILE, mode='w')
    pickle.dump(weights_and_biases, data_file)
    data_file.close()

def test_network():
    network = get_pretrained_network()
    training_data, validation_data, test_data = load_data_wrapper()
    n_right, n_wrong = (0, 0)
    for test_in, test_out in test_data:
        if np.argmax(network.feedforward(test_in)) == test_out:
            n_right += 1
        else:
            n_wrong += 1
    print((n_right, n_wrong, float(n_right) / (n_right + n_wrong)))

def layer_to_image_array(layer):
    w = int(np.ceil(np.sqrt(len(layer))))
    if len(layer) < w ** 2:
        layer = np.append(layer, np.zeros(w ** 2 - len(layer)))
    layer = layer.reshape((w, w))
    return (255 * layer).astype('int')

def maximizing_input(network, layer_index, layer_vect, n_steps=100, seed_guess=None):
    pre_sig_layer_vect = sigmoid_inverse(layer_vect)
    weights, biases = (network.weights, network.biases)
    if seed_guess is not None:
        pre_sig_guess = sigmoid_inverse(seed_guess.flatten())
    else:
        pre_sig_guess = np.random.randn(weights[0].shape[1])
    norms = []
    for step in range(n_steps):
        activations = network.get_activation_of_all_layers(sigmoid(pre_sig_guess), layer_index)
        jacobian = np.diag(sigmoid_prime(pre_sig_guess).flatten())
        for W, a, b in zip(weights, activations, biases):
            jacobian = np.dot(W, jacobian)
            a = a.reshape((a.size, 1))
            sp = sigmoid_prime(np.dot(W, a) + b)
            jacobian = np.dot(np.diag(sp.flatten()), jacobian)
        gradient = np.dot(np.array(layer_vect).reshape((1, len(layer_vect))), jacobian).flatten()
        norm = get_norm(gradient)
        if norm == 0:
            break
        norms.append(norm)
        old_pre_sig_guess = np.array(pre_sig_guess)
        pre_sig_guess += 0.1 * gradient
        print(get_norm(old_pre_sig_guess - pre_sig_guess))
    print('')
    return sigmoid(pre_sig_guess)

def save_organized_images(n_images_per_number=10):
    training_data, validation_data, test_data = load_data_wrapper()
    image_map = dict([(k, []) for k in range(10)])
    for im, output_arr in training_data:
        if min(list(map(len, list(image_map.values())))) >= n_images_per_number:
            break
        value = int(np.argmax(output_arr))
        if len(image_map[value]) >= n_images_per_number:
            continue
        image_map[value].append(im)
    data_file = open(IMAGE_MAP_DATA_FILE, mode='wb')
    pickle.dump(image_map, data_file)
    data_file.close()

def get_organized_images():
    data_file = open(IMAGE_MAP_DATA_FILE, mode='r')
    image_map = pickle.load(data_file, encoding='latin1')
    data_file.close()
    return image_map