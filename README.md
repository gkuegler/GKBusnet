# Busnet - Very Much A Work in Progress
A scada window application implemented in python

Shall connect to remote plc's with modbusTCP.


Steps to Running Through Python Interpreter on Windows:
1. Install Python3.7 or above
2. Run pip_requirements\install_dep_modules.bat
3. Run '___run_myui_with_python.bat' to launch program


Edit Devices: Declare devices as a list of devices in device_list.py
Device tree shall auto generate list.

Linux Install Instructions:
1. apt-get install python3
2. apt-get install python-pip
3. pip3 (install dependencies from file)
4. python3 -m PyInstaller ui_main.py --onefile --noconsole
