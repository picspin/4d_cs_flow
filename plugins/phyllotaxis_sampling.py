def generate_phyllotaxis_sampling(n_phase, n_slice, acceleration_factor, center_fraction=0.04):
    """
    Generate a variable-density phyllotaxis sampling pattern
    
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
    # Initialize mask
    mask = np.zeros((n_phase, n_slice))
    
    # Calculate number of samples to acquire
    n_total = int(n_phase * n_slice / acceleration_factor)
    
    # Golden angle in radians
    golden_angle = np.pi * (3 - np.sqrt(5))
    
    # Generate phyllotaxis pattern
    points = []
    for i in range(n_total):
        radius = np.sqrt(i / n_total)  # Variable density (more points in center)
        theta = i * golden_angle
        
        # Convert to Cartesian coordinates
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        
        # Scale to k-space dimensions
        kx = int((x * 0.95 + 1) * n_slice / 2)
        ky = int((y * 0.95 + 1) * n_phase / 2)
        
        # Ensure within bounds
        kx = max(0, min(n_slice-1, kx))
        ky = max(0, min(n_phase-1, ky))
        
        points.append((ky, kx))
    
    # Set mask values
    for ky, kx in points:
        mask[ky, kx] = 1
    
    # Ensure center of k-space is fully sampled
    center_p = int(n_phase * center_fraction)
    center_s = int(n_slice * center_fraction)
    p_start = n_phase//2 - center_p//2
    p_end = p_start + center_p
    s_start = n_slice//2 - center_s//2
    s_end = s_start + center_s
    mask[p_start:p_end, s_start:s_end] = 1
    
    return mask