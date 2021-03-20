from datetime import datetime
import tensorflow as tf
import logging
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras import applications
from keras.callbacks import ModelCheckpoint
from pathlib import Path
from app.config import GPATH, logging, RANDOM_STATE, MODELS_PATH, CLASSES, USE_MODEL, READY_IMAGE_DIRECTORY
from app.config import TRAINING_CONFIG as tc
from app.custom_loss_and_metrics import weighted_cross_entropy_fn, f1, MCC
from app.data_gather import get_dataframe, train_test_val_split
from numpy.random import seed
from keras.backend import manual_variable_initialization

def train_from_ResNet50_imagenet_weights():
    logging.info("About to train a new resnet50 model from imagenet weights")
    model = Sequential()
    model.add(applications.ResNet50(include_top=False, weights='imagenet', pooling="avg"))
    model.add(Dense(len(CLASSES), activation='sigmoid'))
    return train_model(model)

def train_from_hdf5_file(filename=USE_MODEL):
    logging.info(f"About to start training again from {USE_MODEL}")
    # These three lines are attempting to prevent a weird keras bug where a
    #    model that is read in gets its weights randomized
    seed(RANDOM_STATE)
    tf.random.set_seed(RANDOM_STATE)
    manual_variable_initialization(True)

    full_path = GPATH/MODELS_PATH/filename

    model = keras.models.load_model(full_path, compile=False)
    model.load_weights(full_path)
    return train_model(model)

def train_model(model):
    logging.info("Starting train_model method")
    imageDirectory = GPATH/READY_IMAGE_DIRECTORY

    df = get_dataframe()
    logging.info("gathered dataframe")

    Xy_train, __, Xy_val = train_test_val_split(df)
    logging.info("split data between train and test and val")

    # data generation
    datagen = ImageDataGenerator(rescale=1./255.,
                                width_shift_range=tc.WIDTH_SHIFT_RANGE,
                                height_shift_range=tc.HEIGHT_SHIFT_RANGE,
                                horizontal_flip=tc.HORIZONTAL_FLIP,
                                vertical_flip=tc.VERTICAL_FLIP,
                                rotation_range=tc.ROTATION_RANGE,
                                fill_mode=tc.FILL_MODE,
                                zoom_range=tc.ZOOM_RANGE)

    train_generator = datagen.flow_from_dataframe(dataframe=Xy_train,
                                                directory=imageDirectory,
                                                x_col="filenames",
                                                y_col=CLASSES,
                                                class_mode="raw",
                                                target_size=(224, 224),
                                                batch_size=tc.BATCH_SIZE)
    val_generator = datagen.flow_from_dataframe(dataframe=Xy_val,
                                                directory=imageDirectory,
                                                x_col="filenames",
                                                y_col=CLASSES,
                                                class_mode="raw",
                                                target_size=(224, 224),
                                                batch_size=tc.BATCH_SIZE)

    model.compile(optimizer=keras.optimizers.Adam(learning_rate=tc.LEARNING_RATE),
                loss=weighted_cross_entropy_fn,
                metrics=[tf.keras.metrics.BinaryAccuracy(threshold=0.5, name="acc"),
                        tf.keras.metrics.AUC(),
                        tf.keras.metrics.Recall(),
                        tf.keras.metrics.Precision(),
                        f1,
                        MCC])
    model.summary()
    logging.info("compiled model")

    now = datetime.now()
    timeString = now.strftime("%Y%m%d%H%M%S%f")

    log_dir = GPATH/"logs/fit"/timeString
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    filepath = str(GPATH/MODELS_PATH) + "/model-" + timeString + "-{epoch:02d}-MCC{val_MCC:.2f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor="val_MCC", verbose=1, save_best_only=tc.SAVE_BEST_ONLY, mode='max')
    callbacks_list = [checkpoint, tensorboard_callback]
    
    logging.info(f"Time is {timeString} and starting to train.")

    model.fit_generator(generator=train_generator,
                                validation_data=val_generator,
                                epochs=tc.EPOCHS,
                                verbose=1,
                                callbacks=callbacks_list)
    
    return model



# if __name__ == "__main__":
#     train_from_ResNet50_imagenet_weights()
#     #train_from_hdf5_file('model-20210317133056242979-06-MCC0.54.hdf5')