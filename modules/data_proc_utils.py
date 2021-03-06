"""
Data processing utilities.
"""

from typing import List, Optional, Union
import numpy as np
import pandas as pd

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


def unstack_corr_df(corr: pd.DataFrame,
                    ascending: bool = False,
                    col_name_1: Optional[str] = 'col_1',
                    col_name_2: Optional[str] = 'col_2') -> pd.DataFrame:
    r"""
    Unstuck a correlation matrix to a DataFrame that contains correlations between 'variable_1'
    and 'variable_2' in a column.
    Rows with duplicated correlations and self-correlations are removed.

    Parameters
    ----------
    corr: pd.DataFrame
        Correlation matrix. Typically given by ``DataFrame.corr()`` function.
    ascending: bool
        If sort the correlation in ascending order. Default ``False``, meaning sort in descending order.
    col_name_1: Optional[str]
        Column name of 'variable_1'. Default 'col_1'.
    col_name_2: Optional[str]
        Column name of 'variable_2'.

    Returns
    -------
    pd.DataFrame
        DataFrame has first column as 'variable_1' names, second column as 'variable_2' names and third column as
        correlations between 'variable_1' and 'variable_2'.

    Examples
    --------
    >>> df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [1.5, 2.3, 3.2, 4.1]})
       A    B
    0  1  1.5
    1  2  2.3
    2  3  3.2
    3  4  4.1
    >>> df_correlation = unstack_corr_df(df.corr())
      col_1 col_2      corr
    0     B     A  0.999604
    >>> np.corrcoef(df['A'], df['B'])
    array([[1.        , 0.99960388],
           [0.99960388, 1.        ]])
    """

    corr_uns = corr.unstack()
    corr_uns_sorted = corr_uns.sort_values(ascending=ascending)
    df_corr = corr_uns_sorted.to_frame()
    df_corr.reset_index(drop=False, inplace=True)
    df_corr = df_corr.query('level_0 != level_1')
    df_corr_cols = df_corr[['level_0', 'level_1']]
    dup_mask = ~df_corr_cols.apply(sorted, 1).astype(str).duplicated()
    df_corr = df_corr[dup_mask]
    df_corr.columns = [col_name_1, col_name_2, 'corr']
    df_corr.reset_index(drop=True, inplace=True)

    return df_corr
