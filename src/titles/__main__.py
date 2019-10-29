import os
import sys
import time

from pybman import utils

from . import compile
from . import docterm

from ..utils.paths import LOG_DIR

print("start title extraction!")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

print("console output is redirected to titles.log ...")
stdout = sys.stdout
log = open(LOG_DIR + "titles.log", "w+")
sys.stdout = log

start = time.time()
print("----------------------------------------")
print("start extraction on", time.ctime(start))
print("")
print("#################")
print("## PREPARATION ##")
print("#################")
print("")
dirname, _ = os.path.split(os.path.abspath(__file__))
fpath = dirname + "/resources/genres.txt"
genres = utils.read_plain_clean(fpath)

print("")
print("##############")
print("## LANGUAGE ##")
print("##############")
print("")
print("extracting titles with shared language...")
compile.titles_from_lang()
compile.titles_from_lang(preprocess=True)
print("extracting titles with shared language and year...")
compile.titles_from_lang_by_year()
compile.titles_from_lang_by_year(preprocess=True)
print("extracting titles with shared language, year and genre...")
for g in genres:
    print("about to extract titles from records of type", g, "...")
    compile.titles_from_lang_in_genre_by_year(genre=g)
    compile.titles_from_lang_in_genre_by_year(genre=g, preprocess=True)

print("")
print("###############")
print("## INSTITUTE ##")
print("###############")
print("")
print("extracting titles of institutes with shared language...")
compile.titles_from_mpis()
compile.titles_from_mpis(preprocess=True)
print("extracting titles of institutes with shared language and year...")
compile.titles_from_mpis_by_year()
compile.titles_from_mpis_by_year(preprocess=True)
print("extracting titles of institutes with shared language, year and genre...")
for g in genres:
    compile.titles_from_mpis_by_genre(genre=g)
    compile.titles_from_mpis_by_genre(genre=g, preprocess=True)
    compile.titles_from_mpis_in_genre_by_year(genre=g)
    compile.titles_from_mpis_in_genre_by_year(genre=g, preprocess=True)

print("")
print("##############")
print("## CATEGORY ##")
print("##############")
print("")
print("extracting titles of categories with shared language...")
compile.titles_from_cats()
compile.titles_from_cats(preprocess=True)
print("extracting titles of categories with shared language and year...")
compile.titles_from_cats_by_year()
compile.titles_from_cats_by_year(preprocess=True)
print("extracting titles of categories with shared language, year and genre...")
for g in genres:
    compile.titles_from_cats_in_genre_by_year(genre=g)
    compile.titles_from_cats_in_genre_by_year(genre=g, preprocess=True)

done = time.time()
print("----------------------------------------")
print("finished extraction on", time.ctime(done))
print("after", round((done - start) / 60, 2), "minutes!")
start = time.time()
print("----------------------------------------")
print("start building documents on", time.ctime(start))
docterm.routine()
done = time.time()
print("finished building documents on", time.ctime(done))
print("after", round((done - start) / 60, 2), "minutes!")
start = time.time()
print("----------------------------------------")

log.close()
sys.stdout = stdout

print("all done!")
