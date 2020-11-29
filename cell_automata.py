"""Module to create cellular details in JSON"""

# import pandas as pd
# import numpy as np

import logging
logging.basicConfig(level=logging.DEBUG)

from automaton import Automaton


def get_rule_30(steps=None):
    """for get rule 30

    Args:
        steps (int): number of steps to run the rule 30

    Returns:
        cell_json(list): python object notation of """

    # cells = [[0,0,0,0,1,0,0,0,0],
    #     [0,0,0,1,1,1,0,0,0],
    #     [0,0,1,1,0,0,1,0,0],
    #     [0,1,1,0,1,1,1,1,0],
    #     [1,1,0,0,1,0,0,0,1]]

    cells = Automaton(steps, rule=30).string()

    cell_json = [{"z":cells, "y":list(range(1, steps))}]
    # cell_json = [{"z":cells}]

    logging.info("\n" + str(Automaton(20, rule=30).string()))

    return cell_json
