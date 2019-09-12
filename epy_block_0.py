"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, sample_rate = 24000000, M=64, N=80, tcorr = 32):  # only default arguments here
        self.fixed_index = None
        self.last_index2 = 0
        self.last_index = None
        self.done = False
        self.symbol_part = None

        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Keep M in N',   # will show up in GRC
            in_sig=[(np.complex64,N),np.float32],
            out_sig=[(np.complex64,M),np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.M = M
        self.N = N
        self.sample_rate = sample_rate
        self.tcorr = tcorr
        self.half_cp = M / 8

    def work(self, input_items, output_items):
        half_cp = self.half_cp
        N = self.N
        input_vector = input_items[0][0]
        index = np.int32(input_items[1][0])
        drift_corr = 0
        if (self.done) :
            drift_corr = self.sample_rate*(self.fixed_index-index-self.tcorr)/self.M
            # print drift_corr

        if not self.done :
            output_vector = input_vector[0:self.M]
            if (self.last_index == None) :
                self.last_index = index
                print("1")
            elif (self.last_index == index) :
                self.fixed_index = index
                self.done = True
                print("2")
            elif (self.last_index != index):
                self.last_index = index
                print("3")
            else:
                print("4")


        # print "drift:{}:{}:{}\n".format(index-self.last_index2, index, self.last_index2)
        self.last_index2 = index
        # print "index:{}".format(self.fixed_index)

        if (self.done == True) :
            if (self.fixed_index < half_cp) :
                output_vector = input_vector[self.fixed_index+half_cp:(self.fixed_index-half_cp)+N]
                self.symbol_part = None
            elif (self.fixed_index > (N-(half_cp-1))) :
                output_vector = input_vector[((self.fixed_index+half_cp)-N):N-(half_cp+(N-self.fixed_index))]
                self.symbol_part = None
            else :
                self.symbol_part = input_vector[0:self.fixed_index-half_cp]
                symbol_part2 = input_vector[self.fixed_index+half_cp:N]
                
                output_vector = np.concatenate((input_vector[0:self.fixed_index-half_cp], input_vector[self.fixed_index+half_cp:N]))

        # left or right drift
        # take samples out of middle

        output_items[0][:] = output_vector
        output_items[1][:] = drift_corr
        return len(output_items[0])
