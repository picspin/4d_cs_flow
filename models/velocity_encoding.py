import numpy as np
from pypulseq.make_trap_pulse import make_trapezoid
from pypulseq.opts import Opts

def calculate_venc_moment(venc, system):
    """
    Calculate the first moment for the desired venc
    
    Parameters:
    -----------
    venc : float
        Velocity encoding value in m/s
    system : Opts
        System limits
        
    Returns:
    --------
    m1 : float
        First moment required for the desired venc
    """
    gamma = 42.58e6  # Hz/T
    m1 = np.pi / (gamma * venc)
    return m1

def make_bipolar_gradient(channel, venc, system, duration=1e-3):
    """
    Create a bipolar gradient for velocity encoding
    
    Parameters:
    -----------
    channel : str
        Gradient channel ('x', 'y', or 'z')
    venc : float
        Velocity encoding value in m/s
    system : Opts
        System limits
    duration : float
        Duration of the entire bipolar pulse in seconds
        
    Returns:
    --------
    bipolar_pos, bipolar_neg : tuple
        Positive and negative bipolar gradient objects
    """
    # Calculate the first moment for the desired venc
    m1 = calculate_venc_moment(venc, system)
    
    # Calculate area of each lobe
    area = m1 / 2
    
    # Calculate amplitude based on duration
    amplitude = area / (duration / 2)
    
    # Check if amplitude exceeds system limits
    if amplitude > system.max_grad:
        # Adjust duration if amplitude exceeds system limits
        duration = 2 * area / system.max_grad
        amplitude = system.max_grad
    
    # Create the bipolar gradients
    bipolar_pos = make_trapezoid(channel=channel, system=system, 
                              area=area, duration=duration/2)
    bipolar_neg = make_trapezoid(channel=channel, system=system, 
                              area=-area, duration=duration/2)
    
    return bipolar_pos, bipolar_neg

def create_flow_encoding_gradients(venc, system, flow_directions):
    """
    Create flow encoding gradients for all specified directions
    
    Parameters:
    -----------
    venc : float
        Velocity encoding value in m/s
    system : Opts
        System limits
    flow_directions : list
        List of booleans indicating which directions to encode [x, y, z]
        
    Returns:
    --------
    encoding_schemes : list
        List of dictionaries containing gradient combinations for each encoding
    """
    # Create bipolar gradients for each direction if needed
    gradients = {}
    if flow_directions[0]:  # X direction
        gradients['x'] = make_bipolar_gradient('x', venc, system)
    if flow_directions[1]:  # Y direction
        gradients['y'] = make_bipolar_gradient('y', venc, system)
    if flow_directions[2]:  # Z direction
        gradients['z'] = make_bipolar_gradient('z', venc, system)
    
    # Create 4-point encoding scheme (reference + 3 directions)
    encoding_schemes = [
        {'name': 'reference', 'gradients': {}},  # Reference (no encoding)
    ]
    
    # Add encoding for each direction
    for direction, bipolar in gradients.items():
        scheme = {'name': f'{direction}_encoding', 'gradients': {}}
        scheme['gradients'][direction] = bipolar
        encoding_schemes.append(scheme)
    
    return encoding_schemes

def create_hadamard_encoding(venc, system, flow_directions):
    """
    Create Hadamard-encoded velocity encoding gradients for improved SNR
    
    Parameters:
    -----------
    venc : float
        Velocity encoding value in m/s
    system : Opts
        System limits
    flow_directions : list
        List of booleans indicating which directions to encode [x, y, z]
        
    Returns:
    --------
    encoding_schemes : list
        List of dictionaries containing gradient combinations for Hadamard encoding
    """
    # Create bipolar gradients for each direction if needed
    gradients = {}
    if flow_directions[0]:  # X direction
        gradients['x'] = make_bipolar_gradient('x', venc, system)
    if flow_directions[1]:  # Y direction
        gradients['y'] = make_bipolar_gradient('y', venc, system)
    if flow_directions[2]:  # Z direction
        gradients['z'] = make_bipolar_gradient('z', venc, system)
    
    # Create Hadamard encoding schemes
    # [1  1  1  1]
    # [1  1 -1 -1]
    # [1 -1  1 -1]
    # [1 -1 -1  1]
    
    encoding_schemes = [
        {'name': 'hadamard_1', 'gradients': {}},  # Reference (no encoding)
    ]
    
    # Add Hadamard encoding schemes
    if all(flow_directions):  # Only if all 3 directions are enabled
        # Scheme 2: [1, 1, -1]
        scheme2 = {'name': 'hadamard_2', 'gradients': {}}
        scheme2['gradients']['x'] = gradients['x'][0]  # Positive x
        scheme2['gradients']['y'] = gradients['y'][0]  # Positive y
        scheme2['gradients']['z'] = gradients['z'][1]  # Negative z
        encoding_schemes.append(scheme2)
        
        # Scheme 3: [1, -1, 1]
        scheme3 = {'name': 'hadamard_3', 'gradients': {}}
        scheme3['gradients']['x'] = gradients['x'][0]  # Positive x
        scheme3['gradients']['y'] = gradients['y'][1]  # Negative y
        scheme3['gradients']['z'] = gradients['z'][0]  # Positive z
        encoding_schemes.append(scheme3)
        
        # Scheme 4: [1, -1, -1]
        scheme4 = {'name': 'hadamard_4', 'gradients': {}}
        scheme4['gradients']['x'] = gradients['x'][0]  # Positive x
        scheme4['gradients']['y'] = gradients['y'][1]  # Negative y
        scheme4['gradients']['z'] = gradients['z'][1]  # Negative z
        encoding_schemes.append(scheme4)
    
    return encoding_schemes