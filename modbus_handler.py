import modbus_constants as const
from modbus_utils import test_bit, set_bit
import struct
from threading import Lock
        
class ModService:

    """ Data class for thread safe access to bits and words space """
    def __init__(self):
        self.bits_lock = Lock()
        self.bits = [False] * 0x10000
        self.words_lock = Lock()
        self.words = [0] * 0x10000
        self.debug = True

    def get_bits(self, address, number=1):
        with self.bits_lock:
            if (address >= 0) and (address + number <= len(self.bits)):
                return self.bits[address: number + address]
            else:
                return None

    def set_bits(self, address, bit_list):
        with self.bits_lock:
            if (address >= 0) and (address + len(bit_list) <= len(self.bits)):
                self.bits[address: address + len(bit_list)] = bit_list
                return True
            else:
                return None


    def get_words(self, address, number=1):
        with self.words_lock:
            if (address >= 0) and (address + number <= len(self.words)):
                return self.words[address: number + address]
            else:
                return None


    def set_words(self, address, word_list):
        with self.words_lock:
            if (address >= 0) and (address + len(word_list) <= len(self.words)):
                self.words[address: address + len(word_list)] = word_list
                return True
            else:
                return None

    def handle(self, data):
        """ MBUS FRAME
        NAME                    BYTES   DESCRIPTION
        Transaction identifier  2       For synchronization between messages of server and client
        Protocol identifier     2       0 for Modbus/TCP
        Length field            2       Number of remaining bytes in this frame
        Unit identifier         1       Slave address (255 if not used)
        Function code           1       Function codes as in other variants
        Data bytes              2       Data as response or commands
        Rest                    n
        """
        exp_status = const.EXP_NONE #set clean modbus exception status
        rx_head = data[:7]  #bytes 0-6 so 7 bytes final-start = bytecount
        
        if not rx_head: pass # close connection if no standard 7 bytes header
        # decode header
        (rx_hd_tr_id, rx_hd_pr_id, rx_hd_length, rx_hd_unit_id) = struct.unpack('>HHHB', rx_head)

        if True:
            print(rx_hd_tr_id)
            print(rx_hd_pr_id)
            print(rx_hd_length)
            print(rx_hd_unit_id)
        # close connection if frame header content inconsistency
        if not ((rx_hd_pr_id == 0) and (2 < rx_hd_length < 256)): pass
        # receive body
        rx_body = data[7:]
        # close connection if lack of bytes in frame body
        if not (rx_body and (len(rx_body) == rx_hd_length - 1)): pass
        # body decode: function code
        rx_bd_fc = struct.unpack('B', rx_body[0:1])[0]
        # close connection if function code is inconsistent
        if rx_bd_fc > 0x7F: exp_status = "function code illegal"
        # functions Read Coils (0x01) or Read Discrete Inputs (0x02)
        if rx_bd_fc in (const.READ_COILS, const.READ_DISCRETE_INPUTS):
            (b_address, b_count) = struct.unpack('>HH', rx_body[1:])
            # check quantity of requested bits
            if 0x0001 <= b_count <= 0x07D0:
                bits_l = self.get_bits(b_address, b_count)
                if bits_l:
                    # allocate bytes list
                    b_size = int(b_count / 8)
                    b_size += 1 if (b_count % 8) else 0
                    bytes_l = [0] * b_size
                    # populate bytes list with data bank bits
                    for i, item in enumerate(bits_l):
                        if item:
                            byte_i = int(i/8)
                            bytes_l[byte_i] = set_bit(bytes_l[byte_i], i % 8)
                    # format body of frame with bits
                    tx_body = struct.pack('BB', rx_bd_fc, len(bytes_l))
                    # add bytes with bits
                    for byte in bytes_l: tx_body += struct.pack('B', byte)
                else: exp_status = const.EXP_DATA_ADDRESS
            else: exp_status = const.EXP_DATA_VALUE
        # functions Read Holding Registers (0x03) or Read Input Registers (0x04)
        elif rx_bd_fc in (const.READ_HOLDING_REGISTERS, const.READ_INPUT_REGISTERS):
            (w_address, w_count) = struct.unpack('>HH', rx_body[1:])
            # check quantity of requested words
            if 0x0001 <= w_count <= 0x007D:
                words_l = self.get_words(w_address, w_count)
                if words_l:
                    # format body of frame with words
                    tx_body = struct.pack('BB', rx_bd_fc, w_count * 2)
                    for word in words_l:
                        tx_body += struct.pack('>H', word)
                else: exp_status = const.EXP_DATA_ADDRESS
            else: exp_status = const.EXP_DATA_VALUE
        # function Write Single Coil (0x05)
        elif rx_bd_fc is const.WRITE_SINGLE_COIL:
            (b_address, b_value) = struct.unpack('>HH', rx_body[1:])
            f_b_value = bool(b_value == 0xFF00)
            if self.set_bits(b_address, [f_b_value]):
                # send write ok frame
                tx_body = struct.pack('>BHH', rx_bd_fc, b_address, b_value)
            else: exp_status = const.EXP_DATA_ADDRESS
        # function Write Single Register (0x06)
        elif rx_bd_fc is const.WRITE_SINGLE_REGISTER:
            (w_address, w_value) = struct.unpack('>HH', rx_body[1:])
            if self.set_words(w_address, [w_value]):
                # send write ok frame
                tx_body = struct.pack('>BHH', rx_bd_fc, w_address, w_value)
            else: exp_status = const.EXP_DATA_ADDRESS
        # function Write Multiple Coils (0x0F)
        elif rx_bd_fc is const.WRITE_MULTIPLE_COILS:
            (b_address, b_count, byte_count) = struct.unpack('>HHB', rx_body[1:6])
            # check quantity of updated coils
            if (0x0001 <= b_count <= 0x07B0) and (byte_count >= (b_count/8)):
                # allocate bits list
                bits_l = [False] * b_count
                # populate bits list with bits from rx frame
                for i, item in enumerate(bits_l):
                    b_bit_pos = int(i/8)+6
                    b_bit_val = struct.unpack('B', rx_body[b_bit_pos:b_bit_pos+1])[0]
                    bits_l[i] = test_bit(b_bit_val, i % 8)
                # write words to data bank
                if self.set_bits(b_address, bits_l):
                    # send write ok frame
                    tx_body = struct.pack('>BHH', rx_bd_fc, b_address, b_count)
                else: exp_status = const.EXP_DATA_ADDRESS
            else: exp_status = const.EXP_DATA_VALUE
        # function Write Multiple Registers (0x10)
        elif rx_bd_fc is const.WRITE_MULTIPLE_REGISTERS:
            (w_address, w_count, byte_count) = struct.unpack('>HHB', rx_body[1:6])
            # check quantity of updated words
            if (0x0001 <= w_count <= 0x007B) and (byte_count == w_count * 2):
                # allocate words list
                words_l = [0] * w_count
                # populate words list with words from rx frame
                for i, item in enumerate(words_l):
                    w_offset = i * 2 + 6
                    words_l[i] = struct.unpack('>H', rx_body[w_offset:w_offset + 2])[0]
                # write words to data bank
                if self.set_words(w_address, words_l):
                    # send write ok frame
                    tx_body = struct.pack('>BHH', rx_bd_fc, w_address, w_count)
                else: exp_status = const.EXP_DATA_ADDRESS
            else: exp_status = const.EXP_DATA_VALUE
        #ECHO BACK THE MESSAGE
        elif rx_bd_fc is const.ECHO: tx_body = rx_body

        else: exp_status = const.EXP_ILLEGAL_FUNCTION
        # check exception
        if exp_status != const.EXP_NONE:
            # format body of frame with exception status
            tx_body = struct.pack('BB', rx_bd_fc + 0x80, exp_status)
        # build frame header
        tx_head = struct.pack('>HHHB', rx_hd_tr_id, rx_hd_pr_id, len(tx_body) + 1, rx_hd_unit_id)
        # send frame
        if self.debug:
            print(tx_head)
            print(tx_body)
        return tx_head + tx_body

if __name__ == '__main__':
     
    ti = b'\x00\x01' #Transaction identifier
    pi = b'\x00\x00' #Protocol identifier
    lf = b'\x00\x03' #Length field
    ui = b'\x00' #Unit identifier
    fc = b'\x05' #Function code
    addr = b'\x0f\xa1' #Data bytes
    val = b'\xff\x00'
    
    msg = ti + pi + lf + ui + fc + addr + val
    m = ModService()
    a = m.handle(msg)
    print('bytes message: {}'.format(a))
    print(m.get_bits(4001)[0])

   