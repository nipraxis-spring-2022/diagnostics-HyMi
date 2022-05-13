""" Python script to validate data

Run as:

    python3 scripts/validata_data.py data
"""

import os
import sys
import hashlib


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
    fobj = open(filename, 'rb')
    file_bytes = fobj.read()
    fobj.close()

    # Calculate, return SHA1 has on the bytes from the file.
    hash_value = hashlib.sha1(file_bytes).hexdigest()
    return hash_value


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
    import os.path as op
    import numpy as np

    #data_directory = '/Users/hyesue/Research/nipraxis/week5/collab/diagnostics-HyMi/data/group-01'
    fname = op.join(data_directory, 'hash_list.txt')
    hash_list = np.loadtxt(fname, dtype='str')
    # Split into SHA1 hash and filename

    # Calculate actual hash for given filename.
    for i in range(0, np.shape(hash_list)[0]):
        fname = data_directory + '/../' + hash_list[i,1]

        this_file_hash = file_hash(fname)

        # If hash for filename is not the same as the one in the file, raise
        # ValueError
        if this_file_hash != hash_list[i,0]:
            raise NotImplementedError('Not valid.')


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
