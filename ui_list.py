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

class POSE_UL_grouptype(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name", text="", emboss=False)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			
class POSE_UL_template(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name", text="", emboss=False)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			
class POSE_UL_bonegroup(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		armature = context.object
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name", text="", emboss=False)
				
			#loop on ops from this group type
			for ops in armature.grouptypelist[armature.active_grouptype].ops_ids:
				try:
					if ops.display == False:
						continue
					#retrieve on_off
					for on_off_item in armature.grouptypelist[armature.active_grouptype].group_ids[index].on_off:
					
						if on_off_item.id == ops.id:
							on_off = on_off_item.on_off
					if ops.ops_type == 'EXE': 										#No switchable icon
						icon = ops.icon_on
						if icon == "":
							icon ="QUESTION" 										#if no icon, set QUESION_ICON
					else: 															#switchable icon
						icon = ops.icon_on if on_off == True else ops.icon_off 		#set icon, depend on on_off
						if icon == "":
							icon ="QUESTION" 										#if no icon, set QUESION_ICON
					if item.current_selection == True and ops.ok_for_current_sel == False:
						icon = 'BLANK1'												#Display nothing if ops is not enabled for current selection
						op = layout.operator("pose.dummy", text='', emboss=False, icon=icon)
					else:
						op = layout.operator(ops.ops_exe, text='', emboss=False, icon=icon)
						op.ops_id = ops.id
						op.index	= index
				except:
					icon = 'ERROR' 													#In case of error, display warning error icon
					op = layout.operator("pose.dummy", text='', emboss=False, icon=icon)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			
class POSE_UL_opslist(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name", text="", emboss=False)
			if item.display == True:
				icon = "CHECKBOX_HLT"			
			else:
				icon = "CHECKBOX_DEHLT"
			layout.prop(item, "display", text="", emboss=False,icon=icon)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			
def register():
	bpy.utils.register_class(POSE_UL_grouptype)
	bpy.utils.register_class(POSE_UL_bonegroup) 
	bpy.utils.register_class(POSE_UL_opslist) 
	bpy.utils.register_class(POSE_UL_template)
	
def unregister():
	bpy.utils.unregister_class(POSE_UL_grouptype)
	bpy.utils.unregister_class(POSE_UL_bonegroup)
	bpy.utils.unregister_class(POSE_UL_opslist)
	bpy.utils.unregister_class(POSE_UL_template)
