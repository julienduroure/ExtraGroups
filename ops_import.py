##########################################################################################
#	GPL LICENSE:
#-------------------------
# This file is part of ExtraGroups.
#
#    ExtraGroups is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ExtraGroups is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ExtraGroups.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################################
#
#	Copyright 2016 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################
import bpy
import bpy_extras
import json
from .utils import *
import mathutils

def import_creation(multi_type_mode, grptype_):
	armature = bpy.context.object

	# creation
	if len(armature.jueg_grouptypelist) == 0:
		grouptype = armature.jueg_grouptypelist.add()
		grouptype.name = grptype_["name"]
		armature.jueg_active_grouptype = len(armature.jueg_grouptypelist) - 1
		init_default_ops(armature)

	if multi_type_mode == False:
		grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype]
	else:
		if grptype_["name"] not in [grouptype_.name for grouptype_ in armature.jueg_grouptypelist]:
			grouptype = armature.jueg_grouptypelist.add()
			grouptype.name = grptype_["name"]
			armature.jueg_active_grouptype = len(armature.jueg_grouptypelist) - 1
			copy_data_ops(armature, armature.jueg_active_grouptype)

			grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype]
		else:
			grouptype = [grouptype_ for grouptype_ in armature.jueg_grouptypelist if grouptype_.name == grptype_["name"]][0]

	for gr in grptype_["groups"]:
		if not gr["name"] in grouptype.group_ids.keys():
			bonegroup = grouptype.group_ids.add()
			bonegroup.name = gr["name"]
			grouptype.active_bonegroup = len(grouptype.group_ids) - 1
			if gr["current_selection"] == True:
				bonegroup.current_selection = True
		else:
			bonegroup = grouptype.group_ids[gr["name"]]

		if gr["current_selection"] == False:
			for bone in gr["bones"]:
				if not bone in bonegroup.bone_ids.keys() and bone in armature.data.bones:
					bone_id = bonegroup.bone_ids.add()
					bone_id.name = bone

			bonegroup.keying      		= gr["keying"]
			bonegroup.active_bone 		= gr["active_bone"]
			bonegroup.orientation 		= gr["orientation"]
			bonegroup.manipulator[0] 	= 'TRANSLATE' in gr["manipulator"].split('/')
			bonegroup.manipulator[1] 	= 'ROTATE'    in gr["manipulator"].split('/')
			bonegroup.manipulator[2] 	= 'SCALE'     in gr["manipulator"].split('/')

		bonegroup.color				= mathutils.Color((float(gr["color"].split('/')[0]),float(gr["color"].split('/')[1]),float(gr["color"].split('/')[2])))

		#add on / off for each ops
		on_off   = bonegroup.on_off
		ops_list = grouptype.ops_display
		for ops in ops_list:
			new_ = on_off.add()
			new_.id = ops.id
			new_.on_off = True

		#add solo for each ops
		solo   = bonegroup.solo
		ops_list = grouptype.ops_display
		for ops in ops_list:
			new_ = solo.add()
			new_.id = ops.id
			new_.on_off = False

	# change order of ops, and what is displayed or not
	current_idx = -1
	for ops in grptype_["ops"]:
		current_idx = current_idx + 1
		# retrieve current index of this ops
		old_idx  = -1
		find_idx = -1
		display = False
		for ops_ in grouptype.ops_display:
			find_idx = find_idx + 1
			if ops_.id == ops["ops"]:
				old_idx = find_idx
				display = ops["active"]
				label   = ops["label"]
				break
		if old_idx != -1:
			grouptype.ops_display[old_idx].display = display
			grouptype.ops_display.move(old_idx, current_idx)
			[e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == ops["ops"]][0].name = label


class POSE_OT_jueg_import_from_bone_groups(bpy.types.Operator):
	"""Import from Bone Groups"""
	bl_idname = "jueg.import_from_bone_groups"
	bl_label  = "Import from Bone Groups"

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):

		creation = {}
		armature = context.object


		creation["name"] = "Bone Groups"
		creation["ops"] = []
		creation["groups"] = []
		# retrieve all bone group / bones
		for bone in armature.pose.bones:
			if bone.bone_group:
				if not bone.bone_group.name in [gr["name"] for gr in creation["groups"]]:
					tmp = {}
					tmp["name"] = bone.bone_group.name
					tmp["current_selection"] = False
					tmp["keying"] = ""
					tmp["color"] = "0.0/0.0/0.0"
					tmp["orientation"] = "GLOBAL"
					tmp["manipulator"] = "TRANSLATE"
					tmp["active_bone"] = bone.name
					tmp["bones"] = []
					creation["groups"].append(tmp)
				[gr["bones"] for gr in creation["groups"] if gr["name"] == bone.bone_group.name][0].append(bone.name)

		import_creation(False, creation)

		return {'FINISHED'}

