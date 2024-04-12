"""
The code for the research presented in the paper titled "Enabling inverse design of chirped apodized fiber Bragg grating with deep learning"

This code corresponds to the article's forward Deep Neural Network (DNN) section.
Please cite the paper in any publication using this code.
"""

import matplotlib.pyplot as plt 
import pandas as pd 
import pickle
import csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential 
from keras.layers import Dense
from keras.layers import LeakyReLU
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam

### Load the data from the CSV file (the results of the FDTD solver)
result = pd.read_csv("DL-based_FBG_V.csv", header=None)
result = result.to_numpy()

x = result[0:result.shape[0],0:9]
y = result[0:result.shape[0],10:310]

# Allocation of 70% of the total data to the training data
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.30, shuffle='true')
# Allocation of 50% of the remaining data to the validation data and 50% to the test data (15% validation and 15% test of total)
x_test, x_val, y_test, y_val = train_test_split(x_val, y_val, test_size=0.50, shuffle='true')

### Feature Scaling
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_val = sc.transform(x_val)
x_test = sc.transform(x_test)

# We delete the result to prevent the RAM from being filled up.
del result
### Defining the Layers of the deep neural network (DNN)
# 11 hidden layer and 160 neurons in the central layer
# A slope of 0.2 has been set for the Leaky ReLU
# The input comprises 5 design parameters of the fiber Bragg grating (FBG) and the apodization function vector, which has 4 components.
# Output is the transmission value at the wavelength (300 points)
Model = Sequential()
Model.add(Dense(5, input_dim=9))
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
Model.add(Dense(300))
Model.summary()

# useing EarlyStopping
es = EarlyStopping(monitor= 'val_loss', mode = 'auto', verbose=1, patience=5,)

### Configuring the settings of the training procedure 
# Mean Squared  Error (MSE) function has been used for loss estimation
# AdaDelta Optimizer has been used and a learning rate of 0.1 has been set 
Model.compile(loss='mse',
              optimizer = Adam(learning_rate=0.1))

### Training Model 
# batch size of 80 was set and 1000 epochs were performed
history = Model.fit(x_train, y_train, epochs=1000,
          batch_size = 80, validation_data=(x_val, y_val), callbacks= [es])

### plot the loss graph
plt.plot(history.history['val_loss'], linewidth=1)
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

### Testing Model 
predictions = Model.predict(x_test)
Loss = Model.evaluate(x_test, y_test)
print(Loss)

# save the loss values in CSV file
with open('history_Forward_model.pkl', 'wb') as f:
    pickle.dump(history.history, f)
fieldnames = ['Epoch', 'Training Loss', 'Validation Loss']
with open('loss_Forward_model.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for epoch, train_loss_value, val_loss_value in zip(range(1, len(train_loss) + 1), train_loss, val_loss):
        writer.writerow({'Epoch': epoch, 'Training Loss': train_loss_value, 'Validation Loss': val_loss_value})

# save the forward model and its weights
model_json = Model.to_json()
json_file = open("DL-based_FBG_forward_model.json", "w")
json_file.write(model_json)   
Model.save_weights("DL-based_FBG_forward_model_weights.h5")
json_file.close()
