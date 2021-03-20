from PIL import Image
import requests
from io import BytesIO
import threading
import logging
from pathlib import Path
from app.config import GPATH, RAW_IMAGE_DIRECTORY, MASK_IMAGE, READY_IMAGE_DIRECTORY, NUMBER_OF_THREADS_FOR_IMAGE_CLEANING, logging
from os import path

def fix_one_image(df, num):
    try:
        row = df.iloc[num,]
        url = row.image_urls
        image_id = row.name

        local_full_path = GPATH/RAW_IMAGE_DIRECTORY/'full'/row.filename

        image = Image.open(local_full_path)
        image = image.crop((0,0,image.size[0], image.size[1]-20))

        thumnail_url = url.replace('600w', '260nw')
        response = requests.get(thumnail_url)
        thumnail = Image.open(BytesIO(response.content))
        thumnail = thumnail.crop((0,0,thumnail.size[0], thumnail.size[1]-20))
        thumnail = thumnail.resize(image.size)

        mask = Image.open(GPATH/MASK_IMAGE)
        big_mask = Image.new('RGBA', image.size, (0,0,0,0))
        big_mask.paste(mask, (int((big_mask.size[0]/2)-(mask.size[0]/2)), int((big_mask.size[1]/2)-(mask.size[1]/2))))

        fixed = image.copy()
        fixed.paste(thumnail, mask=big_mask)

        fixed.save(GPATH/READY_IMAGE_DIRECTORY/str(str(image_id) + '.jpg'))
    except:
        logging.error(f"Problem cleaning image {image_id}.")

def fix_many(df, start, end):
    for i in range(start, end):
        fix_one_image(df, i)

def fix_all_with_threads(df):
    notYetCleaned = []
    for i, row in df.iterrows():
        fn = (GPATH/READY_IMAGE_DIRECTORY/str(row.name)).with_suffix(".jpg")
        if not path.exists(fn):
            notYetCleaned.append(i)

    df = df.loc[notYetCleaned]

    number_to_do = len(df.index)
    per_thread = int(number_to_do/NUMBER_OF_THREADS_FOR_IMAGE_CLEANING)

    for i in range(0,NUMBER_OF_THREADS_FOR_IMAGE_CLEANING):
        if i < NUMBER_OF_THREADS_FOR_IMAGE_CLEANING-1:
            threading.Thread( target=fix_many, args=(df, i*per_thread, (i+1)*per_thread) ).start()
        else:
            threading.Thread( target=fix_many, args=(df, i*per_thread, number_to_do) ).start()

    for thread in threading.enumerate():
        if thread == threading.current_thread():
            continue
        thread.join()
    logging.info('Threads joined')