class POSE_OT_jueg_import_from_file(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	"""Import from File"""
	bl_idname = "jueg.import_from_file"
	bl_label  = "Import from File"

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):

		creation = {}
		armature = context.object

		filename_ext = ".txt"

		filter_glob = bpy.props.StringProperty(default="*.txt", options={'HIDDEN'}, maxlen=255,)

		f = open(self.filepath, 'r', encoding='utf-8')
		data = f.read()
		creations = json.loads(data)
		f.close()

		for grouptype in creations["GroupTypes"]:
			import_creation(True, grouptype)

		return {'FINISHED'}

class POSE_OT_jueg_import_from_selection_sets(bpy.types.Operator):
	"""Import from Selection Sets"""
	bl_idname = "jueg.import_from_selection_sets"
	bl_label  = "Import from Selection Sets"

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):

		creation = {}
		armature = context.object

		if not armature.get("selection_sets"):
			return {"CANCELLED"}

		creation["name"] = "Selection Sets"
		creation["ops"] = []
		creation["groups"] = []
		# retrieve all bone group / bones
		for set_ in armature.selection_sets:
			tmp = {}
			tmp["name"] = set_.name
			tmp["current_selection"] = False
			tmp["keying"] = ""
			tmp["color"] = "0.0/0.0/0.0"
			tmp["orientation"] = "GLOBAL"
			tmp["manipulator"] = "TRANSLATE"
			tmp["bones"] = []

			for bone in set_.bone_ids:
				tmp["bones"].append(bone.name)
				tmp["active_bone"] = bone.name
			creation["groups"].append(tmp)

		import_creation(False, creation)

		return {'FINISHED'}

class POSE_OT_jueg_import_from_keying_sets(bpy.types.Operator):
	"""Import from Keying Sets"""
	bl_idname = "jueg.import_from_keying_sets"
	bl_label  = "Import from Keying Sets"

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):

		creation = {}
		armature = context.object

		creation["name"] = "Keying Sets"
		creation["ops"] = []
		creation["groups"] = []
		# retrieve all bone group / bones
		for set_ in bpy.context.scene.keying_sets:
			tmp = {}
			tmp["name"] = set_.bl_label
			tmp["current_selection"] = False
			tmp["keying"] = ""
			tmp["color"] = "0.0/0.0/0.0"
			tmp["orientation"] = "GLOBAL"
			tmp["manipulator"] = "TRANSLATE"
			tmp["bones"] = []
			for path in set_.paths:
				if path.data_path.startswith("pose.bones"):
					tmp_ = path.data_path.split("[", maxsplit=1)[1].split("]", maxsplit=1)
					bone_name = tmp_[0][1:-1]
					print(bone_name)
					tmp["bones"].append(bone_name)
					tmp["active_bone"] = bone_name
			creation["groups"].append(tmp)

		import_creation(False, creation)

		return {'FINISHED'}

class POSE_OT_jueg_init_from_scratch(bpy.types.Operator):
	"""Init from Scratch"""
	bl_idname = "jueg.init_from_scratch"
	bl_label  = "Init from Scratch"

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):

		import_creation(False, {}, "GroupType.1", {})

		return {'FINISHED'}


def register():
	bpy.utils.register_class(POSE_OT_jueg_import_from_bone_groups)
	bpy.utils.register_class(POSE_OT_jueg_import_from_selection_sets)
	bpy.utils.register_class(POSE_OT_jueg_import_from_keying_sets)
	bpy.utils.register_class(POSE_OT_jueg_init_from_scratch)
	bpy.utils.register_class(POSE_OT_jueg_import_from_file)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_import_from_bone_groups)
	bpy.utils.unregister_class(POSE_OT_jueg_import_from_selection_sets)
	bpy.utils.unregister_class(POSE_OT_jueg_import_from_keying_sets)
	bpy.utils.unregister_class(POSE_OT_jueg_init_from_scratch)
	bpy.utils.unregister_class(POSE_OT_jueg_import_from_file)
