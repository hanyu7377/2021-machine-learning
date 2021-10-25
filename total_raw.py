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


data = pd.read_excel("random.xls")
fe_cr_ni=data.iloc[:,:3]
delta_strain=data.iloc[:,3:]

train_data = fe_cr_ni[:700]
val_data = fe_cr_ni[700:800]
test_data = fe_cr_ni[800:]

# evaluate model with standardized dataset
train_target1 =np.array(delta_strain[:700])
val_target1 = np.array(delta_strain[700:800])
test_target1 = np.array(delta_strain[800:])
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
encoded = Dense(encoding_dim * 64, activation='relu')(input_img)
encoded = Dense(encoding_dim * 32, activation='relu')(encoded)
encoded = Dense(encoding_dim * 32, activation='relu')(encoded)
encoded = Dense(encoding_dim * 16, activation='relu')(encoded)
encoded = Dense(encoding_dim * 8, activation='relu')(encoded)
encoded = Dense(encoding_dim * 4, activation='relu')(encoded)
encoded = Dense(encoding_dim , activation='relu')(encoded)

# 把input 跟 output 和神經網路包成一個model
model_1= Model(input_img,encoded)
opt = keras.optimizers.Adam(learning_rate=0.001)
model_1.compile(optimizer = opt , loss = 'mse' , metrics = ['accuracy'])

history = model_1.fit(train_data, train_target, epochs=1000, batch_size=128, shuffle=True, validation_data=(val_data, val_target), verbose=2)
#####BATCH_size代表把140組數據分成幾段去學習
#%%
pred1 = model_1.predict(test_data)
predict=pred1*(max-min)+min
predict1 = np.array(predict)

delta = test_target1[:,0].flatten()
strain = test_target1[:,1].flatten()
predict_delta = predict1[:,0].flatten()
predict_strain = predict1[:,1].flatten()
#inverse_delta = MinMaxScaler.inverse_transform(predict_delta)

plt.figure(1,figsize=(10,4))
plt.subplot(121)
plt.scatter(delta, predict_delta)
plt.title('delta_real v.s. delta_predicted')
plt.xlabel('delta_real')
plt.ylabel('delta_predicted')
plt.xticks(np.linspace(0.5 , 1.4 , 10))
plt.yticks(np.linspace(0.5 , 1.4 , 10))
plt.subplot(122)
plt.scatter(strain, predict_strain)
plt.title('strain_real v.s. strain_predicted')
plt.xlabel('strain_real')
plt.ylabel('strain_predicted')
plt.xticks(np.linspace(0.003 , 0.015 , 5))
plt.yticks(np.linspace(0.003 , 0.015 , 5))
plt.show()

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