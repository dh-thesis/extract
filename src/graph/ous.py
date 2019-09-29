import os
import sys

from pybman import utils

from ..utils.paths import LOG_DIR, PURE_DIR, GRAPH_DIR

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

print("console output is redirected to graph_ous.log ...")

stdout = sys.stdout

log = open(LOG_DIR + "graph_ous.log", "w+")
sys.stdout = log

ous = utils.read_json(PURE_DIR + 'ous/all.json')

org_nodes = [['Id','Label']]
org_edges = [['Source','Target']]

for record in ous['records']:
    org_unit_id = record['data']['objectId']
    org_unit_name = utils.clean_string(record['data']['name'])
    org_nodes.append([org_unit_id, org_unit_name])
    if 'parentAffiliation' in record['data']:
        parent = record['data']['parentAffiliation']['objectId']
        org_edges.append([org_unit_id, parent])

utils.write_csv(GRAPH_DIR + 'pure--ous_nodes.csv', org_nodes)
utils.write_csv(GRAPH_DIR + 'pure--ous_ous_edges.csv', org_edges)

log.close()
sys.stdout = stdout
