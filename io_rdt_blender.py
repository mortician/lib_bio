########################################################################################################################
# IO_RDT - BIOHAZARD .RDT IMPORT/EXPORT ADDON FOR BLENDER 2.5x+
########################################################################################################################
# SUPPORTED:
#			   BIO HAZARD
#			   BIOHAZARD 2 PROTOTYPE (NOV/1996)
#			   BIOHAZARD 2
#			   BIOHAZARD 3: LAST ESCAPE
########################################################################################################################
# 2015, MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)
########################################################################################################################
bl_info = {
    "name": "BIOHAZARD RDT(.RDT)",
    "author": "mortician",
    "version": (0, 4, 0),
    "blender": (2, 79, 0),
    "location": "File > Import-Export",
    "description": "Handles data of BIOHAZARD 123 RDT files",
    "warning": "BETA // Highly experimental...",
    "category": "Import-Export"}
		   
import bpy
import imp
import os
import struct
import lib_bio.lib_rdt as lib_rdt
import lib_bio.lib_rid as lib_rid
import lib_bio.lib_sca as lib_sca
import lib_bio.lib_tools as lib_tools
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

#Reload libs to force update them
imp.reload(lib_rdt)
imp.reload(lib_tools)



#=======================================================================================================================
# GLOBAL VARIABLES...
#=======================================================================================================================
v_scale = float(1000)

#=======================================================================================================================
# HELPER FUNCTIONS...
#=======================================================================================================================
def calc_y_data(value):
	bits = lib_tools.long_to_bits(value)
	bit_count = 0
	base_flag = 0

	y_base = 0
	y_height = 0

	for i in range(32):
		if bits[i] == '1' and base_flag == 0:
			y_base = i * 1.8
			base_flag = 1

		if bits[i] == '1' and base_flag >= 0:
			bit_count += 1
			y_height = bit_count * 1.8

	return [y_base, y_height]

def get_obj_count(tag, max_count):
	obj_count = 0
	
	for i in range(max_count):
		if bpy.data.objects.get(tag + lib_tools.fix_id(i)) is not None:
			obj_count += 1	

	return obj_count
#=======================================================================================================================
# CREATING FUNCTIONS...
#=======================================================================================================================
def create_material(name, diffuse, specular, alpha):
	
	if bpy.data.materials.get(name) is None:
		mat = bpy.data.materials.new(name)
		mat.diffuse_color = diffuse
		mat.diffuse_shader = 'LAMBERT'
		mat.diffuse_intensity = 1.0
		mat.specular_color = specular
		mat.specular_intensity = 0.5
		mat.ambient = 1
		mat.alpha = alpha

		if mat.alpha < 1.0:
			mat.use_transparency = True

	return mat

def create_camera(index, x, y, z, target_x, target_y, target_z, fov):
	cam = bpy.data.cameras.new('RID_' + lib_tools.fix_id(index))
	cam_ob = bpy.data.objects.new('RID_' + lib_tools.fix_id(index), cam)
	bpy.context.scene.objects.link(cam_ob)

	cam_ob.location = (x, z, y)
	cam_ob.data.lens = fov

	empty = bpy.data.objects.new('RID_' + lib_tools.fix_id(index) + '_AIM', None)
	bpy.context.scene.objects.link(empty)
	empty.location = (target_x, target_z, target_y)
	empty.select = True
	bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, 
										 False, False, False, False, False, 
										 False, False, False, False, False, 
										 False, False, False, False, False))
	empty.select = False

	cam_ob.select = True
	aim = cam_ob.constraints.new('TRACK_TO')
	aim.target = empty
	aim.track_axis = 'TRACK_NEGATIVE_Z'
	aim.up_axis = 'UP_Y'
	bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, 
										 False, False, False, False, False, 
										 False, False, False, False, False, 
										 False, False, False, False, False))
	cam_ob.select = False
	
	

	bpy.context.scene.update()

def create_cube(tag, index, x, y, z, width, height, density):
	verts = [
		(x + width, z + density, y),
		(x + width, z, y),
		(x, z, y),
		(x, z + density, y),
		(x + width, z + density, y + height),
		(x + width, z, y + height),
		(x, z, y + height),
		(x, z + density, y + height)]

	faces = [
		(0, 1, 2, 3),
		(4, 7, 6, 5),
		(0, 4, 5, 1),
		(1, 5, 6, 2),
		(2, 6, 7, 3),
		(4, 0, 3, 7)]

	mesh = bpy.data.meshes.new(tag + lib_tools.fix_id(index) + '_MESH')
	cube = bpy.data.objects.new(tag + lib_tools.fix_id(index), mesh)
	bpy.context.scene.objects.link(cube)
	mesh.from_pydata(verts, [], faces)
	mesh.update()

	cube.select = True
	bpy.ops.object.move_to_layer(layers=(True, False, False, False, False, 
										 False, False, False, False, False, 
										 False, False, False, False, False, 
										 False, False, False, False, False))
	bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
	cube.select = False
	bpy.context.scene.update()

def create_cylinder(tag, index, x, y, z, width, height, density):
	x += width / 2
	z += density / 2

	if y == 0:
		bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1, depth= height - y, end_fill_type='NGON',
											location=(x, z, y + height/2),
											layers=(True, False, False, False, False,
													False, False, False, False, False,
													False, False, False, False, False,
													False, False, False, False, False))

	if y != 0:
		bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1, depth= height - y, end_fill_type='NGON',
											location=(x, z, y/2 + height/2),
											layers=(True, False, False, False, False,
													False, False, False, False, False,
													False, False, False, False, False,
													False, False, False, False, False))
	cylinder = bpy.data.objects["Cylinder"]
	mesh = cylinder.data
	mesh.name = tag + lib_tools.fix_id(index) + '_MESH'
	cylinder.name = tag + lib_tools.fix_id(index)
	cylinder.dimensions = (width, density, height - y)

def create_plane(tag, index, x, y, z, width, density):			#add layer selection
	plane = bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False,
											 location=(x + (width / 2), z + (density / 2), y),
											 layers=(False, False, False, True, False,
													 False, False, False, False, False,
													 False, False, False, False, False,
													 False, False, False, False, False))
	bpy.context.object.name = tag + lib_tools.fix_id(index)
	mesh = bpy.context.object.data
	mesh.name = tag + lib_tools.fix_id(index) + '_MESH'
	bpy.data.objects[tag + lib_tools.fix_id(index)].dimensions = (width, density, 0)
	bpy.data.objects[tag + lib_tools.fix_id(index)].select = False

