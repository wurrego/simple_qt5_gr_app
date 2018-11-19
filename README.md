# simple_qt5_gr_app
A simple Python Qt 5 application for use with GNU Radio


# Install QT5 Steps
1. Install Qt 5.10.1
2. Install sip 4.19.8

..* https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.6/sip-4.19.6.tar.gz
..* tar xvf sip-4.19.6.tar.gz
..* cd sip-4.19.6/
..* python configure.py
..* make
..* sudo make install

3. Install PyQt5

..* wget https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.10.1/PyQt5_gpl-5.10.1.tar.gz
..* tar xvf PyQt5_gpl-5.10.1.tar.gz
..* cd PyQt5_gpl-5.10.1.tar.gz/
..*  
```
python configure.py -d <path_to_venv>/lib/python2.7/site-packages/ --sip=<path_to_venv>/bin/sip --sip-incdir=<path_to_sip>/sip-4.19.8/siplib/ --qmake <user_name>/Qt/5.10.1/gcc_64/bin/qmake
```
..* make -j 8
..* sudo make install

4) Test
..* python 
..* import PyQt5

5) add dep
..* sudo apt-get install libx11-xcb1

6) 
..* "error not xcb platform found"
```
QT_QPA_PLATFORM_PLUGIN_PATH=~/Qt/5.10.1/gcc_64/plugins LD_LIBRARY_PATH=. QT_DEBUG_PLUGINS=1 PYTHONPATH=../ python __main__.py 
```
..* or add following to venv/bin/qt.conf
```
Plugins = ~/Qt/5.10.1/gcc_64/plugins
```