# def main():
#     # System limits
#     system = Opts(max_grad=40, grad_unit='mT/m', max_slew=130, slew_unit='T/m/s', 
#                   rf_ringdown_time=30e-6, rf_dead_time=100e-6)
    
#     # Create a new sequence object
#     seq = Sequence(system)
    
#     # Define sequence parameters
#     fov = 280e-3                # Field of view in meters
#     n_readout = 192             # Number of readout points
#     n_phase = 128               # Number of phase encoding steps
#     n_slice = 32                # Number of slices
#     n_cardiac_phases = 20       # Number of cardiac phases
#     slice_thickness = 2.5e-3    # Slice thickness in meters
#     tr = 5.0e-3                 # Repetition time in seconds
#     te = 2.5e-3                 # Echo time in seconds
#     flip_angle = 8              # Flip angle in degrees
#     venc = 150e-2               # Velocity encoding value in m/s (150 cm/s)
#     acceleration_factor = 6     # Acceleration factor for compressed sensing
    
#     # Create the 4D flow sequence
#     seq = create_4d_flow_sequence(seq, system, fov, n_readout, n_phase, n_slice, 
#                                  n_cardiac_phases, slice_thickness, tr, te, 
#                                  flip_angle, venc, acceleration_factor)
    
#     # Check sequence timing
#     ok, error_report = seq.check_timing()
#     if not ok:
#         print("Timing check failed!")
#         print(error_report)
#         return
    
#     # Export the sequence
#     seq.write('4d_flow_cs_recar.seq')
#     print("Sequence successfully exported to 4d_flow_cs_recar.seq")
    
#     # Calculate sequence duration
#     duration = seq.duration()[0]
#     print(f"Sequence duration: {duration:.2f} s ({duration/60:.2f} min)")

# if __name__ == "__main__":
#     main() 

# import os
# import numpy as np
# import matplotlib.pyplot as plt
# from pypulseq.Sequence.sequence import Sequence
# from pypulseq.opts import Opts

# from models.sequence_params import SequenceParams
# from controllers.sequence_builder import SequenceBuilder
# from views.sequence_plot import plot_sequence
# from views.k_space_viewer import plot_sampling_pattern

# def main():
#     """
#     Main function to build and export the 4D flow sequence
#     """
#     # Create output directory if it doesn't exist
#     os.makedirs('output', exist_ok=True)
    
#     # Define system limits
#     system = Opts(max_grad=40, grad_unit='mT/m', 
#                   max_slew=130, slew_unit='T/m/s',
#                   rf_ringdown_time=30e-6, 
#                   rf_dead_time=100e-6)
    
#     # Create sequence parameters
#     params = SequenceParams()
    
#     # Optionally update parameters
#     params.update(
#         fov=[280e-3, 280e-3, 140e-3],
#         matrix_size=[192, 128, 32],
#         venc=150e-2,  # 150 cm/s
#         acceleration_factor=6,
#         n_cardiac_phases=20
#     )
    
#     # Create sequence builder
#     builder = SequenceBuilder(params, system)
    
#     # Build the sequence
#     seq = builder.build_sequence()
    
#     # Check sequence timing
#     ok, error_report = seq.check_timing()
#     if not ok:
#         print("Timing check failed!")
#         print(error_report)
#         return
    
#     # Export the sequence
#     seq.write('output/4d_flow_cs_recar.seq')
#     print("Sequence successfully exported to output/4d_flow_cs_recar.seq")
    
#     # Calculate sequence duration
#     duration = seq.duration()[0]
#     print(f"Sequence duration: {duration:.2f} s ({duration/60:.2f} min)")
    
#     # Plot sequence diagram
#     plot_sequence(seq, 'output/sequence_diagram.png')
    
#     # Plot sampling pattern
#     from models.compressed_sensing import generate_phyllotaxis_sampling
#     mask = generate_phyllotaxis_sampling(
#         params.matrix_size[1], 
#         params.matrix_size[2], 
#         params.acceleration_factor
#     )
#     plot_sampling_pattern(mask, 'output/sampling_pattern.png')

# if __name__ == "__main__":
#     main()

import os
import numpy as np
import matplotlib.pyplot as plt
from pypulseq.Sequence.sequence import Sequence

from config.default_config import DefaultConfig
from config.system_config import SystemConfig
from models.sequence_params import SequenceParams
from controllers.sequence_builder import SequenceBuilder
from controllers.export_controller import export_sequence
from views.sequence_plot import plot_sequence
from views.k_space_viewer import plot_sampling_pattern
from utils.pulseq_utils import check_sequence_timing, calculate_sequence_duration

def main():
    """Main function to build and export the 4D flow sequence."""
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Load default configuration
    default_config = DefaultConfig()
    
    # Create system configuration
    system_config = SystemConfig()
    system = system_config.get_opts()
    
    # Create sequence parameters
    params = SequenceParams()
    
    # Update parameters from default configuration
    params.update(
        fov=default_config.FOV,
        matrix_size=default_config.MATRIX_SIZE,
        venc=default_config.VENC,
        acceleration_factor=default_config.ACCELERATION_FACTOR,
        n_cardiac_phases=default_config.N_CARDIAC_PHASES
    )
    
    # Create sequence builder
    builder = SequenceBuilder(params, system)
    
    # Build the sequence
    seq = builder.build_sequence()
    
    # Check sequence timing
    ok, error_report = check_sequence_timing(seq)
    if not ok:
        print("Timing check failed!")
        print(error_report)
        return
    
    # Export the sequence
    export_sequence(seq, 'output/4d_flow_cs_recar.seq')
    
    # Calculate sequence duration
    duration = calculate_sequence_duration(seq)
    print(f"Sequence duration: {duration:.2f} s ({duration/60:.2f} min)")
    
    # Plot sequence diagram
    plot_sequence(seq, 'output/sequence_diagram.png')
    
    # Plot sampling pattern
    from models.compressed_sensing import generate_phyllotaxis_sampling
    mask = generate_phyllotaxis_sampling(
        params.matrix_size[1], 
        params.matrix_size[2], 
        params.acceleration_factor
    )
    plot_sampling_pattern(mask, 'output/sampling_pattern.png')

if __name__ == "__main__":
    main()