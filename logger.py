import csv
import datetime

class MissingHeader(Exception): pass

class Logger():
    def __init__(self, filename=None, file_verified=False, header=None,  log_enable=None, debug=False):
        self.filename = filename
        self.file_verified = file_verified
        self.header = header
        self.log_enable = log_enable
        self._data = []
        self._plc_data = []
        self._now = []
        self.debug = debug

    def _create_file(self):
        #this will always write the first row and ovverwrite all other rows and add newline
        #file just passes data to callback to logfile
        with open(self.filename, 'w', newline='') as f:
            w = csv.writer(f, delimiter=',')
            w.writerow(self.header)
            print('file created')
        self.file_verified = True
        if self.debug: print('Heder Constructed')
        #when file is created callback to try and log data again with data
        self.log_logic()

    def _verify_file(self):
        try:
            with open(self.filename, 'r') as f:
                    #check if file has anythin in first line
                    if f.readline() in ['\n','']:
                        print('blank 1st line')
                        self._create_file()
                    #line1, line2 = next(f), next(f)
                    #if r != header: raise MissingHeader
                    #print(line1)
                    #print(line2)
                    f.close()
                    self.file_verified = True
                    self.log_logic()

        except FileNotFoundError:
            if self.debug: print('file not found')
            self._create_file()
        except StopIteration:
            if self.debug: print('missing 2nd line')
            self.create_file()
        except MissingHeader:
            if self.debug: print('file has no headers or incorrect headers')
    
    def _write_data(self):
        #will write new row with list input
        with open(self.filename, 'a', newline='') as f:
            r = csv.writer(f, delimiter=",")
            r.writerow(self._data)
            f.close()
    
    def log_logic(self):
        try: 
            if self.file_verified: self._write_data()
            else: self._verify_file()
        #pass data for log() callback
        except (FileNotFoundError, StopIteration): self._verify_file()

        #Entry Method for control program
    def log(self, plc_data):
        self._plc_data = plc_data
        self._now = [str(datetime.datetime.now())]
        self._data = self._now + self._plc_data
        if self.debug: print(self._data)
        if self.log_enable: self.log_logic()
        else: pass