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
from .utils import *

class POSE_OT_jueg_import_from_bone_groups(bpy.types.Operator):
	"""Import from Bone Groups"""
	bl_idname = "jueg.import_from_bone_groups"
	bl_label  = "Import from Bone Groups"

	@classmethod
	def poll(self, context):
		return True

	def execute(self, context):

		creation = {}
		armature = context.object


		# retrieve all bone group / bones
		for bone in armature.pose.bones:
			if bone.bone_group:
				if not bone.bone_group.name in creation.keys():
					creation[bone.bone_group.name] = []
				creation[bone.bone_group.name].append(bone.name)

		# creation
		if len(armature.jueg_grouptypelist) == 0:
			grouptype = armature.jueg_grouptypelist.add()
			grouptype.name = "GroupType.%d" % len(armature.jueg_grouptypelist)
			armature.jueg_active_grouptype = len(armature.jueg_grouptypelist) - 1
			init_default_ops(armature)

		grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids

		for gr in creation.keys():
			if not gr in grouptype.keys():
				bonegroup = grouptype.add()
				bonegroup.name = gr
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_bonegroup = len(grouptype) - 1
			else:
				bonegroup = grouptype[gr]

			for bone in creation[gr]:
				if not bone in bonegroup.bone_ids.keys():
				    bone_id = bonegroup.bone_ids.add()
				    bone_id.name = bone

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

		return {'FINISHED'}

class POSE_OT_jueg_import_from_selection_sets(bpy.types.Operator):
	"""Import from Selection Sets"""
	bl_idname = "jueg.import_from_selection_sets"
	bl_label  = "Import from Selection Sets"

	@classmethod
	def poll(self, context):
		return True

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

		# creation
		if len(armature.jueg_grouptypelist) == 0:
			grouptype = armature.jueg_grouptypelist.add()
			grouptype.name = "GroupType.%d" % len(armature.jueg_grouptypelist)
			armature.jueg_active_grouptype = len(armature.jueg_grouptypelist) - 1
			init_default_ops(armature)

		grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids

		for gr in creation.keys():
			if not gr in grouptype.keys():
				bonegroup = grouptype.add()
				bonegroup.name = gr
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_bonegroup = len(grouptype) - 1
			else:
				bonegroup = grouptype[gr]

			for bone in creation[gr]:
				if not bone in bonegroup.bone_ids.keys():
				    bone_id = bonegroup.bone_ids.add()
				    bone_id.name = bone

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

		return {'FINISHED'}

class POSE_OT_jueg_import_from_keying_sets(bpy.types.Operator):
	"""Import from Keying Sets"""
	bl_idname = "jueg.import_from_keying_sets"
	bl_label  = "Import from Keying Sets"

	@classmethod
	def poll(self, context):
		return True

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

		# creation
		if len(armature.jueg_grouptypelist) == 0:
			grouptype = armature.jueg_grouptypelist.add()
			grouptype.name = "GroupType.%d" % len(armature.jueg_grouptypelist)
			armature.jueg_active_grouptype = len(armature.jueg_grouptypelist) - 1
			init_default_ops(armature)

		grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids

		for gr in creation.keys():
			if not gr in grouptype.keys():
				bonegroup = grouptype.add()
				bonegroup.name = gr
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_bonegroup = len(grouptype) - 1
			else:
				bonegroup = grouptype[gr]

			for bone in creation[gr]:
				if not bone in bonegroup.bone_ids.keys():
				    bone_id = bonegroup.bone_ids.add()
				    bone_id.name = bone

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

		return {'FINISHED'}


def register():
	bpy.utils.register_class(POSE_OT_jueg_import_from_bone_groups)
	bpy.utils.register_class(POSE_OT_jueg_import_from_selection_sets)
	bpy.utils.register_class(POSE_OT_jueg_import_from_keying_sets)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_import_from_bone_groups)
	bpy.utils.unregister_class(POSE_OT_jueg_import_from_selection_sets)
	bpy.utils.unregister_class(POSE_OT_jueg_import_from_keying_sets)
