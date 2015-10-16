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
import uuid
import bpy_extras
from .text_ops_squel import TEMPLATE


class POSE_OT_operator_move(bpy.types.Operator):
	"""Move up or down the current operator in the list"""
	bl_idname = "pose.operator_move"
	bl_label = "Move Operator"
	bl_options = {'REGISTER'}
	
	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')		

	def execute(self, context):
		armature = context.object
		index	= armature.grouptypelist[armature.active_grouptype].active_ops
		
		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index
			
		if new_index < len(armature.grouptypelist[armature.active_grouptype].ops_display) and new_index >= 0:
			armature.grouptypelist[armature.active_grouptype].ops_display.move(index, new_index)
			armature.grouptypelist[armature.active_grouptype].active_ops = new_index
		
		return {'FINISHED'}
		
class POSE_OT_ops_add(bpy.types.Operator):
	"""Add a new operator"""
	bl_idname = "pose.ops_add"
	bl_label = "Add Ops"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')		

	def execute(self, context):
		keep = False
		armature = context.object
		
		if len(armature.grouptypelist) > 0:
			
			ops = context.scene.extragroups_ops.add()
			ops.id   = uuid.uuid4().hex
			ops.name = "Ops.%d" % len(context.scene.extragroups_ops)
			ops.ops_exe = "pose.ope_" + ops.id
			ops.ops_type = 'EXE'
			ops.display = False
			ops.user_defined = True
			# now that id is generated, generate a new file
			textname = ops.id + ".py"
			if textname in bpy.data.texts:
				script = bpy.data.textx[textname]
				script.clear()
			else:
				script = bpy.data.texts.new(textname)
				script.use_module = True
				txt = TEMPLATE
				txt = txt.replace("###opsclass###",ops.id)
				script.write(txt)
				exec(script.as_string() + "\nregister()\n", {})
			
			
			#now add display info on each grouptype
			for grouptype in armature.grouptypelist:
				ope = grouptype.ops_display.add()
				ope.id = ops.id
				ope.display = False
		
			#now add on/off for each existing bone group of each type
			for grouptype in armature.grouptypelist:
				bonegroups = grouptype.group_ids
				for group in bonegroups:
					new_ = group.on_off.add()
					new_.id = ops.id
					new_.on_off = True
	
		return {'FINISHED'}
	
class POSE_OT_ops_remove(bpy.types.Operator):
	"""Remove the operator"""
	bl_idname = "pose.ops_remove"
	bl_label = "Remove Ops"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object
		
		id_to_delete = armature.grouptypelist[armature.active_grouptype].ops_display[armature.grouptypelist[armature.active_grouptype].active_ops].id
		if len(armature.grouptypelist) > 0 and len(armature.grouptypelist[armature.active_grouptype].ops_display) > 0:
			if context.scene.bonegroup_textremove == True:
				file_ = id_to_delete + ".py"
				bpy.ops.text.text_remove(text_id=file_)

			bpy.context.scene.extragroups_ops.remove([i for i,e in enumerate(bpy.context.scene.extragroups_ops) if e.id == id_to_delete][0])
			
			for grouptype in armature.grouptypelist:
				grouptype.ops_display.remove([i for i,e in enumerate(grouptype.ops_display) if e.id == id_to_delete][0])
				
				len_ = len(grouptype.ops_display)
				if (grouptype.active_ops > (len_ - 1) and len_ > 0):
					grouptype.active_ops = len(grouptype.ops_display) - 1
		return {'FINISHED'}
		
def write_operators(context, filepath):
    f = open(filepath, 'w', encoding='utf-8')
    f.write("import bpy\n")
    f.write("try:\n")
    tab = context.scene.extragroups_ops
    for ope in tab:
        f.write("\t#~~~~~~\n")
        f.write("\tif \"" + ope.id + "\" not in [j.id for i,j in enumerate(bpy.context.scene.extragroups_ops)]:\n")
        f.write("\t\tops = bpy.context.scene.extragroups_ops.add()\n")
        f.write("\t\tops.id = \"" + ope.id + "\"\n")
        f.write("\t\tops.name = \"" + ope.name + "\"\n")
        f.write("\t\tops.ops_type = \"" + ope.ops_type + "\"\n")
        f.write("\t\tops.ops_exe = \"" + ope.ops_exe + "\"\n")
        f.write("\t\tops.icon_on = \"" + ope.icon_on + "\"\n")
        f.write("\t\tops.icon_off = \"" + ope.icon_off + "\"\n")
        f.write("\t\tops.ok_for_current_sel = " + str(ope.ok_for_current_sel) + "\n")
        f.write("\t\tops.user_defined = " + str(ope.user_defined) + "\n")
        f.write("\t\tfor grouptype in bpy.context.active_object.grouptypelist:\n")
        f.write("\t\t\tope = grouptype.ops_display.add()\n")
        f.write("\t\t\tope.id = ops.id\n")
        f.write("\t\t\tope.display = False\n")
        f.write("\telse:\n")
        f.write("\t\tbpy.context.scene.extragroups_ops[[i for i,j in enumerate(bpy.context.scene.extragroups_ops) if j.id == \"" + ope.id + "\"][0]].name = \"" + ope.name + "\"\n")
        f.write("\t\tbpy.context.scene.extragroups_ops[[i for i,j in enumerate(bpy.context.scene.extragroups_ops) if j.id == \"" + ope.id + "\"][0]].icon_on = \"" + ope.icon_on + "\"\n")
        f.write("\t\tbpy.context.scene.extragroups_ops[[i for i,j in enumerate(bpy.context.scene.extragroups_ops) if j.id == \"" + ope.id + "\"][0]].icon_off = \"" + ope.icon_off + "\"\n")
		
    f.write("except:\n")
    f.write("\tpass\n")
    f.close()
    
    return {'FINISHED'}
		
class POSE_OT_ExportOps(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    """Export Operator list"""
    bl_idname = "export.extragroups_ops"
    bl_label  = "Export Operator"
    
    filename_ext = ".py"
    
    def execute(self, context):
        return write_operators(context, self.filepath)
		
def read_operator(context, filepath):
    f = open(filepath, 'r', encoding='utf-8')
    data = f.read()
    f.close()
    
    exec(data, {})
    
    return {'FINISHED'}
			
class POSE_OT_ImportOps(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    """Import Template list"""
    bl_idname = "imp.extragroups_ops"
    bl_label  = "Import Operators"
    
    filename_ext = ".py"
    
    def execute(self, context):
        return read_operator(context, self.filepath)
		
class POSE_OT_dummy(bpy.types.Operator):
	bl_idname = "pose.dummy"
	bl_label = "Dummy"
	bl_options = {'REGISTER'}  
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')
				
	def execute(self, context):

		return {'FINISHED'}  
		
def register():
	bpy.utils.register_class(POSE_OT_ops_add)
	bpy.utils.register_class(POSE_OT_ops_remove) 
	bpy.utils.register_class(POSE_OT_operator_move)
	bpy.utils.register_class(POSE_OT_ExportOps)
	bpy.utils.register_class(POSE_OT_ImportOps)
	bpy.utils.register_class(POSE_OT_dummy)
	
def unregister():
	bpy.utils.unregister_class(POSE_OT_ops_add)
	bpy.utils.unregister_class(POSE_OT_ops_remove) 
	bpy.utils.unregister_class(POSE_OT_operator_move)
	bpy.utils.unregister_class(POSE_OT_ExportOps)
	bpy.utils.unregister_class(POSE_OT_ImportOps)
	bpy.utils.unregister_class(POSE_OT_dummy)
