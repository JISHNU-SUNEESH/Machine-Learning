#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split


# 

# In[27]:


model=tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=1,activation='sigmoid',input_shape=[1]),
    tf.keras.layers.Dense(50),
    tf.keras.layers.Dense(1)
])

model.compile(loss=tf.losses.binary_crossentropy,
             optimizer=tf.keras.optimizers.Adam(),
             metrics=[tf.keras.metrics.binary_accuracy])


# In[28]:


data = {
    'Hours_Studied': [2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Passed_Exam': [0, 0, 0, 0, 1, 1, 1, 1, 1]  # 0: Failed, 1: Passed
}

df = pd.DataFrame(data)


# In[29]:


feature=df['Hours_Studied'].astype(np.float32)
label=df['Passed_Exam'].astype(np.float32)
model.fit(feature,label,epochs=100)


# In[37]:


model.predict([1])

