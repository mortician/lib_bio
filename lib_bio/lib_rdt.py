########################################################################################################################
# LIB_RDT - ROOM DATA
########################################################################################################################
# SUPPORTED:
#               BIO HAZARD
#               BIOHAZARD 2 PROTOTYPE (NOV/1996) "BIOHAZARD 1.5 PVB"
#               BIOHAZARD 2
#               BIOHAZARD 3: LAST ESCAPE
########################################################################################################################
# 2014-2019, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
import imp
import os
import struct
import lib_bio.lib_tools as lib_tools

import lib_bio.lib_blk as lib_blk
import lib_bio.lib_esp as lib_esp
import lib_bio.lib_flr as lib_flr
import lib_bio.lib_lit as lib_lit
import lib_bio.lib_md1 as lib_md1
import lib_bio.lib_md2 as lib_md2
import lib_bio.lib_pri as lib_pri
import lib_bio.lib_rbj as lib_rbj
import lib_bio.lib_rid as lib_rid
import lib_bio.lib_rvd as lib_rvd
import lib_bio.lib_sca as lib_sca
import lib_bio.lib_snd as lib_snd
import lib_bio.lib_tim as lib_tim
import lib_bio.lib_tmd as lib_tmd
import lib_bio.lib_vab as lib_vab

imp.reload(lib_tools)

imp.reload(lib_blk)
imp.reload(lib_esp)
imp.reload(lib_flr)
imp.reload(lib_lit)
imp.reload(lib_md1)
imp.reload(lib_md2)
imp.reload(lib_pri)
imp.reload(lib_rbj)
imp.reload(lib_rid)
imp.reload(lib_rvd)
imp.reload(lib_sca)
imp.reload(lib_snd)
imp.reload(lib_tim)
imp.reload(lib_tmd)
imp.reload(lib_vab)

#=======================================================================================================================
# GENERAL
#=======================================================================================================================
def get_rdt_version(filepath):
    file = open(filepath, 'rb')
    file.seek(1)
    h_cut = int(struct.unpack("B", file.read(1))[0])
    file.seek(36)
    o_rid = int(struct.unpack("L", file.read(4))[0])
    file.close()

    if h_cut <= 8 and o_rid > 124 and os.path.basename(filepath)[0:4].upper() == 'ROOM':
        return float(1.0)

    if h_cut < 17 and (o_rid == 96 or o_rid == 124) and os.path.basename(filepath)[0:4].upper() == 'ROOM':
        return float(1.5)

    if h_cut <= 17 and o_rid == 100 and os.path.basename(filepath)[0:4].upper() == 'ROOM':
        return float(2.0)

    if o_rid == 96 and os.path.basename(filepath)[0:4].upper() != 'ROOM':
        return float(3.0)

    return 0

def get_rdt_name(filepath):

    rdt_version = get_rdt_version(filepath)
    rdt_name = 'ROOMXXXX'

    if rdt_version == 1.0 or rdt_version == 1.5 or rdt_version == 2.0:
        rdt_name = os.path.basename(filepath)[0:8].upper()
    if rdt_version == 3.0:
        rdt_name = os.path.basename(filepath)[0:4].upper()

    return rdt_name

def get_rdt_dir(filepath):
    rdt_dir = os.path.dirname(filepath)
    
    return rdt_dir

