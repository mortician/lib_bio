########################################################################################################################
# LIB_EMW - BIO HAZARD PLAYER WEAPON MODELS
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct
import os

import lib_bio.lib_rbj as lib_rbj
import lib_bio.lib_tmd as lib_tmd

class emw_file:
    def __init__(self):
        self.emr = lib_rbj.emr_file(1.0)
        self.edd = lib_rbj.edd_file()
        self.tmd = lib_tmd.tmd_file()
        self.o_edd = 0 #uint32; offset of edd file
        self.o_tmd = 0 #uint32; offset to tmd file

    def read(self, filepath):
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                print('[LIB_EMW] <READ> EMW_FILE\t(' + filepath + ')')

                file_size = os.path.getsize(filepath)
                file = open(filepath, 'rb')
                file.seek(file_size - 8)

                self.o_edd = int(struct.unpack("L", file.read(4))[0])
                self.o_tmd = int(struct.unpack("L", file.read(4))[0])   
                self.edd = self.edd.read_from_stream(file, self.o_edd)
                self.emr = self.emr.read_from_stream(file, 0, self.edd.frame_count)
                
                self.tmd = self.tmd.read_from_stream(file, self.o_tmd)
                file.close()

                return self

            else:
                print('[LIB_EMW] <ERROR> EXPECTED FILE BUT GOT PATH')
        else:
            print('[LIB_EMW] <ERROR> FILE (' + filepath.upper() + ') NOT FOUND')