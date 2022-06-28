from atc_utils import prepare_atc_codes_file
from loinc_utils import prepare_loinc_hierarchy_subset
from diag_utils import prepare_diagnosis_hierarchy_subset
from proc_utils import prepare_procedures_subset
import os


def main():
    data_path = os.path.join(os.getcwd(), '..', 'data')

    prepare_atc_codes_file(data_path)
    prepare_procedures_subset(data_path)
    prepare_diagnosis_hierarchy_subset(data_path)
    prepare_loinc_hierarchy_subset(data_path)


if __name__ == '__main__':
    main()
