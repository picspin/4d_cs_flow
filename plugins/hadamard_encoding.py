def make_hadamard_encoding(seq, venc, system):
    """
    Create Hadamard-encoded velocity encoding gradients
    
    Parameters:
    -----------
    seq : Sequence
        Sequence object
    venc : float
        Velocity encoding value in m/s
    system : Opts
        System limits
        
    Returns:
    --------
    encoding_schemes : list
        List of gradient combinations for Hadamard encoding
    """
    # Create basic bipolar gradients for each direction
    bip_x, bip_x_neg = make_bipolar_gradient(seq, 'x', venc, system)
    bip_y, bip_y_neg = make_bipolar_gradient(seq, 'y', venc, system)
    bip_z, bip_z_neg = make_bipolar_gradient(seq, 'z', venc, system)
    
    # Define Hadamard encoding matrix
    # [1  1  1  1]
    # [1  1 -1 -1]
    # [1 -1  1 -1]
    # [1 -1 -1  1]
    
    # Define encoding schemes
    encoding_schemes = [
        {'x': None, 'y': None, 'z': None},  # Reference (no encoding)
        {'x': bip_x, 'y': bip_y, 'z': bip_z},  # All positive
        {'x': bip_x, 'y': bip_y, 'z': bip_z_neg},  # x+, y+, z-
        {'x': bip_x, 'y': bip_y_neg, 'z': bip_z}   # x+, y-, z+
    ]
    
    return encoding_schemes