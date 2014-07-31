"""
========================
Optical Measurement Code
========================

Started : 29th July 2014
Author : Mark S. Brown

Description
-----------
In this module functions used to process and plot data from
optical experiments conducted on the 9th floor lab are collected.

Associated Ipython notebooks analyse and annotate collected raw_data
"""

from __future__ import print_function, division
from collections import Iterable
import os

def recursive_data_search(key_words, allowed_ext=('txt', 'brdf'), ignored_directories=('optical_measurement_module', 'archive', '/.'), verbose=0):
    """
    Traversal over directory to yield full location of matching files
    """

    if isinstance(key_words, Iterable) and isinstance(key_words, str):
        key_words = [key_words, ]

    for key_word in key_words:
        for root, directories, all_files in os.walk(os.getcwd()):

            if any(root.find(a_directory) >= 0 for a_directory in ignored_directories):
                if verbose > 0:
                    print("Skipping", root)
                continue

            for a_file in all_files:

                if verbose > 0:
                    print("Root : {} \nFile: {}".format(root, a_file))

                if not any(a_file.endswith(ext) for ext in allowed_ext) or not a_file.startswith(key_word):
                    continue

                if verbose > 0:
                     print(a_file)
                yield key_word, os.path.join(root, a_file)
