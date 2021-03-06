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
from .utils import *

def clickable_ops_items(self, context):
	items = []
	armature = context.object

	for ops in armature.jueg_extragroups_ops:
		items.append((ops.id, ops.name, ""))

	return items

def clickable_mode_items(self, context):
	items = []
	armature = context.object
	ops = [ops for ops in armature.jueg_extragroups_ops if ops.id == armature.jueg_clickable_name_data.clickable_ops][0]

	for ev in ops.events:
		items.append((ev.mode, ev.label, ""))

	return items

class Jueg_BoneEntry(bpy.types.PropertyGroup):
	name: bpy.props.StringProperty(name="Bone Name", override={"LIBRARY_OVERRIDABLE"})

class Jueg_OnOffEntry(bpy.types.PropertyGroup):
	id      : bpy.props.StringProperty(name="Id of Ops", override={"LIBRARY_OVERRIDABLE"})
	on_off  : bpy.props.BoolProperty(name="On_Off", override={"LIBRARY_OVERRIDABLE"})

jueg_orientation_items = [
	("GLOBAL", "Global", "", 1),
	("LOCAL", "Local", "", 2),
	("NORMAL", "Normal", "", 3),
	("GIMBAL", "Gimbal", "", 4),
	("VIEW", "View", "", 5),
	]

#Dev note :
#Any new data needs update in
	# copy / copy mirror
	# Import from file
	# Export from file
	# reload linked data

class Jueg_BoneGroup(bpy.types.PropertyGroup):
	name              : bpy.props.StringProperty(name="Group Name", override={"LIBRARY_OVERRIDABLE"})
	bone_ids          : bpy.props.CollectionProperty(type=Jueg_BoneEntry, override={"LIBRARY_OVERRIDABLE", "USE_INSERTION"})
	on_off            : bpy.props.CollectionProperty(type=Jueg_OnOffEntry, override={"LIBRARY_OVERRIDABLE", "USE_INSERTION"})
	solo              : bpy.props.CollectionProperty(type=Jueg_OnOffEntry, override={"LIBRARY_OVERRIDABLE", "USE_INSERTION"})
	current_selection : bpy.props.BoolProperty(override={"LIBRARY_OVERRIDABLE"})
	color             : bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', default=[0.0,0.0,0.0], min=0.0, max=1.0, override={"LIBRARY_OVERRIDABLE"})
	keying            : bpy.props.StringProperty(name="Keying Set", override={"LIBRARY_OVERRIDABLE"})
	manipulator		  : bpy.props.BoolVectorProperty(name="Manipulator", default=(True, False, False), size=3, override={"LIBRARY_OVERRIDABLE"})
	orientation       : bpy.props.EnumProperty(items=jueg_orientation_items, name="Orientation", override={"LIBRARY_OVERRIDABLE"})
	active_bone       : bpy.props.StringProperty(name="Bone Name", override={"LIBRARY_OVERRIDABLE"})

class Jueg_OpsDisplay(bpy.types.PropertyGroup):
	id   : bpy.props.StringProperty(name="Unique id", override={"LIBRARY_OVERRIDABLE"})
	display : bpy.props.BoolProperty(override={"LIBRARY_OVERRIDABLE"})

class Jueg_GroupType(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name="Group Type Name", override={"LIBRARY_OVERRIDABLE"})
	group_ids : bpy.props.CollectionProperty(type=Jueg_BoneGroup, override={"LIBRARY_OVERRIDABLE", "USE_INSERTION"})
	active_bonegroup : bpy.props.IntProperty(override={"LIBRARY_OVERRIDABLE"})
	ops_display : bpy.props.CollectionProperty(type=Jueg_OpsDisplay, override={"LIBRARY_OVERRIDABLE", "USE_INSERTION"})
	active_ops : bpy.props.IntProperty(override={"LIBRARY_OVERRIDABLE"})

class Jueg_menu_temp_data(bpy.types.PropertyGroup):
	event  : bpy.props.StringProperty(name="Event", override={"LIBRARY_OVERRIDABLE"})
	index  : bpy.props.IntProperty(name="Index", override={"LIBRARY_OVERRIDABLE"})
	ops_id : bpy.props.StringProperty(name="Ops ID", override={"LIBRARY_OVERRIDABLE"})
	solo   : bpy.props.BoolProperty(name="Solo", override={"LIBRARY_OVERRIDABLE"})
	mirror : bpy.props.BoolProperty(name="Mirror", override={"LIBRARY_OVERRIDABLE"})

jueg_ops_type_items = [
	("BOOL", "On/Off", "", 1),
	("EXE", "Exec", "", 2),
	]

jueg_event_modif = [
	("NONE", "None", "", 1),
	("SHIFT", "Shift", "", 2),
	("ALT", "Alt", "", 3),
	("CTRL", "Ctrl", "", 4),
	("SHIFT_ALT", "Shift+Alt", "", 5),
	("SHIFT_CTRL", "Shift+Ctrl", "", 6),
	("CTRL_ALT", "Ctrl+Alt", "", 7),
	("CTRL_SHIFT_ALT", "Ctrl+Shift+Alt", "", 8),
]

jueg_ops_context = [
	("EXEC_DEFAULT", "Exec Default", "", 1),
	("INVOKE_DEFAULT", "Invoke Default", "", 2),
]

class Jueg_OpsDetails_IconProp(bpy.types.PropertyGroup):
	expand : bpy.props.BoolProperty(name="Expand", description="Expand, to display all icons at once", default=False, override={"LIBRARY_OVERRIDABLE"})
	search : bpy.props.StringProperty(name="Search", description="Search for icons by name", default="", override={"LIBRARY_OVERRIDABLE"})

