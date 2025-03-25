"""Utility functions for working with pypulseq."""

# def check_sequence_timing(seq):
#     """
#     Check if the sequence timing is valid.
    
#     Parameters:
#     -----------
#     seq : Sequence
#         Sequence object
        
#     Returns:
#     --------
#     ok : bool
#         True if timing is valid, False otherwise
#     error_report : str
#         Report of timing errors
#     """
#     ok, error_report = seq.check_timing()
#     return ok, error_report 

import numpy as np
from pypulseq.Sequence.sequence import Sequence
from pypulseq.calc_duration import calc_duration

def check_sequence_timing(seq):
    """
    Check if the sequence timing is valid.
    
    Parameters:
    -----------
    seq : Sequence
        Sequence object
        
    Returns:
    --------
    ok : bool
        True if timing is valid, False otherwise
    error_report : str
        Report of timing errors
    """
    ok, error_report = seq.check_timing()
    return ok, error_report

def calculate_sequence_duration(seq):
    """
    Calculate the total duration of the sequence.
    
    Parameters:
    -----------
    seq : Sequence
        Sequence object
        
    Returns:
    --------
    duration : float
        Total duration of the sequence in seconds
    """
    return seq.duration()[0]

def set_sequence_definitions(seq, params):
    """
    Set sequence definitions based on parameters.
    
    Parameters:
    -----------
    seq : Sequence
        Sequence object
    params : SequenceParams
        Sequence parameters
        
    Returns:
    --------
    seq : Sequence
        Updated sequence object
    """
    # Required definitions
    seq.set_definition('GradientRasterTime', params.system.grad_raster_time)
    seq.set_definition('RadiofrequencyRasterTime', params.system.rf_raster_time)
    seq.set_definition('AdcRasterTime', params.system.adc_raster_time)
    seq.set_definition('BlockDurationRaster', params.system.block_duration_raster)
    
    # Optional definitions
    seq.set_definition('Name', params.name)
    seq.set_definition('FOV', params.fov)
    seq.set_definition('VoxelSize', params.resolution)
    seq.set_definition('VENC', params.venc)
    seq.set_definition('TR', params.tr)
    seq.set_definition('TE', params.te)
    seq.set_definition('FlipAngle', params.flip_angle)
    seq.set_definition('AccelerationFactor', params.acceleration_factor)
    
    return seq

def calculate_block_duration(events, system):
    """
    Calculate the minimum block duration required for a set of events.
    
    Parameters:
    -----------
    events : dict
        Dictionary of events (rf, gx, gy, gz, adc)
    system : SystemConfig
        System configuration
        
    Returns:
    --------
    duration : float
        Minimum block duration in seconds
    """
    max_duration = 0
    
    # Check each event type
    for event_type, event in events.items():
        if event is not None:
            event_duration = calc_duration(event)
            max_duration = max(max_duration, event_duration)
    
    # Round up to the nearest block duration raster
    block_duration_raster = system.block_duration_raster
    duration_in_raster = np.ceil(max_duration / block_duration_raster)
    
    return duration_in_raster * block_duration_raster