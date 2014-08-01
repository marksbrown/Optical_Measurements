"""
Functions used to process Imaging Sphere Data

Author : Mark S. Brown
Started : Thursday 16th January 2014
"""

from __future__ import division, print_function
import re
from itertools import tee, izip
from .main import recursive_data_search
from numpy import loadtxt

def parse_export_data(key_words, root_loc, verbose=0):

    for key_word, full_loc in recursive_data_search(key_words, root_loc, allowed_ext=('txt')):
        yield full_loc, parse_filename(full_loc), parse_single_measurement(full_loc)

def parse_filename(full_loc, default_value='0'):
    """Full file location contains useful information key_word, incident_angle and repeated file
    Example :: raw_data/imaging_sphere/ptfe-cc/PTFE_single_layer_I20_P0_X0_Y0B.txt """

    key_word, incident_angle = re.findall('.*/(.*)_I(\d*)', full_loc)[0]

    multiple_file = re.findall('.*\d(.).txt', full_loc)

    if len(multiple_file) < 1:
        multiple_file = 0
    else:
        multiple_file = multiple_file[0]

    return key_word, float(incident_angle), multiple_file

def parse_single_measurement(full_loc, verbose=0):
    """
    Parse individual 'export data' files from IS-SA software produced by the Imaging Sphere
    """
    return loadtxt(full_loc, skiprows=9)


def parse_bsdf(key_words, root_loc, verbose=0):

    for key_word, full_loc in recursive_data_search(key_words, root_loc, allowed_ext=('brdf')):
        yield key_word, full_loc, parse_BRDF_rawdata(full_loc, verbose=verbose)

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def parse_BRDF_rawdata(full_loc, verbose=0):
    """
    Function to parse BRDF data from Radiant Zemax Imaging Sphere

    --args--
    full_loc - absolute location and full_loc of raw data we wish to process
    verbose - verbosity control
    """

    length_of_data = {}  # Expected size of each parameter
    key_word_data = {}  # Values of each key from the subsequent line
    raw_data = {}  # output of data

    preamble_finished = False

    for previous_line, next_line in pairwise(open(full_loc, 'r')):

        previous_line = previous_line.strip('\r\n')
        next_line = next_line.strip('\r\n')

        if previous_line == 'DataBegin':
            preamble_finished = True

        if next_line == 'DataEnd':
            break

        if not preamble_finished:
            splitted_line = re.split('\s*', previous_line)

            if len(splitted_line) == 2:
                key, value = splitted_line

                try:
                    float(value)
                except ValueError:
                    continue

                length_of_data[key] = float(value)
                key_word_data[key] = [float(value) for value in re.split('\s*', next_line) if value]

                assert length_of_data[key] == len(key_word_data[key]), "Number of parameters does not match predicted!"

            continue

        if next_line.startswith('Wavelength'):
            current_angle_index = 0
            current_wavelength = float(re.split('\s*', next_line)[-1])
            raw_data[current_wavelength] = {key : [] for key in key_word_data['AngleOfIncidence']}
            continue

        if next_line.startswith('TIS'):  # increment incident angle
            current_angle = key_word_data['AngleOfIncidence'][current_angle_index]
            current_angle_index += 1
            continue

        if not next_line:  # Skips empty lines
            continue

        if next_line.startswith('Tris'):  # TODO :: Colour information is currently not used
            continue

        raw_data[current_wavelength][current_angle].append([float(value) for value in next_line.split('\t')])


    return key_word_data, raw_data

