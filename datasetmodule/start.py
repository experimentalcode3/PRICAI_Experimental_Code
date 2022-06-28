from utils.logger import Logger
from utils.utils import set_random_seed
from .extractionflow.MIMICIVFlow import MimicIVExtractor


def datasetmodule(args):
    # Add or set random seed
    if not getattr(args, 'seed', False):
        args.seed = 0

    set_random_seed(args.seed)

    args.logger = Logger(args)

    flow = MimicIVExtractor(args)

    # Extract dataset
    result = flow.run_flow()
    return result
