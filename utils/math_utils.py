"""Mathematical utility functions."""

# import numpy as np

# def calculate_first_moment(venc):
#     """
#     Calculate the first moment for velocity encoding.
    
#     Parameters:
#     -----------
#     venc : float
#         Velocity encoding value in m/s
        
#     Returns:
#     --------
#     m1 : float
#         First moment required for the desired venc
#     """
#     gamma = 42.58e6  # Hz/T
#     m1 = np.pi / (gamma * venc)
#     return m1 

import numpy as np

def calculate_first_moment(venc):
    """
    Calculate the first moment for velocity encoding.
    
    Parameters:
    -----------
    venc : float
        Velocity encoding value in m/s
        
    Returns:
    --------
    m1 : float
        First moment required for the desired venc
    """
    gamma = 42.58e6  # Hz/T
    m1 = np.pi / (gamma * venc)
    return m1

def calculate_resolution(fov, matrix_size):
    """
    Calculate the resolution based on FOV and matrix size.
    
    Parameters:
    -----------
    fov : list
        Field of view in meters [x, y, z]
    matrix_size : list
        Matrix size [x, y, z]
        
    Returns:
    --------
    resolution : list
        Resolution in meters [x, y, z]
    """
    return [fov[i] / matrix_size[i] for i in range(len(fov))]

def calculate_k_space_coordinates(matrix_size):
    """
    Calculate k-space coordinates.
    
    Parameters:
    -----------
    matrix_size : list
        Matrix size [x, y, z]
        
    Returns:
    --------
    kx, ky, kz : ndarray
        k-space coordinates
    """
    kx = np.linspace(-matrix_size[0]/2, matrix_size[0]/2-1, matrix_size[0])
    ky = np.linspace(-matrix_size[1]/2, matrix_size[1]/2-1, matrix_size[1])
    kz = np.linspace(-matrix_size[2]/2, matrix_size[2]/2-1, matrix_size[2])
    
    return kx, ky, kz

def generate_golden_angle_sequence(n):
    """
    Generate a sequence of angles based on the golden angle.
    
    Parameters:
    -----------
    n : int
        Number of angles to generate
        
    Returns:
    --------
    angles : ndarray
        Array of angles in radians
    """
    golden_angle = np.pi * (3 - np.sqrt(5))
    angles = np.array([(i * golden_angle) % (2 * np.pi) for i in range(n)])
    
    return angles