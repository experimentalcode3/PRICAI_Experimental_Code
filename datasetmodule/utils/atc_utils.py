from datasetmodule.utils.GeneralHierarchy import GeneralHierarchy
import pandas as pd
import json


def get_used_atc_codes(data_path):
    # Read used atc codes from file
    codes = set()
    with open(f'{data_path}/used_atc_codes.csv', 'r') as f:
        for code in f:
            codes.add(code.strip())

    # We should also include the manual mapping of RxNorm - atc codes
    with open(f'{data_path}/rxnorm_atc_map.json', 'r') as f:
        # allcodes are all the level 5 atc codes
        allcodes = json.loads(f.read())
        for code in allcodes:
            codes.add(code['atc_code'].strip())

    return codes


def prepare_atc_codes_file(data_path):
    file_name = 'hrchy_full_atc.json'

    # Read the atc codes used in MIMIC-IV
    used_codes = get_used_atc_codes(data_path)

    # Read atc_codes json file
    pairs = []
    with open(f'{data_path}/{file_name}', 'r') as f:
        # allcodes are all the level 5 atc codes
        allcodes = json.loads(f.read())
        for atc_code in allcodes:
            leaf = atc_code['id'].strip()
            if leaf not in used_codes:
                continue
            l4 = leaf[0:5]
            l3 = leaf[0:4]
            l2 = leaf[0:3]
            l1 = leaf[0]
            l0 = 'ROOT'
            pairs.append([leaf, l4])
            pairs.append([l4, l3])
            pairs.append([l3, l2])
            pairs.append([l2, l1])
            pairs.append([l1, l0])

    subset_hrchy = pd.DataFrame(data=pairs, columns=['CHILD', 'PARENT'])
    subset_hrchy.drop_duplicates(inplace=True)
    subset_hrchy.to_csv(f'{data_path}/hrchy_subset_atc.csv', sep=';', index=False)


def get_atc_hrchy(code_path, index_leaf=False):
    hrchy = GeneralHierarchy(code_path, index_leaf)
    return hrchy


def get_rxnorm_atc_map(file_path):
    rxnorm_to_atc = []
    with open(file_path, 'r') as f:
        # allcodes are all the level 5 atc codes
        atc_manual_map = json.loads(f.read())
        for row in atc_manual_map:
            rxnorm_to_atc.append([row['concept_code'], row['atc_code']])
    return rxnorm_to_atc
