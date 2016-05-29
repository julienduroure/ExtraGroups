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

from .globals import *

class POSE_PT_jueg_grouptype(bpy.types.Panel):
	bl_label = "Group Type"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Extra Groups"
	
	@classmethod
	def poll(self, context):
		armature = context.object
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE'
				and addonpref().multitype == True 
				and len(armature.jueg_extragroups_ops) != 0)
				
	def draw(self, context):
		layout = self.layout
		armature = context.object
		
		row = layout.row()
		row.template_list("POSE_UL_jueg_grouptype", "", armature, "jueg_grouptypelist", armature, "jueg_active_grouptype")
		
		col = row.column()
		row = col.column(align=True)
		row.operator("pose.jueg_grouptype_add", icon="ZOOMIN", text="")
		row.operator("pose.jueg_grouptype_remove", icon="ZOOMOUT", text="")
		row = col.column(align=True)
		row.separator()
		row.operator("pose.jueg_grouptype_move", icon='TRIA_UP', text="").direction = 'UP'
		row.operator("pose.jueg_grouptype_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
		if len(armature.jueg_grouptypelist) == 0:
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
		pcoll = bpy.extragroups_icons["bonegroup"]
		
		if len(armature.jueg_grouptypelist) > 0:
		
			jueg_active_grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype]

			row = layout.row()
			row.template_list("POSE_UL_jueg_bonegroup", "", jueg_active_grouptype, "group_ids", jueg_active_grouptype, "active_bonegroup", rows=6)

			col = row.column()
			row = col.column(align=True)
			row.operator("pose.jueg_bonegroup_add", icon="ZOOMIN", text="").dyn_selection = False
			row.operator("pose.bonegroup_remove", icon="ZOOMOUT", text="")
		
			row = col.column(align=True)
			row.separator()
			row.operator("pose.jueg_bonegroup_move", icon='TRIA_UP', text="").direction = 'UP'
			row.operator("pose.jueg_bonegroup_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
			if len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids) == 0:
				row.enabled = False
		
			if armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_bonegroup].current_selection == False:
				row = col.column(align=True)
				row.separator()
				row.operator("pose.jueg_bonegroup_assign", icon_value=pcoll["bonegroup_assign"].icon_id, text="")
				row.operator("pose.jueg_bonegroup_bone_remove", icon_value=pcoll["bonegroup_remove"].icon_id, text="")
		
				if len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids) == 0:
					row.enabled = False

			if check_if_current_selection_exists() == False:
				row = layout.row()
				row.operator("pose.jueg_bonegroup_add", text="Add Dynamic Selection").dyn_selection = True
			
		else:
			#Not initialized yet. Display "false" List and + operator to be able to create data
			row = layout.row()
			row.template_list("POSE_UL_jueg_grouptype", "", armature, "jueg_grouptypelist", armature, "jueg_active_grouptype")
		
			col = row.column()
			row = col.column(align=True)
			row.operator("pose.jueg_bonegroup_add", icon="ZOOMIN", text="").dyn_selection = False

		
class POSE_PT_jueg_opslist(bpy.types.Panel):
	bl_label = "Operator List"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Extra Groups"
	
	@classmethod
	def poll(self, context):
		armature = context.object
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE' 
				and len(context.active_object.jueg_grouptypelist) > 0 
				and len(armature.jueg_extragroups_ops) != 0
				and addonpref().edit_mode == True)
				
	def draw(self, context):
		layout = self.layout
		armature = context.object
		
		jueg_active_grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype]
		
		row = layout.row()
		row.template_list("POSE_UL_jueg_opslist", "", jueg_active_grouptype, "ops_display", jueg_active_grouptype, "active_ops")
		
		col = row.column()
		row = col.column(align=True)
		sub = row.row(align=True)
		sub.operator("pose.jueg_ops_add", icon="ZOOMIN", text="")
		sub = row.row(align=True)
		sub.operator("pose.jueg_ops_remove", icon="ZOOMOUT", text="")
		sub.enabled = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].user_defined
		row = col.column(align=True)
		row.separator()
		row.operator("pose.jueg_operator_move", icon='TRIA_UP', text="").direction = 'UP'
		row.operator("pose.jueg_operator_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
		if len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display) == 0:
			row.enabled = False
				
