########################################################################################################################
# LIB_TIM - SONY PLAYSTATION BITMAP IMAGE FORMAT
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import imp
import os
import struct
import lib_bio.lib_bmp as lib_bmp
imp.reload(lib_bmp)

#=======================================================================================================================
# DEFINES
#=======================================================================================================================
TIM_BPP_4 = 8
TIM_BPP_8 = 9
TIM_BPP_16 = 2
TIM_BPP_24 = 3

#=======================================================================================================================
# CLASSES
#=======================================================================================================================
class rgb_color:
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

    def from_bgr(self, bgr):
        rgb = 0
        factor = 1
        tmp_val = float(0)

        for i in range(3):
            tmp_val = float(int(bgr) & 0x1F) / float(31) * float(255)
            value = int(tmp_val)

            bgr /= 32
            rgb |= (value * factor)
            factor *= 256

        self.from_long(rgb)
        return self

    def from_long(self, rgb):
        self.r = rgb & 0xFF
        self.g = int(rgb / 0x100) & 0xFF
        self.b = int(rgb / 0x10000) & 0xFF

class tim_header:
    def __init__(self):
        self.magic = 16 #uint32; always 16 (0x10000000)
        self.bpp = 0    #uint32; (8 = 4 bit), (9 = 8 bit), (2 = 16 bit), (3 == 24 bit)
        self.offset = 0 #uint32; when 16 bit it's imagesize - 12, else offset to image header
        self.org_x = 0  #uint16; when 4/8 bpp then it's the clut x origin, for 16/24 bpp it's the image x origin
        self.org_y = 0  #uint16; when 4/8 bpp then it's the clut y origin, for 16/24 bpp it's the image y origin
        self.colors = 0 #uint16; when 4/8 bpp then it's the color count, for 16 bpp it's the width, for 24 bpp *1.5
        self.cluts = 0  #uint16; count of cluts used (only for 4 and 8 bpp files), is height for 16 and 24 bpp

    def read(self, file):
        self.magic = int(struct.unpack("L", file.read(4))[0])
        self.bpp = int(struct.unpack("L", file.read(4))[0])
        self.offset = int(struct.unpack("L", file.read(4))[0])
        self.org_x = int(struct.unpack("H", file.read(2))[0])
        self.org_y = int(struct.unpack("H", file.read(2))[0])
        self.colors = int(struct.unpack("H", file.read(2))[0])
        self.cluts = int(struct.unpack("H", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('L', int(self.magic)))
        file.write(struct.pack('L', int(self.bpp)))
        file.write(struct.pack('L', int(self.offset)))
        file.write(struct.pack('H', int(self.org_x)))
        file.write(struct.pack('H', int(self.org_y)))
        file.write(struct.pack('H', int(self.colors)))
        file.write(struct.pack('H', int(self.cluts)))

class tim_clut:
    def __init__(self):
        self.color = [] #uint16[]; each color is in 16 bit A1B5G5R5 format

    def read(self, file, bpp):
        self.color = []
        
        if bpp == TIM_BPP_4:
            for i in range(16):
                self.color.append(int(struct.unpack("H", file.read(2))[0]))

        if bpp == TIM_BPP_8:
            for i in range(256):
                self.color.append(int(struct.unpack("H", file.read(2))[0]))

        return self

    def write(self, file):
        for i in range(len(self.color)):
            file.write(struct.pack('H', int(self.color[i])))

class tim_image_header:
    def __init__(self):
        self.size = 0   #uint32; total image data size in bytes (image header + image data)
        self.org_x = 0  #uint16; image x origin
        self.org_y = 0  #uint16; image y origin
        self.width = 0  #uint16; *4 for 4 bit, *2 for 8 bit
        self.height = 0 #uint16; height of image

    def read(self, file):
        self.size = int(struct.unpack("L", file.read(4))[0])
        self.org_x = int(struct.unpack("H", file.read(2))[0])
        self.org_y = int(struct.unpack("H", file.read(2))[0])
        self.width = int(struct.unpack("H", file.read(2))[0])
        self.height = int(struct.unpack("H", file.read(2))[0])

        return self

    def write(self, file):
        file.write(struct.pack('L', int(self.size)))
        file.write(struct.pack('H', int(self.org_x)))
        file.write(struct.pack('H', int(self.org_y)))
        file.write(struct.pack('H', int(self.width)))
        file.write(struct.pack('H', int(self.height)))

class tim_image_data:
    def __init__(self):
        self.pixel = [] #two dimensional array, 1st index is y, 2nd is x

    def read(self, file, width, height, bpp):
        self.pixel = []

        if bpp == TIM_BPP_4 or bpp == TIM_BPP_8:
            for y in range(height):
                tmp_row = []
                
                for x in range(width):
                    tmp_row.append(int(struct.unpack("B", file.read(1))[0]))
                
                self.pixel.append(tmp_row)

        if bpp == TIM_BPP_16:
            for y in range(height):
                tmp_row = []
                
                for x in range(width):
                    tmp_row.append(int(struct.unpack("H", file.read(2))[0]))
                
                self.pixel.append(tmp_row)

        if bpp == TIM_BPP_24:
            for y in range(height):
                tmp_row = []
                
                for x in range(width):
                    tmp_rgb = rgb_color()
                    tmp_row.append(tmp_rgb.read(file))
                
                self.pixel.append(tmp_row)

        return self
    
    def write(self, file, bpp):
        if bpp == TIM_BPP_4 or bpp == TIM_BPP_8:
            for y in range(len(self.pixel)):
                for x in range(len(self.pixel[y])):
                    file.write(struct.pack('B', int(self.pixel[y][x])))
                
        if bpp == TIM_BPP_16:
            for y in range(len(self.pixel)):
                for x in range(len(self.pixel[y])):
                    file.write(struct.pack('H', int(self.pixel[y][x])))

        if bpp == TIM_BPP_24:
            for y in range(len(self.pixel)):
                for x in range(len(self.pixel[y])):
                    self.pixel[y][x].write(file)

class tim_file:
    def __init__(self):
        self.header = tim_header()
        self.clut = [] #tim_clut[] array
        self.image_header = tim_image_header()
        self.image_data = tim_image_data()

    def read_from_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_TIM] <READ> TIM_FILE\t(' + str(file.tell()) + ')')

        self.header = self.header.read(file)
        self.clut = []
        self.image_header = tim_image_header()
        self.image_data = tim_image_data()

        #4 bpp file handling...
        if self.header.bpp == TIM_BPP_4:
            for i in range(self.header.cluts):
                tmp_clut = tim_clut()
                tmp_clut = tmp_clut.read(file, self.header.bpp)
                self.clut.append(tmp_clut)
                
            self.image_header = self.image_header.read(file)
            self.image_data = self.image_data.read(file, self.image_header.width * 2, self.image_header.height, self.header.bpp)

        #8 bpp file handling...
        if self.header.bpp == TIM_BPP_8:
            for i in range(self.header.cluts):
                tmp_clut = tim_clut()
                tmp_clut = tmp_clut.read(file, self.header.bpp)
                self.clut.append(tmp_clut)

            self.image_header = self.image_header.read(file)
            self.image_data = self.image_data.read(file, self.image_header.width * 2, self.image_header.height, self.header.bpp)

        #16 bpp file handling...
        if self.header.bpp == TIM_BPP_16:
            self.image_data = self.image_data.read(file, self.header.colors, self.header.cluts, self.header.bpp)
        
        #24 bpp file handling...
        if self.header.bpp == TIM_BPP_24:
            self.image_data = self.image_data.read(file, int(self.header.colors * 1.5), self.header.cluts, self.header.bpp)

        return self

    def read_from_file(self, filepath):
        print('[LIB_TIM] <READ> TIM_FILE\t(' + filepath + ')')

        if os.path.exists(filepath):
            file = open(filepath, 'rb')
            self.read_from_stream(file, 0)
            file.close()

            return self

        else:
            print('[LIB_TIM] <ERROR> CAN NOT FIND \t(' + filepath + ')')

    def write(self, file, offset):
        file.seek(offset)
        print('[LIB_TIM] <WRITE> TIM_FILE\t(' + str(file.tell()) + ')')

        self.header.write(file)
        
        for i in range(len(self.clut)):
            self.clut[i].write(file)

        if self.image_header.size > 0:
            self.image_header.write(file)
        
        #4 bpp file handling...
        if self.header.bpp == 8:
            self.image_data.write(file, 4)
        
        #8 bpp file handling...
        if self.header.bpp == 9:
            self.image_data.write(file, 8)
        
        #16 bpp file handling...
        if self.header.bpp == 2:
            self.image_data.write(file, 16)

        #24 bpp file handling...
        if self.header.bpp == 3:
            self.image_data.write(file, 24)
    
    def save_as_bmp(self, filepath):
        print('[LIB_TIM] <CONVERT> TIM_2_BMP\t(' + filepath + ')')
        if self.header.bpp == TIM_BPP_8:
            tmp_bmp = lib_bmp.bmp_file()
            
            tmp_bmp.header.magic = 19778
            tmp_bmp.header.size = 54 + (((self.image_header.width * 2) * self.image_header.height) * 3)
            tmp_bmp.header.reserved_0 = 0
            tmp_bmp.header.reserved_1 = 0
            tmp_bmp.header.offset = 54
            
            tmp_bmp.dib_header.size = 40
            tmp_bmp.dib_header.width = self.image_header.width * 2
            tmp_bmp.dib_header.height = self.image_header.height

            print(str(self.image_header.width * 2) + ' x ' + str(self.image_header.height))

            tmp_bmp.dib_header.color_planes = 1
            tmp_bmp.dib_header.bpp = 24
            tmp_bmp.dib_header.compression = 0
            tmp_bmp.dib_header.image_size = ((self.image_header.width * 2) * self.image_header.height) * 3

            y_fix = tmp_bmp.dib_header.height - 1

            for y in range(len(self.image_data.pixel)):
                tmp_row = []

                

                for x in range(len(self.image_data.pixel[y])):
                    tmp_rgb = rgb_color()
                    tmp_rgb = rgb_color.from_bgr(tmp_rgb, self.clut[0].color[self.image_data.pixel[y_fix][x]])
                    tmp_row.append(tmp_rgb)
                
                tmp_bmp.image_data.pixel.append(tmp_row)
                y_fix -= 1

            print(str(len(tmp_bmp.image_data.pixel)))

            tmp_bmp.dib_header.h_res = 2835
            tmp_bmp.dib_header.v_res = 2835

            tmp_bmp.write_to_file(filepath)



    def extract(self, filepath):
        print('[LIB_TIM] <EXTRACT> TIM_FILE\t(' + filepath + ')')

        if self.header.bpp > 0:
            file = open(filepath, 'wb')
            self.write(file, 0)
            file.close()