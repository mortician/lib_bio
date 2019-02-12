########################################################################################################################
# LIB_MD2 - CAPCOM'S CUSTOM SONY PLAYSTATION "TMD" 3D MODEL FORMAT
########################################################################################################################
# SUPPORTED:
#               BIOHAZARD 3: LAST ESCAPE
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct

class md2_vertex:
    def __init__(self):
        self.x = 0    #int16; 
        self.y = 0    #int16; 
        self.z = 0    #int16; 
        self.zero = 0 #uint16; 
    
    def read(self, file):
        self.x = int(struct.unpack("h", file.read(2))[0])
        self.y = int(struct.unpack("h", file.read(2))[0])
        self.z = int(struct.unpack("h", file.read(2))[0])
        self.zero = int(struct.unpack("H", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('h', int(self.x)))
        file.write(struct.pack('h', int(self.y)))
        file.write(struct.pack('h', int(self.z)))
        file.write(struct.pack('H', int(self.zero)))

class md2_normal:
    def __init__(self):
        self.x = 0    #int16; 
        self.y = 0    #int16; 
        self.z = 0    #int16; 
        self.zero = 0 #uint16; 
    
    def read(self, file):
        self.x = int(struct.unpack("h", file.read(2))[0])
        self.y = int(struct.unpack("h", file.read(2))[0])
        self.z = int(struct.unpack("h", file.read(2))[0])
        self.zero = int(struct.unpack("H", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('h', int(self.x)))
        file.write(struct.pack('h', int(self.y)))
        file.write(struct.pack('h', int(self.z)))
        file.write(struct.pack('H', int(self.zero)))

class md2_triangle:
    def __init__(self):
        self.tu_0 = 0     #byte; 
        self.tv_0 = 0     #byte; 
        self.dummy_0 = 0  #byte; 
        self.dummy_1 = 0  #byte; 
        self.tu_1 = 0     #byte; 
        self.tv_1 = 0     #byte; 
        self.page = 0     #byte; 
        self.vertex_0 = 0 #byte; 
        self.tu_2 = 0     #byte; 
        self.tv_2 = 0     #byte; 
        self.vertex_1 = 0 #byte; 
        self.vertex_2 = 0 #byte; 

    def read(self, file):
        self.tu_0 = int(struct.unpack("B", file.read(1))[0])
        self.tv_0 = int(struct.unpack("B", file.read(1))[0])
        self.dummy_0 = int(struct.unpack("B", file.read(1))[0])
        self.dummy_1 = int(struct.unpack("B", file.read(1))[0])
        self.tu_1 = int(struct.unpack("B", file.read(1))[0])
        self.tv_1 = int(struct.unpack("B", file.read(1))[0])
        self.page = int(struct.unpack("B", file.read(1))[0])
        self.vertex_0 = int(struct.unpack("B", file.read(1))[0])
        self.tu_2 = int(struct.unpack("B", file.read(1))[0])
        self.tv_2 = int(struct.unpack("B", file.read(1))[0])
        self.vertex_1 = int(struct.unpack("B", file.read(1))[0])
        self.vertex_2 = int(struct.unpack("B", file.read(1))[0])
        return self

    def write(self, file):
        file.write(struct.pack('B', int(self.tu_0)))
        file.write(struct.pack('B', int(self.tv_0)))
        file.write(struct.pack('B', int(self.dummy_0)))
        file.write(struct.pack('B', int(self.dummy_1)))
        file.write(struct.pack('B', int(self.tu_1)))
        file.write(struct.pack('B', int(self.tv_1)))
        file.write(struct.pack('B', int(self.page)))
        file.write(struct.pack('B', int(self.vertex_0)))
        file.write(struct.pack('B', int(self.tu_2)))
        file.write(struct.pack('B', int(self.tv_2)))
        file.write(struct.pack('B', int(self.vertex_1)))
        file.write(struct.pack('B', int(self.vertex_2)))

class md2_quadrangle:
    def __init__(self):
        self.tu_0 = 0     #byte; 
        self.tv_0 = 0     #byte; 
        self.dummy_0 = 0  #byte; 
        self.dummy_1 = 0  #byte; 
        self.tu_1 = 0     #byte; 
        self.tv_1 = 0     #byte; 
        self.page = 0     #byte; 
        self.dummy_3 = 0  #byte; 
        self.tu_2 = 0     #byte; 
        self.tv_2 = 0     #byte; 
        self.vertex_0 = 0 #byte; 
        self.vertex_1 = 0 #byte; 
        self.tu_3 = 0     #byte; 
        self.tv_3 = 0     #byte; 
        self.vertex_2 = 0 #byte; 
        self.vertex_3 = 0 #byte; 

    def read(self, file):
        self.tu_0 = int(struct.unpack("B", file.read(1))[0])
        self.tv_0 = int(struct.unpack("B", file.read(1))[0])
        self.dummy_0 = int(struct.unpack("B", file.read(1))[0])
        self.dummy_1 = int(struct.unpack("B", file.read(1))[0])
        self.tu_1 = int(struct.unpack("B", file.read(1))[0])
        self.tv_1 = int(struct.unpack("B", file.read(1))[0])
        self.page = int(struct.unpack("B", file.read(1))[0])
        self.dummy_3 = int(struct.unpack("B", file.read(1))[0])
        self.tu_2 = int(struct.unpack("B", file.read(1))[0])
        self.tv_2 = int(struct.unpack("B", file.read(1))[0])
        self.vertex_0 = int(struct.unpack("B", file.read(1))[0])
        self.vertex_1 = int(struct.unpack("B", file.read(1))[0])
        self.tu_3 = int(struct.unpack("B", file.read(1))[0])
        self.tv_3 = int(struct.unpack("B", file.read(1))[0])
        self.vertex_2 = int(struct.unpack("B", file.read(1))[0])
        self.vertex_3 = int(struct.unpack("B", file.read(1))[0])
        return self

    def write(self, file):
        file.write(struct.pack('B', int(self.tu_0)))
        file.write(struct.pack('B', int(self.tv_0)))
        file.write(struct.pack('B', int(self.dummy_0)))
        file.write(struct.pack('B', int(self.dummy_1)))
        file.write(struct.pack('B', int(self.tu_1)))
        file.write(struct.pack('B', int(self.tv_1)))
        file.write(struct.pack('B', int(self.page)))
        file.write(struct.pack('B', int(self.dummy_3)))
        file.write(struct.pack('B', int(self.tu_2)))
        file.write(struct.pack('B', int(self.tv_2)))
        file.write(struct.pack('B', int(self.vertex_0)))
        file.write(struct.pack('B', int(self.vertex_1)))
        file.write(struct.pack('B', int(self.tu_3)))
        file.write(struct.pack('B', int(self.tv_3)))
        file.write(struct.pack('B', int(self.vertex_2)))
        file.write(struct.pack('B', int(self.vertex_3)))

class md2_object_header:
    def __init__(self):
        self.vertex_offset = 0 #uint16
        self.unknown_0 = 0     #uint16
        self.normal_offset = 0 #uint16
        self.unknown_1 = 0     #uint16
        self.vertex_count = 0  #uint16
        self.unknown_2 = 0     #uint16
        self.t_offset = 0      #uint16
        self.unknown_3 = 0     #uint16
        self.q_offset = 0      #uint16
        self.unknown_4 = 0     #uint16
        self.t_count = 0       #uint16
        self.q_count = 0       #uint16

    def read(self, file):
        self.vertex_offset = int(struct.unpack("H", file.read(2))[0])
        self.unknown_0 = int(struct.unpack("H", file.read(2))[0])
        self.normal_offset = int(struct.unpack("H", file.read(2))[0])
        self.unknown_1 = int(struct.unpack("H", file.read(2))[0])
        self.vertex_count = int(struct.unpack("H", file.read(2))[0])
        self.unknown_2 = int(struct.unpack("H", file.read(2))[0])
        self.t_offset = int(struct.unpack("H", file.read(2))[0])
        self.unknown_3 = int(struct.unpack("H", file.read(2))[0])
        self.q_offset = int(struct.unpack("H", file.read(2))[0])
        self.unknown_4 = int(struct.unpack("H", file.read(2))[0])
        self.t_count = int(struct.unpack("H", file.read(2))[0])
        self.q_count = int(struct.unpack("H", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('H', int(self.vertex_offset)))
        file.write(struct.pack('H', int(self.unknown_0)))
        file.write(struct.pack('H', int(self.normal_offset)))
        file.write(struct.pack('H', int(self.unknown_1)))
        file.write(struct.pack('H', int(self.vertex_count)))
        file.write(struct.pack('H', int(self.unknown_2)))
        file.write(struct.pack('H', int(self.t_offset)))
        file.write(struct.pack('H', int(self.unknown_3)))
        file.write(struct.pack('H', int(self.q_offset)))
        file.write(struct.pack('H', int(self.unknown_4)))
        file.write(struct.pack('H', int(self.t_count)))
        file.write(struct.pack('H', int(self.q_count)))

class md2_object:
    def __init__(self):
        self.header = md2_object_header()
        self.vertices = []    #md2_vertx array
        self.normals = []     #md2_normal array
        self.triangles = []   #md2_triangle array
        self.quadrangles = [] #md2_quadrangle array

class md2_header:
    def __init__(self):
        self.length = 0 #uint32
        self.count = 0  #uint32

    def read(self, file):
        self.length = int(struct.unpack("L", file.read(4))[0])
        self.count = int(struct.unpack("L", file.read(4))[0])
        return self

    def write(self, file):
        file.write(struct.pack('L', int(self.length)))
        file.write(struct.pack('L', int(self.count)))

class md2_file:
    def __init__(self):
        self.header = md2_header() #md2_header
        self.object = []           #md2_object[]

    def read_from_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_MD1] <READ> MD2_DATA\t(' + str(file.tell()) + ')')

        #read header...
        self.header = self.header.read(file)
    
        #read objects...
        for i in range(self.header.count):
            file.seek(offset + 8 + (i * 24))

            tmp_obj = md2_object()
            tmp_obj.header = tmp_obj.header.read(file)
        
            if (tmp_obj.header.t_count == tmp_obj.header.t_offset) or (tmp_obj.header.t_count == tmp_obj.header.q_offset):
                tmp_obj.header.t_count = 0

            if tmp_obj.header.q_count > 255:
                tmp_obj.header.q_count = 0

            #triangle handling...
            if tmp_obj.header.t_count > 0:

                #read vertices...
                file.seek(offset + 8 + tmp_obj.header.vertex_offset)
                
                for j in range(tmp_obj.header.vertex_count):
                    tmp_vertex = md2_vertex()
                    tmp_vertex = tmp_vertex.read(file)
                    tmp_obj.vertices.append(tmp_vertex)

                #read normals...
                file.seek(offset + 8 + tmp_obj.header.normal_offset)

                for j in range(tmp_obj.header.vertex_count):
                    tmp_normal = md2_normal()
                    tmp_normal = tmp_normal.read(file)
                    tmp_obj.normals.append(tmp_normal)

                #read triangles...
                file.seek(offset + 8 + tmp_obj.header.t_offset)

                for j in range(tmp_obj.header.t_count):
                    tmp_triangle = md2_triangle()
                    tmp_triangle = tmp_triangle.read(file)
                    tmp_obj.triangles.append(tmp_triangle)

            #quadrangle handling...
            if tmp_obj.header.q_count > 0:

                if len(tmp_obj.vertices) == 0:
                    #read vertices...
                    file.seek(offset + 8 + tmp_obj.header.vertex_offset)

                    for j in range(tmp_obj.header.vertex_count):
                        tmp_vertex = md2_vertex()
                        tmp_vertex = tmp_vertex.read(file)
                        tmp_obj.vertices.append(tmp_vertex)

                if len(tmp_obj.normals) == 0:
                    #read normals...
                    file.seek(offset + 8 + tmp_obj.header.normal_offset)

                    for j in range(tmp_obj.header.vertex_count):
                        tmp_normal = md2_normal()
                        tmp_normal = tmp_normal.read(file)
                        tmp_obj.normals.append(tmp_normal)

                #read quadrangles...
                file.seek(offset + 8 + tmp_obj.header.q_offset)

                for j in range(tmp_obj.header.q_count):
                    tmp_quadrangle = md2_quadrangle()
                    tmp_quadrangle = tmp_quadrangle.read(file)
                    tmp_obj.quadrangles.append(tmp_quadrangle)

            self.object.append(tmp_obj)

        return self

    def read_from_file(self, filepath):
        print('[LIB_MD2] <READ> MD2_FILE\t(' + filepath + ')')

        file = open(filepath, 'rb')
        self.read_from_stream(file, 0)
        file.close()

        return self

    def write_to_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_MD2] <WRITE> MD2_DATA\t(' + str(file.tell()) + ')')

        self.header.write(file)

        for i in range(len(self.object)):
            self.object[i].header.write(file)

        for i in range(len(self.object)):
            #write vertices
            file.seek(offset + 8 + self.object[i].header.vertex_offset)

            for j in range(len(self.object[i].vertices)):
                self.object[i].vertices[j].write(file)

            #write normals
            file.seek(offset + 8 + self.object[i].header.normal_offset)

            for j in range(len(self.object[i].normals)):
                self.object[i].normals[j].write(file)

            #write triangles
            if len(self.object[i].triangles) > 0:
                file.seek(offset + 8 + self.object[i].header.t_offset)

                for j in range(len(self.object[i].triangles)):
                    self.object[i].triangles[j].write(file)

            #write quadrangles
            if len(self.object[i].quadrangles) > 0:
                file.seek(offset + 8 + self.object[i].header.q_offset)

                for j in range(len(self.object[i].quadrangles)):
                    self.object[i].quadrangles[j].write(file)

    def write_to_file(self, filepath):
        if self.header.count > 0 and len(self.object) > 0:
            print('[LIB_MD2] <WRITE> MD2_FILE\t(' + filepath + ')')

            file = open(filepath, 'wb')
            self.write_to_stream(file, 0)
            file.close()