from app.config import GPATH, REPORTS_PATH, logging
from app.data_gather import get_raw_dataframe, get_dataframe, train_test_val_split
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from app.helpers import get_timestring

def report_class_counts():
    df = get_dataframe().drop(['filenames'], axis=1)
    class_counts = df.sum()
    filename = get_timestring() + "_class_counts.csv"
    full_path = GPATH/REPORTS_PATH/filename
    class_counts.to_csv(full_path)
    logging.info(f"Saved class count report to {full_path}")
    print(f"Report saved to {full_path}")

def report_ALL_keyword_counts():
    df = get_raw_dataframe()
    k = df['keywords']
    k = k.str.replace(' ', '_')
    k = k.str.replace(',', ' ')
    cv = CountVectorizer()
    data_cv = cv.fit_transform(k)
    data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_dtm.index = k.index
    summed = data_dtm[0:50000].sum()
    summed2 = data_dtm[51000:].sum()
    summed_all = summed+summed2
    sorted_df = summed_all.sort_values(ascending=False)
    top_1000 = sorted_df.head(1000)
    filename = get_timestring() + "_top_1k_keywords.csv"
    full_path = GPATH/REPORTS_PATH/filename
    top_1000.to_csv(full_path)
    logging.info(f"Saved report of ALL keywords counts from data in the csvs_ready directory to {full_path}")
    print(f"Report saved to {full_path}")

# if __name__ == "__main__":
#     report_class_counts()
