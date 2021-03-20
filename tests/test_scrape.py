import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import app.scrape as s

def test_scrape():
    s.scrape(search_term="seamless+pattern+floral", number_of_pages=1)
    assert True
