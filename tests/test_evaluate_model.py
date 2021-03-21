import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import app.evaluate_model as e
from app.config import USE_MODEL

def test_model_meets_minimum_validity():
    analysis = e.evaluate_model(USE_MODEL)
    assert ((analysis.AVERAGE.iloc[0] > 0.85) and  # Average accuracy
           (analysis.AVERAGE.iloc[1] >= 0.49) and    # MCC
           (analysis.AVERAGE.iloc[2] >= 0.49) and    # recall
           (analysis.AVERAGE.iloc[3] >= 0.49) and    # precision
           (analysis.AVERAGE.iloc[4] >= 0.49))       # f1
