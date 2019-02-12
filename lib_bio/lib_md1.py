########################################################################################################################
# LIB_MD1 - CAPCOM'S CUSTOM SONY PLAYSTATION "TMD" 3D MODEL FORMAT
########################################################################################################################
# SUPPORTED:
#               BIOHAZARD 2 PROTOTYPE (NOV/1996)
#               BIOHAZARD 2
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct

class md1_vertex:
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

class md1_normal:
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

class md1_triangle:
    def __init__(self):
        self.normal_0 = 0 #uint16; index of normal 0 of the triangle
        self.vertex_0 = 0 #uint16; index of vertex 0 of the triangle
        self.normal_1 = 0 #uint16; index of normal 1 of the triangle
        self.vertex_1 = 0 #uint16, index of vertex 1 of the triangle
        self.normal_2 = 0 #uint16; index of normal 2 of the triangle
        self.vertex_2 = 0 #uint16; index of vertex 2 of the triangle
    
    def read(self, file):
        self.normal_0 = int(struct.unpack("H", file.read(2))[0])
        self.vertex_0 = int(struct.unpack("H", file.read(2))[0])
        self.normal_1 = int(struct.unpack("H", file.read(2))[0])
        self.vertex_1 = int(struct.unpack("H", file.read(2))[0])
        self.normal_2 = int(struct.unpack("H", file.read(2))[0])
        self.vertex_2 = int(struct.unpack("H", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('H', int(self.normal_0)))
        file.write(struct.pack('H', int(self.vertex_0)))
        file.write(struct.pack('H', int(self.normal_1)))
        file.write(struct.pack('H', int(self.vertex_1)))
        file.write(struct.pack('H', int(self.normal_2)))
        file.write(struct.pack('H', int(self.vertex_2)))

class md1_triangle_uv:
    def __init__(self):
        self.u_0 = 0  #byte; u-coordinate of vertex 0
        self.v_0 = 0  #byte; v-coordinate of vertex 0
        self.clut = 0 #uint16; texture clut id, bits 0-5
        self.u_1 = 0  #byte; u-coordinate of vertex 1
        self.v_1 = 0  #byte; v-coordinate of vertex 1
        self.page = 0 #uint16; texture page
        self.u_2 = 0  #byte; u-coordinate of vertex 2
        self.v_2 = 0  #byte; v-coordinate of vertex 2
        self.zero = 0 #uint16; dummy for padding?

    def read(self, file):
        self.u_0 = int(struct.unpack("B", file.read(1))[0])
        self.v_0 = int(struct.unpack("B", file.read(1))[0])
        self.clut = int(struct.unpack("H", file.read(2))[0])
        self.u_1 = int(struct.unpack("B", file.read(1))[0])
        self.v_1 = int(struct.unpack("B", file.read(1))[0])
        self.page = int(struct.unpack("H", file.read(2))[0])
        self.u_2 = int(struct.unpack("B", file.read(1))[0])
        self.v_2 = int(struct.unpack("B", file.read(1))[0])
        self.zero = int(struct.unpack("H", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('B', int(self.u_0)))
        file.write(struct.pack('B', int(self.v_0)))
        file.write(struct.pack('H', int(self.clut)))
        file.write(struct.pack('B', int(self.u_1)))
        file.write(struct.pack('B', int(self.v_1)))
        file.write(struct.pack('H', int(self.page)))
        file.write(struct.pack('B', int(self.u_2)))
        file.write(struct.pack('B', int(self.v_2)))
        file.write(struct.pack('H', int(self.zero)))

class md1_quadrangle:
    def __init__(self):
        self.normal_0 = 0 #uint16; index of normal 0 of the triangle
        self.vertex_0 = 0 #uint16; index of vertex 0 of the triangle
        self.normal_1 = 0 #uint16; index of normal 1 of the triangle
        self.vertex_1 = 0 #uint16, index of vertex 1 of the triangle
        self.normal_2 = 0 #uint16; index of normal 2 of the triangle
        self.vertex_2 = 0 #uint16; index of vertex 2 of the triangle
        self.normal_3 = 0 #uint16; index of normal 3 of the triangle
        self.vertex_3 = 0 #uint16; index of vertex 3 of the triangle

    def read(self, file):
        self.normal_0 = int(struct.unpack("H", file.read(2))[0])
        self.vertex_0 = int(struct.unpack("H", file.read(2))[0])
        self.normal_1 = int(struct.unpack("H", file.read(2))[0])
        self.vertex_1 = int(struct.unpack("H", file.read(2))[0])
        self.normal_2 = int(struct.unpack("H", file.read(2))[0])
        self.vertex_2 = int(struct.unpack("H", file.read(2))[0])
        self.normal_3 = int(struct.unpack("H", file.read(2))[0])
        self.vertex_3 = int(struct.unpack("H", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('H', int(self.normal_0)))
        file.write(struct.pack('H', int(self.vertex_0)))
        file.write(struct.pack('H', int(self.normal_1)))
        file.write(struct.pack('H', int(self.vertex_1)))
        file.write(struct.pack('H', int(self.normal_2)))
        file.write(struct.pack('H', int(self.vertex_2)))
        file.write(struct.pack('H', int(self.normal_3)))
        file.write(struct.pack('H', int(self.vertex_3)))

class md1_quadrangle_uv:
    def __init__(self):
        self.u_0 = 0    #byte; u-coordinate of vertex 0
        self.v_0 = 0    #byte; v-coordinate of vertex 0
        self.clut = 0   #uint16; texture clut id, bits 0-5
        self.u_1 = 0    #byte; u-coordinate of vertex 1
        self.v_1 = 0    #byte; v-coordinate of vertex 1
        self.page = 0   #uint16; texture page
        self.u_2 = 0    #byte; u-coordinate of vertex 2
        self.v_2 = 0    #byte; v-coordinate of vertex 2
        self.zero_0 = 0 #uint16; dummy for padding?
        self.u_3 = 0    #byte; u-coordinate of vertex 3
        self.v_3 = 0    #byte; v-coordinate of vertex 3
        self.zero_1 = 0 #uint16; dummy for padding?

    def read(self, file):
        self.u_0 = int(struct.unpack("B", file.read(1))[0])
        self.v_0 = int(struct.unpack("B", file.read(1))[0])
        self.clut = int(struct.unpack("H", file.read(2))[0])
        self.u_1 = int(struct.unpack("B", file.read(1))[0])
        self.v_1 = int(struct.unpack("B", file.read(1))[0])
        self.page = int(struct.unpack("H", file.read(2))[0])
        self.u_2 = int(struct.unpack("B", file.read(1))[0])
        self.v_2 = int(struct.unpack("B", file.read(1))[0])
        self.zero_0 = int(struct.unpack("H", file.read(2))[0])
        self.u_3 = int(struct.unpack("B", file.read(1))[0])
        self.v_3 = int(struct.unpack("B", file.read(1))[0])
        self.zero_1 = int(struct.unpack("H", file.read(2))[0])
        return self

    def write(self, file):
        file.write(struct.pack('B', int(self.u_0)))
        file.write(struct.pack('B', int(self.v_0)))
        file.write(struct.pack('H', int(self.clut)))
        file.write(struct.pack('B', int(self.u_1)))
        file.write(struct.pack('B', int(self.v_1)))
        file.write(struct.pack('H', int(self.page)))
        file.write(struct.pack('B', int(self.u_2)))
        file.write(struct.pack('B', int(self.v_2)))
        file.write(struct.pack('H', int(self.zero_0)))
        file.write(struct.pack('B', int(self.u_3)))
        file.write(struct.pack('B', int(self.v_3)))
        file.write(struct.pack('H', int(self.zero_1)))

class md1_object_header:
    def __init__(self):
        self.t_vertex_offset = 0 #uint32; relative offset to md1_vertex array
        self.t_vertex_count = 0  #uint32; total count of object's md1_vertex count
        self.t_normal_offset = 0 #uint32; relative offset to md1_normal array
        self.t_normal_count = 0  #uint32; total count of object's md1_normal count
        self.t_offset = 0        #uint32; relative offset to md1_triangle array
        self.t_count = 0         #uint32; total count of object's md1_triangle count
        self.t_uv_offset = 0     #uint32; relative offset to md1_triangle_uv array
        self.q_vertex_offset = 0 #uint32; relative offset to md1_vertex array
        self.q_vertex_count = 0  #uint32; total count of object's md1_vertex count
        self.q_normal_offset = 0 #uint32; relative offset to md1_normal array
        self.q_normal_count = 0  #uint32; total count of object's md1_normal count
        self.q_offset = 0        #uint32; relative offset to md1_quadrangle array
        self.q_count = 0         #uint32; total count of object's md1_quadrangle count
        self.q_uv_offset = 0     #uint32; relative offset to md1_quadrangle_uv array

    def read(self, file):
        self.t_vertex_offset = int(struct.unpack("L", file.read(4))[0])
        self.t_vertex_count = int(struct.unpack("L", file.read(4))[0])
        self.t_normal_offset = int(struct.unpack("L", file.read(4))[0])
        self.t_normal_count = int(struct.unpack("L", file.read(4))[0])
        self.t_offset = int(struct.unpack("L", file.read(4))[0])
        self.t_count = int(struct.unpack("L", file.read(4))[0])
        self.t_uv_offset = int(struct.unpack("L", file.read(4))[0])
        self.q_vertex_offset = int(struct.unpack("L", file.read(4))[0])
        self.q_vertex_count = int(struct.unpack("L", file.read(4))[0])
        self.q_normal_offset = int(struct.unpack("L", file.read(4))[0])
        self.q_normal_count = int(struct.unpack("L", file.read(4))[0])
        self.q_offset = int(struct.unpack("L", file.read(4))[0])
        self.q_count = int(struct.unpack("L", file.read(4))[0])
        self.q_uv_offset = int(struct.unpack("L", file.read(4))[0])
        return self

    def write(self, file):
        file.write(struct.pack('L', int(self.t_vertex_offset)))
        file.write(struct.pack('L', int(self.t_vertex_count)))
        file.write(struct.pack('L', int(self.t_normal_offset)))
        file.write(struct.pack('L', int(self.t_normal_count)))
        file.write(struct.pack('L', int(self.t_offset)))
        file.write(struct.pack('L', int(self.t_count)))
        file.write(struct.pack('L', int(self.t_uv_offset)))
        file.write(struct.pack('L', int(self.q_vertex_offset)))
        file.write(struct.pack('L', int(self.q_vertex_count)))
        file.write(struct.pack('L', int(self.q_normal_offset)))
        file.write(struct.pack('L', int(self.q_normal_count)))
        file.write(struct.pack('L', int(self.q_offset)))
        file.write(struct.pack('L', int(self.q_count)))
        file.write(struct.pack('L', int(self.q_uv_offset)))

class md1_object:
    def __init__(self):
        self.header = md1_object_header()
        self.vertices = []       #md1_vertex[]
        self.normals = []        #md1_normal[]
        self.triangles = []      #md1_triangle[]
        self.quadrangles = []    #md1_quadrangle[]
        self.triangles_uv = []   #md1_triangle_uv[]
        self.quadrangles_uv = [] #md1_quadrangle_uv[]

class md1_header:
    def __init__(self):
        self.length = 0  #uint32; !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.unknown = 0 #uint32; ?
        self.count = 0   #uint32; total count of objects (meshes)

    def read(self, file):
        self.length = int(struct.unpack("L", file.read(4))[0])
        self.unknown = int(struct.unpack("L", file.read(4))[0])
        self.count = int(struct.unpack("L", file.read(4))[0])
        return self

    def write(self, file):
        file.write(struct.pack('L', int(self.length)))
        file.write(struct.pack('L', int(self.unknown)))
        file.write(struct.pack('L', int(self.count)))

class md1_file:
    def __init__(self):
        self.header = md1_header()
        self.object = [] #md1_object[]

    def read_from_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_MD1] <READ> MD1_DATA\t(' + str(file.tell()) + ')')
        
        self.header = self.header.read(file)
        self.object = []

        for i in range(int(self.header.count / 2)):
            file.seek(offset + 12 + (i * 56))

            tmp_obj = md1_object()
            tmp_obj.header = tmp_obj.header.read(file)
        
            #triangle data handling...
            if tmp_obj.header.t_count > 0:
                #read vertices...
                file.seek(offset + 12 + tmp_obj.header.t_vertex_offset)
            
                for j in range(tmp_obj.header.t_vertex_count):
                    tmp_vertex = md1_vertex()
                    tmp_vertex = tmp_vertex.read(file)
                    tmp_obj.vertices.append(tmp_vertex)

                #read normals...
                file.seek(offset + 12 + tmp_obj.header.t_normal_offset)

                for j in range(tmp_obj.header.t_normal_count):
                    tmp_normal = md1_normal()
                    tmp_normal = tmp_normal.read(file)
                    tmp_obj.normals.append(tmp_normal)

                #read faces...
                file.seek(offset + 12 + tmp_obj.header.t_offset)

                for j in range(tmp_obj.header.t_count):
                    tmp_triangle = md1_triangle()
                    tmp_triangle = tmp_triangle.read(file)
                    tmp_obj.triangles.append(tmp_triangle)

                #read uv...
                file.seek(offset + 12 + tmp_obj.header.t_uv_offset)

                for j in range(tmp_obj.header.t_count):
                    tmp_triangle_uv = md1_triangle_uv()
                    tmp_triangle_uv = tmp_triangle_uv.read(file)
                    tmp_obj.triangles_uv.append(tmp_triangle_uv)

            #quadrangle data handling...
            if tmp_obj.header.q_count > 0:
                
                if len(tmp_obj.triangles) == 0:
                    #read vertices...
                    file.seek(offset + 12 + tmp_obj.header.q_vertex_offset)

                    for j in range(tmp_obj.header.q_vertex_count):
                        tmp_vertex = md1_vertex()
                        tmp_vertex = tmp_vertex.read(file)
                        tmp_obj.vertices.append(tmp_vertex)

                if len(tmp_obj.normals) == 0:
                    #read normals...
                    file.seek(offset + 12 + tmp_obj.header.q_normal_offset)

                    for j in range(tmp_obj.header.q_normal_count):
                        tmp_normal = md1_normal()
                        tmp_normal = tmp_normal.read(file)
                        tmp_obj.normals.append(tmp_normal)

                #read faces...
                file.seek(offset + 12 + tmp_obj.header.q_offset)

                for j in range(tmp_obj.header.q_count):
                    tmp_quadrangle = md1_quadrangle()
                    tmp_quadrangle = tmp_quadrangle.read(file)
                    tmp_obj.quadrangles.append(tmp_quadrangle)

                #read uv...
                file.seek(offset + 12 + tmp_obj.header.q_uv_offset)

                for j in range(tmp_obj.header.q_count):
                    tmp_quadrangle_uv = md1_quadrangle_uv()
                    tmp_quadrangle_uv = tmp_quadrangle_uv.read(file)
                    tmp_obj.quadrangles_uv.append(tmp_quadrangle_uv)

            self.object.append(tmp_obj)

        return self
    
    def read_from_file(self, filepath):
        print('[LIB_MD1] <READ> MD1_FILE\t(' + filepath + ')')

        file = open(filepath, 'rb')
        self.read_from_stream(file, 0)
        file.close()

        return self

    def write_to_stream(self, file, offset):
        file.seek(offset)
        print('[LIB_MD1] <WRITE> MD1_DATA\t(' + str(file.tell()) + ')')

        self.header.write(file)

        for i in range(len(self.object)):
            self.object[i].header.write(file)

        for i in range(len(self.object)):
            #write vertices
            file.seek(offset + 12 + self.object[i].header.t_vertex_offset)

            for j in range(len(self.object[i].vertices)):
                self.object[i].vertices[j].write(file)

            #write normals
            file.seek(offset + 12 + self.object[i].header.t_normal_offset)

            for j in range(len(self.object[i].normals)):
                self.object[i].normals[j].write(file)

            #write triangles
            if len(self.object[i].triangles) > 0:
                file.seek(offset + 12 + self.object[i].header.t_offset)

                for j in range(len(self.object[i].triangles)):
                    self.object[i].triangles[j].write(file)
                
                #write uv...
                file.seek(offset + 12 + self.object[i].header.t_uv_offset)

                for j in range(len(self.object[i].triangles_uv)):
                    self.object[i].triangles_uv[j].write(file)

            #write quadrangles
            if len(self.object[i].quadrangles) > 0:
                file.seek(offset + 12 + self.object[i].header.q_offset)

                for j in range(len(self.object[i].quadrangles)):
                    self.object[i].quadrangles[j].write(file)

                #write uv...
                file.seek(offset + 12 + self.object[i].header.q_uv_offset)

                for j in range(len(self.object[i].quadrangles_uv)):
                    self.object[i].quadrangles_uv[j].write(file)
    
    def write_to_file(self, filepath):
        if self.header.count > 0 and len(self.object) > 0:
            print('[LIB_MD1] <WRITE> MD1_FILE\t(' + filepath + ')')

            file = open(filepath, 'wb')
            self.write_to_stream(file, 0)
            file.close()