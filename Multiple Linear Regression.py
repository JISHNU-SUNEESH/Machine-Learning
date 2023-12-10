#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split


# In[65]:


data=pd.read_csv('/Users/jishnu.suneesh/downloads/data.csv')
data.head()


# In[54]:


feature=data[['Volume','Weight']].astype(np.float32)
label=data['CO2'].astype(np.float32)

X_train,X_test,y_train,y_test=train_test_split(feature,label,test_size=0.2)


# In[259]:


#Model Creation

model=tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=1,input_shape=[2]),
    tf.keras.layers.Dense(200),
    tf.keras.layers.Dense(100),
    tf.keras.layers.Dense(1)
])

model.compile(loss=tf.keras.losses.mean_absolute_error,
              optimizer=tf.keras.optimizers.Adam(learning_rate=0.27),
              metrics=['mae'])

model.fit(X_train,y_train,epochs=500)


# In[256]:


model.evaluate(X_test,y_test)


# In[260]:


y_pred=model.predict(X_test)
y_pred,y_test


# In[261]:


mae=tf.keras.metrics.mean_absolute_error(y_test,y_pred)
mae


# In[262]:



plt.subplot(2,1,1)

#plt.scatter(X_train['Weight'],y_train,c='y',label='Training data(Weight)')
plt.scatter(X_test['Weight'],y_test,c='orange',label='Actual data(Weight)')
plt.scatter(X_test['Weight'],y_pred,c='violet',label='Predicted data(Weight)')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.legend(fontsize='x-small',loc='upper left')

plt.subplot(2,1,2)

#plt.scatter(X_train['Volume'],y_train,c='b',label='Training data(Volume)')
plt.scatter(X_test['Volume'],y_test,c='g',label='Actual data(Volume)')
plt.scatter(X_test['Volume'],y_pred,c='r',label='Predicted data(Volume)')
plt.legend(fontsize='x-small',loc='upper left')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.show()

