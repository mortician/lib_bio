########################################################################################################################
# LIB_RVD - CAMERA SWITCH DATA
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
import os

class rvd_object:
    def __init__(self, version):
        self.version = version
        
        if self.version == 1.0:
            self.cam_1 = 0 #uint16; id of target camera, a value of 9 means it's the far/near visible area of the cam
            self.cam_0 = 0 #uint16; id of source camera
            self.x1 = 0    #uint16;
            self.z1 = 0    #uint16;
            self.x2 = 0    #uint16; 
            self.z2 = 0    #uint16;
            self.x3 = 0    #uint16; 
            self.z3 = 0    #uint16;
            self.x4 = 0    #uint16;
            self.z4 = 0    #uint16;

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            self.flag = 0  #byte; 
            self.floor = 0 #byte; 
            self.cam_0 = 0 #byte; 
            self.cam_1 = 0 #byte; 
            self.x1 = 0    #int16; 
            self.z1 = 0    #int16;
            self.x2 = 0    #int16; 
            self.z2 = 0    #int16;
            self.x3 = 0    #int16; 
            self.z3 = 0    #int16;
            self.x4 = 0    #int16; 
            self.z4 = 0    #int16;

    def read(self, file):
        #print('[LIB_RVD] <READ> RVD_OBJECT ' + str(self.version) + '\t(' + str(file.tell()) + ')')
        if self.version == 1.0:
            self.cam_1 = int(struct.unpack("H", file.read(2))[0])
            self.cam_0 = int(struct.unpack("H", file.read(2))[0])
            self.x1 = int(struct.unpack("H", file.read(2))[0])
            self.z1 = int(struct.unpack("H", file.read(2))[0])
            self.x2 = int(struct.unpack("H", file.read(2))[0])
            self.z2 = int(struct.unpack("H", file.read(2))[0])
            self.x3 = int(struct.unpack("H", file.read(2))[0])
            self.z3 = int(struct.unpack("H", file.read(2))[0])
            self.x4 = int(struct.unpack("H", file.read(2))[0])
            self.z4 = int(struct.unpack("H", file.read(2))[0])

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            self.flag = int(struct.unpack("B", file.read(1))[0])
            self.floor = int(struct.unpack("B", file.read(1))[0])
            self.cam_0 = int(struct.unpack("B", file.read(1))[0])
            self.cam_1 = int(struct.unpack("B", file.read(1))[0])
            self.x1 = int(struct.unpack("h", file.read(2))[0])
            self.z1 = int(struct.unpack("h", file.read(2))[0])
            self.x2 = int(struct.unpack("h", file.read(2))[0])
            self.z2 = int(struct.unpack("h", file.read(2))[0])
            self.x3 = int(struct.unpack("h", file.read(2))[0])
            self.z3 = int(struct.unpack("h", file.read(2))[0])
            self.x4 = int(struct.unpack("h", file.read(2))[0])
            self.z4 = int(struct.unpack("h", file.read(2))[0])
        
        return self

    def write(self, file):
        #print('[LIB_RVD] <WRITE> RVD_OBJECT ' + str(self.version) + '\t(' + str(file.tell()) + ')')
        if self.version == 1.0:
            file.write(struct.pack('H', int(self.cam_1)))
            file.write(struct.pack('H', int(self.cam_0)))
            file.write(struct.pack('H', int(self.x1)))
            file.write(struct.pack('H', int(self.z1)))
            file.write(struct.pack('H', int(self.x2)))
            file.write(struct.pack('H', int(self.z2)))
            file.write(struct.pack('H', int(self.x3)))
            file.write(struct.pack('H', int(self.z3)))
            file.write(struct.pack('H', int(self.x4)))
            file.write(struct.pack('H', int(self.z4)))

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            file.write(struct.pack('B', int(self.flag)))
            file.write(struct.pack('B', int(self.floor)))
            file.write(struct.pack('B', int(self.cam_0)))
            file.write(struct.pack('B', int(self.cam_1)))
            file.write(struct.pack('h', int(self.x1)))
            file.write(struct.pack('h', int(self.z1)))
            file.write(struct.pack('h', int(self.x2)))
            file.write(struct.pack('h', int(self.z2)))
            file.write(struct.pack('h', int(self.x3)))
            file.write(struct.pack('h', int(self.z3)))
            file.write(struct.pack('h', int(self.x4)))
            file.write(struct.pack('h', int(self.z4)))

class rvd_file:
    def __init__(self, version):
        self.version = version
        self.object = []
        
    def read_from_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_RVD] <READ> RVD_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')
        self.object = []
        terminator = 0
        count = 0

        if self.version == 1.0:
            while terminator != 65535:
                try:
                    tmp_obj = rvd_object(self.version)
                    tmp_obj = tmp_obj.read(file)
                    terminator = tmp_obj.cam_1

                    if terminator != 65535:
                        count += 1
                        self.object.append(tmp_obj)

                except:
                    if offset == 0:
                        file.close()
                    break

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            while terminator != 65535:
                try:
                    tmp_obj = rvd_object(self.version)
                    tmp_obj = tmp_obj.read(file)

                    if tmp_obj.cam_0 == 255 and tmp_obj.cam_1 == 255 and tmp_obj.floor == 255 and tmp_obj.flag == 255:
                        break
                    
                    self.object.append(tmp_obj)

                except:
                    if offset == 0:
                        file.close()
                    break
        return self

    def read_from_file(self, filepath):
        print('[LIB_RVD] <READ> RVD_FILE ' + str(self.version) + '\t(' + filepath + ')')

        file = open(filepath, 'rb')
        self.read_from_stream(file, 0)
        file.close()
        
        return self

    def write_to_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_RVD] <WRITE> RVD_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')

        for i in range(len(self.object)):
            self.object[i].write(file)

        file.write(struct.pack('l', int(-1)))

    def write_to_file(self, filepath):
        print('[LIB_RVD] <WRITE> RVD_FILE ' + str(self.version) + '\t(' + filepath + ')')

        file = open(filepath, 'wb')
        self.write_to_stream(file, 0)
        file.close()