#=======================================================================================================================
# FILE FORMAT HANDLING
#=======================================================================================================================
class rdt_header:
    def __init__(self, version):
        self.version = version

        #BIO HAZARD
        if self.version == 1.0:
            self.h_sprite = 0       #byte; 
            self.h_cut = 0          #byte; 
            self.h_object_model = 0 #byte; 
            self.h_item_model = 0   #byte; 
            self.h_item = 0         #byte; 
            self.h_door = 0         #byte; 
                                    #66 byte in length light data is located here
            self.o_rvd = 0          #uint32; 
            self.o_sca = 0          #uint32; 
            self.o_object_model = 0 #uint32; 
            self.o_item_model = 0   #uint32; 
            self.o_blk = 0          #uint32; 
            self.o_flr = 0          #uint32; 
            self.o_scd_main = 0     #uint32;
            self.o_scd_sub_0 = 0    #uint32;
            self.o_scd_sub_1 = 0    #uint32;
            self.o_emr = 0          #uint32;
            self.o_edd = 0          #uint32;
            self.o_msg = 0          #uint32;
            self.o_raw = 0          #uint32;
            self.o_esp = 0          #uint32;
            self.o_eff = 0          #uint32;
            self.o_tim_eff = 0      #uint32;
            self.o_snd = 0          #uint32;
            self.o_vh = 0           #uint32;
            self.o_vb = 0           #uint32;

        #BIOHAZARD 1.5
        if self.version == 1.5:
            self.h_sprite = 0     #byte; ?
            self.h_cut = 0        #byte; holds total number of cameras used
            self.h_model = 0      #byte; holds total number of models used
            self.h_item = 0       #byte; ?
            self.h_door = 0       #byte; ?
            self.h_room = 0       #byte; ?
            self.h_reverb = 0     #byte; is related to the sound...
            self.h_sprite_max = 0 #byte; max number of .pri sprites used by one of the room's cameras
            self.o_snd_0 = 0      #uint32; offset to room .snd sound table data
            self.o_vh_0 = 0       #uint32; offset to room .vab sound data header
            self.o_vb_0 = 0       #uint32; offset to room .vab sound data
            self.o_snd_1 = 0      #uint32; offset to room enemy .snd sound table data
            self.o_vh_1 = 0       #uint32; offset to room enemy .vab sound data header
            self.o_vb_1 = 0       #uint32; offset to room enemy .vab sound data
            self.o_sca = 0        #uint32; offset to .sca data
            self.o_rid = 0        #uint32; offset to .rid data
            self.o_rvd = 0        #uint32; offset to .rvd data
            self.o_lit = 0        #uint32; offset to .lit data
            self.o_model = 0      #uint32; offset to .md1 data
            self.o_flr = 0        #uint32; offset to .flr data
            self.o_blk = 0        #uint32; offset to .blk data
            self.o_msg = 0        #uint32; offset to .msg data
            self.o_scd_main = 0   #uint32; offset to main .scd data
            self.o_scd_sub_0 = 0  #uint32; offset to sub_0 .scd data
            self.o_scd_sub_1 = 0  #uint32; offset to sub_1 .scd data
            self.o_esp = 0        #uint32; offset to .esp data
            self.o_eff = 0        #uint32; offset to .eff data
            self.o_tim_eff = 0    #uint32; offset to effect .tim data
            self.o_tim_model = 0  #uint32; offset to model .tim data
            self.o_rbj = 0        #uint32; offset to .rbj data

        #BIOHAZARD 2
        if self.version == 2.0:
            self.h_sprite = 0     #byte; 
            self.h_cut = 0        #byte; 
            self.h_model = 0      #byte; 
            self.h_item = 0       #byte; 
            self.h_door = 0       #byte; 
            self.h_room = 0       #byte; 
            self.h_reverb = 0     #byte; 
            self.h_sprite_max = 0 #byte; 
            self.o_snd = 0        #uint32; offset to . data in file
            self.o_vh_0 = 0       #uint32; offset to . data in file
            self.o_vb_0 = 0       #uint32; offset to . data in file
            self.o_vh_1 = 0       #uint32; offset to . data in file
            self.o_vb_1 = 0       #uint32; offset to . data in file
            self.o_ota = 0        #uint32; offset to . data in file
            self.o_sca = 0        #uint32; offset to . data in file
            self.o_rid = 0        #uint32; offset to . data in file
            self.o_rvd = 0        #uint32; offset to . data in file
            self.o_lit = 0        #uint32; offset to . data in file
            self.o_model = 0      #uint32; offset to . data in file
            self.o_flr = 0        #uint32; offset to . data in file
            self.o_blk = 0        #uint32; offset to . data in file
            self.o_msg_main = 0   #uint32; offset to . data in file
            self.o_msg_sub = 0    #uint32; offset to . data in file
            self.o_tim_cam = 0    #uint32; offset to . data in file
            self.o_scd_main = 0   #uint32; offset to . data in file
            self.o_scd_sub = 0    #uint32; offset to . data in file
            self.o_esp = 0        #uint32; offset to . data in file
            self.o_eff = 0        #uint32; offset to . data in file
            self.o_tim_eff = 0    #uint32; offset to . data in file
            self.o_tim_model = 0  #uint32; offset to . data in file
            self.o_rbj = 0        #uint32; offset to . data in file
        
        #BIOHAZARD 3: LAST ESCAPE
        if self.version == 3.0:
            self.h_sprite = 0     #byte; ?
            self.h_cut = 0        #byte; holds total number of cameras used
            self.h_model = 0      #byte; holds total number of models used
            self.h_item = 0       #byte; ?
            self.h_door = 0       #byte; ?
            self.h_room = 0       #byte; ?
            self.h_reverb = 0     #byte; is related to the sound...
            self.h_sprite_max = 0 #byte; max number of .pri sprites used by one of the room's cameras
            self.o_snd = 0        #uint32;
            self.o_vh_0 = 0       #uint32;
            self.o_vb_0 = 0       #uint32;
            self.o_vh_1 = 0       #uint32;
            self.o_vb_1 = 0       #uint32;
            self.o_ota = 0        #uint32;
            self.o_sca = 0        #uint32;
            self.o_rid = 0        #uint32;
            self.o_rvd = 0        #uint32;
            self.o_lit = 0        #uint32;
            self.o_model = 0      #uint32;
            self.o_flr = 0        #uint32;
            self.o_blk = 0        #uint32;
            self.o_msg_0 = 0      #uint32;
            self.o_msg_1 = 0      #uint32;
            self.o_tim_cam = 0    #uint32;
            self.o_scd = 0        #uint32;
            self.o_esp = 0        #uint32;
            self.o_eff = 0        #uint32;
            self.o_unknown_0 = 0  #uint32; camera related data? seems to utilize h_cut...
            self.o_tim_model = 0  #uint32;
            self.o_unknown_1 = 0  #uint32;

    def read(self, file):
        print('[LIB_RDT] <READ> RDT_HEADER ' + str(self.version) + '\t(' + str(file.tell()) + ')')
        
        #BIO HAZARD
        if self.version == 1.0:
            self.h_sprite = int(struct.unpack("B", file.read(1))[0])
            self.h_cut = int(struct.unpack("B", file.read(1))[0])
            self.h_object_model = int(struct.unpack("B", file.read(1))[0])
            self.h_item_model = int(struct.unpack("B", file.read(1))[0])
            self.h_item = int(struct.unpack("B", file.read(1))[0])
            self.h_door = int(struct.unpack("B", file.read(1))[0])
        
            file.seek(66, 1)     #skip lit data for now
        
            self.o_rvd = int(struct.unpack("L", file.read(4))[0])
            self.o_sca = int(struct.unpack("L", file.read(4))[0])
            #self.o_object_model = int(struct.unpack("L", file.read(4))[0])
            #self.o_item_model = int(struct.unpack("L", file.read(4))[0])
            self.o_blk = int(struct.unpack("L", file.read(4))[0])
            self.o_flr = int(struct.unpack("L", file.read(4))[0])
            self.o_scd_main = int(struct.unpack("L", file.read(4))[0])
            self.o_scd_sub_0 = int(struct.unpack("L", file.read(4))[0])
            self.o_scd_sub_1 = int(struct.unpack("L", file.read(4))[0])
            self.o_emr = int(struct.unpack("L", file.read(4))[0])
            self.o_edd = int(struct.unpack("L", file.read(4))[0])
            self.o_msg = int(struct.unpack("L", file.read(4))[0])
            self.o_raw = int(struct.unpack("L", file.read(4))[0])
            self.o_esp = int(struct.unpack("L", file.read(4))[0])
            self.o_eff = int(struct.unpack("L", file.read(4))[0])
            #self.o_tim_eff = int(struct.unpack("L", file.read(4))[0])
            self.o_snd = int(struct.unpack("L", file.read(4))[0])
            self.o_vh = int(struct.unpack("L", file.read(4))[0])
            self.o_vb = int(struct.unpack("L", file.read(4))[0])
        
        #BIOHAZARD 1.5
        if self.version == 1.5:
            self.h_sprite = int(struct.unpack("B", file.read(1))[0])
            self.h_cut = int(struct.unpack("B", file.read(1))[0])
            self.h_model = int(struct.unpack("B", file.read(1))[0])
            self.h_item = int(struct.unpack("B", file.read(1))[0])
            self.h_door = int(struct.unpack("B", file.read(1))[0])
            self.h_room = int(struct.unpack("B", file.read(1))[0])
            self.h_reverb = int(struct.unpack("B", file.read(1))[0])
            self.h_sprite_max  = int(struct.unpack("B", file.read(1))[0])
            self.o_snd_0 = int(struct.unpack("L", file.read(4))[0])
            self.o_vh_0 = int(struct.unpack("L", file.read(4))[0])
            self.o_vb_0 = int(struct.unpack("L", file.read(4))[0])
            self.o_snd_1 = int(struct.unpack("L", file.read(4))[0])
            self.o_vh_1 = int(struct.unpack("L", file.read(4))[0])
            self.o_vb_1 = int(struct.unpack("L", file.read(4))[0])
            self.o_sca = int(struct.unpack("L", file.read(4))[0])
            self.o_rid = int(struct.unpack("L", file.read(4))[0])
            self.o_rvd = int(struct.unpack("L", file.read(4))[0])
            self.o_lit = int(struct.unpack("L", file.read(4))[0])
            self.o_model = int(struct.unpack("L", file.read(4))[0])
            self.o_flr = int(struct.unpack("L", file.read(4))[0])
            self.o_blk = int(struct.unpack("L", file.read(4))[0])
            self.o_msg = int(struct.unpack("L", file.read(4))[0])
            self.o_scd_main = int(struct.unpack("L", file.read(4))[0])
            self.o_scd_sub_0 = int(struct.unpack("L", file.read(4))[0])
            self.o_scd_sub_1 = int(struct.unpack("L", file.read(4))[0])
            self.o_esp = int(struct.unpack("L", file.read(4))[0])
            self.o_eff = int(struct.unpack("L", file.read(4))[0])
            self.o_tim_eff = int(struct.unpack("L", file.read(4))[0])
            self.o_tim_model = int(struct.unpack("L", file.read(4))[0])
            self.o_rbj = int(struct.unpack("L", file.read(4))[0])
        
        #BIOHAZARD 2
        if self.version == 2.0:
            self.h_sprite = int(struct.unpack("B", file.read(1))[0])
            self.h_cut = int(struct.unpack("B", file.read(1))[0])
            self.h_model = int(struct.unpack("B", file.read(1))[0])
            self.h_item = int(struct.unpack("B", file.read(1))[0])
            self.h_door = int(struct.unpack("B", file.read(1))[0])
            self.h_room = int(struct.unpack("B", file.read(1))[0])
            self.h_reverb = int(struct.unpack("B", file.read(1))[0])
            self.h_sprite_max = int(struct.unpack("B", file.read(1))[0])
            self.o_snd = int(struct.unpack("L", file.read(4))[0])
            self.o_vh_0 = int(struct.unpack("L", file.read(4))[0])
            self.o_vb_0 = int(struct.unpack("L", file.read(4))[0])
            self.o_vh_1 = int(struct.unpack("L", file.read(4))[0])
            self.o_vb_1 = int(struct.unpack("L", file.read(4))[0])
            self.o_ota = int(struct.unpack("L", file.read(4))[0])
            self.o_sca = int(struct.unpack("L", file.read(4))[0])
            self.o_rid = int(struct.unpack("L", file.read(4))[0])
            self.o_rvd = int(struct.unpack("L", file.read(4))[0])
            self.o_lit = int(struct.unpack("L", file.read(4))[0])
            self.o_model = int(struct.unpack("L", file.read(4))[0])
            self.o_flr = int(struct.unpack("L", file.read(4))[0])
            self.o_blk = int(struct.unpack("L", file.read(4))[0])
            self.o_msg_main = int(struct.unpack("L", file.read(4))[0])
            self.o_msg_sub = int(struct.unpack("L", file.read(4))[0])
            self.o_tim_cam = int(struct.unpack("L", file.read(4))[0])
            self.o_scd_main = int(struct.unpack("L", file.read(4))[0])
            self.o_scd_sub = int(struct.unpack("L", file.read(4))[0])
            self.o_esp = int(struct.unpack("L", file.read(4))[0])
            self.o_eff = int(struct.unpack("L", file.read(4))[0])
            self.o_tim_eff = int(struct.unpack("L", file.read(4))[0])
            self.o_tim_model = int(struct.unpack("L", file.read(4))[0])
            self.o_rbj = int(struct.unpack("L", file.read(4))[0])

        #BIOHAZARD 3: LAST ESCAPE
        if self.version == 3.0:
            self.h_sprite = int(struct.unpack("B", file.read(1))[0])
            self.h_cut = int(struct.unpack("B", file.read(1))[0])
            self.h_model = int(struct.unpack("B", file.read(1))[0])
            self.h_item = int(struct.unpack("B", file.read(1))[0])
            self.h_door = int(struct.unpack("B", file.read(1))[0])
            self.h_room = int(struct.unpack("B", file.read(1))[0])
            self.h_reverb = int(struct.unpack("B", file.read(1))[0])
            self.h_sprite_max = int(struct.unpack("B", file.read(1))[0])
            self.o_snd = int(struct.unpack("L", file.read(4))[0])
            self.o_vh_0 = int(struct.unpack("L", file.read(4))[0])
            self.o_vb_0 = int(struct.unpack("L", file.read(4))[0])
            self.o_vh_1 = int(struct.unpack("L", file.read(4))[0])
            self.o_vb_1 = int(struct.unpack("L", file.read(4))[0])
            self.o_ota = int(struct.unpack("L", file.read(4))[0])
            self.o_sca = int(struct.unpack("L", file.read(4))[0])
            self.o_rid = int(struct.unpack("L", file.read(4))[0])
            self.o_rvd = int(struct.unpack("L", file.read(4))[0])
            self.o_lit = int(struct.unpack("L", file.read(4))[0])
            self.o_model = int(struct.unpack("L", file.read(4))[0])
            self.o_flr = int(struct.unpack("L", file.read(4))[0])
            self.o_blk = int(struct.unpack("L", file.read(4))[0])
            self.o_msg_main = int(struct.unpack("L", file.read(4))[0])
            self.o_msg_sub = int(struct.unpack("L", file.read(4))[0])
            self.o_tim_cam = int(struct.unpack("L", file.read(4))[0])
            self.o_scd = int(struct.unpack("L", file.read(4))[0])
            self.o_esp = int(struct.unpack("L", file.read(4))[0])
            self.o_eff = int(struct.unpack("L", file.read(4))[0])
            self.o_unknown_0 = int(struct.unpack("L", file.read(4))[0])
            self.o_tim_model = int(struct.unpack("L", file.read(4))[0])
            self.o_unknown_1 = int(struct.unpack("L", file.read(4))[0])

        return self

    def write(self, file):
        print('[LIB_RDT] <WRITE> RDT_HEADER ' + str(self.version) + '\t(' + str(file.tell()) + ')')

        #BIO HAZARD
        if self.version == 1.0: #TO DO!
            file.write(struct.pack('B', int(self.h_sprite)))
            file.write(struct.pack('B', int(self.h_cut)))
            file.write(struct.pack('B', int(self.h_object_model)))
            file.write(struct.pack('B', int(self.h_item_model)))
            file.write(struct.pack('B', int(self.h_item)))
            file.write(struct.pack('B', int(self.h_door)))
        
            file.seek(66, 1)     #skip lit data for now
        
            file.write(struct.pack('L', int(self.o_rvd)))
            file.write(struct.pack('L', int(self.o_sca)))
            file.write(struct.pack('L', int(self.o_object_model)))
            file.write(struct.pack('L', int(self.o_item_model)))
            file.write(struct.pack('L', int(self.o_blk)))
            file.write(struct.pack('L', int(self.o_flr)))
            file.write(struct.pack('L', int(self.o_scd_main)))
            file.write(struct.pack('L', int(self.o_scd_sub_0)))
            file.write(struct.pack('L', int(self.o_scd_sub_1)))
            file.write(struct.pack('L', int(self.o_emr)))
            file.write(struct.pack('L', int(self.o_edd)))
            file.write(struct.pack('L', int(self.o_msg)))
            file.write(struct.pack('L', int(self.o_raw)))
            file.write(struct.pack('L', int(self.o_esp)))
            file.write(struct.pack('L', int(self.o_eff)))
            file.write(struct.pack('L', int(self.o_tim_eff)))
            file.write(struct.pack('L', int(self.o_snd)))
            file.write(struct.pack('L', int(self.o_vh)))
            file.write(struct.pack('L', int(self.o_vb)))
       
        #BIOHAZARD 1.5
        if self.version == 1.5:
            file.write(struct.pack('B', int(self.h_sprite)))
            file.write(struct.pack('B', int(self.h_cut)))
            file.write(struct.pack('B', int(self.h_model)))
            file.write(struct.pack('B', int(self.h_item)))
            file.write(struct.pack('B', int(self.h_door)))
            file.write(struct.pack('B', int(self.h_room)))
            file.write(struct.pack('B', int(self.h_reverb)))
            file.write(struct.pack('B', int(self.h_sprite_max)))
            file.write(struct.pack('L', int(self.o_snd_0)))
            file.write(struct.pack('L', int(self.o_vh_0)))
            file.write(struct.pack('L', int(self.o_vb_0)))
            file.write(struct.pack('L', int(self.o_snd_1)))
            file.write(struct.pack('L', int(self.o_vh_1)))
            file.write(struct.pack('L', int(self.o_vb_1)))
            file.write(struct.pack('L', int(self.o_sca)))
            file.write(struct.pack('L', int(self.o_rid)))
            file.write(struct.pack('L', int(self.o_rvd)))
            file.write(struct.pack('L', int(self.o_lit)))
            file.write(struct.pack('L', int(self.o_model)))
            file.write(struct.pack('L', int(self.o_flr)))
            file.write(struct.pack('L', int(self.o_blk)))
            file.write(struct.pack('L', int(self.o_msg)))
            file.write(struct.pack('L', int(self.o_scd_main)))
            file.write(struct.pack('L', int(self.o_scd_sub_0)))
            file.write(struct.pack('L', int(self.o_scd_sub_1)))
            file.write(struct.pack('L', int(self.o_esp)))
            file.write(struct.pack('L', int(self.o_eff)))
            file.write(struct.pack('L', int(self.o_tim_eff)))
            file.write(struct.pack('L', int(self.o_tim_model)))
            file.write(struct.pack('L', int(self.o_rbj)))

        #BIOHAZARD 2
        if self.version == 2.0:
            file.write(struct.pack('B', int(self.h_sprite)))
            file.write(struct.pack('B', int(self.h_cut)))
            file.write(struct.pack('B', int(self.h_model)))
            file.write(struct.pack('B', int(self.h_item)))
            file.write(struct.pack('B', int(self.h_door)))
            file.write(struct.pack('B', int(self.h_room)))
            file.write(struct.pack('B', int(self.h_reverb)))
            file.write(struct.pack('B', int(self.h_sprite_max)))
            file.write(struct.pack('L', int(self.o_snd)))
            file.write(struct.pack('L', int(self.o_vh_0)))
            file.write(struct.pack('L', int(self.o_vb_0)))
            file.write(struct.pack('L', int(self.o_vh_1)))
            file.write(struct.pack('L', int(self.o_vb_1)))
            file.write(struct.pack('L', int(self.o_ota)))
            file.write(struct.pack('L', int(self.o_sca)))
            file.write(struct.pack('L', int(self.o_rid)))
            file.write(struct.pack('L', int(self.o_rvd)))
            file.write(struct.pack('L', int(self.o_lit)))
            file.write(struct.pack('L', int(self.o_model)))
            file.write(struct.pack('L', int(self.o_flr)))
            file.write(struct.pack('L', int(self.o_blk)))
            file.write(struct.pack('L', int(self.o_msg_main)))
            file.write(struct.pack('L', int(self.o_msg_sub)))
            file.write(struct.pack('L', int(self.o_tim_cam)))
            file.write(struct.pack('L', int(self.o_scd_main)))
            file.write(struct.pack('L', int(self.o_scd_sub)))
            file.write(struct.pack('L', int(self.o_esp)))
            file.write(struct.pack('L', int(self.o_eff)))
            file.write(struct.pack('L', int(self.o_tim_eff)))
            file.write(struct.pack('L', int(self.o_tim_model)))
            file.write(struct.pack('L', int(self.o_rbj)))
        
        #BIOHAZARD 3: LAST ESCAPE
        if self.version == 3.0:
            file.write(struct.pack('B', int(self.h_sprite)))
            file.write(struct.pack('B', int(self.h_cut)))
            file.write(struct.pack('B', int(self.h_model)))
            file.write(struct.pack('B', int(self.h_item)))
            file.write(struct.pack('B', int(self.h_door)))
            file.write(struct.pack('B', int(self.h_room)))
            file.write(struct.pack('B', int(self.h_reverb)))
            file.write(struct.pack('B', int(self.h_sprite_max)))
            file.write(struct.pack('L', int(self.o_snd)))
            file.write(struct.pack('L', int(self.o_vh_0)))
            file.write(struct.pack('L', int(self.o_vb_0)))
            file.write(struct.pack('L', int(self.o_vh_1)))
            file.write(struct.pack('L', int(self.o_vb_1)))
            file.write(struct.pack('L', int(self.o_ota)))
            file.write(struct.pack('L', int(self.o_sca)))
            file.write(struct.pack('L', int(self.o_rid)))
            file.write(struct.pack('L', int(self.o_rvd)))
            file.write(struct.pack('L', int(self.o_lit)))
            file.write(struct.pack('L', int(self.o_model)))
            file.write(struct.pack('L', int(self.o_flr)))
            file.write(struct.pack('L', int(self.o_blk)))
            file.write(struct.pack('L', int(self.o_msg_0)))
            file.write(struct.pack('L', int(self.o_msg_1)))
            file.write(struct.pack('L', int(self.o_tim_cam)))
            file.write(struct.pack('L', int(self.o_scd)))
            file.write(struct.pack('L', int(self.o_esp)))
            file.write(struct.pack('L', int(self.o_eff)))
            file.write(struct.pack('L', int(self.o_unknown_0)))
            file.write(struct.pack('L', int(self.o_tim_model)))
            file.write(struct.pack('L', int(self.o_unknown_1)))

