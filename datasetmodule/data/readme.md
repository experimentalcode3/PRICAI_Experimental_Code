## Readme
This file contains a description of the files contained within the mimiciv data folder.  
These files are the primary source of auxiliary data for the construction of 
relevant auxiliary hierarchies that can be added to the EHR graph.

## Used Concept Codes
The following files are used to speedup the process of extracting and formatting auxiliary hierarchies 
for subsequent extraction of hierarchical concept features.  
The following queries can be run after successfull setup of the OMOP CDM mapped MIMIC-IV dataset on a Google Big Query.  
The files `used_loinc_codes`, `used_atc_codes`, `used_diag_code`, and `used_proc_codes` have been pre extracted
and added to this folder for easy access.

### used_loinc_codes.csv
This file contains the loinc codes used in the MIMIC-IV dataset.  
The codes are used to heavily limit the construction time of the axial hierarchy for loinc codes by subsampling
the relevant parts of the hierarchy.  
The codes can be extracted from a Google Big Query setup over the schema of the OMOP CDM mapped MIMIC-IV dataset as:
```sql
select distinct C.concept_code
from `mimiciv.cdm_measurement` M
join `mimiciv.voc_concept` C on M.measurement_concept_id = C.concept_id
where C.vocabulary_id = 'LOINC'
```

### used_proc_codes
This file contains the icd9 procedure codes used in the MIMIC-IV dataset.  
The codes are used to limit the construction time of the icd9 procedure hierarchy by subsampling
the relevant parts of the hierarchy with only concepts used within the MIMIC-IV dataset.  
The codes can be extracted from a Google Big Query setup over the schema of the OMOP CDM mapped MIMIC-IV dataset as:
```sql
SELECT DISTINCT C.concept_code
FROM `mimiciv.cdm_procedure_occurrence` CO
join `mimiciv.voc_concept` C on C.concept_id = CO.procedure_concept_id
where C.vocabulary_id = 'ICD9Proc'
```

### used_diag_codes
Contains the subset of ICD9 diagnosis codes we are interested in, extracted from the MIMIC-IV dataset.  
The codes were queried from a Google Big Query setup over the schema of the OMOP CDM mapped MIMIC-IV data as:
```sql
select distinct FILT.level4
from `mimiciv.icd9_filtered` as FILT
join `mimiciv.cdm_condition_occurrence` CO on CO.condition_source_value = FILT.level4
join `mimiciv.voc_concept` C on C.concept_id = CO.condition_source_concept_id
where C.vocabulary_id = 'ICD9CM'
group by FILT.level4
having count(*) > 500;
```
The table `mimiciv.icd9_filtered` is a manually curated table of diagnosis codes used within the MIMIC-IV dataset filtered
for diagnoses codes with a low number of patient samples and filtered for diagnoses codes related to infants and other 
non-discernable codes as summarized in the table below.
        
| Codes Omitted     | Num Codes      | Description     |
| ------------- | ------------- | -------- |
| 290-319          | 375         | Mental Disorders  |
| 630-679           | 530         | Comp. of Pregnancy  |
| 780-799           | 330         | Injuries and Poison  |
| 800-999           | 1617         | Ill-Defined Conditions  |
| E and V           | 1467         | Ext. Causes of Injury  |

The table can be directly imported into google big query using the csv file `icd9_filtered.csv`.

### used_atc_codes
Contain a subset of atc codes used in the conversion from RxNorm to atc.
The subset is extracted from the OMOP CDM vocabularies with the following query:
```sql
select distinct C3.concept_code as atc_code
from `mimiciv.cdm_drug_exposure` DE
join `mimiciv.voc_concept` C1 on C1.concept_id = DE.drug_concept_id
join `mimiciv.voc_concept_ancestor` CA on CA.descendant_concept_id = C1.concept_id
join `mimiciv.voc_concept` C2 on C2.concept_id = CA.ancestor_concept_id
join `mimiciv.voc_concept_relationship` CR on C2.concept_id = CR.concept_id_1
join `mimiciv.voc_concept` C3 on C3.concept_id = CR.concept_id_2
where DE.drug_concept_id > 0
and CA.min_levels_of_separation = 1
and C2.vocabulary_id = 'RxNorm'
and C2.concept_class_id = 'Clinical Drug Form'
and CR.relationship_id = 'RxNorm - ATC'
```

## Full Auxiliary hierarchies
The following files contains the full auxiliary hierarchies.  
The full hierarchies for `loinc`, `icd9`, and `atc` are pre-downloaded for easy access'

### hrchy_full_loinc
This file contains the complete multiAxialHierarchy of LOINC codes downloadable from the [LOINC website](https://loinc.org/file-access/?download-id=470626).  
A free user is required to download the file. The hierarch is processed for removal of all codes not used in the MIMIC-IV data.

### hrchy_full_diag
A json file with the full ICD9 diagnosis code hierarchy. The hierarchy contains all ICD9 diagnosis codes and their ancestry.

### hrchy_full_atc
A json file with the full ATC medication code hierarchy. The hierarchy contains all ATC medication codes and their ancestry.

## Subset Hierarchies
The following explains how to compute the preprocessed subset hierarchies of the `loinc`, `atc`, `proc`, and `diag` hierarchies. 
All subset hierarchies can be created using the script `datasetmodule/utils/subset_hierarchies`.  
The subset hierarchies for `atc`, `loinc`, `diag`, and `proc` are precomputed for easy access.

### hrchy_subset_atc
This file contains the subset hierarchy extracted from the full set of atc codes based on the atc codes used within
the MIMIC-IV dataset. The file can be created using the script `datasetmodule/utils/subset_hierarchies`.  
To create this file an additional file `rxnorm_atc_map.json` is required. Since not all rxnorm codes could be automatically
translated into atc codes, we add manually curated rxnorm codes and their translation into atc codes.

### hrchy_subset_proc
This file contains the hierarchy of child-parent codes forming the ICD-9 procedure code hierarchy. The file can be 
created using the script `datasetmodule/utils/subset_hierarchies`. The only requirement is the `used_proc_codes` 
created in a previous step.

### hrchy_subset_diag
This file contains the hierarchy of child-parent codes forming the ICD-9 diagnosis code hierarchy. The file can be 
created using the script `datasetmodule/utils/subset_hierarchies`. The only requirement is the `used_diag_codes` 
created in a previous step.

### hrchy_subset_loinc
This file contains the hierarchy of child-parent codes forming the loinc code hierarchy. The file can be 
created using the script `datasetmodule/utils/subset_hierarchies`. The only requirement is the `used_loinc_codes` 
created in a previous step.