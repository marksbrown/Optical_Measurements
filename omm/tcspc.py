"""
Functions to process Time Correlated Single Photon Counting Data

Author : Mark S. Brown
Started : Wednesday 30th July 2014
"""

from __future__ import division, print_function
from .main import recursive_data_search
import string
import pandas as pd
from itertools import chain

def parse_time_data(file_parameters, root_dir, dropcols=None, verbose=0, **kwargs):
    """
    Returns clean Pandas DataFrame when given useful file_parameters for associated data
    of form key_word : (
    """

    for key_word, full_loc in recursive_data_search(file_parameters, root_dir, allowed_ext=('csv', 'txt'), **kwargs):
        if verbose > 0:
            print(key_word, full_loc)

        with open(full_loc, 'r') as f:

                for k, a_line in enumerate(f):
                    if a_line.startswith('0.00'):
                        columns_to_pull = len(a_line.split(',')) - 1   # first and last columns are ignored
                        break


        columns = ['time']+list(string.uppercase[:columns_to_pull])
        df = pd.read_csv(full_loc, skiprows=k, sep=",", names=columns)

        df.index = df.time

        for col in chain(('time', columns[-1])):
            try:
                df = df.drop(col, axis=1)
            except ValueError:
                if verbose > 0:
                    print("there is no {} column\nColumns available are : {}".format(col, df.columns))
                break

        yield key_word, full_loc, df
