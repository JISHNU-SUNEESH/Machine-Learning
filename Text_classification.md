```python
import pandas as pd
import numpy as np
import tensorflow as tf
import datasets

fake_news=pd.read_csv('/Users/jishnu.suneesh/downloads/archive/fake.csv')
true_news=pd.read_csv('/Users/jishnu.suneesh/downloads/archive/true.csv')
fake_news['true_or_false'] = 0
true_news['true_or_false'] = 1
df_news=pd.concat([fake_news,true_news])
df_news.reset_index(drop=True,inplace=True)
df_news=datasets.Dataset.from_pandas(df_news[['title','true_or_false']])
df_news
```




    Dataset({
        features: ['title', 'true_or_false'],
        num_rows: 44898
    })




```python
df_news[0]
```




    {'title': ' Donald Trump Sends Out Embarrassing New Year’s Eve Message; This is Disturbing',
     'label': 0}




```python
df_news=df_news.rename_column(original_column_name='true_or_false',new_column_name='label')
```


```python
from sklearn.model_selection import train_test_split
train_dataset, test_dataset = train_test_split(df_news, test_size=0.2, random_state=42)
train_dataset=datasets.Dataset.from_dict(train_dataset)
test_dataset=datasets.Dataset.from_dict(test_dataset)

```


```python
train_dataset
```




    Dataset({
        features: ['title', 'label'],
        num_rows: 35918
    })




```python
test_dataset
```




    Dataset({
        features: ['title', 'label'],
        num_rows: 8980
    })




```python
from transformers import AutoTokenizer
tokenizer=AutoTokenizer.from_pretrained("distilbert-base-uncased")

def preprocess_function(examples):
    return tokenizer(examples['title'],truncation=True)

train_tokenized=train_dataset.map(preprocess_function,batched=True)
test_tokenized=test_dataset.map(preprocess_function,batched=True)
```


    Map:   0%|          | 0/35918 [00:00<?, ? examples/s]



    Map:   0%|          | 0/8980 [00:00<?, ? examples/s]



```python
train_tokenized
```




    Dataset({
        features: ['title', 'label', 'input_ids', 'attention_mask'],
        num_rows: 35918
    })




```python
test_tokenized
```




    Dataset({
        features: ['title', 'label', 'input_ids', 'attention_mask'],
        num_rows: 8980
    })




```python
from transformers import DataCollatorWithPadding

data_collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="np")
```


```python
import evaluate

accuracy = evaluate.load("accuracy")

import numpy as np


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)
```


```python
id2label = {0: "NEGATIVE", 1: "POSITIVE"}
label2id = {"NEGATIVE": 0, "POSITIVE": 1}
```


```python
from transformers import create_optimizer
import tensorflow as tf

batch_size = 16
num_epochs = 5
batches_per_epoch = len(train_tokenized) // batch_size
total_train_steps = int(batches_per_epoch * num_epochs)
optimizer, schedule = create_optimizer(init_lr=2e-5, num_warmup_steps=0, num_train_steps=total_train_steps)
```

    WARNING:absl:At this time, the v2.11+ optimizer `tf.keras.optimizers.Adam` runs slowly on M1/M2 Macs, please use the legacy Keras optimizer instead, located at `tf.keras.optimizers.legacy.Adam`.



```python
from transformers import TFAutoModelForSequenceClassification

model = TFAutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2, id2label=id2label, label2id=label2id
)
```

    Some weights of the PyTorch model were not used when initializing the TF 2.0 model TFDistilBertForSequenceClassification: ['vocab_projector.bias', 'vocab_transform.bias', 'vocab_layer_norm.bias', 'vocab_layer_norm.weight', 'vocab_transform.weight']
    - This IS expected if you are initializing TFDistilBertForSequenceClassification from a PyTorch model trained on another task or with another architecture (e.g. initializing a TFBertForSequenceClassification model from a BertForPreTraining model).
    - This IS NOT expected if you are initializing TFDistilBertForSequenceClassification from a PyTorch model that you expect to be exactly identical (e.g. initializing a TFBertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights or buffers of the TF 2.0 model TFDistilBertForSequenceClassification were not initialized from the PyTorch model and are newly initialized: ['pre_classifier.weight', 'pre_classifier.bias', 'classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.



```python
tf_train_set = model.prepare_tf_dataset(
    train_tokenized,
    shuffle=True,
    batch_size=16,
    collate_fn=data_collator,
)

tf_validation_set = model.prepare_tf_dataset(
    test_tokenized,
    shuffle=False,
    batch_size=16,
    collate_fn=data_collator,
)
```


```python
tf_train_set
```




    <_PrefetchDataset element_spec=({'input_ids': TensorSpec(shape=(16, None), dtype=tf.int64, name=None), 'attention_mask': TensorSpec(shape=(16, None), dtype=tf.int64, name=None)}, TensorSpec(shape=(16,), dtype=tf.int64, name=None))>




```python
tf_validation_set
```




    <_PrefetchDataset element_spec=({'input_ids': TensorSpec(shape=(None, None), dtype=tf.int64, name=None), 'attention_mask': TensorSpec(shape=(None, None), dtype=tf.int64, name=None)}, TensorSpec(shape=(None,), dtype=tf.int64, name=None))>




```python
importransformerssorflow as tf

model.compile(optimizer=optimizer)  # No loss argument!
```


```python
from transformers.keras_callbacks import KerasMetricCallback

metric_callback = KerasMetricCallback(metric_fn=compute_metrics, eval_dataset=tf_validation_set,batch_size=16)
callbacks = [metric_callback]
```


```python
model.fit(x=tf_train_set, validation_data=tf_validation_set, epochs=3, callbacks=callbacks)
```

    Epoch 1/3
    2244/2244 [==============================] - 1301s 577ms/step - loss: 0.0745 - val_loss: 0.0390 - accuracy: 0.9859
    Epoch 2/3
    2244/2244 [==============================] - 2146s 957ms/step - loss: 0.0212 - val_loss: 0.0355 - accuracy: 0.9885
    Epoch 3/3
    2244/2244 [==============================] - 1316s 587ms/step - loss: 0.0066 - val_loss: 0.0426 - accuracy: 0.9890





    <keras.src.callbacks.History at 0x2ef7981d0>




```python
from transformers import pipeline

classifier=pipeline('sentiment-analysis',model=model,tokenizer=tokenizer)

text='Donald Trump Sends Out Embarrassing New Year’s Eve Message; This is Disturbing'
classifier(text)
```




    [{'label': 'NEGATIVE', 'score': 0.9999377727508545}]


