#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Gr-gsm Livemon
# Author: Piotr Krysik
# Description: Interactive monitor of a single C0 channel with analysis performed by Wireshark (command to run wireshark: sudo wireshark -k -f udp -Y gsmtap -i lo)
# Generated: Mon Jul 18 18:08:34 2016
##################################################
# modified Jan 2017 lin_s for headless mode
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from math import pi
from optparse import OptionParser
import grgsm
import osmosdr
import pmt
import sip
import sys
import time


class grgsm_livemon(gr.top_block):

    def __init__(self, args="", fc=939.4e6, gain=30, ppm=0, samp_rate=2000000.052982, shiftoff=400e3, osr=4):
        gr.top_block.__init__(self, "Gr-gsm Livemon")

        ##################################################
        # Parameters
        ##################################################
        self.args = args
        self.fc = fc
        self.gain = gain
        self.ppm = ppm
        self.samp_rate = samp_rate
        self.shiftoff = shiftoff
        self.osr = osr

        print " [+] starting grgsm_livemon_headless..."
        print " [>] frequency: %s Hz (specify with -fc)" % fc
        print " [>] gain: %s dB (specify with --gain)" % gain
        print " [>] ppm: %s (specify with --ppm)" % ppm
        print " [>] sample rate: %s (specify with --samp_rate)" % samp_rate
        print " [>] shift offset: %s Hz (specify with --shiftoff)" % shiftoff

        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + args )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(fc-shiftoff, 0)
        self.rtlsdr_source_0.set_freq_corr(self.ppm, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(self.gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(250e3+abs(shiftoff), 0)
          
        self.gsm_sdcch8_demapper_0 = grgsm.gsm_sdcch8_demapper(
            timeslot_nr=1,
        )
        self.gsm_receiver_0 = grgsm.receiver(4, ([0]), ([]), False)
        self.gsm_message_printer_1 = grgsm.message_printer(pmt.intern(""), False,
            False, False)
        self.gsm_input_0 = grgsm.gsm_input(
            ppm=0,
            osr=4,
            fc=fc,
            samp_rate_in=samp_rate,
        )
        self.gsm_decryption_0 = grgsm.decryption(([]), 1)
        self.gsm_control_channels_decoder_0_0 = grgsm.control_channels_decoder()
        self.gsm_control_channels_decoder_0 = grgsm.control_channels_decoder()
        self.gsm_clock_offset_control_0 = grgsm.clock_offset_control(fc-shiftoff, samp_rate, osr)
        self.gsm_bcch_ccch_demapper_0 = grgsm.gsm_bcch_ccch_demapper(
            timeslot_nr=0,
        )
        self.blocks_socket_pdu_0_0 = blocks.socket_pdu("UDP_SERVER", "127.0.0.1", "4730", 10000, False)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_CLIENT", "127.0.0.1", "4729", 10000, False)
        self.blocks_rotator_cc_0 = blocks.rotator_cc(-2*pi*shiftoff/samp_rate)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gsm_bcch_ccch_demapper_0, 'bursts'), (self.gsm_control_channels_decoder_0, 'bursts'))    
        self.msg_connect((self.gsm_clock_offset_control_0, 'ctrl'), (self.gsm_input_0, 'ctrl_in'))    
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.gsm_message_printer_1, 'msgs'))    
        self.msg_connect((self.gsm_control_channels_decoder_0_0, 'msgs'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.msg_connect((self.gsm_control_channels_decoder_0_0, 'msgs'), (self.gsm_message_printer_1, 'msgs'))    
        self.msg_connect((self.gsm_decryption_0, 'bursts'), (self.gsm_control_channels_decoder_0_0, 'bursts'))    
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_bcch_ccch_demapper_0, 'bursts'))    
        self.msg_connect((self.gsm_receiver_0, 'measurements'), (self.gsm_clock_offset_control_0, 'measurements'))    
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_sdcch8_demapper_0, 'bursts'))    
        self.msg_connect((self.gsm_sdcch8_demapper_0, 'bursts'), (self.gsm_decryption_0, 'bursts'))    
        self.connect((self.blocks_rotator_cc_0, 0), (self.gsm_input_0, 0))    
        self.connect((self.gsm_input_0, 0), (self.gsm_receiver_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_rotator_cc_0, 0))    
        
        print " [+] go!"

def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "", "--args", dest="args", type="string", default="",
        help="Set Device Arguments [default=%default]")
    parser.add_option(
        "-f", "--fc", dest="fc", type="eng_float", default=eng_notation.num_to_str(939.4e6),
        help="Set fc [default=%default]")
    parser.add_option(
        "-g", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(30),
        help="Set gain [default=%default]")
    parser.add_option(
        "-p", "--ppm", dest="ppm", type="intx", default=0,
        help="Set ppm [default=%default]")
    parser.add_option(
        "-s", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(2000000.052982),
        help="Set samp_rate [default=%default]")
    parser.add_option(
        "-o", "--shiftoff", dest="shiftoff", type="eng_float", default=eng_notation.num_to_str(400e3),
        help="Set shiftoff [default=%default]")
    parser.add_option(
        "", "--osr", dest="osr", type="intx", default=4,
        help="Set OSR [default=%default]")
    return parser

def main(options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = grgsm_livemon(args=options.args, fc=options.fc, gain=options.gain, ppm=options.ppm, samp_rate=options.samp_rate, shiftoff=options.shiftoff, osr=options.osr)
    tb.start()
    while True:
        pass

if __name__ == '__main__':
    main()
