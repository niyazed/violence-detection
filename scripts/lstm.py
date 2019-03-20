import numpy as np
import os
import cv2
import keras
import sklearn
import pandas
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import *
from keras.utils import to_categorical
from keras.models import load_model
from keras import layers
from keras import Model
from keras.callbacks import TensorBoard
from keras import optimizers


labels=['violent','non_violent']


# Train dataset loading and Stacking both label

X_train = np.load('C:/Users/NBH/Desktop/violence-detection/28x28/train/'+labels[0] + '.npy')
y_train = np.zeros(X_train.shape[0])

for i, label in enumerate(labels[1:]):
    x = np.load('C:/Users/NBH/Desktop/violence-detection/28x28/train/'+label + '.npy')
    X_train = np.vstack((X_train, x))
    y_train = np.append(y_train, np.full(x.shape[0], fill_value= (i + 1)))



# Test dataset loading and  Stacking both label

X_test = np.load('C:/Users/NBH/Desktop/violence-detection/28x28/test/'+labels[0] + '.npy')
y_test = np.zeros(X_test.shape[0])

for i, label in enumerate(labels[1:]):
    x = np.load('C:/Users/NBH/Desktop/violence-detection/28x28/test/'+label + '.npy')
    X_test = np.vstack((X_test, x))
    y_test = np.append(y_test, np.full(x.shape[0], fill_value= (i + 1)))



#Normalizing

#x_train = X_train.astype('float32')/255
#x_test = X_test.astype('float32')/255

# X_train = X_train.reshape(X_train.shape[0],30,30,1)
# X_test = X_test.reshape(X_test.shape[0],30,30,1)



print(X_train.shape)

#MODEL

inp = Input((28,28))

layer = CuDNNLSTM(50,return_sequences=True) (inp)
layer = BatchNormalization() (layer)
layer = Dropout(0.8)(layer)

layer = Flatten() (layer)

layer = Dense(10,activation='relu') (layer)
layer = Dropout(0.8) (layer)

out = (Dense(1, activation='sigmoid')) (layer)

model = Model(input = inp, output = out)
model.summary()



# rmsprop = optimizers.RMSprop(lr=0.01, rho=0.9, epsilon=None, decay=0.001)

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X_train,y_train, epochs=2000, verbose=1, validation_data=(X_test,y_test), batch_size=70, callbacks=[TensorBoard(log_dir='/tmp/cnn')])