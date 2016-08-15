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

class Jueg_BoneEntry(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Bone Name")

class Jueg_OnOffEntry(bpy.types.PropertyGroup):
	id      = bpy.props.StringProperty(name="Id of Ops")
	on_off  = bpy.props.BoolProperty(name="On_Off")

class Jueg_BoneGroup(bpy.types.PropertyGroup):
	name              = bpy.props.StringProperty(name="Group Name")
	bone_ids          = bpy.props.CollectionProperty(type=Jueg_BoneEntry)
	on_off            = bpy.props.CollectionProperty(type=Jueg_OnOffEntry)
	solo              = bpy.props.CollectionProperty(type=Jueg_OnOffEntry)
	current_selection = bpy.props.BoolProperty()
	color             = bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', default=[0.0,0.0,0.0], min=0.0, max=1.0)
	keying            = bpy.props.StringProperty(name="Keying Set")

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

class Jueg_OpsDetails_IconProp(bpy.types.PropertyGroup):
	expand = bpy.props.BoolProperty(name="Expand", description="Expand, to display all icons at once", default=False)
	search = bpy.props.StringProperty(name="Search", description="Search for icons by name", default="")

class Jueg_OpsDetails_DisplayProp(bpy.types.PropertyGroup):
	icon_on  = bpy.props.PointerProperty(type=Jueg_OpsDetails_IconProp)
	icon_off = bpy.props.PointerProperty(type=Jueg_OpsDetails_IconProp)
	amount   = bpy.props.IntProperty(default=10)

class Jueg_EventData(bpy.types.PropertyGroup):
	mode = bpy.props.StringProperty(name="mode")
	event = bpy.props.EnumProperty(items=jueg_event_modif)
	solo  = bpy.props.BoolProperty()

#Dev note :
#Any new data needs update in
	# init_default_ops ( 2 times )
	# POSE_OT_jueg_reload_linked_data

class Jueg_OpsItem(bpy.types.PropertyGroup):
	id   = bpy.props.StringProperty(name="Unique id")
	name = bpy.props.StringProperty(name="Ops Name")
	ops_exe = bpy.props.StringProperty(name="Ops Exe")
	ops_type = bpy.props.EnumProperty(items=jueg_ops_type_items)
	icon_on	= bpy.props.StringProperty(name="Icon On")
	icon_off   = bpy.props.StringProperty(name="Icon Off")
	ok_for_current_sel = bpy.props.BoolProperty()
	user_defined = bpy.props.BoolProperty()
	event_manage = bpy.props.BoolProperty(default=False)
	events = bpy.props.CollectionProperty(type=Jueg_EventData)
	active_event = bpy.props.IntProperty(default=0)
	icons = bpy.props.PointerProperty(type=Jueg_OpsDetails_DisplayProp)
	update_nb = bpy.props.IntProperty(default=0)

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
