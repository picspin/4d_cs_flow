"""Compressed sensing sampling patterns for 4D flow MRI."""

import numpy as np

def generate_variable_density_mask(n_phase, n_slice, acceleration_factor, center_fraction=0.04):
    """
    Generate a variable-density sampling mask for compressed sensing.
    
    Parameters:
    -----------
    n_phase : int
        Number of phase encoding steps
    n_slice : int
        Number of slice encoding steps
    acceleration_factor : float
        Acceleration factor (e.g., 4 for 4x acceleration)
    center_fraction : float
        Fraction of k-space center to fully sample
        
    Returns:
    --------
    mask : ndarray
        2D sampling mask (n_phase x n_slice)
    """
    mask = np.zeros((n_phase, n_slice))
    
    center_p = int(n_phase * center_fraction)
    center_s = int(n_slice * center_fraction)
    p_start = n_phase // 2 - center_p // 2
    p_end = p_start + center_p
    s_start = n_slice // 2 - center_s // 2
    s_end = s_start + center_s
    mask[p_start:p_end, s_start:s_end] = 1
    
    n_center = np.sum(mask)
    n_total = int(n_phase * n_slice / acceleration_factor)
    n_random = n_total - n_center
    
    y, x = np.mgrid[:n_phase, :n_slice]
    x = (x - n_slice / 2) / (n_slice / 2)
    y = (y - n_phase / 2) / (n_phase / 2)
    r = np.sqrt(x**2 + y**2)
    pdf = (1 - r)**2
    pdf[mask == 1] = 0
    
    if np.sum(pdf) > 0:
        pdf = pdf / np.sum(pdf)
    
    indices = np.random.choice(n_phase * n_slice, size=n_random, replace=False, p=pdf.flatten())
    y_indices, x_indices = np.unravel_index(indices, (n_phase, n_slice))
    mask[y_indices, x_indices] = 1
    
    return mask