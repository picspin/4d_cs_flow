import numpy as np
from pypulseq.Sequence.sequence import Sequence
from pypulseq.calc_duration import calc_duration
from pypulseq.make_adc import make_adc
from pypulseq.make_delay import make_delay
from pypulseq.make_sinc_pulse import make_sinc_pulse
from pypulseq.make_trap_pulse import make_trap_pulse
from pypulseq.make_block_pulse import make_block_pulse
from pypulseq.opts import Opts

# System limits
system = Opts(max_grad=40, grad_unit='mT/m', max_slew=130, slew_unit='T/m/s', 
              rf_ringdown_time=30e-6, rf_dead_time=100e-6)

# Create a new sequence object
seq = Sequence(system)

# Define sequence parameters
fov = 280e-3                # Field of view in meters
n_readout = 192             # Number of readout points
n_phase = 128               # Number of phase encoding steps
n_slice = 32                # Number of slices
n_cardiac_phases = 20       # Number of cardiac phases
slice_thickness = 2.5e-3    # Slice thickness in meters
tr = 5.0e-3                 # Repetition time in seconds
te = 2.5e-3                 # Echo time in seconds
flip_angle = 8              # Flip angle in degrees
venc = 150e-2               # Velocity encoding value in m/s (150 cm/s)