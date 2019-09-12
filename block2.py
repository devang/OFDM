"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from multiprocessing import Pool, TimeoutError


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, frame_length=80):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Find Correlation',   # will show up in GRC
            in_sig=[(np.float32, frame_length), (np.float32, frame_length)],
            out_sig=[np.float32, np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.frame_length = frame_length

    def work(self, input_items, output_items):

        index_at_corr = np.argmax(input_items[0][0])
        val_at_corr = input_items[1][0][index_at_corr]

        # print 'index:{}:{}'.format(index_at_corr, val_at_corr)

        output_items[0][:] = index_at_corr
        output_items[1][:] = val_at_corr
        return len(output_items[0])
