import os
import sys
import csv
import time

from pybman import utils
from pybman import DataSet

from ..utils.paths import DATA_DIR, LOG_DIR, MPIS_DIR, STATS_OUT


def routine():

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    print("console output is redirected to count_journals.log ...")

    stdout = sys.stdout
    log = open(LOG_DIR + "count_journals.log", "w+")
    sys.stdout = log

    from ..utils.local import ld

    JOUR_STATS = STATS_OUT + 'journals/'

    if not os.path.exists(JOUR_STATS):
        os.makedirs(JOUR_STATS)

    ous_ctx = utils.read_json(DATA_DIR + 'base/ctx_sel.json')
    mpis = list(ous_ctx.keys())
    mpis.sort()

    mpis = utils.read_json(MPIS_DIR + 'mapped/ous_mpi.json')

    print("start processing!")
    start_time = time.time()

    for mpi in mpis:
        if mpi not in ous_ctx:
            print(mpis[mpi] + " has no contexts!")
            print("")
            continue

        print("processing "+mpis[mpi]+"...")

        articles = []
        journals = {}
        counter = 0
        nojour = 0

        mpi_ctxs = ous_ctx[mpi]
        for mpi_ctx in mpi_ctxs:
            print("extracting " + mpi_ctx + " ...")

            all = ld.get_data(mpi_ctx)[0]

            # consider only released items
            data_set = DataSet(data_id=all.idx+"_released", raw=all.get_items_released())

            if not data_set.records:
                print(mpi_ctx + " has no records!")
                continue

            print(str(data_set.num) + " records to process...")

            for record in data_set.records:
                data = record['data']
                if data['publicState'] == 'RELEASED':
                    if data['metadata']['genre'] == 'ARTICLE':
                        articles.append(record)

            for article in articles:
                jour = False
                if 'sources' in article['data']['metadata']:
                    for source in article['data']['metadata']['sources']:
                        if source['genre'] == 'JOURNAL':
                            if 'title' in source:
                                jour = True
                                counter += 1
                                if source['title'] in journals:
                                    journals[source['title']] += 1
                                else:
                                    journals[source['title']] = 1
                            else:
                                print(article['data']['objectId'] + " has journal as source without title!")
                                continue
                        if jour:
                            break
                    if not jour:
                        nojour += 1
                else:
                    print("found article " + article['data']['objectId'] + " without any source!")

        print('found ' + str(counter) + ' articles with journals as source')
        print('found ' + str(nojour) + ' articles without a journal as souce')

        journals = sorted(journals.items(), key=lambda x: x[1], reverse=True)

        total = len(journals)

        path = JOUR_STATS + mpi + '_jour_art.csv'

        print("write stats to file: "+path)

        with open(path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)  # quoting=csv.QUOTE_NONE
            csv_writer.writerow(['journals', 'articles'])
            for i in range(0, total):
                jour, art = journals[i]
                jour = jour.replace('\t',' ')
                jour = jour.replace(',','')
                jour = utils.clean_string(jour)
                csv_writer.writerow([jour, art])

        print("finished " + mpis[mpi] + "!")
        print("")

    print("finished processing after %s sec!" % round(time.time() - start_time, 2))

    log.close()
    sys.stdout = stdout


if __name__ == '__main__':
    routine()
