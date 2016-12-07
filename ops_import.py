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

def import_creation(multi_type_mode, creation, label):
	armature = bpy.context.object

	# creation
	if len(armature.jueg_grouptypelist) == 0:
		grouptype = armature.jueg_grouptypelist.add()
		grouptype.name = label
		armature.jueg_active_grouptype = len(armature.jueg_grouptypelist) - 1
		init_default_ops(armature)
		bonegroup = grouptype.group_ids.add()
		bonegroup.current_selection = True
		bonegroup.name = "Current Selection"
		#add on / off for each ops
		on_off   = bonegroup.on_off
		ops_list = armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display
		for ops in ops_list:
			new_ = on_off.add()
			new_.id = ops.id
			new_.on_off = True

		#add solo for each ops
		solo   = bonegroup.solo
		ops_list = armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display
		for ops in ops_list:
			new_ = solo.add()
			new_.id = ops.id
			new_.on_off = False

	if multi_type_mode == False:
		grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype]
	else:
		if label not in [grouptype_.name for grouptype_ in armature.jueg_grouptypelist]:
			grouptype = armature.jueg_grouptypelist.add()
			grouptype.name = label
			armature.jueg_active_grouptype = len(armature.jueg_grouptypelist) - 1
			copy_data_ops(armature, armature.jueg_active_grouptype)
			bonegroup = grouptype.group_ids.add()
			bonegroup.current_selection = True
			bonegroup.name = "Current Selection"
			#add on / off for each ops
			on_off   = bonegroup.on_off
			ops_list = armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display
			for ops in ops_list:
				new_ = on_off.add()
				new_.id = ops.id
				new_.on_off = True

			#add solo for each ops
			solo   = bonegroup.solo
			ops_list = armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display
			for ops in ops_list:
				new_ = solo.add()
				new_.id = ops.id
				new_.on_off = False
			grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype]
		else:
			grouptype = [grouptype_ for grouptype_ in armature.jueg_grouptypelist if grouptype_.name == label][0]

	for gr in creation.keys():
		if not gr in grouptype.group_ids.keys():
			bonegroup = grouptype.group_ids.add()
			bonegroup.name = gr
			grouptype.active_bonegroup = len(grouptype.group_ids) - 1
		else:
			bonegroup = grouptype.group_ids[gr]

		for bone in creation[gr]:
			if not bone in bonegroup.bone_ids.keys() and bone in armature.data.bones:
				bone_id = bonegroup.bone_ids.add()
				bone_id.name = bone

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


		# retrieve all bone group / bones
		for bone in armature.pose.bones:
			if bone.bone_group:
				if not bone.bone_group.name in creation.keys():
					creation[bone.bone_group.name] = []
				creation[bone.bone_group.name].append(bone.name)

		import_creation(False, creation, "Bone Groups")

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

		for grouptype in creations["Extragroups"]:
			creation = {}
			for group_ in grouptype["groups"]:
				creation[group_["name"]] = group_["bones"]
			import_creation(True, creation, grouptype["name"])

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

		# retrieve all bone group / bones
		for set_ in armature.selection_sets:
			creation[set_.name] = []
			for bone in set_.bone_ids:
				creation[set_.name].append(bone.name)

		import_creation(False, creation, "Selection Sets")

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

		# retrieve all bone group / bones
		for set_ in bpy.context.scene.keying_sets:
			creation[set_.bl_label] = []
			for path in set_.paths:
				if path.data_path.startswith("pose.bones"):
					tmp = path.data_path.split("[", maxsplit=1)[1].split("]", maxsplit=1)
					bone_name = tmp[0][1:-1]
					creation[set_.bl_label].append(bone_name)

		import_creation(False, creation, "Keying Sets")

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

		import_creation(False, {}, "GroupType.1")

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
