########################################################################################################################
# LIB_FLR - FLOOR STEP SOUND AREAS
########################################################################################################################
# SUPPORTED:
#               BIO HAZARD
#               BIOHAZARD 2 PROTOTYPE (NOV/1996)
#               BIOHAZARD 2
#               BIOHAZARD 3: LAST ESCAPE
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct

class flr_object:
    def __init__(self, version):
        self.version = version

        if self.version == 1.0:
            self.x = 0       #uint16;
            self.z = 0       #uint16;
            self.width = 0   #uint16;
            self.density = 0 #uint16;
            self.sound = 0   #uint16;

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            self.x = 0       #int16;
            self.z = 0       #int16;
            self.width = 0   #uint16;
            self.density = 0 #uint16;
            self.sound = 0   #uint16;
            self.flag = 0    #uint16;

    def read(self, file):
        if self.version == 1.0:
            self.x = int(struct.unpack("H", file.read(2))[0])
            self.z = int(struct.unpack("H", file.read(2))[0])
            self.width = int(struct.unpack("H", file.read(2))[0])
            self.density = int(struct.unpack("H", file.read(2))[0])
            self.sound = int(struct.unpack("H", file.read(2))[0])
            return self

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            self.x = int(struct.unpack("h", file.read(2))[0])
            self.z = int(struct.unpack("h", file.read(2))[0])
            self.width = int(struct.unpack("H", file.read(2))[0])
            self.density = int(struct.unpack("H", file.read(2))[0])
            self.sound = int(struct.unpack("H", file.read(2))[0])
            self.flag = int(struct.unpack("H", file.read(2))[0])
            return self

    def write(self, file):
        if self.version == 1.0:
            file.write(struct.pack('H', int(self.x)))
            file.write(struct.pack('H', int(self.z)))
            file.write(struct.pack('H', int(self.width)))
            file.write(struct.pack('H', int(self.density)))
            file.write(struct.pack('H', int(self.sound)))

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            file.write(struct.pack('h', int(self.x)))
            file.write(struct.pack('h', int(self.z)))
            file.write(struct.pack('H', int(self.width)))
            file.write(struct.pack('H', int(self.density)))
            file.write(struct.pack('H', int(self.sound)))
            file.write(struct.pack('H', int(self.flag)))

class flr_file:
    def __init__(self, version):
        self.version = version

        if self.version == 1.0:
            self.amount = 0  #uint16; total amount of objects
            self.object = [] #flr_object[self.amount]

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            self.amount = 0  #uint16; total amount of objects
            self.object = [] #flr_object[self.amount]
            self.dummy = 0   #uint16; ?

    def read_from_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_FLR] <READ> FLR_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')
        
        self.amount = int(struct.unpack("H", file.read(2))[0])
        self.object = []

        for i in range(self.amount):
            tmp_obj = flr_object(self.version)
            tmp_obj = tmp_obj.read(file)
            self.object.append(tmp_obj)
        
        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            self.dummy = int(struct.unpack("H", file.read(2))[0])

        return self

    def read_from_file(self, filepath):
        print('[LIB_FLR] <READ> FLR_FILE ' + str(self.version) + '\t(' + filepath.upper() + ')')

        file = open(filepath, 'rb')
        self.read_from_stream(file, 0)
        file.close()

        return self

    def write_to_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_FLR] <WRITE> FLR_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')
        
        file.write(struct.pack('H', int(self.amount)))

        for i in range(len(self.object)):
            self.object[i].write(file)

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            file.write(struct.pack('H', int(self.dummy)))

    def write_to_file(self, filepath):
        print('[LIB_FLR] <WRITE> FLR_FILE ' + str(self.version) + '\t(' + filepath.upper() + ')')

        file = open(filepath, 'wb')
        self.write_to_stream(file, 0)
        file.close()
