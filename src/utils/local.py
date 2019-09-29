import os

from pybman import LocalData

from .paths import ITEMS_DIR

data_paths = []

for root, dirs, files in os.walk(ITEMS_DIR):
    for name in files:
        if name.endswith(".json"):
            data_paths.append(os.path.realpath(os.path.join(root, name)))

ld = LocalData(base_dir=ITEMS_DIR)
