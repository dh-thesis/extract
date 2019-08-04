import sys

from pybman import utils

from .utils_path import BASE_DIR

print("console output is redirected to data_ous_mpis.log ...")

stdout = sys.stdout

log = open("log/data_ous_mpis.log", "w+")
sys.stdout = log

MPIS_DIR = BASE_DIR + 'mpis/'
PURE_DIR = BASE_DIR + 'pure/'

TEMP_DIR = '../data/tmp/'

OUT_DIR = '../data/'
GRAPH_DIR = OUT_DIR + 'graph/'
TABLES_DIR = OUT_DIR + 'tables/'

mpis = utils.read_json(MPIS_DIR + 'mapped/ous_ctx.json')
ous = utils.read_json(PURE_DIR + "ous/all.json")

ous_nodes = [["Id","Label"]]
ous_edges = [["Source","Target"]]

children = []

ous_collected = []

for rec in ous['records']:
    if rec['data']['objectId'] in mpis:
        objectId = rec['data']['objectId']
        name = rec['data']['name']
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
            name = rec['data']['name']
            ous_nodes.append([objectId,name])
            ous_collected.append(objectId)
            parent = rec['data']['parentAffiliation']['objectId']
            ous_edges.append([objectId,parent])
            if rec['data']['hasChildren'] == True:
                children.append(objectId)

# utils.write_csv(TEMP_DIR + "tree_ous_nodes1.csv",ous_nodes)
# utils.write_csv(TEMP_DIR + "tree_ous_edges1.csv",ous_edges)

for rec in ous['records']:
    if rec['data']['objectId'] not in ous_collected and 'parentAffiliation' in rec['data']:
        if rec['data']['parentAffiliation']['objectId'] in mpis \
        or rec['data']['parentAffiliation']['objectId'] in children:
            objectId = rec['data']['objectId']
            name = rec['data']['name']
            ous_nodes.append([objectId,name])
            ous_collected.append(objectId)
            parent = rec['data']['parentAffiliation']['objectId']
            ous_edges.append([objectId,parent])
            if rec['data']['hasChildren'] == True:
                children.append(objectId)

# utils.write_csv(TEMP_DIR + "tree_ous2_nodes.csv",ous_nodes)
# utils.write_csv(TEMP_DIR + "tree_ous2_edges.csv",ous_edges)

for rec in ous['records']:
    if rec['data']['objectId'] not in ous_collected and 'parentAffiliation' in rec['data']:
        if rec['data']['parentAffiliation']['objectId'] in mpis \
        or rec['data']['parentAffiliation']['objectId'] in children:
            objectId = rec['data']['objectId']
            name = rec['data']['name']
            ous_nodes.append([objectId,name])
            ous_collected.append(objectId)
            parent = rec['data']['parentAffiliation']['objectId']
            ous_edges.append([objectId,parent])
            if rec['data']['hasChildren'] == True:
                children.append(objectId)

# utils.write_csv(TEMP_DIR + "tree_ous3_nodes.csv",ous_nodes)
# utils.write_csv(TEMP_DIR + "tree_ous3_edges.csv",ous_edges)

utils.write_csv(GRAPH_DIR + "mpis--ous_nodes--tree.csv",ous_nodes)
utils.write_csv(GRAPH_DIR + "mpis--ous_ous_edges--tree.csv",ous_edges)

# check for parents not yet collected

#for edge in ous_edges:
#    if edge[1] not in ous_collected:
#        for rec in ous['records']:
#            if rec['data']['objectId'] == edge[1]:
#                objectId = rec['data']['objectId']
#                name = rec['data']['name']
#                ous_nodes.append([objectId,name])
#                ous_collected.append(objectId)
#                if 'parentAffiliation' in rec['data']:
#                    parent = rec['data']['parentAffiliation']['objectId']
#                    ous_edges.append([objectId,parent])
#                    ous_collected.append(parent)
#                break

# utils.write_csv(TEMP_DIR + "tree_full_nodes.csv",ous_nodes)
# utils.write_csv(TEMP_DIR + "tree_full_edges.csv",ous_edges)

## Institutes

institutes = [['Id','Name']]

for rec in ous['records']:
    if rec['data']['objectId'] in mpis:
        objectId = rec['data']['objectId']
        name = rec['data']['name']
        institutes.append([objectId,name])

utils.write_csv(GRAPH_DIR + 'mpis--ous_nodes.csv', institutes)

## Children of Institutes

kids_names = [["Id","Name"]]

mpis_kids_nodes = utils.read_csv_with_header(GRAPH_DIR + 'mpis--ous_nodes--tree.csv')
mpis_kids_nodes = list(mpis_kids_nodes.values())

for i in range(1,len(mpis_kids_nodes[0])):
    kid_id = mpis_kids_nodes[0][i]
    kid_name = utils.clean_string(mpis_kids_nodes[1][i])
    if kid_id not in mpis:
        kids_names.append([kid_id, kid_name])

utils.write_csv(GRAPH_DIR + 'mpis--ous_nodes--tree--clean.csv', kids_names)

mpis_kids = utils.read_plain_clean(GRAPH_DIR + 'mpis--ous_ous_edges--tree.csv')
mpis_kids = [mpi_kids.replace('"','').split(',') for mpi_kids in mpis_kids]
utils.write_csv(GRAPH_DIR + 'mpis--ous_ous_edges--tree--clean.csv', mpis_kids)

log.close()
sys.stdout = stdout
