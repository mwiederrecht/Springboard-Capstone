from app.config import GPATH, READY_IMAGE_DIRECTORY, MODELS_PATH, TRAINING_CONFIG as tc, CLASSES, RANDOM_STATE
import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import pandas as pd
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from numpy.random import seed
from keras.backend import manual_variable_initialization
from pathlib import Path
from app.data_gather import get_dataframe, train_test_val_split
from sklearn.metrics import roc_auc_score, recall_score, precision_score
from app.custom_loss_and_metrics import weighted_cross_entropy_fn, f1, MCC, binary_acc

def get_predictions(model, test_data):
    
    image_directory = GPATH/READY_IMAGE_DIRECTORY

    datagen = ImageDataGenerator(rescale = 1./255.)

    test_generator = datagen.flow_from_dataframe(dataframe=test_data,
                                                directory=image_directory,
                                                x_col="filenames",
                                                y_col=CLASSES,
                                                class_mode="raw",
                                                target_size=(224, 224),
                                                batch_size=tc.BATCH_SIZE,
                                                shuffle=False)
    
    pred = model.predict_generator(test_generator, verbose=1)
    filenames = test_generator.filenames
    predictions = list(zip(CLASSES, list(map(list, zip(*pred)))))
    with_filenames = [('Filename',filenames)] + predictions
    results = pd.DataFrame(dict(with_filenames))
    results['id'] = results.Filename.str.split('.', expand=True).iloc[:,0]
    results.id = pd.to_numeric(results.id)
    results.set_index('id', inplace=True)
    results.drop(columns=['Filename'], inplace=True)
    results.sort_index(inplace=True)
    return results

def evaluate(df, pred):
    true_column_names = [s + '_true' for s in CLASSES]
    column_renaming = dict(zip(CLASSES, true_column_names))
    df = df.rename(columns=column_renaming)
    df = pd.merge(pred, df, left_on='id', right_on='id', how='inner')

    acc_0_5_values = [np.round(binary_acc(df[c+"_true"].astype(float), df[c], 0.5), 2) for c in CLASSES]
    mcc_values = [np.round(MCC(df[c+"_true"].astype(float), df[c]).numpy(), 2) for c in CLASSES]
    recall_values = [np.round(recall_score(df[c+"_true"], np.rint(df[c])), 2) for c in CLASSES]
    precision_values = [np.round(precision_score(df[c+"_true"], np.rint(df[c])), 2) for c in CLASSES]
    f1_values = [np.round(f1(df[c+"_true"].astype(float), df[c]).numpy(), 2) for c in CLASSES]

    metrics_df = pd.DataFrame([acc_0_5_values, mcc_values, recall_values, precision_values, f1_values],
                        columns=CLASSES,
                        index=['acc_0.5', 'mcc', 'recall', 'precision', 'f1'])

    metrics_df['AVERAGE'] = np.round(metrics_df.mean(axis=1), 2)
    return metrics_df

def evaluate_model(model_file):
    seed(RANDOM_STATE)
    tf.random.set_seed(RANDOM_STATE)
    manual_variable_initialization(True)

    model = keras.models.load_model(GPATH/MODELS_PATH/model_file, compile=False)
    model.compile()

    df = get_dataframe()
    _, Xy_test, _ = train_test_val_split(df)

    Xy_test.sort_index(inplace=True)

    pred = get_predictions(model, Xy_test)
    analysis = evaluate(Xy_test, pred)
    print(analysis)
    return analysis

def evaluate_model_and_save(model_file):
    analysis = evaluate_model(model_file)
    print(analysis)
    filename = model_file.split(".")[0] + '_analysis.csv'
    full_path = GPATH/MODELS_PATH/filename
    analysis.to_csv(full_path)
    logging.info(f"Saved model analysis to {full_path}")

# if __name__ == "__main__":
#     evaluate_model_and_save(USE_MODEL)
