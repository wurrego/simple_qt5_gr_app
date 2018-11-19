
from gnuradio import blocks, analog, gr
import numpy as np


def constant_0():
    '''
    function to create and return a GNURadio source block that outputs constant 0s
    :return : cosine wave of frequency 0
    :return type: GNURadio analog.sig_source_c block
    '''
    return analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)


def bytes(vector = None):
    '''
    function to create and return a GNURadio source block that outputs constant 0s
    :return : block that produces a random vector of 10000 ints between 0 and 255
    :return type: GNURadio blocks.vector_source_b block
    '''
    if vector is None:
        return blocks.vector_source_b(map(int, np.random.randint(0, 255, 1000)), True)
    else:
        return blocks.vector_source_b(vector, True)


def noise(noise_amp):
    '''
    function to create and return a GNURadio source block that outputs constant 0s
    :param noise_amp: variance of noise amplitude for the desired SNR
    :type noise_amp: float

    :return : block that produces a random vector of 8192 floats with mean 0 and variance noise_amp
    :return type: GNURadio blocks.vector_source_b block
    '''
    return analog.fastnoise_source_c(analog.GR_GAUSSIAN, noise_amp, 0, 8192)
