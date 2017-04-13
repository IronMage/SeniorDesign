import numpy as np 
import neurolab as nl 

#The ideahere is to replace the defualt error functions used by the training function 
#with a custom one that retrieves the output of the fuzzy logic system

def myError(self, target, output):
	print("here")
	e = target - output
	v = .5 * np.sum(np.square(e))
	return v

def myErrorDeriv(self, target, output):
	print("there")
	return target - output

nl.error.SSE.__call__ = myError
nl.error.SSE.deriv = myErrorDeriv

#random input
in1 = np.random.uniform(-0.5, 0.5, (10, 2))
target = (in1[:, 0] + in1[:, 1]).reshape(10, 1)
#new network
net = nl.net.newff([[-0.5, 0.5], [-0.5, 0.5]], [5, 1])

# Train process
err = net.train(in1, target, show=1)

