"""
A Simple Signal Quantizer for GNURadio, written as an embedded Python Block.
Freeware
Steve Hageman, 30Aug24
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block - Quantizer"""

    def __init__(self, bits=255, vref=1.0, clipping=False):  # only default arguments here
        """ bits (int)      = The number of bits to quantize input signal to
            vref (float)    = The reference voltage, the range is from: (-vref) to (+vref - 1 LSB)
            clipping (bool) = Flag to specify if the output signal is to be clipped to the
                              range: (-vref) to (+vref - 1 LSB) as would be in a real ADC or DAC.
                              Default is no clipping.
        """
        gr.sync_block.__init__(
            self,
            name='Quantizer',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )

        # Save class variables
        self.bits = bits
        self.vref = vref
        self.clipping = clipping

    def work(self, input_items, output_items):

        # These assignments could be out in the __init__(), but then they would not be runtime adjustable.
        levels = (2**self.bits)/2
        vmax = self.vref - (self.vref / levels)
        vmin = -self.vref

        if not self.clipping:
            # If not clipping, then the clip range is +/- Infinity
            vmax = np.finfo(np.float32).max
            vmin = np.finfo(np.float32).min

        # The np.floor() function quantizes the signal, the np.clip() function clips the signal to the range specified.
        output_items[0][:] = np.clip((np.floor(input_items[0]/self.vref*levels) / levels) * self.vref, a_max=vmax, a_min=vmin)

        return len(output_items[0])
