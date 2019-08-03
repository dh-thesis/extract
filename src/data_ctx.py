import sys

from pybman import utils

print("console output is redirected to data_ctx.log ...")

stdout = sys.stdout

log = open("log/data_ctx.log", "w+")
sys.stdout = log

BASE_DIR = '../pubdata/data/'
PURE_DIR = BASE_DIR + 'pure/'
MPIS_DIR = BASE_DIR + 'mpis/'

OUT_DIR = '../data/'
NODES_DIR = OUT_DIR + 'nodes/'
EDGES_DIR = OUT_DIR + 'edges/'

ctxs = utils.read_json(PURE_DIR + "ctx/all.json")
mpis_ctx = utils.read_json(MPIS_DIR + 'mapped/ous_ctx.json')

ctx_nodes = [["Id","Name"]]
ctx_edges = [["Source","Target"]]

for rec in ctxs['records']:
    objectId = rec['data']['objectId']
    name = rec['data']['name']
    ctx_nodes.append([objectId, name])
    maintainers = rec['data']['responsibleAffiliations']
    for m in maintainers:
        maintainer = m['objectId']
        ctx_edges.append([objectId, maintainer])

utils.write_csv(NODES_DIR + "pure--ctx_nodes.csv", ctx_nodes)
utils.write_csv(EDGES_DIR + "pure--ctx_ous_edges.csv", ctx_edges)

log.close()
sys.stdout = stdout
