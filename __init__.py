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
bl_info = {
	"name": "Extra Groups",
	"version": (0, 0, 1),
	"author": "Julien Duroure",
	"blender": (2, 77, 0),
	"description": "Extra Groups Tools",
	"location": "Toolshelf > Extra Groups Tab, and 3DView property panel",
	"wiki_url": "http://julienduroure.com/extragroups/",
	"tracker_url": "https://github.com/julienduroure/extragroups",
	"category": "Animation"
}

if "bpy" in locals():
	import imp
	imp.reload(addon_pref)
	imp.reload(ops_grouptype)
	imp.reload(ops_bonegroup)
	imp.reload(ops_ops)
	imp.reload(ops_text)
	imp.reload(ui_list)
	imp.reload(ui_panel)
	imp.reload(template_default_ops)
	imp.reload(text_ops_squel)
else:
	from .globals import *
	from .addon_pref import *
	from .ops_grouptype import *
	from .ops_bonegroup import *
	from .ops_ops import *
	from .ops_text import *
	from .ui_list import *
	from .ui_panel import *
	from .template_default_ops import *
	from .text_ops_squel import *
	
import bpy
import bpy.utils.previews
import os

def register():
	globals.register()
	addon_pref.register()
	ops_grouptype.register()
	ops_bonegroup.register()
	ops_ops.register()
	ops_text.register()
	ui_list.register()
	ui_panel.register()
	template_default_ops.register()
	
	bpy.types.Object.grouptypelist = bpy.props.CollectionProperty(type=GroupType)
	bpy.types.Object.active_grouptype = bpy.props.IntProperty()
	bpy.types.Scene.extragroups_save = bpy.props.CollectionProperty(type=OpsItem)
	
	bpy.app.handlers.load_post.append(load_handler)
	bpy.app.handlers.save_pre.append(save_handler)

	bpy.extragroups_icons = {}
	
	pcoll = bpy.utils.previews.new()
	my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")
	pcoll.load("bonegroup_assign", os.path.join(my_icons_dir, "bonegroup_assign.png"), 'IMAGE')
	pcoll.load("bonegroup_remove", os.path.join(my_icons_dir, "bonegroup_remove.png"), 'IMAGE')
	bpy.extragroups_icons["bonegroup"] = pcoll
	
def unregister():
	del bpy.types.Object.grouptypelist
	del bpy.types.Object.active_grouptype
	del bpy.types.Scene.extragroups_save

	globals.unregister()
	addon_pref.unregister()
	ops_grouptype.unregister()
	ops_bonegroup.unregister()
	ops_ops.unregister()
	ops_text.unregister()
	ui_list.unregister()
	ui_panel.unregister()
	template_default_ops.unregister()

	for pcoll in bpy.extragroups_icons.values():
		bpy.utils.previews.remove(pcoll)
	bpy.extragroups_icons.clear()
	
if __name__ == "__main__":
    register()