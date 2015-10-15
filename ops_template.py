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
import bpy_extras

def write_template(context, filepath):
    f = open(filepath, 'w', encoding='utf-8')
    f.write("import bpy\n")
    f.write("try:\n")
    tab = context.scene.templatelist
    for temp in tab:
        f.write("\ttemplate = bpy.context.scene.templatelist.add()\n")
        f.write("\ttemplate.name = \"" + temp.name + "\"\n")
        f.write("\ttemplate.ops_type = \"" + temp.ops_type + "\"\n")
        f.write("\ttemplate.ops_exe = \"" + temp.ops_exe + "\"\n")
        f.write("\ttemplate.icon_on = \"" + temp.icon_on + "\"\n")
        f.write("\ttemplate.icon_off = \"" + temp.icon_off + "\"\n")
        f.write("\ttemplate.ok_for_current_sel = " + str(temp.ok_for_current_sel) + "\n")
    f.write("\tbpy.context.scene.active_template = len(bpy.context.scene.templatelist) - 1\n")
    f.write("except:\n")
    f.write("\tpass\n")
    f.close()
    
    return {'FINISHED'}
	
def read_template(context, filepath):
    f = open(filepath, 'r', encoding='utf-8')
    data = f.read()
    f.close()
    
    exec(data, {})
    
    return {'FINISHED'}

class ExportTemplate(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    """Export Template list"""
    bl_idname = "export.bonegroup_template"
    bl_label  = "Export Template"
    
    filename_ext = ".py"
    
    def execute(self, context):
        return write_template(context, self.filepath)
		
		
class ImportTemplate(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    """Import Template list"""
    bl_idname = "imp.bonegroup_template"
    bl_label  = "Import Template"
    
    filename_ext = ".py"
    
    def execute(self, context):
        return read_template(context, self.filepath)
	
def register():
	bpy.utils.register_class(ExportTemplate)
	bpy.utils.register_class(ImportTemplate)
	
def unregister():
	bpy.utils.unregister_class(ExportTemplate)
	bpy.utils.unregister_class(ImportTemplate)
