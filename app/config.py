from pathlib import Path
from app.helpers import dotdict

GPATH = Path(__file__).parent  # G for global.

import logging
LOG_FILE = 'logs/app.log'
logging.basicConfig(filename=GPATH/LOG_FILE, filemode='a', format='%(process)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

RANDOM_STATE = 24

# General
RAW_CSV_DIRECTORY = "data/csvs_raw"
READY_CSV_DIRECTORY = "data/csvs_ready"
RAW_IMAGE_DIRECTORY = "data/images_raw"
READY_IMAGE_DIRECTORY = "data/images_ready/full"
MODELS_PATH = "models"
REPORTS_PATH = "reports"
EXTRACTED_FEATURES_DIRECTORY = "data/extracted_features"

# Cleaning
MASK_IMAGE = "mask.png"
NUMBER_OF_THREADS_FOR_IMAGE_CLEANING = 10

# Classes
CLASSES = ["check", "damask", "ikat", "floral", "stripe", "geometric", "curve", "grungy", "marble", "terrazzo", "wavy", "pastel", "iridescent", "holographic", "linen", "butterfly", "tropical", "triangle", "star", "bird", "leaf", "abstract", "botanical", "white", "nature", "flower", "colorful", "summer", "color", "blue", "black", "line", "drawing", "trendy", "shape", "watercolor", "creative", "spring", "beautiful", "pink", "purple", "grunge", "ornate", "bright", "template", "cute", "plant", "natural", "textured", "simple", "ethnic", "green", "traditional", "old", "elegant", "paint", "artistic", "mosaic", "drawn", "hand", "classic", "garden", "exotic", "beauty", "light", "ornamental", "doodle", "blossom", "cloth", "monochrome", "tribal", "wave", "animal", "romantic", "cartoon", "elegance", "stone", "yellow", "effect", "luxury", "brush", "boho", "artwork", "floor", "jungle", "gradient", "sketch", "antique", "oriental", "silhouette", "palm", "set", "flora", "gray", "vibrant", "circle", "batik", "tree", "gold", "branch", "painting", "leaves", "rose", "organic", "baby", "foliage", "rock", "grey", "granite", "plaid", "lines", "victorian", "dark", "water", "wild", "rainbow", "hipster", "grid", "hawaii", "brown", "petal", "dye", "swirl", "bloom", "happy", "tropic", "rough", "beige", "baroque", "orange", "dot", "fantasy", "minimal", "folk", "diagonal", "checkered", "distressed", "bohemian", "pretty", "sea", "love", "tartan", "rustic", "zigzag", "chevron"] # That's 145

# Training
TRAINING_CONFIG = dotdict({
    "TEST_SIZE": 0.10,
    "VAL_SIZE": 0.10, # Out of what remains after test data is taken out
    "BATCH_SIZE": 8,
    "EPOCHS": 100,
    "LEARNING_RATE": 0.0003,
    "WEIGHTS": {0: 1., 1: 1.5},
    "SAVE_BEST_ONLY": False,    # If this is false, it will save a model every epoch
    "WIDTH_SHIFT_RANGE": 0.5,
    "HEIGHT_SHIFT_RANGE": 0.5,
    "HORIZONTAL_FLIP": True,
    "VERTICAL_FLIP": True,
    "ROTATION_RANGE": 360,
    "FILL_MODE": "wrap",
    "ZOOM_RANGE": [0.7, 1.3]
})

# Web App
USE_MODEL = "model-20210317160456894379-18-MCC0.58.hdf5"
STATIC_CONTENT_PATH = "static"
THRESHOLD_FOR_SHOWING_USER = 0.5
TMP_IMG_FILE = "tmp/saved_image.jpg"
