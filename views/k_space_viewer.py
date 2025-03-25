"""Visualization of k-space sampling patterns."""

# import matplotlib.pyplot as plt

# def plot_sampling_pattern(mask, filename):
#     """
#     Plot the k-space sampling pattern.
    
#     Parameters:
#     -----------
#     mask : ndarray
#         K-space sampling mask
#     filename : str
#         Filename for saving the plot
#     """
#     plt.imshow(mask, cmap='gray')
#     plt.title("K-Space Sampling Pattern")
#     plt.xlabel("Slice Index")
#     plt.ylabel("Phase Index")
#     plt.colorbar(label='Sampling (1 = Sampled, 0 = Not Sampled)')
#     plt.savefig(filename)
#     plt.close()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_sampling_pattern(mask, filename=None):
    """
    Plot the k-space sampling pattern.
    
    Parameters:
    -----------
    mask : ndarray
        K-space sampling mask
    filename : str, optional
        Filename for saving the plot
        
    Returns:
    --------
    fig : Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    im = ax.imshow(mask, cmap='viridis', origin='lower')
    plt.colorbar(im, ax=ax, label='Sampling (1 = Sampled, 0 = Not Sampled)')
    
    ax.set_title('K-Space Sampling Pattern')
    ax.set_xlabel('Slice Encoding')
    ax.set_ylabel('Phase Encoding')
    
    # Save or show the plot
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.tight_layout()
        plt.show()
        
    return fig

def plot_3d_sampling_pattern(mask, n_cardiac_phases=1, filename=None):
    """
    Plot the 3D k-space sampling pattern.
    
    Parameters:
    -----------
    mask : ndarray
        K-space sampling mask (2D)
    n_cardiac_phases : int, optional
        Number of cardiac phases
    filename : str, optional
        Filename for saving the plot
        
    Returns:
    --------
    fig : Figure
        Matplotlib figure object
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Get coordinates of sampled points
    y_indices, x_indices = np.where(mask == 1)
    
    # Center coordinates
    y_indices = y_indices - mask.shape[0] / 2
    x_indices = x_indices - mask.shape[1] / 2
    
    # Create points for all cardiac phases
    all_points = []
    for t in range(n_cardiac_phases):
        for y, x in zip(y_indices, x_indices):
            all_points.append((x, y, t))
    
    # Convert to numpy array
    all_points = np.array(all_points)
    
    # Plot points
    ax.scatter(all_points[:, 0], all_points[:, 1], all_points[:, 2], 
               c=all_points[:, 2], cmap='viridis', marker='o', s=10)
    
    ax.set_title('3D K-Space Sampling Pattern (with Cardiac Phases)')
    ax.set_xlabel('Slice Encoding')
    ax.set_ylabel('Phase Encoding')
    ax.set_zlabel('Cardiac Phase')
    
    # Save or show the plot
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.tight_layout()
        plt.show()
        
    return fig
