########################################################################################################################
# LIB_TMD - SONY PLAYSTATION 3D MODEL FORMAT
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct

#TO DO: SAVE TMD FILE FUNCTION!
	
class tmd_vertex:
	def __init_(self):
		self.x = 0	#int16
		self.y = 0	#int16
		self.z = 0	#int16
		self.zero = 0 #uint16

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

class tmd_normal:
	def __init_(self):
		self.x = 0	#int16
		self.y = 0	#int16
		self.z = 0	#int16
		self.zero = 0 #uint16

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

class tmd_primitve_header:
	def __init__(self):
		self.unknown_0 = 0
		self.length = 0
		self.unknown_1 = 0
		self.type = 0

	def read(self, file):
		self.unknown_0 = int(struct.unpack("B", file.read(1))[0])
		self.length = int(struct.unpack("B", file.read(1))[0])
		self.unknown_1 = int(struct.unpack("B", file.read(1))[0])
		self.type = int(struct.unpack("B", file.read(1))[0])
		return self

	def write(self, file):
		file.write(struct.pack('B', int(self.unknown_0)))
		file.write(struct.pack('B', int(self.length)))
		file.write(struct.pack('B', int(self.unknown_1)))
		file.write(struct.pack('B', int(self.type)))

#0x34; uv-textured triangle
class tmd_primitive_0x34:
	def __init__(self):
		self.unknown = 0  #uint32; tmd_primitive_header...
		self.tu_0 = 0	 #byte;
		self.tv_0 = 0	 #byte;
		self.clut = 0	 #uint16; texture clut id, bits 0-5
		self.tu_1 = 0	 #byte;
		self.tv_1 = 0	 #byte;
		self.page = 0	 #uint16;
		self.tu_2 = 0	 #byte;
		self.tv_2 = 0	 #byte;
		self.zero = 0	 #uint16;
		self.normal_0 = 0 #uint16;
		self.vertex_0 = 0 #uint16;
		self.normal_1 = 0 #uint16;
		self.vertex_1 = 0 #uint16;
		self.normal_2 = 0 #uint16;
		self.vertex_2 = 0 #uint16;

	def read(self, file):
		self.unknown = int(struct.unpack("L", file.read(4))[0])
		self.tu_0 = int(struct.unpack("B", file.read(1))[0])
		self.tv_0 = int(struct.unpack("B", file.read(1))[0])
		self.clut = int(struct.unpack("H", file.read(2))[0])
		self.tu_1 = int(struct.unpack("B", file.read(1))[0])
		self.tv_1 = int(struct.unpack("B", file.read(1))[0])
		self.page = int(struct.unpack("H", file.read(2))[0])
		self.tu_2 = int(struct.unpack("B", file.read(1))[0])
		self.tv_2 = int(struct.unpack("B", file.read(1))[0])
		self.zero = int(struct.unpack("H", file.read(2))[0])
		self.normal_0 = int(struct.unpack("H", file.read(2))[0])
		self.vertex_0 = int(struct.unpack("H", file.read(2))[0])
		self.normal_1 = int(struct.unpack("H", file.read(2))[0])
		self.vertex_1 = int(struct.unpack("H", file.read(2))[0])
		self.normal_2 = int(struct.unpack("H", file.read(2))[0])
		self.vertex_2 = int(struct.unpack("H", file.read(2))[0])
		return self

	def write(self, file):
		file.write(struct.pack('L', int(self.unknown)))
		file.write(struct.pack('B', int(self.tu_0)))
		file.write(struct.pack('B', int(self.tv_0)))
		file.write(struct.pack('H', int(self.clut)))
		file.write(struct.pack('B', int(self.tu_1)))
		file.write(struct.pack('B', int(self.tv_1)))
		file.write(struct.pack('H', int(self.page)))
		file.write(struct.pack('B', int(self.tu_2)))
		file.write(struct.pack('B', int(self.tv_2)))
		file.write(struct.pack('H', int(self.zero)))
		file.write(struct.pack('H', int(self.normal_0)))
		file.write(struct.pack('H', int(self.vertex_0)))
		file.write(struct.pack('H', int(self.normal_1)))
		file.write(struct.pack('H', int(self.vertex_1)))
		file.write(struct.pack('H', int(self.normal_2)))
		file.write(struct.pack('H', int(self.vertex_2)))

