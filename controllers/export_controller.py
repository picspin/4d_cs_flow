"""Export functionality for the 4D flow MRI sequence."""

from pypulseq.Sequence.sequence import Sequence

def export_sequence(seq, filename):
    """
    Export the sequence to a Pulseq file.
    
    Parameters:
    -----------
    seq : Sequence
        Sequence object
    filename : str
        Filename for the output sequence file
    """
    seq.write(filename)
    print(f"Sequence successfully exported to {filename}")