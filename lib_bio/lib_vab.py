########################################################################################################################
# LIB_VAB - SONY PLAYSTATION SOUND SOURCE DATA
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct

#=======================================================================================================================
# GENERIC
#=======================================================================================================================
class vh_program_attribute_table:
    def __init__(self):
        self.object = []

    def read(self, file):
        self.object = []

        for i in range(16):
            self.object.append(file.read(128))

        return self

    def write(self, file):
        for i in range(len(self.object)):
            file.write(self.object[i])

class vh_tone_attribute_table:
    def __init__(self):
        self.object = []

    def read(self, file):
        self.object = []

        for i in range(32):
            self.object.append(file.read(16))

        return self

    def write(self, file):
        for i in range(len(self.object)):
            file.write(self.object[i])

class vh_header:
    def __init__(self):
        self.magic = 1447117424   #uint32; "pBAV"
        self.version = 0          #uint32; format version
        self.id = 0               #uint32; vab id
        self.size = 0             #uint32; waveform size in bytes
        self.reserved_0 = 0       #uint16; system reserved value...
        self.programs = 0         #uint16; total number of programs used
        self.tones = 0            #uint16; total number of tones used
        self.vag_count = 0        #uint16; total number of .vag files used
        self.master_volume = 0    #byte; master volume used
        self.master_pan = 0       #byte; master pan used
        self.bank_attribute_1 = 0 #byte; user defined attribute of bank 1
        self.bank_attribute_2 = 0 #byte; user defined attribute of bank 2
        self.reserved_1 = 0       #uint32; system reserved value...

    def read(self, file):
        self.magic = int(struct.unpack("L", file.read(4))[0])
        self.version = int(struct.unpack("L", file.read(4))[0])
        self.id = int(struct.unpack("L", file.read(4))[0])
        self.size = int(struct.unpack("L", file.read(4))[0])
        self.reserved_0 = int(struct.unpack("H", file.read(2))[0])
        self.programs = int(struct.unpack("H", file.read(2))[0])
        self.tones = int(struct.unpack("H", file.read(2))[0])
        self.vag_count = int(struct.unpack("H", file.read(2))[0])
        self.master_volume = int(struct.unpack("B", file.read(1))[0])
        self.master_pan = int(struct.unpack("B", file.read(1))[0])
        self.bank_attribute_1 = int(struct.unpack("B", file.read(1))[0])
        self.bank_attribute_2 = int(struct.unpack("B", file.read(1))[0])
        self.reserved_1 = int(struct.unpack("L", file.read(4))[0])

        return self

    def write(self, file):
        file.write(struct.pack('L', int(self.magic)))
        file.write(struct.pack('L', int(self.version)))
        file.write(struct.pack('L', int(self.id)))
        file.write(struct.pack('L', int(self.size)))
        file.write(struct.pack('H', int(self.reserved_0)))
        file.write(struct.pack('H', int(self.programs)))
        file.write(struct.pack('H', int(self.tones)))
        file.write(struct.pack('H', int(self.vag_count)))
        file.write(struct.pack('B', int(self.master_volume)))
        file.write(struct.pack('B', int(self.master_pan)))
        file.write(struct.pack('B', int(self.bank_attribute_1)))
        file.write(struct.pack('B', int(self.bank_attribute_2)))
        file.write(struct.pack('L', int(self.reserved_1)))

class vh_file:
    def __init__(self):
        self.header = vh_header()
        self.program_attribute_table = vh_program_attribute_table()
        self.tone_attribute_table = [] #vh_tone_attribute_table[self.header.programs]
        self.vag_offset_table = []

    def read(self, file, offset):
        file.seek(offset)
        print('[LIB_VAB] <READ> VH_FILE\t(' + str(file.tell()) + ')')

        self.header = self.header.read(file)
        self.program_attribute_table.read(file)

        for i in range(self.header.programs):
            tmp_obj = vh_tone_attribute_table()
            tmp_obj = tmp_obj.read(file)
            self.tone_attribute_table.append(tmp_obj)
        
        file.seek(2, 1)

        for i in range(self.header.vag_count):
            self.vag_offset_table.append(int(struct.unpack("H", file.read(2))[0]) << 3)
        
        return self

    def write(self, file, offset):
        file.seek(offset)
        print('[LIB_VAB] <WRITE> VH_FILE\t(' + str(offset) + ')')
        
        self.header.write(file)
        self.program_attribute_table.write(file)

        for i in range(self.header.programs):
            self.tone_attribute_table[i].write(file)
        
        o_tmp = file.tell()

        for i in range(128):
            file.write(struct.pack('L', int(0) >> 3))
        
        file.seek(-510, 1)

        for i in range(self.header.vag_count):
            file.write(struct.pack('H', int(self.vag_offset_table[i]) >> 3))

        file.seek(offset + o_tmp + 512)

    def extract(self, filepath):
        print('[LIB_VAB] <EXTRACT> VH_FILE\t(' + filepath + ')')

        file = open(filepath, 'wb')
        self.write(file, 0)
        file.close()

class vb_file:
    def __init__(self):
        self.object = []

    def read(self, file, offset, vag_offset_table):
        file.seek(offset)
        print('[LIB_VAB] <READ> VB_FILE\t(' + str(file.tell()) + ')')
        self.object = []

        for i in range(len(vag_offset_table)):
            self.object.append(file.read(vag_offset_table[i]))
        
        return self

    def write(self, file, offset):
        file.seek(offset)
        print('[LIB_VAB] <WRITE> VB_FILE\t(' + str(file.tell()) + ')')

        for i in range(len(self.object)):
            file.write(self.object[i])

    def extract(self, filepath):
        print('[LIB_VAB] <EXTRACT> VB_FILE\t(' + filepath + ')')

        file = open(filepath, 'wb')
        self.write(file, 0)
        file.close()