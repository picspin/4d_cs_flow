def create_4d_flow_sequence(seq, system, fov, n_readout, n_phase, n_slice, 
                           n_cardiac_phases, slice_thickness, tr, te, 
                           flip_angle, venc, acceleration_factor=4):
    """
    Create a complete 4D flow MRI sequence
    
    Parameters:
    -----------
    seq : Sequence
        Sequence object
    system : Opts
        System limits
    fov : float
        Field of view in meters
    n_readout : int
        Number of readout points
    n_phase : int
        Number of phase encoding steps
    n_slice : int
        Number of slices
    n_cardiac_phases : int
        Number of cardiac phases
    slice_thickness : float
        Slice thickness in meters
    tr : float
        Repetition time in seconds
    te : float
        Echo time in seconds
    flip_angle : float
        Flip angle in degrees
    venc : float
        Velocity encoding value in m/s
    acceleration_factor : float
        Acceleration factor for compressed sensing
        
    Returns:
    --------
    seq : Sequence
        Completed sequence object
    """
    # Generate sampling mask for compressed sensing
    mask = generate_variable_density_mask(n_phase, n_slice, acceleration_factor)
    
    # Generate k-space sampling order using ReCAR
    sampling_order = recar_reordering(mask, n_cardiac_phases)
    
    # Add sequence blocks for each point in the sampling order
    for p_idx, s_idx, c_phase in sampling_order:
        # For each k-space point, we need 4 acquisitions (reference + 3 flow encodings)
        # Reference scan (no flow encoding)
        make_gre_module(seq, fov, n_readout, slice_thickness, flip_angle, 
                       system, te, tr, p_idx, s_idx, 'ref')
        
        # X flow encoding
        make_gre_module(seq, fov, n_readout, slice_thickness, flip_angle, 
                       system, te, tr, p_idx, s_idx, 'x')
        
        # Y flow encoding
        make_gre_module(seq, fov, n_readout, slice_thickness, flip_angle, 
                       system, te, tr, p_idx, s_idx, 'y')
        
        # Z flow encoding
        make_gre_module(seq, fov, n_readout, slice_thickness, flip_angle, 
                       system, te, tr, p_idx, s_idx, 'z')
    
    # Set sequence parameters
    seq.set_definition('FOV', [fov, fov, n_slice*slice_thickness])
    seq.set_definition('Name', '4D_flow_CS_ReCAR')
    seq.set_definition('VoxelSize', [fov/n_readout, fov/n_phase, slice_thickness])
    seq.set_definition('VENC', venc)
    
    return seq