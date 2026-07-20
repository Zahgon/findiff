import itertools
from itertools import product

import numpy as np


def interior_mask_as_ndarray(shape):
    pass


def all_index_tuples_as_list(shape):
    pass


def get_long_indices_for_all_grid_points_as_ndarray(shape):
    return get_long_indices_for_all_grid_points_as_1d_array(shape).reshape(shape)


def get_long_indices_for_all_grid_points_as_1d_array(shape):
    return np.arange(np.prod(shape), dtype=np.int64)


def to_long_index(idx, shape):

    ndims = len(shape)
    long_idx = 0
    siz = 1
    for axis in range(ndims):
        idx_ = idx[ndims - 1 - axis]
        long_idx += idx_ * siz
        siz *= shape[ndims - 1 - axis]

    return long_idx


def to_index_tuple(long_idx, shape):
    pass


def get_list_of_multiindex_tuples(shape):
    short_inds = [np.arange(shape[k]) for k in range(len(shape))]
    short_inds = list(itertools.product(*short_inds))
    return short_inds


