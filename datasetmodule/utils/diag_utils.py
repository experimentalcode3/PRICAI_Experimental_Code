from datasetmodule.utils.GeneralHierarchy import GeneralHierarchy
import pandas as pd
import torch as th
import json


def roll_to_level(node, level):
    while node.depth > level:
        node = node.parent
    return node


def rollup_code(code, hierarchy, target_level):
    node = hierarchy.get_code(code)
    while node.depth > target_level:
        node = node.parent
    return node.code


def apply_rollup(code, icd9_hierarchy,  level):
    node = icd9_hierarchy.get_code(code)
    node = roll_to_level(node, level)
    return node.code


def remove_dash(code):
    index = code.find('-')
    return code[index + 1:]


def remove_dot(code):
    return code.replace('.', '')


def add_dot(mimic_code):
    if mimic_code is None:
        return None
    if '-' in mimic_code:
        return mimic_code

    icd9_code = ""
    if len(mimic_code) == 3:
        icd9_code = mimic_code
    elif len(mimic_code) > 3:
        mimic_code = list(mimic_code)
        mimic_code.insert(3, ".")
        icd9_code = ''.join(mimic_code)

    return icd9_code


def get_diag_hrchy(file_path):
    hrchy = GeneralHierarchy(file_path)
    return hrchy


def get_used_diagnosis_codes(data_path):
    # Read used icd9 codes from file
    codes = []
    with open(f'{data_path}/used_diag_codes.csv', 'r') as f:
        for code in f:
            codes.append(code.strip())

    return codes


def prepare_diagnosis_hierarchy_subset(data_path):
    # Load the used diagnosis codes
    used_codes = get_used_diagnosis_codes(data_path)

    # Read the full ICD9 diagnosis code hierarch
    with open(f'{data_path}/hrchy_full_diag.json', 'r') as f:
        allcodes = json.loads(f.read())
        
        ancestry = []
        found_codes = []
        for hierarchy in allcodes:
            # If no codes from this hierarchy is present in the list of codes
            # used within the MIMIC-IV dataset, we skip the hierarchy path
            if not {remove_dot(node['code']) for node in hierarchy}.intersection(set(used_codes)):
                continue

            # Here we know the code is important for us, so we store its ancestry
            for i, (child, parent) in enumerate(zip(hierarchy[1:], hierarchy[0:-1])):
                # Add 'ROOT' if first relation
                if i == 0:
                    ancestry.append([remove_dot(parent['code']), 'ROOT', parent['descr']])

                ancestry.append([remove_dot(child['code']), remove_dot(parent['code']), child['descr']])

            found_codes.append(remove_dot(child['code']))

        # Convert the ancestry to a pandas dataframe
        subset_hierarchy = pd.DataFrame(ancestry, columns=['CHILD', 'PARENT', 'DESCR'])

        # Drop duplicates and save hierarchy
        subset_hierarchy.drop_duplicates(inplace=True)
        subset_hierarchy.to_csv(f'{data_path}/hrchy_subset_diag.csv', sep=';', index=False)


def get_rollup_map(init_map: dict, out_depth: int, diag_hrchy: GeneralHierarchy) -> dict:
    """
    Parameters
    ----------
    init_map: The initial map current label indexes to corresponding ICD9 codes
    out_depth: The depth we with to roll to
    diag_hrchy: ICD9 hierarchy

    Returns:
    -------
    out_map: tensor mappings from initial column indexes to output column indexes
    """
    # New mapping between ICD9 codes and their label indexes
    new_map = {}

    for key, value in init_map.items():
        node = diag_hrchy.get_code(value)

        # Find the corresponding node of specific depth
        while node.depth > out_depth:
            node = node.parent

        # Add the node to the new map
        if node.code in new_map:
            new_map[node.code].add(key)
        else:
            new_map[node.code] = {key}

    # Create map between indexes of initial tensor, and rolled up tensor
    out_map = {index: list(columns) for index, columns in enumerate(new_map.values())}

    return out_map


def rollup_tensor(input_tensor: th.Tensor, aggregation: dict, agg_func: callable) -> th.tensor:

    agg_tensor = th.zeros(size=(input_tensor.shape[0], len(aggregation)), dtype=th.float32)
    for i, agg_indexes in enumerate(aggregation.values()):
        agg_tensor[:, i] = agg_func(input_tensor[:, agg_indexes], dim=1)[0]

    return agg_tensor
