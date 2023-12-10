#!/usr/bin/env python
# coding: utf-8





import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.model_selection import train_test_split





#dataset

feature=np.arange(1,9)
feature=tf.constant(feature)
feature=tf.cast(feature,dtype=tf.float32)
label=tf.constant([7.9,12.0,9.5,11.3,11.8,11.3,4.2,0.2])

X_train,X_test,y_train,y_test=train_test_split(np.array(feature),np.array(label),test_size=0.2)
X_test,y_test





#Defining a Model

model=tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=1,input_shape=[1]),
    tf.keras.layers.Dense(units=50),
    tf.keras.layers.Dense(units=1)
    
])

#compiling the model

model.compile(loss=tf.keras.losses.mean_absolute_error,
              optimizer=tf.keras.optimizers.RMSprop(),
              metrics=['mae']
             )

model.fit(X_train,y_train,epochs=100)





history=model.fit(X_train,y_train,epochs=100,verbose=0)
hist=pd.DataFrame(history.history)
weight=model.get_weights()[0]
bias=model.get_weights()[1]
weight,bias





model.evaluate(X_test,y_test)





y_pred=model.predict(X_test)
y_pred,y_test,X_test





model.summary()





#Second Model

model_2=tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=1,input_shape=[1]),
    tf.keras.layers.Dense(units=200),
    tf.keras.layers.Dense(units=100),
    tf.keras.layers.Dense(units=50),
    tf.keras.layers.Dense(1)
])

model_2.compile(loss=tf.keras.losses.mean_squared_error,
              optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.02),
              metrics=[tf.keras.metrics.mean_squared_error]
               )

model_2.fit(X_train,y_train,epochs=200,verbose=0)





model_2.evaluate(X_test,y_test)





y_pred=model_2.predict(X_test)
history=model_2.fit(X_train,y_train,epochs=100,verbose=0)
hist=pd.DataFrame(history.history) 

weight=model_2.get_weights()[0]
bias=model_2.get_weights()[1]
weight,bias,y_pred,y_test





#Plotting function

def plot_model(X_train,y_train,X_test,y_test,y_pred,weight,bias,feature):
    plt.scatter(X_train,y_train,c='b',label='Training data')
    plt.scatter(X_test,y_test,c='r',label='Actual data')
    plt.scatter(X_test,y_pred,c='g',label='Predicted data')
    
    #Regression Line
    m=weight
    c=bias
    y=c+(m*feature)
    plt.plot(feature,tf.squeeze(y),linestyle='--',c='y',label='Regression Line')
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.legend(loc='upper right',fontsize='x-small')
    plt.show()
    
def plot_metrics(history,hist):
    plt.rcParams['figure.facecolor']='lightgrey'
    plt.scatter(history.epoch,hist.iloc[: ,1])
    plt.title('Metric vs Epochs')
    plt.show()
    
    







plot_model(X_train,y_train,X_test,y_test,y_pred,weight,bias,feature) 





plot_metrics(history,hist)