def create_prism(tag, index, x, y, z, width, height, density, direction):
	#triangle based prism "\|": 1 or 129
	if direction == 'NE':
		verts = [
			(x + width, z + density, y),
			(x, z + density, y),
			(x + width, z,  y),
			(x + width, z + density, y + height),
			(x, z + density, y + height),
			(x + width, z, y + height)]

		faces = [
			(0, 1, 2),
			(3, 4, 5),
			(0, 1, 4, 3),
			(1, 2, 5, 4),
			(0, 3, 5, 2)]

	#triangle based prism "|/": 2 or 130
	if direction == 'NW':
		verts = [
			(x, z + density, y),
			(x, z, y),
			(x + width, z + density, y),
			(x, z + density, y + height),
			(x, z, y + height),
			(x + width, z + density, y + height)]

		faces = [
			(0, 1, 2),
			(3, 4, 5),
			(0, 1, 4, 3),
			(1, 2, 5, 4),
			(0, 3, 5, 2)]

	#triangle based prism "/|": 3 or 131
	if direction == 'SE':
		verts = [
			(x + width, z + density, y),
			(x, z,  y),
			(x + width, z, y),
			(x + width, z + density, y + height),
			(x, z, y + height),
			(x + width, z, y + height)]

		faces = [
			(0,1,2),
			(3,4,5),
			(0,1,4,3),
			(1,2,5,4),
			(0,3,5,2)]

	#triangle based prism "|\": 4 or 132
	if direction == 'SW':
		verts = [
			(x, z + density, y),
			(x, z, y),
			(x + width, z, y),
			(x, z + density, y + height),
			(x, z, y + height),
			(x + width, z, y + height)]

		faces = [
			(0, 1, 2),
			(3, 4, 5),
			(0, 1, 4, 3),
			(1, 2, 5, 4),
			(0, 3, 5, 2)]

	#Slope going down from south to north
	if direction == 'SN':
		verts = [
			(x + width, z + density, y),
			(x + width, z, y),
			(x, z, y),
			(x, z + density, y),
			(x + width, z + density, y + height - 1.8),
			(x, z + density, y + height - 1.8)]

		faces = [
			(0, 1, 2, 3),
			(4, 1, 2, 5),
			(0, 4, 5, 3),
			(2, 5, 3),
			(0, 4, 1)]
			
	#Slope going down from north to south 
	if direction == 'NS':
		verts = [
			(x + width, z + density, y),
			(x + width, z, y),
			(x, z, y),
			(x, z + density, y),
			(x + width, z, y + height - 1.8),
			(x, z, y + height - 1.8)]

		faces = [
			(0, 1, 2, 3),
			(2, 1, 4, 5),
			(5, 4, 0, 3),
			(2, 5, 3),
			(0, 4, 1)]
			
	#Slope going down from east to west 
	if direction == 'EW':
		verts = [
			(x + width, z + density, y),
			(x + width, z, y),
			(x, z, y),
			(x, z + density, y),
			(x, z + density, y + height - 1.8),
			(x, z, y + height - 1.8)]

		faces = [
			(0, 1, 2, 3),
			(3, 2, 5, 4),
			(5, 1, 0, 4),
			(2, 1, 5),
			(0, 3, 4)]
			
	#Slope going down from west to east 
	if direction == 'WE':
		verts = [
			(x + width, z + density, y),
			(x + width, z, y),
			(x, z, y),
			(x, z + density, y),
			(x + width, z + density, y + height - 1.8),
			(x + width, z, y + height - 1.8)]

		faces = [
			(0, 1, 2, 3),
			(3, 2, 5, 4),
			(5, 1, 0, 4),
			(2, 1, 5),
			(0, 3, 4)]

	#<>
	if direction == 'NESW':
		verts = [
			(x + (width / 2), z + density, y),
			(x + width, z + (density / 2), y),
			(x + (width / 2), z, y),
			(x, z + (density / 2), y),
			(x + (width / 2), z + density, y + height),
			(x + width, z + (density / 2), y + height),
			(x + (width / 2), z, y + height),
			(x, z + (density / 2), y + height)]

		faces = [
			(0, 1, 2, 3),
			(4, 7, 6, 5),
			(0, 4, 5, 1),
			(1, 5, 6, 2),
			(2, 6, 7, 3),
			(4, 0, 3, 7)]

	mesh = bpy.data.meshes.new(tag + lib_tools.fix_id(index)  + '_MESH')
	prism = bpy.data.objects.new(tag + lib_tools.fix_id(index), mesh)
	bpy.context.scene.objects.link(prism)
	mesh.from_pydata(verts, [], faces)
	mesh.update()	
	prism.select = True
	bpy.ops.object.move_to_layer(layers=(True, False, False, False, False, 
										 False, False, False, False, False, 
										 False, False, False, False, False, 
										 False, False, False, False, False))
	bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
	prism.select = False
	bpy.context.scene.update()

def create_quadrangle(name, x1, z1, x2, z2, x3, z3, x4, z4, y):
	verts = [
		(x1, z1, y),
		(x2, z2, y),
		(x3, z3, y),
		(x4, z4, y)]

	faces = [(0, 1, 2, 3)]

	mesh = bpy.data.meshes.new(name + '_MESH')
	quad = bpy.data.objects.new(name, mesh)
	bpy.context.scene.objects.link(quad)
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	quad.select = True
	bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
	quad.select = False
	bpy.context.scene.update()

#=======================================================================================================================
# IMPORT FUNCTIONS...
#=======================================================================================================================
def import_rid(data):
	print('[IO_RDT]  <IMPORT> RID ' + str(data.version))

	if len(data.object) > 0:
		
		for i in range(len(data.object)):
			if data.version == 1.0:
				x = float(data.object[i].x) / v_scale
				y = -float(data.object[i].y) / v_scale
				z = float(data.object[i].z) / v_scale
				target_x = float(data.object[i].target_x) / v_scale
				target_y = -float(data.object[i].target_y) / v_scale
				target_z = float(data.object[i].target_z) / v_scale
				fov = float(data.object[i].fov) / 10.0

			if data.version == 1.5 or data.version == 2.0 or data.version == 3.0:
				x = float(data.object[i].x) / v_scale
				y = -float(data.object[i].y) / v_scale
				z = float(data.object[i].z) / v_scale
				target_x = float(data.object[i].target_x) / v_scale
				target_y = -float(data.object[i].target_y) / v_scale
				target_z = float(data.object[i].target_z) / v_scale
				fov = float(data.object[i].fov) / v_scale - 6.0

			create_camera(i, x, y, z, target_x, target_y, target_z, fov)

	else:
		print('!!! ERROR: NO OBJECTS AVAILABLE')

def import_rvd(data):									   #MISSING BIO1 SUPPORT ATM
	print('[IO_RDT] <IMPORT> RVD ' + str(data.version))

	if bpy.data.materials.get('MTL_RVD_ZONE') is None:
		mat = create_material('MTL_RVD_ZONE', (0.0, 0.255, 0.225), (0.0, 0.255, 0.225), 0.1)
	if bpy.data.materials.get('MTL_RVD_SWITCH') is None:
		mat2 = create_material('MTL_RVD_SWITCH', (0.888, 0.666, 0), (0.888, 0.666, 0), 0.2)

	current_cam = -1
	switch_id = 0

	if len(data.object) > 0:
		for i in range(len(data.object)):

			if data.version == 1.5 or data.version == 2.0 or data.version == 3.0:
				if data.object[i].floor != 255:
					y = data.object[i].floor * 1.8
				else:
					y = 0

				if data.object[i].cam_0 != current_cam:
					name = 'RVD_' + lib_tools.fix_id(data.object[i].cam_0) + '_ZONE'
					mat = bpy.data.materials.get('MTL_RVD_ZONE')
					current_cam = data.object[i].cam_0
					switch_id = 0

				else:
					name = 'RVD_' + lib_tools.fix_id(data.object[i].cam_0) + '_SWITCH_' + lib_tools.fix_id(switch_id)
					mat = bpy.data.materials.get('MTL_RVD_SWITCH')
					switch_id += 1

				create_quadrangle(name,
								  float(data.object[i].x1) / v_scale,
								  float(data.object[i].z1) / v_scale,
								  float(data.object[i].x2) / v_scale,
								  float(data.object[i].z2) / v_scale,
								  float(data.object[i].x3) / v_scale,
								  float(data.object[i].z3) / v_scale,
								  float(data.object[i].x4) / v_scale,
								  float(data.object[i].z4) / v_scale,
								  y)

			bpy.data.objects[name].data.materials.append(mat)
			bpy.data.objects[name].show_transparent = True
			bpy.data.objects[name].show_wire = True
			bpy.data.objects[name].select = True
			bpy.ops.object.move_to_layer(layers=(False, False, True, False, False, 
												False, False, False, False, False, 
												False, False, False, False, False, 
												False, False, False, False, False))
			bpy.data.objects[name].select = False
			bpy.data.objects[name]['FLAG'] = data.object[i].flag
			bpy.data.objects[name]['FLOOR'] = data.object[i].floor
			bpy.data.objects[name]['CAM_1'] = data.object[i].cam_1

			#bpy.data.objects['RVD_' + lib_tools.fix_id(i)].hide = True
	else:
		print('!!! ERROR: NO OBJECTS AVAILABLE')

