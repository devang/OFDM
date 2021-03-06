"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import pmt
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, sample_rate=1000000, fft_len = 256):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Freq Correction',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.message_port_register_out(pmt.to_pmt("out"))
        self.sample_rate = sample_rate
        self.fft_len = fft_len
        self.fcorr = sample_rate/fft_len

    def work(self, input_items, output_items):

        val = np.abs(self.fcorr*input_items[0][0])
        self.message_port_pub(pmt.to_pmt("out"), pmt.cons(pmt.intern("freq"), pmt.to_pmt(val)))

        output_items[0][:] = 0
        return len(output_items[0])

