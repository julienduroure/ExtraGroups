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
from .globs import *
from .utils import *

class POSE_OT_jueg_grouptype_move(bpy.types.Operator):
	"""Move group type up or down in the list"""
	bl_idname = "pose.jueg_grouptype_move"
	bl_label = "Move Group Type"
	bl_options = {'REGISTER'}

	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object
		index	= armature.jueg_active_grouptype

		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index

		if new_index < len(armature.jueg_grouptypelist) and new_index >= 0:
			armature.jueg_grouptypelist.move(index, new_index)
			armature.jueg_active_grouptype = new_index

		return {'FINISHED'}

class POSE_OT_jueg_grouptype_add(bpy.types.Operator):
	"""Add a new group type"""
	bl_idname = "pose.jueg_grouptype_add"
	bl_label = "Add Group Type"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object

		grouptype = armature.jueg_grouptypelist.add()
		grouptype.name = "GroupType.%d" % len(armature.jueg_grouptypelist)
		armature.jueg_active_grouptype = len(armature.jueg_grouptypelist) - 1

		if len(armature.jueg_grouptypelist) == 1 and len(armature.jueg_extragroups_ops) == 0: #in case of first initialisation
			init_default_ops(armature)
			bonegroup = grouptype.group_ids.add()
			bonegroup.current_selection = True
			bonegroup.name = "Current Selection"
		else:
			copy_data_ops(armature, armature.jueg_active_grouptype)

		return {'FINISHED'}

class POSE_OT_jueg_grouptype_remove(bpy.types.Operator):
	"""Remove the current group type"""
	bl_idname = "pose.jueg_grouptype_remove"
	bl_label = "Remove Group Type"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object

		armature.jueg_grouptypelist.remove(armature.jueg_active_grouptype)
		len_ = len(armature.jueg_grouptypelist)
		if (armature.jueg_active_grouptype > (len_ - 1) and len_ > 0):
			armature.jueg_active_grouptype = len(armature.jueg_grouptypelist) - 1

		if len_ == 0:
			# when delete last grouptype, need to delete ops
			for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
				obj.jueg_extragroups_ops.clear()
				obj.jueg_active_grouptype = -1

		return {'FINISHED'}

def register():
	bpy.utils.register_class(POSE_OT_jueg_grouptype_add)
	bpy.utils.register_class(POSE_OT_jueg_grouptype_remove)
	bpy.utils.register_class(POSE_OT_jueg_grouptype_move)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_grouptype_add)
	bpy.utils.unregister_class(POSE_OT_jueg_grouptype_remove)
	bpy.utils.unregister_class(POSE_OT_jueg_grouptype_move)
