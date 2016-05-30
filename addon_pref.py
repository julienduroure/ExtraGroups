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
from .globals import *

class jueg_AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	multitype  = bpy.props.BoolProperty(default= False)
	textremove = bpy.props.BoolProperty(default= True)
	edit_mode  = bpy.props.BoolProperty(default= False)

	category = bpy.props.StringProperty(name="Category", default="AutoRefSpace", update=update_panel)

	def draw(self, context):
		layout = self.layout
		row_global = layout.row()

		col = row_global.column()
		row_ = col.row()
		box = row_.box()
		row = box.row()
		row.prop(self, "category", text="Addon tab")
		row = box.row()
		row.prop(self, "edit_mode", text="Edit Mode")
		row = box.row()
		if check_new_default_ops_in_new_addon_version() == True:
			row.operator("pose.jueg_update_new_addon_version", text="Update data to new addon version")

		col = row_global.column()
		row = col.row()
		row.label("Options")
		row_ = col.row()
		box = row_.box()
		box.prop(self, "multitype", text="Use Multitype")
		box.prop(self, "textremove", text="Remove text when delete Operator")

def register():
	bpy.utils.register_class(jueg_AddonPreferences)

def unregister():
	bpy.utils.unregister_class(jueg_AddonPreferences)
