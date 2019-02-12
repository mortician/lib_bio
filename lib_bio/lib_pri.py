########################################################################################################################
# LIB_PRI - CAMERA MASK SRPITE DATA
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
# BIO HAZARD
#=======================================================================================================================
class pri_header:
    def __init__(self, version):
        self.version = version

        if self.version == 1.0:
            self.offsets = 0 #uint32; total count of relative offsets. If no data is available it's 0
        
        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            self.offsets = 0 #uint16; total count of relative offsets.
                             #        if no data is available it's 65535, or -1 if read as signed int
            self.masks = 0   #uint16; total count of mask tiles.
                             #        if no data is available it's 65535, or -1 if read as signed int

    def read(self, file):
        if self.version == 1.0:
            self.offsets = int(struct.unpack("L", file.read(4))[0])
            return self
        
        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            self.offsets = int(struct.unpack("H", file.read(2))[0])
            self.masks = int(struct.unpack("H", file.read(2))[0])
            return self

    def write(self, file):
        if self.version == 1.0:
            file.write(struct.pack('L', int(self.offsets)))

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            file.write(struct.pack('H', int(self.offsets)))
            file.write(struct.pack('H', int(self.masks)))

class pri_relative_offset:
    def __init__(self):
        self.count = 0   #uint32; total count of masks using this relative offset
        self.unknown = 0 #uint32; ?
        self.x = 0       #int16; x-coordinate to draw the masks from/to on the screen, can be negative!
        self.y = 0       #int16; y-coordinate to draw the masks from/to on the screen, can be negative!

    def read(self, file):
        self.count = int(struct.unpack("H", file.read(2))[0])
        self.unknown = int(struct.unpack("H", file.read(2))[0])
        self.x = int(struct.unpack("h", file.read(2))[0])
        self.y = int(struct.unpack("h", file.read(2))[0])
        
        return self

    def write(self, file):
        file.write(struct.pack('H', int(self.count)))
        file.write(struct.pack('H', int(self.unknown)))
        file.write(struct.pack('h', int(self.x)))
        file.write(struct.pack('h', int(self.y)))

class pri_mask_square:
    def __init__(self, version):
        self.version = version

        if self.version == 1.0 or self.version == 1.5:
            self.src_x = 0 #byte; x-coordinate on source .tim image
            self.src_y = 0 #byte; x-coordinate on source .tim image
            self.x = 0     #byte; destination x-coordinate
            self.y = 0     #byte; destination y-coordinate
            self.z = 0     #uint16; destination z-coordinate (depth/z-buffer)
            self.dummy = 0 #byte; BIO HAZARD = 0xC0; BIOHAZARD 1.5 = 0x95
            self.width = 0 #byte; width of the mask tile, it's also the height since it's a square :P

        if self.version == 2.0 or self.version == 3.0:
            self.src_x = 0 #byte; x-coordinate on source .tim image
            self.src_y = 0 #byte; x-coordinate on source .tim image
            self.x = 0     #byte; destination x-coordinate
            self.y = 0     #byte; destination y-coordinate
            self.z = 0     #uint16; destination z-coordinate (depth/z-buffer)
            self.width = 0 #uint16; width of the mask tile, it's also the height since it's a square :P

    def read(self, file):
        if self.version == 1.0 or self.version == 1.5:
            self.src_x = int(struct.unpack("B", file.read(1))[0])
            self.src_y = int(struct.unpack("B", file.read(1))[0])
            self.x = int(struct.unpack("B", file.read(1))[0])
            self.y = int(struct.unpack("B", file.read(1))[0])
            self.z = int(struct.unpack("H", file.read(2))[0])
            self.dummy = int(struct.unpack("B", file.read(1))[0])
            self.width = int(struct.unpack("B", file.read(1))[0])
            return self

        if self.version == 2.0 or self.version == 3.0:
            self.src_x = int(struct.unpack("B", file.read(1))[0])
            self.src_y = int(struct.unpack("B", file.read(1))[0])
            self.x = int(struct.unpack("B", file.read(1))[0])
            self.y = int(struct.unpack("B", file.read(1))[0])
            self.z = int(struct.unpack("H", file.read(2))[0])
            self.width = int(struct.unpack("H", file.read(2))[0])
            return self

    def write(self, file):
        if self.version == 1.0 or self.version == 1.5:
            file.write(struct.pack('B', int(self.src_x)))
            file.write(struct.pack('B', int(self.src_y)))
            file.write(struct.pack('B', int(self.x)))
            file.write(struct.pack('B', int(self.y)))
            file.write(struct.pack('H', int(self.z)))
            file.write(struct.pack('B', int(self.dummy)))
            file.write(struct.pack('B', int(self.width)))

        if self.version == 2.0 or self.version == 3.0:
            file.write(struct.pack('B', int(self.src_x)))
            file.write(struct.pack('B', int(self.src_y)))
            file.write(struct.pack('B', int(self.x)))
            file.write(struct.pack('B', int(self.y)))
            file.write(struct.pack('H', int(self.z)))
            file.write(struct.pack('H', int(self.width)))