def import_lit(data):	#missing BIO3!
	print('[IO_RDT] <IMPORT> LIT ' + str(data.version))

	if len(data.object) > 0:
		if data.version == 1.0:
			#CREATE LIGHTS... 
			bpy.ops.group.create(name='LIT')
		
			lit0 = bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(
				float(data.object[0].position.x) / v_scale, 
				float(data.object[0].position.z) / v_scale, 
				float(-data.object[0].position.y) / v_scale))

			bpy.context.object.name = 'LIT_00'
			bpy.context.object.data.energy = data.object[0].luminosity
			bpy.context.object.data.distance = 1
			bpy.context.object.data.color = (data.object[0].color.r, data.object[0].color.g, data.object[0].color.b)
			bpy.ops.object.group_link(group='LIT')
			 
			lit1 = bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(
				float(data.object[1].position.x) / v_scale, 
				float(data.object[1].position.z) / v_scale, 
				float(-data.object[1].position.y) / v_scale))

			bpy.context.object.name = 'LIT_01'
			bpy.context.object.data.energy = data.object[1].luminosity
			bpy.context.object.data.distance = 1
			bpy.context.object.data.color = (data.object[1].color.r, data.object[1].color.g, data.object[1].color.b)
			bpy.ops.object.group_link(group='LIT')   
				
			lit2 = bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(
				float(data.object[2].position.x) / v_scale, 
				float(data.object[2].position.z) / v_scale, 
				float(-data.object[2].position.y) / v_scale))

			bpy.context.object.name = 'LIT_02'
			bpy.context.object.data.energy = data.object[2].luminosity
			bpy.context.object.data.distance = 1
			bpy.context.object.data.color = (data.object[2].color.r, data.object[2].color.g, data.object[2].color.b)
			bpy.ops.object.group_link(group='LIT')				
		
			bpy.context.scene.update()									#ONLY BH1 SUPPORTED ATM !! ADD TYPE AND MODE AND OTHER MISSING STUFF BIO2!

		if data.version == 1.5 or data.version == 2.0:

			for i in range(len(data.object)):
				
				#Create group to house each 3 point lights per object
				bpy.ops.group.create(name='LIT_' + lib_tools.fix_id(i))

				lit0 = bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(float(data.object[i].position[0].x) / v_scale, 
																			 float(data.object[i].position[0].z) / v_scale, 
																			 float(-data.object[i].position[0].y) / v_scale), layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

				bpy.context.object.name = 'LIT_' + lib_tools.fix_id(i) + '_00'
				bpy.context.object.data.energy = data.object[i].luminosity[0] / v_scale
				bpy.context.object.data.distance = 1
				bpy.context.object.data.color = (data.object[i].color[0].r/255, data.object[i].color[0].g/255, data.object[i].color[0].b/255)			
				bpy.ops.object.group_link(group='LIT_' + lib_tools.fix_id(i))


				lit1 = bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(float(data.object[i].position[1].x) / v_scale, 
																			 float(data.object[i].position[1].z) / v_scale, 
																			 float(-data.object[i].position[1].y) / v_scale), layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
				
				bpy.context.object.name = 'LIT_' + lib_tools.fix_id(i) + '_01'
				bpy.context.object.data.energy = data.object[i].luminosity[1] / v_scale
				bpy.context.object.data.distance = 1
				bpy.context.object.data.color = (data.object[i].color[1].r/255, data.object[i].color[1].g/255, data.object[i].color[1].b/255)
				bpy.ops.object.group_link(group='LIT_' + lib_tools.fix_id(i))


				lit2 = bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(float(data.object[i].position[2].x) / v_scale, 
																			 float(data.object[i].position[2].z) / v_scale, 
																			 float(-data.object[i].position[2].y) / v_scale), layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
				
				bpy.context.object.name = 'LIT_' + lib_tools.fix_id(i) + '_02'
				bpy.context.object.data.energy = data.object[i].luminosity[2] / v_scale
				bpy.context.object.data.distance = 1
				bpy.context.object.data.color = (data.object[i].color[2].r/255, data.object[i].color[2].g/255, data.object[i].color[2].b/255)
				bpy.ops.object.group_link(group='LIT_' + lib_tools.fix_id(i))



				bpy.context.scene.update()

