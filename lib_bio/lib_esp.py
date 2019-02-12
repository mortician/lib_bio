########################################################################################################################
# LIB_ESP - EFFECT SPRITE DATA
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

#**********************************************************************************************************************
# TO DO:     fix write to stream and write function to import data from folder...
#**********************************************************************************************************************
class esp_header:
    def __init__(self, version):
        self.version = version

        self.object = [] #byte[]; holding id of sprite to use
    
    def read(self, file):
        self.object = []

        if self.version == 1.0 or self.version == 1.5 or self.version == 2.0:
            for i in range(8):
                self.object.append(int(struct.unpack("B", file.read(1))[0]))
            
            return self

        if self.version == 3.0:
            for i in range(16):
                self.object.append(int(struct.unpack("B", file.read(1))[0]))

            return self

    def write(self, file):
        for i in range(len(self.object)):
            file.write(struct.pack('B', int(self.object[i])))

class esp_data:
    def __init__(self, version):
        self.version = version

        self.header = esp_header(self.version)
        self.object = []
        self.offset = []

    def read_from_stream(self, file, o_esp, o_eff):
        file.seek(o_esp)
        print('[LIB_ESP] <READ> ESP_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')

        self.header = self.header.read(file)
        count = 0

        for i in range(len(self.header.object)):
            if self.header.object[i] != 255:
                count += 1

        file.seek(o_eff)

        for i in range(len(self.header.object)):
            self.offset.append(int(struct.unpack("l", file.read(4))[0]))
            file.seek(-8, 1)
        
        if self.version == 1.0:
            file.seek(self.offset[0])
        else:
            file.seek(o_esp + self.offset[0])

        for i in range(count):
            if i < count - 1:
                size = self.offset[i + 1] - self.offset[i]
            else:
                if self.version == 1.0:
                    size = (o_eff - (len(self.header.object) - 1) * 4) - (self.offset[i])
                else:
                    size = (o_eff - (len(self.header.object) - 1) * 4) - (o_esp + self.offset[i])

            self.object.append(file.read(size))
           
        return self

    def read_from_folder(self, folder):

        return self

    def write_to_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_ESP] <WRITE> ESP_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')

        file.write(struct.pack('H', int(self.ceiling_x)))

        for i in range(len(self.object)):
            self.object[i].write(file)

        file.write(struct.pack('L', int((len(self.object) * 12) + 24)))

    def write_to_folder(self, folder):
        #print('[LIB_ESP] <WRITE> ESP_HEADER ' + str(self.version) + '\t(' + folder.upper() + 'ESP.BIN' + ')')
        file = open(folder + 'ESP.BIN', 'wb')
        
        for i in range(len(self.header.object)):
            file.write(struct.pack('B', int(self.header.object[i])))
        file.close()

        for i in range(len(self.object)):
            print('[LIB_ESP] <WRITE> ESP_FILE ' + str(self.version) + '\t(' + (folder + 'ESP_' + hex(self.header.object[i])[2:].zfill(2)).upper() + '.EFF' + ')')
            file = open((folder + 'ESP_' + hex(self.header.object[i])[2:].zfill(2)).upper() + '.EFF', 'wb')
            file.write(self.object[i])
            file.close()