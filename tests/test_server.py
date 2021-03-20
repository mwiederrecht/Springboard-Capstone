import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import app.server as s
from PIL import Image
import math
import numpy as np

from app.config import GPATH

# Testing the prepare_image() function from server.py
def test_prepare_image():
    img = Image.open(GPATH/'tests/test_images/damask-seamless-pattern_1236-57.jpg')
    x = s.prepare_image(img, (224, 224))
    assert (math.isclose(x[0][0][0][0], 0.90588236, rel_tol=0.0001) and  # first item is correctish
           math.isclose(np.mean(x), 0.62827986, rel_tol=0.0001) and      # mean is correctish
           (np.max(x) <= 1.0) and (np.min(x) >= 0.0) and                 # all elements are between 0 and 1
           x.shape == (1, 224, 224, 3))                                  # array shape is right

# Testing the decode_predictions() function from server.py
def test_decode_predictions():
    preds = [[0.38273498, 0.0038811, 0.0239934, 0.00573327, 0.58115244,
              0.5090237, 0.03060067, 0.72172683, 0.15080863, 0.00202293,
              0.01625071, 0.00836794]]
    expected_results_beginning = '<ul><li><b>grungy</b> (0.72)</il>'
    assert (s.decode_predictions(preds[0]).startswith(expected_results_beginning))