def import_sca(data):
	print('[IO_RDT]  <IMPORT> SCA ' + str(data.version))

	if len(data.object) > 0:
 		#Create materials...
		create_material('MTL_SCA_Cube', (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), 0.25)
		create_material('MTL_SCA_Cylinder', (0.0, 0.5, 0.0), (1.0, 1.0, 1.0), 0.25)
		create_material('MTL_SCA_Prism', (0.0, 0.5, 0.0), (1.0, 1.0, 1.0), 0.25)
		create_material('MTL_SCA_Diamond', (0.5, 0.5, 0.5), (1.0, 1.0, 1.0), 0.25)
		create_material('MTL_SCA_Slope', (0.5, 1.0, 0.5), (1.0, 1.0, 1.0), 0.50)
		create_material('MTL_SCA_Stairs', (1.0, 1.0, 0.0), (1.0, 1.0, 1.0), 0.50)
		create_material('MTL_SCA_Climb_up', (0.0, 1.0, 0.0), (1.0, 1.0, 1.0), 0.50)
		create_material('MTL_SCA_Climb_down', (0.0, 0.8, 0.0), (1.0, 1.0, 1.0), 0.50)
		create_material('MTL_SCA_Half_cylinder', (0.0, 1.0, 0.0), (1.0, 1.0, 1.0), 0.25)

		#Create ceiling object...
		if data.version == 1.0 or data.version == 1.5:
			print('N/A')
		if data.version == 2.0:
			create_plane("SCA_CEILING", 0, data.ceiling_x / v_scale, -(data.ceiling_z/ v_scale), data.ceiling_y/ v_scale, data.ceiling_width/ v_scale, data.ceiling_density/ v_scale )

			obj = bpy.data.objects.get('SCA_CEILING00')
			obj.name = "SCA_CEILING"
			obj.data.name = "SCA_CEILING"

		if data.version == 3.0:
			print('N/A')

		#Create objects...
		for i in range(len(data.object)):		
			#==================================================================================================================
			#BIO HAZARD
			#==================================================================================================================
			if data.version == 1.0:
				x = float(data.object[i].x2) / v_scale
				y = 0
				z = float(data.object[i].z2) / v_scale
				width = float(data.object[i].x1 - data.object[i].x2) / v_scale
				height = float(data.object[i].floor) * 1.8
				density = float(data.object[i].z1 - data.object[i].z2) / v_scale
				shape = data.object[i].type
					
				#0 - Unassigned/placeholder?
				if shape == 0:
					create_cube('SCA_', i, x, y, z, width, height, density)
					
				#1 - Standard rectangle
				if shape == 1:
					create_cube('SCA_', i, x, y, z, width, height, density)
					
				#3: circles/pillars
				if shape == 3:
					create_cylinder('SCA_', i, x, y, z, width, height, density)

				#4 - Prism?
				if shape == 4:
					create_cube('SCA_', i, x, y, z, width, height, density)
					
				#5 - Prism?
				if shape == 5:
					create_cube('SCA_', i, x, y, z, width, height, density)
				
				#Last resort, create unknown shape as rectangle/cube		
				if bpy.data.objects.get('SCA_' + lib_tools.fix_id(i)) is None:
					create_cube('SCA_', i, x, y, z, width, height, density)
				
				#add object properties...
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Shape"]=shape
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["u0"]=data.object[i].u0
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["u1"]=data.object[i].u1
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor"]=data.object[i].floor			
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Version"]=data.version
				
			#==================================================================================================================
			#BIOHAZARD 2 PROTOTYPE
			#==================================================================================================================
			if data.version == 1.5:
				x = float(data.object[i].x) / v_scale
				y = float(data.object[i].u1) * 1.8
				z = float(data.object[i].z) / v_scale
				width = float(data.object[i].width) / v_scale
				height = (float(data.object[i].floor) * 1.8)
				density = float(data.object[i].density) / v_scale
				shape = data.object[i].type

				#0 - Empty (Placeholder for script use)
				if shape == 0:
					create_cube('SCA_', i, x, y, z, width, height, density)

				#1 - Standard rectangle
				if shape == 1:
					create_cube('SCA_', i, x, y, z, width, height, density)

				#2 - Prism <>
				if shape == 2:
					create_prism('SCA_', i, x, y, z, width, height, density, 'NESW')

				#3 - Cylinder/circle/pillar
				if shape == 3:
					create_cylinder('SCA_', i, x, y, z, width, height, density)

				#4 - Prism \|
				if shape == 4:
					create_prism('SCA_', i, x, y, z, width, height, density, 'NE')

				#5 - Prism |/
				if shape == 5:
					create_prism('SCA_', i, x, y, z, width, height, density, 'NW')

				#6 - Prism /|
				if shape == 6:
					create_prism('SCA_', i, x, y, z, width, height, density, 'SE')

				#7 - Prism |\
				if shape == 7:
					create_prism('SCA_', i, x, y, z, width, height, density, 'SW')

				#8 - Rectangle with rounded corners on x-axis
				if shape == 8:
					create_cylinder('SCA_', i, x, y, z, width, height, density)

				#9 - Rectangle with rounded corners on y-axis
				if shape == 9:
					create_cylinder('SCA_', i, x, y, z, width, height, density)
				
				#Last resort, create unknown shape as rectangle/cube
				if bpy.data.objects.get('SCA_' + lib_tools.fix_id(i)) is None:
					create_cube('SCA_', i, x, y, z, width, height, density)
				
				#add object properties...
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Shape"]=shape
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["u0"]=data.object[i].u0
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["u1"]=data.object[i].u1
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor"]=data.object[i].floor			
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Version"]=data.version
				
			#==================================================================================================================
			#BIOHAZARD 2
			#==================================================================================================================
			if data.version == 2.0:

				#Prepare bitmask data for later use as properties
				b_id = bin(data.object[i].id).replace('0b','').zfill(16)
				b_typ = bin(data.object[i].type).replace('0b','').zfill(16)
				b_floor = bin(data.object[i].floor).replace('0b','').zfill(32)

				id_shape = int(b_id[12:16], 2)
				id_weapon_collision = int(b_id[8:12], 2)				
				id_can_walk_under = int(b_id[7], 2)
				id_unknown_0 = int(b_id[7], 2)
				id_enemy_collision = int(b_id[6], 2)
				id_unknown_1 = int(b_id[5], 2)
				id_unknown_2 = int(b_id[4], 2)
				id_bullet_collision = int(b_id[3], 2)
				id_object_collision = int(b_id[2], 2)
				id_player_collision = int(b_id[1], 2)

				type_width_multiplicator = int(b_typ[14:16], 2)
				type_depth_multiplicator = int(b_typ[12:14], 2)
				type_climb_direction = int(b_typ[10:12], 2)
				type_height_multiplicator = int(b_typ[4:10], 2)
				type_dummy_9 = int(b_typ[0:4], 2)

				y_data = calc_y_data(data.object[i].floor)
				x = float(data.object[i].x) / v_scale
				y = y_data[0]
				z = float(data.object[i].z) / v_scale
				width = float(data.object[i].width) / v_scale
				height = y_data[1]
				density = float(data.object[i].density) / v_scale
				
				#Standard rectangle/cube
				if id_shape == 0:
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Cube'))
				
				#Prism |\ 
				if id_shape == 1:
					create_prism('SCA_', i, x, y, z, width, height, density, 'NE')
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Prism'))
				
				#Prism /|
				if id_shape == 2:
					create_prism('SCA_', i, x, y, z, width, height, density, 'NW')
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Prism'))

				#Prism |/
				if id_shape == 3:
					create_prism('SCA_', i, x, y, z, width, height, density, 'SE')
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Prism'))

				#Prism \|
				if id_shape == 4:
					create_prism('SCA_', i, x, y, z, width, height, density, 'SW')
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Prism'))

				#Prism <>
				if id_shape == 5:
					create_prism('SCA_', i, x, y, z, width, height, density, 'NESW')
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Prism'))

				#Cylinder/Circle/Pillar
				if id_shape == 6:
					y = y_data[0]
					#height = y_data[0] + y_data[1]
					heigth = type_height_multiplicator * 1.8
					create_cylinder('SCA_', i, x, y, z, width, (y_data[0]) + ((type_height_multiplicator * 1.8)), density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Cylinder'))

				#Rectangle with rounded corners on x-axis
				if id_shape == 7:						
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Cube'))
				
				#Rectangle with rounded corners on y-axis
				if id_shape == 8:						
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Cube'))

				#Rectangle "Climb up area"
				if id_shape == 9:						
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Climb_up'))

				#Rectangle "Climb down area"
				if id_shape == 10:						
					create_cube('SCA_', i, x, y, z, width, height, density)	
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Climb_down'))
					
				#Slope
				if id_shape == 11:
									
					if type_climb_direction == 0:
						create_prism('SCA_', i, x, y, z, width, height, density, 'WE')	

					if type_climb_direction == 1:	
						create_prism('SCA_', i, x, y, z, width, height, density, 'EW')						
					
					if type_climb_direction == 2:
						create_prism('SCA_', i, x, y, z, width, height, density, 'SN')
				
					if type_climb_direction == 3:
						create_prism('SCA_', i, x, y, z, width, height, density, 'NS')

					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Slope'))

				#Rectangle "Stairs"
				if id_shape == 12:
					height -= 1.8
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Stairs'))

				#Half cylinder? (only found in ROOM40B and ROOM40F	)
				if id_shape == 13:						
					create_cube('SCA_', i, x, y, z, width, height, density)					
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Half_cylinder'))
				
				#ADD FAILSAFE AGAINST ILLEGAL SHAPE !	
				bpy.data.objects['SCA_' + lib_tools.fix_id(i)].draw_type = 'SOLID'
				bpy.data.objects['SCA_' + lib_tools.fix_id(i)].show_transparent = True
				bpy.data.objects['SCA_' + lib_tools.fix_id(i)].show_wire = True
				bpy.data.objects['SCA_' + lib_tools.fix_id(i)].show_name = True
				
				if id_weapon_collision == 8:
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].draw_type = 'SOLID'
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].show_transparent = False

				#add object properties...
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_0_Shape"]=id_shape
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_1_Weapon collision"]=id_weapon_collision
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_2_Can walk under"]=id_can_walk_under
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_3_Unknown 0"]=id_unknown_0
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_4_Enemy collision"]=id_enemy_collision
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_5_Unknown 1"]=id_unknown_1
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_6_Unknown 2"]=id_unknown_2
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_7_Bullet collision"]=id_bullet_collision
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_8_Object collision"]=id_object_collision
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_9_Player collision"]=id_player_collision
				
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Type_0_Width multiplicator"]=type_width_multiplicator
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Type_1_Depth multiplicator"]=type_depth_multiplicator
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Type_2_Climb direction"]=type_climb_direction
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Type_3_Height multiplicator"]=type_height_multiplicator
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Type_4_Dummy 9"]=type_dummy_9
				
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_00"]=b_floor[31]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_01"]=b_floor[30]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_02"]=b_floor[29]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_03"]=b_floor[28]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_04"]=b_floor[27]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_05"]=b_floor[26]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_06"]=b_floor[25]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_07"]=b_floor[24]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_08"]=b_floor[23]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_09"]=b_floor[22]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_10"]=b_floor[21]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_11"]=b_floor[20]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_12"]=b_floor[19]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_13"]=b_floor[18]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_14"]=b_floor[17]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_15"]=b_floor[16]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_16"]=b_floor[15]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_17"]=b_floor[14]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_18"]=b_floor[13]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_19"]=b_floor[12]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_20"]=b_floor[11]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_21"]=b_floor[10]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_22"]=b_floor[9]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_23"]=b_floor[8]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_24"]=b_floor[7]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_25"]=b_floor[6]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_26"]=b_floor[5]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_27"]=b_floor[4]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_28"]=b_floor[3]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_29"]=b_floor[2]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_30"]=b_floor[1]
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor_31"]=b_floor[0]


			#==================================================================================================================
			#BIOHAZARD 3 LAST ESCAPE
			#==================================================================================================================				
			if data.version == 3.0:
				x = float(data.object[i].x1) / v_scale
				y = data.object[i].u3 * 1.8
				z = float(data.object[i].z1) / v_scale
				width = float(data.object[i].x2 - data.object[i].x1) / v_scale
				height = (float(-data.object[i].floor) / v_scale) - y
				density = float(data.object[i].z2 - data.object[i].z1) / v_scale
				
				#Prepare bitmask data for later use as properties
				b_id = bin(data.object[i].id).replace('0b','').zfill(16)
				b_typ = bin(data.object[i].type).replace('0b','').zfill(16)
				b_floor = bin(data.object[i].floor).replace('0b','').zfill(16)
				
				id_shape = int(b_id[12:16], 2)
				id_direction = int(b_id[10:12], 2)
				id_weapon_collision = int(b_id[8:10], 2)				
				id_can_walk_under = int(b_id[7], 2)
				id_unknown_0 = int(b_id[7], 2)
				id_enemy_collision = int(b_id[6], 2)
				id_unknown_1 = int(b_id[5], 2)
				id_unknown_2 = int(b_id[4], 2)
				id_bullet_collision = int(b_id[3], 2)
				id_object_collision = int(b_id[2], 2)
				id_player_collision = int(b_id[1], 2)

				#R101	106 med stairs   (8 step)
				#R101	122 small stairs (4 step)
				
				#Cylinders...
				if id_shape == 0:
					create_cylinder('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Cylinder'))

				#Cubes...
				if id_shape == 1:
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Cube'))

				#2		 <> ?
				if id_shape == 2:
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Cube'))

				#Prism \|
				if id_shape == 3:
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Cube'))

				#Prism |\
				if id_shape == 4:
					if id_direction == 0:
						create_prism('SCA_', i, x, y, z, width, height, density, 'NE')

					if id_direction == 1:
						create_prism('SCA_', i, x, y, z, width, height, density, 'NW')
						
					if id_direction == 2:
						create_prism('SCA_', i, x, y, z, width, height, density, 'SE')
						
					if id_direction == 3:
						create_prism('SCA_', i, x, y, z, width, height, density, 'SW')
				#5
				if id_shape == 5:
					create_prism('SCA_', i, x, y, z, width, height, density, 'NW')
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Prism'))

				#Prisms... \|
				if id_shape == 6:
					if id_direction == 0:
						create_prism('SCA_', i, x, y, z, width, height, density, 'NE')

					if id_direction == 1:
						create_prism('SCA_', i, x, y, z, width, height, density, 'NW')
						
					if id_direction == 2:
						create_prism('SCA_', i, x, y, z, width, height, density, 'SE')
						
					if id_direction == 3:
						create_prism('SCA_', i, x, y, z, width, height, density, 'SW')

						
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Prism'))

				#7 // Climb up zone
				if id_shape == 7:
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Climb_up'))

				#8 // Climb down zone
				if id_shape == 8:
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Climb_down'))

				#Slopes...
				if id_shape == 9:
					
					if id_direction == 0:
						create_prism('SCA_', i, x, y, z, width, height, density, 'WE')
					
					if id_direction == 1:
						create_prism('SCA_', i, x, y, z, width, height, density, 'EW')
						
					if id_direction == 2:
						create_prism('SCA_', i, x, y, z, width, height, density, 'SN')

					if id_direction == 3:
						create_prism('SCA_', i, x, y, z, width, height, density, 'NS')
						
						
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Slope'))

					#ROOM500 #11 N>S

				#Stairs
				if id_shape == 10:
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Stairs'))

 				#11
				if id_shape == 11:
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Cube'))

				#12
				if id_shape == 12:
					create_cube('SCA_', i, x, y, z, width, height, density)
					bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_Cube'))

				#if sca_type == 54 or sca_type == 118 or sca_type == 246:
				#	create_prism('SCA_', i, x, y, z, width, height, density, 'SW')

				#Prism NE


				#if id_shape == 22 or sca_type == 86 or sca_type == 214:
				#	create_prism('SCA_', i, x, y, z, width, height, density, 'NW')

				#if id_shape == 38 or sca_type == 102:
				#	create_prism('SCA_', i, x, y, z, width, height, density, 'SE')

				if bpy.data.objects.get('SCA_' + lib_tools.fix_id(i)) is None:
					create_cube('SCA_', i, x, y, z, width, height, density)
		  		
				#add object properties...
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_0_Shape"]=id_shape
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_0_Direction"]=id_direction
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_1_Weapon collision"]=id_weapon_collision
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_2_Can walk under"]=id_can_walk_under
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_3_Unknown 0"]=id_unknown_0
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_4_Enemy collision"]=id_enemy_collision
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_5_Unknown 1"]=id_unknown_1
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_6_Unknown 2"]=id_unknown_2
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_7_Bullet collision"]=id_bullet_collision
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_8_Object collision"]=id_object_collision
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["ID_9_Player collision"]=id_player_collision
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Type"]=data.object[i].type
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["u0"]=data.object[i].u0
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["u1"]=data.object[i].u1
				bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Floor"]=float(-data.object[i].floor)
		


			if (len(bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials) == 0):
				bpy.data.objects['SCA_' + lib_tools.fix_id(i)].data.materials.append(bpy.data.materials.get('MTL_SCA_00'))

			

			bpy.data.objects['SCA_' + lib_tools.fix_id(i)].show_wire = True
			bpy.data.objects['SCA_' + lib_tools.fix_id(i)].show_transparent = True
			bpy.data.objects['SCA_' + lib_tools.fix_id(i)].draw_type = 'SOLID'
			#bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))["Version"]=data.version
	else:
		print('!!! ERROR: NO OBJECTS AVAILABLE')

