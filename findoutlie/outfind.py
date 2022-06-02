"""
Module for identify outliers. Ran using python3 scripts/find_outliers.py data
"""

import os.path as op
from glob import glob
import numpy as np
import nibabel as nib



def detect_outliers(fname):
    img = nib.load(fname) # takes in image from the input from find_outliers.py that is used below:
                        # image_fnames = glob(op.join(data_directory, '**', 'sub-*.nii.gz'), recursive=True)
    data = img.get_fdata()

    # Convert the 4D image to a 1D vector with all voxel values
    data_1d = np.ravel(data)

    # There are approximately 20 million voxels, we will sample a 00.1%, or 22000, voxel population to use in subsequent steps
    voxel_N_tosample = int(len(data_1d)*.001)

    # sample n_samples means to get a reasonable range of voxel values to create population distribution
    n_samples = 1000

    # create an array that has zeros for our n = 1000 population
    sample_means = np.zeros(n_samples)
    rng = np.random.default_rng()

    for i in range(n_samples):
        # randomly selects a subsample, with replacement, from the 1D data for a 00.1% of the voxels
        sample = rng.choice(data_1d, size=voxel_N_tosample, replace=True)

        # Calculates the mean from the subsample of voxels
        sample_means[i] = np.mean(sample)

    # standard deviation of sampling distribution of mean
    # this is smaller than the std of the original voxel values (more conservative)
    sample_std = np.std(sample_means)

    # use (mean +/- 1.5*std) as a criteria for selecting outliers
    # 1.5 is the conservativeness (larger value = more conservative)
        # future iterations of the 1.5 can be optimized on a larger dataset
    criteria_lwr = np.mean(sample_means) - 1.5*sample_std
    criteria_upr = np.mean(sample_means) + 1.5*sample_std

    outliers_index = np.array([])


    for v in np.arange(data.shape[-1]):
        # if a volume has voxels with values outside the criteria, mark as outlier
        vol_data_1d = np.ravel(data[:, :, :, v])
        vol_mean = np.mean(vol_data_1d)

        # defining which means for a given volume are 1.5*SD below or  above the population mean
        # appends the index of outlier
        if vol_mean < criteria_lwr or vol_mean > criteria_upr:
            outliers_index = np.append(outliers_index, v)

    #import pdb
    #pdb.set_trace()

    # returning all indices for our outliers
    return outliers_index


def find_outliers(data_directory):
    """ Return filenames and outlier indices for images in `data_directory`.

    Parameters
    ----------
    data_directory : str
        Directory containing containing images.

    Returns
    -------
    outlier_dict : dict
        Dictionary with keys being filenames and values being lists of outliers
        for filename.
    """
    image_fnames = glob(op.join(data_directory, '**', 'sub-*.nii.gz'),
                        recursive=True)
    # import pdb
    # pdb.set_trace()
    outlier_dict = {}
    for fname in image_fnames:
        outliers = detect_outliers(fname)
        outlier_dict[fname] = outliers
    return outlier_dict

