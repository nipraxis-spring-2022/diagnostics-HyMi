""" Module with routines for finding outliers
"""

import os.path as op
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import nipraxis


def detect_outliers(fname):
    img = nib.load(fname)
    data = img.get_fdata()

    # make a 1D vector with all voxel values
    data_1d = np.ravel(data)

    # sample n_samples means to get a reasonable range of voxel values
    n_samples = 1000
    sample_means = np.zeros(n_samples)
    rng = np.random.default_rng()

    for i in range(n_samples):
        sample = rng.choice(data_1d, size=n_samples, replace=False)
        sample_means[i] = np.mean(sample)

    # standard deviation of sampling distribution of mean
    # this is smaller than the std of the original voxel values (more conservative)
    sample_std = np.std(sample_means)

    # use (mean +/- c*std) as a criteria for selecting outliers
    # c (0-1) controls the conservativeness (smaller value = more conservative)
    criteria_lwr = np.mean(sample_means) - 0.4*sample_std
    criteria_upr = np.mean(sample_means) + 0.4*sample_std

    outliers_index = np.array([])

    for v in np.arange(data.shape[-1]):
        # if a volume has voxels with values outside the criteria, mark as outlier
        vol_data_1d = np.ravel(data[:, :, :, v])
        vol_mean = np.mean(vol_data_1d)
        if vol_mean < criteria_lwr or vol_mean > criteria_upr:
            outliers_index = np.append(outliers_index, v)

    #import pdb
    #pdb.set_trace()
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