def import_blk(data):
	print('[IO_RDT]  <IMPORT> BLK ' + str(data.version))

	if len(data.object) > 0:
		if bpy.data.materials.get('MTL_BLK') is None:
			mat = create_material('MTL_BLK', (0.5, 0.5, 1.0), (1.0, 1.0, 1.0), 0.25)
		
		for i in range(len(data.object)):
			x = float(data.object[i].x1) / v_scale
			y = 0
			z = float(data.object[i].z1) / v_scale
			width = float(data.object[i].x2 - data.object[i].x1) / v_scale
			density = float(data.object[i].z2 - data.object[i].z1) / v_scale

			create_plane('BLK_', i, x, y, z, width, density)
			bpy.data.objects['BLK_' + lib_tools.fix_id(i)]['DIRECTION'] = data.object[i].direction
			bpy.data.objects['BLK_' + lib_tools.fix_id(i)]['ATTRIBUTE'] = data.object[i].attribute
			bpy.data.objects['BLK_' + lib_tools.fix_id(i)].data.materials.append(mat)
			bpy.data.objects['BLK_' + lib_tools.fix_id(i)].show_wire = True
			bpy.data.objects['BLK_' + lib_tools.fix_id(i)].show_transparent = True
			bpy.data.objects['BLK_' + lib_tools.fix_id(i)].draw_type = 'SOLID'
	else:
		print('!!! ERROR: NO OBJECTS AVAILABLE')

