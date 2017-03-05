#
# ExtraGroups is part of BleRiFa. http://BleRiFa.com
#
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
#	Copyright 2016-2017 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################
import bpy
from .globs import *
from .utils import *


class POSE_OT_jueg_bonegroup_assign(bpy.types.Operator):
	"""Add selected bones to current group"""
	bl_idname = "pose.jueg_bonegroup_assign"
	bl_label = "Assign Bones to Bone Group"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object
		pose = armature.pose

		for bone in pose.bones:
				if (bone.bone.select):
					if bone.name not in [b_.name for b_ in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_bonegroup].bone_ids ]:
						bone_id = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_bonegroup].bone_ids.add()
						bone_id.name = bone.name

		return {'FINISHED'}

class POSE_OT_jueg_bonegroup_bone_remove(bpy.types.Operator):
	"""Remove selected bones from current group"""
	bl_idname = "pose.jueg_bonegroup_bone_remove"
	bl_label = "Remove Bones from Bone Group"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object
		pose = armature.pose

		for bone in pose.bones:
				if (bone.bone.select):
					idx = 0
					for b_ in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_bonegroup].bone_ids:
						if bone.name == b_.name:
							armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_bonegroup].bone_ids.remove(idx)
							break
						idx = idx + 1
		return {'FINISHED'}



def register():
	bpy.utils.register_class(POSE_OT_jueg_bonegroup_assign)
	bpy.utils.register_class(POSE_OT_jueg_bonegroup_bone_remove)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_bonegroup_assign)
	bpy.utils.unregister_class(POSE_OT_jueg_bonegroup_bone_remove)
