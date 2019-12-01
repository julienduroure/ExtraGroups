#
# ExtraGroups is part of BleRiFa. http://BleRiFa.com
#
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
#	Copyright 2016-2017 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################
import bpy
from .globs import *
from .utils import *

class POSE_UL_jueg_grouptype(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name", text="", emboss=False)

		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'

class POSE_UL_jueg_events(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		armature = context.object
		jueg_active_grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype]
		ops = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == jueg_active_grouptype.ops_display[jueg_active_grouptype.active_ops].id][0]
		user_defined = ops.user_defined

		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			if user_defined == False:
				layout.label(text=item.label, translate=False)
			else:
				layout.prop(item, "label", text="", emboss=False)

		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'

class POSE_UL_jueg_bonegroup(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

		armature = context.object
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			if addonpref().use_color == False:
				row = layout.row()
			else:
				row = layout.row()
				sub = row.row()
				sub.prop(item, "color", text="")
				sub.enabled = addonpref().edit_mode

			if addonpref().edit_mode == False and armature.jueg_clickable_name_data.name_clickable == True:
				# check if ops is available for current selection

				row.operator_context = [ops_ for ops_ in armature.jueg_extragroups_ops if ops_.id == armature.jueg_clickable_name_data.clickable_ops][0].ops_context
				op = row.operator([ops_ for ops_ in armature.jueg_extragroups_ops if ops_.id == armature.jueg_clickable_name_data.clickable_ops][0].ops_exe, item.name, emboss=False)
				op.index = index
				op.ops_id = armature.jueg_clickable_name_data.clickable_ops
				if armature.jueg_clickable_name_data.clickable_events_on == False:
					if [ops_ for ops_ in armature.jueg_extragroups_ops if ops_.id == armature.jueg_clickable_name_data.clickable_ops][0].event_manage == True:
						op.force_mode = armature.jueg_clickable_name_data.clickable_mode
					op.reset_solo = False
				else:
					ops = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_clickable_name_data.clickable_ops][0]

					#retrieve if solo mode exist
					solo_somewhere  = False
					solo_me         = False
					for solo_item in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[index].solo:
						if solo_item.id == ops.id:
							solo_me  = solo_item.on_off

					index_group = 0
					for other_groups in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
						if index_group != index:
							for solo_other in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[index_group].solo:
								if solo_other.id == ops.id:
									if solo_other.on_off == True:
										solo_somewhere = True
						index_group = index_group + 1

					if solo_somewhere == False or (solo_somewhere == True and solo_me == True):
						op.reset_solo = False
					else:
						op.reset_solo = True
					op.force_mode = ''

			else:
				row.prop(item, "name", text="", emboss=False)

			#loop on ops from this group type
			for ope in armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display:
				ops = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == ope.id][0]
				try:
					if ope.display == False:
						continue
					#retrieve on_off
					for on_off_item in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[index].on_off:
						if on_off_item.id == ops.id:
							on_off = on_off_item.on_off

					#retrieve if solo mode exist
					solo_somewhere  = False
					solo_me         = False
					for solo_item in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[index].solo:
						if solo_item.id == ops.id:
							solo_me  = solo_item.on_off

					index_group = 0
					for other_groups in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
						if index_group != index:
							for solo_other in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[index_group].solo:
								if solo_other.id == ops.id:
									if solo_other.on_off == True:
										solo_somewhere = True
						index_group = index_group + 1

					if ops.ops_type == 'EXE': 										#No switchable icon
						icon = ops.icon_on
						if icon == "":
							icon ="QUESTION" 										#if no icon, set QUESION_ICON
					else: 															#switchable icon
						if solo_somewhere == False:
							icon = ops.icon_on if on_off == True else ops.icon_off 		#set icon, depend on on_off
						else:
							if solo_me == True:
								icon = ops.icon_on if on_off == True else ops.icon_off 		#set icon, depend on on_off
							else:
								icon = 'SOLO_OFF'
						if icon == "":
							icon ="QUESTION" 										#if no icon, set QUESION_ICON
					if item.current_selection == True and ops.ok_for_current_sel == False:
						icon = 'BLANK1'												#Display nothing if ops is not enabled for current selection
						row.operator_context = "EXEC_DEFAULT"
						op = row.operator("pose.jueg_dummy", text='', emboss=False, icon=icon)
					else:
						row.operator_context = ops.ops_context
						op = row.operator(ops.ops_exe, text='', emboss=False, icon=icon)
						op.ops_id = ops.id
						op.index	= index
						if solo_somewhere == False or (solo_somewhere == True and solo_me == True):
							op.reset_solo = False
						else:
							op.reset_solo = True
						op.force_mode = ''

				except:
					icon = 'ERROR' 													#In case of error, display warning error icon
					row.operator_context = "EXEC_DEFAULT"
					op = row.operator("pose.jueg_dummy", text='', emboss=False, icon=icon)

		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'

class POSE_UL_jueg_opslist(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

		armature = context.object
		jueg_active_grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype]
		ops = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == item.id][0]
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			if ops.user_defined == True:
				icon = "POSE_DATA"
			else:
				icon = "BLANK1"
			layout.operator("pose.jueg_dummy", text='', emboss=False, icon=icon)
			layout.prop(ops, "name", text="", emboss=False)
			if item.display == True:
				icon = "CHECKBOX_HLT"
			else:
				icon = "CHECKBOX_DEHLT"
			layout.prop(item, "display", text="", emboss=False,icon=icon)

		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'

def register():
	bpy.utils.register_class(POSE_UL_jueg_grouptype)
	bpy.utils.register_class(POSE_UL_jueg_bonegroup)
	bpy.utils.register_class(POSE_UL_jueg_opslist)
	bpy.utils.register_class(POSE_UL_jueg_events)

def unregister():
	bpy.utils.unregister_class(POSE_UL_jueg_grouptype)
	bpy.utils.unregister_class(POSE_UL_jueg_bonegroup)
	bpy.utils.unregister_class(POSE_UL_jueg_opslist)
	bpy.utils.unregister_class(POSE_UL_jueg_events)
