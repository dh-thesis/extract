import os

from pybman import utils

from ..utils.paths import TITLES_OUT


def routine():
    data_paths = []
    for root, dirs, files in os.walk(TITLES_OUT):
        for name in files:
            if name.endswith(".txt"):
                data_paths.append(os.path.realpath(os.path.join(root, name)))
    for dp in data_paths:
        out_dir = "/".join(dp.split("/")[:-1])
        out_pre = out_file = dp.split("/")[-1].split(".")[0]
        out_file = out_pre + ".csv"
        out_path = out_dir + '/' + out_file
        doc = [["Doc", "Term"]]
        doc_id = 1
        lines = utils.read_plain_clean(dp)
        for line in lines:
            for word in line.split():
                doc.append([out_pre + ":" + str(doc_id), word])
            doc_id += 1
        utils.write_csv(out_path, doc)
