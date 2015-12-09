from Logit import *
import numpy as np
from numpy.random import random_sample
#from sklearn.datasets import make_classification
from sklearn.preprocessing import LabelBinarizer
import re

#####
xtrain_original = []
ytrain = []
x_unique = []
x_unique_freq = []
f = open('train', 'r')
for line in f:
	line = line.rstrip()
	#print line
	if line != '':
		xtrain_original.append(line.split(' ')[0])
		ytrain.append(line.split(' ')[1])
f.close()

POS_list = []
g = open('allPOS', 'r')
for line in g:
	line = line.rstrip()
	#print line
	if line != '':
		POS_list.append(line)
g.close()
'''
#one-off code to write in nonunique file
for x in xtrain_original:
	if x not in x_unique:
		x_unique.append(x)
		x_unique_freq.append(1)
	else:
		x_unique_freq[x_unique.index(x)] += 1
print x_unique
count = 0
nonunique = []

for i, value in enumerate(x_unique_freq):
	if value > 5:
		count +=1
		nonunique.append(x_unique[i])
print count

v = open('nonunique', 'w')
for i, item in enumerate(nonunique):
	v.write(nonunique[i]+ '\n')
v.close

'''





# #####------ Nonunique words will be feature
nonunique = []
v = open('nonunique', 'r')
for line in v:
	line = line.rstrip()
	nonunique.append(line)
v.close()
print nonunique
##load test set
xtest = []
h = open('dev.in', 'r')
for line in h:
	line = line.rstrip()
	if line != '':
		xtest.append(line)
h.close()

#print len(xtest)
#set up feature size first, will change later
#load dev/test set (dev.in!)

#binarize the y set to the correct form
ytrain_2 = []
for value in ytrain:
	ytrain_2.append(POS_list.index(value))
ytrain_2 = np.asarray(ytrain_2)
print ytrain_2.shape
lb = LabelBinarizer()
Y = lb.fit_transform(ytrain_2)
#print y_binarized


# x_train = np.zeros((feature_size, len(xtrain_original)))
count = 0

#list of features, in order of index: 
# len(nonunique): number of unique words
# word length features: is english words (<= 15 char count, or more than 10)
# constant term
# Some regex feature
feature_size = len(nonunique) + 3
print len(nonunique)

###
def end_1(word):
	toReturn = 0
	if re.match(r'^[a-zA-Z]+ing$', word):
		toReturn = 1
	#if re.match(r'^[a-zA-Z]+ion$', word):
	#	toReturn = 2
	#elif re.match(r'^[a-zA-Z]+ed$', word):
	#	toReturn = 3
	#elif re.match(r'^[a-zA-Z]+ly$', word):
	#	toReturn = 4
	#if re.match(r'^[a-zA-Z]+ity$', word):
	#	toReturn = 2
	return toReturn

#---- convert data to the format trainable by logistic regression
def convert_data(data, featsize):
	train_matrix = np.zeros((len(data), featsize))
	for j, value in enumerate(data):
		try:
			word_index = nonunique.index(value)
			if value in nonunique:
				train_matrix[j][word_index] += 1
		except ValueError:
			pass
		# word length feature
		train_matrix[j][featsize-1] = len(value)
		reg_res = end_1(value)
		if reg_res >0:
			train_matrix[j][featsize-reg_res-1] = 1 

		#whether they are special characters
	return train_matrix
X = convert_data(xtrain_original, feature_size)
m = train(X, Y, itrs=1500, learn_rate=0.1, reg=1e-4, momentum=0.9, proj_layer_size=50)




#######Test data
xtest_original = []
ytest = []
f = open('dev.out', 'r')
for line in f:
	line = line.rstrip()
	#print line
	if line != '':
		xtest_original.append(line.split(' ')[0])
		ytest.append(line.split(' ')[1])
f.close()
ytest2 = []
for i in range(len(ytest)):
	ytest2.append(POS_list.index(ytest[i]))
YtestT = lb.transform(ytest2)

###Fit xtest to the model:
###Result of logistic regression will be probability distributions
xtest_proper = convert_data(xtest_original, feature_size)
m1 = predict(xtest_proper, m)

# def weighted_values(values, probabilities, size):
#     bins = np.add.accumulate(probabilities)
#     return values[np.digitize(random_sample(size), bins)]

# #function to transform logistic regression result into tag
# def convert_y(logit_result):
# 	y=[]
# 	indices = np.asarray(range(logit_result.shape[1]))
# 	for i in range(len(logit_result)):
# 		dist = np.asarray(logit_result[i])
# 		y.append(weighted_values(indices, dist, 1)[0])
# 	return y

# Y_test_predict = lb.transform(convert_y(m1))



#score of prediction
def score(Yh, Y):
    return 1- sum( np.not_equal(np.argmax(Yh,axis=1), np.argmax(Y,axis=1))) / float(Yh.shape[0])
print score(m1, YtestT)

'''
	r'^[a-zA-Z]+ing$',
		r'^[a-zA-Z]+ion$',
		r'^[a-zA-Z]+ed$',
		r'^[a-zA-Z]+ly$',
		r'^[a-zA-Z]+ity$',
'''
