from decouple import config as get_env
import configparser
import os


class Config:
    def __init__(self, file_path, rel_extract=False, feat_extract=False, ent_extract=False, path=os.getcwd()):
        conf = configparser.ConfigParser()

        try:
            conf.read(file_path)
        except:
            print("Could not read dataset module config.ini file")

        # paths
        self.dataset = 'mimiciv'
        self.rel_extract = rel_extract
        self.feat_extract = feat_extract
        self.ent_extract = ent_extract
        self.path = {'dataset_fold': './output/datasets/',
                     'input_fold': './dataset/' + self.dataset + '/',
                     'config_fold': path + '/datasetmodule/conf/',
                     'output_fold': path + '/datasetmodule/output/',
                     'data_fold': path + '/datasetmodule/data/'}

        # Read Logger Arguments
        self.use_logging = conf.getboolean('NEPTUNE', 'use_logging', fallback=None)
        self.neptune_project_id = conf.get('NEPTUNE', 'neptune_project_id', fallback=None)
        self.neptune_api_token = get_env('neptune_api_token')

        self.project_id = conf.get('GBQ', 'project_id', fallback=None)
        self.gbq_name = conf.get('GBQ', 'dataset_name', fallback=None)
        self.query_prefix = f'{self.project_id}.{self.gbq_name}'
