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

def parse_time_data(file_parameters, verbose=0):
    """
    Returns clean Pandas DataFrame when given useful file_parameters for associated data
    of form key_word : (
    """

    for key_word, full_loc in recursive_data_search(file_parameters.keys(), allowed_ext=('txt')):

        specific_parameters = file_parameters[key_word]
        with open(full_loc, 'r') as f:

                for k, a_line in enumerate(f):
                    if a_line.startswith('0.00'):
                        columns_to_pull = len(a_line.split(',')) - 1   # first and last columns are ignored
                        break


        columns = ['time']+list(string.uppercase[:columns_to_pull])
        df = pd.read_csv(full_loc, skiprows=k, sep=",", names=columns)

        df.index = df.time

        for col in chain(('time', columns[-1]), specific_parameters['dropcols']):
            df = df.drop(col, axis=1)

        yield key_word, full_loc, df
