import os
import time

from pybman import utils
from pybman import extract
from pybman import DataSet

from .preprocess import clean

from ..utils.local import ld
from ..utils.paths import DATA_DIR, MPIS_DIR, PURE_DIR, TITLES_OUT

ALL_LANG = os.path.join(TITLES_OUT, 'all-lang/')
ALL_LANG_YEARS = os.path.join(TITLES_OUT, 'all-lang-year/')
ALL_LANG_GENRE = os.path.join(TITLES_OUT, 'all-lang-genre/')
ALL_LANG_YEARS_GENRE = os.path.join(TITLES_OUT, 'all-lang-year-genre/')

MPI_LANG = os.path.join(TITLES_OUT, 'mpi-lang/')
MPI_LANG_YEARS = os.path.join(TITLES_OUT, 'mpi-lang-year/')
MPI_LANG_GENRE = os.path.join(TITLES_OUT, 'mpi-lang-genre/')
MPI_LANG_YEARS_GENRE = os.path.join(TITLES_OUT, 'mpi-lang-year-genre/')

PERS_LANG = os.path.join(TITLES_OUT, 'pers-lang/')
PERS_LANG_YEARS = os.path.join(TITLES_OUT, 'pers-lang-year/')
PERS_LANG_GENRE = os.path.join(TITLES_OUT, 'pers-lang-genre/')
PERS_LANG_YEARS_GENRE = os.path.join(TITLES_OUT, 'pers-lang-year-genre/')

CAT_LANG = os.path.join(TITLES_OUT, 'cat-lang/')
CAT_LANG_YEARS = os.path.join(TITLES_OUT, 'cat-lang-year/')
CAT_LANG_YEARS_GENRE = os.path.join(TITLES_OUT, 'cat-lang-year-genre/')

YEARS = list(range(2000, 2020))

langs = utils.read_json(PURE_DIR + "lang/collection.json")
cat_ous = utils.read_json(MPIS_DIR + 'mapped/cat_ous.json')
ous_ctx = utils.read_json(DATA_DIR + 'base/ctx_sel.json')
cats = list(cat_ous.keys())
mpis = list(ous_ctx.keys())
cats.sort()
mpis.sort()


def titles_from_ctx_in_language(ctx_id='ctx_1542176', lang_id='eng', preprocess=True):
    total = ld.get_data(ctx_id)[0]
    data_set = DataSet(data_id=ctx_id+"_released", raw=total.get_items_released())
    lang_data = data_set.get_languages_data()
    if lang_id in lang_data:
        lang_records = lang_data[lang_id]
        lang_data = DataSet(data_id=ctx_id+'_'+lang_id, raw=lang_records)
        lang_titles = extract.titles_from_records(lang_data.records)
        if preprocess:
            lang_titles = [clean(title) for title in lang_titles if clean(title)]
        return lang_titles
    else:
        print(ctx_id, "has no " + lang_id + " publications!")
        return []


def titles_from_ctx_in_language_by_year(ctx_id='ctx_1542176', lang_id='eng', preprocess=True):
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
            if preprocess:
                lang_year_titles = [clean(title) for title in lang_year_titles if clean(title)]
            lang_years_titles[year] = lang_year_titles
        return lang_years_titles
    else:
        print(ctx_id, "has no " + lang_id + " publications!")
        return {}


def titles_from_ctx_in_language_and_genre(ctx_id='ctx_1542176', lang_id='eng', genre='ARTICLE', preprocess=True):
    total = ld.get_data(ctx_id)[0]
    data_set = DataSet(data_id=ctx_id+"_released", raw=total.get_items_released())
    genres = data_set.get_genre_data()
    if genre in genres:
        genre_data = DataSet(data_id=ctx_id+genre, raw=genres[genre])
        lang_data = genre_data.get_languages_data()
        if lang_id in lang_data:
            lang_records = lang_data[lang_id]
            lang_data = DataSet(data_id=ctx_id+'_'+lang_id, raw=lang_records)
            lang_titles = extract.titles_from_records(lang_data.records)
            if preprocess:
                lang_titles = [clean(title) for title in lang_titles if clean(title)]
            return lang_titles
        else:
            print(ctx_id, "has no " + lang_id + " publications with genre", genre + "!")
            return []
    else:
        print(ctx_id, "has no publications with genre", genre + "!")
        return []


