import torch as th
import numpy as np
import random
import dgl


def set_random_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    th.manual_seed(seed)
    th.cuda.manual_seed(seed)
    dgl.seed(seed)
