import numpy as np
#this is to test the code, using sklearn to make random classification and label
from sklearn.datasets import make_classification
from sklearn.preprocessing import LabelBinarizer

###--- Usage:
###-----Training the model:
###---  train(Xtrain, Ytrain, itrs=500, learn_rate=0.1, reg=1e-4, momentum=0.9, proj_layer_size=50)
###--- X_train's dimension: (Number_of_data_point, number_of_feature)
###--- Y_train's dimension: (Number_of_data_point, number_of_tags)
###---- For example: if we have 43 tags, each Yi would look like [0 0 0 0 0 0 0 0 0...... 0 1 0 0 0 0 0] 
###-----(1 on the correct tag, 0 for everything else)

#set up transform matrix so that it is consistent for train & predict
Transform_matrix = None

def sigmoid(A, x):
	return np.hstack(((1+np.exp(-np.dot(A, x)))**-1,1))

def basismap(A,X):
	dim_new = sigmoid(A,X[0,:]).shape[0]
	Xn = np.zeros((X.shape[0], dim_new))
	for i,xi in enumerate(X):
		Xn[i,:] = sigmoid(A,xi)
	return Xn

#gradient with regularizer
def gradient(Xn, Y, reg, W):
	Yh = softmax(np.dot(Xn, W.T))
	return -np.dot(Y.T-Yh.T,Xn)/Xn.shape[0] + reg*W

#run the optimization, return the model parameter
def train(X, Y, itrs=100, learn_rate=0.1, reg=0.1,
		momentum=0.5, report_cost=False, proj_layer_size=10):
	"""
	Fit the model. 
	itrs - number of iterations to run
	learn_rate - size of step to use for gradient descent
	reg - regularization penalty
	momentum - weight of the previous gradient in the update step
	proj_layer_size - number of dimensions in the projection (mixing) layer. Higher -> more variance
	"""
	global Transform_matrix
	#first map to a new basis

	A = X[np.random.permutation(X.shape[0])[:proj_layer_size],:]
	Transform_matrix = A
	Xn = basismap(A,X)
	
	#initial weight
	W = np.random.uniform(-0.1, 0.1, (Y.shape[1], Xn.shape[1]))

	#optimize
	costs = []
	previous_grad = np.zeros(W.shape) #used in momentum
	for i in range(itrs):
		grad = gradient(Xn, Y, reg, W) #compute gradient
		W = W - learn_rate*(grad + momentum*previous_grad) #take a step, use previous gradient as well.
		previous_grad = grad
	return W

def softmax(Z):
	#returns sigmoid elementwise
	Z = np.maximum(Z, -1e3)
	Z = np.minimum(Z, 1e3)
	numerator = np.exp(Z)
	return numerator / np.sum(numerator, axis=1).reshape((-1,1))

def predict(X, W):
	Xn = basismap(Transform_matrix,X)
	return softmax(np.dot(Xn, W.T))




###############--------------------- Test code------------------------#######
# X,Y = make_classification(n_features=20, n_informative=6, n_redundant=14,
# 						n_repeated=0, n_classes=5, n_clusters_per_class=3,n_samples=400)
# lb = LabelBinarizer()
# Y = lb.fit_transform(Y)

# print X.shape
# print Y.shape

# m = train(X[:300,:], Y[:300,:], itrs=500, learn_rate=0.1, reg=1e-4, momentum=0.9, 
# 			proj_layer_size=50)
# print Y
#print m #this is the parameter of our prediction (i.e like y_predicted = AX etc...)

