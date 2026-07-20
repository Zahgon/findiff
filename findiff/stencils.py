import math
from itertools import product

import numpy as np

from .utils import to_index_tuple, to_long_index


class StencilSet:

    def __init__(self, diff_op, shape, old_stl=None):
        """
        Constructor for Stencil objects.

        :param shape: tuple of ints
            Shape of the grid on which the stencil should be applied.

        :param axis: int >= 0
            The coordinate axis along which to take the partial derivative.

        :param order: int > 0
            The order of the derivative.

        :param h: float
            The spacing of the (equidistant) grid

        """

        self.shape = shape
        self.diff_op = diff_op
        self.char_pts = self._det_characteristic_points()

        self.data = {}

        self._create_stencil()

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

    def apply(self, u, idx0):
        pass

    def apply_all(self, u):
        pass

    def _create_stencil(self):
        pass

    def _typical_index_tuple_for_char_point(self, pt):
        pass

    def _det_characteristic_points(self):
        pass


class Stencil:

    def __init__(self, offsets, partials, spacings=None):

        self.partials = partials
        self.max_order = 100
        if not hasattr(offsets[0], "__len__"):
            ndims = 1
            self.offsets = [(off,) for off in offsets]
        else:
            ndims = len(offsets[0])
            self.offsets = offsets

        if spacings is None:
            spacings = [1] * ndims
        elif not hasattr(spacings, "__len__"):
            spacings = [spacings] * ndims
        assert len(spacings) == ndims
        self.spacings = spacings
        self.ndims = ndims
        self.sol, self.sol_as_dict = self._make_stencil()

    def __call__(self, f, at=None, on=None):
        if at is not None and on is None:
            return self._apply_at_single_point(f, at)
        if at is None and on is not None:
            if isinstance(on[0], slice):
                return self._apply_on_multi_slice(f, on)
            else:
                return self._apply_on_mask(f, on)
        raise Exception('Cannot specify both *at* and *on* parameters.')

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return str(self.values)

    def _apply_on_mask(self, f, mask):
        pass

    def _apply_on_multi_slice(self, f, on):
        pass

    def _apply_at_single_point(self, f, at):
        pass

    def _make_offset_mask(self, mask, offset):
        pass

    def _canonic_slice(self, sl, length):
        pass

    @property
    def values(self):
        pass

    @property
    def accuracy(self):
        pass

    def _calc_accuracy(self):
        tol = 1.E-6
        deriv_order = 0
        for pows in self.partials.keys():
            order = sum(pows)
            if order > deriv_order:
                deriv_order = order
        for order in range(deriv_order, deriv_order + 10):
            terms = self._multinomial_powers(order)
            for term in terms:
                row = self._system_matrix_row(term)
                resid = np.sum(np.array(self.sol) * np.array(row))
                if abs(resid) > tol and term not in self.partials:
                    return order - deriv_order

    def _make_stencil(self):
        pass

    def _system_matrix(self):
        pass

    def _system_matrix_row(self, powers):
        row = []
        for a in self.offsets:
            value = 1
            for i, power in enumerate(powers):
                value *= a[i] ** power
            row.append(value)
        return row

    def _multinomial_powers(self, the_sum):
        """Returns all tuples of a given dimension that add up to the_sum."""
        all_combs = list(product(range(the_sum + 1), repeat=self.ndims))
        return list(filter(lambda tpl: sum(tpl) == the_sum, all_combs))

    def _rows_are_linearly_independent(self, matrix):
        pass
