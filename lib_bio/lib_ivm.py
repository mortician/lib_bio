########################################################################################################################
# LIB_IVM - BIO HAZARD ITEM CHECK/INVENTORY MODELS
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct
import os

import lib_bio.lib_tim as lib_tim
import lib_bio.lib_tmd as lib_tmd

class ivm_file:
    def __init__(self):
        self.tim = lib_tim.tim_file()
        self.tmd = lib_tmd.tmd_file()

    def read(self, filepath):
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                print('[LIB_IVM] <READ> IVM_FILE\t(' + filepath + ')')

                file = open(filepath, 'rb')
                self.tim = self.tim.read_from_stream(file, 0)
                self.tmd = self.tmd.read_from_stream(file, 66080)
                file.close()

                return self

            else:
                print('[LIB_IVM] <ERROR> EXPECTED FILE BUT GOT PATH')
        else:
            print('[LIB_IVM] <ERROR> FILE (' + filepath.upper() + ') NOT FOUND')