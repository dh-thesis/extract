import sys

from pybman import utils

stdout = sys.stdout

print("console output is redirected to data_lang.log ...")

log = open("log/data_lang.log", "w+")
sys.stdout = log

ITEMS_DIR = '../pubdata/data/items/'
NODES_DIR = '../data/nodes/'

## Languages
languages_raw = utils.read_json('../pubdata/data/pure/lang/collection.json')

languages = [['Id','Name','Coordinates']]

dc_title = 'http_purl_org_dc_elements_1_1_title'
dc_idx = 'http_purl_org_dc_elements_1_1_identifier'
google_coordinates = 'http_earth_google_com_kml_2_1_coordinates'

for lang in languages_raw:
    name = ''
    if dc_title in languages_raw[lang]:
        name = languages_raw[lang][dc_title]
        if type(name) == list:
            name = name[0]
    else:
        print("no name found for language", lang)
    coordinates = ''
    if google_coordinates in languages_raw[lang]:
        coordinates = languages_raw[lang][google_coordinates]
    languages.append([lang, name, coordinates])

utils.write_csv(NODES_DIR + 'pure--lang_nodes.csv', languages)

log.close()
sys.stdout = stdout
