"""Default configuration parameters for 4D flow MRI."""

class DefaultConfig:
    """Default configuration parameters for 4D flow MRI."""
    
    # Spatial parameters
    FOV = [280e-3, 280e-3, 140e-3]  # Field of view [x, y, z] in meters
    MATRIX_SIZE = [192, 128, 32]  # Matrix size [x, y, z]
    
    # Timing parameters
    TR = 5.0e-3  # Repetition time [s]
    TE = 2.5e-3  # Echo time [s]
    RF_DURATION = 1.0e-3  # RF pulse duration [s]
    READOUT_DURATION = 2.0e-3  # Readout duration [s]
    
    # Flow encoding parameters
    VENC = 150e-2  # Velocity encoding value [m/s] (150 cm/s)
    FLOW_DIRECTIONS = [True, True, True]  # Encode in [x, y, z] directions
    ENCODING_SCHEME = 'simple'  # 'simple' or 'hadamard'
    
    # RF parameters
    FLIP_ANGLE = 8  # Flip angle [degrees]
    
    # Acceleration parameters
    ACCELERATION_FACTOR = 6  # Acceleration factor for compressed sensing
    CENTER_FRACTION = 0.04  # Fraction of k-space center to fully sample
    SAMPLING_PATTERN = 'phyllotaxis'  # 'phyllotaxis' or 'poisson'
    
    # Cardiac parameters
    N_CARDIAC_PHASES = 20  # Number of cardiac phases
    
    # ReCAR parameters
    RECAR_ENABLED = True  # Enable ReCAR
    NAVIGATOR_ENABLED = True  # Enable navigator echo for respiratory gating
    
    # Sequence name
    NAME = '4D_flow_CS_ReCAR'