def titles_from_ctx_in_language_and_genre_by_year(ctx_id='ctx_1542176', lang_id='eng', genre='ARTICLE', preprocess=True):
    total = ld.get_data(ctx_id)[0]
    data_set = DataSet(data_id=ctx_id+"_released", raw=total.get_items_released())
    genres = data_set.get_genre_data()
    if genre in genres:
        genre_data = DataSet(data_id=ctx_id+genre, raw=genres[genre])
        lang_data = genre_data.get_languages_data()
        if lang_id in lang_data:
            lang_records = lang_data[lang_id]
            lang_data = DataSet(data_id=ctx_id+'_'+lang_id, raw=lang_records)
            years_data = lang_data.get_years_data()
            lang_years_titles = {}
            for year in years_data:
                lang_year_data = DataSet(data_id=lang_id + '_' + year, raw=years_data[year])
                lang_year_titles = extract.titles_from_records(lang_year_data.records)
                if preprocess:
                    lang_year_titles = [clean(title) for title in lang_year_titles if clean(title)]
                lang_years_titles[year] = lang_year_titles
            return lang_years_titles
        else:
            print(ctx_id, "has no " + lang_id + " publications with genre", genre + "!")
            return {}
    else:
        print(ctx_id, "has no publications with genre", genre + "!")
        return {}

def titles_from_ctx_in_language_by_person(ctx_id='ctx_1542176', lang_id='eng', preprocess=True):
    total = ld.get_data(ctx_id)[0]
    data_set = DataSet(data_id=ctx_id+"_released", raw=total.get_items_released())
    lang_data = data_set.get_languages_data()
    if lang_id in lang_data:
        lang_records = lang_data[lang_id]
        lang_data = DataSet(data_id=ctx_id+'_'+lang_id, raw=lang_records)
        creator_rec = lang_data.get_creators_data()
        creators = list(creator_rec.keys())
        creator_titles = {}
        creators.sort()
        for c in creators:
            titles = extract.titles_from_records(creator_rec[c])
            if preprocess:
                titles = [clean(title) for title in titles if clean(title)]
            creator_titles[c] = titles
        return creator_titles
    else:
        print(ctx_id, "has no " + lang_id + " publications!")
        return {}


def titles_from_ctx_in_language_by_person_and_year(ctx_id='ctx_1542176', lang_id='eng', preprocess=True):
    total = ld.get_data(ctx_id)[0]
    data_set = DataSet(data_id=ctx_id+"_released", raw=total.get_items_released())
    lang_data = data_set.get_languages_data()
    if lang_id in lang_data:
        lang_records = lang_data[lang_id]
        lang_data = DataSet(data_id=ctx_id+'_'+lang_id, raw=lang_records)
        creator_rec = lang_data.get_creators_data()
        creators = list(creator_rec.keys())
        creator_titles = {}
        creators.sort()
        for c in creators:
            creator_titles[c] = {}
            creator_data = DataSet(data_id=ctx_id+"_subset", raw=creator_rec[c])
            years_data = creator_data.get_years_data()
            for year in years_data:
                titles = extract.titles_from_records(years_data[year])
                if preprocess:
                    titles = [clean(title) for title in titles if clean(title)]
                creator_titles[c][year] = titles
        return creator_titles
    else:
        print(ctx_id, "has no " + lang_id + " publications!")
        return {}