def import_flr(data):
	print('[IO_RDT]  <IMPORT> FLR ' + str(data.version))

	if len(data.object) > 0:
		if bpy.data.materials.get('MTL_FLR') is None:
			mat = create_material('MTL_FLR', (1.0, 0.0, 1.0), (1.0, 1.0, 1.0), 0.25)

		for i in range(len(data.object)):
			x = float(data.object[i].x) / v_scale
			y = 0
			z = float(data.object[i].z) / v_scale
			width = float(data.object[i].width) / v_scale
			density = float(data.object[i].density) / v_scale

			create_plane('FLR_', i, x, y, z, width, density)
			bpy.data.objects['FLR_' + lib_tools.fix_id(i)]['SOUND'] = data.object[i].sound
			bpy.data.objects['FLR_' + lib_tools.fix_id(i)]['FLAG'] = data.object[i].flag
			bpy.data.objects['FLR_' + lib_tools.fix_id(i)].data.materials.append(mat)
			bpy.data.objects['FLR_' + lib_tools.fix_id(i)].show_wire = True
			bpy.data.objects['FLR_' + lib_tools.fix_id(i)].show_transparent = True
			bpy.data.objects['FLR_' + lib_tools.fix_id(i)].draw_type = 'SOLID'
	else:
		print('!!! ERROR: NO OBJECTS AVAILABLE')

def import_rdt(context, filepath):
	print('\n' + ("=" * 96) + '\n')
	print("BIOHAZARD RDT FILE IMPORT" + '\n')
	print("=" * 96)
	print("2014, 2019 - MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)")
	print("=" * 96)

	rdt_dir = lib_rdt.get_rdt_dir(filepath) 
	rdt_name = lib_rdt.get_rdt_name(filepath)
	rdt_version = float(lib_rdt.get_rdt_version(filepath))
	wip_dir = rdt_dir + '/WIP'
	tmp_rdt = lib_rdt.rdt_file(rdt_version)

	print('FILE:	' + filepath.upper())
	print('WIP_DIR: ' + wip_dir + '/' + rdt_name)
	print('ROOM_ID: ' + rdt_name.upper())
	print('VERSION: ' + str(rdt_version))
	print('=' * 96)

	#add filesize and other checks...
	if os.path.exists(filepath):

		#check if source folder is read only
		if os.access(filepath, os.W_OK):
			lib_tools.create_dir(wip_dir)

			#check for wip version of RDT file
			if os.path.exists(wip_dir + '/' + rdt_name):
				print('FOUND WIP VERSION')
				print('>> LOADING WIP VERSION')

				if os.path.exists(wip_dir + '/' + rdt_name + '/CAMERA/CAMERAS.RID'):
					tmp_rdt.rid = tmp_rdt.rid.read_from_file(wip_dir + '/' + rdt_name + '/CAMERA/CAMERAS.RID')

				if os.path.exists(wip_dir + '/' + rdt_name + '/CAMERA/ZONES.RVD'):
					tmp_rdt.rvd = tmp_rdt.rvd.read_from_file(wip_dir + '/' + rdt_name + '/CAMERA/ZONES.RVD')

				if os.path.exists(wip_dir + '/' + rdt_name + '/CAMERA/LIGHTS.LIT'):
					tmp_rdt.lit = tmp_rdt.lit.read_from_file(wip_dir + '/' + rdt_name + '/CAMERA/LIGHTS.LIT')

				if os.path.exists(wip_dir + '/' + rdt_name + '/CAMERA/COLLISIONS.SCA'):
					tmp_rdt.sca = tmp_rdt.sca.read_from_file(wip_dir + '/' + rdt_name + '/CAMERA/COLLISIONS.SCA')
			
				if os.path.exists(wip_dir + '/' + rdt_name + '/CAMERA/FLOORS.FLR'):
					tmp_rdt.flr = tmp_rdt.flr.read_from_file(wip_dir + '/' + rdt_name + '/CAMERA/FLOORS.FLR')

				if os.path.exists(wip_dir + '/' + rdt_name + '/CAMERA/ROAMING.BLK'):
					tmp_rdt.blk = tmp_rdt.blk.read_from_file(wip_dir + '/' + rdt_name + '/CAMERA/ROAMING.BLK')

			else:
				print('>> CREATE WIP VERSION')
				lib_tools.create_dir(wip_dir + '/' + rdt_name)

				tmp_rdt = tmp_rdt.read(filepath)
				tmp_rdt.extract(wip_dir + '/' + rdt_name)
			
			#Add properties for file handling...
			bpy.context.scene["RDT_Name"] = rdt_name.upper()
			bpy.context.scene["RDT_Version"] = rdt_version
			bpy.context.scene["RDT_Directory"] = wip_dir + '/' + rdt_name
			
			#Set render resolution to 640x480
			bpy.context.scene.render.resolution_x = 640
			bpy.context.scene.render.resolution_y = 480
			bpy.context.scene.render.resolution_percentage = 100

			if rdt_version == 1.0:
				import_rid(tmp_rdt.rid)
				import_lit(tmp_rdt.lit)
				#import_rvd(tmp_rdt.rvd)
				import_sca(tmp_rdt.sca)

			if rdt_version == 1.5:
				import_rid(tmp_rdt.rid)
				import_rvd(tmp_rdt.rvd)
				import_lit(tmp_rdt.lit)
				import_sca(tmp_rdt.sca)
				import_blk(tmp_rdt.blk)

			if rdt_version == 2.0:
				import_rid(tmp_rdt.rid)
				import_rvd(tmp_rdt.rvd)
				import_lit(tmp_rdt.lit)
				import_sca(tmp_rdt.sca)
				import_blk(tmp_rdt.blk)
				import_flr(tmp_rdt.flr)

			if rdt_version == 3.0:
				import_rid(tmp_rdt.rid)
				import_rvd(tmp_rdt.rvd)
				import_sca(tmp_rdt.sca)

		else:
			print('FILE ERROR: READ-ONLY ACCESS')
			print('THE PLUGIN CAN NOT CREATE WIP FOLDERS IN READ-ONLY DIRECTORIES')
			print('CHECK IF YOU TRIED TO LOAD A FILE DIRECTLY FROM CD-ROM ETC.')

	return {'FINISHED'}

def import_scd_main():
	print('[IO_RDT]  <IMPORT> SCD_MAIN ')

