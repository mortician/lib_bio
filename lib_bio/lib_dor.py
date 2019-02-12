########################################################################################################################
# LIB_DOR - BIO HAZARD DOOR MODEL FILE
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct
import os

import lib_bio.lib_rbj as lib_rbj
import lib_bio.lib_tim as lib_tim
import lib_bio.lib_tmd as lib_tmd

class dor_file_header:
	def __init__(self):
		o_rbj = 0
		o_tmd = 0
		o_tim = 0

class dor_file:
	def __init__(self):
		self.header = dor_file_header()
		self.rbj = lib_rbj.rbj_file()
		self.tmd = lib_tmd.tmd_file()
		self.tim = lib_tim.tim_file()

	def read(self, filepath):
		if os.path.exists(filepath):
			if os.path.isfile(filepath):
				print('[LIB_DOR] <READ> DOR_FILE\t(' + filepath + ')')

				file = open(filepath, 'rb')
				self.header.o_rbj = int(struct.unpack("L", file.read(4))[0])
				self.header.o_tmd = int(struct.unpack("L", file.read(4))[0])
				self.header.o_tim = int(struct.unpack("L", file.read(4))[0])
				self.tim = self.tim.read_from_stream(file, o_tmd)
				self.tmd = self.tmd.read_from_stream(file, o_tim)
				file.close()

				return self

			else:
				print('[LIB_DOR] <ERROR> EXPECTED FILE BUT GOT PATH')
		else:
			print('[LIB_DOR] <ERROR> FILE (' + filepath.upper() + ') NOT FOUND')
