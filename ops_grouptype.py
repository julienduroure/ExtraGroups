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

class POSE_OT_grouptype_move(bpy.types.Operator):
	"""Move group type up or down in the list"""
	bl_idname = "pose.grouptype_move"
	bl_label = "Move Group Type"
	bl_options = {'REGISTER'}
	
	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')		

	def execute(self, context):
		armature = context.object
		index	= armature.active_grouptype
		
		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index
			
		if new_index < len(armature.grouptypelist) and new_index >= 0:
			armature.grouptypelist.move(index, new_index)
			armature.active_grouptype = new_index
		
		return {'FINISHED'}
		
class POSE_OT_grouptype_add(bpy.types.Operator):
	"""Add a new group type"""
	bl_idname = "pose.grouptype_add"
	bl_label = "Add Group Type"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')
				
	def execute(self, context):
		armature = context.object
		
		grouptype = armature.grouptypelist.add()
		grouptype.name = "GroupType.%d" % len(armature.grouptypelist)
		armature.active_grouptype = len(armature.grouptypelist) - 1
		
		return {'FINISHED'}
	
class POSE_OT_grouptype_remove(bpy.types.Operator):
	"""Remove the current group type"""
	bl_idname = "pose.grouptype_remove"
	bl_label = "Remove Group Type"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')
				
	def execute(self, context):
		armature = context.object	 
		
		armature.grouptypelist.remove(armature.active_grouptype)
		len_ = len(armature.grouptypelist)
		if (armature.active_grouptype > (len_ - 1) and len_ > 0):
			armature.active_grouptype = len(armature.grouptypelist) - 1
		return {'FINISHED'}   
	
def register():
	bpy.utils.register_class(POSE_OT_grouptype_add)
	bpy.utils.register_class(POSE_OT_grouptype_remove) 
	bpy.utils.register_class(POSE_OT_grouptype_move)
		
def unregister():
	bpy.utils.unregister_class(POSE_OT_grouptype_add)
	bpy.utils.unregister_class(POSE_OT_grouptype_remove) 
	bpy.utils.unregister_class(POSE_OT_grouptype_move) 
