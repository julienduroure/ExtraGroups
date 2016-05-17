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

	multitype = bpy.props.BoolProperty(default= False)
	textremove = bpy.props.BoolProperty(default= True)
	extragroups_ops = bpy.props.CollectionProperty(type=Jueg_OpsItem)
	scene_name = bpy.props.StringProperty() #scene name that will temporary store data for saving


	def draw(self, context):
		layout = self.layout
		row_global = layout.row()

		col = row_global.column()
		row = col.row()
		row.label("Options")
		row_ = col.row()
		box = row_.box()
		box.prop(self, "multitype", text="Use Multitype")
		box.prop(self, "textremove", text="Remove text when delete Operator")

		
		col = row_global.column()
		row = col.row()
		row.label("Import / Export")
		row_ = col.row()
		box = row_.box()
		box.operator("export.jueg_extragroups_ops", text="Export Operators")
		box.operator("imp.jueg_extragroups_ops", text="Import Operators")
		box.enabled = (len(self.extragroups_ops) != 0)


def register():
	bpy.utils.register_class(jueg_AddonPreferences)

def unregister():
	bpy.utils.unregister_class(jueg_AddonPreferences)

