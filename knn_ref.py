import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

dataset = pd.read_csv('myrecorded_data.csv')

x = dataset.iloc[:,0:8]
y = dataset.iloc[:,8]
X_train, X_test, y_train, y_test = train_test_split(x,y, random_state=0, test_size=0.2)

sc_x = StandardScaler()
x_train = sc_x.fit_transform(X_train)
x_test = sc_x.transform(X_test)

print(y_test)
# classifier = KNeighborsClassifier(n_neighbours=, p=2, metric='euclidean')