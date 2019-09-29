import os

FILE_DIR, _ = os.path.split(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(FILE_DIR, '../../')
MAIN_DIR = os.path.join(PROJECT_DIR, '../')
LOG_DIR = os.path.join(PROJECT_DIR, 'log/')

BASE_DIR = os.path.join(MAIN_DIR, 'base/data/')
MPIS_DIR = os.path.join(BASE_DIR, 'mpis/')
PURE_DIR = os.path.join(BASE_DIR, 'pure/')
ITEMS_DIR = os.path.join(BASE_DIR, 'items/')

DATA_DIR = os.path.join(MAIN_DIR, 'data/')
STATS_OUT = os.path.join(DATA_DIR, 'count/')
TITLES_OUT = os.path.join(DATA_DIR, 'titles/')

GRAPH_DIR = os.path.join(DATA_DIR, 'graph/')
TABLES_DIR = os.path.join(DATA_DIR, 'tables/')
