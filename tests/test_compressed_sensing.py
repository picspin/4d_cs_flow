"""Unit tests for compressed sensing module."""

import unittest
import numpy as np

from models.compressed_sensing import generate_variable_density_mask
from models.compressed_sensing import generate_phyllotaxis_sampling

class TestCompressedSensing(unittest.TestCase):
    """Test compressed sensing functions."""
    
    def setUp(self):
        """Set up test environment."""
        self.n_phase = 128
        self.n_slice = 32
        self.acceleration_factor = 6
        self.center_fraction = 0.04
        
    def test_generate_variable_density_mask(self):
        """Test generation of variable-density sampling mask."""
        mask = generate_variable_density_mask(
            self.n_phase, 
            self.n_slice, 
            self.acceleration_factor, 
            self.center_fraction
        )
        
        # Check mask dimensions
        self.assertEqual(mask.shape, (self.n_phase, self.n_slice))
        
        # Check acceleration factor
        actual_acceleration = self.n_phase * self.n_slice / np.sum(mask)
        self.assertAlmostEqual(actual_acceleration, self.acceleration_factor, delta=0.5)
        
        # Check center is fully sampled
        center_p = int(self.n_phase * self.center_fraction)
        center_s = int(self.n_slice * self.center_fraction)
        p_start = self.n_phase // 2 - center_p // 2
        p_end = p_start + center_p
        s_start = self.n_slice // 2 - center_s // 2
        s_end = s_start + center_s
        
        center_mask = mask[p_start:p_end, s_start:s_end]
        self.assertTrue(np.all(center_mask == 1))
        
    def test_generate_phyllotaxis_sampling(self):
        """Test generation of phyllotaxis sampling pattern."""
        mask = generate_phyllotaxis_sampling(
            self.n_phase, 
            self.n_slice, 
            self.acceleration_factor, 
            self.center_fraction
        )
        
        # Check mask dimensions
        self.assertEqual(mask.shape, (self.n_phase, self.n_slice))
        
        # Check acceleration factor
        actual_acceleration = self.n_phase * self.n_slice / np.sum(mask)
        self.assertAlmostEqual(actual_acceleration, self.acceleration_factor, delta=0.5)

if __name__ == '__main__':
    unittest.main()