import Logit
import numpy as np
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

# #one-off code to write in nonunique file
# for x in xtrain_original:
# 	if x not in x_unique:
# 		x_unique.append(x)
# 		x_unique_freq.append(1)
# 	else:
# 		x_unique_freq[x_unique.index(x)] += 1
# print x_unique
# count = 0
# nonunique = []

# for i, value in enumerate(x_unique_freq):
# 	if value > 1:
# 		count +=1
# 		nonunique.append(x_unique[i])
# print count

# # v = open('nonunique', 'w')
# # for i, item in enumerate(nonunique):
# # 	v.write(nonunique[i]+ '\n')
# # v.close







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
#print ytrain_2
lb = LabelBinarizer()
y_binarized = lb.fit_transform(ytrain_2)
#print y_binarized


# x_train = np.zeros((feature_size, len(xtrain_original)))
count = 0

#list of features, in order of index: 
# len(nonunique): number of unique words
# word length
# whether they are special characters: 
number_of_special_character = 0
feature_size = len(nonunique) + 1 + number_of_special_character




#---- convert data to the format trainable by logistic regression
def convert_data(data, featsize):
	global count
	train_matrix = np.zeros((len(data), featsize))
	for j, value in enumerate(data):
		try:
			word_index = nonunique.index(value)
			if value in nonunique:
				train_matrix[j][word_index] += 1
		except ValueError:
			count +=1
			pass
		# word length
		train_matrix[j][featsize-1] = len(value)
		#whether they are special characters
	return train_matrix

a= convert_data(xtrain_original, feature_size)
print a