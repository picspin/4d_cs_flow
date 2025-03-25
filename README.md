# 4D Flow MRI Sequence Implementation

This project implements a 4D phase-contrast MRI sequence for velocity encoding using the pypulseq framework. The sequence incorporates Compressed Sensing for acceleration and Respiratory Controlled Adaptive k-space Reordering (ReCAR) for motion artifact reduction.

## Overview

4D flow MRI (time-resolved 3D phase-contrast MRI) is a powerful technique for measuring and visualizing blood flow dynamics in three dimensions over time. This implementation provides a flexible framework for designing and optimizing 4D flow sequences with advanced features:

- **Velocity Encoding**: Bipolar gradients for encoding velocity in three spatial dimensions
- **Compressed Sensing**: Variable-density sampling patterns for accelerated acquisition
- **ReCAR**: Respiratory Controlled Adaptive k-space Reordering for motion artifact reduction
- **Visualization**: Tools for visualizing the sequence and k-space sampling patterns

## Installation

<!-- 1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/4d-flow-mri.git
   cd 4d-flow-mri  -->

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate 
``` 
```
4d_flow_mri/
│
├── models/                  # Core sequence components and physics models
│   ├── __init__.py
│   ├── sequence_params.py   # Sequence parameters definition
│   ├── gradient_lib.py      # Gradient waveform generation
│   ├── rf_lib.py            # RF pulse generation
│   ├── velocity_encoding.py # Velocity encoding strategies
│   └── compressed_sensing.py # CS sampling patterns
│
├── controllers/             # Sequence control logic
│   ├── __init__.py
│   ├── sequence_builder.py  # Main sequence assembly
│   ├── recar_controller.py  # ReCAR implementation
│   ├── cs_controller.py     # Compressed sensing controller
│   └── export_controller.py # Sequence export functionality
│
├── views/                   # Visualization and UI components
│   ├── __init__.py
│   ├── sequence_plot.py     # Sequence visualization
│   └── k_space_viewer.py    # k-space sampling pattern visualization
│
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── pulseq_utils.py      # Helpers for pypulseq
│   └── math_utils.py        # Mathematical helper functions
│
├── config/                  # Configuration files
│   ├── __init__.py
│   ├── default_config.py    # Default sequence parameters
│   └── system_config.py     # MRI system specifications
│
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_velocity_encoding.py
│   └── test_compressed_sensing.py
│
├── examples/                # Example implementations
│   ├── basic_4d_flow.py     # Basic 4D flow sequence
│   ├── cs_4d_flow.py        # 4D flow with compressed sensing
│   └── full_4d_flow.py      # Complete implementation with CS and ReCAR
│
├── main.py                  # Main entry point
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation 
``` 
This will create a 4D flow sequence with default parameters and export it to output/4d_flow_cs_recar.seq.

Custom Parameters
You can customize the sequence parameters by modifying the config/default_config.py file or by passing parameters to the SequenceParams class: 

```
from models.sequence_params import SequenceParams

params = SequenceParams()
params.update(
    fov=[280e-3, 280e-3, 140e-3],
    matrix_size=[192, 128, 32],
    venc=150e-2,  # 150 cm/s
    acceleration_factor=6,
    n_cardiac_phases=20
)  
``` 
## Examples  

The examples/ directory contains several example implementations:

- basic_4d_flow.py: A basic 4D flow sequence without acceleration
- cs_4d_flow.py: A 4D flow sequence with Compressed Sensing
- full_4d_flow.py: A complete 4D flow sequence with CS and ReCAR
## Key Features  
### Velocity Encoding  
The sequence uses bipolar gradients for velocity encoding in three spatial dimensions. The velocity encoding value (VENC) can be customized to match the expected flow velocities. 
```
from models.velocity_encoding import create_flow_encoding_gradients

flow_encodings = create_flow_encoding_gradients(
    venc=150e-2,  # 150 cm/s
    system=system,
    flow_directions=[True, True, True]  # Encode in x, y, z directions
)
```  

## Compressed Sensing  

The sequence uses variable-density sampling patterns for accelerated acquisition. Two sampling patterns are implemented:

Variable-density Poisson disk sampling
Phyllotaxis sampling (golden angle-based) 

## ReCAR (Respiratory Controlled Adaptive k-space Reordering)
ReCAR adaptively reorders k-space acquisition based on respiratory position to reduce motion artifacts. The implementation includes a navigator echo for respiratory motion tracking.  
## Visualization
The project includes tools for visualizing the sequence and k-space sampling patterns: 
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
The pypulseq team for providing the framework for MRI sequence development
The authors of the referenced papers for their contributions to 4D flow MRI techniques