"""
The code for the research presented in the paper titled "Enabling inverse design of chirped apodized fiber Bragg grating with deep learning."

This code corresponds to the article's forward Deep Neural Network (DNN) section.
Please cite the paper in any publication using this code.
"""
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

import csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential 
from keras.layers import Dense
from keras.layers import LeakyReLU
from keras.layers import Dropout
from keras.optimizers import Adam

### Load the data from CSV file (the results of FDTD solver)
result = pd.read_csv("DL-based_FBG_H.csv", header=None)
result = result.to_numpy()
result=result.astype(np.float16)

# warning! : the results of the ports should not be negative! 
x = abs(result[0:result.shape[0],0:300])
y = result[0:result.shape[0],300:309]

# Allocation of 70% of the total data to the training data
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.30, shuffle='true')
# Allocation of 50% of the remaining data to the validation data and 50% to the test data (15% validation and 15% test of total)
x_test, x_val, y_test, y_val = train_test_split(x_val, y_val, test_size=0.50, shuffle='true')

### Feature Scaling
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_val = sc.transform(x_val)

### Defining the Layers of the deep neural network (DNN)
# 6 hidden layer and 60 neurons in each layer
# A slope of 0.2 has been set for the Leaky ReLU
# Input consists of 1600 points of transmission spectrum (300 points)
# Output consists of 5 geometric parameters of the fiber Bragg grating (FBG)
Model = Sequential()
Model.add(Dense(5, input_dim=300))
Model.add((LeakyReLU(alpha=0.2)))
Model.add(Dropout(0.1))
Model.add(Dense(10))
Model.add((LeakyReLU(alpha=0.2)))
Model.add(Dropout(0.1))
Model.add(Dense(20))
Model.add((LeakyReLU(alpha=0.2)))
Model.add(Dropout(0.1))
Model.add(Dense(40))
Model.add((LeakyReLU(alpha=0.2)))
Model.add(Dropout(0.1))
Model.add(Dense(80))
Model.add((LeakyReLU(alpha=0.2)))
Model.add(Dropout(0.1))
Model.add(Dense(160))
Model.add((LeakyReLU(alpha=0.2)))
Model.add(Dropout(0.1))
Model.add(Dense(80))
Model.add((LeakyReLU(alpha=0.2)))
Model.add(Dropout(0.1))
Model.add(Dense(40))
Model.add((LeakyReLU(alpha=0.2)))
Model.add(Dropout(0.1))
Model.add(Dense(20))
Model.add((LeakyReLU(alpha=0.2)))
Model.add(Dropout(0.1))
Model.add(Dense(10))
Model.add((LeakyReLU(alpha=0.2)))
Model.add(Dropout(0.1))
Model.add(Dense(5))
Model.add((LeakyReLU(alpha=0.2)))
Model.add(Dense(9))
Model.summary()

### Configuring the settings of the training procedure 
# Mean Squared Error (MSE) function has been used for loss estimation
# AdaDelta Optimizer has been used and a learning rate of 0.1 has been set 
Model.compile(loss='mse',
              optimizer= Adam(learning_rate=0.1))

### Training Model 
# batch size of 80 was set and 1000 epochs were performed
history = Model.fit(x_train, y_train, epochs=1000,
          batch_size = 80, validation_data=(x_val, y_val))

### plot the loss graph
plt.plot(history.history['val_loss'], linewidth=1, linestyle='--')
plt.plot(history.history['loss'], linewidth=2, linestyle='--')
plt.title('The loss of training model', fontname='Times New Roman', fontsize=18, loc='center')
plt.xlabel('epochs', fontname='Times New Roman', fontsize=18)
plt.ylabel('loss', fontname='Times New Roman', fontsize=18)
plt.xticks(fontfamily='Times New Roman', fontsize=14)
plt.yticks(fontfamily='Times New Roman', fontsize=14)
plt.legend(['train', 'Validation', 'test'])
plt.show()

### loss value of train and validation data
train_loss = history.history['loss']
val_loss = history.history['val_loss']

# save the loss values in csv file
fieldnames = ['Epoch', 'Training Loss', 'Validation Loss']
with open('loss.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for epoch, train_loss_value, val_loss_value in zip(range(1, len(train_loss) + 1), train_loss, val_loss):
        writer.writerow({'Epoch': epoch, 'Training Loss': train_loss_value, 'Validation Loss': val_loss_value})

# save the inverse model and its weights
model_json = Model.to_json()
json_file = open("DL-based_FBG_inverse_model.json", "w")
json_file.write(model_json)   
Model.save_weights("DL-based_FBG_inverse_model_weights.h5")
json_file.close()