class rdt_model_table_entry:
    def __init__(self, version):
        self.version = version
        #this is the order used by the original BIO HAZARD, for the other games the order is reversed
        self.o_model = 0   #uint32; absolute offset to model file
        self.o_texture = 0 #uint32; absolute offset to the model's texture file

    def read(self, file):
        self.o_model = 0
        self.o_texture = 0

        if self.version == 1.0:
            self.o_model = int(struct.unpack("L", file.read(4))[0])
            self.o_texture = int(struct.unpack("L", file.read(4))[0])
            return self

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            self.o_texture = int(struct.unpack("L", file.read(4))[0])
            self.o_model = int(struct.unpack("L", file.read(4))[0])
            return self

    def write(self, file):
        if self.version == 1.0:
            file.write(struct.pack('L', int(self.o_model)))
            file.write(struct.pack('L', int(self.o_texture)))

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            file.write(struct.pack('L', int(self.o_texture)))
            file.write(struct.pack('L', int(self.o_model)))

class rdt_model_table:
    def __init__(self, version):
        self.version = version
        self.object = []
    
    def read(self, file, offset, count):
        file.seek(offset)
        print('[LIB_RDT] <READ> MODEL_TABLE ' + str(self.version) + '\t(' + str(file.tell()) + ')')
        self.object = []

        for i in range(count):
            tmp_obj = rdt_model_table_entry(self.version)
            tmp_obj = tmp_obj.read(file)
            self.object.append(tmp_obj)

        return self

    def write(self, file, offset, version):
        file.seek(offset)
        
        for i in range(len(self.object)):
            self.object[i].write(file)

