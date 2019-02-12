########################################################################################################################
# LIB_RBJ - ANIMATION DATA
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

class edd_header_object:
    def __init__(self):
        self.count = 0  #uint16;
        self.offset = 0 #uint16;

    def read(self, file):
        self.count = int(struct.unpack("H", file.read(2))[0])
        self.offset = int(struct.unpack("H", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('H', int(self.count)))
        file.write(struct.pack('H', int(self.offset)))

class edd_header:
    def __init__(self):
        self.object = [] #edd_header_object[]; 

    def read(self, file):
        file.seek(2, 1)
        count = int(struct.unpack("H", file.read(2))[0] / 4)
        file.seek(-4, 1)

        for i in range(count):
            tmp_obj = edd_header_object()
            tmp_obj = tmp_obj.read(file)
            self.object.append(tmp_obj)
        
        return self

    def write(self, file):
        for i in range(len(self.object)):
            self.object[i].write(file)

class edd_table_object:
    def __init__(self):
        self.frame = 0  #byte;
        self.frame0 = 0 #byte;
        self.flags = 0  #byte;
        self.flags0 = 0 #byte;

    def read(self, file):
        self.frame = int(struct.unpack("B", file.read(1))[0])
        self.frame0 = int(struct.unpack("B", file.read(1))[0])
        self.flags = int(struct.unpack("B", file.read(1))[0])
        self.flags0 = int(struct.unpack("B", file.read(1))[0])
        return self

    def write(self, file):
        file.write(struct.pack('B', int(self.frame)))
        file.write(struct.pack('B', int(self.frame0)))
        file.write(struct.pack('B', int(self.flags)))
        file.write(struct.pack('B', int(self.flags0)))

class edd_table:
    def __init__(self):
        self.object = [] #edd_table_object[]

    def read(self, file, count):
        for i in range(count):
            tmp_obj = edd_table_object()
            tmp_obj = tmp_obj.read(file)
            self.object.append(tmp_obj)

        return self

    def write(self, file):
        for i in range(len(self.object)):
            self.object[i].write(file)

class edd_file:
    def __init__(self):
        self.header = edd_header()
        self.object = []
        self.size = 0 #uint32; total size of file
        self.frame_count = 0 #custom value, to keep track of total frame count
    
    def read_from_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_RBJ] <READ> EDD_DATA\t(' + str(file.tell()) + ')')

        self.header = self.header.read(file)      
        self.frame_count = 0

        for i in range(len(self.header.object)):
            tmp_obj = edd_table()
            tmp_obj = tmp_obj.read(file, self.header.object[i].count)
            self.object.append(tmp_obj)

            for j in range(len(tmp_obj.object)):
                if tmp_obj.object[j].frame > self.frame_count:
                    self.frame_count = tmp_obj.object[j].frame

        self.size = int(struct.unpack("L", file.read(4))[0])
        self.frame_count += 1
        return self

    def read_from_file(self, filepath):
        print('[LIB_RBJ] <READ> EDD_FILE\t(' + filepath + ')')

        file = open(filepath, 'rb')
        self.read_from_stream(file, 0)
        file.close()

        return self

    def write_to_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_RBJ] <WRITE> EDD_DATA\t(' + str(file.tell()) + ')')

        self.header.write(file)
        
        for i in range(len(self.header.object)):
            self.object[i].write(file)

        file.write(struct.pack('L', int(self.size)))

    def write_to_file(self, filepath):
        print('[LIB_RBJ] <WRITE> EDD_FILE\t(' + filepath + ')')

        file = open(filepath, 'wb')
        self.write_to_stream(file, 0)
        file.close()

class emr_header:
    def __init__(self):
        self.o_armatures = 0 #uint16; 
        self.o_frames = 0    #uint16; 
        self.count = 0       #uint16; 
        self.size = 0        #uint16; 
        
    def read(self, file):
        self.o_armatures = int(struct.unpack("H", file.read(2))[0])
        self.o_frames =  int(struct.unpack("H", file.read(2))[0])
        self.count = int(struct.unpack("H", file.read(2))[0])
        self.size = int(struct.unpack("H", file.read(2))[0])

        #some .rbj files in rooms use this...
        if self.o_armatures < 8 and self.o_frames == 0:
            file.seek(-4, 1)
            self.o_armatures = int(struct.unpack("H", file.read(2))[0])
            self.o_frames =  int(struct.unpack("H", file.read(2))[0])
            self.count = int(struct.unpack("H", file.read(2))[0])
            self.size = int(struct.unpack("H", file.read(2))[0])

        return self

    def write(self, file):
        file.write(struct.pack('H', int(self.o_armatures)))
        file.write(struct.pack('H', int(self.o_frames)))
        file.write(struct.pack('H', int(self.count)))
        file.write(struct.pack('H', int(self.size)))

