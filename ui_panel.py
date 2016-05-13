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

class POSE_PT_jueg_grouptype(bpy.types.Panel):
	bl_label = "Group Type"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Extra Groups"
	
	@classmethod
	def poll(self, context):
		user_preferences = context.user_preferences
		addon_prefs = user_preferences.addons[__package__].preferences

		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE'
				and addon_prefs.multitype == True 
				and len(addon_prefs.extragroups_ops) != 0)
				
	def draw(self, context):
		layout = self.layout
		armature = context.object
		
		row = layout.row()
		row.template_list("POSE_UL_grouptype", "", armature, "grouptypelist", armature, "active_grouptype")
		
		col = row.column()
		row = col.column(align=True)
		row.operator("pose.grouptype_add", icon="ZOOMIN", text="")
		row.operator("pose.grouptype_remove", icon="ZOOMOUT", text="")
		row = col.column(align=True)
		row.separator()
		row.operator("pose.grouptype_move", icon='TRIA_UP', text="").direction = 'UP'
		row.operator("pose.grouptype_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
		if len(armature.grouptypelist) == 0:
			row.enabled = False
		
	  
class POSE_PT_jueg_bonegroup(bpy.types.Panel):
	bl_label = "Bone Group"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Extra Groups"
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')
				
	def draw(self, context):
		layout = self.layout
		armature = context.object
		user_preferences = context.user_preferences
		addon_prefs = user_preferences.addons[__package__].preferences
		pcoll = bpy.extragroups_icons["bonegroup"]
		
		if len(armature.grouptypelist) > 0:
			if len(addon_prefs.extragroups_ops) != 0:
				active_grouptype = armature.grouptypelist[armature.active_grouptype]
		
				row = layout.row()
				row.template_list("POSE_UL_bonegroup", "", active_grouptype, "group_ids", active_grouptype, "active_bonegroup", rows=6)
		
				col = row.column()
				row = col.column(align=True)
				row.operator("pose.jueg_bonegroup_add", icon="ZOOMIN", text="").dyn_selection = False
				row.operator("pose.bonegroup_remove", icon="ZOOMOUT", text="")
			
				row = col.column(align=True)
				row.separator()
				row.operator("pose.jueg_bonegroup_move", icon='TRIA_UP', text="").direction = 'UP'
				row.operator("pose.jueg_bonegroup_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
				if len(armature.grouptypelist[armature.active_grouptype].group_ids) == 0:
					row.enabled = False
			
				row = col.column(align=True)
				row.separator()
				row.operator("pose.jueg_bonegroup_assign", icon_value=pcoll["bonegroup_assign"].icon_id, text="")
				row.operator("pose.jueg_bonegroup_bone_remove", icon_value=pcoll["bonegroup_remove"].icon_id, text="")
			
				if len(armature.grouptypelist[armature.active_grouptype].group_ids) == 0:
					row.enabled = False
		
				row = layout.row()
				row.operator("pose.jueg_bonegroup_add", text="Add Dynamic Selection").dyn_selection = True

			else:
				row = layout.row()
				row.operator("pose.extragroups_reload", text="Reload Extragroups data")
		else:
			row = layout.row()
			row.operator("pose.grouptype_add", text="Init Bone Groups for this Rig")

			
		
		
class POSE_PT_jueg_opslist(bpy.types.Panel):
	bl_label = "Operator List"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	
	@classmethod
	def poll(self, context):
		user_preferences = context.user_preferences
		addon_prefs = user_preferences.addons[__package__].preferences
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE' 
				and len(context.active_object.grouptypelist) > 0 
				and len(addon_prefs.extragroups_ops) != 0)
				
	def draw(self, context):
		layout = self.layout
		armature = context.object
		user_preferences = bpy.context.user_preferences
		addon_prefs = user_preferences.addons[__package__].preferences	
		
		active_grouptype = armature.grouptypelist[armature.active_grouptype]
		
		row = layout.row()
		row.template_list("POSE_UL_opslist", "", active_grouptype, "ops_display", active_grouptype, "active_ops")
		
		col = row.column()
		row = col.column(align=True)
		sub = row.row(align=True)
		sub.operator("pose.ops_add", icon="ZOOMIN", text="")
		sub = row.row(align=True)
		sub.operator("pose.ops_remove", icon="ZOOMOUT", text="")
		sub.enabled = [e for i,e in enumerate(addon_prefs.extragroups_ops) if e.id == armature.grouptypelist[armature.active_grouptype].ops_display[armature.grouptypelist[armature.active_grouptype].active_ops].id][0].user_defined
		row = col.column(align=True)
		row.separator()
		row.operator("pose.operator_move", icon='TRIA_UP', text="").direction = 'UP'
		row.operator("pose.operator_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
		if len(armature.grouptypelist[armature.active_grouptype].ops_display) == 0:
			row.enabled = False
				
class POSE_PT_jueg_opsdetail(bpy.types.Panel):
	bl_label = "Operator Detail"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	
	@classmethod
	def poll(self, context):
		user_preferences = context.user_preferences
		addon_prefs = user_preferences.addons[__package__].preferences
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE'  
				and len(context.active_object.grouptypelist) > 0
				and len(context.active_object.grouptypelist[context.active_object.active_grouptype].ops_display) > 0
				and len(addon_prefs.extragroups_ops) != 0 )
				
	def draw(self, context):
		layout = self.layout
		armature = context.object
		user_preferences = bpy.context.user_preferences
		addon_prefs = user_preferences.addons[__package__].preferences	

		active_grouptype = armature.grouptypelist[armature.active_grouptype]
		ops = [e for i,e in enumerate(addon_prefs.extragroups_ops) if e.id == active_grouptype.ops_display[active_grouptype.active_ops].id][0]
		ops_display = active_grouptype.ops_display[active_grouptype.active_ops]
		
		row = layout.row()
		row.prop(ops, "name", text="Name")
		row = layout.row()
		row.prop(ops, "ops_type", text="Type")
		row.enabled = ops.user_defined
		row = layout.row()
		row.prop(ops, "ops_exe", text="Operator")
		row.enabled = ops.user_defined
		row = layout.row()
		row.prop(ops, "icon_on", text="Icon On")
		if ops.ops_type == "BOOL":
			row = layout.row()
			row.prop(ops, "icon_off", text="Icon Off")
		row = layout.row()
		row.prop(ops, "ok_for_current_sel", text="Enabled for Current Selection")
		row.enabled = ops.user_defined
		row = layout.row()
		row.prop(ops_display, "display", text="Display")
		if ops.user_defined == True:
			row = layout.row()
			file_ = ops.id + ".py"
			if file_ in bpy.data.texts:
				row.operator("pose.text_display", text="Edit Source").text_id = file_
			else:
				row.label("Warning : Text doesn't exist anymore", icon="ERROR")
		
		
def register():
	bpy.utils.register_class(POSE_PT_jueg_grouptype) 
	bpy.utils.register_class(POSE_PT_jueg_bonegroup) 
	bpy.utils.register_class(POSE_PT_jueg_opslist)
	bpy.utils.register_class(POSE_PT_jueg_opsdetail)
	
def unregister():
	bpy.utils.unregister_class(POSE_PT_jueg_grouptype)
	bpy.utils.unregister_class(POSE_PT_jueg_bonegroup)
	bpy.utils.unregister_class(POSE_PT_jueg_opslist)
	bpy.utils.unregister_class(POSE_PT_jueg_opsdetail) 
