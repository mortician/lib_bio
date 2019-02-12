########################################################################################################################
# LIB_SND - SOUND ATTRIBUTE TABLE DATA
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

#=======================================================================================================================
# GENERIC
#=======================================================================================================================
class snd_object:
    def __init__(self):
        self.id = 0   #byte; "id check"
        self.pan = 0  #byte; "pan programming"
        self.tone = 0 #byte; "tone"
        self.mono = 0 #byte; "monopoly"

    def read(self, file):
        self.id = int(struct.unpack("B", file.read(1))[0])
        self.pan = int(struct.unpack("B", file.read(1))[0])
        self.tone = int(struct.unpack("B", file.read(1))[0])
        self.mono = int(struct.unpack("B", file.read(1))[0])
        return self

    def write(self, file):
        file.write(struct.pack('B', int(self.id)))
        file.write(struct.pack('B', int(self.pan)))
        file.write(struct.pack('B', int(self.tone)))
        file.write(struct.pack('B', int(self.mono)))

class snd_file:
    def __init__(self):
        self.object = [] #snd_object[];

    def read(self, file, offset, count):
        file.seek(offset)
        print('[LIB_SND] <READ> SND_FILE\t(' + str(file.tell()) + ')')

        self.object = []

        for i in range(count):
            tmp_obj = snd_object()
            tmp_obj = tmp_obj.read(file)
            self.object.append(tmp_obj)

        return self

    def write(self, file, offset):
        file.seek(offset)
        print('[LIB_SND] <WRITE> SND_FILE\t(' + str(offset) + ')')
        
        for i in range(len(self.object)):
            self.object[i].write(file)

    def extract(self, filepath):
        print('[LIB_SND] <EXTRACT> SND_FILE\t(' + filepath + ')')

        file = open(filepath, 'wb')
        self.write(file, 0)
        file.close()

