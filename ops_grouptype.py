#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================
import bpy
from .globals import *

class POSE_OT_jueg_Jueg_GroupType_move(bpy.types.Operator):
	"""Move group type up or down in the list"""
	bl_idname = "pose.jueg_Jueg_GroupType_move"
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
		index	= armature.active_Jueg_GroupType
		
		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index
			
		if new_index < len(armature.Jueg_GroupTypelist) and new_index >= 0:
			armature.Jueg_GroupTypelist.move(index, new_index)
			armature.active_Jueg_GroupType = new_index
		
		return {'FINISHED'}

class POSE_OT_jueg_Jueg_GroupType_reload(bpy.types.Operator):
	"""Reload data after addon unregister"""
	bl_idname = "pose.jueg_extragroups_reload"
	bl_label = "Reload data after addon unregister"
	bl_options = {'REGISTER'}	

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object
		user_preferences = context.user_preferences
		addon_prefs = user_preferences.addons[__package__].preferences	
		scene_found = False	
		for scene in bpy.data.scenes:
			if len(scene.extragroups_save) != 0:
				scene_found = True
				addon_prefs.scene_name = scene.name
				save_collection(bpy.data.scenes[addon_prefs.scene_name].extragroups_save, addon_prefs.extragroups_ops)
				break
		return {'FINISHED'}

class POSE_OT_jueg_Jueg_GroupType_add(bpy.types.Operator):
	"""Add a new group type"""
	bl_idname = "pose.jueg_Jueg_GroupType_add"
	bl_label = "Add Group Type"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')
				
	def execute(self, context):
		armature = context.object
		user_preferences = context.user_preferences
		addon_prefs = user_preferences.addons[__package__].preferences

		Jueg_GroupType = armature.Jueg_GroupTypelist.add()
		Jueg_GroupType.name = "Jueg_GroupType.%d" % len(armature.Jueg_GroupTypelist)
		armature.active_Jueg_GroupType = len(armature.Jueg_GroupTypelist) - 1

		if len(armature.Jueg_GroupTypelist) == 1 and len(addon_prefs.extragroups_ops) == 0: #in case of first initialisation
			scene_found = False
			for scene in bpy.data.scenes:
				if len(scene.extragroups_save) != 0:
					scene_found = True
					addon_prefs.scene_name = scene.name
					save_collection(bpy.data.scenes[addon_prefs.scene_name].extragroups_save, addon_prefs.extragroups_ops)
					copy(armature, armature.active_Jueg_GroupType)
					break
			if scene_found == False:
				init(armature)
		else:
			copy(armature, armature.active_Jueg_GroupType)
		
		return {'FINISHED'}
	
class POSE_OT_jueg_Jueg_GroupType_remove(bpy.types.Operator):
	"""Remove the current group type"""
	bl_idname = "pose.jueg_Jueg_GroupType_remove"
	bl_label = "Remove Group Type"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')
				
	def execute(self, context):
		armature = context.object	 
		
		armature.Jueg_GroupTypelist.remove(armature.active_Jueg_GroupType)
		len_ = len(armature.Jueg_GroupTypelist)
		if (armature.active_Jueg_GroupType > (len_ - 1) and len_ > 0):
			armature.active_Jueg_GroupType = len(armature.Jueg_GroupTypelist) - 1
		return {'FINISHED'}   

def copy(armature,index_Jueg_GroupType):
	user_preferences = bpy.context.user_preferences
	addon_prefs = user_preferences.addons[__package__].preferences	
	for ops in addon_prefs.extragroups_ops:
		new = armature.Jueg_GroupTypelist[index_Jueg_GroupType].ops_display.add()
		new.id = ops.id
		new.display = False

def init(armature):
	user_preferences = bpy.context.user_preferences
	addon_prefs = user_preferences.addons[__package__].preferences	
	ops = addon_prefs.extragroups_ops.add()  
	ops.name = "Select Only"
	ops.id = "bf258537303e41529b5adb4e3af6ed43"
	ops.ops_type = 'EXE'
	ops.ops_exe   = "pose.jueg_selectonly"
	ops.icon_on  = "HAND"
	ops.ok_for_current_sel = False
	ops.display = False
	ops.user_defined = False
	ops = addon_prefs.extragroups_ops.add() 
	ops.name = "Add to selection"
	ops.id = "fbd9a8fc639a4074bbd56f7be35e4690"
	ops.ops_type = 'EXE'
	ops.ops_exe   = "pose.jueg_addtoselection"
	ops.icon_on  = "ZOOMIN"
	ops.ok_for_current_sel = False
	ops.display = False
	ops.user_defined = False
	ops = addon_prefs.extragroups_ops.add()  
	ops.name = "Mute"
	ops.id = "f31027b2b65d4a90b610281ea09f08fb"
	ops.ops_type = 'BOOL'
	ops.ops_exe   = "pose.jueg_bonemute"
	ops.icon_on  = "MUTE_IPO_OFF"
	ops.icon_off  = "MUTE_IPO_ON"
	ops.ok_for_current_sel = True
	ops.display = False
	ops.user_defined = False
	ops = addon_prefs.extragroups_ops.add()   
	ops.name = "Toggle Visibility"
	ops.id = "b9eac1a0a2fd4dcd94140d05a6a3af86"
	ops.ops_type = 'BOOL'
	ops.ops_exe   = "pose.jueg_change_visibility"
	ops.icon_on  = "VISIBLE_IPO_ON"
	ops.icon_off  = "VISIBLE_IPO_OFF"
	ops.ok_for_current_sel = False
	ops.display = False
	ops.user_defined = False
	ops = addon_prefs.extragroups_ops.add()   
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
	armature.Jueg_GroupTypelist[0].active_ops = len(addon_prefs.extragroups_ops) - 1
	
def register():
	bpy.utils.register_class(POSE_OT_jueg_Jueg_GroupType_add)
	bpy.utils.register_class(POSE_OT_jueg_Jueg_GroupType_remove) 
	bpy.utils.register_class(POSE_OT_jueg_Jueg_GroupType_move)
	bpy.utils.register_class(POSE_OT_jueg_Jueg_GroupType_reload)
		
def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_Jueg_GroupType_add)
	bpy.utils.unregister_class(POSE_OT_jueg_Jueg_GroupType_remove) 
	bpy.utils.unregister_class(POSE_OT_jueg_Jueg_GroupType_move) 
	bpy.utils.unregister_class(POSE_OT_jueg_Jueg_GroupType_reload)
