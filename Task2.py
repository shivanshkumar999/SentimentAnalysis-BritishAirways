# -*- coding: utf-8 -*-
"""CustomerBuyingBehaviour

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eSG9CHBPU5idYDWgJmV3t7GwpYayWKsF
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt


data = pd.read_csv('/content/customer_booking.csv', encoding='latin-1')
data = data.drop_duplicates()

booking_done = data['booking_complete'].squeeze()
plt.pie(booking_done.value_counts(), labels=['0', '1'], explode = [0.1, 0], colors = ['Grey', 'Yellow'] , autopct = '%1.1f%%')
plt.title('Booking percentage')

print("======================================Data Dimensions==============================================")
print("The data shape is ", data.shape)
print("======================================statistical Evaluations==============================================")
print(data.describe())
print("======================================Data Types of Data==============================================")
print(data.info())
print("======================================Unique value Count==============================================")
print(data.nunique())
print("======================================Null value Count==============================================")
print(data.isnull().sum())
print("======================================Not Null Value Count==============================================")
print(data.notnull().sum())

data = data.dropna()

x = data.drop('booking_complete', axis = 1)
y = data.booking_complete

for col in x.select_dtypes(['object','float']):
  x[col], _ = x[col].factorize()

x.info()

from sklearn.feature_selection import mutual_info_classif


miscore = mutual_info_classif(x,y)
miscore = pd.Series(miscore, name = 'MiScore', index = x.columns)
miscore = miscore.sort_values(ascending = False)

miscore

def plot_miscore(scores):
  scores = scores.sort_values(ascending = True)
  width = np.arange(len(scores))
  ticks = list(scores.index)
  plt.barh(width, scores)
  plt.yticks(width, ticks)
  plt.title('Mutual Info Score')

plt.figure(dpi = 100, figsize=(9,6))
plot_miscore(miscore)

from sklearn.model_selection import train_test_split
def splits(x, y):
  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

  return (x_train, x_test, y_train, y_test)

from sklearn.preprocessing import MinMaxScaler

def scale(x):
    scaler = MinMaxScaler()
    scaler.fit(x)
    return x

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score

fea = ['booking_origin', 'wants_extra_baggage', 'route', 'flight_duration', 'wants_in_flight_meals', 'flight_hour']
x = data[fea]
# one hot encoding
x = pd.get_dummies(x, columns = fea)
y = data.booking_complete

forest = RandomForestClassifier(random_state = 1)
x_train, x_test, y_train, y_test = splits(x, y)
forest.fit(x_train, y_train)

results = forest.predict(x_test)

count1, count0 = 0, 0

for x in results:
  if x == 1:
    count1+=1
  else:
    count0+=1

print("The total number of bookings possibilities are -", (count1/(count0+count1)*100),"%")
print("The total number of bookings non-possibilities are -", (count0/(count0+count1)*100),"%")

plt.title("Booking Percentage after the Predications")
legends = ['Non-Booking', 'Booking']
plt.pie([count0, count1], colors=['grey', 'yellow'], explode = [0, 0.15], autopct = '%1.1f%%')
plt.legend(legends)
plt.show()

print("The model is ", accuracy_score(y_test,results)*100,"% Accurate.")
print("It's AUC Score is ", roc_auc_score(y_test,results), ".")

xx_train, xx_test, yy_train, yy_test = splits(x, y)

forest2 = RandomForestClassifier(random_state=1)
forest2.fit(xx_train, yy_train)

results2 = forest2.predict(xx_test)

count11, count00 = 0, 0

for x in results2:
  if x == 1:
    count11+=1
  else:
    count00+=1

print("The total number of bookings possibilities are -", (count11/(count00+count11)*100),"%")
print("The total number of bookings non-possibilities are -", (count00/(count00+count11)*100),"%")

plt.title("Booking Percentage after the Predications")
legends = ['Non-Booking', 'Booking']
plt.pie([count00, count11], colors=['grey', 'yellow'], explode = [0, 0.15], autopct = '%1.1f%%')
plt.legend(legends)
plt.show()

print("The model is ", accuracy_score(yy_test,results)*100,"% Accurate.")
print("It's AUC Score is ", roc_auc_score(yy_test,results), ".")