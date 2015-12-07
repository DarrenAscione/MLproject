import Logit
import numpy as np
#from sklearn.datasets import make_classification
from sklearn.preprocessing import LabelBinarizer

#####
xtrain_original = []
xtrain = []
ytrain = []
x_unique = []
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

#one-off code to write in unique file
# for x in xtrain_original:
# 	if x not in x_unique:
# 		x_unique.append(x)
#v = open('unique', 'w')
# for i, item in enumerate(x_unique):
# 	v.write(x_unique[i]+ '\n')

v = open('unique', 'r')
for line in v:
	line = line.rstrip()
	x_unique.append(line)
v.close()

#load test set
xtest = []
h = open('dev.in', 'r')
for line in h:
	line = line.rstrip()
	if line != '':
		xtest.append(line)
h.close()

print len(xtest)
#set up feature size first, will change later
feature_size = len(x_unique)
#load dev/test set (dev.in!)
for k, value in enumerate(xtrain_original):
	np.zeros((feature_size, len(xtest)))
	
