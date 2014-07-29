"""
UV Spectrophotometer Code

Code used to process UV spectrophotometer data
"""

from .main import recursive_data_search
import pandas as pd

def fetch_data(key_words):
    """
    fetches and cleans data for key_word(s) passed to function
    from UV spectrophotometer
    """

    for key_word, full_loc in recursive_data_search(key_words):
        yield key_word, full_loc, pd.read_csv(full_loc, skiprows=1, sep=",")
