#!/usr/bin/env python
# coding: utf-8

# In[1]:
#Model_3 performs with 100% accuracy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler,OneHotEncoder
from sklearn.model_selection import train_test_split


# In[2]:


from sklearn.datasets import make_circles
X,y=make_circles(n_samples=1000,noise=0.03,random_state=42)


# In[7]:


X[:10],y[:10]


# In[13]:


circles=pd.DataFrame({"X0":X[:,0],"X1":X[:,1],"label":y})
circles


# In[17]:


plt.scatter(X[ :, 0],X[:, 1],c=y,cmap=plt.cm.RdYlBu)


# In[ ]:


#Classification general model

model=tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(224,224,3)),#No of features here for image height,width and colors
    tf.keras.layers.Dense(100,activation='relu'),
    tf.keras.layers.Dense(3,activation='softmax')#output layer ,here 3 categories so units=3
])

#Compile the model

model.compile(loss=tf.keras.losses.categorical_crossentropy(),
              optimizer=tf.keras.optimizers.Adam(),
             metrics=['accuracy'])


# In[18]:


X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)


# In[110]:


model_2=tf.keras.Sequential([
    tf.keras.Input(shape=(2)),
    tf.keras.layers.Dense(100,activation='relu'),
    tf.keras.layers.Dense(200,activation='sigmoid'),
    tf.keras.layers.Dense(500,activation='selu'),
    tf.keras.layers.Dense(100,activation=tf.keras.activations.mish),
    tf.keras.layers.Dense(100,activation=tf.keras.activations.sigmoid),
    tf.keras.layers.Dense(1,activation='sigmoid')
])

model_2.compile(loss=tf.keras.losses.binary_crossentropy,
               optimizer=tf.keras.optimizers.Adam(learning_rate=0.2),
               metrics=["accuracy"]
               )
model_2.fit(X_train,y_train,epochs=300,verbose=0)


# In[111]:


model_2.evaluate(X_test,y_test)


# In[105]:


y_pred=model_2.predict(X_test)
y_pred


# In[59]:


plt.subplot(1,2,1)
plt.scatter(X_test[:, 0],X_test[:, 1],c=y_pred,cmap=plt.cm.RdYlBu)
plt.title("Predicted")
plt.subplot(1,2,2)
plt.scatter(X_test[:, 0],X_test[:, 1],c=y_test,cmap=plt.cm.RdYlBu)
plt.title("Actual")
#plt.legend()
plt.show()


# In[62]:


y_test


# In[117]:


model_3=tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(2)),
    tf.keras.layers.Dense(100,activation='relu'),
    tf.keras.layers.Dense(1,activation='sigmoid')
    
])

model_3.compile(loss=tf.keras.losses.binary_crossentropy,
                optimizer='Adam',
                metrics=['accuracy']
)
history=model_3.fit(X_train,y_train,epochs=300,verbose=0)


# In[118]:


model_3.evaluate(X_test,y_test)


# In[119]:


y_pred=model_3.predict(X_test)


# In[120]:


plt.subplot(1,2,1)
plt.scatter(X_test[:, 0],X_test[:, 1],c=y_pred,cmap=plt.cm.RdYlBu)
plt.title("Predicted")
plt.subplot(1,2,2)
plt.scatter(X_test[:, 0],X_test[:, 1],c=y_test,cmap=plt.cm.RdYlBu)
plt.title("Actual")
#plt.legend()
plt.show()

