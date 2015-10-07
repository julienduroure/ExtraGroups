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

class POSE_PT_grouptype(bpy.types.Panel):
	bl_label = "Group Type"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Extra Groups"
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE'
				and context.scene.bonegroup_multitype == True)
				
	def draw(self, context):
		layout = self.layout
		armature = context.object
		
		row = layout.row()
		row.label(text="Bones mode", icon='BONE_DATA')
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
		
class POSE_PT_template(bpy.types.Panel):
	bl_label = "Template"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Extra Groups"
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE'
				and context.scene.bonegroup_editmode == True)
				
	def draw(self, context):
		layout = self.layout
		armature = context.object

		row = layout.row()
		row.label(text="Bones mode", icon='BONE_DATA')
		if len(context.scene.templatelist) == 0:
			row = layout.row()
			row.label("Initialisation")
			row = layout.row()
			box = row.box()
			row = box.row()
			row.operator("pose.template_init", text="Init Template List")
			row = box.row()
			row.operator("imp.bonegroup_template", text="Import templates")
			
		else:
		
			row = layout.row()
			row.template_list("POSE_UL_template", "", context.scene, "templatelist", context.scene, "active_template")
		
			col = row.column()
			row = col.column(align=True)
			row.operator("pose.template_add", icon="ZOOMIN", text="")
			row.operator("pose.template_remove", icon="ZOOMOUT", text="")
			row.enabled = context.scene.bonegroup_editmode == True and context.scene.bonegroup_devmode == True and context.scene.bonegroup_adminmode == True
			row = col.column(align=True)
			row.separator()
			row.operator("pose.template_move", icon='TRIA_UP', text="").direction = 'UP'
			row.operator("pose.template_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
			if len(context.scene.templatelist) == 0:
				row.enabled = False
		
			row = layout.row()
			row.operator("pose.ops_add", text="Add to Operator List").from_template = True
			if len(context.scene.templatelist) == 0:		
				row.enabled = False
				
			row = layout.row()
			if context.scene.bonegroup_editmode == True and context.scene.bonegroup_devmode == True and context.scene.bonegroup_adminmode == True:
				row = layout.row()
				row.label("Import / Export")
				row = layout.row()
				box = row.box()
				box.operator("export.bonegroup_template", text="Export Templates")
				row = box.row()
				row.operator("imp.bonegroup_template", text="Import Templates")
			
		
	  
class POSE_PT_bonegroup(bpy.types.Panel):
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
		pcoll = bpy.bonegroup_icons["bonegroup"]
		
		row = layout.row()
		row.label(text="Bones mode", icon='BONE_DATA')
		if len(armature.grouptypelist) > 0:
			active_grouptype = armature.grouptypelist[armature.active_grouptype]
		
			row = layout.row()
			row.template_list("POSE_UL_bonegroup", "", active_grouptype, "group_ids", active_grouptype, "active_bonegroup", rows=6)
		
			col = row.column()
			row = col.column(align=True)
			row.operator("pose.bonegroup_add", icon="ZOOMIN", text="").dyn_selection = False
			row.operator("pose.bonegroup_remove", icon="ZOOMOUT", text="")
			row = col.column(align=True)
			row.separator()
			row.operator("pose.bonegroup_move", icon='TRIA_UP', text="").direction = 'UP'
			row.operator("pose.bonegroup_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
			if len(armature.grouptypelist[armature.active_grouptype].group_ids) == 0:
				row.enabled = False
			row = col.column(align=True)
			row.separator()
			row.operator("pose.bonegroup_assign", icon_value=pcoll["bonegroup_assign"].icon_id, text="")
			row.operator("pose.bonegroup_bone_remove", icon_value=pcoll["bonegroup_remove"].icon_id, text="")
			if len(armature.grouptypelist[armature.active_grouptype].group_ids) == 0:
				row.enabled = False
		
		
			if context.scene.bonegroup_editmode == True:
				row = layout.row()
				row.operator("pose.bonegroup_add", text="Add Dynamic Selection").dyn_selection = True
		else:
			row = layout.row()
			row.operator("pose.grouptype_add", text="Init Bone Groups for this Rig")
		
		
class POSE_PT_opslist(bpy.types.Panel):
	bl_label = "Operator List"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Extra Groups"
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE' and 
				context.scene.bonegroup_editmode == True) 
				
	def draw(self, context):
		layout = self.layout
		armature = context.object
		
		active_grouptype = armature.grouptypelist[armature.active_grouptype]
		
		row = layout.row()
		row.label(text="Bones mode", icon='BONE_DATA')
		row = layout.row()
		row.template_list("POSE_UL_opslist", "", active_grouptype, "ops_ids", active_grouptype, "active_ops")
		
		col = row.column()
		row = col.column(align=True)
		row.operator("pose.ops_add", icon="ZOOMIN", text="").from_template = False
		row.operator("pose.ops_remove", icon="ZOOMOUT", text="")
		row.enabled = context.scene.bonegroup_devmode
		row = col.column(align=True)
		row.separator()
		row.operator("pose.operator_move", icon='TRIA_UP', text="").direction = 'UP'
		row.operator("pose.operator_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
		if len(armature.grouptypelist[armature.active_grouptype].ops_ids) == 0:
			row.enabled = False
		
		
class POSE_PT_opsdetail(bpy.types.Panel):
	bl_label = "Operator Detail"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Extra Groups"
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE' and
				context.scene.bonegroup_editmode == True and
				context.scene.bonegroup_devmode == True 
				and len(context.active_object.grouptypelist[context.active_object.active_grouptype].ops_ids) > 0)
				
	def draw(self, context):
		layout = self.layout
		armature = context.object
		
		active_grouptype = armature.grouptypelist[armature.active_grouptype]
		ops = active_grouptype.ops_ids[active_grouptype.active_ops]
		
		row = layout.row()
		row.prop(ops, "name", text="Name")
		row = layout.row()
		row.prop(ops, "ops_type", text="Type")
		row = layout.row()
		row.prop(ops, "ops_exe", text="Operator")
		if ops.from_template == True:
			row.enabled = False 
		if ops.from_template == True:
			row.enabled = False
		row = layout.row()
		row.prop(ops, "icon_on", text="Icon On")
		if ops.ops_type == "BOOL":
			row = layout.row()
			row.prop(ops, "icon_off", text="Icon Off")
		row = layout.row()
		row.prop(ops, "ok_for_current_sel", text="Enabled for Current Selection")
		if ops.from_template == False:
			row = layout.row()
			file_ = ops.id + ".py"
			row.operator("pose.text_display", text="Edit Source").text_id = file_
		
class POSE_PT_templatedetail(bpy.types.Panel):
	bl_label = "Template Detail"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Extra Groups"
	
	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE' and
				context.scene.bonegroup_editmode == True and 
				context.scene.bonegroup_devmode == True and
				context.scene.bonegroup_adminmode == True
				and len(context.scene.templatelist) > 0)
				
	def draw(self, context):
		layout = self.layout
		armature = context.object
		
		template = context.scene.templatelist[context.scene.active_template]
		
		row = layout.row()
		row.prop(template, "name", text="Name")
		row = layout.row()
		row.prop(template, "ops_type", text="Type")
		row = layout.row()
		row.prop(template, "ops_exe", text="Operator")
		row = layout.row()
		row.prop(template, "icon_on", text="Icon On")
		if template.ops_type == "BOOL":
			row = layout.row()
			row.prop(template, "icon_off", text="Icon Off")   
		row = layout.row()
		row.prop(template, "ok_for_current_sel", text="Enable for Current Selection")
			
