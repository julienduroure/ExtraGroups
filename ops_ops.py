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
			
		if new_index < len(armature.grouptypelist[armature.active_grouptype].ops_ids) and new_index >= 0:
			armature.grouptypelist[armature.active_grouptype].ops_ids.move(index, new_index)
			armature.grouptypelist[armature.active_grouptype].active_ops = new_index
		
		return {'FINISHED'}
		
class POSE_OT_ops_add(bpy.types.Operator):
	"""Add a new operator"""
	bl_idname = "pose.ops_add"
	bl_label = "Add Ops"
	bl_options = {'REGISTER'}
	
	from_template = bpy.props.BoolProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')		

	def execute(self, context):
		keep = False
		armature = context.object
		
		if len(armature.grouptypelist) > 0:
			opslist = armature.grouptypelist[armature.active_grouptype].ops_ids

			ops = opslist.add()
			ops.id   = uuid.uuid4().hex
			if self.from_template == True:
				#retrieve current template
				template = context.scene.templatelist[context.scene.active_template]
				ops.name = template.name
				ops.ops_exe = template.ops_exe
				ops.ops_type = template.ops_type
				ops.icon_on	= template.icon_on
				ops.icon_off   = template.icon_off
				ops.from_template = True
				ops.ok_for_current_sel = template.ok_for_current_sel
				ops.display = False
			else:
				ops.name = "Ops.%d" % len(opslist)
				ops.ops_exe = "pose.ope_" + ops.id
				ops.from_template = False
				ops.ops_type = 'EXE'
				ops.display = False
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
			armature.grouptypelist[armature.active_grouptype].active_ops = len(opslist) - 1
		
			#now add on/off for each existing bone group of this type
			bonegroups = armature.grouptypelist[armature.active_grouptype].group_ids
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
		
		if len(armature.grouptypelist) > 0 and len(armature.grouptypelist[armature.active_grouptype].ops_ids) > 0:
			if armature.grouptypelist[armature.active_grouptype].ops_ids[armature.grouptypelist[armature.active_grouptype].active_ops].from_template == False:
				if context.scene.bonegroup_textremove == True:
					file_ = armature.grouptypelist[armature.active_grouptype].ops_ids[armature.grouptypelist[armature.active_grouptype].active_ops].id + ".py"
					bpy.ops.text.text_remove(text_id=file_)

			armature.grouptypelist[armature.active_grouptype].ops_ids.remove(armature.grouptypelist[armature.active_grouptype].active_ops)
			len_ = len(armature.grouptypelist[armature.active_grouptype].ops_ids)
			if (armature.grouptypelist[armature.active_grouptype].active_ops > (len_ - 1) and len_ > 0):
				armature.grouptypelist[armature.active_grouptype].active_ops = len(armature.grouptypelist[armature.active_grouptype].ops_ids) - 1
		return {'FINISHED'}
		
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
	bpy.utils.register_class(POSE_OT_dummy)
	
def unregister():
	bpy.utils.unregister_class(POSE_OT_ops_add)
	bpy.utils.unregister_class(POSE_OT_ops_remove) 
	bpy.utils.unregister_class(POSE_OT_operator_move)
	bpy.utils.unregister_class(POSE_OT_dummy)