class tmd_object_header:
	def __init__(self):
		self.vertex_offset = 0	#uint32;
		self.vertex_count = 0	 #uint32;
		self.normal_offset = 0	#uint32;
		self.normal_count = 0	 #uint32;
		self.primitive_offset = 0 #uint32;
		self.primitive_count = 0  #uint32;
		self.dummy = 0			#uint32;

	def read(self, file):
		self.vertex_offset = int(struct.unpack("L", file.read(4))[0])
		self.vertex_count = int(struct.unpack("L", file.read(4))[0])
		self.normal_offset =int(struct.unpack("L", file.read(4))[0])
		self.normal_count = int(struct.unpack("L", file.read(4))[0])
		self.primitive_offset = int(struct.unpack("L", file.read(4))[0])
		self.primitive_count = int(struct.unpack("L", file.read(4))[0])
		self.dummy = int(struct.unpack("L", file.read(4))[0])
		return self

	def write(self, file):
		file.write(struct.pack('L', int(self.vertex_offset)))
		file.write(struct.pack('L', int(self.vertex_count)))
		file.write(struct.pack('L', int(self.normal_offset)))
		file.write(struct.pack('L', int(self.normal_count)))
		file.write(struct.pack('L', int(self.primitive_offset)))
		file.write(struct.pack('L', int(self.primitive_count)))
		file.write(struct.pack('L', int(self.dummy)))

class tmd_object:
	def __init__(self):
		self.header = tmd_object_header()
		self.vertices = []	   #tmd_vertx array
		self.normals = []		#tmd_normal array
		self.primitives = []	 #

class tmd_header:
	def __init__(self):
		self.id = 0	#uint32; always 0x41
		self.unknown = 0   #uint32; 
		self.count = 0 #uint32; 

	def read(self, file):
		self.id = int(struct.unpack("L", file.read(4))[0])
		self.unknown = int(struct.unpack("L", file.read(4))[0])
		self.count = int(struct.unpack("L", file.read(4))[0])
		return self
	
	def write(self, file):
		file.write(struct.pack('L', int(self.id)))
		file.write(struct.pack('L', int(self.unknown)))
		file.write(struct.pack('L', int(self.count)))

class tmd_file:
	def __init__(self):
		self.header = tmd_header() #tmd_header
		self.object = []		   #tmd_object array

	def read_from_stream(self, file, offset):
		file.seek(offset)
		print('[LIB_TMD] <READ> TMD_DATA\t(' + str(file.tell()) + ')')

		self.header = self.header.read(file)
		self.object = []

		for i in range(self.header.count):
			file.seek(offset + 12 + (i * 28))

			tmp_obj = tmd_object()
			tmp_obj.header = tmp_obj.header.read(file)

			if tmp_obj.header.primitive_count > 0:
				#read vertices...
				file.seek(offset + 12 + tmp_obj.header.vertex_offset)
			
				for j in range(tmp_obj.header.vertex_count):
					tmp_vertex = tmd_vertex()
					tmp_vertex = tmp_vertex.read(file)
					tmp_obj.vertices.append(tmp_vertex)

				#read normals...
				file.seek(offset + 12 + tmp_obj.header.normal_offset)

				for j in range(tmp_obj.header.normal_count):
					tmp_normal = tmd_normal()
					tmp_normal = tmp_normal.read(file)
					tmp_obj.normals.append(tmp_normal)

				#read triangles...
				file.seek(offset + 12 + tmp_obj.header.primitive_offset)

				for j in range(tmp_obj.header.primitive_count):
					tmp_triangle = tmd_primitive_0x34()
					tmp_triangle = tmp_triangle.read(file)
					tmp_obj.primitives.append(tmp_triangle)

				self.object.append(tmp_obj)
				print(str(i))

		return self

	def read_from_file(self, filepath):
		print('[LIB_TMD] <READ> TMD_FILE\t(' + filepath + ')')

		file = open(filepath, 'rb')
		self.read_from_stream(file, 0)
		file.close()

		return self

	def write_to_stream(self, file, offset):
		file.seek(offset)
		print('[LIB_TMD] <WRITE> TMD_DATA\t(' + str(file.tell()) + ')')

		for i in range(self.header.count):
			self.object[i].header.write(file)
		
		for i in range(self.header.count):
			if self.object[i].header.primitive_count > 0:
				#write vertices...
				file.seek(offset + 12 + self.object[i].header.vertex_offset)
			
				for j in range(self.object[i].header.vertex_count):
					self.object[i].vertices[j].write(file)

				#read normals...
				file.seek(offset + 12 + self.object[i].header.normal_offset)

				for j in range(self.object[i].header.normal_count):
					self.object[i].normals[j].write(file)

				#read triangles...
				file.seek(offset + 12 + self.object[i].header.primitive_offset)

				for j in range(self.object[i].header.primitive_count):
					self.object[i].primitives[j].write(file)

	def write_to_file(self, filepath):
		if self.header.count > 0 and len(self.object) > 0:
			print('[LIB_TMD] <WRITE> TMD_FILE\t(' + filepath + ')')

			file = open(filepath, 'wb')
			self.write_to_stream(file, 0)
			file.close()