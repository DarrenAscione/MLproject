import numpy as np
import sklearn.metrics as met
from itertools import izip

def sigmoid(X):
	return 1.0/(1 + np.e ** (-1.0*X))

#---- Soft max function: use for multiclass logi
def softMax(W, b, x):
	vect = np.exp(np.add(np.dot(x, W.T),b))
	return vect.T/np.sum(vect, axis = 1)

class Logit(object):

	#Predictor function:
	def predict(self, x):
		return softMax(self.W, self.b, x)

	#return the labels
	def lable(self, y):
	    return self.labels[y];
	
	#map the input to its labels
	def classify(self,x):
		#indices of data/label
		indices = self.predict(x).argmax(axis = 1)
		return map(self.lable, indices)

	#check accuracy of model, returning the error
	def validate(self, x, y):
		#classify input
		prediction = self.classify(x)
		#error score
		return 1.0 - met.accuracy_score(y, prediction)

	#return negative loglikelihood
	def nll(self, params):
		#training data
		x,y = self.args

		self.update_params(params)
		sigmoid_activation = softMax(self.W, self.b, x)
		index = [range(0, np.shape(sigmoid_activation)[0]), y]
		p=sigmoid_activation[index]
		return -np.mean(np.log(p))

	#gradient computation, single data sample
	def comp_grad(self, out, x, y):
		out = (np.reshape(out, (np.shape(out)[0], 1)))
		out[y] -= 1
		W = out * x.T
		return np.vstack((W.T, out.flatten()))

	#gradient computation, all input samples
	def gradients(self, params = None):
		x,y = self.args

		self.update_params(params)
		sigmoid_activation = softMax(self.W, self.b, x)
		e = [ self.comp_grad(a,c,b) for a, c,b in izip(sigmoid_activation,y,x)]
		return np.mean(e, axis = 0).T.flatten()

	





