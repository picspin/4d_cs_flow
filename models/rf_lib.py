"""RF pulse generation for 4D flow MRI."""

import numpy as np
from pypulseq.make_sinc_pulse import make_sinc_pulse

def make_excitation_pulse(flip_angle, duration, slice_thickness, system):
    """
    Create an excitation RF pulse.
    
    Parameters:
    -----------
    flip_angle : float
        Flip angle in degrees
    duration : float
        Pulse duration in seconds
    slice_thickness : float
        Slice thickness in meters
    system : Opts
        System limits
        
    Returns:
    --------
    rf : RF pulse
    gz : Slice-select gradient
    """
    rf, gz, _ = make_sinc_pulse(flip_angle=flip_angle, duration=duration,
                                 slice_thickness=slice_thickness,
                                 apodization=0.5, time_bw_product=4,
                                 system=system, return_gz=True)
    
    return rf, gz

def make_refocusing_pulse(flip_angle, duration, slice_thickness, system):
    """
    Create a refocusing RF pulse.
    
    Parameters:
    -----------
    flip_angle : float
        Flip angle in degrees
    duration : float
        Pulse duration in seconds
    slice_thickness : float
        Slice thickness in meters
    system : Opts
        System limits
        
    Returns:
    --------
    rf : RF pulse
    gz : Slice-select gradient
    """
    rf, gz, _ = make_sinc_pulse(flip_angle=flip_angle, duration=duration,
                                 slice_thickness=slice_thickness,
                                 apodization=0.5, time_bw_product=8,
                                 system=system, return_gz=True)
    
    return rf, gz