"""Unit tests for velocity encoding module."""

import unittest
import numpy as np
from pypulseq.opts import Opts

from models.velocity_encoding import calculate_venc_moment, make_bipolar_gradient
from models.velocity_encoding import create_flow_encoding_gradients, create_hadamard_encoding

class TestVelocityEncoding(unittest.TestCase):
    """Test velocity encoding functions."""
    
    def setUp(self):
        """Set up test environment."""
        self.system = Opts(max_grad=40, grad_unit='mT/m', 
                          max_slew=130, slew_unit='T/m/s',
                          rf_ringdown_time=30e-6, 
                          rf_dead_time=100e-6)
        self.venc = 150e-2  # 150 cm/s
        
    def test_calculate_venc_moment(self):
        """Test calculation of first moment for velocity encoding."""
        m1 = calculate_venc_moment(self.venc)
        self.assertGreater(m1, 0)
        
    def test_make_bipolar_gradient(self):
        """Test creation of bipolar gradient."""
        bipolar_pos, bipolar_neg = make_bipolar_gradient('x', self.venc, self.system)
        
        # Check that gradients have opposite areas
        self.assertAlmostEqual(bipolar_pos.area, -bipolar_neg.area)
        
    def test_create_flow_encoding_gradients(self):
        """Test creation of flow encoding gradients."""
        flow_directions = [True, True, True]
        encoding_schemes = create_flow_encoding_gradients(self.venc, self.system, flow_directions)
        
        # Should have 4 encoding schemes (reference + 3 directions)
        self.assertEqual(len(encoding_schemes), 4)
        
        # Reference scheme should have no gradients
        self.assertEqual(len(encoding_schemes[0]['gradients']), 0)
        
    def test_create_hadamard_encoding(self):
        """Test creation of Hadamard encoding."""
        flow_directions = [True, True, True]
        encoding_schemes = create_hadamard_encoding(self.venc, self.system, flow_directions)
        
        # Should have 4 encoding schemes
        self.assertEqual(len(encoding_schemes), 4)

if __name__ == '__main__':
    unittest.main()