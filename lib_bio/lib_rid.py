########################################################################################################################
# LIB_RID - CAMERA DATA
########################################################################################################################
# SUPPORTED:
#      BIO HAZARD
#      BIOHAZARD 2 PROTOTYPE (NOV/1996)
#      BIOHAZARD 2
#      BIOHAZARD 3: LAST ESCAPE
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct
import os

class rid_object:
	def __init__(self, version):
		self.version = version		#float; custom value to keep track of file format version

		#BIO HAZARD
		if self.version == 1.0:
			self.o_pri = 0 #uint32; offset to .pri data for this camera
			self.o_tim = 0 #uint32; offset to .tim image data for this camera
			self.x = 0  #uint32; camera x-coordinate
			self.y = 0  #int32; camera y-coordinate
			self.z = 0  #uint32; camera z-coordinate
			self.target_x = 0 #uint32; camera target x-coordinate
			self.target_y = 0 #int32; camera target y-coordinate
			self.target_z = 0 #uint32; camera target z-coordinate
			self.roll = 0  #uint32; ?
			self.zero = 0  #uint32; dummy data?
			self.fov = 0   #uint32; field of view

		#BIOHAZARD 1.5, 2 & 3
		if self.version == 2.0:
			self.flag = 0  #uint16; this will be 1 if the object is last in row
			self.fov = 0   #uint16; field of view
			self.x = 0  #int32; camera x-coordinate 
			self.y = 0  #int32; camera y-coordinate 
			self.z = 0  #int32; camera z-coordinate 
			self.target_x = 0 #int32; camera target x-coordinate 
			self.target_y = 0 #int32; camera target y-coordinate 
			self.target_z = 0 #int32; camera target z-coordinate 
			self.o_pri = 0 #uint32; offset to .pri data for this camera

	def read(self, file):
		#print('[LIB_RID] <READ> RID_OBJECT ' + str(self.version) + '\t(' + str(file.tell()) + ')')

		#BIO HAZARD
		if self.version == 1.0:
			self.o_pri = int(struct.unpack("L", file.read(4))[0])
			self.o_tim = int(struct.unpack("L", file.read(4))[0])
			self.x = int(struct.unpack("L", file.read(4))[0])
			self.y = int(struct.unpack("l", file.read(4))[0])
			self.z = int(struct.unpack("L", file.read(4))[0])
			self.target_x = int(struct.unpack("L", file.read(4))[0])
			self.target_y = int(struct.unpack("l", file.read(4))[0])
			self.target_z = int(struct.unpack("L", file.read(4))[0])
			self.roll = int(struct.unpack("L", file.read(4))[0])
			self.zero = int(struct.unpack("L", file.read(4))[0])
			self.fov = int(struct.unpack("L", file.read(4))[0])

		#BIOHAZARD 1.5, 2 & 3
		if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
			self.flag = int(struct.unpack("H", file.read(2))[0])
			self.fov = int(struct.unpack("H",file.read(2))[0])
			self.x = int(struct.unpack("l", file.read(4))[0])
			self.y = int(struct.unpack("l", file.read(4))[0])
			self.z = int(struct.unpack("l", file.read(4))[0])
			self.target_x = int(struct.unpack("l", file.read(4))[0])
			self.target_y = int(struct.unpack("l", file.read(4))[0])
			self.target_z = int(struct.unpack("l", file.read(4))[0])
			self.o_pri = int(struct.unpack("L", file.read(4))[0])

		return self

	def write(self, file):
	#print('[LIB_RID] <WRITE> RID_OBJECT ' + str(self.version) + '\t(' + str(file.tell()) + ')')
	
		#BIO HAZARD
		if self.version == 1.0:
			file.write(struct.pack('L', int(self.o_pri)))
			file.write(struct.pack('L', int(self.o_tim)))
			file.write(struct.pack('L', int(self.x)))
			file.write(struct.pack('l', int(self.y)))
			file.write(struct.pack('L', int(self.z)))
			file.write(struct.pack('L', int(self.target_x)))
			file.write(struct.pack('l', int(self.target_y)))
			file.write(struct.pack('L', int(self.target_z)))
			file.write(struct.pack('L', int(self.roll)))
			file.write(struct.pack('L', int(self.zero)))
			file.write(struct.pack('L', int(self.fov)))

		#BIOHAZARD 1.5, 2 & 3
		if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
			file.write(struct.pack('H', int(self.flag)))
			file.write(struct.pack('H', int(self.fov)))
			file.write(struct.pack('l', int(self.x)))
			file.write(struct.pack('l', int(self.y)))
			file.write(struct.pack('l', int(self.z)))
			file.write(struct.pack('l', int(self.target_x)))
			file.write(struct.pack('l', int(self.target_y)))
			file.write(struct.pack('l', int(self.target_z)))
			file.write(struct.pack('L', int(self.o_pri)))

class rid_file:
	def __init__(self, version):
		self.version = version #float; custom value to keep track of file format version
		self.object = []    #rid_object[rdt_header.h_cut]; 

	def read_from_stream(self, file, offset, count):
		file.seek(offset)
		print('[LIB_RID] <READ> RID_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')
		self.object = []

		for i in range(count):
			tmp_obj = rid_object(self.version)
			tmp_obj = tmp_obj.read(file)
			self.object.append(tmp_obj)

		return self

	def read_from_file(self, filepath):
		print('[LIB_RID] <READ> RID_FILE ' + str(self.version) + '\t(' + filepath.upper() + ')')
		count = 0

		if self.version == 1.0:
			count = int(os.path.getsize(filepath) / 44)

		if self.version == 2.0:
			count = int(os.path.getsize(filepath) / 32)

		if count > 1:
			file = open(filepath, 'rb')
			self = self.read_from_stream(file, 0, count)
			file.close()

		return self

	def write_to_stream(self, file, offset):
		file.seek(offset)
		print('[LIB_RID] <WRITE> RID_DATA ' + str(self.version) + '\t(' + str(file.tell()) + ')')

		for i in range(len(self.object)):
			self.object[i].write(file)

	def write_to_file(self, filepath):
		print('[LIB_RID] <WRITE> RID_FILE ' + str(self.version) + '\t(' + filepath.upper() + ')')

		file = open(filepath, 'wb')

		for i in range(len(self.object)):
			self.object[i].write(file)

		file.close()