#=======================================================================================================================
# EXPORT FUNCTIONS...
#=======================================================================================================================
def export_rid(filepath, version):
	print('=' * 64)
	print('RID EXPORT')
	print('=' * 64)

	#get total object amount...
	obj_count = get_obj_count('RID_', 64)
	
	if obj_count > 0:
		print('FOUND OBJECT COUNT: ' + str(obj_count))
	
		#get object data
		tmp_rid = lib_rid.rid_file(version)

		for i in range(obj_count):
			
			tmp_rid_obj = lib_rid.rid_object(version)

			if bpy.data.objects.get('RID_' + lib_tools.fix_id(i)) is not None and bpy.data.objects.get('RID_' + lib_tools.fix_id(i) + '_AIM') is not None:	
				
				cam_obj = bpy.data.objects.get('RID_' + lib_tools.fix_id(i))
				cam_target_obj = bpy.data.objects.get('RID_' + lib_tools.fix_id(i) + '_AIM')
			
				if version == 1.0:
					tmp_rid_obj.fov = int((round(cam_obj.data.lens, 5) + float(6)) * v_scale)
					tmp_rid_obj.x = int(cam_obj.location[0] * v_scale) 
					tmp_rid_obj.z = int(cam_obj.location[1] * v_scale)
					tmp_rid_obj.y = int(cam_obj.location[2] * v_scale)
					tmp_rid_obj.target_x = int(cam_target_obj.location[0] * v_scale)
					tmp_rid_obj.target_z = int(cam_target_obj.location[1] * v_scale)
					tmp_rid_obj.target_y = int(cam_target_obj.location[2] * v_scale)
					tmp_rid_obj.o_tim = 0xFFFFFFFF
					tmp_rid_obj.o_pri = 0xFFFFFFFF

				if version == 1.5 or version == 2.0 or version == 3.0:
					tmp_rid_obj.fov = int((round(cam_obj.data.lens, 5) + float(6)) * v_scale)
					tmp_rid_obj.x = int(round(cam_obj.location[0] * v_scale))
					print(str(i) + ' _ ' + str(tmp_rid_obj.fov))
					tmp_rid_obj.z = int(round(cam_obj.location[1] * v_scale))
					tmp_rid_obj.y = -int(round(cam_obj.location[2] * v_scale))
					tmp_rid_obj.target_x = int(round(cam_target_obj.location[0] * v_scale))
					tmp_rid_obj.target_z = int(round(cam_target_obj.location[1] * v_scale))
					tmp_rid_obj.target_y = int(round(cam_target_obj.location[2] * v_scale))
					tmp_rid_obj.o_pri = 0xFFFFFFFF

					if i == obj_count-1:
						tmp_rid_obj.flag = 1

				tmp_rid.object.append(tmp_rid_obj)
		
		print(str(len(tmp_rid.object)))
		tmp_rid.write_to_file(filepath)

def export_sca(filepath, version):	
	print('=' * 64)
	print('SCA EXPORT')
	print('=' * 64)
	
	#orientation point lower left corner!

	tmp_sca = lib_sca.sca_file(version)

	#get ceiling data...
	if bpy.data.objects.get('SCA_CEILING') is not None:
		obj = bpy.data.objects.get('SCA_CEILING')

		if version == 1.0:
			print('Ceiling of BIO1 SCA not implemented yet')

		if version == 2.0:
			print("Getting ceiling data...")
			tmp_sca.ceiling_x = int(round(obj.location[0] * v_scale))
			tmp_sca.ceiling_y = int(round(obj.location[2] * v_scale))
			tmp_sca.ceiling_z = int(round(obj.location[1] * v_scale))
			tmp_sca.ceiling_density = int(round(obj.dimensions[0] * v_scale))
			tmp_sca.ceiling_width = int(round(obj.dimensions[1] * v_scale))

			
	else:
		print("!!! CEILING IS MISSING --- WILL USE DUMMY PLACEHOLDER !!!")

	#get total object amount...
	obj_count = get_obj_count('SCA_', 64)
	
	tmp_sca.count = obj_count + 1

	print('FOUND OBJECT COUNT: ' + str(obj_count))
	
	for i in range(obj_count):
		
		tmp_obj = lib_sca.sca_object(version)
		
		if bpy.data.objects.get('SCA_' + lib_tools.fix_id(i)) is not None:	
			obj = bpy.data.objects.get('SCA_' + lib_tools.fix_id(i))
	
			if version == 2.0:

				tmp_obj.floor = int(round(obj.location[2] * v_scale))	   #needs fixing, isn't handling floor bit sets yet...
				tmp_obj.width  = int(round(obj.dimensions[0] * v_scale)) 
				tmp_obj.density  = int(round(obj.dimensions[1] * v_scale))
				tmp_obj.x = int(round(obj.location[0] * v_scale)) - int(tmp_obj.width / 2)
				tmp_obj.z = int(round(obj.location[1] * v_scale)) - int(tmp_obj.density / 2)
				#tmp_obj.id0 = int(obj["Shape"])
				h = int(round(obj.dimensions[2] * v_scale))

			tmp_sca.object.append(tmp_obj)
			#print(str(i) + "\tx: (" + str(x - int(w/2)) + ") y: (" + str(y - int(d/2)) + ") w: (" + str(w) + ") d: (" + (str(d) + ')'))
		else:
			print('!!! MISSING OBJECT: SCA_' + lib_tools.fix_id(i) + ' --- WILL BE FILLED BY A DUMMY PLACEHOLDER !!!')

	tmp_sca.write_to_file(filepath)

def export_rdt(context, filepath):
	print('\n' + ("=" * 96) + '\n')
	print("BIOHAZARD RDT FILE EXPORT" + '\n')
	print("=" * 96)
	print("2014, 2019 - MORTICIAN (THE_MORTICIAN@HOTMAIL.DE)")
	print("=" * 96)

	dir_selected = ""

	if (os.path.isdir(filepath)):
		print('Export RDT to ... ' + filepath)
		dir_selected = filepath.replace("\\", "/")
	else:
		print('Export RDT to... - ERROR! USE A FOLDER AS TARGET ' + filepath)
		print(os.path.dirname(filepath))
		dir_selected = os.path.dirname(filepath).replace("\\", "/")

	#Get properties for file handling...
	tmp_rdt_version = bpy.context.scene['RDT_Version']
	tmp_rdt_org_dir = bpy.context.scene['RDT_Directory']
	tmp_rdt_org_name = bpy.context.scene['RDT_Name']

	#Get wip dir...
	wip_dir = dir_selected
	rdt_dir = dir_selected + '/WIP/' + tmp_rdt_org_name + '/' + tmp_rdt_org_name + '.RDT'

	print('WIP_DIR ' + wip_dir)

	#Export data...
	if (os.path.isdir(wip_dir)):
		print('WIP DIR EXISTS! ' + dir_selected + '/WIP/' + tmp_rdt_org_name + '/')
		
		if os.path.exists(wip_dir + '/CAMERA') == False:
			lib_tools.create_dir(wip_dir + '/CAMERA')

		export_rid(wip_dir + '/CAMERA/CAMERAS.RID', tmp_rdt_version)
			#tmp_rdt.rvd = tmp_rdt.rvd.read_from_file(wip_dir + '/' + rdt_name + '/CAMERA/ZONES.RVD')
			#tmp_rdt.lit = tmp_rdt.lit.read_from_file(wip_dir + '/' + rdt_name + '/CAMERA/LIGHTS.LIT')
		export_sca(wip_dir + '/CAMERA/COLLISIONS.SCA', tmp_rdt_version)
			#tmp_rdt.flr = tmp_rdt.flr.read_from_file(wip_dir + '/' + rdt_name + '/CAMERA/FLOORS.FLR')
			#tmp_rdt.blk = tmp_rdt.blk.read_from_file(wip_dir + '/' + rdt_name + '/CAMERA/ROAMING.BLK')

		#Now rebuild the RDT file...!
		tmp_rdt = lib_rdt.rdt_file(tmp_rdt_version)
		tmp_rdt.rebuild(wip_dir + '/' + tmp_rdt_org_name + '.RDT')
	
	return {'FINISHED'}

