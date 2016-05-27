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
from bpy.app.handlers import persistent

class Jueg_BoneEntry(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Bone Name")
	
class Jueg_OnOffEntry(bpy.types.PropertyGroup):
	id      = bpy.props.StringProperty(name="Id of Ops")
	on_off  = bpy.props.BoolProperty(name="On_Off")

class Jueg_BoneGroup(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Group Name")
	bone_ids = bpy.props.CollectionProperty(type=Jueg_BoneEntry)
	on_off = bpy.props.CollectionProperty(type=Jueg_OnOffEntry)
	current_selection = bpy.props.BoolProperty()
	
class Jueg_OpsDisplay(bpy.types.PropertyGroup):
	id   = bpy.props.StringProperty(name="Unique id")
	display = bpy.props.BoolProperty()

class Jueg_GroupType(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Group Type Name")
	group_ids = bpy.props.CollectionProperty(type=Jueg_BoneGroup)
	active_bonegroup = bpy.props.IntProperty()
	ops_display = bpy.props.CollectionProperty(type=Jueg_OpsDisplay)
	active_ops = bpy.props.IntProperty()

jueg_ops_type_items = [
	("BOOL", "On/Off", "", 1),
	("EXE", "Exec", "", 2),
	]

class Jueg_OpsItem(bpy.types.PropertyGroup):
	id   = bpy.props.StringProperty(name="Unique id")
	name = bpy.props.StringProperty(name="Ops Name")
	ops_exe = bpy.props.StringProperty(name="Ops Exe")
	ops_type = bpy.props.EnumProperty(items=jueg_ops_type_items)
	icon_on	= bpy.props.StringProperty(name="Icon On")
	icon_off   = bpy.props.StringProperty(name="Icon Off")
	ok_for_current_sel = bpy.props.BoolProperty()
	user_defined = bpy.props.BoolProperty()
	
#shortcut to prefs
def addonpref():
	user_preferences = bpy.context.user_preferences
	return user_preferences.addons[__package__].preferences
	
def copy_data_ops(armature,index_grouptype):
	for ops in armature.jueg_extragroups_ops:
		new = armature.jueg_grouptypelist[index_grouptype].ops_display.add()
		new.id = ops.id
		new.display = False
		
def check_if_current_selection_exists():
	for group in bpy.context.object.jueg_grouptypelist[bpy.context.object.jueg_active_grouptype].group_ids:
		if group.current_selection == True:
			return True
	return False
	
def lib_proxy_armature():
	if bpy.context.object.data.library == None:
		return False, ""
	else:
		return True, bpy.context.object.data.library.filepath
		
def init_default_ops(armature):
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
	copy_data_ops(armature, 0)
	armature.jueg_grouptypelist[0].active_ops = len(armature.jueg_extragroups_ops) - 1

def register():
	bpy.utils.register_class(Jueg_OnOffEntry)
	bpy.utils.register_class(Jueg_BoneEntry)
	bpy.utils.register_class(Jueg_BoneGroup)
	bpy.utils.register_class(Jueg_OpsDisplay)
	bpy.utils.register_class(Jueg_GroupType)
	bpy.utils.register_class(Jueg_OpsItem)
	
def unregister():
	bpy.utils.unregister_class(Jueg_OnOffEntry)
	bpy.utils.unregister_class(Jueg_BoneEntry)
	bpy.utils.unregister_class(Jueg_BoneGroup)
	bpy.utils.unregister_class(Jueg_OpsDisplay)
	bpy.utils.unregister_class(Jueg_GroupType)
	bpy.utils.unregister_class(Jueg_OpsItem)