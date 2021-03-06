# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 17:31:12 2021

@author: hanyu
"""

import numpy as np
import pandas as pd
import keras
from keras import optimizers
from keras.layers import Input, Dense
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt




data = pd.read_excel("angle_cut_20.xls")
fe_cr_ni=data.iloc[:,:3]
delta_strain=data.iloc[:,3:]
total_data = pd.read_excel("total.xls")
total_fe_cr_ni = total_data.iloc[:,:3]
total_fe_cr_ni = np.array(total_fe_cr_ni)

train_data = fe_cr_ni[:700]
val_data = fe_cr_ni[700:959]
test_data = total_fe_cr_ni[:4851]

# evaluate model with standardized dataset
train_target1 =np.array(delta_strain[:700])
val_target1 = np.array(delta_strain[700:959])
test_target1 = np.array(delta_strain[959:])
max=np.amax(train_target1,axis=0)
min=np.amin(train_target1,axis=0)
max=np.array(max).flatten().reshape(1,2)
min=np.array(min).flatten().reshape(1,2)
train_target=(train_target1-min)/(max-min)
val_target=(val_target1-min)/(max-min)    ###normalize
test_target=(test_target1-min)/(max-min)

# define the model
encoding_dim = 2   
input_img = Input(shape=(3, ))

# "encoded" is the encoded representation of the inputs



#encoded = Dense(encoding_dim * 256, activation='relu')(encoded)


encoded = Dense(encoding_dim * 256, activation='relu')(input_img)
encoded = Dense(encoding_dim * 128, activation='relu')(encoded)
#encoded = Dense(encoding_dim * 128, activation='relu')(encoded)
#encoded = Dense(encoding_dim * 128, activation='relu')(encoded)
#encoded = Dense(encoding_dim * 128, activation='relu')(encoded)
#encoded = Dense(encoding_dim * 64, activation='relu')(encoded)
encoded = Dense(encoding_dim * 64, activation='relu')(encoded)
encoded = Dense(encoding_dim * 32, activation='relu')(encoded)
encoded = Dense(encoding_dim * 16, activation='relu')(encoded)
encoded = Dense(encoding_dim * 8, activation='relu')(encoded)
encoded = Dense(encoding_dim * 4, activation='relu')(encoded)
encoded = Dense(encoding_dim * 2, activation='relu')(encoded)
encoded = Dense(encoding_dim , activation='relu')(encoded)

# ???input ??? output ???????????????????????????model
model_1= Model(input_img,encoded)
opt = keras.optimizers.Adam(learning_rate=0.001)
model_1.compile(optimizer = opt , loss = 'mse' , metrics = ['accuracy'])

history = model_1.fit(train_data, train_target, epochs=2048, batch_size=32, shuffle=True, validation_data=(val_data, val_target), verbose=2)
#####BATCH_size?????????140??????????????????????????????
#%%
pred1 = model_1.predict(test_data)
predict=pred1*(max-min)+min
predict1 = np.array(predict)


predict_delta = predict1[:,0].flatten()
predict_strain = predict1[:,1].flatten()
#inverse_delta = MinMaxScaler.inverse_transform(predict_delta)
plt.figure(1,figsize=(10,4))
plt.subplot(121)
plt.scatter(predict_delta, predict_strain)
plt.title('real_delta v.s. real_strain')
plt.xlabel('delta_real')
plt.ylabel('strain_real')
plt.show()
'''
plt.figure(1,figsize=(10,4))
plt.subplot(121)
plt.scatter(delta, predict_delta)
plt.title('delta_real v.s. delta_predicted')
plt.xlabel('delta_real')
plt.ylabel('delta_predicted')
plt.xticks(np.linspace(1.28 , 1.40 , 7))
plt.yticks(np.linspace(1.28 , 1.40 , 7))
plt.subplot(122)
plt.scatter(strain, predict_strain)
plt.title('strain_real v.s. strain_predicted')
plt.xlabel('strain_real')
plt.ylabel('strain_predicted')
plt.xticks(np.linspace(0.006 , 0.013 , 8))
plt.yticks(np.linspace(0.006 , 0.013 , 8))
plt.show()
'''
#%%
# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='best')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='best')
plt.show()