class POSE_PT_bonegroup_option(bpy.types.Panel):
	bl_label = "Options"
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
		
		row = layout.row()	
		row.label("Display")
		row = layout.row()
		box = row.box()
		box.prop(context.scene, "bonegroup_multitype", text="Multi Type")
		row = layout.row()
		row = layout.row()
		row.label("Mode")
		row = layout.row()
		box = row.box()
		box.prop(context.scene, "bonegroup_editmode", text="Edit Mode")
		row = box.row()	
		row.prop(context.scene, "bonegroup_devmode", text="Dev Mode")
		row.enabled = context.scene.bonegroup_editmode
		row = box.row()	
		row.prop(context.scene, "bonegroup_adminmode", text="Admin Mode")
		row.enabled = context.scene.bonegroup_devmode
		row = layout.row()	
		row = layout.row()
		row.label("Text Management")
		row = layout.row()
		box = row.box()
		box.prop(context.scene, "bonegroup_textremove", text="Text Remove")
		
		
def register():
	bpy.utils.register_class(POSE_PT_grouptype) 
	bpy.utils.register_class(POSE_PT_bonegroup) 
	bpy.utils.register_class(POSE_PT_opslist)
	bpy.utils.register_class(POSE_PT_opsdetail)
	bpy.utils.register_class(POSE_PT_template) 
	bpy.utils.register_class(POSE_PT_templatedetail) 
	bpy.utils.register_class(POSE_PT_bonegroup_option)
	
def unregister():
	bpy.utils.unregister_class(POSE_PT_grouptype)
	bpy.utils.unregister_class(POSE_PT_bonegroup)
	bpy.utils.unregister_class(POSE_PT_opslist)
	bpy.utils.unregister_class(POSE_PT_opsdetail) 
	bpy.utils.unregister_class(POSE_PT_template)
	bpy.utils.unregister_class(POSE_PT_templatedetail)
	bpy.utils.unregister_class(POSE_PT_bonegroup_option)
