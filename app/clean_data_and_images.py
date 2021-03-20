'''

Will pull in ALL keyword data saved in the RAW_CSV_DIRECTORY and combine them into one nice csv for training.
If you don't want all that data included, remove them from that directory first.

Will remove unneccesary info, remove duplicates, etc.

'''
import pandas as pd
import json
import numpy as np
import os
from os import path
import glob
from app.config import GPATH, RAW_CSV_DIRECTORY, logging, READY_CSV_DIRECTORY, RAW_IMAGE_DIRECTORY
from pathlib import Path
from datetime import datetime
from app.clean_images import fix_all_with_threads

def clean_csv_data_and_images():

    # Read in all csvs from the RAW_CSV_DIRECTORY and concat them into one dataframe
    files = glob.glob("{}/*.csv".format(GPATH/RAW_CSV_DIRECTORY))
    logging.info("Globbing {} csvs for cleaning.".format(len(files)))
    df = pd.concat((pd.read_csv(f) for f in files))
    logging.info("The df has shape {}.".format(df.shape))

    df.set_index('id', inplace=True)

    # Drop duplicates (based on id)
    count_before = len(df.index)
    df = df[~df.index.duplicated(keep='first')]
    count_after = len(df.index)
    logging.info(f'Dropped {count_before-count_after} items with duplicate indices.')

    # Drop na
    df.dropna(inplace=True)

    # Keyword preprocessing
    k = df['keywords']
    k = k.str.replace(' ', '_')
    k = k.str.replace(',', ' ')
    df.keywords = k

    # Get the filenames of the images cleanly without any paths
    filenames_list = []
    for i, row in df.iterrows():
        try:
            filename = eval(row.images)[0]['path'].split('/')[1]
        except:
            filename = ""
        filenames_list.append(filename)
    df['filename'] = filenames_list
    # Drop the images column
    df.drop(['images', 'searchTerm', 'pageNum', 'contributer', 'type'], axis=1, inplace=True)

    # Ensure the files really are there
    badIds = []
    for i, row in df.iterrows():
        fn = GPATH/RAW_IMAGE_DIRECTORY/'full'/row.filename
        if not path.exists(fn):
            badIds.append(i)
    if len(badIds) > 0:
        logging.warning(f'Found {len(badIds)} ids with no image file. Dropping them from the cleaned df.')
        df.drop(badIds, inplace=True)
    else:
        logging.info('All files checked and exist while cleaning the data.')
    
    # Sort by index
    df.sort_index(inplace=True)
    print(df.info())

    # Clean the images
    fix_all_with_threads(df)

    # Drop a few more columns
    df.drop(['image_urls', 'filename'], axis=1, inplace=True)

    # Save out a compiled and cleaned csv
    now = datetime.now()
    timeString = now.strftime("%Y%m%d%H%M%S%f")
    csv_file_name = timeString + ".csv"

    full_path = GPATH/READY_CSV_DIRECTORY/csv_file_name
    df.to_csv(full_path)
    logging.info("The final df has shape {}.".format(df.shape))
    logging.info(f"Saving cleaned data to {full_path}.")

if __name__ == "__main__":
    clean_csv_data_and_images()
