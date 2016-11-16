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
bl_info = {
	"name": "Extra Groups",
	"version": (0, 0, 4),
	"author": "Julien Duroure",
	"blender": (2, 78, 0),
	"description": "Extra Groups Tools",
	"location": "Toolshelf > Extra Groups Tab",
	"wiki_url": "http://blerifa.com/tools/ExtraGroups/",
	"tracker_url": "https://github.com/julienduroure/ExtraGroups/issues/",
	"category": "Animation"
}

if "bpy" in locals():
	import imp
	imp.reload(globs)
	imp.reload(utils)
	imp.reload(addon_pref)
	imp.reload(ops_grouptype)
	imp.reload(ops_bonegroup)
	imp.reload(ops_ops)
	imp.reload(ops_text)
	imp.reload(ops_event)
	imp.reload(ui_list)
	imp.reload(ui_panel)
	imp.reload(template_default_ops)
	imp.reload(text_ops_squel)
	imp.reload(ops_import)
else:
	from .globs import *
	from .utils import *
	from .addon_pref import *
	from .ops_grouptype import *
	from .ops_bonegroup import *
	from .ops_ops import *
	from .ops_text import *
	from .ops_event import *
	from .ui_list import *
	from .ui_panel import *
	from .template_default_ops import *
	from .text_ops_squel import *
	from .ops_import import *

import bpy
import bpy.utils.previews
import os

def register():
	globs.register()
	addon_pref.register()
	ops_grouptype.register()
	ops_bonegroup.register()
	ops_ops.register()
	ops_text.register()
	ops_event.register()
	ui_list.register()
	ui_panel.register()
	template_default_ops.register()
	ops_import.register()

	bpy.types.Object.jueg_grouptypelist = bpy.props.CollectionProperty(type=globs.Jueg_GroupType)
	bpy.types.Object.jueg_extragroups_ops = bpy.props.CollectionProperty(type=globs.Jueg_OpsItem)
	bpy.types.Object.jueg_active_grouptype = bpy.props.IntProperty()

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

	globs.unregister()
	addon_pref.unregister()
	ops_grouptype.unregister()
	ops_bonegroup.unregister()
	ops_ops.unregister()
	ops_text.unregister()
	ops_event.unregister()
	ui_list.unregister()
	ui_panel.unregister()
	template_default_ops.unregister()
	ops_import.unregister()

	for pcoll in bpy.extragroups_icons.values():
		bpy.utils.previews.remove(pcoll)
	bpy.extragroups_icons.clear()

if __name__ == "__main__":
    register()
