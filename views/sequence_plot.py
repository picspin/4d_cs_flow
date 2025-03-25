"""Visualization of the 4D flow MRI sequence."""

import matplotlib.pyplot as plt

# def plot_sequence(seq, filename):
#     """
#     Plot the sequence diagram.
    
#     Parameters:
#     -----------
#     seq : Sequence
#         Sequence object
#     filename : str
#         Filename for saving the plot
#     """
#     plt.figure(figsize=(10, 5))
#     plt.title("4D Flow MRI Sequence Diagram")
#     # Here you can add more detailed plotting logic based on the sequence
#     plt.xlabel("Time [s]")
#     plt.ylabel("Events")
#     plt.grid()
#     plt.savefig(filename)
#     plt.close()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def plot_sequence(seq, filename=None, time_range=None, plot_type='full'):
    """
    Plot the sequence diagram.
    
    Parameters:
    -----------
    seq : Sequence
        Sequence object
    filename : str, optional
        Filename for saving the plot
    time_range : tuple, optional
        Time range to plot (start, end) in seconds
    plot_type : str, optional
        Type of plot ('full', 'compact', or 'kspace')
        
    Returns:
    --------
    fig : Figure
        Matplotlib figure object
    """
    # Get sequence timing
    if hasattr(seq, 'block_durations'):
        block_durations = seq.block_durations
    else:
        block_durations = []
        for block in seq.blocks:
            block_durations.append(block.block_duration)
    
    # Calculate cumulative durations
    cum_durations = np.cumsum([0] + block_durations)
    
    # Set time range
    if time_range is None:
        t_start = 0
        t_end = cum_durations[-1]
    else:
        t_start, t_end = time_range
    
    # Create figure
    fig, axes = plt.subplots(5, 1, figsize=(12, 8), sharex=True)
    plt.subplots_adjust(hspace=0.1)
    
    # Plot RF, Gx, Gy, Gz, ADC
    labels = ['RF', 'Gx', 'Gy', 'Gz', 'ADC']
    
    for i, ax in enumerate(axes):
        ax.set_ylabel(labels[i])
        ax.grid(True)
        
        if i < 4:  # RF and gradients
            ax.set_ylim(-1.1, 1.1)
        else:  # ADC
            ax.set_ylim(-0.1, 1.1)
            
    # Set x-axis limits
    axes[-1].set_xlim(t_start, t_end)
    axes[-1].set_xlabel('Time (s)')
    
    # Add title
    plt.suptitle('4D Flow MRI Sequence Diagram')
    
    # Save or show the plot
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.tight_layout()
        plt.show()
        
    return fig

def plot_gradient_waveforms(gx, gy, gz, filename=None):
    """
    Plot gradient waveforms.
    
    Parameters:
    -----------
    gx, gy, gz : ndarray
        Gradient waveforms
    filename : str, optional
        Filename for saving the plot
        
    Returns:
    --------
    fig : Figure
        Matplotlib figure object
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
    
    # Time axis
    t = np.arange(len(gx)) * 1e-6  # Assuming 1us sampling
    
    # Plot gradients
    axes[0].plot(t, gx)
    axes[0].set_ylabel('Gx (Hz/m)')
    axes[0].grid(True)
    
    axes[1].plot(t, gy)
    axes[1].set_ylabel('Gy (Hz/m)')
    axes[1].grid(True)
    
    axes[2].plot(t, gz)
    axes[2].set_ylabel('Gz (Hz/m)')
    axes[2].grid(True)
    
    # Set x-axis
    axes[2].set_xlabel('Time (s)')
    
    # Add title
    plt.suptitle('Gradient Waveforms')
    
    # Save or show the plot
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.tight_layout()
        plt.show()
        
    return fig