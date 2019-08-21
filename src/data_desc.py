import sys

from pybman import utils

from .utils_path import BASE_DIR

stdout = sys.stdout

print("console output is redirected to data_desc.log ...")

log = open("log/data_desc.log", "w+")
sys.stdout = log

MPIS_DIR = BASE_DIR + 'mpis/'

OUT_DIR = '../data/'
GRAPH_DIR = OUT_DIR + 'graph/'

## Tags of Institutes

ous_tags = utils.read_json(MPIS_DIR + 'mapped/ous_tags.json')
tags = utils.read_plain_clean(MPIS_DIR + 'mapped/ous_tags_all.txt')

tag_nodes = [["Id","Label"]]
tags.sort()

for i, t in enumerate(tags):
    tag_id = 'tag_' + str(i+1)
    tag_nodes.append([tag_id, t])

utils.write_csv(GRAPH_DIR + "mpis--tags_nodes.csv", tag_nodes)

mpis_tags = [['Source','Target']]

print("try to find tags for",len(ous_tags),"institutes")

for mpi in ous_tags:
    mpi_tags = ous_tags[mpi]
    for tag in mpi_tags:
        tag_id = tags.index(tag) + 1
        tag_id = 'tag_' + str(tag_id)
        mpis_tags.append([mpi, tag_id])

print("found",len(mpis_tags)-1,"edges from",
      len(ous_tags), "institutes to",
      len(tag_nodes)-1,"tags")

utils.write_csv(GRAPH_DIR + 'mpis--ous_tags_edges.csv', mpis_tags)

## Categories of Institutes

mpis = utils.read_json(MPIS_DIR + 'mapped/ous_mpi.json')
cats = utils.read_json(MPIS_DIR + 'mapped/cat_ous.json')

cat_nodes = [["Id","Label"]]
cat_edges = [["Source","Target"]]

mpis_nodes = [["Id","Label"]]

all_mpis = []
all_cats = list(cats.keys())
all_cats.sort()

print("try to find categories for",len(mpis),"institutes")

for i, category in enumerate(all_cats):
    cat_idx = "category_"+str(i+1)
    cat_nodes.append([cat_idx, category])
    ous_idx = cats[category]
    for ou_idx in ous_idx:
        if ou_idx not in all_mpis:
            all_mpis.append(ou_idx)
            mpis_nodes.append([ou_idx, mpis[ou_idx]])
        cat_edges.append([ou_idx, cat_idx])

print("found",len(cat_edges)-1,"edges from",
      len(all_mpis), "institutes to",
      len(all_cats),"categories")

utils.write_csv(GRAPH_DIR + "mpis--ous_nodes--cats.csv", mpis_nodes)
utils.write_csv(GRAPH_DIR + "mpis--cats_nodes.csv", cat_nodes)
utils.write_csv(GRAPH_DIR + "mpis--ous_cat_edges.csv", cat_edges)

## Tags of Institutes of Categories

cats = utils.read_json(MPIS_DIR + 'mapped/cat_ous.json')
tags = utils.read_json(MPIS_DIR + 'mapped/ous_tags.json')

t = list(tags.keys())
t.sort()

c = list(cats.keys())
c.sort()

all_c = []
all_t = []

cat_tags = {}
tags_cat = {}

for cat in c:
    cat_tags[cat] = []
    for ou_idx in cats[cat]:
        if not ou_idx in all_c:
            all_c.append(ou_idx)
        ou_tags = tags[ou_idx]
        for ou_tag in ou_tags:
            if ou_tag not in all_t:
                all_t.append(ou_tag)
            if ou_tag not in tags_cat:
                tags_cat[ou_tag] = [cat]
            else:
                if cat not in tags_cat[ou_tag]:
                    tags_cat[ou_tag].append(cat)
            if ou_tag not in cat_tags[cat]:
                cat_tags[cat].append(ou_tag)

all_c.sort()

# cat_nodes = [["Id","Label"]]
ctags = {}

for i, cat in enumerate(c):
    cat_idx = "category_"+str(i+1)
    # cat_nodes.append([cat_idx, cat])
    ctags[cat_idx] = cat_tags[cat]

# tags_nodes = [["Id", "Label"]]

ct_edge = {}

for cat in ctags:
    ct_edge[cat] = []

all_t.sort()

for i, tag in enumerate(all_t):
    tag_idx = "tag_"+str(i+1)
    # tags_nodes.append([tag_idx, tag])
    for cat in ctags:
        if tag in ctags[cat]:
            ct_edge[cat].append(tag_idx)
        else:
            continue

cat_edges = [["Source","Target"]]

for cat in ct_edge:
    tags = ct_edge[cat]
    for cat_tag in tags:
        cat_edges.append([cat, cat_tag])

print("found categories for",len(all_c),"institutes")

# utils.write_csv(GRAPH_DIR + "mpis--cats_nodes--cats-tags.csv", cat_nodes)
# utils.write_csv(GRAPH_DIR + "mpis--tags_nodes--cats-tags.csv", tags_nodes)
utils.write_csv(GRAPH_DIR + "mpis--cats-tags_edges.csv", cat_edges)

log.close()
sys.stdout = stdout
