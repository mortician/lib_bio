########################################################################################################################
# LIB_DO2 - BIO HAZARD DOOR MODEL FILE
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct
import os

import lib_bio.lib_rbj as lib_rbj
import lib_bio.lib_tim as lib_tim
import lib_bio.lib_md1 as lib_md1

class dor_file_header:
	def __init__(self):
		o_rbj = 0
		o_md1 = 0
		o_tim = 0

class dor_file:
	def __init__(self):
		self.header = dor_file_header()
		self.rbj = lib_rbj.rbj_file()
		self.md1 = lib_md1.md1_file()
		self.tim = lib_tim.tim_file()

	def read(self, filepath):
		if os.path.exists(filepath):
			if os.path.isfile(filepath):
				print('[LIB_DO2] <READ> DO2_FILE\t(' + filepath + ')')

				#CODE IS NOT WORKING YET! USES BIO1 DOR CODE...

				file = open(filepath, 'rb')
				self.header.o_rbj = int(struct.unpack("L", file.read(4))[0])
				self.header.o_md1 = int(struct.unpack("L", file.read(4))[0])
				self.header.o_tim = int(struct.unpack("L", file.read(4))[0])
				self.tim = self.tim.read_from_stream(file, o_tmd)
				self.md1 = self.md1.read_from_stream(file, o_tim)
				file.close()

				return self

			else:
				print('[LIB_DO2] <ERROR> EXPECTED FILE BUT GOT PATH')
		else:
			print('[LIB_DO2] <ERROR> FILE (' + filepath.upper() + ') NOT FOUND')

