import os
import csv
import time

from pybman import utils
from pybman import DataSet

from ..utils.local import ld
from ..utils.paths import MPIS_DIR, STATS_OUT

REC_STATS = os.path.join(STATS_OUT, 'records/')

if not os.path.exists(REC_STATS):
    os.makedirs(REC_STATS)

ous_ctx = utils.read_json(MPIS_DIR + 'mapped/ous_ctx.json')
mpis = list(ous_ctx.keys())
mpis.sort()

mpis = utils.read_json(MPIS_DIR + 'mapped/ous_mpi.json')

stats = {}

print("start counting!")
start_time = time.time()

for mpi in mpis:
    if not mpi in ous_ctx:
        print(mpi,"has no contexts!")
        print("")
        continue
    print("")
    print("processing", mpi,"...")
    mpi_ctxs = ous_ctx[mpi]
    mpi_total = 0
    for mpi_ctx in mpi_ctxs:
        print("extracting", mpi_ctx,"...")

        all = ld.get_data(mpi_ctx)[0]

        # consider only released items
        data_set = DataSet(data_id=all.idx+"_released", raw=all.get_items_released())

        if not data_set.records:
            print(mpi_ctx,"has no records!")
            print("")
            continue

        print("with", data_set.num, "records...")
        mpi_total += data_set.num

    stats[mpi] = mpi_total


print("finished counting after %s sec!" % round(time.time() - start_time, 2))

total = len(stats)

stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)

path = REC_STATS + 'all.csv'

with open(path,'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
    csv_writer.writerow(['institute','publications'])
    for i in range(0, total):
        ou, pub = stats[i]
        mpi = mpis[ou].replace(" (Hannover)", "").replace(" (Greifswald)","")
        csv_writer.writerow([mpi,pub])
