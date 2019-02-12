########################################################################################################################
# LIB_EMD - PC & NPC MODELS
########################################################################################################################
# SUPPORTED:
#               BIO HAZARD
#               BIOHAZARD 2 PROTOTYPE (NOV/1996)
#               BIOHAZARD 2
#               !!!BIOHAZARD 3: LAST ESCAPE      MISSING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import struct
import os

import lib_bio.lib_md1 as lib_md1
import lib_bio.lib_md2 as lib_md2
import lib_bio.lib_rbj as lib_rbj
import lib_bio.lib_tim as lib_tim
import lib_bio.lib_tmd as lib_tmd

class emd_file:
    def __init__(self, version):
        self.version = version

        if self.version == 1.0:
            self.emr_0 = lib_rbj.emr_file(self.version)
            self.edd_0 = lib_rbj.edd_file()
            self.emr_1 = lib_rbj.emr_file(self.version)
            self.edd_1 = lib_rbj.edd_file()
            self.tmd = lib_tmd.tmd_file()
            self.tim = lib_tim.tim_file()
            self.o_edd_0 = 0 #uint32; offset to first .edd file
            self.o_emr_1 = 0 #uint32; offset to second .emr file
            self.o_edd_1 = 0 #uint32; offset to second .edd file
            self.o_tmd = 0   #uint32; offset to model file
            self.o_tim = 0   #uint32; offset to texture file

        if self.version == 1.5:
            self.emr_0 = lib_rbj.emr_file(self.version)
            self.edd_0 = lib_rbj.edd_file()
            self.emr_1 = lib_rbj.emr_file(self.version)
            self.edd_1 = lib_rbj.edd_file()
            self.md1 = lib_tmd.tmd_file()
            self.tim = lib_tim.tim_file()

        if self.version == 2.0:
            self.o_dir = 0
            self.dir_count = 0
            self.edd_0 = lib_rbj.edd_file()
            self.emr_0 = lib_rbj.emr_file(self.version)
            self.edd_0 = lib_rbj.edd_file()
            self.emr_0 = lib_rbj.emr_file(self.version)
            self.edd_0 = lib_rbj.edd_file()
            self.emr_0 = lib_rbj.emr_file(self.version)
            self.md1 = lib_md1.md1_file()
            self.o_unk = 0
            self.o_edd_0 = 0
            self.o_emr_0 = 0
            self.o_edd_1 = 0
            self.o_emr_1 = 0
            self.o_edd_2 = 0
            self.o_emr_2 = 0
            self.o_md1 = 0

    def read_from_file(self, filepath):
        file = open(filepath, 'rb')

        if self.version == 1.0:
            file.seek(-20, 2)

            self.o_edd_0 = int(struct.unpack("L", file.read(4))[0])
            self.o_emr_1 = int(struct.unpack("L", file.read(4))[0])
            self.o_edd_1 = int(struct.unpack("L", file.read(4))[0])
            self.o_tmd = int(struct.unpack("L", file.read(4))[0])
            self.o_tim = int(struct.unpack("L", file.read(4))[0])

            if self.o_edd_0 == 0 and self.o_emr_1 == 0:
                self.edd_1 = self.edd_1.read_from_stream(file, self.o_edd_1)
                self.emr_1 = self.emr_1.read_from_stream(file, 0, self.edd_1.frame_count)
            else:
                self.edd_0 = self.edd_0.read_from_stream(file, self.o_edd_0)
                self.emr_0 = self.emr_0.read_from_stream(file, 0, self.edd_0.frame_count)
                self.edd_1 = self.edd_1.read_from_stream(file, self.o_edd_1)
                self.emr_1 = self.emr_1.read_from_stream(file, self.o_emr_1, self.edd_1.frame_count)

            self.tmd = self.tmd.read_from_stream(file, self.o_tmd)
            self.tim = self.tim.read_from_stream(file, self.o_tim)
            print(self.o_edd_0)
            print(self.o_emr_1)
            print(self.o_edd_1)
            print(self.o_tmd)
            print(self.o_tim)

            file.close()

            return self