def titles_from_ctx_in_language_by_person_from_genre(ctx_id='ctx_1542176', lang_id='eng', genre='ARTICLE', preprocess=True):
    total = ld.get_data(ctx_id)[0]
    data_set = DataSet(data_id=ctx_id+"_released", raw=total.get_items_released())
    genres = data_set.get_genre_data()
    if genre in genres:
        genre_data = DataSet(data_id=ctx_id+genre, raw=genres[genre])
        lang_data = genre_data.get_languages_data()
        if lang_id in lang_data:
            lang_records = lang_data[lang_id]
            lang_data = DataSet(data_id=ctx_id+'_'+lang_id, raw=lang_records)
            creator_rec = lang_data.get_creators_data()
            creators = list(creator_rec.keys())
            creator_titles = {}
            creators.sort()
            for c in creators:
                titles = extract.titles_from_records(creator_rec[c])
                if preprocess:
                    titles = [clean(title) for title in titles if clean(title)]
                creator_titles[c] = titles
            return creator_titles
        else:
            print(ctx_id, "has no " + lang_id + " publications!")
            return {}
    else:
        print(ctx_id, "has no publications with genre", genre + "!")
        return {}


def titles_from_ctx_in_language_by_person_from_genre_by_year(ctx_id='ctx_1542176', lang_id='eng', genre='ARTICLE', preprocess=True):
    total = ld.get_data(ctx_id)[0]
    data_set = DataSet(data_id=ctx_id+"_released", raw=total.get_items_released())
    genres = data_set.get_genre_data()
    if genre in genres:
        genre_data = DataSet(data_id=ctx_id+genre, raw=genres[genre])
        lang_data = genre_data.get_languages_data()
        if lang_id in lang_data:
            lang_records = lang_data[lang_id]
            lang_data = DataSet(data_id=ctx_id+'_'+lang_id, raw=lang_records)
            creator_rec = lang_data.get_creators_data()
            creators = list(creator_rec.keys())
            creator_titles = {}
            creators.sort()
            for c in creators:
                creator_titles[c] = {}
                creator_data = DataSet(data_id=ctx_id+"_subset", raw=creator_rec[c])
                years_data = creator_data.get_years_data()
                for year in years_data:
                    titles = extract.titles_from_records(years_data[year])
                    if preprocess:
                        titles = [clean(title) for title in titles if clean(title)]
                    creator_titles[c][year] = titles
            return creator_titles
        else:
            print(ctx_id, "has no " + lang_id + " publications!")
            return {}
    else:
        print(ctx_id, "has no publications with genre", genre + "!")
        return {}