class POSE_PT_jueg_opsdetail(bpy.types.Panel):
	bl_label = "Operator Detail"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Extra Groups"
	
	@classmethod
	def poll(self, context):
		armature = context.object
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE'  
				and len(context.active_object.jueg_grouptypelist) > 0
				and len(context.active_object.jueg_grouptypelist[context.active_object.jueg_active_grouptype].ops_display) > 0
				and len(armature.jueg_extragroups_ops) != 0 
				and addonpref().edit_mode == True)
				
	def draw(self, context):
		layout = self.layout
		armature = context.object

		jueg_active_grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype]
		ops = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == jueg_active_grouptype.ops_display[jueg_active_grouptype.active_ops].id][0]
		ops_display = jueg_active_grouptype.ops_display[jueg_active_grouptype.active_ops]
		
		row_global = layout.row()
		box = row_global.box()
		row = box.row()
		row.prop(ops, "name", text="Name")
		row = box.row()
		row.prop(ops, "ops_type", text="Type")
		row.enabled = ops.user_defined
		row = box.row()
		row.prop(ops, "ops_exe", text="Operator")
		row.enabled = ops.user_defined
		row_global = layout.row()
		box = row_global.box()
		row = box.row()
		col = row.column()
		row_ = col.row()
		if ops.icons.icon_on.expand == False:
			row_.prop(ops.icons.icon_on, "expand", icon="TRIA_RIGHT", icon_only=True, emboss=False)
			row_.prop(ops, "icon_on", text="Icon On")
			col = row.column()
			row_ = col.row()
			try:
				row_.label(text="", icon=ops.icon_on)
			except:
				row_.label(text="", icon='QUESTION')
		else:
			row_.prop(ops.icons.icon_on, "expand", icon="TRIA_DOWN", icon_only=True, emboss=False)
			row_.prop(ops.icons.icon_on, "search", icon="VIEWZOOM", text="")
			row_ = col.row()
			if len(get_filter_icons(ops.icons.icon_on.search)) == 0:
				row_.label("No icons found")
			else:
				for i, icon in enumerate(get_filter_icons(ops.icons.icon_on.search)):
					if i % ops.icons.amount == 0:
						row_ = col.row()
					op = row_.operator("jueg.select_icon", text=" ", icon=icon, emboss=False)
					op.icon_type = "icon_on"
					op.icon = icon
				for i in range(ops.icons.amount - len(get_filter_icons(ops.icons.icon_on.search)) % ops.icons.amount):
					row_.label("")
		if ops.ops_type == "BOOL":
			row = box.row()
			col = row.column()
			row_ = col.row()
			if ops.icons.icon_off.expand == False:
				row_.prop(ops.icons.icon_off, "expand", icon="TRIA_RIGHT", icon_only=True, emboss=False)
				row_.prop(ops, "icon_off", text="Icon Off")
				col = row.column()
				row_ = col.row()
				try:
					row_.label(text="", icon=ops.icon_off)
				except:
					row_.label(text="", icon='QUESTION')
			else:
				row_.prop(ops.icons.icon_off, "expand", icon="TRIA_DOWN", icon_only=True, emboss=False)
				row_.prop(ops.icons.icon_off, "search", icon="VIEWZOOM", text="")
				row_ = col.row()
				if len(get_filter_icons(ops.icons.icon_off.search)) == 0:
					row_.label("No icons found")
				else:
					for i, icon in enumerate(get_filter_icons(ops.icons.icon_off.search)):
						if i % ops.icons.amount == 0:
							row_ = col.row()
						op = row_.operator("jueg.select_icon", text=" ", icon=icon, emboss=False)
						op.icon_type = "icon_off"
						op.icon = icon
					for i in range(ops.icons.amount - len(get_filter_icons(ops.icons.icon_off.search)) % ops.icons.amount):
						row_.label("")
		row_global = layout.row()
		row_global.prop(ops, "ok_for_current_sel", text="Enabled for 'Dynamic Selection'")
		row_global.enabled = ops.user_defined
		if ops.user_defined == True:
			row_global = layout.row()
			file_ = ops.id + ".py"
			if file_ in bpy.data.texts:
				row_global.operator("pose.jueg_text_display", text="Edit Source").text_id = file_
			else:
				row_global.label("Warning : Text doesn't exist anymore", icon="ERROR")
		
class POSE_PT_jueg_reloaddata(bpy.types.Panel):
	bl_label = "Reload Data"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Extra Groups"
	
	@classmethod
	def poll(self, context):
		armature = context.active_object
		try:
			linked, filepath = lib_proxy_armature()
		except:
			linked = False

		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE'  
				and addonpref().edit_mode == True
				and linked == True)
				
	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("pose.jueg_reload_linked_data", text="Reload data from library")
			
def register():
	bpy.utils.register_class(POSE_PT_jueg_grouptype) 
	bpy.utils.register_class(POSE_PT_jueg_bonegroup) 
	bpy.utils.register_class(POSE_PT_jueg_opslist)
	bpy.utils.register_class(POSE_PT_jueg_opsdetail)
	bpy.utils.register_class(POSE_PT_jueg_reloaddata)
	
def unregister():
	bpy.utils.unregister_class(POSE_PT_jueg_grouptype)
	bpy.utils.unregister_class(POSE_PT_jueg_bonegroup)
	bpy.utils.unregister_class(POSE_PT_jueg_opslist)
	bpy.utils.unregister_class(POSE_PT_jueg_opsdetail)
	bpy.utils.unregister_class(POSE_PT_jueg_reloaddata)
