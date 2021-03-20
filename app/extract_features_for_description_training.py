from app.config import RANDOM_STATE, GPATH, MODELS_PATH, USE_MODEL, READY_IMAGE_DIRECTORY, EXTRACTED_FEATURES_DIRECTORY
import os
import tensorflow as tf
import pandas as pd
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from numpy.random import seed
from keras.backend import manual_variable_initialization
import app.helpers

from tensorflow.compat.v1.keras.backend import set_session
configtf = tf.compat.v1.ConfigProto()
configtf.gpu_options.allow_growth = True
configtf.log_device_placement = True
sess = tf.compat.v1.Session(config=configtf)
set_session(sess)

def extract_features():
    seed(RANDOM_STATE); tf.random.set_seed(RANDOM_STATE); manual_variable_initialization(True)
    my_model = keras.models.load_model(GPATH/MODELS_PATH/USE_MODEL, compile=False)
    my_model.compile()
    my_model = my_model.get_layer('resnet50')

    datagen = ImageDataGenerator(rescale = 1./255.)
    image_gen = datagen.flow_from_directory((GPATH/READY_IMAGE_DIRECTORY).parent,
                                            class_mode=None,
                                            target_size=(224, 224),
                                            batch_size=32,
                                            shuffle=False)
    image_gen.reset()
    pred_my_model = pd.DataFrame(my_model.predict_generator(image_gen, verbose=1))
    filenames = image_gen.filenames
    df_all = pred_my_model
    df_all['Filename'] = filenames
    df_all['Filename'] = df_all.Filename.str.split('\\', expand=True).iloc[:,1]
    df_all['id'] = df_all.Filename.str.split('.', expand=True).iloc[:,0]
    df_all.id = pd.to_numeric(df_all.id)
    df_all.set_index('id', inplace=True)
    df_all.drop(columns=['Filename'], inplace=True)
    df_all.columns = [str(i) for i in range(0, len(df_all.columns))]
    df_all = df_all.loc[:, (df_all != 0).any(axis=0)]
    return df_all

def extract_features_and_save_csv():
    ALL_features = extract_features()
    ALL_features.to_csv((GPATH/EXTRACTED_FEATURES_DIRECTORY/str(helpers.get_timestring())).with_suffix('.csv'))
    print("saved the csv file")

if __name__ == "__main__":
    extract_features_and_save_csv()
