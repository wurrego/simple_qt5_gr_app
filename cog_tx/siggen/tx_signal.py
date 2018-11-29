import numpy as np
from gnuradio import gr
import sources
from sinks import usrp_head_sink
import modulations
from cog_tx.mem_manager.shmem import shm_mem


class transmit(gr.top_block):

    # class constants
    antenna = 'TX/RX'
    preamble_size_bits = 256
    random_sequence_size_bits = 10240

    # Input Parameters
    center_freq_hz = 0.0
    symbol_rate_Bd = 0.0
    modulation_type = None
    gain_dB = 0.0
    number_of_symbols = 0
    samples_per_symbol = 0
    excess_bw = 0.0

    # Calculated Parameters
    sample_rate_hz = 0.0

    # grc graph parameters
    source = None

    def __init__(self, cbp, _tx_id, _center_freq_hz, _symbol_rate_Bd, _modulation_type, _gain_dB, _number_of_symbols, _samples_per_symbol=2, _excess_bw = 0.35, device_ip = "192.168.10.2"):

        gr.top_block.__init__(self, "Top Block")

        # save input parameters
        self.cbp = cbp
        self.frame_id = _tx_id
        self.center_freq_hz = _center_freq_hz
        self.symbol_rate_Bd = _symbol_rate_Bd
        self.modulation_type = _modulation_type
        self.gain_dB = _gain_dB
        self.number_of_symbols = _number_of_symbols
        self.samples_per_symbol = _samples_per_symbol
        self.excess_bw = _excess_bw
        self.usrp_device_ip = device_ip

        # calculate other transmitter parameters
        self.sample_rate_hz = self.symbol_rate_Bd * self.samples_per_symbol
        bits_per_symbol = modulations.get_bits_per_symbol(self.modulation_type)

        if not isinstance(bits_per_symbol, (int, long, float)):
            print("Fatal Error: Unable to calculate bits per symbol.")
            return

        total_bits_to_transmit = self.number_of_symbols * bits_per_symbol
        number_of_times_burst_vector_is_repeated = float(total_bits_to_transmit) / float(self.random_sequence_size_bits + self.preamble_size_bits)

        # source block  (0-255 represents 8 random bits (1 byte)
        preamble = map(int, np.random.randint(0, 255, int(self.preamble_size_bits/8.0)))
        data = map(int, np.random.randint(0, 255, int(self.random_sequence_size_bits/8.0)))
        #data = map(int, np.random.randint(0, 255, int((total_bits_to_transmit-self.preamble_size_bits)/8.0) ))
        burst_vector = preamble+data
        samples_to_tx = self.number_of_symbols * self.samples_per_symbol

        # save in shared mem
        self.cbp.write_channel_header(center_frequency_hz = self.center_freq_hz, sample_rate_hz=self.sample_rate_hz)
        self.cbp.write_frame_header(self.frame_id, len(burst_vector), 'i', number_of_times_burst_vector_is_repeated, len(preamble))
        self.cbp.write_int32_vector(burst_vector)

        # read from shared memory

        # read channel info
        channel_header =  self.cbp.read_channel_header()
        print ('[Channel Info]')
        print ('---- [Channel ID] ', channel_header.channel_id)
        print ('---- [Active Pointer] ', channel_header.active_pointer)
        print ('---- [Source] ', channel_header.source)
        print ('---- [Center Freq (MHz)] ', channel_header.center_freq_hz/1e6)
        print ('---- [Sample Rate (Ksps] ', channel_header.sample_rate_hz/1e3)

        # read frame info
        frame_index = 0+ self.cbp.channel_header_size_bytes
        frame_header =  self.cbp.read_frame_header(frame_index)
        print ('[Frame Info]')
        print ('---- [Frame ID] ', frame_header.frame_id)
        print ('---- [Frame Index] ', frame_index)
        print ('---- [Length] ', frame_header.length)
        print ('---- [Type] ', frame_header.type)
        print ('---- [Number of Instances] ', frame_header.number_of_instances)
        print ('---- [Preamble Length] ', frame_header.preamble_length)

        # read frame data
        rdata = self.cbp.read_int32_vector(frame_header.length, frame_header.data_index)

        assert np.array_equal(rdata,burst_vector)

        # source block with burst vector as sequence
        self.source = sources.bytes(burst_vector)

        # modulation block
        self.mod = self.parse_mod_type(self.modulation_type)

        # sink block
        self.sink = usrp_head_sink(center_freq_hz=self.center_freq_hz, sample_rate_hz=self.sample_rate_hz, antenna=self.antenna, gain_dB=self.gain_dB, ipv4_address=self.usrp_device_ip, N=samples_to_tx)

        # connect
        self.connect(self.source, self.mod, self.sink)

        file = open('test_output', 'w')
        file.write("[Channel Info] \n")
        file.write('---- [Channel ID] ' + str(channel_header.channel_id) + '\n')
        file.write('---- [Active Pointer] '+ str(channel_header.active_pointer) + '\n')
        file.write('---- [Source] '+ str(channel_header.source) + '\n')
        file.write('---- [Center Freq (MHz)] '+ str(channel_header.center_freq_hz / 1e6) + '\n')
        file.write('---- [Sample Rate (Ksps] '+ str(channel_header.sample_rate_hz / 1e3)+ '\n')

        file.write('[Frame Info] \n')
        file.write('---- [Frame ID] ' +  str(frame_header.frame_id) + '\n')
        file.write('---- [Frame Index] '+ str(frame_index) + '\n')
        file.write('---- [Length] '+ str(frame_header.length) + '\n')
        file.write('---- [Type] '+ str(frame_header.type) + '\n')
        file.write('---- [Number of Instances] '+ str(frame_header.number_of_instances) + '\n')
        file.write('---- [Preamble Length] ' +str(frame_header.preamble_length) + '\n')

        file.write('\n [Preamble] \n')
        file.write(preamble.__str__())

        file.write('\n [Burst Data] \n')
        file.write(data.__str__())
        file.close()


    def parse_mod_type(self, modulation_type):
        print('Using modulation: ' + modulation_type)
        return {
            'BPSK': modulations.bpsk(self.samples_per_symbol, self.excess_bw),
            'QPSK': modulations.qpsk(self.samples_per_symbol, self.excess_bw),
            '8PSK': modulations.psk8(self.samples_per_symbol, self.excess_bw),
            '16PSK': modulations.psk16(self.samples_per_symbol, self.excess_bw),
            'QAM16': modulations.qam16(self.samples_per_symbol, self.excess_bw),
            'PI4QPSK': modulations.Pi4DQPSKMod(self.sample_rate_hz, self.samples_per_symbol, self.excess_bw),
            'GMSK': modulations.gmsk(self.samples_per_symbol, self.excess_bw),
        }[modulation_type]