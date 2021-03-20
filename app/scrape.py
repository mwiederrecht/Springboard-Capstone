'''
This is a wrapper for the command line call to scrapy (for web scraping).
If it is broken, it is likely because shutterstock changes their website constantly.

It pulls its arguments from config.py.

It should store csvs in the data/csvs directory and images in data/images_raw.  (Unless you changed the images directory in the config.)
'''
import os
import logging
from datetime import datetime
from app.config import SEARCH_TERM, GPATH, logging, RAW_CSV_DIRECTORY, CLASSES, STARTING_PAGE, USER_AGENT
from pathlib import Path

def scrape(search_term=SEARCH_TERM, number_of_pages=1):
    logging.info(f"Starting to scrape {search_term}.")
    now = datetime.now()
    timeString = now.strftime("%Y%m%d%H%M%S%f")

    start_url = 'https://www.shutterstock.com/search/'+search_term

    csv_file_name = timeString + "_" + search_term.replace("+", "_") + ".csv"

    csv_file_path = GPATH/RAW_CSV_DIRECTORY

    path_and_file = csv_file_path/csv_file_name

    command = "scrapy crawl shutterstock-spider -o \"file:///{}\":csv -a start_url=\"{}\" -a search_term=\"{}\" -a pages_to_scrape=\"{}\" -a starting_page=\"{}\" -a user_agent=\"{}\"".format(path_and_file, start_url, search_term, number_of_pages, STARTING_PAGE, USER_AGENT)
    
    logging.info(f"Scrape command: {command}")

    spider_path = GPATH/'app/scrapy'
    os.chdir(spider_path)
    os.system(command)

def scrape_all_classes(pages_per_class):
    logging.info(f"Scraping all classes with {pages_per_class} pages per class.")
    for c in CLASSES:
        sterm = 'seamless+pattern+' + c
        scrape(sterm, pages_per_class)

# if __name__ == "__main__":
#     pass
#     #fire.Fire()
#     #scrape(SEARCH_TERM, NUM_PAGES_TO_SCRAPE)
#     # scrape_all_classes(50)
