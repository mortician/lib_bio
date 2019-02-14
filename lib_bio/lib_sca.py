########################################################################################################################
# LIB_SCA - COLLISION DATA
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

class sca_object:
    def __init__(self, version):
        self.version = version

        if self.version == 1.0:
            self.x1 = 0    #uint16;		//X1 coordinate
            self.z1 = 0    #uint16;		//Y1 coordinate
            self.x2 = 0    #uint16;		//X2 coordinate
            self.z2 = 0    #uint16;		//Y2 coordinate
            self.type = 0  #byte;		//Shape ID	(0 = Unassigned?; 1 = Standard cube/rectangle; 3 = Circle/cylinder; 4 = ?; 5 = ?)
            self.u0 = 0    #byte;		//Additional flags, has to be treated as bit flag array
            self.u1 = 0    #byte;		//Additional flags, has to be treated as bit flag array
            self.floor = 0 #byte;		//nFloor?

        if self.version == 1.5:
            self.width = 0   #uint16;	//Width on x axis
            self.density = 0 #uint16;	//Density on z axis
            self.x = 0       #int16;	//X coordinate
            self.z = 0       #int16;	//Y coordinate
            self.type = 0    #byte;		//Shape ID	(0 = Unassigned?; 1 = Standard cube/rectangle; 3 = Circle/cylinder; 4 = ?; 5 = ?)
            self.u0 = 0      #byte;		//Additional flags, has to be treated as bit flag array
            self.u1 = 0      #byte;		//Additional flags, has to be treated as bit flag array
            self.floor = 0   #byte;		//nFloor?

        if self.version == 2.0:
            self.x = 0       #int16;
            self.z = 0       #int16;
            self.width = 0   #uint16;
            self.density = 0 #uint16;
            self.id = 0      #uint16;
            self.type = 0    #uint16;
            self.floor = 0   #uint32;

        if self.version == 3.0:
            self.x1 = 0    #int16;
            self.z1 = 0    #int16;
            self.x2 = 0    #int16;
            self.z2 = 0    #int16;
            self.type = 0  #byte; not sure!
            self.u0 = 0    #byte; ?
            self.u1 = 0    #byte; ?
            self.u2 = 0    #byte; ?
            self.u3 = 0    #byte; ?
            self.u4 = 0    #byte; ?
            self.floor = 0 #int16;

    def read(self, file):
        if self.version == 1.0:
            self.x1 = int(struct.unpack("H", file.read(2))[0])
            self.z1 = int(struct.unpack("H", file.read(2))[0])
            self.x2 = int(struct.unpack("H", file.read(2))[0])
            self.z2 = int(struct.unpack("H", file.read(2))[0])
            self.type = int(struct.unpack("B", file.read(1))[0])
            self.u0 = int(struct.unpack("B", file.read(1))[0])
            self.u1 = int(struct.unpack("B", file.read(1))[0])
            self.floor = int(struct.unpack("B", file.read(1))[0])
            return self

        if self.version == 1.5:
            self.width = int(struct.unpack("H", file.read(2))[0])
            self.density = int(struct.unpack("H", file.read(2))[0])
            self.x = int(struct.unpack("h", file.read(2))[0])
            self.z = int(struct.unpack("h", file.read(2))[0])
            self.type = int(struct.unpack("B", file.read(1))[0])
            self.u0 = int(struct.unpack("B", file.read(1))[0])
            self.u1 = int(struct.unpack("B", file.read(1))[0])
            self.floor = int(struct.unpack("B", file.read(1))[0])
            return self

        if self.version == 2.0:
            self.x = int(struct.unpack("h", file.read(2))[0])
            self.z = int(struct.unpack("h", file.read(2))[0])
            self.width = int(struct.unpack("H", file.read(2))[0])
            self.density = int(struct.unpack("H", file.read(2))[0])
            self.id = int(struct.unpack("H", file.read(2))[0])
            self.type = int(struct.unpack("H", file.read(2))[0])
            self.floor = int(struct.unpack("L", file.read(4))[0])
            return self

        if self.version == 3.0:
            self.x1 = int(struct.unpack("h", file.read(2))[0])
            self.z1 = int(struct.unpack("h", file.read(2))[0])
            self.x2 = int(struct.unpack("h", file.read(2))[0])
            self.z2 = int(struct.unpack("h", file.read(2))[0])
            self.id = int(struct.unpack("H", file.read(2))[0])
            self.type = int(struct.unpack("H", file.read(2))[0])
            self.u0 = int(struct.unpack("B", file.read(1))[0])
            self.u1 = int(struct.unpack("B", file.read(1))[0])
            self.floor = int(struct.unpack("h", file.read(2))[0])
            return self

    def write(self, file):
        if self.version == 1.0:
            file.write(struct.pack('H', int(self.x1)))
            file.write(struct.pack('H', int(self.z1)))
            file.write(struct.pack('H', int(self.x2)))
            file.write(struct.pack('H', int(self.z2)))
            file.write(struct.pack('B', int(self.type)))
            file.write(struct.pack('B', int(self.u0)))
            file.write(struct.pack('B', int(self.u1)))
            file.write(struct.pack('B', int(self.floor)))

        if self.version == 1.5:
            file.write(struct.pack('H', int(self.width)))
            file.write(struct.pack('H', int(self.density)))
            file.write(struct.pack('h', int(self.x)))
            file.write(struct.pack('h', int(self.z)))
            file.write(struct.pack('B', int(self.type)))
            file.write(struct.pack('B', int(self.u0)))
            file.write(struct.pack('B', int(self.u1)))
            file.write(struct.pack('B', int(self.floor)))

        if self.version == 2.0:
            file.write(struct.pack('h', int(self.x)))
            file.write(struct.pack('h', int(self.z)))
            file.write(struct.pack('H', int(self.width)))
            file.write(struct.pack('H', int(self.density)))
            file.write(struct.pack('H', int(self.id)))
            file.write(struct.pack('H', int(self.type)))
            file.write(struct.pack('L', int(self.floor)))

        if self.version == 3.0:
            file.write(struct.pack('h', int(self.x1)))
            file.write(struct.pack('h', int(self.z1)))
            file.write(struct.pack('h', int(self.x2)))
            file.write(struct.pack('h', int(self.z2)))
            file.write(struct.pack('H', int(self.id)))
            file.write(struct.pack('H', int(self.type)))
            file.write(struct.pack('B', int(self.u0)))
            file.write(struct.pack('B', int(self.u1)))
            file.write(struct.pack('h', int(self.floor)))

