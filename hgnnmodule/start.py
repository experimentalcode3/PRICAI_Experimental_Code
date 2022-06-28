from utils.logger import Logger
from utils.utils import set_random_seed
from .utils.FeatInitExperiment import FeatInitExperiment
from .utils.hpo import hpo_experiment


def hgnnmodule(args):
    # Add or set random seed
    args.logger = Logger(args)

    # Add best configuration to args
    set_random_seed(args.seed)

    # If we want hyperparameter tuning
    if getattr(args, "use_hpo", False):
        hpo_experiment(args)

    else:
        flow = FeatInitExperiment(args)
        result = flow.train()
        return result
