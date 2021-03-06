import numpy as np
import data 
from data import Data

sigmoid = lambda x : 1.0/(1.0+np.exp(-x))

sigmoid_prime = lambda z : sigmoid(z)*(1-sigmoid(z))

structure = [6,16,16,16,16,16,1]

d = Data ()

global weights
weights = []
global biases
biases = []
activations = []
preactive = []
size = len(structure)

for x in range (0, (size - 1)):
	weights.append(np.asarray(np.random.uniform(-1,1, (structure[x+1],structure[x]))))
	biases.append(np.asarray(np.random.uniform(-1,1, (structure[x+1],1))))

for x in range (0, size):
	activations.append(np.zeros((structure[x],1)))

def feedforward(data, structure):
	global activations
	global weights
	global biases
	# min-max scaling
	Z = (data[0]-min(d.getZ()))/(max(d.getZ())-min(d.getZ()))
	N = (data[1]-min(d.getN()))/(max(d.getN())-min(d.getN()))
	A = (data[2]-min(d.getA()))/(max(d.getA())-min(d.getA()))
	Q = (data[3]-min(d.getQ()))/(max(d.getQ())-min(d.getQ()))
	Zd = (data[4]-min(d.getZDist()))/(max(d.getZDist())-min(d.getZDist()))
	Nd = (data[5]-min(d.getNDist()))/(max(d.getNDist())-min(d.getNDist()))

	activations [0] = np.array([[Z], [N], [A], [Q], [Zd], [Nd]]) # use scaled inputs as initial activations

	for x in range (0, size - 2):
		a = activations [x]
		mult = np.array([np.matmul(weights [x], a)])
		mult = np.reshape(mult, (structure [x+1],1))
		preactive.append (mult + biases [x])
		activations [x+1] = sigmoid(mult + biases[x])

	af = np.array([])
	mult = np.array([np.matmul(weights[size - 2],activations [size - 2])])
	mult = np.reshape (mult, (structure[size - 1],1))
	af = mult + biases[size - 2]
	activations.append([af])
	preactive.append ([af])

	return af

def backpropagation (activation, target, learningrate):
	global weights
	global biases

	deltaw = []
	deltab = []

	# error in last layer
	error_l = activation - target # getting error
	error_l = error_l = np.reshape (error_l, (structure[-1], 1)) # reshaping error to be array
	deltab.insert (0, error_l) # error = delta biases
	deltaw.insert (0, np.matmul(error_l, activations[4].transpose())) # weight delta is error propagated backwards

	# error in second last layer
	foo = np.matmul (weights[-1].transpose(), error_l)
	error_2l = np.multiply (foo, sigmoid_prime (preactive[-3]))
	error_2l = np.reshape (error_2l, (structure[-2], 1))
	deltab.insert (0, error_2l)
	deltaw.insert (0, np.matmul(error_2l, activations[3].transpose()))
			
	# error in third last layer
	foo = np.matmul (weights[-2].transpose(), error_2l)
	error_3l = np.multiply (foo, sigmoid_prime (preactive[-4]))
	error_3l = np.reshape (error_3l, (structure[-3], 1))
	deltab.insert (0, error_3l)
	deltaw.insert (0, np.matmul(error_3l, activations[2].transpose()))
	
	# error in fourth last layer
	foo = np.matmul (weights[-3].transpose(), error_3l)
	error_4l = np.multiply (foo, sigmoid_prime (preactive[-5]))
	error_4l = np.reshape (error_4l, (structure[-4], 1))
	deltab.insert (0, error_4l)
	deltaw.insert (0, np.matmul(error_4l, activations[1].transpose()))
			
	# error in 5th last layer
	foo = np.matmul (weights[-4].transpose(), error_4l)
	error_5l = np.multiply (foo, sigmoid_prime (preactive[-6]))
	error_5l = np.reshape (error_5l, (structure[-5], 1))
	deltab.insert (0, error_5l)
	deltaw.insert (0, np.matmul(error_5l, activations[0].transpose()))
	

	for x in range (0,5):
		weights [x] = weights [x] - (learningrate * deltaw[x])
	for x in range (0,5):
		biases[x] = biases [x] - (learningrate * deltab[x])


def iterbackprop (activation, target, learningrate):
	global weights
	global biases

	deltaw = []
	deltab = []

	# error in last layer
	error_l = activation - target # getting error
	error_l = np.reshape (error_l, (structure[-1], 1)) # reshaping error to be array
	deltab.insert (0, error_l) # error = delta biases
	deltaw.insert (0, np.matmul(error_l, activations[4].transpose())) # weight delta is error propagated backwards

	for x in range (0, size - 2):
		prop = np.matmul (weights[-(x+1)].transpose(), error_l)
		error_l = np.multiply (prop, sigmoid_prime (preactive[-(x+3)]))
		error_l = np.reshape (error_l, (structure[-(x+2)] , 1))
		deltab.insert (0, error_l)
		deltaw.insert (0, np.matmul(error_l, activations[((size-3)-x)].transpose()))

	for x in range (0,5):
		weights [x] = weights [x] - (learningrate * deltaw[x])
	for x in range (0,5):
		biases[x] = biases [x] - (learningrate * deltab[x])

structure = [6, 16, 16, 16, 16, 1]







i = 123
isotope = d.getIsotope()

error = feedforward (isotope[i], structure) - np.log10 (d.getHL()[i])
print (f"Error Before: {error}")

for z in range (0, 5000):
	activation = feedforward (isotope[i], structure)
	backpropagation (activation, np.log10 (d.getHL()[i]), 0.01)

error = feedforward (isotope[i], structure) - np.log10 (d.getHL()[i])
print (f"Error After: {error}")