class emr_armature:
    def __init__(self):
        self.count = 0  #uint16; 
        self.offset = 0 #uint16; 
        self.children = []

    def read(self, file):
        self.count = int(struct.unpack("H", file.read(2))[0])
        self.offset = int(struct.unpack("H", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('H', int(self.count)))
        file.write(struct.pack('H', int(self.offset)))

class emr_relative_position:
    def __init__(self):
        self.x = 0 #int16
        self.y = 0 #int16
        self.z = 0 #int16

    def read(self, file):
        self.x = int(struct.unpack("h", file.read(2))[0])
        self.y = int(struct.unpack("h", file.read(2))[0])
        self.z = int(struct.unpack("h", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('h', int(self.x)))
        file.write(struct.pack('h', int(self.y)))
        file.write(struct.pack('h', int(self.z)))

class emr_frame:
    def __init__(self):
        self.x_offset = 0 #int16
        self.y_offset = 0 #int16
        self.z_offset = 0 #int16
        self.x_speed = 0  #uint16
        self.y_speed = 0  #uint16
        self.z_speed = 0  #uint16
        self.angles = []   #emr_relative_position[mesh count]

    def read(self, file, mesh_count):
        self.x_offset = int(struct.unpack("h", file.read(2))[0])
        self.y_offset = int(struct.unpack("h", file.read(2))[0])
        self.z_offset = int(struct.unpack("h", file.read(2))[0])
        self.x_speed = int(struct.unpack("H", file.read(2))[0])
        self.y_speed = int(struct.unpack("H", file.read(2))[0])
        self.z_speed = int(struct.unpack("H", file.read(2))[0])

        for i in range(mesh_count):
            tmp_angle = emr_relative_position()
            tmp_angle = tmp_angle.read(file)
            self.angles.append(tmp_angle)

        return self

    def write(self, file):
        file.write(struct.pack('h', int(self.x_offset)))
        file.write(struct.pack('h', int(self.y_offset)))
        file.write(struct.pack('h', int(self.z_offset)))
        file.write(struct.pack('H', int(self.x_speed)))
        file.write(struct.pack('H', int(self.y_speed)))
        file.write(struct.pack('H', int(self.z_speed)))

        for i in range(len(self.angles)):
            self.angles[i].write(file)

class emr_file:
    def __init__(self, version):
        self.version = version

        self.header = emr_header()
        self.relative_position = [] #emr_relative_position[self.header.count]
        self.armature = []          #emr_armature array[self.header.count]
        self.mesh = []              #byte array[self.header.count]
        self.frame = []             #emr_frame array[]; count obtained by reading the related .edd file...

    def read_from_stream(self, file, offset, frames):
        file.seek(offset)
        print('[LIB_RBJ] <READ> EMR_FILE\t(' + str(file.tell()) + ')')
    
        self.header = self.header.read(file)
    
        for i in range(self.header.count):
            tmp_rel = emr_relative_position()
            tmp_rel = tmp_rel.read(file)
            self.relative_position.append(tmp_rel)

        file.seek(offset + self.header.o_armatures)

        for i in range(self.header.count):
            tmp_armature = emr_armature()
            tmp_armature = tmp_armature.read(file)
            self.armature.append(tmp_armature)

        for i in range(self.header.count):
            file.seek(offset + self.header.o_armatures + self.armature[i].offset)

            lst_bones = []

            for j in range(self.armature[i].count):
                self.armature[i].children.append(str(int(struct.unpack("B", file.read(1))[0])))

            print(self.armature[i].children)

        file.seek(offset + self.header.o_armatures + self.armature[0].offset)

        for i in range(self.header.count):
            self.mesh.append(int(struct.unpack("B", file.read(1))[0]))
        
        print('Mesh_list: ' + str(self.mesh))

        o_dbg = 0

        for i in range(frames):
            file.seek(offset + self.header.o_frames + (i * self.header.size))
            
            tmp_frame = emr_frame()
            tmp_frame = tmp_frame.read(file, self.header.count)
            
            o_dbg = file.tell()
            self.frame.append(tmp_frame)
        
        file.seek(offset + self.header.o_frames + (len(self.frame) * self.header.size))
        return self

    def read_from_file(self, filepath, frames):
        print('[LIB_RBJ] <READ> EMR_FILE\t(' + filepath + ')')

        file = open(filepath, 'rb')
        self.read_from_stream(file, 0, frames)
        file.close()

        return self

    def write_to_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_RBJ] <WRITE> EMR_FILE\t(' + str(file.tell()) + ')')

        self.header.write(file)
        
        for i in range(self.header.count):
            self.relative_position[i].write(file)

        file.seek(offset + self.header.o_armatures)

        for i in range(self.header.count):
            self.armature[i].write(file)

        for i in range(self.header.count):
            file.write(struct.pack('B', int(self.mesh[i])))

        file.seek(offset + self.header.o_frames)

        pad_byte_count = self.header.size - (12 + self.header.count * 6)

        for i in range(len(self.frame)):
            self.frame[i].write(file)

            if pad_byte_count > 0:
                for j in range(pad_byte_count):
                    file.write(struct.pack('B', int(0)))
        
        if self.version == 1.0:
            file.write(struct.pack('L', int((self.header.o_frames - 8) + (len(self.frame) * self.header.size))))

    def write_to_file(self, filepath):
        if len(self.frame) > 0:
            print('[LIB_RBJ] <WRITE> EMR_FILE\t(' + filepath + ')')

            file = open(filepath, 'wb')
            self.write_to_stream(file, 0)
            file.close()


class rbj_file:
    def __init__(self, version):
        self.version = version

        self.emr = emr_file(self.version)
        self.edd = edd_file()

    def read(self, file, o_emr, o_edd):
        self.edd = self.edd.read_from_stream(file, o_edd)
        self.emr = self.emr.read_from_stream(file, o_emr, self.edd.frame_count)
        return self
















#=======================================================================================================================
# BIO HAZARD
#=======================================================================================================================

#=======================================================================================================================
# BIOHAZARD 1.5/2/3
#=======================================================================================================================

