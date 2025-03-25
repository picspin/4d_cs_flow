def recar_reordering(mask, n_cardiac_phases):
    """
    Implement ReCAR k-space reordering strategy
    
    Parameters:
    -----------
    mask : ndarray
        2D sampling mask (n_phase x n_slice)
    n_cardiac_phases : int
        Number of cardiac phases
        
    Returns:
    --------
    sampling_order : list
        List of (phase_idx, slice_idx, cardiac_phase) tuples in acquisition order
    """
    n_phase, n_slice = mask.shape
    sampling_order = []
    
    # Get all points to sample
    points_to_sample = []
    for p in range(n_phase):
        for s in range(n_slice):
            if mask[p, s] == 1:
                # Calculate k-space radius (distance from center)
                kp = p - n_phase/2
                ks = s - n_slice/2
                k_radius = np.sqrt(kp**2 + ks**2)
                
                # Store point with its radius
                points_to_sample.append((p, s, k_radius))
    
    # Sort points by radius (center-out ordering)
    points_to_sample.sort(key=lambda x: x[2])
    
    # Assign cardiac phases and create final sampling order
    for cardiac_phase in range(n_cardiac_phases):
        for p, s, _ in points_to_sample:
            sampling_order.append((p, s, cardiac_phase))
    
    # In a real implementation, this would be dynamically reordered based on respiratory position
    # Here we just return the basic ordering
    return sampling_order