class rdt_file:
    def __init__(self, version):
        self.version = version

		#BIO HAZARD
        if self.version == 1.0:
            self.header = rdt_header(self.version)
            self.lit = lib_lit.lit_file(self.version)
            self.rid = lib_rid.rid_file(self.version)
            self.object_model_table = rdt_model_table(self.version)
            self.item_model_table = rdt_model_table(self.version)
            self.rvd = lib_rvd.rvd_file(self.version)
            self.pri = []
            self.tim_pri = []
            self.sca = lib_sca.sca_file(self.version)
            self.blk = lib_blk.blk_file(self.version)
            self.flr = lib_flr.flr_file(self.version)
            self.scd_main = []
            self.scd_sub_0 = []
            self.scd_sub_1 = []
            self.emr = lib_rbj.emr_file(self.version)
            self.edd = lib_rbj.edd_file()
            self.msg = []
            self.raw = []
            self.object_model = []
            self.item_model = []
            self.esp = lib_esp.esp_data(self.version)
            self.snd = lib_snd.snd_file()
            self.vh = lib_vab.vh_file()
            self.vb = lib_vab.vb_file()
            self.tim_object_model = []
            self.tim_item_model = []
            self.tim_eff = []

		#BIOHAZARD 2 PROTOTYPE
        if self.version == 1.5:
            self.header = rdt_header(self.version)
            self.rid = lib_rid.rid_file(self.version)
            self.model_table = rdt_model_table(self.version)
            self.rvd = lib_rvd.rvd_file(self.version)
            self.lit = lib_lit.lit_file(self.version)
            self.pri = []
            self.sca = lib_sca.sca_file(self.version)
            self.blk = lib_blk.blk_file(self.version)
            self.flr = lib_flr.flr_file(self.version)
            self.scd_main = []
            self.scd_sub_0 = []
            self.scd_sub_1 = []
            self.rbj = lib_rbj.rbj_file(self.version)
            self.model = []
            self.esp = lib_esp.esp_data(self.version)
            self.snd_0 = lib_snd.snd_file()
            self.vh_0 = lib_vab.vh_file()
            self.snd_1 = lib_snd.snd_file()
            self.vh_1 = lib_vab.vh_file()
            self.vb_0 = lib_vab.vb_file()
            self.vb_1 = lib_vab.vb_file()

            self.tim_eff = []
            self.tim_model = []

		#BIOHAZARD 2
        if self.version == 2.0:
            self.header = rdt_header(self.version)
            self.rid = lib_rid.rid_file(self.version)
            self.model_table = rdt_model_table(self.version)
            self.rvd = lib_rvd.rvd_file(self.version)
            self.pri = []
            self.lit = lib_lit.lit_file(self.version)
            self.sca = lib_sca.sca_file(self.version)
            self.blk = lib_blk.blk_file(self.version)
            self.flr = lib_flr.flr_file(self.version)
            self.scd_main = []
            self.scd_sub = []
            self.msg_main = []
            self.msg_sub = []
            self.tim_cam = []
            self.model = []
            self.esp = lib_esp.esp_data(self.version)
            self.rbj = [] #lib_rbj.rbj_file[]
            self.snd = lib_snd.snd_file()
            self.vh_0 = lib_vab.vh_file()
            self.vb_0 = lib_vab.vb_file()
            self.vh_1 = lib_vab.vh_file()
            self.vb_1 = lib_vab.vb_file()
            self.tim_model = []

		#BIOHAZARD 3 LAST ESCAPE
        if self.version == 3.0:
            self.header = rdt_header(self.version)
            self.rid = lib_rid.rid_file(self.version)
            self.model_table = rdt_model_table(self.version)
            self.rvd = lib_rvd.rvd_file(self.version)
            self.lit = lib_lit.lit_file(self.version)
            self.pri = []
            self.sca = lib_sca.sca_file(self.version)
            #self.blk = lib_blk.blk_file(self.version)
            self.flr = lib_flr.flr_file(self.version)
            self.scd = []
            self.msg = []
            #unknown data.. cam related...
            self.tim_cam = []
            self.model = []
            self.esp = lib_esp.esp_data(self.version)
            
            self.snd = lib_snd.snd_file()
            self.vh_0 = lib_vab.vh_file()
            self.vb_0 = lib_vab.vb_file()
            self.vh_1 = lib_vab.vh_file()
            self.vb_1 = lib_vab.vb_file()

            self.tim_model = []

    def read_script_data(self, file, offset):
        tmp_array = []
        file.seek(offset)

        if self.version == 1.0:
            if offset == self.header.o_scd_main:
                print('[LIB_RDT] <READ> SCD_MAIN\t(' + str(file.tell()) + ')')
                size = int(struct.unpack("H", file.read(2))[0])
                tmp_array.append(file.read(size))
                return tmp_array
            
            if offset == self.header.o_scd_sub_0:
                print('[LIB_RDT] <READ> SCD_SUB_0\t(' + str(file.tell()) + ')')
                size = int(struct.unpack("H", file.read(2))[0])
                tmp_array.append(file.read(size))
                return tmp_array

            if offset == self.header.o_scd_sub_1:
                print('[LIB_RDT] <READ> SCD_SUB_1\t(' + str(file.tell()) + ')')
                count = int(struct.unpack("L", file.read(4))[0] / 4)
                file.seek(-4, 1)
                offsets = []

                o_end = self.header.o_emr

                if o_end == 0:
                    o_end = self.header.o_msg
                if o_end == 0:
                    o_end = self.header.o_raw
                
                if o_end > offset:
                    #read relative offset array...
                    for i in range(count):
                        offsets.append(int(struct.unpack("L", file.read(4))[0]))
                
                    #read object array...
                    for i in range(count - 1):
                        file.seek(offset + offsets[i])

                        if i < count - 2:
                            size = offsets[i + 1] - offsets[i]
                        else:
                            size = o_end - (offset + offsets[i])
                
                        tmp_array.append(file.read(size))

            if offset == self.header.o_msg:
                print('[LIB_RDT] <READ> MSG\t(' + str(file.tell()) + ')')
                count = int(struct.unpack("H", file.read(2))[0] / 2)
                file.seek(-2, 1)
                offsets = []

                o_end = self.header.o_raw

                if o_end == 0:
                    o_end = self.header.o_esp

                if o_end > offset:
                    #read relative offset array...
                    for i in range(count):
                        offsets.append(int(struct.unpack("H", file.read(2))[0]))
                
                    #read object array...
                    for i in range(count):
                        file.seek(offset + offsets[i])

                        if i < count - 1:
                            size = offsets[i + 1] - offsets[i]
                        else:
                            size = o_end - (offset + offsets[i])
                
                        tmp_array.append(file.read(size))

        if self.version == 2.0:
            
            o_end = 0

            if offset > 0:
                file.seek(offset)
                count = int(struct.unpack("H", file.read(2))[0] / 2)
                file.seek(-2, 1)
                offsets = []

                #scd_0 "main" area handling...
                if offset == self.header.o_scd_main:
                    print('[LIB_RDT] <READ> SCD_MAIN\t(' + str(offset) + ')')
                    o_end = self.header.o_scd_sub
                
                    if o_end == 0 and self.header.o_msg_main > 0:
                        o_end == self.header.o_msg_main
                    if o_end == 0 and self.header.o_msg_sub > 0:
                        o_end == self.header.o_msg_main
                    if o_end == 0 and self.header.o_tim_cam > 0:
                        o_end == self.header.o_tim_cam
                    if o_end == 0 and self.header.h_model > 0:
                        for i in range(self.header.h_model):
                            if self.model_table.object[i].o_model != 0:
                                o_end = self.model_table.object[i].o_model
                                break
                    if o_end == 0 and self.header.o_esp > 0:
                        o_end == self.header.o_esp
                    if o_end == 0 and self.header.o_snd > 0:
                        o_end == self.header.o_snd

                #scd_1 "sub" area handling...
                if offset == self.header.o_scd_sub:
                    print('[LIB_RDT] <READ> SCD_SUB\t(' + str(offset) + ')')
                    o_end = self.header.o_msg_main

                    if o_end == 0 and self.header.o_msg_main > 0:
                        o_end == self.header.o_msg_sub
                    if o_end == 0 and self.header.o_tim_cam > 0:
                        o_end == self.header.o_tim_cam
                    if o_end == 0 and self.header.h_model > 0:
                        for i in range(self.header.h_model):
                            if self.model_table.object[i].o_model != 0:
                                o_end = self.model_table.object[i].o_model
                                break
                    if o_end == 0 and self.header.o_esp > 0:
                        o_end == self.header.o_esp
                    if o_end == 0 and self.header.o_snd > 0:
                        o_end == self.header.o_snd
            
                #msg_0 "main" area handling...
                if offset == self.header.o_msg_main:
                    print('[LIB_RDT] <READ> MSG_MAIN\t(' + str(offset) + ')')
                    o_end = self.header.o_msg_sub

                    if o_end == 0 and self.header.o_tim_cam > 0:
                        o_end == self.header.o_tim_cam
                    if o_end == 0 and self.header.h_model > 0:
                        for i in range(self.header.h_model):
                            if self.model_table.object[i].o_model != 0:
                                o_end = self.model_table.object[i].o_model
                                break
                    if o_end == 0 and self.header.o_esp > 0:
                        o_end == self.header.o_esp
                    if o_end == 0 and self.header.o_snd > 0:
                        o_end == self.header.o_snd
            
                #msg_1 "sub" area handling...
                if offset == self.header.o_msg_sub:
                    print('[LIB_RDT] <READ> MSG_SUB\t(' + str(offset) + ')')
                    o_end = self.header.o_tim_cam

                    if o_end == 0 and self.header.h_model > 0:
                        for i in range(self.header.h_model):
                            if self.model_table.object[i].o_model != 0:
                                o_end = self.model_table.object[i].o_model
                                break
                    if o_end == 0 and self.header.o_esp > 0:
                        o_end == self.header.o_esp
                    if o_end == 0 and self.header.o_snd > 0:
                        o_end == self.header.o_snd

                if o_end > offset:
                    #read relative offset array...
                    for i in range(count):
                        offsets.append(int(struct.unpack("H", file.read(2))[0]))
                
                    #read object array...
                    for i in range(count):
                        file.seek(offset + offsets[i])

                        if i < count - 1:
                            size = offsets[i + 1] - offsets[i]
                        else:
                            size = o_end - (offset + offsets[i])
                
                        tmp_array.append(file.read(size))

        return tmp_array

    def read(self, filepath):
        print('\n')
        print('=' * 128)
        print('[LIB_RDT] <READ> RDT_FILE ' + str(self.version) + '\t(' + filepath.upper() + ')')
        print('=' * 128)
        
        file = open(filepath, 'rb')

        #read header...
        self.header = self.header.read(file)

        #BIO HAZARD                             #DONE!
        if self.version == 1.0:
            #read light data...
            self.lit = self.lit.read_from_stream(file, 6, 3)

            #read camera data...
            if self.header.h_cut > 0:
                self.rid = self.rid.read_from_stream(file, 148, self.header.h_cut)

            #read item and object model tables...
            if self.header.h_object_model > 0:
                self.object_model_table = self.object_model_table.read(file, self.header.o_object_model, self.header.h_object_model)

            if self.header.h_item_model > 0:
                self.item_model_table = self.item_model_table.read(file, self.header.o_item_model, self.header.h_item_model)

            #read camera switch zone data...
            if self.header.o_rvd > 0:
                self.rvd = self.rvd.read_from_stream(file, self.header.o_rvd)

            #read camera mask sprite and camera mask sprite image data...
            if self.header.h_cut > 0:
                for i in range(len(self.rid.object)):
                    tmp_pri = lib_pri.pri_file(self.version)
                    tmp_pri = tmp_pri.read(file, self.rid.object[i].o_pri)
                    self.pri.append(tmp_pri)

                for i in range(len(self.rid.object)):
                    if self.rid.object[i].o_tim > 0:
                        tmp_tim = lib_tim.tim_file()
                        tmp_tim = tmp_tim.read_from_stream(file, self.rid.object[i].o_tim)
                        self.tim_pri.append(tmp_tim)
                    
                    else:
                        tmp_tim = lib_tim.tim_file()
                        self.tim_pri.append(tmp_tim)
            
            #read collision data...
            if self.header.o_sca > 0:
                self.sca = self.sca.read_from_stream(file, self.header.o_sca)
        
            #read enemy roaming area data...
            #if self.header.o_blk > 0:
            #    self.blk = self.blk.read_from_stream(file, self.header.o_blk)
            
            #read floorstep sound area data...
            #if self.header.o_flr > 0:
            #    self.flr = self.flr.read_from_stream(file, self.header.o_flr)

            #read script data...
            #if self.header.o_scd_main > 0:
            #    self.scd_main = self.read_script_data(file, self.header.o_scd_main)

            #if self.header.o_scd_sub_0 > 0:
            #    self.scd_sub_0 = self.read_script_data(file, self.header.o_scd_sub_0)

            #if self.header.o_scd_sub_1 > 0:
             #   self.scd_sub_1 = self.read_script_data(file, self.header.o_scd_sub_1)

            #read animation data...
            #if self.header.o_edd > 0:
            #    self.edd = self.edd.read_from_stream(file, self.header.o_edd)
            
            #if self.header.o_emr > 0:
            #    self.emr = self.emr.read_from_stream(file, self.header.o_emr, self.edd.frame_count)

            #read message data...
            #if self.header.o_msg > 0:
            #    self.msg = self.read_script_data(file, self.header.o_msg)

            #read item image data...
            if self.header.o_raw > 0 and self.header.h_item_model > 0:
                file.seek(self.header.o_raw)

                for i in range(self.header.h_item_model):
                    self.raw.append(file.read(1200))

            #read effect sprite data...
            #if self.header.o_esp > 0:
            #    self.esp = self.esp.read_from_stream(file, self.header.o_esp, self.header.o_eff)

            #read object models...
            if self.header.h_object_model > 0 and self.header.o_object_model > 0:
                for i in range(len(self.object_model_table.object)):
                    tmp_model = lib_tmd.tmd_file()

                    if self.object_model_table.object[i].o_model > 0:                   
                        tmp_model = tmp_model.read_from_stream(file, self.object_model_table.object[i].o_model)
                    else:
                        tmp_model = lib_tmd.tmd_file()
                                      
                    self.object_model.append(tmp_model)
            
            #read item models...
            if self.header.h_item_model > 0 and self.header.o_item_model > 0:
                for i in range(len(self.item_model_table.object)):
                    tmp_model = lib_tmd.tmd_file()

                    if self.item_model_table.object[i].o_model > 0:                   
                        tmp_model = tmp_model.read_from_stream(file, self.item_model_table.object[i].o_model)
                    else:
                        tmp_model = lib_tmd.tmd_file()
                                      
                    self.item_model.append(tmp_model)

            #read sound data...
            if self.header.o_snd > 0:
                self.snd = self.snd.read(file, self.header.o_snd, 48)

            if self.header.o_vh > 0:
                self.vh = self.vh.read(file, self.header.o_vh)

            if self.header.o_vb > 0:
                self.vb = self.vb.read(file, self.header.o_vb, self.vh.vag_offset_table)
            
            #read object model .tim textures...
            #if self.header.h_object_model > 0:
            #    for i in range(len(self.object_model_table.object)):
            #        tmp_tim = lib_tim.tim_file()

            #        if self.object_model_table.object[i].o_texture > 0:                   
            #            tmp_tim = tmp_tim.read_from_stream(file, self.object_model_table.object[i].o_texture)
            #        else:
            #           tmp_tim = lib_tim.tim_file()

            #        self.tim_object_model.append(tmp_tim)

            #read item model .tim textures...
            #if self.header.h_item_model > 0:
            #    for i in range(len(self.item_model_table.object)):
            #       tmp_tim = lib_tim.tim_file()
