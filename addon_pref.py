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
from .globs import *

class jueg_AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	multitype      = bpy.props.BoolProperty(default= False)
	textremove     = bpy.props.BoolProperty(default= True)
	edit_mode      = bpy.props.BoolProperty(default= False)
	use_color      = bpy.props.BoolProperty(default= False)
	use_keyingset  = bpy.props.BoolProperty(default= False)

	internal_keyingset = bpy.props.StringProperty(default="ExtraGroups KeyingSet")

	category = bpy.props.StringProperty(name="Category", default="ExtraGroups", update=update_panel_cb)

	tab1 = bpy.props.BoolProperty(default=False)
	tab2 = bpy.props.BoolProperty(default=False)
	tab3 = bpy.props.BoolProperty(default=False)
	tab4 = bpy.props.BoolProperty(default=False)

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
		row_global.prop(self, "edit_mode", text="Edit Mode")
		row_global = layout.row()
		row_global.prop(self, "tab1", text="Options", icon='SOLO_ON')
		if self.tab1 == True:
			row_global = layout.row()
			row_global.prop(self, "multitype", text="Use Multitype")
			row_global = layout.row()
			row_global.prop(self, "use_keyingset", text="KeyingSet Management")
			row_global = layout.row()
			row_global.prop(self, "textremove", text="Remove text when delete Operator")


		row_global = layout.row()
		row_global.prop(self, "tab2", text="Display", icon='SOLO_ON')
		if self.tab2 == True:
			row_global = layout.row()
			col = row_global.column()
			row = col.row()
			row.prop(self, "category", text="Addon tab")
			row = col.row()
			row.prop(self, "use_color", text="Use color")

		row_global = layout.row()
		row_global.prop(self, "tab3", text="Import/Export", icon='SOLO_ON')
		if self.tab3 == True:
			row_global = layout.row()
			col = row_global.column()
			row = col.row()
			row.operator("jueg.import_from_bone_groups", text="Import from Bone Groups")
			col = row_global.column()
			row = col.row()
			row.operator("jueg.import_from_selection_sets", text="Import from Selection Sets")
			col = row_global.column()
			row = col.row()
			row.operator("jueg.import_from_keying_sets", text="Import from Keying Sets")
			col = row_global.column()
			row = col.row()
			row.operator("jueg.import_from_file", text="Import from File")
			row_global = layout.row()
			col = row_global.column()
			row = col.row()
			row.operator("jueg.export_to_file", text="Export to File")

		row_global = layout.row()
		row_global.prop(self, "tab4", text="Danger Zone", icon='SOLO_ON')
		if self.tab4 == True:
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
