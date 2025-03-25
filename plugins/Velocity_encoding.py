def make_bipolar_gradient(seq, axis, venc, system):
    """
    Create a bipolar gradient for velocity encoding
    
    Parameters:
    -----------
    seq : Sequence
        Sequence object
    axis : str
        Gradient axis ('x', 'y', or 'z')
    venc : float
        Velocity encoding value in m/s
    system : Opts
        System limits
        
    Returns:
    --------
    bipolar : Gradient
        Bipolar gradient object
    """
    # Calculate the first moment for the desired venc
    gamma = 42.58e6  # Hz/T
    m1 = np.pi / (gamma * venc)
    
    # Design a bipolar gradient
    area = m1 / 2  # Area of each lobe
    duration = 1e-3  # Duration of the entire bipolar pulse (1 ms)
    amplitude = area / (duration / 2)
    
    if amplitude > system.max_grad:
        # Adjust duration if amplitude exceeds system limits
        duration = 2 * area / system.max_grad
        amplitude = system.max_grad
    
    # Create the bipolar gradient
    if axis == 'x':
        bipolar = make_trap_pulse(channel='x', system=system, 
                                  area=area, duration=duration/2)
        bipolar_neg = make_trap_pulse(channel='x', system=system, 
                                     area=-area, duration=duration/2)
    elif axis == 'y':
        bipolar = make_trap_pulse(channel='y', system=system, 
                                  area=area, duration=duration/2)
        bipolar_neg = make_trap_pulse(channel='y', system=system, 
                                     area=-area, duration=duration/2)
    elif axis == 'z':
        bipolar = make_trap_pulse(channel='z', system=system, 
                                  area=area, duration=duration/2)
        bipolar_neg = make_trap_pulse(channel='z', system=system, 
                                     area=-area, duration=duration/2)
    
    return bipolar, bipolar_neg