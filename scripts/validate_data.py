""" Python script to validate data

Run as:

    python3 scripts/validata_data.py data
"""


import os.path as op
import sys
import hashlib
import os

def file_hash(filename):
    """ Get byte contents of file `filename`, return SHA1 hash

    Parameters
    ----------
    filename : str
        Name of file to read

    Returns
    -------
    hash : str
        SHA1 hexadecimal hash string for contents of `filename`.
    """
    # Open the file, read contents as bytes.
    # Calculate, return SHA1 has on the bytes from the file.
    with open(filename, 'rb') as fobj:
        contents = fobj.read()
    return hashlib.sha1(contents).hexdigest()


def validate_data(data_directory):
    """ Read ``hash_list.txt`` file in ``data_directory``, check hashes

    An example file ``data_hashes.txt`` is found in the baseline version
    of the repository template for your reference.

    Parameters
    ----------
    data_directory : str
        Directory containing data and ``hash_list.txt`` file.

    Returns
    -------
    None

    Raises
    ------
    ValueError:
        If hash value for any file is different from hash value recorded in
        ``hash_list.txt`` file.
    """
    # Read lines from ``hash_list.txt`` file.
    for line in open(os.path.join(data_directory, 'data_hashes.txt'), 'rt'):
    # Split into SHA1 hash and filename
    hash, filename = line.strip().split()
    # Calculate actual hash for given filename.
    actual_hash = file_hash(os.path.join(data_directory, filename))
    # If hash for filename is not the same as the one in the file, raise
    # ValueError
    if hash != actual_hash:
        raise ValueError("Hash for {} does not match".format(filename))


def main():
    # This function (main) called when this file run as a script.
    #
    # Get the data directory from the command line arguments
    if len(sys.argv) < 2:
        raise RuntimeError("Please give data directory on "
                           "command line")
    data_directory = sys.argv[1]
    # Call function to validate data in data directory
    validate_data(data_directory)

if __name__ == '__main__':
    # Python is running this file as a script, not importing it.
    main()
