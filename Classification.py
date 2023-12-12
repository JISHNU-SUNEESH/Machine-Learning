#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler,OneHotEncoder
from sklearn.model_selection import train_test_split


# In[ ]:


#Classification general model

model=tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(224,224,3)),#No of features here for image height,width and colors
    tf.keras.layers.Dense(100,activation='relu'),
    tf.keras.layers.Dense(3,activation='softmax')#output layer
])

#Compile the model

model.compile(loss=tf.keras.losses.categorical_crossentropy(),
              optimizer=tf.keras.optimizers.Adam(),
             metrics=['accuracy'])

