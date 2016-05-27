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
		if ops.id not in [display.id for display in armature.jueg_grouptypelist[index_grouptype].ops_display]:
			new = armature.jueg_grouptypelist[index_grouptype].ops_display.add()
			new.id = ops.id
			new.display = False
		
def check_if_current_selection_exists():
	for group in bpy.context.object.jueg_grouptypelist[bpy.context.object.jueg_active_grouptype].group_ids:
		if group.current_selection == True:
			return True
	return False
	
def lib_proxy_armature():
	if bpy.context.active_object != None and bpy.context.active_object.data.library == None:
		return False, ""
	else:
		return True, bpy.context.active_object.data.library.filepath
		
def check_new_default_ops_in_new_addon_version():
	for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
		if len(obj.jueg_extragroups_ops) > 0:
			for def_ops in get_default_ops_id().keys():
				if def_ops not in [ops.id for ops in obj.jueg_extragroups_ops if ops.user_defined == False]:
					return True
				
			return False
	
def get_default_ops_id():

	dict_ = {}
	dict_['bf258537303e41529b5adb4e3af6ed43'] = {}
	dict_['bf258537303e41529b5adb4e3af6ed43']['name'] = "Select Only"
	dict_['bf258537303e41529b5adb4e3af6ed43']['ops_type'] = 'EXE'
	dict_['bf258537303e41529b5adb4e3af6ed43']['ops_exe'] = "pose.jueg_selectonly"
	dict_['bf258537303e41529b5adb4e3af6ed43']['icon_on'] = "HAND"
	dict_['bf258537303e41529b5adb4e3af6ed43']['icon_off'] = ""
	dict_['bf258537303e41529b5adb4e3af6ed43']['ok_for_current_sel'] = False
	dict_['bf258537303e41529b5adb4e3af6ed43']['display'] = False
	dict_['bf258537303e41529b5adb4e3af6ed43']['user_defined'] = False
	
	dict_['fbd9a8fc639a4074bbd56f7be35e4690'] = {}
	dict_['fbd9a8fc639a4074bbd56f7be35e4690']['name'] = "Add to selection"
	dict_['fbd9a8fc639a4074bbd56f7be35e4690']['ops_type'] = 'EXE'
	dict_['fbd9a8fc639a4074bbd56f7be35e4690']['ops_exe'] = "pose.jueg_selectonly"
	dict_['fbd9a8fc639a4074bbd56f7be35e4690']['icon_on'] = "HAND"
	dict_['fbd9a8fc639a4074bbd56f7be35e4690']['icon_off'] = ""
	dict_['fbd9a8fc639a4074bbd56f7be35e4690']['ok_for_current_sel'] = False
	dict_['fbd9a8fc639a4074bbd56f7be35e4690']['display'] = False
	dict_['fbd9a8fc639a4074bbd56f7be35e4690']['user_defined'] = False
	
	dict_['f31027b2b65d4a90b610281ea09f08fb'] = {}
	dict_['f31027b2b65d4a90b610281ea09f08fb']['name'] = "Mute"
	dict_['f31027b2b65d4a90b610281ea09f08fb']['ops_type'] = 'BOOL'
	dict_['f31027b2b65d4a90b610281ea09f08fb']['ops_exe'] = "pose.jueg_bonemute"
	dict_['f31027b2b65d4a90b610281ea09f08fb']['icon_on'] = "MUTE_IPO_OFF"
	dict_['f31027b2b65d4a90b610281ea09f08fb']['icon_off'] = "MUTE_IPO_ON"
	dict_['f31027b2b65d4a90b610281ea09f08fb']['ok_for_current_sel'] = True
	dict_['f31027b2b65d4a90b610281ea09f08fb']['display'] = False
	dict_['f31027b2b65d4a90b610281ea09f08fb']['user_defined'] = False
	
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86'] = {}
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['name'] = "Toggle Visibility"
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['ops_type'] = 'BOOL'
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['ops_exe'] = "pose.jueg_change_visibility"
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['icon_on'] = "VISIBLE_IPO_ON"
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['icon_off'] = "VISIBLE_IPO_OFF"
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['ok_for_current_sel'] = False
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['display'] = False
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['user_defined'] = False
	
	dict_['9d5257bf3d6245afacabb452bf7a455e'] = {}
	dict_['9d5257bf3d6245afacabb452bf7a455e']['name'] = "Restrict/Allow Selection"
	dict_['9d5257bf3d6245afacabb452bf7a455e']['ops_type'] = 'BOOL'
	dict_['9d5257bf3d6245afacabb452bf7a455e']['ops_exe'] = "pose.jueg_restrict_select"
	dict_['9d5257bf3d6245afacabb452bf7a455e']['icon_on'] = "RESTRICT_SELECT_OFF"
	dict_['9d5257bf3d6245afacabb452bf7a455e']['icon_off'] = "RESTRICT_SELECT_ON"
	dict_['9d5257bf3d6245afacabb452bf7a455e']['ok_for_current_sel'] = True
	dict_['9d5257bf3d6245afacabb452bf7a455e']['display'] = False
	dict_['9d5257bf3d6245afacabb452bf7a455e']['user_defined'] = False
	
	dict_['9d5257bf3d6245afacabb452bf7a455e'] = {}
	dict_['9d5257bf3d6245afacabb452bf7a455e']['name'] = "Magic Select"
	dict_['9d5257bf3d6245afacabb452bf7a455e']['ops_type'] = 'EXE'
	dict_['9d5257bf3d6245afacabb452bf7a455e']['ops_exe'] = "pose.jueg_magic_select"
	dict_['9d5257bf3d6245afacabb452bf7a455e']['icon_on'] = "HAND"
	dict_['9d5257bf3d6245afacabb452bf7a455e']['icon_off'] = ""
	dict_['9d5257bf3d6245afacabb452bf7a455e']['ok_for_current_sel'] = False
	dict_['9d5257bf3d6245afacabb452bf7a455e']['display'] = False
	dict_['9d5257bf3d6245afacabb452bf7a455e']['user_defined'] = False
	
	return dict_
		
def init_default_ops(armature):

	#first check if some objects have already data
	for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
		if obj.jueg_extragroups_ops and len(obj.jueg_extragroups_ops) > 0:
			for ops_src in obj.jueg_extragroups_ops:
				ops = armature.jueg_extragroups_ops.add()
				ops.id   = ops_src.id 
				ops.name = ops_src.name
				ops.ops_exe = ops_src.ops_exe
				ops.ops_type = ops_src.ops_type
				ops.icon_on	= ops_src.icon_on
				ops.icon_off   = ops_src.icon_off
				ops.ok_for_current_sel = ops_src.ok_for_current_sel
				ops.user_defined = ops_src.user_defined
			copy_data_ops(armature, 0)
			armature.jueg_grouptypelist[0].active_ops = len(armature.jueg_extragroups_ops) - 1
			return True
		
	#if no data found, init with default ops
	for id in get_default_ops_id().keys():
		ops = armature.jueg_extragroups_ops.add()
		ops.name     = get_default_ops_id()[id]["name"]
		ops.id       = id
		ops.ops_type = get_default_ops_id()[id]["ops_type"]
		ops.ops_exe  = get_default_ops_id()[id]["ops_exe"]
		ops.icon_on = get_default_ops_id()[id]["icon_on"]
		ops.icon_off = get_default_ops_id()[id]["icon_off"]
		ops.ok_for_current_sel = get_default_ops_id()[id]["ok_for_current_sel"]
		ops.display = get_default_ops_id()[id]["display"]
		ops.user_defined = get_default_ops_id()[id]["user_defined"]

	copy_data_ops(armature,0)
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