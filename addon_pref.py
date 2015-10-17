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

class ExtragroupsPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	multitype = bpy.props.BoolProperty(default= False)

	textremove = bpy.props.BoolProperty(default= True)

	extragroups_ops = bpy.props.CollectionProperty(type=OpsItem)


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
	bpy.utils.register_class(OpsItem)
	bpy.utils.register_class(ExtragroupsPreferences)

def unregister():
	bpy.utils.unregister_class(OpsItem)
	bpy.utils.unregister_class(ExtragroupsPreferences)

