from pathlib import Path
from app.config import GPATH, READY_CSV_DIRECTORY, RANDOM_STATE, CLASSES, TRAINING_CONFIG as tc
import glob
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

def get_raw_dataframe():
    files = glob.glob("{}/*.csv".format(GPATH/READY_CSV_DIRECTORY))
    df = pd.concat((pd.read_csv(f) for f in files)).set_index('id')
    df = df[~df.index.duplicated(keep='first')]
    return df

def get_dataframe():
    df = get_raw_dataframe()

    # add filenames
    df['filenames'] = [str(x)+'.jpg' for x in df.index]

    # one hot encode
    for keyword in CLASSES:
        df[keyword] = np.where((df.keywords.str.contains(keyword, case=False) | df.description.str.contains(keyword, case=False)), 1, 0)
    df.drop(['keywords', 'description'], axis=1, inplace=True)

    df.sort_index(inplace=True)

    return df

def train_test_val_split(df):
    # split between train and test data
    X_train, X_test, y_train, y_test = train_test_split(df.filenames, df.drop(['filenames'], axis=1), test_size=tc.TEST_SIZE, random_state=RANDOM_STATE)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=tc.VAL_SIZE, random_state=RANDOM_STATE)

    # Make one df for train and one for test since that is what the generators need
    Xy_train = pd.concat([X_train, y_train], axis=1)
    Xy_test = pd.concat([X_test, y_test], axis=1)
    Xy_val = pd.concat([X_val, y_val], axis=1)

    return Xy_train, Xy_test, Xy_val

if __name__ == "__main__":
    print(get_dataframe().head(10))
