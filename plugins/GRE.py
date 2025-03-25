def make_gre_module(seq, fov, n_readout, slice_thickness, flip_angle, 
                    system, te, tr, phase_index, slice_index, flow_encoding):
    """
    Create a gradient echo module with flow encoding
    
    Parameters:
    -----------
    seq : Sequence
        Sequence object
    fov : float
        Field of view in meters
    n_readout : int
        Number of readout points
    slice_thickness : float
        Slice thickness in meters
    flip_angle : float
        Flip angle in degrees
    system : Opts
        System limits
    te : float
        Echo time in seconds
    tr : float
        Repetition time in seconds
    phase_index : int
        Phase encoding index
    slice_index : int
        Slice encoding index
    flow_encoding : str
        Flow encoding direction ('x', 'y', 'z', 'ref')
        
    Returns:
    --------
    None
    """
    # Calculate derived parameters
    delta_k = 1 / fov
    k_width = n_readout * delta_k
    
    # Create RF pulse (sinc with 3 lobes)
    rf, gz, _ = make_sinc_pulse(flip_angle=flip_angle, duration=1e-3, 
                               slice_thickness=slice_thickness, 
                               apodization=0.5, time_bw_product=4,
                               system=system, return_gz=True)
    
    # Create slice refocusing gradient
    gz_reph = make_trap_pulse(channel='z', system=system, 
                             area=-gz.area / 2, duration=1e-3)
    
    # Phase encoding gradient
    phase_area = (phase_index - n_phase/2) * delta_k
    gy_phase = make_trap_pulse(channel='y', system=system, 
                              area=phase_area, duration=1e-3)
    
    # Slice encoding gradient (for 3D)
    slice_area = (slice_index - n_slice/2) * delta_k
    gz_phase = make_trap_pulse(channel='z', system=system, 
                              area=slice_area, duration=1e-3)
    
    # Readout gradient
    gx_pre = make_trap_pulse(channel='x', system=system, 
                            area=-k_width/2, duration=1e-3)
    gx_readout = make_trap_pulse(channel='x', system=system, 
                                area=k_width, duration=3e-3, 
                                flat_time=2e-3)
    
    # ADC
    adc = make_adc(num_samples=n_readout, duration=2e-3, 
                  delay=0.5e-3, system=system)
    
    # Flow encoding gradients
    if flow_encoding != 'ref':
        bipolar, bipolar_neg = make_bipolar_gradient(seq, flow_encoding, venc, system)
    
    # Calculate timing
    delay_te = te - calc_duration(rf) - calc_duration(gz_reph) - calc_duration(gx_pre) - calc_duration(gx_readout)/2
    delay_tr = tr - calc_duration(rf) - calc_duration(gz_reph) - calc_duration(gx_pre) - calc_duration(gx_readout) - delay_te
    
    if delay_te < 0:
        raise ValueError("TE too short for sequence timing")
    if delay_tr < 0:
        raise ValueError("TR too short for sequence timing")
    
    # Add blocks to sequence
    seq.add_block(rf, gz)
    seq.add_block(gz_reph)
    
    # Add flow encoding if needed
    if flow_encoding != 'ref':
        seq.add_block(bipolar)
        seq.add_block(bipolar_neg)
    
    # Continue with phase encoding and readout
    seq.add_block(gy_phase, gz_phase, gx_pre)
    
    if delay_te > 0:
        seq.add_block(make_delay(delay_te))
    
    seq.add_block(gx_readout, adc)
    
    if delay_tr > 0:
        seq.add_block(make_delay(delay_tr))