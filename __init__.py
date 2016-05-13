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
	from . import addon_pref
	from . import ops_grouptype
	from . import ops_bonegroup
	from . import ops_ops
	from . import ops_text
	from . import ui_list
	from . import ui_panel
	from . import template_default_ops
	from . import text_ops_squel
	
import bpy
import bpy.utils.previews
import os
from bpy.app.handlers import persistent

class BoneEntry(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Bone Name")
	
class OnOffEntry(bpy.types.PropertyGroup):
	id      = bpy.props.StringProperty(name="Id of Ops")
	on_off  = bpy.props.BoolProperty(name="On_Off")

class BoneGroup(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Group Name")
	bone_ids = bpy.props.CollectionProperty(type=BoneEntry)
	on_off = bpy.props.CollectionProperty(type=OnOffEntry)
	current_selection = bpy.props.BoolProperty()
	
class OpsDisplay(bpy.types.PropertyGroup):
	id   = bpy.props.StringProperty(name="Unique id")
	display = bpy.props.BoolProperty()

class GroupType(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Group Type Name")
	group_ids = bpy.props.CollectionProperty(type=BoneGroup)
	active_bonegroup = bpy.props.IntProperty()
	ops_display = bpy.props.CollectionProperty(type=OpsDisplay)
	active_ops = bpy.props.IntProperty()
	
def update_editmode_func(self, context):
	if context.scene.bonegroup_editmode == False:
		context.scene.bonegroup_devmode = False
		context.scene.bonegroup_adminmode = False
		
def update_devmode_func(self, context):
	if context.scene.bonegroup_devmode == False:
		context.scene.bonegroup_adminmode = False

ops_type_items = [
	("BOOL", "On/Off", "", 1),
	("EXE", "Exec", "", 2),
	]

class OpsItem(bpy.types.PropertyGroup):
	id   = bpy.props.StringProperty(name="Unique id")
	name = bpy.props.StringProperty(name="Ops Name")
	ops_exe = bpy.props.StringProperty(name="Ops Exe")
	ops_type = bpy.props.EnumProperty(items=ops_type_items)
	icon_on	= bpy.props.StringProperty(name="Icon On")
	icon_off   = bpy.props.StringProperty(name="Icon Off")
	ok_for_current_sel = bpy.props.BoolProperty()
	user_defined = bpy.props.BoolProperty()

def save_collection(source, target):
	#delete existing
	while len(target) != 0:
		target.remove(0)
	#add
	for ope in source:
		ops = target.add()
		ops.id = ope.id
		ops.name = ope.name
		ops.ops_exe = ope.ops_exe
		ops.ops_type = ope.ops_type
		ops.icon_on = ope.icon_on
		ops.icon_off = ope.icon_off
		ops.ok_for_current_sel = ope.ok_for_current_sel
		ops.user_defined = ope.user_defined

@persistent
def load_handler(dummy):
	#check if data is already saved in a scene
	user_preferences = bpy.context.user_preferences
	addon_prefs = user_preferences.addons[__package__].preferences
	if addon_prefs.scene_name != "":
		save_collection(bpy.data.scenes[addon_prefs.scene_name].extragroups_save, addon_prefs.extragroups_ops)
	else:
		for scene in bpy.data.scenes:
			if len(scene.extragroups_save) != 0:
				addon_prefs.scene_name = scene.name
				save_collection(bpy.data.scenes[addon_prefs.scene_name].extragroups_save, addon_prefs.extragroups_ops)
				break


@persistent
def save_handler(dummy):
	user_preferences = bpy.context.user_preferences
	if __package__ in user_preferences.addons:
		addon_prefs = user_preferences.addons[__package__].preferences	
		if addon_prefs.scene_name == "":
			addon_prefs.scene_name = bpy.context.scene.name
		save_collection(addon_prefs.extragroups_ops, bpy.data.scenes[addon_prefs.scene_name].extragroups_save)

def register():
	bpy.app.handlers.load_post.append(load_handler)
	bpy.app.handlers.save_pre.append(save_handler)
	bpy.utils.register_class(OnOffEntry)
	bpy.utils.register_class(BoneEntry)
	bpy.utils.register_class(BoneGroup)
	bpy.utils.register_class(OpsDisplay)
	bpy.utils.register_class(GroupType)
	bpy.utils.register_class(OpsItem)
	bpy.utils.register_class
	
	bpy.types.Object.grouptypelist = bpy.props.CollectionProperty(type=GroupType)
	bpy.types.Object.active_grouptype = bpy.props.IntProperty()
	bpy.types.Scene.extragroups_save = bpy.props.CollectionProperty(type=OpsItem)

	addon_pref.register()
	ops_grouptype.register()
	ops_bonegroup.register()
	ops_ops.register()
	ops_text.register()
	ui_list.register()
	ui_panel.register()
	template_default_ops.register()

	bpy.extragroups_icons = {}
	
	pcoll = bpy.utils.previews.new()
	my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")
	pcoll.load("bonegroup_assign", os.path.join(my_icons_dir, "bonegroup_assign.png"), 'IMAGE')
	pcoll.load("bonegroup_remove", os.path.join(my_icons_dir, "bonegroup_remove.png"), 'IMAGE')
	bpy.extragroups_icons["bonegroup"] = pcoll
	
def unregister():
	bpy.utils.unregister_class(OnOffEntry)
	bpy.utils.unregister_class(BoneEntry)
	bpy.utils.unregister_class(BoneGroup)
	bpy.utils.unregister_class(OpsDisplay)
	bpy.utils.unregister_class(GroupType)
	bpy.utils.unregister_class(OpsItem)
	
	del bpy.types.Object.grouptypelist
	del bpy.types.Object.active_grouptype
	del bpy.types.Scene.extragroups_save

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