def titles_from_lang(lang_id='eng', preprocess=False):
    if not os.path.exists(ALL_LANG):
        os.makedirs(ALL_LANG)
    out_prefix = ALL_LANG + lang_id
    if not preprocess:
        out_prefix += "_raw"
    out_file = out_prefix + '.txt'
    f = open(out_file, 'w', encoding="utf8")
    print("start extraction!")
    start_time = time.time()
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            titles = titles_from_ctx_in_language(mpi_ctx,
                                                 lang_id=lang_id,
                                                 preprocess=preprocess)
            if titles:
                f.write("\n".join(titles) + "\n")
    f.close()
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_lang_in_genre(genre='ARTICLE', lang_id='eng', preprocess=False):
    if not os.path.exists(ALL_LANG_GENRE):
        os.makedirs(ALL_LANG_GENRE)
    print("start extraction!")
    start_time = time.time()
    init = True
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            titles =\
                titles_from_ctx_in_language_and_genre(mpi_ctx,
                                                      genre=genre,
                                                      lang_id=lang_id,
                                                      preprocess=preprocess)
            out_base = ALL_LANG_GENRE + lang_id + '_' + genre
            if titles:
                out_prefix = ALL_LANG_GENRE + lang_id + '_' + genre
                if not preprocess:
                    out_prefix += '_raw'
                out_file = out_prefix + '.txt'
                if init:
                    with open(out_file, 'w', encoding="UTF-8") as f:
                        f.write("\n".join(titles) + "\n")
                    init = False
                else:
                    with open(out_file, 'a', encoding="UTF-8") as f:
                        f.write("\n".join(titles) + "\n")
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_lang_by_year(lang_id='eng', preprocess=False):
    if not os.path.exists(ALL_LANG_YEARS):
        os.makedirs(ALL_LANG_YEARS)
    out_base = ALL_LANG_YEARS + lang_id + '_'
    print("start extraction!")
    start_time = time.time()
    init = {}
    for year in YEARS:
        init[str(year)] = True
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        mpi_ctxs = ous_ctx[mpi]
        
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            titles_lang_years = titles_from_ctx_in_language_by_year(mpi_ctx,
                                                                    lang_id=lang_id,
                                                                    preprocess=preprocess)
            for year in YEARS:
                year = str(year)
                if year in titles_lang_years:
                    titles = titles_lang_years[year]
                    if titles:
                        out_prefix = out_base + year
                        if not preprocess:
                            out_prefix += '_raw'
                        out_file = out_prefix + '.txt'
                        if init[year]:
                            with open(out_file, 'w', encoding="UTF-8") as f:
                                f.write("\n".join(titles) + "\n")
                            init[year] = False
                        else:
                            with open(out_file, 'a', encoding="UTF-8") as f:
                                f.write("\n".join(titles) + "\n")
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_lang_in_genre_by_year(genre='ARTICLE', lang_id='eng', preprocess=False):
    if not os.path.exists(ALL_LANG_YEARS_GENRE):
        os.makedirs(ALL_LANG_YEARS_GENRE)
    print("start extraction!")
    start_time = time.time()
    init = {}
    for year in YEARS:
        init[str(year)] = True
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            titles_lang_years =\
                titles_from_ctx_in_language_and_genre_by_year(mpi_ctx,
                                                              genre=genre,
                                                              lang_id=lang_id,
                                                              preprocess=preprocess)
            out_base = ALL_LANG_YEARS_GENRE + lang_id + '_' + genre + '_'
            for year in YEARS:
                year = str(year)
                if year in titles_lang_years:
                    titles = titles_lang_years[year]
                    if titles:
                        out_prefix = out_base + year
                        if not preprocess:
                            out_prefix += '_raw'
                        out_file = out_prefix + '.txt'
                        if init[year]:
                            with open(out_file, 'w', encoding="UTF-8") as f:
                                f.write("\n".join(titles) + "\n")
                            init[year] = False
                        else:
                            with open(out_file, 'a', encoding="UTF-8") as f:
                                f.write("\n".join(titles) + "\n")
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_mpis(lang_id='eng', preprocess=False):
    if not os.path.exists(MPI_LANG):
        os.makedirs(MPI_LANG)
    print("start extraction!")
    start_time = time.time()
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        mpi_ctxs = ous_ctx[mpi]
        out_prefix = MPI_LANG + mpi + '_' + lang_id
        if not preprocess:
            out_prefix += '_raw'
        out_file = out_prefix + '.txt'
        first = True
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            titles = titles_from_ctx_in_language(mpi_ctx,
                                                 lang_id=lang_id,
                                                 preprocess=preprocess)
            if titles:
                if first:
                    with open(out_file, 'w', encoding="UTF-8") as f:
                        f.write("\n".join(titles) + "\n")
                    first = False
                else:
                    with open(out_file, 'a', encoding="UTF-8") as f:
                        f.write("\n".join(titles) + "\n")
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_mpis_by_year(lang_id='eng', preprocess=False):
    if not os.path.exists(MPI_LANG_YEARS):
        os.makedirs(MPI_LANG_YEARS)
    print("start extraction!")
    start_time = time.time()
    init = {}
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        for year in YEARS:
            init[str(year)] = True
        mpi_ctxs = ous_ctx[mpi]
        out_base = MPI_LANG_YEARS + mpi + '_' + lang_id + '_'
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            titles_lang_years = titles_from_ctx_in_language_by_year(mpi_ctx,
                                                                    lang_id=lang_id,
                                                                    preprocess=preprocess)
            for year in YEARS:
                year = str(year)
                if year in titles_lang_years:
                    titles = titles_lang_years[year]
                    if titles:
                        out_prefix = out_base + year
                        if not preprocess:
                            out_prefix += '_raw'
                        out_file = out_prefix + '.txt'
                        if init[year]:
                            with open(out_file, 'w', encoding="UTF-8") as f:
                                f.write("\n".join(titles) + "\n")
                            init[year] = False
                        else:
                            with open(out_file, 'a', encoding="UTF-8") as f:
                                f.write("\n".join(titles) + "\n")
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_mpis_by_genre(genre='ARTICLE', lang_id='eng', preprocess=False):
    if not os.path.exists(MPI_LANG_GENRE):
        os.makedirs(MPI_LANG_GENRE)
    print("start extraction!")
    start_time = time.time()
    init = True
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            titles = titles_from_ctx_in_language_and_genre(mpi_ctx,
                                                           genre=genre,
                                                           lang_id=lang_id,
                                                           preprocess=preprocess)
            if titles:
                out_prefix = MPI_LANG_GENRE + mpi + '_' + genre
                if not preprocess:
                    out_prefix += '_raw'
                out_file = out_prefix + '.txt'
                if init:
                    with open(out_file, 'w', encoding="UTF-8") as f:
                        f.write("\n".join(titles) + "\n")
                    init = False
                else:
                    with open(out_file, 'a', encoding="UTF-8") as f:
                        f.write("\n".join(titles) + "\n")
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_mpis_in_genre_by_year(genre='ARTICLE', lang_id='eng', preprocess=False):
    if not os.path.exists(MPI_LANG_YEARS_GENRE):
        os.makedirs(MPI_LANG_YEARS_GENRE)
    print("start extraction!")
    start_time = time.time()
    init = {}
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        for year in YEARS:
            init[str(year)] = True
        mpi_ctxs = ous_ctx[mpi]
        out_base = MPI_LANG_YEARS_GENRE + mpi + '_' + lang_id + '_' + genre + '_'
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            titles_lang_years = titles_from_ctx_in_language_and_genre_by_year(mpi_ctx,
                                                                              genre=genre,
                                                                              lang_id=lang_id,
                                                                              preprocess=preprocess)
            for year in YEARS:
                year = str(year)
                if year in titles_lang_years:
                    titles = titles_lang_years[year]
                    if titles:
                        out_prefix = out_base + year
                        if not preprocess:
                            out_prefix += '_raw'
                        out_file = out_prefix + '.txt'
                        if init[year]:
                            with open(out_file, 'w', encoding="UTF-8") as f:
                                f.write("\n".join(titles) + "\n")
                            init[year] = False
                        else:
                            with open(out_file, 'a', encoding="UTF-8") as f:
                                f.write("\n".join(titles) + "\n")
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_persons(lang_id='eng', preprocess=False):
    if not os.path.exists(PERS_LANG):
        os.makedirs(PERS_LANG)
    written = {}
    print("start extraction!")
    start_time = time.time()
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            pers_titles = titles_from_ctx_in_language_by_person(mpi_ctx,
                                                                lang_id=lang_id,
                                                                preprocess=preprocess)
            for pers in pers_titles:
                titles = pers_titles[pers]
                if len(titles) > 1:
                    if pers in written:
                        out_file = written[pers]
                        with open(out_file, 'a', encoding="UTF-8") as f:
                            f.write("\n".join(titles) + "\n")
                    else:
                        out_prefix = PERS_LANG + pers + "_" + lang_id
                        if not preprocess:
                            out_prefix += '_raw'
                        out_file = out_prefix + '.txt'
                        with open(out_file, 'w', encoding="UTF-8") as f:
                            f.write("\n".join(titles) + "\n")
                        written[pers] = out_file
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_persons_by_year(lang_id='eng', preprocess=False):
    if not os.path.exists(PERS_LANG_YEARS):
        os.makedirs(PERS_LANG_YEARS)
    out_base = PERS_LANG_YEARS
    print("start extraction!")
    start_time = time.time()
    written = {}
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            titles_lang_pers_years = titles_from_ctx_in_language_by_person_and_year(mpi_ctx,
                                                                                    lang_id=lang_id,
                                                                                    preprocess=preprocess)
            for pers in titles_lang_pers_years:
                out_pers_base = out_base + pers + "_" + lang_id + "_"
                for year in YEARS:
                    year = str(year)
                    if year in titles_lang_pers_years[pers]:
                        titles = titles_lang_pers_years[pers][year]
                        if titles:
                            out_prefix = out_pers_base + year
                            if not preprocess:
                                out_prefix += '_raw'
                            if out_prefix in written:
                                out_file = written[out_prefix]
                                with open(out_file, 'a', encoding="UTF-8") as f:
                                    f.write("\n".join(titles) + "\n")
                            else:
                                out_file = out_prefix + '.txt'
                                with open(out_file, 'w', encoding="UTF-8") as f:
                                    f.write("\n".join(titles) + "\n")
                                written[out_prefix] = out_file
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_persons_in_genre(genre='ARTICLE',lang_id='eng', preprocess=False):
    if not os.path.exists(PERS_LANG_GENRE):
        os.makedirs(PERS_LANG_GENRE)
    out_base = PERS_LANG_GENRE
    print("start extraction!")
    start_time = time.time()
    written = {}
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            titles_lang_pers_genre = titles_from_ctx_in_language_by_person_from_genre(mpi_ctx,
                                                                                      genre=genre,
                                                                                      lang_id=lang_id,
                                                                                      preprocess=preprocess)
            for pers in titles_lang_pers_genre:
                titles = titles_lang_pers_genre[pers]
                if titles:
                    out_prefix = out_base + pers + '_' + lang_id + '_' + genre
                    if not preprocess:
                        out_prefix += '_raw'
                    if out_prefix in written:
                        out_file = written[out_prefix]
                        with open(out_file, 'a', encoding="UTF-8") as f:
                            f.write("\n".join(titles) + "\n")
                    else:
                        out_file = out_prefix + '.txt'
                        with open(out_file, 'w', encoding="UTF-8") as f:
                            f.write("\n".join(titles) + "\n")
                        written[out_prefix] = out_file
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_persons_in_genre_by_year(genre='ARTICLE',lang_id='eng', preprocess=False):
    if not os.path.exists(PERS_LANG_YEARS_GENRE):
        os.makedirs(PERS_LANG_YEARS_GENRE)
    out_base = PERS_LANG_YEARS_GENRE
    print("start extraction!")
    start_time = time.time()
    written = {}
    for mpi in mpis:
        print("")
        print("processing", mpi, "...")
        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting", mpi_ctx, "...")
            titles_lang_pers_years = titles_from_ctx_in_language_by_person_from_genre_by_year(mpi_ctx,
                                                                                              genre=genre,
                                                                                              lang_id=lang_id,
                                                                                              preprocess=preprocess)
            for pers in titles_lang_pers_years:
                out_pers_base = out_base + pers + "_" + lang_id + "_" + genre + "_"
                for year in YEARS:
                    year = str(year)
                    if year in titles_lang_pers_years[pers]:
                        titles = titles_lang_pers_years[pers][year]
                        if titles:
                            out_prefix = out_pers_base + year
                            if not preprocess:
                                out_prefix += '_raw'
                            if out_prefix in written:
                                out_file = written[out_prefix]
                                with open(out_file, 'a', encoding="UTF-8") as f:
                                    f.write("\n".join(titles) + "\n")
                            else:
                                out_file = out_prefix + '.txt'
                                with open(out_file, 'w', encoding="UTF-8") as f:
                                    f.write("\n".join(titles) + "\n")
                                written[out_prefix] = out_file
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_cats(lang_id="eng", preprocess=False):
    if not os.path.exists(CAT_LANG):
        os.makedirs(CAT_LANG)
    print("start extraction!")
    start_time = time.time()
    for cat in cats:
        print("")
        print("processing", cat, "...")
        init = True
        ous = cat_ous[cat]
        for ou in ous:
            if ou in mpis:
                mpi_ctxs = ous_ctx[ou]
                for mpi_ctx in mpi_ctxs:
                    print("extracting", mpi_ctx, "...")
                    titles = titles_from_ctx_in_language(mpi_ctx, lang_id=lang_id, preprocess=preprocess)
                    out_prefix = CAT_LANG + cat + '_' + lang_id
                    if not preprocess:
                        out_prefix += '_raw'
                    out_file = out_prefix + '.txt'
                    if init:
                        with open(out_file, 'w', encoding="UTF-8") as f:
                            f.write("\n".join(titles) + "\n")
                        init = False
                    else:
                        with open(out_file, 'a', encoding="UTF-8") as f:
                            f.write("\n".join(titles) + "\n")
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_cats_by_year(lang_id="eng", preprocess=False):
    if not os.path.exists(CAT_LANG_YEARS):
        os.makedirs(CAT_LANG_YEARS)
    print("start extraction!")
    start_time = time.time()
    init = {}
    for cat in cats:
        print("")
        print("processing", cat, "...")
        for year in YEARS:
            init[str(year)] = True
        out_base = CAT_LANG_YEARS + cat + '_' + lang_id + '_'
        ous = cat_ous[cat]
        for ou in ous:
            if ou in mpis:
                mpi_ctxs = ous_ctx[ou]
                for mpi_ctx in mpi_ctxs:
                    print("extracting", mpi_ctx, "...")
                    titles_lang_years = titles_from_ctx_in_language_by_year(mpi_ctx,
                                                                            lang_id=lang_id,
                                                                            preprocess=preprocess)
                    for year in YEARS:
                        year = str(year)
                        if year in titles_lang_years:
                            titles = titles_lang_years[year]
                            if titles:
                                out_prefix = out_base + year
                                if not preprocess:
                                    out_prefix += '_raw'
                                out_file = out_prefix + '.txt'
                                if init[year]:
                                    with open(out_file, 'w', encoding="UTF-8") as f:
                                        f.write("\n".join(titles) + "\n")
                                    init[year] = False
                                else:
                                    with open(out_file, 'a', encoding="UTF-8") as f:
                                        f.write("\n".join(titles) + "\n")
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))


