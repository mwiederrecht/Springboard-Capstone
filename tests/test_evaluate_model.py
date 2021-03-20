import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import app.evaluate_model as e
from app.config import USE_MODEL

def test_model_meets_minimum_validity():
    analysis = e.evaluate_model(USE_MODEL)
    assert ((analysis.AVERAGE.iloc[0] > 0.85) and  # Average accuracy is > 0.85
           (analysis.AVERAGE.iloc[1] > 0.5) and    # MCC > 0.5
           (analysis.AVERAGE.iloc[2] > 0.5) and    # recall > 0.5
           (analysis.AVERAGE.iloc[3] > 0.5) and    # precision > 0.5
           (analysis.AVERAGE.iloc[4] > 0.5))       # f1 > 0.5
