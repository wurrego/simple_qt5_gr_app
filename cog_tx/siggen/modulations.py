from gnuradio import blocks
from gnuradio import digital
from modulations_pi4qpsk import *
import math
import numpy as np


"""
These functions create and return blocks that modulate incoming data, producing symbols.
"""

mod_types = {
    'discrete': ['BPSK', 'QPSK', '8PSK', '16PSK', 'QAM16', 'QAM32', 'QAM64', 'GFSK',
                 'GMSK', 'QAM32', 'PI4QPSK'],
    'none': ['NOISE']
}


def get_bits_per_symbol(modulation):

    switch = {
        "BPSK": np.log2(float(2)),
        "QPSK": np.log2(float(4)),
        "8PSK": np.log2(float(8)),
        "16PSK": np.log2(float(16)),
        "PI4QPSK": np.log2(float(4)),
        "QAM16": np.log2(float(16)),
        "GMSK": np.log2(float(2)),
    }

    return switch.get(modulation, lambda: None)



def bpsk(sps, excess_bw=0.35):
    return digital.psk.psk_mod(
        constellation_points=2,
        mod_code="gray",
        differential=True,
        samples_per_symbol=sps,
        excess_bw=excess_bw,
        verbose=False,
        log=False,
    )


def qpsk(sps, excess_bw=0.35):
    return digital.psk.psk_mod(
        constellation_points=4,
        mod_code="gray",
        differential=True,
        samples_per_symbol=sps,
        excess_bw=excess_bw,
        verbose=False,
        log=False,
    )


def psk8(sps, excess_bw=0.35):
    return digital.psk.psk_mod(
        constellation_points=8,
        mod_code="gray",
        differential=True,
        samples_per_symbol=sps,
        excess_bw=excess_bw,
        verbose=False,
        log=False,
    )


def psk16(sps, excess_bw=0.35):
    return digital.psk.psk_mod(
        constellation_points=16,
        mod_code="gray",
        differential=True,
        samples_per_symbol=sps,
        excess_bw=excess_bw,
        verbose=False,
        log=False,
    )


def qam16(sps, excess_bw=0.35):
    return digital.qam.qam_mod(
        constellation_points=16,
        mod_code="gray",
        differential=True,
        samples_per_symbol=sps,
        excess_bw=excess_bw,
        verbose=False,
        log=False,
    )


def qam32(sps, excess_bw=0.35):
    qam32_constellation = digital.constellation_calcdist(([x / math.sqrt(20) for x in
                                                           [-3 + 5j, -1 + 5j, 1 + 5j, 3 + 5j, -5 + 3j, -3 + 3j, -1 + 3j,
                                                            1 + 3j, 3 + 3j, 5 + 3j, -5 + 1j, -3 + 1j, -1 + 1j, 1 + 1j,
                                                            3 + 1j, 5 + 1j, -5 - 1j, -3 - 1j, -1 - 1j, 1 - 1j, 3 - 1j,
                                                            5 - 1j, -5 - 3j, -3 - 3j, -1 - 3j, 1 - 3j, 3 - 3j, 5 - 3j,
                                                            -3 - 5j, -1 - 5j, 1 - 5j, 3 - 5j]]), (
                                                         [0, 1, 29, 28, 4, 8, 12, 16, 20, 24, 5, 9, 13, 17, 21, 25, 6,
                                                          10, 14, 18, 22, 26, 7, 11, 15, 19, 23, 27, 3, 2, 30, 31]), 4,
                                                         1).base()

    return digital.generic_mod(
        constellation=qam32_constellation,
        differential=True,
        samples_per_symbol=sps,
        pre_diff_code=True,
        excess_bw=excess_bw,
        verbose=False,
        log=False,
    )


def qam64(sps, excess_bw=0.35):
    return digital.qam.qam_mod(
        constellation_points=64,
        mod_code="gray",
        differential=True,
        samples_per_symbol=sps,
        excess_bw=excess_bw,
        verbose=False,
        log=False,
    )


def gmsk(sps, excess_bw=0.35):
    return digital.gmsk_mod(
        samples_per_symbol=sps,
        bt=excess_bw,
        verbose=False,
        log=False,
    )


def gfsk(sps, sensitivity, excess_bw=0.35):
    return digital.gfsk_mod(
        samples_per_symbol=sps,
        sensitivity=sensitivity,
        bt=excess_bw,
        verbose=False,
        log=False,
    )


def no_mod():
    '''
    Creates a GNURadio block that passes through the incoming signal
    :return: GNURadio block that passes through data
    '''
    return blocks.multiply_const_cc(1)