class Jueg_OpsDetails_DisplayProp(bpy.types.PropertyGroup):
	icon_on  : bpy.props.PointerProperty(type=Jueg_OpsDetails_IconProp, override={"LIBRARY_OVERRIDABLE"})
	icon_off : bpy.props.PointerProperty(type=Jueg_OpsDetails_IconProp, override={"LIBRARY_OVERRIDABLE"})
	amount   : bpy.props.IntProperty(default=10, override={"LIBRARY_OVERRIDABLE"})

class Jueg_EventData(bpy.types.PropertyGroup):
	label  : bpy.props.StringProperty(name="label", override={"LIBRARY_OVERRIDABLE"})
	mode   : bpy.props.StringProperty(name="mode", override={"LIBRARY_OVERRIDABLE"})
	event  : bpy.props.EnumProperty(items=jueg_event_modif, override={"LIBRARY_OVERRIDABLE"})
	solo   : bpy.props.BoolProperty(override={"LIBRARY_OVERRIDABLE"})
	active : bpy.props.BoolProperty(default=True, name="Active", override={"LIBRARY_OVERRIDABLE"})
	mirror : bpy.props.BoolProperty(default=False, name="Mirror", override={"LIBRARY_OVERRIDABLE"})

#Dev note :
#Any new data needs update in
	# init_default_ops ( 2 times )
	# POSE_OT_jueg_reload_linked_data

class Jueg_OpsItem(bpy.types.PropertyGroup):
	id   : bpy.props.StringProperty(name="Unique id", override={"LIBRARY_OVERRIDABLE"})
	name : bpy.props.StringProperty(name="Ops Name", override={"LIBRARY_OVERRIDABLE"})
	ops_exe : bpy.props.StringProperty(name="Ops Exe", override={"LIBRARY_OVERRIDABLE"})
	ops_type : bpy.props.EnumProperty(items=jueg_ops_type_items, override={"LIBRARY_OVERRIDABLE"})
	icon_on	: bpy.props.StringProperty(name="Icon On", override={"LIBRARY_OVERRIDABLE"})
	icon_off   : bpy.props.StringProperty(name="Icon Off", override={"LIBRARY_OVERRIDABLE"})
	ok_for_current_sel : bpy.props.BoolProperty(override={"LIBRARY_OVERRIDABLE"})
	ops_context : bpy.props.EnumProperty(items=jueg_ops_context, name="Context", override={"LIBRARY_OVERRIDABLE"})
	user_defined : bpy.props.BoolProperty(override={"LIBRARY_OVERRIDABLE"})
	event_manage : bpy.props.BoolProperty(default=False, override={"LIBRARY_OVERRIDABLE"})
	events : bpy.props.CollectionProperty(type=Jueg_EventData, override={"LIBRARY_OVERRIDABLE", "USE_INSERTION"})
	active_event : bpy.props.IntProperty(default=0, override={"LIBRARY_OVERRIDABLE"})
	icons : bpy.props.PointerProperty(type=Jueg_OpsDetails_DisplayProp, override={"LIBRARY_OVERRIDABLE"})
	magic_nb : bpy.props.IntProperty(default=0, override={"LIBRARY_OVERRIDABLE"})

class Jueg_SideItem(bpy.types.PropertyGroup):
	name_R : bpy.props.StringProperty(name="Side name R", override={"LIBRARY_OVERRIDABLE"})
	name_L : bpy.props.StringProperty(name="Side name L", override={"LIBRARY_OVERRIDABLE"})

class Jueg_Clickable_Name(bpy.types.PropertyGroup):
	name_clickable : bpy.props.BoolProperty(default=False, override={"LIBRARY_OVERRIDABLE"})
	clickable_ops  : bpy.props.EnumProperty(items=clickable_ops_items, override={"LIBRARY_OVERRIDABLE"})
	clickable_mode : bpy.props.EnumProperty(items=clickable_mode_items, override={"LIBRARY_OVERRIDABLE"})
	clickable_events_on : bpy.props.BoolProperty(default=False, override={"LIBRARY_OVERRIDABLE"})

def register():
	bpy.utils.register_class(Jueg_OnOffEntry)
	bpy.utils.register_class(Jueg_BoneEntry)
	bpy.utils.register_class(Jueg_BoneGroup)
	bpy.utils.register_class(Jueg_OpsDisplay)
	bpy.utils.register_class(Jueg_GroupType)
	bpy.utils.register_class(Jueg_OpsDetails_IconProp)
	bpy.utils.register_class(Jueg_OpsDetails_DisplayProp)
	bpy.utils.register_class(Jueg_EventData)
	bpy.utils.register_class(Jueg_OpsItem)
	bpy.utils.register_class(Jueg_menu_temp_data)
	bpy.utils.register_class(Jueg_SideItem)
	bpy.utils.register_class(Jueg_Clickable_Name)


def unregister():
	bpy.utils.unregister_class(Jueg_OnOffEntry)
	bpy.utils.unregister_class(Jueg_BoneEntry)
	bpy.utils.unregister_class(Jueg_BoneGroup)
	bpy.utils.unregister_class(Jueg_OpsDisplay)
	bpy.utils.unregister_class(Jueg_GroupType)
	bpy.utils.unregister_class(Jueg_EventData)
	bpy.utils.unregister_class(Jueg_OpsItem)
	bpy.utils.unregister_class(Jueg_OpsDetails_IconProp)
	bpy.utils.unregister_class(Jueg_OpsDetails_DisplayProp)
	bpy.utils.unregister_class(Jueg_menu_temp_data)
	bpy.utils.unregister_class(Jueg_SideItem)
	bpy.utils.unregister_class(Jueg_Clickable_Name)
