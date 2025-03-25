import numpy as np
from pypulseq.Sequence.sequence import Sequence
from pypulseq.calc_duration import calc_duration
from pypulseq.make_adc import make_adc
from pypulseq.make_delay import make_delay
from pypulseq.make_sinc_pulse import make_sinc_pulse
from pypulseq.make_trap_pulse import make_trapezoid
from pypulseq.opts import Opts

class SequenceBuilder:
    """
    Main controller for building the 4D flow MRI sequence
    """
    def __init__(self, params, system):
        """
        Initialize sequence builder
        
        Parameters:
        -----------
        params : SequenceParams
            Sequence parameters
        system : Opts
            System limits
        """
        self.params = params
        self.system = system
        self.seq = Sequence(system)
        
        # Import required modules
        from models.velocity_encoding import create_flow_encoding_gradients
        from models.compressed_sensing import generate_phyllotaxis_sampling
        from controllers.recar_controller import RecarController
        
        # Create flow encoding gradients
        self.flow_encodings = create_flow_encoding_gradients(
            self.params.venc, 
            self.system, 
            self.params.flow_directions
        )
        
        # Create sampling mask for compressed sensing
        self.sampling_mask = generate_phyllotaxis_sampling(
            self.params.matrix_size[1],  # phase
            self.params.matrix_size[2],  # slice
            self.params.acceleration_factor,
            self.params.center_fraction
        )
        
        # Create ReCAR controller
        self.recar = RecarController(
            self.sampling_mask,
            self.params.n_cardiac_phases
        )
        
    def make_gre_module(self, phase_index, slice_index, flow_encoding):
        """
        Create a gradient echo module with flow encoding
        
        Parameters:
        -----------
        phase_index : int
            Phase encoding index
        slice_index : int
            Slice encoding index
        flow_encoding : dict
            Flow encoding gradients
            
        Returns:
        --------
        None
        """
        # Calculate derived parameters
        delta_k_phase = 1 / self.params.fov[1]
        delta_k_slice = 1 / self.params.fov[2]
        
        # Create RF pulse (sinc with 3 lobes)
        rf, gz = make_sinc_pulse(flip_angle=self.params.flip_angle, 
                               duration=self.params.t_rf,
                               slice_thickness=self.params.resolution[2],
                               apodization=0.5, 
                               time_bw_product=4,
                               system=self.system, 
                               return_gz=True)
        
        # Create slice refocusing gradient
        gz_reph = make_trapezoid(channel='z', 
                               system=self.system,
                               area=-gz.area/2, 
                               duration=0.5e-3)
        
        # Phase encoding gradient
        phase_area = (phase_index - self.params.matrix_size[1]/2) * delta_k_phase
        gy_phase = make_trapezoid(channel='y', 
                                system=self.system,
                                area=phase_area, 
                                duration=0.5e-3)
        
        # Slice encoding gradient (for 3D)
        slice_area = (slice_index - self.params.matrix_size[2]/2) * delta_k_slice
        gz_phase = make_trapezoid(channel='z', 
                                system=self.system,
                                area=slice_area, 
                                duration=0.5e-3)
        
        # Readout gradient
        gx_pre = make_trapezoid(channel='x', 
                              system=self.system,
                              area=-self.params.matrix_size[0]/2 * delta_k_phase, 
                              duration=0.5e-3)
        
        gx_readout = make_trapezoid(channel='x', 
                                  system=self.system,
                                  area=self.params.matrix_size[0] * delta_k_phase, 
                                  duration=self.params.t_readout + 0.6e-3,
                                  flat_time=self.params.t_readout)
        
        # ADC
        adc = make_adc(num_samples=self.params.matrix_size[0], 
                      duration=self.params.t_readout,
                      delay=0.3e-3, 
                      system=self.system)
        
        # Add blocks to sequence
        self.seq.add_block(rf, gz)
        self.seq.add_block(gz_reph)
        
        # Add flow encoding if needed
        if flow_encoding['name'] != 'reference':
            for direction, bipolar_pair in flow_encoding['gradients'].items():
                bipolar_pos, bipolar_neg = bipolar_pair
                self.seq.add_block(bipolar_pos)
                self.seq.add_block(bipolar_neg)
        
        # Continue with phase encoding and readout
        self.seq.add_block(gy_phase, gz_phase, gx_pre)
        
        # Calculate timing for TE
        delay_te = self.params.te - calc_duration(rf) - calc_duration(gz_reph) - calc_duration(gx_pre) - calc_duration(gx_readout)/2
        if delay_te > 0:
            self.seq.add_block(make_delay(delay_te))
        
        self.seq.add_block(gx_readout, adc)
        
        # Calculate timing for TR
        delay_tr = self.params.tr - calc_duration(rf) - calc_duration(gz_reph) - calc_duration(gx_pre) - calc_duration(gx_readout) - delay_te
        if delay_tr > 0:
            self.seq.add_block(make_delay(delay_tr))
    
    def build_sequence(self):
        """
        Build the complete 4D flow sequence
        
        Returns:
        --------
        seq : Sequence
            Completed sequence object
        """
        # Get sampling order from ReCAR
        sampling_order = self.recar.get_sampling_order()
        
        # Add navigator echo if enabled
        if self.params.navigator_enabled:
            self.recar.add_navigator_echo(self.seq, self.system)
        
        # Add sequence blocks for each point in the sampling order
        for p_idx, s_idx, c_phase in sampling_order:
            # For each k-space point, we need multiple acquisitions (reference + flow encodings)
            for flow_encoding in self.flow_encodings:
                self.make_gre_module(p_idx, s_idx, flow_encoding)
        
        # Set sequence parameters
        self.seq.set_definition('FOV', self.params.fov)
        self.seq.set_definition('Name', '4D_flow_CS_ReCAR')
        self.seq.set_definition('VoxelSize', self.params.resolution)
        self.seq.set_definition('VENC', self.params.venc)
        
        return self.seq