class sca_file:
    def __init__(self, version):
        self.version = version

        if self.version == 1.0 or self.version == 1.5:
            self.ceiling_x = 0 #uint16;
            self.ceiling_z = 0 #uint16;
            self.count = []    #uint32[5];
            self.object = []   #sca_object[];

        if self.version == 2.0:
            self.ceiling_x = 0       #int16;
            self.ceiling_z = 0       #int16;
            self.count = 0           #uint32;
            self.ceiling_y = 0       #int32;
            self.ceiling_width = 0   #uint16;
            self.ceiling_density = 0 #uint16;
            self.object = []         #sca_object[self.count - 1];

        if self.version == 3.0:
            self.count = 0      #uint32;
            self.ceiling_x1 = 0 #int16;
            self.ceiling_z1 = 0 #int16
            self.ceiling_x2 = 0 #int16;
            self.ceiling_z2 = 0 #int16;
            self.unknown = 0    #uint32; not sure!
            self.object = []    #sca_object[self.count - 1];

    def read_from_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_SCA] <READ> SCA_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')
        self.object = []

        tmp_count = 0

        if self.version == 1.0 or self.version == 1.5:
            self.ceiling_x = int(struct.unpack("H", file.read(2))[0])
            self.ceiling_z = int(struct.unpack("H", file.read(2))[0])
        
            for i in range(5):
                self.count.append(int(struct.unpack("L", file.read(4))[0]))
                tmp_count += self.count[i]
            
        if self.version == 2.0:
            self.ceiling_x = int(struct.unpack("h", file.read(2))[0])
            self.ceiling_z = int(struct.unpack("h", file.read(2))[0])
            self.count = int(struct.unpack("L", file.read(4))[0])
            self.ceiling_y = int(struct.unpack("l", file.read(4))[0])
            self.ceiling_width = int(struct.unpack("H", file.read(2))[0])
            self.ceiling_density = int(struct.unpack("H", file.read(2))[0])
        
            tmp_count = self.count - 1

        if self.version == 3.0:
            self.count = int(struct.unpack("L", file.read(4))[0])
            self.ceiling_x1 = int(struct.unpack("h", file.read(2))[0])
            self.ceiling_z1 = int(struct.unpack("h", file.read(2))[0])
            self.ceiling_x2 = int(struct.unpack("h", file.read(2))[0])
            self.ceiling_z2 = int(struct.unpack("h", file.read(2))[0])
            self.unknown = int(struct.unpack("L", file.read(4))[0])
            
            tmp_count = self.count - 1

        for j in range(tmp_count):
            tmp_obj = sca_object(self.version)
            tmp_obj = tmp_obj.read(file)
            self.object.append(tmp_obj)
            
        return self
   
    def read_from_file(self, filepath):
        print('[LIB_SCA] <READ> SCA_FILE ' + str(self.version) + '\t(' + filepath.upper() + ')')
        
        file = open(filepath, 'rb')
        self.read_from_stream(file, 0)
        file.close()

        return self

    def write_to_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_SCA] <WRITE> SCA_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')

        if self.version == 1.0 or self.version == 1.5:
            file.write(struct.pack('H', int(self.ceiling_x)))
            file.write(struct.pack('H', int(self.ceiling_z)))
            file.write(struct.pack('L', int(self.count[0])))
            file.write(struct.pack('L', int(self.count[1])))
            file.write(struct.pack('L', int(self.count[2])))
            file.write(struct.pack('L', int(self.count[3])))
            file.write(struct.pack('L', int(self.count[4])))
        
        if self.version == 2.0:
            file.write(struct.pack('h', int(self.ceiling_x)))
            file.write(struct.pack('h', int(self.ceiling_z)))
            file.write(struct.pack('L', int(self.count)))
            file.write(struct.pack('l', int(self.ceiling_y)))
            file.write(struct.pack('H', int(self.ceiling_width)))
            file.write(struct.pack('H', int(self.ceiling_density)))

        if self.version == 3.0:
            file.write(struct.pack('L', int(self.count)))
            file.write(struct.pack('h', int(self.ceiling_x1)))
            file.write(struct.pack('h', int(self.ceiling_z1)))
            file.write(struct.pack('h', int(self.ceiling_x2)))
            file.write(struct.pack('h', int(self.ceiling_z2)))
            file.write(struct.pack('L', int(self.unknown)))

        for i in range(len(self.object)):
            self.object[i].write(file)
        
        if self.version == 1.0 or self.version == 1.5:
            file.write(struct.pack('L', int((len(self.object) * 12) + 24)))

    def write_to_file(self, filepath):
        print('[LIB_SCA] <WRITE> SCA_FILE ' + str(self.version) + '\t(' + filepath.upper() + ')')

        file = open(filepath, 'wb')
        self.write_to_stream(file, 0)
        file.close()

