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
        """ bits (int)      = The number of bits to quantize to
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

        # Calculate variables needed
        self.vref = vref
        self.levels = (2**bits)/2
        self.vmax = vref - (vref / self.levels)
        self.vmin = -vref

        if not clipping:
            # If not clipping, then the clip range is +/- Infinity
            self.vmax = np.finfo(np.float32).max
            self.vmin = np.finfo(np.float32).min

    def work(self, input_items, output_items):

        # The np.floor() function quantized the signal, the np.clip function clips the signal to the range specified.
        output_items[0][:] = np.clip((np.floor(input_items[0]/self.vref*self.levels) / self.levels) * self.vref, a_max=self.vmax, a_min=self.vmin)

        return len(output_items[0])
