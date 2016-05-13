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


class POSE_OT_jueg_Jueg_BoneGroup_assign(bpy.types.Operator):
	"""Add selected bones to current group"""
	bl_idname = "pose.jueg_Jueg_BoneGroup_assign"
	bl_label = "Assign Bones to Bone Group"
	bl_options = {'REGISTER'}	
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')   
				
	def execute(self, context):
		armature = context.object
		pose = armature.pose
		
		for bone in pose.bones:
				if (bone.bone.select):
					if bone.name not in [b_.name for b_ in armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].group_ids[armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup].bone_ids ]:
						bone_id = armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].group_ids[armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup].bone_ids.add()
						bone_id.name = bone.name
						
		return {'FINISHED'}
	
class POSE_OT_jueg_Jueg_BoneGroup_bone_remove(bpy.types.Operator):
	"""Remove selected bones from current group"""
	bl_idname = "pose.jueg_Jueg_BoneGroup_bone_remove"
	bl_label = "Remove Bones from Bone Group"
	bl_options = {'REGISTER'}	
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')   
				
	def execute(self, context):
		armature = context.object
		pose = armature.pose
		
		for bone in pose.bones:
				if (bone.bone.select):
					idx = 0
					for b_ in armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].group_ids[armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup].bone_ids:
						if bone.name == b_.name:
							armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].group_ids[armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup].bone_ids.remove(idx)
							break
						idx = idx + 1  
		return {'FINISHED'}

class POSE_OT_jueg_Jueg_BoneGroup_add(bpy.types.Operator):
	"""Add a new group, and assign selected bones"""
	bl_idname = "pose.jueg_Jueg_BoneGroup_add"
	bl_label = "Add Bone Group"
	bl_options = {'REGISTER'}
	
	dyn_selection = bpy.props.BoolProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')		

	def execute(self, context):
		keep = False
		armature = context.object
		pose = armature.pose
		
		
		
		Jueg_GroupType = armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].group_ids

		Jueg_BoneGroup = Jueg_GroupType.add()
		Jueg_BoneGroup.name = "Group.%d" % len(Jueg_GroupType)
		armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup = len(Jueg_GroupType) - 1
		if self.dyn_selection == False:
			for bone in pose.bones:
				if (bone.bone.select):
					bone_id = Jueg_BoneGroup.bone_ids.add()
					bone_id.name = bone.name
					keep = True
		else:
			Jueg_BoneGroup.current_selection = True
			Jueg_BoneGroup.name = "Current Selection"
			keep = True

		#add on / off for each ops
		on_off   = Jueg_BoneGroup.on_off
		ops_list = armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].ops_display
		for ops in ops_list:
			new_ = on_off.add()
			new_.id = ops.id
			new_.on_off = True

		if (not keep):
			Jueg_GroupType.remove(armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup)
			len_ = len(Jueg_GroupType)
			if (armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup > (len_ - 1) and len_ > 0):
				armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup = len(Jueg_GroupType) - 1
			return {'CANCELLED'}

		return {'FINISHED'}
	
class POSE_OT_jueg_Jueg_BoneGroup_move(bpy.types.Operator):
	"""Move group up or down in the list"""
	bl_idname = "pose.jueg_Jueg_BoneGroup_move"
	bl_label = "Move Bone Group"
	bl_options = {'REGISTER'}
	
	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')		

	def execute(self, context):
		armature = context.object
		index	= armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup
		
		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index
			
		if new_index < len(armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].group_ids) and new_index >= 0:
			armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].group_ids.move(index, new_index)
			armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup = new_index
		
		return {'FINISHED'}
		
class POSE_OT_jueg_Jueg_BoneGroup_remove(bpy.types.Operator):
	"""Remove group"""
	bl_idname = "pose.Jueg_BoneGroup_remove"
	bl_label = "Remove Bone Group"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object

		armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].group_ids.remove(armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup)
		len_ = len(armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].group_ids)
		if (armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup > (len_ - 1) and len_ > 0):
			armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].active_Jueg_BoneGroup = len(armature.Jueg_GroupTypelist[armature.active_Jueg_GroupType].group_ids) - 1
		return {'FINISHED'}
		
def register():
	bpy.utils.register_class(POSE_OT_jueg_Jueg_BoneGroup_add)
	bpy.utils.register_class(POSE_OT_jueg_Jueg_BoneGroup_remove) 
	bpy.utils.register_class(POSE_OT_jueg_Jueg_BoneGroup_move)
	bpy.utils.register_class(POSE_OT_jueg_Jueg_BoneGroup_assign)
	bpy.utils.register_class(POSE_OT_jueg_Jueg_BoneGroup_bone_remove)
	
def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_Jueg_BoneGroup_add)
	bpy.utils.unregister_class(POSE_OT_jueg_Jueg_BoneGroup_remove)
	bpy.utils.unregister_class(POSE_OT_jueg_Jueg_BoneGroup_move)
	bpy.utils.unregister_class(POSE_OT_jueg_Jueg_BoneGroup_assign)
	bpy.utils.unregister_class(POSE_OT_jueg_Jueg_BoneGroup_bone_remove)
