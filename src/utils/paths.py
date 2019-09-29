import os

FILE_DIR, _ = os.path.split(os.path.abspath(__file__))

MAIN_DIR = os.path.join(FILE_DIR, '../../../')

BASE_DIR = os.path.join(MAIN_DIR, 'base/data/')
MPIS_DIR = os.path.join(BASE_DIR, 'mpis/')
PURE_DIR = os.path.join(BASE_DIR, 'pure/')
ITEMS_DIR = os.path.join(BASE_DIR, 'items/')

DATA_DIR = os.path.join(MAIN_DIR, 'data/')
STATS_OUT = os.path.join(DATA_DIR, 'count/')
TITLES_OUT = os.path.join(DATA_DIR, 'titles/')
