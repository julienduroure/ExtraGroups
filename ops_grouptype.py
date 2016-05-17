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
from .globals import *

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
			init(armature)
		else:
			copy(armature, armature.jueg_active_grouptype)
	
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
		return {'FINISHED'}   

def copy(armature,index_grouptype):
	for ops in armature.jueg_extragroups_ops:
		new = armature.jueg_grouptypelist[index_grouptype].ops_display.add()
		new.id = ops.id
		new.display = False
		
def init(armature):
	ops = armature.jueg_extragroups_ops.add()  
	ops.name = "Select Only"
	ops.id = "bf258537303e41529b5adb4e3af6ed43"
	ops.ops_type = 'EXE'
	ops.ops_exe   = "pose.jueg_selectonly"
	ops.icon_on  = "HAND"
	ops.ok_for_current_sel = False
	ops.display = False
	ops.user_defined = False
	ops = armature.jueg_extragroups_ops.add() 
	ops.name = "Add to selection"
	ops.id = "fbd9a8fc639a4074bbd56f7be35e4690"
	ops.ops_type = 'EXE'
	ops.ops_exe   = "pose.jueg_addtoselection"
	ops.icon_on  = "ZOOMIN"
	ops.ok_for_current_sel = False
	ops.display = False
	ops.user_defined = False
	ops = armature.jueg_extragroups_ops.add()  
	ops.name = "Mute"
	ops.id = "f31027b2b65d4a90b610281ea09f08fb"
	ops.ops_type = 'BOOL'
	ops.ops_exe   = "pose.jueg_bonemute"
	ops.icon_on  = "MUTE_IPO_OFF"
	ops.icon_off  = "MUTE_IPO_ON"
	ops.ok_for_current_sel = True
	ops.display = False
	ops.user_defined = False
	ops = armature.jueg_extragroups_ops.add()   
	ops.name = "Toggle Visibility"
	ops.id = "b9eac1a0a2fd4dcd94140d05a6a3af86"
	ops.ops_type = 'BOOL'
	ops.ops_exe   = "pose.jueg_change_visibility"
	ops.icon_on  = "VISIBLE_IPO_ON"
	ops.icon_off  = "VISIBLE_IPO_OFF"
	ops.ok_for_current_sel = False
	ops.display = False
	ops.user_defined = False
	ops = armature.jueg_extragroups_ops.add()   
	ops.name = "Restrict/Allow Selection"
	ops.id = "9d5257bf3d6245afacabb452bf7a455e"
	ops.ops_type = 'BOOL'
	ops.ops_exe   = "pose.jueg_restrict_select"
	ops.icon_on  = "RESTRICT_SELECT_OFF"
	ops.icon_off  = "RESTRICT_SELECT_ON"
	ops.ok_for_current_sel = True
	ops.display = False
	ops.user_defined = False
	copy(armature, 0)
	armature.jueg_grouptypelist[0].active_ops = len(armature.jueg_extragroups_ops) - 1
	
def register():
	bpy.utils.register_class(POSE_OT_jueg_grouptype_add)
	bpy.utils.register_class(POSE_OT_jueg_grouptype_remove) 
	bpy.utils.register_class(POSE_OT_jueg_grouptype_move)
		
def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_grouptype_add)
	bpy.utils.unregister_class(POSE_OT_jueg_grouptype_remove) 
	bpy.utils.unregister_class(POSE_OT_jueg_grouptype_move) 
