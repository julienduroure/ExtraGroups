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


class POSE_OT_template_move(bpy.types.Operator):
	"""Move the template up or down in the list"""
	bl_idname = "pose.template_move"
	bl_label = "Move Template"
	bl_options = {'REGISTER'}
	
	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')		

	def execute(self, context):
		armature = context.object
		index	= context.scene.active_template
		
		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index
			
		if new_index < len(context.scene.templatelist) and new_index >= 0:
			context.scene.templatelist.move(index, new_index)
			context.scene.active_template = new_index
		
		return {'FINISHED'}
		
		
class POSE_OT_template_add(bpy.types.Operator):
	"""Add a new template"""
	bl_idname = "pose.template_add"
	bl_label = "Add Template"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')
				
	def execute(self, context):
		armature = context.object
		
		template = context.scene.templatelist.add()
		template.name = "Template.%d" % len(context.scene.templatelist)
		template.ops_type = 'EXE'
		context.scene.active_template = len(context.scene.templatelist) - 1
		
		return {'FINISHED'}
	
class POSE_OT_template_remove(bpy.types.Operator):
	"""Remove the current template"""
	bl_idname = "pose.template_remove"
	bl_label = "Remove Template"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')
				
	def execute(self, context):
		armature = context.object	 
		
		context.scene.templatelist.remove(context.scene.active_template)
		len_ = len(context.scene.templatelist)
		if (context.scene.active_template > (len_ - 1) and len_ > 0):
			context.scene.active_template = len(context.scene.templatelist) - 1
		return {'FINISHED'}   

class POSE_OT_template_init(bpy.types.Operator):
	"""Init template list with default values from Addon"""
	bl_idname = "pose.template_init"
	bl_label = "Template list Init"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')
				
	def execute(self, context):
		#don't use it !!!! will be deleted
		template = bpy.context.scene.templatelist.add()  
		template.name = "Select Only"
		template.ops_type = 'EXE'
		template.ops_exe   = "pose.selectonly"
		template.icon_on  = "HAND"
		template.ok_for_current_sel = False
		template = bpy.context.scene.templatelist.add()  
		template.name = "Add to selection"
		template.ops_type = 'EXE'
		template.ops_exe   = "pose.addtoselection"
		template.icon_on  = "ZOOMIN"
		template.ok_for_current_sel = False
		template = bpy.context.scene.templatelist.add()  
		template.name = "Mute"
		template.ops_type = 'BOOL'
		template.ops_exe   = "pose.bonemute"
		template.icon_on  = "MUTE_IPO_OFF"
		template.icon_off  = "MUTE_IPO_ON"
		template.ok_for_current_sel = True
		template = bpy.context.scene.templatelist.add()  
		template.name = "Toggle Visibility"
		template.ops_type = 'BOOL'
		template.ops_exe   = "pose.change_visibility"
		template.icon_on  = "VISIBLE_IPO_ON"
		template.icon_off  = "VISIBLE_IPO_OFF"
		template.ok_for_current_sel = False
		template = bpy.context.scene.templatelist.add()  
		template.name = "Restrict/Allow Selection"
		template.ops_type = 'BOOL'
		template.ops_exe   = "pose.restrict_select"
		template.icon_on  = "RESTRICT_SELECT_OFF"
		template.icon_off  = "RESTRICT_SELECT_ON"
		template.ok_for_current_sel = True
		bpy.context.scene.active_template = len(bpy.context.scene.templatelist) - 1	 
		
		
		return {'FINISHED'}  

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
	bpy.utils.register_class(POSE_OT_template_add)
	bpy.utils.register_class(POSE_OT_template_remove)
	bpy.utils.register_class(POSE_OT_template_move)
	bpy.utils.register_class(POSE_OT_template_init)
	bpy.utils.register_class(ExportTemplate)
	bpy.utils.register_class(ImportTemplate)
	
def unregister():
	bpy.utils.unregister_class(POSE_OT_template_add)
	bpy.utils.unregister_class(POSE_OT_template_remove)
	bpy.utils.unregister_class(POSE_OT_template_move)
	bpy.utils.unregister_class(POSE_OT_template_init)
	bpy.utils.unregister_class(ExportTemplate)
	bpy.utils.unregister_class(ImportTemplate)
