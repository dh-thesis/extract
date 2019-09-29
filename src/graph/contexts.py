import os
import sys

from pybman import utils

from ..utils.paths import LOG_DIR, PURE_DIR, MPIS_DIR, GRAPH_DIR

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

print("console output is redirected to graph_contexts.log ...")

stdout = sys.stdout

log = open(LOG_DIR + "graph_contexts.log", "w+")
sys.stdout = log

ctxs = utils.read_json(PURE_DIR + "ctx/all.json")
mpis_ctx = utils.read_json(MPIS_DIR + 'mapped/ous_ctx.json')

ctx_nodes = [["Id","Label"]]
ctx_edges = [["Source","Target"]]

for rec in ctxs['records']:
    objectId = rec['data']['objectId']
    name = rec['data']['name']
    ctx_nodes.append([objectId, name])
    maintainers = rec['data']['responsibleAffiliations']
    for m in maintainers:
        maintainer = m['objectId']
        ctx_edges.append([objectId, maintainer])

utils.write_csv(GRAPH_DIR + "pure--ctx_nodes.csv", ctx_nodes)
utils.write_csv(GRAPH_DIR + "pure--ctx_ous_edges.csv", ctx_edges)

log.close()
sys.stdout = stdout
