"""MRI system configuration parameters."""

class SystemConfig:
    """Class to store MRI system configuration."""
    
    def __init__(self):
        # System limits
        self.max_grad = 40  # Maximum gradient amplitude [mT/m]
        self.max_slew = 130  # Maximum slew rate [T/m/s]
        self.grad_unit = 'mT/m'  # Gradient amplitude unit
        self.slew_unit = 'T/m/s'  # Slew rate unit
        
        # RF system parameters
        self.rf_dead_time = 100e-6  # RF dead time [s]
        self.rf_ringdown_time = 30e-6  # RF ringdown time [s]
        
        # System frequencies
        self.larmor_freq = 123.2  # Larmor frequency [MHz] for 3T
        
        # Raster times
        self.rf_raster_time = 1e-6  # RF raster time [s]
        self.grad_raster_time = 10e-6  # Gradient raster time [s]
        self.adc_raster_time = 100e-9  # ADC raster time [s]
        self.block_duration_raster = 10e-6  # Block duration raster [s]
        
    def get_opts(self):
        """Return system parameters as pypulseq Opts object."""
        from pypulseq.opts import Opts
        
        return Opts(
            max_grad=self.max_grad,
            grad_unit=self.grad_unit,
            max_slew=self.max_slew,
            slew_unit=self.slew_unit,
            rf_ringdown_time=self.rf_ringdown_time,
            rf_dead_time=self.rf_dead_time
        )