"""Gradient waveform generation for 4D flow MRI."""

import numpy as np
from pypulseq.make_trap_pulse import make_trapezoid

def make_readout_gradient(fov, n_readout, system, duration=None):
    """
    Create a readout gradient.
    
    Parameters:
    -----------
    fov : float
        Field of view in meters
    n_readout : int
        Number of readout points
    system : Opts
        System limits
    duration : float, optional
        Duration of the readout gradient in seconds
        
    Returns:
    --------
    gx_pre : Prephasing gradient
    gx_readout : Readout gradient
    """
    delta_k = 1 / fov
    k_width = n_readout * delta_k
    
    gx_pre = make_trapezoid(channel='x', system=system, area=-k_width/2, duration=0.5e-3)
    
    if duration is None:
        flat_time = 2e-3
        gx_readout = make_trapezoid(channel='x', system=system, area=k_width, duration=flat_time + 0.6e-3, flat_time=flat_time)
    else:
        flat_time = duration - 0.6e-3
        gx_readout = make_trapezoid(channel='x', system=system, area=k_width, duration=duration, flat_time=flat_time)
    
    return gx_pre, gx_readout

def make_phase_encoding_gradient(fov, n_phase, phase_index, system):
    """
    Create a phase encoding gradient.
    
    Parameters:
    -----------
    fov : float
        Field of view in meters
    n_phase : int
        Number of phase encoding steps
    phase_index : int
        Current phase encoding index
    system : Opts
        System limits
        
    Returns:
    --------
    gy_phase : Phase encoding gradient
    """
    delta_k = 1 / fov
    phase_area = (phase_index - n_phase / 2) * delta_k
    gy_phase = make_trapezoid(channel='y', system=system, area=phase_area, duration=0.5e-3)
    
    return gy_phase

def make_slice_encoding_gradient(fov, n_slice, slice_index, system):
    """
    Create a slice encoding gradient for 3D imaging.
    
    Parameters:
    -----------
    fov : float
        Field of view in meters
    n_slice : int
        Number of slice encoding steps
    slice_index : int
        Current slice encoding index
    system : Opts
        System limits
        
    Returns:
    --------
    gz_phase : Slice encoding gradient
    """
    delta_k = 1 / fov
    slice_area = (slice_index - n_slice / 2) * delta_k
    gz_phase = make_trapezoid(channel='z', system=system, area=slice_area, duration=0.5e-3)
    
    return gz_phase