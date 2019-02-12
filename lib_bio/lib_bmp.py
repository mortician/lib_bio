########################################################################################################################
# LIB_BMP - BITMAP IMAGE FORMAT
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct

#=======================================================================================================================
# DEFINES
#=======================================================================================================================

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

        return self

    def from_long(self, rgb):
        self.r = rgb & 0xFF
        self.g = int(rgb / 0x100) & 0xFF
        self.b = int(rgb / 0x10000) & 0xFF

class bmp_header:
    def __init__(self):
        self.magic = 16     #uint16; "BM" or 0x424D
        self.size = 0       #uint32; total size in bytes
        self.reserved_0 = 0 #uint16; reserved, actual value depends on the application that creates the image
        self.reserved_1 = 0 #uint16; reserved, actual value depends on the application that creates the image
        self.offset = 0     #uint16; starting address of the bitmap image data

    def read(self, file):
        self.magic = int(struct.unpack("H", file.read(2))[0])
        self.size = int(struct.unpack("L", file.read(4))[0])
        self.reserved_0 = int(struct.unpack("H", file.read(2))[0])
        self.reserved_1 = int(struct.unpack("H", file.read(2))[0])
        self.offset = int(struct.unpack("L", file.read(4))[0])
        return self

    def write(self, file):
        file.write(struct.pack('H', int(self.magic)))
        file.write(struct.pack('L', int(self.size)))
        file.write(struct.pack('H', int(self.reserved_0)))
        file.write(struct.pack('H', int(self.reserved_1)))
        file.write(struct.pack('L', int(self.offset)))

class dib_header:
    def __init__(self):
        self.size = 0         #uint32; total size of header in bytes
        self.width = 0        #int32; width in pixels
        self.height = 0       #int32; height in pixels
        self.color_planes = 0 #uint16; number of color planes, must be 1
        self.bpp = 0          #uint16; bits per pixel (color depth) 1, 4, 8, 16, 24 or 32
        self.compression = 0  #uint32; compression method being used
        self.image_size = 0   #uint32; compression method being used
        self.h_res = 0        #int32; horizontal resolution of the image (pixel per meter)
        self.v_res = 0        #int32; vertical resolution of the image (pixel per meter)
        self.colors = 0       #uint32; number of colors in the palette
        self.important_colors = 0 #uint32; number of important colors used, 0 when every color is important

    def read(self, file):
        self.size = int(struct.unpack("L", file.read(4))[0])
        self.width = int(struct.unpack("l", file.read(4))[0])
        self.height = int(struct.unpack("l", file.read(4))[0])
        self.color_planes = int(struct.unpack("H", file.read(2))[0])
        self.bpp = int(struct.unpack("H", file.read(2))[0])
        self.compression = int(struct.unpack("L", file.read(4))[0])
        self.image_size = int(struct.unpack("L", file.read(4))[0])
        self.h_res = int(struct.unpack("l", file.read(4))[0])
        self.v_res = int(struct.unpack("l", file.read(4))[0])
        self.colors = int(struct.unpack("L", file.read(4))[0])
        self.important_colors = int(struct.unpack("L", file.read(4))[0])
        return self

    def write(self, file):
        file.write(struct.pack('L', int(self.size)))
        file.write(struct.pack('l', int(self.width)))
        file.write(struct.pack('l', int(self.height)))
        file.write(struct.pack('H', int(self.color_planes)))
        file.write(struct.pack('H', int(self.bpp)))
        file.write(struct.pack('L', int(self.compression)))
        file.write(struct.pack('L', int(self.image_size)))
        file.write(struct.pack('L', int(self.h_res)))
        file.write(struct.pack('l', int(self.v_res)))
        file.write(struct.pack('L', int(self.colors)))
        file.write(struct.pack('L', int(self.important_colors)))
        
class bmp_palette:
    def __init__(self):
        self.color = [] #uint16[]; each color is in 16 bit A1B5G5R5 format

    def read(self, file, bpp):
        self.color = []
        
        if bpp == 4:
            for i in range(16):
                self.color.append(int(struct.unpack("H", file.read(2))[0]))

        if bpp == 8:
            for i in range(256):
                self.color.append(int(struct.unpack("H", file.read(2))[0]))

        return self

    def write(self, file):
        for i in range(len(self.color)):
            file.write(struct.pack('H', int(self.color[i])))

class bmp_image_data:
    def __init__(self):
        self.pixel = [] #two dimensional array, 1st index is y, 2nd is x

    def read(self, file, width, height, bpp):
        self.pixel = []

        if bpp == 24:
            for y in range(height):
                tmp_row = []
                
                for x in range(width):
                    tmp_rgb = rgb_color()
                    tmp_row.append(tmp_rgb.read(file))
                
                self.pixel.append(tmp_row)

        return self
    
    def write(self, file, bpp):
        if len(self.pixel) > 0:
            if bpp == 24:
                for y in range(len(self.pixel)):
                    for x in range(len(self.pixel[y])):
                        file.write(struct.pack('B', int(self.pixel[y][x].b)))
                        file.write(struct.pack('B', int(self.pixel[y][x].g)))
                        file.write(struct.pack('B', int(self.pixel[y][x].r)))
        else:
            print('NO BMP IMAGE DATA')
class bmp_file:
    def __init__(self):
        self.header = bmp_header()
        self.palette = [] #bmp_palette[] array
        self.dib_header = dib_header()
        self.image_data = bmp_image_data()

    def read_from_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_BMP] <READ> BMP_FILE\t(' + str(file.tell()) + ')')

        self.header = self.header.read(file)
        self.dib_header = dib_header()
        self.image_data = bmp_image_data()

        if self.header.bpp == 24:
            self.image_data = self.image_data.read(file, self.image_header.width * 2, self.image_header.height, self.header.bpp)
        
        else:
            print('[LIB_BMP] <ERROR> ONLY 24 BIT FILES ARE SUPPORTED')

        return self

    def write_to_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_BMP] <WRITE> BMP_DATA\t(' + str(file.tell()) + ')')

        self.header.write(file)
        self.dib_header.write(file)
        self.image_data.write(file, self.dib_header.bpp)

    def write_to_file(self, filepath):
        print('[LIB_BMP] <WRITE> BMP_FILE\t(' + filepath + ')')
        print(self.dib_header.bpp)
        file = open(filepath, 'wb')
        self.write_to_stream(file, 0)
        file.close()