#=======================================================================================================================
# OPERATORS...
#=======================================================================================================================
class rdt_import(Operator, ImportHelper):
	"""This appears in the tooltip of the operator and in the generated docs"""
	bl_idname = "lib_bio.io_rdt_blender_import"  # important since its how bpy.ops.lib_bio.io_rdt_blender is constructed
	bl_label = "Import RDT"
	filename_ext = ".rdt"

	filter_glob = StringProperty(
			default="*.rdt",
			options={'HIDDEN'},
			)

	opt_cam = BoolProperty(
			name=".RID",
			description="Import cameras",
			default=False,
			)
	opt_lit = BoolProperty(
			name=".RVD",
			description="Import camera switch zones",
			default=False,
			)
	opt_data_2 = BoolProperty(
			name=".LIT",
			description="Import lights",
			default=False,
			)
	opt_obj = BoolProperty(
			name=".SCA",
			description="Import collision boundaries",
			default=False,
			)
	opt_data_4 = BoolProperty(
			name=".FLR",
			description="Import floor step-sound areas",
			default=False,
			)
	opt_data_5 = BoolProperty(
			name=".BLK",
			description="Import enemy roaming areas",
			default=False,
			)

	def execute(self, context):
		return import_rdt(context, self.filepath)

class rdt_export(Operator, ImportHelper):
	"""This appears in the tooltip of the operator and in the generated docs"""
	bl_idname = "lib_bio.io_rdt_blender_export"	# important since its how bpy.ops.lib_bio.io_rdt_blender is constructed
	bl_label = "Export RDT"
	filename_ext = ""

	filter_glob = StringProperty(
			default="*.rdt",
			options={'HIDDEN'},
			)

	opt_cam = BoolProperty(
			name=".RID",
			description="Export cameras",
			default=False,
			)
	opt_lit = BoolProperty(
			name=".RVD",
			description="Export camera switch zones",
			default=False,
			)
	opt_data_2 = BoolProperty(
			name=".LIT",
			description="Export lights",
			default=False,
			)
	opt_obj = BoolProperty(
			name=".SCA",
			description="Export collision boundaries",
			default=False,
			)
	opt_data_4 = BoolProperty(
			name=".FLR",
			description="Export floor step-sound areas",
			default=False,
			)
	opt_data_5 = BoolProperty(
			name=".BLK",
			description="Export enemy roaming areas",
			default=False,
			)

	def execute(self, context):
		return export_rdt(context, self.filepath)

class rdt_tools_sca_panel(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "RDT SCA"
	bl_idname = "OBJECT_PT_hello"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = 'RDT'

	def draw(self, context):
		layout = self.layout
		split = layout.split()
		obj = context.object

		row = layout.row()
		col = split.column(align=True)
		col.operator("rdt_tools.button", text="Toogle data visibility").handle = 'toggle_vis_sca'
		col.operator("rdt_tools.button", text="Toogle object names").handle = 'toggle_name_sca'
		col.operator("rdt_tools.button", text="Toogle transparency").handle = 'toggle_transparency_sca'
		col.label(text="Create object")
		#col = split.column(align=True)
		col.operator("rdt_tools.button", text="0 - Standard").handle = 'sca_shape_0'
		col.operator("rdt_tools.button", text="1 - Triangle Upper-Left Corner").handle = 'sca_shape_1'
		col.operator("rdt_tools.button", text="2 - Triangle Upper-Right Corner").handle = 'sca_shape_2'
		col.operator("rdt_tools.button", text="3 - Triangle Lower-Left Corner").handle = 'sca_shape_3'
		col.operator("rdt_tools.button", text="4 - Triangle Lower-Right Corner").handle = 'sca_shape_4'
		col.operator("rdt_tools.button", text="5 - Diamond").handle = 'sca_shape_5'
		col.operator("rdt_tools.button", text="6-  Cylinder").handle = 'sca_shape_6'
		col.operator("rdt_tools.button", text="7 - Rectangle w. rounded corners x").handle = 'sca_shape_7'
		col.operator("rdt_tools.button", text="8 - Rectangle w. rounded corners y").handle = 'sca_shape_8'
		col.operator("rdt_tools.button", text="9 - Climb up area").handle = 'sca_shape_9'
		col.operator("rdt_tools.button", text="10 - Climb down area").handle = 'sca_shape_10'
		col.operator("rdt_tools.button", text="11 - Slope").handle = 'sca_shape_11'
		col.operator("rdt_tools.button", text="11 - Stairs").handle = 'sca_shape_12'
		col.operator("rdt_tools.button", text="13 - Half cylinder?").handle = 'sca_shape_13'

class rdt_tools_rid_panel(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "RDT RID"
	bl_idname = "OBJECT_PT_hello2"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = 'RDT'

	def draw(self, context):
		layout = self.layout
		split = layout.split()
		obj = context.object

		row = layout.row()
		col = split.column(align=True)
		col.operator("rdt_tools.button", text="Toogle data visibility").handle = 'toggle_vis_rid'
		col.operator("rdt_tools.button", text="Toogle object names").handle = 'toggle_name_rid'
		col.label(text="Create object")
		#col = split.column(align=True)
		col.operator("rdt_tools.button", text="Create camera set").handle = 'import_rbj'

class rdt_tools_button(bpy.types.Operator):
	bl_idname = "rdt_tools.button"
	bl_label = ""
	handle = bpy.props.StringProperty()

	def execute(self, context):
		
		if "toggle_vis" in self.handle: 
			#print('Toggle SCA object visibility')

			for i in range(get_obj_count(self.handle[-3:].upper() + "_", 64)):
				if bpy.data.objects.get(self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)) is not None:
					if bpy.data.objects[self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)].hide == False:
						bpy.data.objects[self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)].hide = True
					else:
						bpy.data.objects[self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)].hide = False

		if "toggle_name" in self.handle: 
			#print('Toggle SCA object visibility')

			for i in range(get_obj_count(self.handle[-3:].upper() + "_", 64)):
				if bpy.data.objects.get(self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)) is not None:
					if bpy.data.objects[self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)].show_name == False:
						bpy.data.objects[self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)].show_name = True
					else:
						bpy.data.objects[self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)].show_name = False
		
		if "toggle_transparency" in self.handle: 
			#print('Toggle SCA object visibility')

			for i in range(get_obj_count(self.handle[-3:].upper() + "_", 64)):
				if bpy.data.objects.get(self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)) is not None:
					if bpy.data.objects[self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)].show_transparent == False:
						bpy.data.objects[self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)].show_transparent = True
					else:
						bpy.data.objects[self.handle[-3:].upper() + "_" + lib_tools.fix_id(i)].show_transparent = False
		return{'FINISHED'}

def menu_func_import(self, context):
	self.layout.operator(rdt_import.bl_idname, text="BIO HAZARD Rooms (.rdt)")

def menu_func_export(self, context):
	self.layout.operator(rdt_export.bl_idname, text="BIO HAZARD Rooms (.rdt)")

def register():
	bpy.utils.register_class(rdt_import)
	bpy.utils.register_class(rdt_export)
	bpy.utils.register_class(rdt_tools_rid_panel)
	bpy.utils.register_class(rdt_tools_sca_panel)
	bpy.utils.register_class(rdt_tools_button)
	bpy.types.INFO_MT_file_import.append(menu_func_import)
	bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
	bpy.utils.unregister_class(rdt_import)
	bpy.utils.unregister_class(rdt_export)
	bpy.utils.unregister_class(rdt_tools_rid_panel)
	bpy.utils.unregister_class(rdt_tools_sca_panel)
	bpy.utils.unregister_class(rdt_tools_button)
	bpy.types.INFO_MT_file_import.remove(menu_func_import)
	bpy.types.INFO_MT_file_import.remove(menu_func_export)

if __name__ == "__main__":
	register()
	bpy.ops.lib_bio.io_rdt_blender('INVOKE_DEFAULT')