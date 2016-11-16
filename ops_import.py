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

def register():
	bpy.utils.register_class(POSE_OT_jueg_import_from_bone_groups)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_import_from_bone_groups)
