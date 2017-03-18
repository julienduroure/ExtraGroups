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
from .globs import *

class jueg_AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	edit_mode       = bpy.props.BoolProperty(default= False)
	options			= bpy.props.BoolProperty(default= False)
	import_export 	= bpy.props.BoolProperty(default= False)

	multitype       = bpy.props.BoolProperty(default= False)
	use_color       = bpy.props.BoolProperty(default= False)
	use_keyingset   = bpy.props.BoolProperty(default= False)
	use_manipulator = bpy.props.BoolProperty(default= False)

	dev_mode		= bpy.props.BoolProperty(default= False)
	enable_popup    = bpy.props.BoolProperty(default= True, update=update_enable_popup_cb)
	textremove      = bpy.props.BoolProperty(default= True )

	keymap_key		= bpy.props.StringProperty(default='Q', update=update_keymap_cb)
	keymap_shift	= bpy.props.BoolProperty(default=False, update=update_keymap_cb)
	keymap_ctrl		= bpy.props.BoolProperty(default=False, update=update_keymap_cb)
	keymap_alt		= bpy.props.BoolProperty(default=False, update=update_keymap_cb)

	internal_keyingset = bpy.props.StringProperty(default="ExtraGroups KeyingSet")

	category = bpy.props.StringProperty(name="Category", default="ExtraGroups", update=update_panel_cb)

	xx_popup_display_multitype = bpy.props.BoolProperty(default=False)
	xx_sides = bpy.props.CollectionProperty(type=Jueg_SideItem)
	xx_active_side = bpy.props.IntProperty()

	name_clickable = bpy.props.BoolProperty(default=False)
	clickable_ops  = bpy.props.EnumProperty(items=clickable_ops_items)
	clickable_mode = bpy.props.EnumProperty(items=clickable_mode_items)

	tab1 = bpy.props.BoolProperty(default=False)
	tab2 = bpy.props.BoolProperty(default=False)
	tab3 = bpy.props.BoolProperty(default=False)

	def draw(self, context):
		armature = context.active_object
		try:
			linked, filepath = lib_proxy_armature()
		except:
			linked = False

		layout = self.layout
		row_global = layout.row()
		if check_addon_update_needed() == True and linked == False:
			row_global.operator("pose.jueg_update_new_addon_version", text="Update data to new addon version")
		elif check_addon_update_needed() == True and linked == True:
			row_global.operator("pose.jueg_reload_linked_data", text="Reload data from library")
			row_global = layout.row()
			row_global.label("Be sure to update your library file first", icon="ERROR")




		row_global = layout.row()
		row_global.prop(self, "tab1", text="Display", icon='SOLO_ON')
		if self.tab1 == True:
			row_global = layout.row()
			col = row_global.column()
			box = col.box()
			row = box.row()
			row.prop(self, "enable_popup", text="Enable Popup")
			if self.enable_popup == True:
				row = box.row()
				row.prop(self, "keymap_key", text="Key")
				row = box.row()
				row.prop(self, "keymap_shift", text="Shift")
				row = box.row()
				row.prop(self, "keymap_ctrl", text="Ctrl")
				row = box.row()
				row.prop(self, "keymap_alt", text="Alt")
			col = row_global.column()
			box = col.box()
			row = box.row()
			row.prop(self, "category", text="Addon tab")


		row_global = layout.row()
		row_global.prop(self, "tab2", text="Options", icon='SOLO_ON')
		if self.tab2 == True:
			row_global = layout.row()
			row_global.prop(self, "dev_mode", text="Developer mode")
			if self.dev_mode == True:
				row_global.prop(self, "textremove", text="Remove text when delete Operator")

		row_global = layout.row()
		row_global.prop(self, "tab3", text="Danger Zone", icon='SOLO_ON')
		if self.tab3 == True:
			row_global = layout.row()
			row_global.label("In case addon goes wrong, you can delete all data of this addon")
			row_global = layout.row()
			row_global.label("I repeat : THIS WILL ERASE ALL THIS ADDON DATA")
			row_global = layout.row()
			row_global.operator("pose.jueg_erase_data", text="ERASE ALL", icon="ERROR")

def register():
	bpy.utils.register_class(jueg_AddonPreferences)

def unregister():
	bpy.utils.unregister_class(jueg_AddonPreferences)
