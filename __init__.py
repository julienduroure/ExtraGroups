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
bl_info = {
	"name": "Extra Groups",
	"version": (0, 9, 0),
	"author": "Julien Duroure",
	"blender": (2, 78, 0),
	"description": "Extra Groups Tools",
	"location": "Toolshelf > Extra Groups Tab",
	"wiki_url": "http://blerifa.com/tools/ExtraGroups/",
	"tracker_url": "https://github.com/julienduroure/BleRiFa/issues/",
	"category": "Animation"
}

if "bpy" in locals():
	import imp
	imp.reload(globs)
	imp.reload(utils)
	imp.reload(addon_pref)
	imp.reload(ops_bonegroup)
	imp.reload(ops_ops)
	imp.reload(ops_text)
	imp.reload(ui_list)
	imp.reload(ui_panel)
	imp.reload(ui_popup)
	imp.reload(ui_ops_ops)
	imp.reload(ui_ops_grouptype)
	imp.reload(ui_ops_bonegroup)
	imp.reload(ui_ops_event)
	imp.reload(ops)
	imp.reload(text_ops_squel)
	imp.reload(ops_import)
	imp.reload(ops_export)
	imp.reload(ops_addon_update)
	imp.reload(keymap)
else:
	from .globs import *
	from .utils import *
	from .addon_pref import *
	from .ops_bonegroup import *
	from .ops_ops import *
	from .ops_text import *
	from .ui_list import *
	from .ui_panel import *
	from .ui_popup import *
	from .ui_ops_ops import *
	from .ui_ops_grouptype import *
	from .ui_ops_bonegroup import *
	from .ui_ops_event import *
	from .ops import *
	from .text_ops_squel import *
	from .ops_import import *
	from .ops_export import *
	from .ops_addon_update import *
	from .keymap import *

import bpy
import bpy.utils.previews
import os

def register():
	globs.register()
	addon_pref.register()
	ops_bonegroup.register()
	ops_ops.register()
	ops_text.register()
	ui_list.register()
	ui_panel.register()
	ui_popup.register()
	ui_ops_ops.register()
	ui_ops_grouptype.register()
	ui_ops_bonegroup.register()
	ui_ops_event.register()
	ops.register()
	ops_import.register()
	ops_export.register()
	ops_addon_update.register()
	keymap.register_keymap()

	bpy.types.Object.jueg_grouptypelist = bpy.props.CollectionProperty(type=globs.Jueg_GroupType)
	bpy.types.Object.jueg_extragroups_ops = bpy.props.CollectionProperty(type=globs.Jueg_OpsItem)
	bpy.types.Object.jueg_active_grouptype = bpy.props.IntProperty()
	bpy.types.Object.jueg_menu_temp_data = bpy.props.PointerProperty(type=globs.Jueg_menu_temp_data)

	bpy.types.Scene.on_off_save = bpy.props.CollectionProperty(type=globs.Jueg_OnOffEntry)  #used only temp for update addon
	bpy.types.Scene.solo_save = bpy.props.CollectionProperty(type=globs.Jueg_OnOffEntry)    #used only temp for update addon
	bpy.types.Scene.display_save = bpy.props.CollectionProperty(type=globs.Jueg_OpsDisplay) #used only temp for update addon

	bpy.extragroups_icons = {}

	pcoll = bpy.utils.previews.new()
	my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")
	pcoll.load("bonegroup_assign", os.path.join(my_icons_dir, "bonegroup_assign.png"), 'IMAGE')
	pcoll.load("bonegroup_remove", os.path.join(my_icons_dir, "bonegroup_remove.png"), 'IMAGE')
	bpy.extragroups_icons["bonegroup"] = pcoll

def unregister():
	del bpy.types.Object.jueg_grouptypelist
	del bpy.types.Object.jueg_active_grouptype
	del bpy.types.Object.jueg_extragroups_ops
	del bpy.types.Object.jueg_menu_temp_data

	globs.unregister()
	addon_pref.unregister()
	ops_bonegroup.unregister()
	ops_ops.unregister()
	ops_text.unregister()
	ui_list.unregister()
	ui_panel.unregister()
	ui_popup.unregister()
	ui_ops_ops.unregister()
	ui_ops_grouptype.unregister()
	ui_ops_bonegroup.unregister()
	ui_ops_event.unregister()
	ops.unregister()
	ops_import.unregister()
	ops_export.unregister()
	ops_addon_update.unregister()
	keymap.unregister_keymap()

	for pcoll in bpy.extragroups_icons.values():
		bpy.utils.previews.remove(pcoll)
	bpy.extragroups_icons.clear()

if __name__ == "__main__":
	register()
