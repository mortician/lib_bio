########################################################################################################################
# LIB_LIT - LIGHT DATA
########################################################################################################################
# SUPPORTED:
#               BIO HAZARD
#               BIOHAZARD 2 PROTOTYPE (NOV/1996)
#               BIOHAZARD 2
#               !!!BIOHAZARD 3: LAST ESCAPE      MISSING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct
import os

class lit_rgb_color:
    def __init__(self):
        self.r = 0 #byte; red value
        self.g = 0 #byte; green value
        self.b = 0 #byte; blue value

    def read(self, file):
        self.r = int(struct.unpack("B", file.read(1))[0])
        self.g = int(struct.unpack("B", file.read(1))[0])
        self.b = int(struct.unpack("B", file.read(1))[0])
        return self

    def write(self, file):
        file.write(struct.pack('B', int(self.r)))
        file.write(struct.pack('B', int(self.g)))
        file.write(struct.pack('B', int(self.b)))

class lit_position:
    def __init__(self):
        self.x = 0 #var, depends on .rdt version...
        self.y = 0 #var, depends on .rdt version...
        self.z = 0 #var, depends on .rdt version...

    def read_long(self, file):
        self.x = int(struct.unpack("l", file.read(4))[0])
        self.y = int(struct.unpack("l", file.read(4))[0])
        self.z = int(struct.unpack("l", file.read(4))[0])
        return self

    def read_short(self, file):
        self.x = int(struct.unpack("h", file.read(2))[0])
        self.y = int(struct.unpack("h", file.read(2))[0])
        self.z = int(struct.unpack("h", file.read(2))[0])
        return self

    def write_long(self, file):
        file.write(struct.pack('l', int(self.x)))
        file.write(struct.pack('l', int(self.y)))
        file.write(struct.pack('l', int(self.z)))

    def write_short(self, file):
        file.write(struct.pack('h', int(self.x)))
        file.write(struct.pack('h', int(self.y)))
        file.write(struct.pack('h', int(self.z)))

class lit_object:
    def __init__(self, version):
        self.version = version

        if self.version == 1.0:
            self.position = lit_position()
            self.color = lit_rgb_color()
            self.mode = 0       #uint16;
            self.dummy = 0      #byte;
            self.luminosity = 0 #uint16; valid range = 0-65536
        
        if self.version == 1.5 or self.version == 2.0:
            self.type = 0                  #uint16;
            self.mode = 0                  #uint16;
            self.color = []                #lit_rgb_color[3];
            self.ambient = lit_rgb_color() #lit_rgb_color;
            self.position = []             #lit_position[3];
            self.luminosity = []           #uint16[3];

    def read(self, file):
        if self.version == 1.0:
            self.position = self.position.read_long(file)
            self.color = self.color.read(file)
            self.mode = int(struct.unpack("H", file.read(2))[0])
            self.dummy = int(struct.unpack("B", file.read(1))[0])
            self.luminosity = int(struct.unpack("H", file.read(2))[0])
            return self

        if self.version == 1.5 or self.version == 2.0:
            self.type = int(struct.unpack("H", file.read(2))[0])
            self.mode = int(struct.unpack("H", file.read(2))[0])

            for i in range(3):
                tmp_color = lit_rgb_color()
                tmp_color = tmp_color.read(file)
                self.color.append(tmp_color)

            self.ambient = self.ambient.read(file)

            for i in range(3):
                tmp_position = lit_position()
                tmp_position = tmp_position.read_short(file)
                self.position.append(tmp_position)

            for i in range(3):
                self.luminosity.append(int(struct.unpack("H", file.read(2))[0]))

            return self

    def write(self, file):
        if self.version == 1.0:
            self.position.write_long(file)
            self.color.write(file)
            file.write(struct.pack('H', int(self.mode)))
            file.write(struct.pack('B', int(self.dummy)))
            file.write(struct.pack('H', int(self.luminosity)))

        if self.version == 1.5 or self.version == 2.0:
            file.write(struct.pack('H', int(self.type)))
            file.write(struct.pack('H', int(self.mode)))

            for i in range(len(self.color)):
                self.color[i].write(file)
        
            self.ambient.write(file)

            for i in range(len(self.position)):
                self.position[i].write_short(file)

            for i in range(len(self.luminosity)):
                file.write(struct.pack('H', int(self.luminosity[i])))

class lit_file:
    def __init__(self, version):
        self.version = version

        if self.version == 1.0:
            self.ambient = [] #uint16[3]; valid range = 0-4096
            self.object = []  #lit_object[3];

        if self.version == 1.5 or self.version == 2.0:
            self.object = [] #lit_object[rdt_header.h_cut];

    def read_from_stream(self, file, offset, count):
        file.seek(offset)
        print('[LIB_LIT] <READ> LIT_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')

        if self.version == 1.0:
            self.ambient = []
            self.object = []

            for i in range(3):
                self.ambient.append(int(struct.unpack("H", file.read(2))[0]))

        for i in range(count):
            tmp_obj = lit_object(self.version)
            tmp_obj = tmp_obj.read(file)
            self.object.append(tmp_obj)

        return self

    def read_from_file(self, filepath):
        print('[LIB_LIT] <READ> LIT_FILE ' + str(self.version) + '\t(' + filepath.upper() + ')')
        tmp_count = 0

        if self.version == 1.0:
            if os.path.getsize(filepath) == 66:
                tmp_count = 3

        if self.version == 1.5 or self.version == 2.0:
            tmp_count = int(os.path.getsize(filepath) / 40)

        if tmp_count > 0:
            file = open(filepath, 'rb')
            self.read_from_stream(file, 0, tmp_count)
            file.close()

        return self

    def write_to_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_LIT] <WRITE> LIT_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')
        
        if self.version == 1.0:
            for i in range(len(self.ambient)):
                file.write(struct.pack('H', int(self.ambient[i])))

        for i in range(len(self.object)):
            self.object[i].write(file)

    def write_to_file(self, filepath):
        print('[LIB_LIT] <WRITE> LIT_FILE ' + str(self.version) + '\t(' + filepath.upper() + ')')

        file = open(filepath, 'wb')
        self.write_to_stream(file, 0)
        file.close()
