[ここ](https://colab.research.google.com/github/tensorflow/tensorboard/blob/master/docs/r2/tensorboard_quickstart.ipynb)を参考にした。
* リンク切れてる…。
* もともとは、[このツイート](https://twitter.com/random_forests/status/1100543755747241985?s=12)だったんだが、非公開にしちゃったのかな？

```          
!pip install -q tf-nightly-2.0-preview
# Load the TensorBoard notebook extension
%load_ext tensorboard.notebook 
```   

```
import tensorflow as tf
import datetime
```          

``` 
# Clear any logs from previous runs
!rm -rf ./logs/ 
``` 

``` 
mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

def create_model():
  return tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
  ])
``` 

``` 
model = create_model()
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

log_dir="logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
         
model.fit(x=x_train, 
          y=y_train, 
          epochs=5, 
          validation_data=(x_test, y_test), 
          callbacks=[tensorboard_callback])
```

```          
%tensorboard --logdir logs/fit
```
