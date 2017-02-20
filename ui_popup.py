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

from .globs import *
from .utils import *


class POSE_MT_jueg_popup(bpy.types.Menu):
	bl_idname = "extragroups.popup"
	bl_label  = "ExtraGroups"

	def draw(self, context):
		layout = self.layout
		armature = context.object

		start = True
		split = layout.split()

		for ope in [ope for ope in armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display if ope.display == True]:
			ops = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == ope.id][0]
			if start == True:
				start = False
				col = split.column()
				for item in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
					col.label(item.name)
			col = split.column()

			index = -1
			for item in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
				index = index + 1
				try:
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
						col.operator_context = "EXEC_DEFAULT"
						op = col.operator("pose.jueg_dummy", text='', emboss=False, icon=icon)
					else:
						if solo_somewhere == False:
							col.operator_context = ops.ops_context
							op = col.operator(ops.ops_exe, text='', emboss=False, icon=icon)
							op.ops_id = ops.id
							op.index	= index
						else:
							if solo_me == True:
								col.operator_context = ops.ops_context
								op = col.operator(ops.ops_exe, text='', emboss=False, icon=icon)
								op.ops_id = ops.id
								op.index	= index
							else:
								col.operator_context = "EXEC_DEFAULT"
								op = col.operator("pose.jueg_dummy_solo", text='', emboss=False, icon=icon)
				except:
					icon = 'ERROR' 													#In case of error, display warning error icon
					col.operator_context = "EXEC_DEFAULT"
					op = col.operator("pose.jueg_dummy", text='', emboss=False, icon=icon)


def register():
	bpy.utils.register_class(POSE_MT_jueg_popup)	

def unregister():
	bpy.utils.unregister_class(POSE_MT_jueg_popup)
