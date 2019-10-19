import os
import time

from pybman import utils
from pybman import extract
from pybman import LocalData
from pybman import DataSet

from .preprocess import clean
from ..utils.local import ld
from ..utils.paths import DATA_DIR, MPIS_DIR, PURE_DIR, TITLES_OUT

MPI_LANG = os.path.join(TITLES_OUT,'mpis-eng/')
MPI_LANG_YEARS = os.path.join(TITLES_OUT,'mpis-eng-years/')
MPI_LANG_GENRE_YEARS = os.path.join(TITLES_OUT,'mpis-eng-years-genre/')
CAT_LANG_YEARS = os.path.join(TITLES_OUT,'cats-eng-years/')

YEARS = list(range(2000,2020))

langs = utils.read_json(PURE_DIR + "lang/collection.json")
cat_ous = utils.read_json(MPIS_DIR + 'mapped/cat_ous.json')
# ous_ctx = utils.read_json(MPIS_DIR + 'mapped/ous_ctx.json')
ous_ctx = utils.read_json(DATA_DIR + 'base/ctx_sel.json')
cats = list(cat_ous.keys())
mpis = list(ous_ctx.keys())
cats.sort()
mpis.sort()

def titles_from_ctx_in_language(ctx_id='ctx_1542176', lang_id='eng'):
    total = ld.get_data(ctx_id)[0]
    data_set = DataSet(data_id=ctx_id+"_released", raw=total.get_items_released())
    lang_data = data_set.get_languages_data()
    if lang_id in lang_data:
        lang_records = lang_data[lang_id]
        lang_data = DataSet(data_id=ctx_id+'_'+lang_id, raw=lang_records)
        lang_titles = extract.titles_from_records(lang_data.records)
        return [clean(title) for title in lang_titles if clean(title)]
    else:
        print(ctx_id, "has no " + lang_id + " publications!")
        return {}

def titles_from_ctx_in_language_by_year(ctx_id='ctx_1542176', lang_id='eng'):
    total = ld.get_data(ctx_id)[0]
    data_set = DataSet(data_id=ctx_id+"_released", raw=total.get_items_released())
    lang_data = data_set.get_languages_data()
    if lang_id in lang_data:
        lang_records = lang_data[lang_id]
        lang_data = DataSet(data_id=ctx_id+'_'+lang_id, raw=lang_records)
        years_data = lang_data.get_years_data()
        lang_years_titles = {}
        for year in years_data:
            lang_year_data = DataSet(data_id=lang_id + '_' + year, raw=years_data[year])
            lang_year_titles = extract.titles_from_records(lang_year_data.records)
            lang_year_titles = [clean(title) for title in lang_year_titles if clean(title)]
            lang_years_titles[year] = lang_year_titles
        return lang_years_titles
    else:
        print(ctx_id, "has no " + lang_id + " publications!")
        return {}

def titles_from_ctx_in_language_and_genre_by_year(ctx_id='ctx_1542176', lang_id='eng', genre='ARTICLE'):
    total = ld.get_data(ctx_id)[0]
    data_set = DataSet(data_id=ctx_id+"_released", raw=total.get_items_released())
    genres = data_set.get_genre_data()
    if genre in genres:
        genr_data = DataSet(data_id=ctx_id+genre, raw=genres[genre])
        lang_data = genr_data.get_languages_data()
        if lang_id in lang_data:
            lang_records = lang_data[lang_id]
            lang_data = DataSet(data_id=ctx_id+'_'+lang_id, raw=lang_records)
            years_data = lang_data.get_years_data()
            lang_years_titles = {}
            for year in years_data:
                lang_year_data = DataSet(data_id=lang_id + '_' + year, raw=years_data[year])
                lang_year_titles = extract.titles_from_records(lang_year_data.records)
                lang_year_titles = [clean(title) for title in lang_year_titles if clean(title)]
                lang_years_titles[year] = lang_year_titles
            return lang_years_titles
        else:
            print(ctx_id, "has no " + lang_id + " publications with genre", genre + "!")
            return {}
    else:
        print(ctx_id, "has no publications with genre", genre + "!")
        return {}

def titles_from_mpis(lang_id='eng'):
    if not os.path.exists(MPI_LANG):
        os.makedirs(MPI_LANG)
    print("start extraction!")
    start_time = time.time()
    for mpi in mpis:
        print("")
        print("processing", mpi,"...")
        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx,"...")
            titles_lang = titles_from_ctx_in_language(mpi_ctx, lang_id='eng')
            if titles_lang:
                out_file = MPI_LANG + mpi + '_' + lang_id + '.txt'
                utils.write_list(out_file, titles_lang)
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))

def titles_from_mpis_by_year(lang_id='eng'):
    if not os.path.exists(MPI_LANG_YEARS):
        os.makedirs(MPI_LANG_YEARS)
    print("start extraction!")
    start_time = time.time()
    for mpi in mpis:
        print("")
        print("processing", mpi,"...")
        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx,"...")
            titles_lang_years = titles_from_ctx_in_language_by_year(mpi_ctx, lang_id='eng')
            out_prefix = MPI_LANG_YEARS + mpi + '_' + lang_id + '_'
            for year in YEARS:
                year = str(year)
                if year in titles_lang_years:
                    titles = titles_lang_years[year]
                    if titles:
                        out_file = out_prefix + year + '.txt'
                        utils.write_list(out_file, titles)
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))

def titles_from_mpis_in_genre_by_year(genre='ARTICLE', lang_id='eng'):
    if not os.path.exists(MPI_LANG_GENRE_YEARS):
        os.makedirs(MPI_LANG_GENRE_YEARS)
    print("start extraction!")
    start_time = time.time()
    for mpi in mpis:
        print("")
        print("processing", mpi,"...")
        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx,"...")
            titles_lang_years = titles_from_ctx_in_language_and_genre_by_year(mpi_ctx,genre=genre, lang_id='eng')
            out_prefix = MPI_LANG_GENRE_YEARS + mpi + '_' + lang_id + '_' + genre + '_'
            for year in YEARS:
                year = str(year)
                if year in titles_lang_years:
                    titles = titles_lang_years[year]
                    if titles:
                        out_file = out_prefix + year + '.txt'
                        utils.write_list(out_file, titles)
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))

def titles_from_cats_by_year():
    if not os.path.exists(CAT_LANG_YEARS):
        os.makedirs(CAT_LANG_YEARS)
    print("start extraction!")
    start_time = time.time()
    for cat in cats:
        print("")
        print("processing", cat,"...")
        cat_years_titles = {}
        ous = cat_ous[cat]
        for ou in ous:
            if ou in mpis:
                mpi_ctxs = ous_ctx[ou]
                for mpi_ctx in mpi_ctxs:
                    print("extracting", mpi_ctx,"...")
                    titles_lang_years = titles_from_ctx_in_language_by_year(mpi_ctx)
                    for year in YEARS:
                        year = str(year)
                        if year in titles_lang_years:
                            titles = titles_lang_years[year]
                            if year in cat_years_titles:
                                for title in titles:
                                    cat_years_titles[year].append(title)
                            else:
                                cat_years_titles[year] = []
                                for title in titles:
                                    cat_years_titles[year].append(title)
        for year in cat_years_titles:
            titles = cat_years_titles[year]
            out_prefix = CAT_LANG_YEARS + cat + '_eng_'
            out_file = out_prefix + year + '.txt'
            utils.write_list(out_file, titles)
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))
