import sys

from pybman import utils

from .utils_path import BASE_DIR

print("console output is redirected to data_ctx_mpis.log ...")

stdout = sys.stdout

log = open("log/data_ctx_mpis.log", "w+")
sys.stdout = log

MPIS_DIR = BASE_DIR + 'mpis/'

OUT_DIR = '../data/'
GRAPH_DIR = OUT_DIR + 'graph/'

mpis_ctx = utils.read_json(MPIS_DIR + 'mapped/ous_ctx.json')

institutes_contexts = [['Source','Target']]
for mpi in mpis_ctx:
    for context in mpis_ctx[mpi]:
        institutes_contexts.append([mpi, context])

utils.write_csv(GRAPH_DIR + 'mpis--ous_ctx_edges.csv', institutes_contexts)

log.close()
sys.stdout = stdout
