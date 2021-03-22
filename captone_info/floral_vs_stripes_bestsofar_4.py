import os
from datetime import datetime
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from numpy import expand_dims
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.layers import Activation, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split

# loading in the data
df = pd.read_csv('33k_stripes_and_florals.csv')
df = df.set_index('id')

# labelling based on if it is floral or stripes
df['floral'] = np.where(df.keywords.str.contains('floral'), 1, 0)
df = df.drop(columns=['categories', 'type', 'contributer', 'description', 'keywords', 'image_urls'])
df = df.sample(frac=1)  # shuffle

# add filenames
df['filenames'] = [str(x)+'.jpg' for x in df.index]

# split between train and test data
X_train, X_test, y_train, y_test = train_test_split(df.filenames, df.floral, test_size=0.25, random_state=24)

# Make one df for train and one for test since that is what the generators need
Xy_train = pd.concat([X_train, y_train], axis=1)
Xy_train['stripe'] = np.where(y_train == 0, 1, 0)
Xy_test = pd.concat([X_test, y_test], axis=1)
Xy_test['stripe'] = np.where(y_test == 0, 1, 0)

# data generation
datagen = ImageDataGenerator()
datagen = ImageDataGenerator(width_shift_range=0.5,
                             height_shift_range=0.5,
                             horizontal_flip=True,
                             vertical_flip=True,
                             rotation_range=360,
                             fill_mode="wrap",
                             zoom_range=[0.7, 1.3])

train_generator = datagen.flow_from_dataframe(dataframe=Xy_train,
                                              directory="images_edited",
                                              x_col="filenames", y_col=["floral", "stripe"],
                                              class_mode="raw",
                                              target_size=(128, 128),
                                              batch_size=64)
test_generator = datagen.flow_from_dataframe(dataframe=Xy_test,
                                             directory="images_edited",
                                             x_col="filenames",
                                             y_col=["floral", "stripe"],
                                             class_mode="raw",
                                             target_size=(128, 128),
                                             batch_size=64)

model = Sequential()
model.add(Conv2D(32, 5, padding='same', input_shape=(128, 128, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(256, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(512, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.1))
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.1))
model.add(Dense(2, activation='linear'))
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=["acc"])
model.summary()

now = datetime.now()
timeString = now.strftime("%Y%m%d%H%M%S%f")

log_dir = "logs/fit/" + timeString
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

filepath = "model-" + timeString + "-{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint, tensorboard_callback]

history = model.fit_generator(generator=train_generator,
                              validation_data=test_generator,
                              epochs=300,
                              verbose=1,
                              callbacks=callbacks_list)

# model.predict(test_generator)