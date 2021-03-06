""" Python script to find outliers using the outfind.py commands


This is the python script put together to detect outliers by Hyesue & Michael as part of the HyMi Nipraxis group
Run as:
    python3 scripts/find_outliers.py data

It runs within the findoulie module that was created for the course
"""

import os.path as op
import sys

from argparse import ArgumentParser, RawDescriptionHelpFormatter

# Put the findoutlie directory on the Python path.
PACKAGE_DIR = op.join(op.dirname(__file__), '..')
sys.path.append(PACKAGE_DIR)

# Importing the findoutlie module which is located in *diagnostics-HyMi/findoutlie
from findoutlie import outfind

if len(sys.argv) != 2:
    print(" \nThis scripts identifies outliers on all *nii.gz files within a subject directory (e.g., sub-01) or directory with subjects data (e.g. data/group-01)")
    print(" Usage: python find_outliers.py <data folder> <SD threshold>")
    print(" Example: python3 scripts/find_outliers.py data/group-01")
    sys.exit()

def print_outliers(data_directory):
    outlier_dict = outfind.find_outliers(data_directory)
    for fname, outliers in outlier_dict.items():
        if len(outliers) == 0:
            continue
        outlier_strs = []
        for out_ind in outliers:
            outlier_strs.append(str(out_ind))
        print(', '.join([fname] + outlier_strs))


def get_parser():
    parser = ArgumentParser(description=__doc__,  # Usage from docstring
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('data_directory',
                        help='Directory containing data')
    return parser


def main():
    # This function (main) called when this file run as a script.
    # Get the data directory from the command line arguments
    parser = get_parser()
    args = parser.parse_args()
    # Call function to find outliers.
    print_outliers(args.data_directory)


if __name__ == '__main__':
    # Python is running this file as a script, not importing it.
    main()