class pri_mask_rectangle:
    def __init__(self):
        self.src_x = 0  #byte; x-coordinate on source .tim image
        self.src_y = 0  #byte; x-coordinate on source .tim image
        self.x = 0      #byte; destination x-coordinate
        self.y = 0      #byte; destination y-coordinate
        self.z = 0      #uint16; destination z-coordinate (depth/z-buffer)
        self.dummy = 0  #uint16; 
        self.width = 0  #uint16; width of the mask tile
        self.height = 0 #uint16; height of the mask tile

    def read(self, file):
        self.src_x = int(struct.unpack("B", file.read(1))[0])
        self.src_y = int(struct.unpack("B", file.read(1))[0])
        self.x = int(struct.unpack("B", file.read(1))[0])
        self.y = int(struct.unpack("B", file.read(1))[0])
        self.z = int(struct.unpack("H", file.read(2))[0])
        self.dummy = int(struct.unpack("H", file.read(2))[0])
        self.width = int(struct.unpack("H", file.read(2))[0])
        self.height = int(struct.unpack("H", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('B', int(self.src_x)))
        file.write(struct.pack('B', int(self.src_y)))
        file.write(struct.pack('B', int(self.x)))
        file.write(struct.pack('B', int(self.y)))
        file.write(struct.pack('H', int(self.z)))
        file.write(struct.pack('H', int(self.dummy)))
        file.write(struct.pack('H', int(self.width)))
        file.write(struct.pack('H', int(self.height)))

class pri_file:
    def __init__(self, version):
        self.version = version

        self.header = pri_header(self.version)
        self.offsets = [] #pri_relative_offset[] 
        self.masks = []   #pri_mask_***[]; multi-dimensional, 1st index = offset, 2nd = mask[i] of offset

    def read(self, file, offset):
        file.seek(offset)
        print('[LIB_PRI] <READ> PRI_FILE\t(' + str(file.tell()) + ')')

        self.header = self.header.read(file)
        self.offsets = []
        self.masks = []

        if self.header.offsets > 0 and self.header.offsets != 65535:
            for i in range(self.header.offsets):
                tmp_obj = pri_relative_offset()
                tmp_obj = tmp_obj.read(file)
                self.offsets.append(tmp_obj)
                
            for i in range(self.header.offsets):
                tmp_masks = []

                for j in range(self.offsets[i].count):
                    
                    if self.version == 1.0 or self.version == 1.5:
                        file.seek(7, 1)

                    if self.version == 2.0 or self.version == 3.0:
                        file.seek(6, 1)
                    
                    width = int(struct.unpack("B", file.read(1))[0])
                    
                    if self.version == 1.0 or self.version == 1.5:
                        if width != 0x00:
                            file.seek(-8, 1)
                            tmp_mask = pri_mask_square(self.version)
                            tmp_mask = tmp_mask.read(file)
                            tmp_masks.append(tmp_mask)

                        else:
                            file.seek(-8, 1)
                            tmp_mask = pri_mask_rectangle()
                            tmp_mask = tmp_mask.read(file)
                            tmp_masks.append(tmp_mask)

                    if self.version == 2.0 or self.version == 3.0:
                        if width != 0x00:
                            file.seek(-7, 1)
                            tmp_mask = pri_mask_square(self.version)
                            tmp_mask = tmp_mask.read(file)
                            tmp_masks.append(tmp_mask)

                        else:
                            file.seek(-7, 1)
                            tmp_mask = pri_mask_rectangle()
                            tmp_mask = tmp_mask.read(file)
                            tmp_masks.append(tmp_mask)

                self.masks.append(tmp_masks)
        return self

    def write(self, file, offset):
        file.seek(offset)
        print('[LIB_PRI] <WRITE> PRI_FILE\t(' + str(file.tell()) + ')')

        if self.header.offsets > 0 and self.header.offsets != 65535:
            self.header.write(file)
                
            for i in range(self.header.offsets):
                self.offsets[i].write(file)

            for i in range(len(self.masks)):
                for j in range(len(self.masks[i])):
                    self.masks[i][j].write(file)

        else:
            if self.version == 1.0:
                file.write(struct.pack('L', int(0)))
            
            if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
                file.write(struct.pack('l', int(-1)))

    def extract(self, filepath):
        print('[LIB_PRI] <EXTRACT> PRI_FILE\t(' + filepath + ')')
        
        file = open(filepath, 'wb')
        self.write(file, 0)
        file.close()
