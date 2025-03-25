class SequenceParams:
    """
    Class to store and manage 4D flow sequence parameters
    """
    def __init__(self):
        # Spatial parameters
        self.fov = [280e-3, 280e-3, 140e-3]  # Field of view in meters [x, y, z]
        self.matrix_size = [192, 128, 32]     # Matrix size [x, y, z]
        self.resolution = [self.fov[i]/self.matrix_size[i] for i in range(3)]  # Resolution in meters
        
        # Timing parameters
        self.tr = 5.0e-3        # Repetition time in seconds
        self.te = 2.5e-3        # Echo time in seconds
        self.t_rf = 1.0e-3      # RF pulse duration in seconds
        self.t_readout = 2.0e-3 # Readout duration in seconds
        
        # Flow encoding parameters
        self.venc = 150e-2      # Velocity encoding value in m/s (150 cm/s)
        self.flow_directions = [True, True, True]  # Encode in [x, y, z] directions
        
        # RF parameters
        self.flip_angle = 8     # Flip angle in degrees
        
        # Acceleration parameters
        self.acceleration_factor = 6  # Acceleration factor for compressed sensing
        self.center_fraction = 0.04   # Fraction of k-space center to fully sample
        
        # Cardiac parameters
        self.n_cardiac_phases = 20    # Number of cardiac phases
        
        # ReCAR parameters
        self.recar_enabled = True     # Enable ReCAR
        self.navigator_enabled = True  # Enable navigator echo for respiratory gating
        
    def update(self, **kwargs):
        """Update parameters with provided values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"SequenceParams has no attribute '{key}'")