"""
Utilities used as math tools.
"""

from typing import List, Union
import numpy as np

LST = Union[List[int], np.ndarray]


def get_consecutive_num_intervals(arr: LST, ret_idx: bool = True) -> np.ndarray:
    r"""
    Identify groups of continuous numbers in a list.

    Parameters
    ----------
    arr: List[int], np.ndarray
        List-like
    ret_idx: bool
        Specify return to be whether return group boundary indexes or group
        numbers. Default ``True``, meaning return boundary indexes. Set to
        ``False`` to return group numbers.

    Returns
    -------
    np.ndarray
        Either group boundary indexes or group numbers.

    Examples
    --------
    >>> data = np.array([2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 20])
    >>> group_boundary_idx = get_consecutive_num_intervals(data, ret_idx=True)
    [[0, 3], [4, 9], [10, 10]]
    >>> grouped_numbers = get_consecutive_num_intervals(data, ret_idx=False)
    [array([2, 3, 4, 5]), array([12, 13, 14, 15, 16, 17]), array([20])]

    References
    ----------
    [1] https://stackoverflow.com/questions/2154249/identify-groups-of-continuous-numbers-in-a-list
    """

    bound_idx = [_i for _i, _diff in enumerate(np.diff(arr)) if not _diff == 1]
    bound_idx = np.hstack([-1, bound_idx, len(arr) - 1])
    bound_idx = np.vstack([bound_idx[:-1] + 1, bound_idx[1:]]).T

    if ret_idx:
        return bound_idx
    else:
        return np.array([np.arange(arr[_s], arr[_e]+1) for _s, _e in bound_idx])
