import os
import sys
import math
import pprint

import torch

from torchdrug import core
from torchdrug.utils import comm

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from grsnn import dataset, layer, model, task, util


def test(cfg, solver):
    solver.model.split = "test"
    solver.evaluate("test")


if __name__ == "__main__":
    args, vars = util.parse_args()
    cfg = util.load_config(args.config, context=vars)

    torch.manual_seed(args.seed + comm.get_rank())

    logger = util.get_root_logger()
    if comm.get_rank() == 0:
        logger.warning("Config file: %s" % args.config)
        logger.warning(pprint.pformat(cfg))

    dataset = core.Configurable.load_config_dict(cfg.dataset)
    solver = util.build_solver(cfg, dataset)

        
    # Add checkpoint loading
    if hasattr(args, "checkpoint"):
        solver.load(args.checkpoint)
        logger.warning(f"Loaded checkpoint from {args.checkpoint}")
    else:
        logger.warning("No checkpoint specified, using initial model")


    test(cfg, solver)
