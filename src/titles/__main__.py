import os
import sys
import time

from ..utils.paths import LOG_DIR

print("start extraction of titles!")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

print("console output is redirected to titles.log ...")
stdout = sys.stdout
log = open(LOG_DIR + "titles.log", "w+")
sys.stdout = log

start = time.time()
print("----------------------------------------")
print("start extraction on",time.ctime(start))

from .compile import *

titles_from_mpis()
titles_from_cats_by_year()
titles_from_mpis_by_year()

from pybman import utils

dirname, _ = os.path.split(os.path.abspath(__file__))
fpath = dirname + "/resources/genres.txt"
genres = utils.read_plain_clean(fpath)

for g in genres:
    titles_from_mpis_in_genre_by_year(genre=g)

# titles_from_mpis_in_genre_by_year(genre='ARTICLE')
# titles_from_mpis_in_genre_by_year(genre='BOOK_ITEM')

done = time.time()
print("----------------------------------------")
print("finished extraction on",time.ctime(done))
print("after", round((done - start) / 60, 2), "minutes!")

log.close()
sys.stdout = stdout

print("finished extraction after %s min!" % round((done - start)/60, 2))
