from sklearn.metrics import confusion_matrix
y_pred=model_2.predict(X_test)
confuaion_matrix=confusion_matrix(y_test,tf.round(y_pred))
from sklearn.metrics import ConfusionMatrixDisplay
ConfusionMatrixDisplay.from_predictions(y_test,tf.round(y_pred))

