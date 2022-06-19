from numba import jit, njit
import numpy as np


@njit(parallel=True)
def scaled_window(window: np.ndarray, criteria):
    window = (window - criteria) / criteria
    return window 
