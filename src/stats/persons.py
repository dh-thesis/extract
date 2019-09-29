import os
import csv
import time
import logging

from pybman import utils
from pybman import DataSet

from ..utils.local import ld
from ..utils.paths import MPIS_DIR, STATS_OUT

logging.basicConfig(filename='log/stats_pers.log', level=logging.INFO)

PERS_STATS = os.path.join(STATS_OUT, 'persons/')

if not os.path.exists(PERS_STATS):
    os.makedirs(PERS_STATS)

ous_ctx = utils.read_json(MPIS_DIR + 'mapped/ous_ctx.json')
mpis = list(ous_ctx.keys())
mpis.sort()

mpis = utils.read_json(MPIS_DIR + 'mapped/ous_mpi.json')

print("start processing!")

logging.info("start processing!")
start_time = time.time()

for mpi in mpis:
    if not mpi in ous_ctx:
        logging.info(mpis[mpi]+ " has no contexts!")
        logging.info("")
        continue

    logging.info("processing "+mpis[mpi]+"...")
    stats = {}
    mpi_ctxs = ous_ctx[mpi]
    for mpi_ctx in mpi_ctxs:
        logging.info("extracting " +  mpi_ctx + " ...")

        all = ld.get_data(mpi_ctx)[0]

        # consider only released items
        data_set = DataSet(data_id=all.idx+"_released", raw=all.get_items_released())

        if not data_set.records:
            logging.info(mpi_ctx+ " has no records!")
            continue

        authors = data_set.get_creators_data() # only CoNE related authors!

        a = list(authors.keys())
        a.sort()

        logging.info(str(len(a)) + " CoNE persons to process ...")

        records = 0

        for i in a:
            if i in stats:
                stats[i] += len(authors[i])
            else:
                stats[i] = len(authors[i])
            records += len(authors[i])

        logging.info("... with " + str(records) + " attributed records!")

    if not stats:
        continue

    stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)

    idx, num_pub = zip(*stats)

    total = len(idx)


    path = PERS_STATS + mpi + '_pers_pub.csv'

    logging.info("write stats to file: "+path)

    with open(path,'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='\t', quotechar='', quoting=csv.QUOTE_NONE) # , quoting=csv.QUOTE_MINIMAL
        csv_writer.writerow(['authors','publications'])
        for i in range(0, total):
            csv_writer.writerow([idx[i],num_pub[i]])

    logging.info("finished "+mpis[mpi]+"!")
    logging.info("")
    
print("finished processing after %s sec!" % round(time.time() - start_time, 2))
logging.info("finished processing after %s sec!" % round(time.time() - start_time, 2))
