```python
import tensorflow as tf

```


```python
model_2=tf.keras.models.load_model("drwas_circles_model.keras")
```


```python
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
X,y=make_circles(n_samples=1000,noise=0.03,random_state=42)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
```


```python
from sklearn.metrics import confusion_matrix
y_pred=model_2.predict(X_test)
confuaion_matrix=confusion_matrix(y_test,tf.round(y_pred))
from sklearn.metrics import ConfusionMatrixDisplay
ConfusionMatrixDisplay.from_predictions(y_test,tf.round(y_pred))

```

    7/7 [==============================] - 0s 1ms/step





    <sklearn.metrics._plot.confusion_matrix.ConfusionMatrixDisplay at 0x7f8c39ea90a0>




    
![png](/Users/jishnu.suneesh/downloads/Confusion_metrics/output_3_2.png)
    



```python

```

