from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio import uhd
from gnuradio import channels
from random import getrandbits
from random import randint


def usrp_sink(center_freq_hz, sample_rate_hz, antenna, gain_dB, ipv4_address):

    u = uhd.usrp_sink(",".join(("addr="+ipv4_address, "")), uhd.stream_args(cpu_format="fc32", channels=range(1), ), )

    u.set_center_freq(center_freq_hz, 0)
    u.set_samp_rate(sample_rate_hz)
    u.set_antenna(antenna, 0)
    u.set_gain(gain_dB, 0)

    return u


class usrp_head_sink(gr.hier_block2):

    def __init__(self, center_freq_hz, sample_rate_hz, antenna, gain_dB, ipv4_address, N):
        gr.hier_block2.__init__(
            self, "usrp_head_sink",
            gr.io_signature(1, 1, gr.sizeof_gr_complex * 1),
            gr.io_signature(0, 0, 0),
        )

        self.head = blocks.head(gr.sizeof_gr_complex * 1, N)

        print("Using USRP Device with IPv4 Address: " + str(ipv4_address))
        self.usrp = uhd.usrp_sink(",".join(("addr=" + str(ipv4_address), "")), uhd.stream_args(cpu_format="fc32", channels=range(1), ), )

        self.usrp.set_center_freq(center_freq_hz, 0)
        self.usrp.set_samp_rate(sample_rate_hz)
        self.usrp.set_antenna(antenna, 0)
        self.usrp.set_gain(gain_dB, 0)

        self.connect(self.head, self.usrp)
        self.connect(self, (self.head, 0))


class snr_usrp(gr.hier_block2):

    def __init__(self, values, snr_reference):
        gr.hier_block2.__init__(
            self, "snr_usrp_sink",
            gr.io_signature(1, 1, gr.sizeof_gr_complex * 1),
            gr.io_signature(0, 0, 0),
        )

        noise_amp = 10 ** (-values['snr'] / (snr_reference * 20.0))

        self.add = blocks.add_vcc(1)
        self.noise_source = analog.fastnoise_source_c(analog.GR_GAUSSIAN, noise_amp, 0, 8192)
        self.u = usrp_sink(values)

        self.connect(self.noise_source, (self.add, 0), self.u)
        self.connect(self, (self.add, 1))


class snr_head_file(gr.hier_block2):

    def __init__(self, snr, snr_reference, sink_file):
        gr.hier_block2.__init__(
            self, "snr_head_file",
            gr.io_signature(1, 1, gr.sizeof_gr_complex * 1),
            gr.io_signature(0, 0, 0),
        )
        noise_amp = 10 ** (-snr / (snr_reference * 20.0))

        self.head = blocks.head(gr.sizeof_gr_complex * 1, 1024)
        self.skiphead = blocks.skiphead(gr.sizeof_gr_complex * 1, 10000)
        self.file_sink = blocks.file_sink(gr.sizeof_gr_complex * 1, sink_file, False)
        self.file_sink.set_unbuffered(False)
        self.add = blocks.add_vcc(1)
        self.noise_source = analog.fastnoise_source_c(analog.GR_GAUSSIAN, noise_amp, 0, 8192)

        self.connect(self.noise_source, (self.add, 0), self.skiphead, self.head, self.file_sink)
        self.connect(self, (self.add, 1))


