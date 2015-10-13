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
	"blender": (2, 75, 0),
	"description": "Extra Groups Tools",
	"location": "Toolshelf > Extra Groups Tab",
	"wiki_url": "http://julienduroure.com/extragroups/",
	"tracker_url": "https://github.com/julienduroure/extragroups",
	"category": "Animation"
}
	
if "bpy" in locals():
	import importlib
	importlib.reload(ops_grouptype)
	importlib.reload(ops_bonegroup)
	importlib.reload(ops_ops)
	importlib.reload(ops_template)
	importlib.reload(ops_text)
	importlib.reload(ui_list)
	importlib.reload(ui_panel)
	importlib.reload(template_default_ops)
	importlib.reload(text_ops_squel)
else:
	from . import ( ops_grouptype, ops_bonegroup, ops_ops, ops_template, ops_text, ui_list, ui_panel, template_default_ops )


import bpy
import bpy.utils.previews
import os

ops_type_items = [
	("BOOL", "On/Off", "", 1),
	("EXE", "Exec", "", 2),
	]

class BoneEntry(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Bone Name")
	
class OnOffEntry(bpy.types.PropertyGroup):
	id = bpy.props.StringProperty(name="Id of Ops")
	value = bpy.props.BoolProperty(name="Value")


class TemplateItem(bpy.types.PropertyGroup):
	id   = bpy.props.StringProperty(name="Unique id")
	name = bpy.props.StringProperty(name="Ops Name")
	ops_exe = bpy.props.StringProperty(name="Ops Exe")
	ops_type = bpy.props.EnumProperty(items=ops_type_items)
	icon_on	= bpy.props.StringProperty(name="Icon On")
	icon_off   = bpy.props.StringProperty(name="Icon Off")
	ok_for_current_sel = bpy.props.BoolProperty()

class OpsItem(bpy.types.PropertyGroup):
	id   = bpy.props.StringProperty(name="Unique id")
	name = bpy.props.StringProperty(name="Ops Name")
	ops_exe = bpy.props.StringProperty(name="Ops Exe")
	ops_type = bpy.props.EnumProperty(items=ops_type_items)
	icon_on	= bpy.props.StringProperty(name="Icon On")
	icon_off   = bpy.props.StringProperty(name="Icon Off")
	from_template = bpy.props.BoolProperty()
	ok_for_current_sel = bpy.props.BoolProperty()

class BoneGroup(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Group Name")
	bone_ids = bpy.props.CollectionProperty(type=BoneEntry)
	on_off = bpy.props.CollectionProperty(type=OnOffEntry)
	current_selection = bpy.props.BoolProperty()

class GroupType(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Group Type Name")
	group_ids = bpy.props.CollectionProperty(type=BoneGroup)
	active_bonegroup = bpy.props.IntProperty()
	ops_ids = bpy.props.CollectionProperty(type=OpsItem)
	active_ops = bpy.props.IntProperty()
	
def update_editmode_func(self, context):
	if context.scene.bonegroup_editmode == False:
		context.scene.bonegroup_devmode = False
		context.scene.bonegroup_adminmode = False
		
def update_devmode_func(self, context):
	if context.scene.bonegroup_devmode == False:
		context.scene.bonegroup_adminmode = False
	
def register():
	bpy.utils.register_class(OnOffEntry)
	bpy.utils.register_class(BoneEntry)
	bpy.utils.register_class(BoneGroup)
	bpy.utils.register_class(OpsItem)
	bpy.utils.register_class(GroupType)
	bpy.utils.register_class(TemplateItem)
	
	bpy.types.Object.grouptypelist = bpy.props.CollectionProperty(type=GroupType)
	bpy.types.Scene.templatelist  = bpy.props.CollectionProperty(type=TemplateItem)
	bpy.types.Object.active_grouptype = bpy.props.IntProperty()
	bpy.types.Scene.active_template  = bpy.props.IntProperty()
	
	bpy.types.Scene.bonegroup_editmode   = bpy.props.BoolProperty(default= False, update=update_editmode_func)
	bpy.types.Scene.bonegroup_devmode	= bpy.props.BoolProperty(default= False, update=update_devmode_func)
	bpy.types.Scene.bonegroup_adminmode  = bpy.props.BoolProperty(default= False)
	bpy.types.Scene.bonegroup_textremove = bpy.props.BoolProperty(default= True)
	bpy.types.Scene.bonegroup_multitype  = bpy.props.BoolProperty(default= False)

	ops_grouptype.register()
	ops_bonegroup.register()
	ops_ops.register()
	ops_template.register()
	ops_text.register()
	ui_list.register()
	ui_panel.register()
	template_default_ops.register()

	bpy.bonegroup_icons = {}

	pcoll = bpy.utils.previews.new()
	my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")
	pcoll.load("bonegroup_assign", os.path.join(my_icons_dir, "bonegroup_assign.png"), 'IMAGE')
	pcoll.load("bonegroup_remove", os.path.join(my_icons_dir, "bonegroup_remove.png"), 'IMAGE')
	bpy.bonegroup_icons["bonegroup"] = pcoll
	
def unregister():
	bpy.utils.unregister_class(OnOffEntry)
	bpy.utils.unregister_class(BoneEntry)
	bpy.utils.unregister_class(BoneGroup)
	bpy.utils.unregister_class(OpsItem)
	bpy.utils.unregister_class(GroupType)
	bpy.utils.unregister_class(TemplateItem)
	
	del bpy.types.Object.grouptypelist
	del bpy.types.Scene.templatelist
	del bpy.types.Object.active_grouptype
	del bpy.types.Scene.active_template
	
	del bpy.types.Scene.bonegroup_editmode   
	del bpy.types.Scene.bonegroup_devmode	
	del bpy.types.Scene.bonegroup_adminmode  
	del bpy.types.Scene.bonegroup_textremove
	del bpy.types.Scene.bonegroup_multitype

	ops_grouptype.unregister()
	ops_bonegroup.unregister()
	ops_ops.unregister()
	ops_template.unregister()
	ops_text.unregister()
	ui_list.unregister()
	ui_panel.unregister()
	template_default_ops.unregister()

	for pcoll in bpy.bonegroup_icons.values():
		bpy.utils.previews.remove(pcoll)
	bpy.bonegroup_icons.clear()
	
if __name__ == "__main__":
    register()
