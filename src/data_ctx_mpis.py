import sys

from pybman import utils

from .utils_path import BASE_DIR

print("console output is redirected to data_ctx_mpis.log ...")

stdout = sys.stdout

log = open("log/data_ctx_mpis.log", "w+")
sys.stdout = log

MPIS_DIR = BASE_DIR + 'mpis/'
PURE_DIR = BASE_DIR + 'pure/'

OUT_DIR = '../data/'
GRAPH_DIR = OUT_DIR + 'graph/'

ous = utils.read_json(PURE_DIR + "ous/all.json")
mpis = utils.read_json(MPIS_DIR + 'mapped/ous_ctx.json')

institutes = [['Id','Label']]

for rec in ous['records']:
    if rec['data']['objectId'] in mpis:
        objectId = rec['data']['objectId']
        name = utils.clean_string(rec['data']['name'])
        institutes.append([objectId,name])

utils.write_csv(GRAPH_DIR + 'mpis--ous_nodes--ctx.csv', institutes)

institutes_contexts = [['Source','Target']]
for mpi in mpis:
    for context in mpis[mpi]:
        institutes_contexts.append([mpi, context])

utils.write_csv(GRAPH_DIR + 'mpis--ous_ctx_edges.csv', institutes_contexts)

log.close()
sys.stdout = stdout
