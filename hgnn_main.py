import argparse
from hgnnmodule.config import Config
from hgnnmodule.start import hgnnmodule

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', '-g', default='0', type=int, help='-1 means cpu')
    parser.add_argument('--use_hpo', action='store_true', help='hyper-parameter optimization')
    args = parser.parse_args()

    config_file = ["./hgnnmodule/config.ini"]
    config = Config(file_path=config_file, gpu=args.gpu)
    config.use_hpo = args.use_hpo
    hgnnmodule(args=config)
