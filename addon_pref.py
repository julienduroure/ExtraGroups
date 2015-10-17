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
import bpy

class ExtragroupsPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	multitype = bpy.props.BoolProperty(default= False)

	textremove = bpy.props.BoolProperty(default= True)


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
		box.operator("export.extragroups_ops", text="Export Operators")
		box.operator("imp.extragroups_ops", text="Import Operators")


def register():
	bpy.utils.register_class(ExtragroupsPreferences)

def unregister():
	bpy.utils.unregister_class(ExtragroupsPreferences)