#
            #        if self.item_model_table.object[i].o_texture > 0:                   
            #            tmp_tim = tmp_tim.read_from_stream(file, self.item_model_table.object[i].o_texture)
            #       else:
            #            tmp_tim = lib_tim.tim_file()
#
            #        self.tim_item_model.append(tmp_tim)
            
            ##read effect sprite .tim files...
            #if len(self.esp.object) > 0:
            #    if self.header.o_tim_eff > 0:
            #        file.seek(self.header.o_tim_eff)

            #        o_tmp = []

            #        for i in range(len(self.esp.object)):
            #            o_tmp.append(struct.unpack("L", file.read(4))[0])
            #            file.seek(-8, 1)

            #        for i in range(len(o_tmp)):
            #            tmp_tim = lib_tim.tim_file()
            #            tmp_tim = tmp_tim.read_from_stream(file, o_tmp[i])
            #            self.tim_eff.append(tmp_tim)
            
            #close file and return data...
            file.close()
            return self

        #BIOHAZARD 1.5                          #MISSING SCRIPTS/MESSAGES/RBJ...!!!!
        if self.version == 1.5:
            #read camera data...
            if self.header.h_cut > 0 and self.header.o_rid > 0:
                self.rid = self.rid.read_from_stream(file, self.header.o_rid, self.header.h_cut)
            
            #read model table...
            if self.header.h_model > 0:
                self.model_table = self.model_table.read(file, self.header.o_model, self.header.h_model)

            #read camera switch zone data...
            if self.header.o_rvd > 0:
                self.rvd = self.rvd.read_from_stream(file, self.header.o_rvd)

            #read light data...
            if len(self.rid.object) > 0 and self.header.o_lit > 0:
                self.lit = self.lit.read_from_stream(file, self.header.o_lit, self.header.h_cut)

            #read camera sprite data...
            if len(self.rid.object) > 0:
                for i in range(len(self.rid.object)):
                    tmp_pri = lib_pri.pri_file(self.version)
                    tmp_pri = tmp_pri.read(file, self.rid.object[i].o_pri)
                    self.pri.append(tmp_pri)
            
            #read collision data...
            if self.header.o_sca > 0:
                self.sca = self.sca.read_from_stream(file, self.header.o_sca)

            #read enemy roaming area data...
            if self.header.o_blk > 0:
                self.blk = self.blk.read_from_stream(file, self.header.o_blk)

            #read floorstep sound area data...
            if self.header.o_flr > 0:
                self.flr = self.flr.read_from_stream(file, self.header.o_flr)

            #scd_main
            #scd_sub_0
            #scd_sub_1

            #if self.header.o_rbj > 0:

            #read model data...
            if self.header.h_model > 0 and self.header.o_model > 0:
                for i in range(len(self.model_table.object)):
                    tmp_model = lib_md1.md1_file()

                    if self.model_table.object[i].o_model > 0:                   
                        tmp_model = tmp_model.read_from_stream(file, self.model_table.object[i].o_model)
                    else:
                        tmp_model = lib_md1.md1_file()
                                      
                    self.model.append(tmp_model)

            #read effect sprite data...
            if self.header.o_esp > 0:
                self.esp = self.esp.read_from_stream(file, self.header.o_esp, self.header.o_eff)

            #read sound data...
            if self.header.o_snd_0 > 0:
                self.snd_0 = self.snd_0.read(file, self.header.o_snd_0, 32)

            if self.header.o_vh_0 > 0:
                self.vh_0 = self.vh_0.read(file, self.header.o_vh_0)

            if self.header.o_snd_1 > 0:
                self.snd_1 = self.snd_1.read(file, self.header.o_snd_1, 24)

            if self.header.o_vh_1 > 0:
                self.vh_1 = self.vh_1.read(file, self.header.o_vh_1)

            if self.header.o_vb_0 > 0:
                self.vb_0 = self.vb_0.read(file, self.header.o_vh_0, self.vh_0.vag_offset_table)

            if self.header.o_vb_1 > 0:
                self.vb_1 = self.vb_1.read(file, self.header.o_vh_1, self.vh_1.vag_offset_table)

            #read effect sprite image data...
            if len(self.esp.object) > 0:
                if self.header.o_tim_eff > 0:
                    file.seek(self.header.o_tim_eff)

                    o_tmp = file.tell()

                    for i in range(len(self.esp.object)):
                        tmp_tim = lib_tim.tim_file()
                        tmp_tim = tmp_tim.read_from_stream(file, file.tell())

                        self.tim_eff.append(tmp_tim)
            
            #read model texture data...
            if self.header.h_model > 0 and self.header.o_model > 0:
                for i in range(len(self.model_table.object)):
                    tmp_tim = lib_tim.tim_file()

                    if self.model_table.object[i].o_texture > 0:                   
                        tmp_tim = tmp_tim.read_from_stream(file, self.model_table.object[i].o_texture)
                    else:
                        tmp_tim = lib_tim.tim_file()

                    self.tim_model.append(tmp_tim)

            #close file and return data...
            file.close()
            return self

        #BIOHAZARD 2
        if self.version == 2.0:
            #read camera data...
            if self.header.h_cut > 0 and self.header.o_rid > 0:
                self.rid = self.rid.read_from_stream(file, self.header.o_rid, self.header.h_cut)
        
            #read model table...
            if self.header.h_model > 0:
                self.model_table = self.model_table.read(file, self.header.o_model, self.header.h_model)

            #read camera switch zone data...
            if self.header.o_rvd > 0:
                self.rvd = self.rvd.read_from_stream(file, self.header.o_rvd)

            #read light data...
            if len(self.rid.object) > 0 and self.header.o_lit > 0:
                self.lit = self.lit.read_from_stream(file, self.header.o_lit, self.header.h_cut)

            #read camera sprite data...
            if len(self.rid.object) > 0:
                for i in range(len(self.rid.object)):
                    tmp_pri = lib_pri.pri_file(self.version)
                    tmp_pri = tmp_pri.read(file, self.rid.object[i].o_pri)
                    self.pri.append(tmp_pri)
        
            #read collision data...
            if self.header.o_sca > 0:
                self.sca = self.sca.read_from_stream(file, self.header.o_sca)

            #read enemy roaming area data...
            if self.header.o_blk > 0:
                self.blk = self.blk.read_from_stream(file, self.header.o_blk)
        
            #read floorstep sound area data...
            if self.header.o_flr > 0:
                self.flr = self.flr.read_from_stream(file, self.header.o_flr)

            #read script data...
            if self.header.o_scd_main > 0:
                self.scd_main = self.read_script_data(file, self.header.o_scd_main)

            if self.header.o_scd_sub > 0:
                self.scd_sub = self.read_script_data(file, self.header.o_scd_sub)

            #read message data...
            if self.header.o_msg_main > 0:
                self.msg_main = self.read_script_data(file, self.header.o_msg_main)

            if self.header.o_msg_sub > 0:
                self.msg_sub = self.read_script_data(file, self.header.o_msg_sub)

            #read camera scroll image data...
            if self.header.o_tim_cam > 0:
                print('[LIB_RDT] <READ> TIM_CAM\t(' + str(self.header.o_tim_cam) + ')')
                file.seek(self.header.o_tim_cam)
                self.tim_cam = file.read(153600)

            #read model data...
            if self.header.h_model > 0 and self.header.o_model > 0:
                for i in range(len(self.model_table.object)):
                    tmp_model = lib_md1.md1_file()

                    if self.model_table.object[i].o_model > 0:                   
                        tmp_model = tmp_model.read_from_stream(file, self.model_table.object[i].o_model)
                    else:
                        tmp_model = lib_md1.md1_file()
                                      
                    self.model.append(tmp_model)
        
            #read effect sprite data...
            if self.header.o_esp > 0:
                self.esp = self.esp.read_from_stream(file, self.header.o_esp, self.header.o_eff)
            
            #read sound data...
            if self.header.o_snd > 0:
                self.snd = self.snd.read(file, self.header.o_snd, 48)
            
            if self.header.o_vh_0 > 0:
                self.vh_0 = self.vh_0.read(file, self.header.o_vh_0)

            if self.header.o_vb_0 > 0:
                self.vb_0 = self.vb_0.read(file, self.header.o_vb_0, self.vh_0.vag_offset_table)

            #read model texture data...
            if self.header.h_model > 0 and self.header.o_model > 0:
                for i in range(len(self.model_table.object)):
                    tmp_tim = lib_tim.tim_file()

                    if self.model_table.object[i].o_texture > 0:                   
                        tmp_tim = tmp_tim.read_from_stream(file, self.model_table.object[i].o_texture)
                    else:
                        tmp_tim = lib_tim.tim_file()

                    self.tim_model.append(tmp_tim)

            #close file and return data...
            file.close()
            return self
        
        #BIOHAZARD 3: LAST ESCAPE
        if self.version == 3.0:
            #read camera data...
            if self.header.h_cut > 0 and self.header.o_rid > 0:
                self.rid = self.rid.read_from_stream(file, self.header.o_rid, self.header.h_cut)
        
            #read model table...
            if self.header.h_model > 0:
                self.model_table = self.model_table.read(file, self.header.o_model, self.header.h_model)

            #read camera switch zone data...
            if self.header.o_rvd > 0:
                self.rvd = self.rvd.read_from_stream(file, self.header.o_rvd)

            #read light data...
            #if len(self.rid.object) > 0 and self.header.o_lit > 0:
            #    self.lit = self.lit.read_from_stream(file, self.header.o_lit, self.header.h_cut)

            #read camera sprite data...
            if len(self.rid.object) > 0:
                for i in range(len(self.rid.object)):
                    tmp_pri = lib_pri.pri_file(self.version)
                    tmp_pri = tmp_pri.read(file, self.rid.object[i].o_pri)
                    self.pri.append(tmp_pri)
        
            #read collision data...
            if self.header.o_sca > 0:
                self.sca = self.sca.read_from_stream(file, self.header.o_sca)

            #read enemy roaming area data...
            #if self.header.o_blk > 0:
            #    self.blk = self.blk.read_from_stream(file, self.header.o_blk)
        
            #read floorstep sound area data...
            if self.header.o_flr > 0:
                self.flr = self.flr.read_from_stream(file, self.header.o_flr)

            #read script data...
            #if self.header.o_scd_main > 0:
            #    self.scd_main = self.read_script_data(file, self.header.o_scd_main)

            #if self.header.o_scd_sub > 0:
            #    self.scd_sub = self.read_script_data(file, self.header.o_scd_sub)

            #read message data...
            #if self.header.o_msg > 0:
            #    self.msg_main = self.read_script_data(file, self.header.o_msg_main)

            #read camera scroll image data...
            if self.header.o_tim_cam > 0:
                print('[LIB_RDT] <READ> TIM_CAM\t(' + str(self.header.o_tim_cam) + ')')
                file.seek(self.header.o_tim_cam)
                self.tim_cam = file.read(153600)

            #read model data...
            if self.header.h_model > 0 and self.header.o_model > 0:
                for i in range(len(self.model_table.object)):
                    tmp_model = lib_md2.md2_file()

                    print(str(i) + ' ::: ' + str(self.model_table.object[i].o_model))

                    if self.model_table.object[i].o_model > 0:                   
                        tmp_model = tmp_model.read_from_stream(file, self.model_table.object[i].o_model + 24)
                    else:
                        tmp_model = lib_md2.md2_file()
                                      
                    self.model.append(tmp_model)
        
            #read effect sprite data...
            if self.header.o_esp > 0:
                self.esp = self.esp.read_from_stream(file, self.header.o_esp, self.header.o_eff)
            
            #read sound data...
            if self.header.o_snd > 0:
                self.snd = self.snd.read(file, self.header.o_snd, 48)
            
            #if self.header.o_vh_0 > 0:
            #    self.vh_0 = self.vh_0.read(file, self.header.o_vh_0)

            #if self.header.o_vb_0 > 0:
            #    self.vb_0 = self.vb_0.read(file, self.header.o_vb_0, self.vh_0.vag_offset_table)

            #read model texture data...
            if self.header.h_model > 0 and self.header.o_model > 0:
                for i in range(len(self.model_table.object)):
                    tmp_tim = lib_tim.tim_file()

                    if self.model_table.object[i].o_texture > 0:                   
                        tmp_tim = tmp_tim.read_from_stream(file, self.model_table.object[i].o_texture)
                    else:
                        tmp_tim = lib_tim.tim_file()

                    self.tim_model.append(tmp_tim)

            #close file and return data...
            file.close()
            return self

    def extract(self, filepath):
        print('\n')
        print('=' * 128)
        print('[LIB_RDT] <EXTRACT> RDT FILE\t' + str(self.version) + '\t(' + filepath + ')')
        print('=' * 128)
        lib_tools.create_dir(filepath)
        lib_tools.create_dir(filepath + '/CAMERA')
        lib_tools.create_dir(filepath + '/MODEL')
        lib_tools.create_dir(filepath + '/EFFECT')
        lib_tools.create_dir(filepath + '/SOUND')
        lib_tools.create_dir(filepath + '/ANIMATION')
        lib_tools.create_dir(filepath + '/MESSAGE')
        lib_tools.create_dir(filepath + '/SCRIPT')

        #BIO HAZARD
        if self.version == 1.0:
            lib_tools.create_dir(filepath + '/ITEM')
        
            if len(self.lit.object) == 3:
                self.lit.write_to_file(filepath + '/CAMERA/LIGHTS.LIT')

            if len(self.rid.object) > 0:
                self.rid.write_to_file(filepath + '/CAMERA/CAMERAS.RID')

            if len(self.rvd.object) > 0:
                self.rvd.write_to_file(filepath + '/CAMERA/ZONES.RVD')

            if len(self.scd_main) > 0:
                print('[LIB_RDT] <EXTRACT> SCD_MAIN\t(' + filepath.upper() + '/SCRIPT/MAIN_00.SCD' + ')')
                file = open(filepath + '/SCRIPT/MAIN_00.SCD', 'wb')
                file.write(self.scd_main[0])
                file.close()

            if len(self.scd_sub_0) > 0:
                print('[LIB_RDT] <EXTRACT> SCD_SUB_0\t(' + filepath.upper() + '/SCRIPT/SUB0_00.SCD' + ')')
                file = open(filepath + '/SCRIPT/SUB0_00.SCD', 'wb')
                file.write(self.scd_sub_0[0])
                file.close()
            
            if len(self.scd_sub_1) > 0:
                for i in range(len(self.scd_sub_1)):
                    print('[LIB_RDT] <EXTRACT> SCD_SUB_1\t(' + filepath.upper() + '/SCRIPT/SUB1_' + lib_tools.fix_id(i) + '.SCD' + ')')
                    file = open(filepath + '/SCRIPT/SUB1_' + lib_tools.fix_id(i) + '.SCD', 'wb')
                    file.write(self.scd_sub_1[i])
                    file.close()

            for i in range(len(self.pri)):
                if self.pri[i].header.offsets > 0 and len(self.pri[i].masks) > 0:
                    self.pri[i].extract(filepath + '/CAMERA/MASK_' + lib_tools.fix_id(i) + '.PRI')

            for i in range(len(self.tim_pri)):
                if self.tim_pri[i].header.bpp != 0:
                    self.tim_pri[i].extract(filepath.upper() + '/CAMERA/MASK_' + lib_tools.fix_id(i) + '.TIM')

            if self.header.o_sca > 0:
                self.sca.write_to_file(filepath + '/CAMERA/COLLISIONS.SCA')

            if self.header.o_blk > 0:
                self.blk.write_to_file(filepath+ '/CAMERA/ROAMING.BLK')
        
            if self.header.o_flr > 0:
                self.flr.write_to_file(filepath+ '/CAMERA/FLOORS.FLR')
        
            if len(self.msg) > 0:
                for i in range(len(self.msg)):
                    print('[LIB_RDT] <EXTRACT> MSG\t(' + filepath.upper() + '/MESSAGE/MESSAGE_' + lib_tools.fix_id(i) + '.MSG' + ')')
                    file = open(filepath + '/MESSAGE/MESSAGE_' + lib_tools.fix_id(i) + '.MSG', 'wb')
                    file.write(self.msg[i])
                    file.close()

            if len(self.raw) > 0:
                clut = [0x739c8000, 0x63186f7b, 0x5ad65ef7, 0x4e7356b5, 0x42104a52, 0x39ce3def, 0x318c35ad, 0x1ce72529, 
                        0x14a518c6, 0xc631084, 0x46324e74, 0x294c39cf, 0x35b739d1, 0x29552d74, 0x18cf0c67, 0x1091108e, 
                        0xe0011, 0x8000a, 0x44e0002, 0x10d52d96, 0x4238044b, 0x31d82970, 0x19372db7, 0x4900493, 
                        0x46791116, 0xb508d3, 0x4f708ad, 0x29b21d2e, 0x110e4afe, 0x1d7008ee, 0x29d325f7, 0x9311db4, 
                        0x133296c, 0x56d7675b, 0x4a9635cf, 0x29b03a56, 0x150b3258, 0x4e950886, 0x2dd021f5, 0x150a4afa, 
                        0x4642657, 0x214b31cf, 0x156e1db0, 0x2dae4eb6, 0x1dd12a34, 0x116e0885, 0x2e763a75, 0x36d92613, 
                        0x11b0114c, 0x36fa3a32, 0x1daf3f7f, 0x22550cc7, 0x158e3b3c, 0xa343f9f, 0x25f03eb6, 0x5092e74, 
                        0x63301d0, 0x9ae0675, 0x254a058d, 0x19083610, 0x1e1021ef, 0x1e522273, 0x11ee0e52, 0x22500549, 
                        0x19490969, 0x9aa08c5, 0xa071d69, 0x21ea0e88, 0x21c90d85, 0x160616a7, 0x296a6338, 0x10a435ed, 
                        0x44110e4, 0x12631144, 0xd0105e0, 0x27001600, 0x114015a0, 0x22012680, 0x37201d25, 0x31e82183, 
                        0x21803680, 0x3a4239eb, 0x2da13200, 0x42222120, 0x63176b59, 0x39c22949, 0x5a205200, 0x55c04180, 
                        0x61e03101, 0x3d005180, 0x450155ea, 0x55ca5120, 0x49895e71, 0x356a5deb, 0x45273081, 0x5d0438e5, 
                        0x24835a51, 0x4dcd5926, 0x3c826568, 0x76504ca2, 0x71ed3d07, 0x38c530a4, 0x34623062, 0x527358a4, 
                        0x3dce4a31, 0x358c39ad, 0x398c66f7, 0x29086ad6, 0x418c5210, 0x49ad3129, 0x38e7414a, 0x386330c6, 
                        0x6ce82c42, 0x2c015422, 0x24222801, 0x24432401, 0x28c72485, 0xc011c02, 0x350c356c, 0x7bbe2889, 
                        0x1c077fff, 0x310f282c, 0x285028cd, 0x28ce2832, 0xc061c0e, 0x80c0c0d, 0x40a148c, 0x118b3]
            
                for i in range(len(self.raw)):
                    print('[LIB_RDT] <EXTRACT> ITEM_IMAGE\t(' + filepath.upper() + '/ITEM/ITEM_' + lib_tools.fix_id(i) + '.TIM' + ')')
                
                    file = open(filepath.upper() + '/ITEM/ITEM_' + lib_tools.fix_id(i) + '.TIM', 'wb')
                
                    file.write(struct.pack('L', int(16)))
                    file.write(struct.pack('L', int(9)))
                    file.write(struct.pack('L', int(524)))
                    file.write(struct.pack('H', int(0)))
                    file.write(struct.pack('H', int(496)))
                    file.write(struct.pack('H', int(256)))
                    file.write(struct.pack('H', int(1)))

                    for j in range(len(clut)):
                        file.write(struct.pack('L', int(clut[j])))
                
                    file.write(struct.pack('L', int(1212)))
                    file.write(struct.pack('L', int(960)))
                    file.write(struct.pack('H', int(20)))
                    file.write(struct.pack('H', int(30)))
                    file.write(self.raw[i])

                    file.close()

            if len(self.object_model) > 0:
                for i in range(len(self.object_model)):
                    self.object_model[i].write_to_file(filepath.upper() + '/MODEL/OBJECT_' + lib_tools.fix_id(i) + '.TMD')
                    self.tim_object_model[i].extract(filepath.upper() + '/MODEL/OBJECT_' + lib_tools.fix_id(i) + '.TIM')
            
            if len(self.item_model) > 0:
                for i in range(len(self.item_model)):
                    self.item_model[i].write_to_file(filepath.upper() + '/MODEL/ITEM_' + lib_tools.fix_id(i) + '.TMD')
                    self.tim_item_model[i].extract(filepath.upper() + '/MODEL/ITEM_' + lib_tools.fix_id(i) + '.TIM')
        
            if self.header.o_esp > 0:
                if len(self.esp.object) > 0:
                    self.esp.write_to_folder(filepath + '/EFFECT/')
        
            if len(self.esp.object) > 0:
                if len(self.tim_eff) > 0:
                    for i in range(len(self.tim_eff)):
                        self.tim_eff[i].extract(filepath + '/EFFECT/ESP_' + hex(self.esp.header.object[i])[2:].zfill(2).upper() + '.TIM')

            if len(self.snd.object) == 48:
                self.snd.extract(filepath.upper() + '/SOUND/ROOM.SND')

            if self.header.o_vh > 0 and self.header.o_vb > 0:
                self.vh.extract(filepath.upper() + '/SOUND/ROOM.VH')
                self.vb.extract(filepath.upper() + '/SOUND/ROOM.VB')

            if len(self.edd.header.object) > 0:
                if self.edd.header.object[0].count > 0:
                    self.edd.write_to_file(filepath.upper() + '/ANIMATION/PLAYER.EDD')
                    self.emr.write_to_file(filepath.upper() + '/ANIMATION/PLAYER.EMR')

        if self.version == 1.5:
            if len(self.rid.object) > 0:
                self.rid.write_to_file(filepath + '/CAMERA/CAMERAS.RID')

            if len(self.rvd.object) > 0:
                self.rvd.write_to_file(filepath + '/CAMERA/ZONES.RVD')
            
            if len(self.lit.object) > 0:
                self.lit.write_to_file(filepath + '/CAMERA/LIGHTS.LIT')

            for i in range(len(self.pri)):
                if self.pri[i].header.offsets > 0 and len(self.pri[i].masks) > 0:
                    self.pri[i].extract(filepath + '/CAMERA/MASK_' + lib_tools.fix_id(i) + '.PRI')

            if len(self.sca.object) > 0:
                self.sca.write_to_file(filepath + '/CAMERA/COLLISIONS.SCA')

            if len(self.snd_0.object) == 32:
                self.snd_0.extract(filepath.upper() + '/SOUND/ROOM.SND')
            
            if len(self.snd_1.object) == 24:
                self.snd_1.extract(filepath.upper() + '/SOUND/ENEMY.SND')

            if self.header.o_vh_0 > 0 and self.header.o_vb_0 > 0:
                self.vh_0.extract(filepath.upper() + '/SOUND/ROOM.VH')
                self.vb_0.extract(filepath.upper() + '/SOUND/ROOM.VB')

            if self.header.o_vh_1 > 0 and self.header.o_vb_1 > 0:
                self.vh_1.extract(filepath.upper() + '/SOUND/ENEMY.VH')
                self.vb_1.extract(filepath.upper() + '/SOUND/ENEMY.VB')

        if self.version == 2.0:
            if len(self.rid.object) > 0:
                self.rid.write_to_file(filepath + '/CAMERA/CAMERAS.RID')

            if len(self.rvd.object) > 0:
                self.rvd.write_to_file(filepath + '/CAMERA/ZONES.RVD')

            if len(self.sca.object) > 0:
                self.sca.write_to_file(filepath + '/CAMERA/COLLISIONS.SCA')

            if self.header.o_blk > 0 and len(self.blk.object) > 0:
                self.blk.write_to_file(filepath + '/CAMERA/ROAMING.BLK')

            if self.header.o_flr > 0 and len(self.flr.object) > 0:
                self.flr.write_to_file(filepath + '/CAMERA/FLOORS.FLR')

            for i in range(len(self.pri)):
                if self.pri[i].header.offsets > 0 and len(self.pri[i].masks) > 0:
                    self.pri[i].extract(filepath + '/CAMERA/MASK_' + lib_tools.fix_id(i) + '.PRI')

            for i in range(len(self.scd_main)):
                print('[LIB_RDT] <EXTRACT> SCD_MAIN\t(' + filepath.upper() + '/SCRIPT/MAIN_' + lib_tools.fix_id(i) + '.SCD' + ')')
                file = open(filepath + '/SCRIPT/MAIN_' + lib_tools.fix_id(i) + '.SCD', 'wb')
                file.write(self.scd_main[i])
                file.close()

            for i in range(len(self.scd_sub)):
                print('[LIB_RDT] <EXTRACT> SCD_SUB\t(' + filepath.upper() + '/SCRIPT/SUB_' + lib_tools.fix_id(i) + '.SCD' + ')')
                file = open(filepath + '/SCRIPT/SUB_' + lib_tools.fix_id(i) + '.SCD', 'wb')
                file.write(self.scd_sub[i])
                file.close()
        
            #extract messages...
            for i in range(len(self.msg_main)):
                print('[LIB_RDT] <EXTRACT> MSG_MAIN\t(' + filepath.upper() + '/MESSAGE/MAIN_' + lib_tools.fix_id(i) + '.MSG' + ')')
                file = open(filepath + '/MESSAGE/MAIN_' + lib_tools.fix_id(i) + '.MSG', 'wb')
                file.write(self.msg_main[i])
                file.close()

            for i in range(len(self.msg_sub)):
                print('[LIB_RDT] <EXTRACT> MSG_SUB\t(' + filepath.upper() + '/MESSAGE/SUB_' + lib_tools.fix_id(i) + '.MSG' + ')')
                file = open(filepath + '/MESSAGE/SUB_' + lib_tools.fix_id(i) + '.MSG', 'wb')
                file.write(self.msg_sub[i])
                file.close()

        #extract embedded .tim file used for camera scrolling cutscenes, if available
        if self.version == 2.0:
            if self.header.o_tim_cam > 0 and len(self.tim_cam) > 0:
                print('[LIB_RDT] <EXTRACT> TIM_CAM\t(' + filepath.upper() + '/CAMERA/CAM_SCROLL.TIM' + ')')
                file = open(filepath + '/CAMERA/CAM_SCROLL.TIM', 'wb')

                file.write(struct.pack('L', int(16)))
                file.write(struct.pack('L', int(2)))
                file.write(struct.pack('L', int(153612)))
                file.write(struct.pack('L', int(0)))
                file.write(struct.pack('H', int(320)))
                file.write(struct.pack('H', int(240)))
                file.write(self.tim_cam)

                file.close()

        if self.version == 1.5 or self.version == 2.0 or self.version == 3.0:
            if len(self.model) > 0:
                for i in range(len(self.model)):
                    if self.model[i].header.count > 0:
                        self.model[i].write_to_file(filepath.upper() + '/MODEL/OBJECT_' + lib_tools.fix_id(i) + '.MD1')
        
                for i in range(len(self.tim_model)):
                    self.tim_model[i].extract(filepath.upper() + '/MODEL/OBJECT_' + lib_tools.fix_id(i) + '.TIM')
        
        #extract effect data...


        #extract sound data...

        


        if self.version == 2.0:
            if len(self.snd.object) > 0:
                self.snd.extract(filepath.upper() + '/SOUND/ROOM.SND')

            if self.header.o_vh_0 > 0 and self.header.o_vb_0 > 0:
                self.vh_0.extract(filepath.upper() + '/SOUND/ROOM.VH')
                self.vb_0.extract(filepath.upper() + '/SOUND/ROOM.VB')
        