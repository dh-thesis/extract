import os
import csv
import sys
import time

from pybman import utils
from pybman import DataSet

from ..utils.paths import LOG_DIR, MPIS_DIR, STATS_OUT

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

print("console output is redirected to count_persons.log ...")

stdout = sys.stdout

log = open(LOG_DIR + "count_persons.log", "w+")
sys.stdout = log

from ..utils.local import ld

PERS_STATS = os.path.join(STATS_OUT, 'persons/')

if not os.path.exists(PERS_STATS):
    os.makedirs(PERS_STATS)

ous_ctx = utils.read_json(MPIS_DIR + 'mapped/ous_ctx.json')
mpis = list(ous_ctx.keys())
mpis.sort()

mpis = utils.read_json(MPIS_DIR + 'mapped/ous_mpi.json')

print("start processing!")

start_time = time.time()

for mpi in mpis:
    if not mpi in ous_ctx:
        
        print(mpis[mpi]+ " has no contexts!")
        print("")
        continue

    print("processing "+mpis[mpi]+"...")
    stats = {}
    mpi_ctxs = ous_ctx[mpi]
    for mpi_ctx in mpi_ctxs:
        print("extracting " +  mpi_ctx + " ...")

        all = ld.get_data(mpi_ctx)[0]

        # consider only released items
        data_set = DataSet(data_id=all.idx+"_released", raw=all.get_items_released())

        if not data_set.records:
            print(mpi_ctx+ " has no records!")
            continue

        authors = data_set.get_creators_data() # only CoNE related authors!

        a = list(authors.keys())
        a.sort()

        print(str(len(a)) + " CoNE persons to process ...")

        records = 0

        for i in a:
            if i in stats:
                stats[i] += len(authors[i])
            else:
                stats[i] = len(authors[i])
            records += len(authors[i])

        print("... with " + str(records) + " attributed records!")

    if not stats:
        continue

    stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)

    idx, num_pub = zip(*stats)

    total = len(idx)


    path = PERS_STATS + mpi + '_pers_pub.csv'

    print("write stats to file: "+path)

    with open(path,'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='\t', quotechar='', quoting=csv.QUOTE_NONE) # , quoting=csv.QUOTE_MINIMAL
        csv_writer.writerow(['authors','publications'])
        for i in range(0, total):
            csv_writer.writerow([idx[i],num_pub[i]])

    print("finished "+mpis[mpi]+"!")
    print("")
    
print("finished processing after %s sec!" % round(time.time() - start_time, 2))

log.close()
sys.stdout = stdout
