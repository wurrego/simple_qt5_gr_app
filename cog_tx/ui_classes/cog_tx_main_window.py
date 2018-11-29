from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject

from cog_tx.ui.ui_mainwindow import Ui_MainWindow
from cog_tx.siggen.tx_signal import transmit
from cog_tx.mem_manager.shmem import shm_mem


class CogTransmit_MainWindow(QtWidgets.QMainWindow, Ui_MainWindow, QObject):

    # class members
    window = None
    transmit_button_state = False
    transmitter = None
    tx_center_freq_hz = 0.0
    tx_symbol_rate_bd = 0.0
    tx_modulation_type = None
    tx_number_of_symbols = 0
    transmission_count = 0
    gain = 0
    filter_bw = 0.0
    usrp_ip = None
    parent = None

    def __init__(self, parent=None):

        super(CogTransmit_MainWindow, self).__init__()

        self.parent = parent

        # init shared memory
        self.cbp = shm_mem(channel_id=0, write_permissions=True)

        # setup ui
        self.setupUi(self)

        # configure input fields
        self.setupInputField()

        # connect buttons
        self.transmit_button.clicked.connect(self.on_transmitButton_Clicked)

        # show ui
        self.show()


    def setupInputField(self):

        # tuning frequency bounds
        self.center_frequency_mhz_spinBox.setMinimum(20)
        self.center_frequency_mhz_spinBox.setMaximum(6000)
        self.center_frequency_mhz_spinBox.setSingleStep(.01)
        self.center_frequency_mhz_spinBox.setValue(895)

        # Gain Bounds
        self.gain_spinBox.setMinimum(0)
        self.gain_spinBox.setMaximum(30)
        self.gain_spinBox.setSingleStep(1)
        self.gain_spinBox.setValue(10)

        # symbol rate bounds
        self.symbol_rate_kBd_spinBox.setMinimum(2.4)
        self.symbol_rate_kBd_spinBox.setMaximum(1024)
        self.symbol_rate_kBd_spinBox.setSingleStep(2.4)
        self.symbol_rate_kBd_spinBox.setValue(200.0)

        # number of symbols to generate bounds
        self.number_of_symbols_spinBox.setMinimum(1000)
        self.number_of_symbols_spinBox.setMaximum(1000000000)
        self.number_of_symbols_spinBox.setSingleStep(1)
        self.number_of_symbols_spinBox.setValue(200000)

        # modulation choices
        self.modulation_comboBox.addItem("BPSK")
        self.modulation_comboBox.addItem("QPSK")
        self.modulation_comboBox.addItem("8PSK")
        self.modulation_comboBox.addItem("16PSK")
        self.modulation_comboBox.addItem("QAM16")
        self.modulation_comboBox.addItem("PI4QPSK")
        self.modulation_comboBox.addItem("GMSK")

        # RRC Filter Excess Bandwidth (Beta)
        self.filter_excess_bw_SpinBox.setMinimum(0)
        self.filter_excess_bw_SpinBox.setMaximum(1)
        self.filter_excess_bw_SpinBox.setSingleStep(.01)
        self.filter_excess_bw_SpinBox.setValue(0.35)

        # USRP Device IPv4 Address
        self.device_ip_lineEdit.setText("192.168.10.2")


    def on_transmitButton_Clicked(self):

        # toggle state
        self.transmit_button_state = not self.transmit_button_state

        # update button text
        if self.transmit_button_state:
            self.transmit_button.setText("Halt")
            self.start_transmit()
        else:
            self.transmit_button.setText("Transmit")
            self.stop_transmit()

    def get_ui_values(self):

        self.tx_center_freq_hz = self.center_frequency_mhz_spinBox.value() * 1e6
        self.tx_symbol_rate_bd = self.symbol_rate_kBd_spinBox.value() * 1e3
        self.tx_modulation_type = self.modulation_comboBox.currentText()
        self.tx_number_of_symbols = self.number_of_symbols_spinBox.value()
        self.gain = self.gain_spinBox.value()
        self.filter_bw = self.filter_excess_bw_SpinBox.value()
        self.usrp_ip = self.device_ip_lineEdit.text()

    def stop_transmit(self):

        print('Halting Transmit')

        if self.transmitter is not None:
            self.transmitter.stop()


    def start_transmit(self):

        print('Starting Transmit')

        self.get_ui_values()

        # increment number of transmissions
        self.transmission_count += 1

        # transmit the user selected signal
        self.transmitter = transmit(self.cbp, _tx_id=self.transmission_count, _center_freq_hz=self.tx_center_freq_hz, _symbol_rate_Bd=self.tx_symbol_rate_bd, _modulation_type=self.tx_modulation_type, _gain_dB=self.gain, _number_of_symbols=self.tx_number_of_symbols, _samples_per_symbol=2, _excess_bw = self.filter_bw, device_ip = self.usrp_ip)

        self.transmitter.start()

