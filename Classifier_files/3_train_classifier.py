import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

data_dict = pickle.load(open('./data_for_training.pickle','rb'))
# for sample in data_dict['data']:
#     print(len(sample))

data = np.asarray(data_dict['data'])
print("Dimensiones de data: ", data.shape)
labels = np.asarray(data_dict['labels'])
print("Dimensiones de labels: ", labels.shape)

#spliting the data for training, and another part of the info for testing
#Shuffling the data always
#Stratify -> We are going to create the dataset, but keeping the same proportion of the different categories.
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = RandomForestClassifier()

model.fit(x_train, y_train)

y_preditc = model.predict(x_test)
score = accuracy_score(y_preditc,y_test)
print('{:.2f}% of samples were classifed correctly !'.format(score*100))


f = open('model_for_training.p','wb')
pickle.dump({'model': model},f)
f.close()