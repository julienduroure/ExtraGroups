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
	
def update_editmode_func(self, context):
	if context.scene.bonegroup_editmode == False:
		context.scene.bonegroup_devmode = False
		context.scene.bonegroup_adminmode = False
		
def update_devmode_func(self, context):
	if context.scene.bonegroup_devmode == False:
		context.scene.bonegroup_adminmode = False

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
		save_collection(bpy.data.scenes[addon_prefs.scene_name].jueg_extragroups_save, addon_prefs.extragroups_ops)
	else:
		for scene in bpy.data.scenes:
			if len(scene.jueg_extragroups_save) != 0:
				addon_prefs.scene_name = scene.name
				save_collection(bpy.data.scenes[addon_prefs.scene_name].jueg_extragroups_save, addon_prefs.extragroups_ops)
				break


@persistent
def save_handler(dummy):
	user_preferences = bpy.context.user_preferences
	if __package__ in user_preferences.addons:
		addon_prefs = user_preferences.addons[__package__].preferences	
		if addon_prefs.scene_name == "":
			addon_prefs.scene_name = bpy.context.scene.name
		save_collection(addon_prefs.extragroups_ops, bpy.data.scenes[addon_prefs.scene_name].jueg_extragroups_save)

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