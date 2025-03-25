def add_navigator_echo(seq, system):
    """
    Add a navigator echo for respiratory motion tracking
    
    Parameters:
    -----------
    seq : Sequence
        Sequence object
    system : Opts
        System limits
        
    Returns:
    --------
    None
    """
    # Create a pencil-beam excitation
    rf_nav, gz_nav, _ = make_sinc_pulse(flip_angle=10, duration=1e-3, 
                                       slice_thickness=30e-3, 
                                       apodization=0.5, time_bw_product=4,
                                       system=system, return_gz=True)
    
    # Create readout gradient for navigator
    gz_nav_readout = make_trap_pulse(channel='z', system=system, 
                                    area=1/30e-3 * 64, duration=3e-3, 
                                    flat_time=2e-3)
    
    # ADC for navigator
    adc_nav = make_adc(num_samples=64, duration=2e-3, 
                      delay=0.5e-3, system=system)
    
    # Add navigator blocks to sequence
    seq.add_block(rf_nav, gz_nav)
    seq.add_block(gz_nav_readout, adc_nav)