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
import uuid
import bpy_extras
from .text_ops_squel import TEMPLATE
from .globals import *


class POSE_OT_jueg_operator_move(bpy.types.Operator):
	"""Move up or down the current operator in the list"""
	bl_idname = "pose.jueg_operator_move"
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
		index	= armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops
		
		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index
			
		if new_index < len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display) and new_index >= 0:
			armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display.move(index, new_index)
			armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops = new_index
		
		return {'FINISHED'}
		
class POSE_OT_jueg_ops_add(bpy.types.Operator):
	"""Add a new operator"""
	bl_idname = "pose.jueg_ops_add"
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
		
		if len(armature.jueg_grouptypelist) > 0:
			
			ops = addonpref().extragroups_ops.add()
			ops.id   = uuid.uuid4().hex
			ops.name = "Ops.%d" % len(addonpref().extragroups_ops)
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
			for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
				for grouptype in obj.jueg_grouptypelist:
					ope = grouptype.ops_display.add()
					ope.id = ops.id
					ope.display = False
		
			#now add on/off for each existing bone group of each type
			for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
				for grouptype in obj.jueg_grouptypelist:
					bonegroups = grouptype.group_ids
					for group in bonegroups:
						new_ = group.on_off.add()
						new_.id = ops.id
						new_.on_off = True

			armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops = len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display) - 1
	
		return {'FINISHED'}
	
class POSE_OT_jueg_ops_remove(bpy.types.Operator):
	"""Remove the operator"""
	bl_idname = "pose.jueg_ops_remove"
	bl_label = "Remove Ops"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object
		
		id_to_delete = armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id
		if len(armature.jueg_grouptypelist) > 0 and len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display) > 0:
			if addonpref().textremove == True:
				file_ = id_to_delete + ".py"
				bpy.ops.text.jueg_text_remove(text_id=file_)

			addonpref().extragroups_ops.remove([i for i,e in enumerate(addonpref().extragroups_ops) if e.id == id_to_delete][0])
			
			for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
				for grouptype in obj.jueg_grouptypelist:
					grouptype.ops_display.remove([i for i,e in enumerate(grouptype.ops_display) if e.id == id_to_delete][0])
				
					len_ = len(grouptype.ops_display)
					if (grouptype.active_ops > (len_ - 1) and len_ > 0):
						grouptype.active_ops = len(grouptype.ops_display) - 1

					#also remove on/off for each existing bonegroup of each type (of each armature)
					bonegroups = grouptype.group_ids
					for group in bonegroups:
						group.on_off.remove([i for i,j in enumerate(group.on_off) if j.id == id_to_delete][0])
				
		return {'FINISHED'}
		
def write_operators(context, filepath):
    tab = addonpref().extragroups_ops
    f = open(filepath, 'w', encoding='utf-8')
    f.write("import bpy\n")
    f.write("user_preferences = bpy.context.user_preferences\n")
    f.write("addonpref() = user_preferences.addons[\"extragroups\"].preferences\n")
    f.write("try:\n")
    for ope in tab:
        f.write("\t#~~~~~~\n")
        f.write("\tif \"" + ope.id + "\" not in [j.id for i,j in enumerate(addonpref().extragroups_ops)]:\n")
        f.write("\t\tops = addonpref().extragroups_ops.add()\n")
        f.write("\t\tops.id = \"" + ope.id + "\"\n")
        f.write("\t\tops.name = \"" + ope.name + "\"\n")
        f.write("\t\tops.ops_type = \"" + ope.ops_type + "\"\n")
        f.write("\t\tops.ops_exe = \"" + ope.ops_exe + "\"\n")
        f.write("\t\tops.icon_on = \"" + ope.icon_on + "\"\n")
        f.write("\t\tops.icon_off = \"" + ope.icon_off + "\"\n")
        f.write("\t\tops.ok_for_current_sel = " + str(ope.ok_for_current_sel) + "\n")
        f.write("\t\tops.user_defined = " + str(ope.user_defined) + "\n")
        f.write("\t\tfor obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:\n")
        f.write("\t\t\tfor grouptype in obj.jueg_grouptypelist:\n")
        f.write("\t\t\t\toper = grouptype.ops_display.add()\n")
        f.write("\t\t\t\toper.id = \"" + ope.id + "\"\n")
        f.write("\t\t\t\toper.display = False\n")
        f.write("\t\tfor obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:\n")
        f.write("\t\t\tfor grouptype in obj.jueg_grouptypelist:\n")
        f.write("\t\t\t\tbonegroups = grouptype.group_ids\n")
        f.write("\t\t\t\tfor group in bonegroups:\n")
        f.write("\t\t\t\t\tnew_ = group.on_off.add()\n")
        f.write("\t\t\t\t\tnew_.id = \"" + ope.id + "\"\n")
        f.write("\t\t\t\t\tnew_.on_off = True\n")
        f.write("\telse:\n")
        f.write("\t\taddonpref().extragroups_ops[[i for i,j in enumerate(addonpref().extragroups_ops) if j.id == \"" + ope.id + "\"][0]].name = \"" + ope.name + "\"\n")
        f.write("\t\taddonpref().extragroups_ops[[i for i,j in enumerate(addonpref().extragroups_ops) if j.id == \"" + ope.id + "\"][0]].icon_on = \"" + ope.icon_on + "\"\n")
        f.write("\t\taddonpref().extragroups_ops[[i for i,j in enumerate(addonpref().extragroups_ops) if j.id == \"" + ope.id + "\"][0]].icon_off = \"" + ope.icon_off + "\"\n")
		
    f.write("except:\n")
    f.write("\tpass\n")
    f.close()
    
    return {'FINISHED'}
		
class POSE_OT_jueg_ExportOps(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    """Export Operator list"""
    bl_idname = "export.jueg_extragroups_ops"
    bl_label  = "Export Operator"
    
    filename_ext = ".py"
    
    def execute(self, context):
        return write_operators(context, self.filepath)
		
def read_operator(context, filepath):
    try:
        f = open(filepath, 'r', encoding='utf-8')
        data = f.read()
        f.close()
    
        exec(data, {})
    except:
        print("Error reading / exec imported file...")
    return {'FINISHED'}
			
class POSE_OT_jueg_ImportOps(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    """Import Template list"""
    bl_idname = "imp.jueg_extragroups_ops"
    bl_label  = "Import Operators"
    
    filename_ext = ".py"
    
    def execute(self, context):
        return read_operator(context, self.filepath)
		
class POSE_OT_jueg_dummy(bpy.types.Operator):
	bl_idname = "pose.jueg_dummy"
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
	bpy.utils.register_class(POSE_OT_jueg_ops_add)
	bpy.utils.register_class(POSE_OT_jueg_ops_remove) 
	bpy.utils.register_class(POSE_OT_jueg_operator_move)
	bpy.utils.register_class(POSE_OT_jueg_ExportOps)
	bpy.utils.register_class(POSE_OT_jueg_ImportOps)
	bpy.utils.register_class(POSE_OT_jueg_dummy)
	
def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_ops_add)
	bpy.utils.unregister_class(POSE_OT_jueg_ops_remove) 
	bpy.utils.unregister_class(POSE_OT_jueg_operator_move)
	bpy.utils.unregister_class(POSE_OT_jueg_ExportOps)
	bpy.utils.unregister_class(POSE_OT_jueg_ImportOps)
	bpy.utils.unregister_class(POSE_OT_jueg_dummy)
