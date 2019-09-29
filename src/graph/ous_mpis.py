import os
import sys

from pybman import utils

from ..utils.paths import LOG_DIR, MPIS_DIR, PURE_DIR, GRAPH_DIR

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

print("console output is redirected to graph_ous_mpis.log ...")

stdout = sys.stdout

log = open(LOG_DIR + "graph_ous_mpis.log", "w+")
sys.stdout = log

mpis = utils.read_json(MPIS_DIR + 'mapped/ous_mpi.json')
ous = utils.read_json(PURE_DIR + "ous/all.json")

ous_nodes = [["Id","Label"]]
ous_edges = [["Source","Target"]]

children = []

ous_collected = []

for rec in ous['records']:
    if rec['data']['objectId'] in mpis:
        objectId = rec['data']['objectId']
        name = utils.clean_string(rec['data']['name'])
        ous_nodes.append([objectId,name])
        ous_collected.append(objectId)
        if 'parentAffiliation' in rec['data']:
            parent = rec['data']['parentAffiliation']['objectId']
            ous_edges.append([objectId,parent])
        else:
            print("no parent:",objectId)
    if rec['data']['objectId'] not in mpis and 'parentAffiliation' in rec['data']:
        if rec['data']['parentAffiliation']['objectId'] in mpis \
        or rec['data']['parentAffiliation']['objectId'] in children:
            objectId = rec['data']['objectId']
            name = utils.clean_string(rec['data']['name'])
            ous_nodes.append([objectId,name])
            ous_collected.append(objectId)
            parent = rec['data']['parentAffiliation']['objectId']
            ous_edges.append([objectId,parent])
            if rec['data']['hasChildren'] == True:
                children.append(objectId)

found = True
while found:
    changed = False
    for rec in ous['records']:
        if rec['data']['objectId'] not in ous_collected and 'parentAffiliation' in rec['data']:
            if rec['data']['parentAffiliation']['objectId'] in mpis \
            or rec['data']['parentAffiliation']['objectId'] in children:
                objectId = rec['data']['objectId']
                name = utils.clean_string(rec['data']['name'])
                ous_nodes.append([objectId,name])
                ous_collected.append(objectId)
                changed = True
                parent = rec['data']['parentAffiliation']['objectId']
                ous_edges.append([objectId,parent])
                if rec['data']['hasChildren'] == True:
                    children.append(objectId)
    if not changed:
        found = False

utils.write_csv(GRAPH_DIR + "mpis--ous_nodes--tree-full.csv",ous_nodes)
utils.write_csv(GRAPH_DIR + "mpis--ous_ous_edges--tree.csv",ous_edges)

## Institutes

institutes = [['Id','Label']]

for rec in ous['records']:
    if rec['data']['objectId'] in mpis:
        objectId = rec['data']['objectId']
        name = utils.clean_string(rec['data']['name'])
        institutes.append([objectId,name])

utils.write_csv(GRAPH_DIR + 'mpis--ous_nodes.csv', institutes)

## Children of Institutes

kids_names = [["Id","Label"]]

mpis_kids_nodes = utils.read_csv_with_header(GRAPH_DIR + 'mpis--ous_nodes--tree-full.csv')
mpis_kids_nodes = list(mpis_kids_nodes.values())

for i in range(1,len(mpis_kids_nodes[0])):
    kid_id = mpis_kids_nodes[0][i]
    kid_name = utils.clean_string(mpis_kids_nodes[1][i])
    if kid_id not in mpis:
        kids_names.append([kid_id, kid_name])

utils.write_csv(GRAPH_DIR + 'mpis--ous_nodes--tree-children.csv', kids_names)

# mpis_kids = utils.read_plain_clean(GRAPH_DIR + 'mpis--ous_ous_edges--tree.csv')
# mpis_kids = [mpi_kids.replace('"','').split(',') for mpi_kids in mpis_kids]
# utils.write_csv(GRAPH_DIR + 'mpis--ous_ous_edges--tree--clean.csv', mpis_kids)

log.close()
sys.stdout = stdout
