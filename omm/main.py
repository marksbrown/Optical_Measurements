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

def recursive_data_search(key_words, root_dir, allowed_ext=('txt', 'brdf'),
        ignored_directories=('optical_measurement_module', 'archive', '/.'), verbose=0):
    """
    Traversal over directory to yield full location of matching files
    """

    if isinstance(key_words, Iterable) and isinstance(key_words, str):
        key_words = [key_words, ]  # if only a single key_word, allows correct iteration

    for key_word in key_words:
        for root, directories, all_files in os.walk(root_dir):

            if any(root.find(a_directory) >= 0 for a_directory in ignored_directories):
                print("Skipping", root)
                continue

            for a_file in all_files:

                if verbose > 0:
                    print("Root : {} \nFile: {}".format(root, a_file))

                if key_word != '':
                    if a_file.find(key_word) < 0:
                        continue

                if not any(a_file.endswith(ext) for ext in allowed_ext): 
                    continue

                if verbose > 0:
                     print(a_file)
                yield key_word, os.path.join(root, a_file)
