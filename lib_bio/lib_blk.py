########################################################################################################################
# LIB_BLK - ENEMY ROAMING AREA DATA
########################################################################################################################
# SUPPORTED:
#               BIO HAZARD
#               BIOHAZARD 2 PROTOTYPE (NOV/1996)
#               BIOHAZARD 2
#               !BIOHAZARD 3: LAST ESCAPE;          NEED TO CHECK FORMAT USED...
########################################################################################################################
# 2014-2024, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct

#=======================================================================================================================
# BIO HAZARD
#=======================================================================================================================
class blk_object:
    def __init__(self, version):
        self.version = version

        if self.version == 1.0:
            self.x1 = 0        #uint16;
            self.z1 = 0        #uint16;
            self.x2 = 0        #uint16;
            self.z2 = 0        #uint16;
            self.direction = 0 #uint16;
            self.attribute = 0 #uint16;

        if self.version == 1.5 or self.version == 2.0:
            self.x1 = 0        #int16;
            self.z1 = 0        #int16;
            self.x2 = 0        #int16;
            self.z2 = 0        #int16;
            self.direction = 0 #uint16;
            self.attribute = 0 #uint16;

    def read(self, file):
        if self.version == 1.0:
            self.x1 = int(struct.unpack("H", file.read(2))[0])
            self.z1 = int(struct.unpack("H", file.read(2))[0])
            self.x2 = int(struct.unpack("H", file.read(2))[0])
            self.z2 = int(struct.unpack("H", file.read(2))[0])
            self.direction = int(struct.unpack("H", file.read(2))[0])
            self.attribute = int(struct.unpack("H", file.read(2))[0])
            return self

        if self.version == 1.5 or self.version == 2.0:
            self.x1 = int(struct.unpack("h", file.read(2))[0])
            self.z1 = int(struct.unpack("h", file.read(2))[0])
            self.x2 = int(struct.unpack("h", file.read(2))[0])
            self.z2 = int(struct.unpack("h", file.read(2))[0])
            self.direction = int(struct.unpack("H", file.read(2))[0])
            self.attribute = int(struct.unpack("H", file.read(2))[0])
            return self

    def write(self, file):
        if self.version == 1.0:
            file.write(struct.pack('H', int(self.x1)))
            file.write(struct.pack('H', int(self.z1)))
            file.write(struct.pack('H', int(self.x2)))
            file.write(struct.pack('H', int(self.z2)))
            file.write(struct.pack('H', int(self.direction)))
            file.write(struct.pack('H', int(self.attribute)))
        
        if self.version == 1.5 or self.version == 2.0:
            file.write(struct.pack('h', int(self.x1)))
            file.write(struct.pack('h', int(self.z1)))
            file.write(struct.pack('h', int(self.x2)))
            file.write(struct.pack('h', int(self.z2)))
            file.write(struct.pack('H', int(self.direction)))
            file.write(struct.pack('H', int(self.attribute)))

class blk_file:
    def __init__(self, version):
        self.version = version

        if self.version == 1.0:
            self.amount = 0  #uint16; total amount of objects
            self.object = [] #blk_object[self.amount]
            self.dummy = 0   #uint16; ?
    
        if self.version == 1.5 or self.version == 2.0:
            self.amount = 0  #uint32; total amount of objects
            self.object = [] #blk2_object[self.amount]
        
    def read_from_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_BLK] <READ> BLK_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')
        self.object = []

        if self.version == 1.0:
            self.amount = int(struct.unpack("H", file.read(2))[0])
        
        if self.version == 1.5 or self.version == 2.0:
            self.amount = int(struct.unpack("L", file.read(4))[0])
            
        for i in range(self.amount):
            tmp_obj = blk_object(self.version)
            tmp_obj = tmp_obj.read(file)
            self.object.append(tmp_obj)
        
        if self.version == 1.0:
            self.dummy = int(struct.unpack("H", file.read(2))[0])

        return self

    def read_from_file(self, filepath):
        print('[LIB_BLK] <READ> BLK_FILE ' + str(self.version) + '\t(' + filepath + ')')

        file = open(filepath, 'wb')
        self.read_from_stream(file, 0)
        file.close()

        return self

    def write_to_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_BLK] <WRITE> BLK_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')
        
        if self.version == 1.0:
            file.write(struct.pack('H', int(self.amount)))

        if self.version == 1.5 or self.version == 2.0:
            file.write(struct.pack('L', int(self.amount)))

        for i in range(len(self.object)):
            self.object[i].write(file)
        
        if self.version == 1.0:
            file.write(struct.pack('H', int(self.dummy)))

    def write_to_file(self, filepath):
        print('[LIB_BLK] <WRITE> BLK_FILE ' + str(self.version) + '\t(' + filepath + ')')

        if len(self.object) > 0:
            file = open(filepath, 'wb')
            self.write_to_stream(file, 0)
            file.close()
