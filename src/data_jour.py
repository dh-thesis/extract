import sys

from pybman import utils

from .utils_path import BASE_DIR

stdout = sys.stdout

print("console output is redirected to data_jour.log ...")

log = open("log/data_jour.log", "w+")
sys.stdout = log

GRAPH_DIR = '../data/graph/'

## Journals
journals_raw =  utils.read_json(BASE_DIR + 'pure/jour/collection.json')

dc_title            = 'http_purl_org_dc_elements_1_1_title'
dc_publisher        = 'http_purl_org_dc_elements_1_1_publisher'
dc_identifier       = 'http_purl_org_dc_elements_1_1_identifier'
dc_identifier_type  = 'http_www_w3_org_2001_XMLSchema_instance_type'
dc_identifier_value = 'http_www_w3_org_1999_02_22_rdf_syntax_ns_value'
dc_terms_alt        = 'http_purl_org_dc_terms_alternative'  # alternative title
dc_terms_pub        = 'http_purl_org_dc_terms_publisher'    # publishing place

escidoc_issn = 'http://purl.org/escidoc/metadata/terms/0.1/ISSN'
##
##  TO DO !!
##

journals = [['Id','Name','Publisher','Place','ISSN']] 

for j in journals_raw:
    jour_id = j
    name = ''
    if dc_title in journals_raw[j]:
        name = journals_raw[j][dc_title]
        if type(name) == str:
            name = utils.clean_string(name)
        elif type(name) != str and type(name) == list:
            name = utils.clean_string(name[0])
        else:
            print("unhandled data type (name) of journal", j+"!")
    else:
        print("no name found for journal", j+"!")
    publisher = ''
    if dc_publisher in journals_raw[j]:
        publisher = journals_raw[j][dc_publisher]
    place = ''
    if dc_terms_pub in journals_raw[j]:
        place = journals_raw[j][dc_terms_pub]
    issn = ''
    if dc_identifier in journals_raw[j]:
        idx = journals_raw[j][dc_identifier]
        if type(idx) == dict:
            if dc_identifier_type in idx:
                if 'ISSN' in idx[dc_identifier_type]:
                    issn = idx[dc_identifier_value]
                else:
                    print("journal",j,"has an identifier but not an ISSN:")
                    print(idx[dc_identifier_type])
            else:
                print("journal",j,"has an identifier but no type is given!")
                print(idx)
        elif type(idx) == list:
            print("handle list of identifiers!!!!!")
    else:
        print("journal",j,"has no identifier!")
    journals.append([jour_id, name, publisher, place, issn])

utils.write_csv(GRAPH_DIR+'pure--jour_nodes.csv', journals)

log.close()
sys.stdout = stdout
