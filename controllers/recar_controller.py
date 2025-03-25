import numpy as np

class RecarController:
    """
    Controller for Respiratory Controlled Adaptive k-space Reordering (ReCAR)
    """
    def __init__(self, sampling_mask, n_cardiac_phases):
        """
        Initialize ReCAR controller
        
        Parameters:
        -----------
        sampling_mask : ndarray
            2D sampling mask (n_phase x n_slice)
        n_cardiac_phases : int
            Number of cardiac phases
        """
        self.sampling_mask = sampling_mask
        self.n_cardiac_phases = n_cardiac_phases
        self.n_phase, self.n_slice = sampling_mask.shape
        self.sampling_order = self._generate_sampling_order()
        
    def _generate_sampling_order(self):
        """
        Generate k-space sampling order using ReCAR strategy
        
        Returns:
        --------
        sampling_order : list
            List of (phase_idx, slice_idx, cardiac_phase) tuples in acquisition order
        """
        # Get all points to sample
        points_to_sample = []
        for p in range(self.n_phase):
            for s in range(self.n_slice):
                if self.sampling_mask[p, s] == 1:
                    # Calculate k-space radius (distance from center)
                    kp = p - self.n_phase/2
                    ks = s - self.n_slice/2
                    k_radius = np.sqrt(kp**2 + ks**2)
                    
                    # Store point with its radius
                    points_to_sample.append((p, s, k_radius))
        
        # Sort points by radius (center-out ordering)
        points_to_sample.sort(key=lambda x: x[2])
        
        # Assign cardiac phases and create final sampling order
        sampling_order = []
        for cardiac_phase in range(self.n_cardiac_phases):
            for p, s, _ in points_to_sample:
                sampling_order.append((p, s, cardiac_phase))
        
        return sampling_order
    
    def get_sampling_order(self):
        """
        Get the sampling order
        
        Returns:
        --------
        sampling_order : list
            List of (phase_idx, slice_idx, cardiac_phase) tuples in acquisition order
        """
        return self.sampling_order
    
    def reorder_based_on_respiratory_position(self, resp_position):
        """
        Reorder k-space sampling based on respiratory position
        
        Parameters:
        -----------
        resp_position : float
            Current respiratory position (0 = end-expiration, 1 = end-inspiration)
            
        Returns:
        --------
        reordered_sampling : list
            Reordered sampling points
        """
        # In a real implementation, this would dynamically reorder based on respiratory position
        # Here we just return the basic ordering
        return self.sampling_order
    
    def add_navigator_echo(self, seq, system):
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
        from pypulseq.make_sinc_pulse import make_sinc_pulse
        from pypulseq.make_trap_pulse import make_trapezoid
        from pypulseq.make_adc import make_adc
        
        # Create a pencil-beam excitation
        rf_nav, gz_nav = make_sinc_pulse(flip_angle=10, duration=1e-3, 
                                       slice_thickness=30e-3, 
                                       apodization=0.5, time_bw_product=4,
                                       system=system, return_gz=True)
        
        # Create readout gradient for navigator
        gz_nav_readout = make_trapezoid(channel='z', system=system, 
                                      area=1/30e-3 * 64, duration=3e-3, 
                                      flat_time=2e-3)
        
        # ADC for navigator
        adc_nav = make_adc(num_samples=64, duration=2e-3, 
                          delay=0.5e-3, system=system)
        
        # Add navigator blocks to sequence
        seq.add_block(rf_nav, gz_nav)
        seq.add_block(gz_nav_readout, adc_nav)
        
        return seq