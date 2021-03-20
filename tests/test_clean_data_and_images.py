import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import app.clean_data_and_images as c

def test_just_catch_errors():
    '''
    Just run the thing and if there are errors we will see.
    (Stupid test, but at least will catch big errors.)
    '''
    c.clean_csv_data_and_images()
    assert True