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
TABLES_DIR = OUT_DIR + 'tables/'

## Tags

tags = utils.read_plain_clean(BASE_DIR + 'mpis/mapped/ous_tags_all.txt')
utils.write_list(GRAPH_DIR + 'mpis--all_tags.txt', tags)

## Tags of Institutes

mpis_tags = utils.read_json(BASE_DIR + 'mpis/mapped/ous_tags.json')

institutes_tags = [['Source','Target']]

for mpi in mpis_tags:
    mpi_tags = mpis_tags[mpi]
    for tag in mpi_tags:
        institutes_tags.append([mpi, tag])

utils.write_csv(GRAPH_DIR + 'mpis--ous_tags_edges.csv', institutes_tags)

## CATEGORIES

# categories_raw = utils.read_json(BASE_DIR + 'mpis/mapped/cat_ous.json')

#categories = list(categories_raw.keys())
#categories.sort()

#utils.write_list(GRAPH_DIR + 'mpis--all_categories.txt', categories)

## Categories of Institutes (TABLE)

# mpis_cat = utils.read_json(BASE_DIR + 'mpis/mapped/ous_cat.json')

# institutes_categories = [['Institute','Categories']]

#for mpi in mpis_cat:
#    for mpi_cat in mpis_cat[mpi]:
#        institutes_categories.append([mpi,mpi_cat])

#utils.write_csv(TABLES_DIR + 'institutes_categories.csv', institutes_categories)

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


print("found",len(cat_edges)-1,"edges between",
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

cat_nodes = [["Id","Label"]]
ctags = {}

for i, cat in enumerate(c):
    cat_idx = "category_"+str(i+1)
    cat_nodes.append([cat_idx, cat])
    ctags[cat_idx] = cat_tags[cat]


tags_nodes = [["Id", "Label"]]

ct_edge = {}

for cat in ctags:
    ct_edge[cat] = []

all_t.sort()

for i, tag in enumerate(all_t):
    tag_idx = "tag_"+str(i+1)
    tags_nodes.append([tag_idx, tag])
    for cat in ctags:
        if tag in ctags[cat]:
            ct_edge[cat].append(tag_idx)
        else:
            continue

cat_edges = [["Source","Target"]]

for cat in ct_edge:
    tags = ct_edge[cat]
    for cat_tag in tags:
        cat_edges.append([cat_tag, cat])

print("found categories for",len(all_c),"institutes")

utils.write_csv(GRAPH_DIR + "mpis--cats_nodes--cats-tags.csv", cat_nodes)
utils.write_csv(GRAPH_DIR + "mpis--tags_nodes--cats-tags.csv", tags_nodes)
utils.write_csv(GRAPH_DIR + "mpis--cats-tags_edges.csv", cat_edges)

log.close()
sys.stdout = stdout