def titles_from_cats_in_genre_by_year(genre='ARTICLE', lang_id='eng', preprocess=False):
    if not os.path.exists(CAT_LANG_YEARS_GENRE):
        os.makedirs(CAT_LANG_YEARS_GENRE)
    print("start extraction!")
    start_time = time.time()
    init = {}
    for cat in cats:
        print("")
        print("processing", cat, "...")
        for year in YEARS:
            init[str(year)] = True
        ous = cat_ous[cat]
        out_base = CAT_LANG_YEARS_GENRE + cat + '_' + lang_id + '_' + genre + '_'
        for ou in ous:
            if ou in mpis:
                mpi_ctxs = ous_ctx[ou]
                for mpi_ctx in mpi_ctxs:
                    print("extracting", mpi_ctx, "...")
                    titles_lang_years =\
                        titles_from_ctx_in_language_and_genre_by_year(mpi_ctx,
                                                                      genre=genre,
                                                                      lang_id=lang_id,
                                                                      preprocess=preprocess)
                    for year in YEARS:
                        year = str(year)
                        if year in titles_lang_years:
                            titles = titles_lang_years[year]
                            if titles:
                                out_prefix = out_base + year
                                if not preprocess:
                                    out_prefix += '_raw'
                                out_file = out_prefix + '.txt'
                                if init[year]:
                                    with open(out_file, 'w', encoding="UTF-8") as f:
                                        f.write("\n".join(titles) + "\n")
                                    init[year] = False
                                else:
                                    with open(out_file, 'a', encoding="UTF-8") as f:
                                        f.write("\n".join(titles) + "\n")
    print("finished extraction after %s sec!" % round(time.time() - start_time, 2))
