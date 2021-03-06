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
#	Copyright 2016-2021 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################
import bpy
from ..utils import *

from bpy.props import (
	BoolProperty,
	StringProperty,
	IntProperty,
)

from bpy.types import (
	Operator,
)

class POSE_OT_jueg_motionpath(Operator):
	"""Motion Path (see events for more info)"""
	bl_idname = "pose.jueg_motionpath"
	bl_label = "Motion Path"


	ops_id		 : StringProperty()
	index		 : IntProperty()
	reset_solo   : BoolProperty()
	force_mode   : StringProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def invoke(self, context, event):
		armature = context.object

		# change highlight in UIList
		armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_bonegroup = self.index

		if self.force_mode == '':
			#retrieve event
			internal_event = ""
			if not event.shift and not event.alt and not event.ctrl:
				internal_event = "NONE"
			if event.shift and not event.alt and not event.ctrl:
				internal_event = "SHIFT"
			if not event.shift and event.alt and not event.ctrl:
				internal_event = "ALT"
			if not event.shift and not event.alt and event.ctrl:
				internal_event = "CTRL"
			if event.shift and event.alt and not event.ctrl:
				internal_event = "SHIFT_ALT"
			if event.shift and not event.alt and event.ctrl:
				internal_event = "SHIFT_CTRL"
			if not event.shift and event.alt and event.ctrl:
				internal_event = "CTRL_ALT"
			if event.shift and event.alt and event.ctrl:
				internal_event = "CTRL_SHIFT_ALT"

			#retrieve events
			found = False
			events = []
			use_event = False
			for ops in armature.jueg_extragroups_ops:
				if ops.id == self.ops_id:
					events = [ev for ev in ops.events if ev.active == True]
					use_event = ops.event_manage
					found = True

			if found == False:
				self.report({'ERROR'}, "Error retrieving events")
				return {'CANCELLED'}

			#retrieve mode used
			mode = ""
			solo = False
			if use_event == True:
				for ev in events:
					if ev.event == internal_event:
						mode = ev.mode
						solo = ev.solo
						mirror = ev.mirror
			else:
				mode = "JUEG_DUMMY"

			if mode == "":
				self.report({'ERROR'}, "No event assigned")
				return {'CANCELLED'}

			if mode == "JUEG_DUMMY":
				mode = ""
				mirror = False
		else:
			mode = self.force_mode
			for ops in armature.jueg_extragroups_ops:
				if ops.id == self.ops_id:
					events = [ev for ev in ops.events if ev.active == True]
					break
			for ev in events:
				if ev.mode == mode:
					solo = ev.solo
					mirror = ev.mirror

		#retrieve on_off
		on_off = False
		found = False
		for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].on_off:
			if ops.id == self.ops_id:
				on_off = ops.on_off
				found = True


		if found == False:
			self.report({'ERROR'}, "Error retrieving data on_off")
			return {'CANCELLED'}

		solo_already = False
		found = False
		#add solo data if not exist already
		if len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo) == 0:
			for ops in armature.jueg_extragroups_ops:
				new_ = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo.add()
				new_.id = ops.id
				new_.on_off = False

		for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo:
			if ops.id == self.ops_id:
				solo_already = ops.on_off
				found = True

		if found == False:
			self.report({'ERROR'}, "Error retrieving data Solo")
			return {'CANCELLED'}

		if mirror == True and len(addonpref().xx_sides) == 0:
			init_sides(context)

		current_selection = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].current_selection
		if current_selection == False:
			bones = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids
		else:
			bones = []
			for bone in armature.pose.bones:
				if bone.bone.select == True:
					bones.append(bone)

		if mirror == True:
			bones = [armature.pose.bones[get_symm_name(bone.name)] for bone in bones ]

		#No Before

		to_deleted = []
		idx = -1
		for bone in bones:
			idx = idx + 1
			if bone.name not in armature.data.bones:
				to_deleted.append(idx)
				continue
################################## Insert your code here ##########################
		# Store current selection
		current_selection = []
		for bone in armature.data.bones:
			if bone.select == True:
				current_selection.append(bone.name)
				bone.select = False

		# Store current active bone
		current_active_bone_name = armature.data.bones.active.name

		#Select all bones of group
		for bone in bones:
			armature.data.bones[bone.name].select = True
			if mode == "UPDATE" or mode == "UPDATE_MIRROR":
				# Set active bone --> One (random) of group
				armature.data.bones.active = armature.data.bones[bone.name]
###################################################################################
		if (mode == "ADD" or mode == "ADD_MIRROR") and on_off == True:
			bpy.ops.pose.paths_calculate(start_frame=bpy.context.scene.frame_start, end_frame=bpy.context.scene.frame_end, bake_location='HEADS')
		if (mode == "ADD" or mode == "ADD_MIRROR") and on_off == False:
			bpy.ops.pose.paths_clear()
		if (mode == "UPDATE" or mode == "UPDATE_MIRROR") and on_off == False:
			bpy.ops.pose.paths_update()
###################################################################################
		#Restore selection
		for bone in armature.data.bones:
			bone.select = False
			if bone.name in current_selection:
				bone.select = True

		# restore active bone
		armature.data.bones.active = armature.data.bones[current_active_bone_name]
###################################################################################

		if len(to_deleted) > 0:
			for i in to_deleted:
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids.remove(i)

		if mode == "ADD" or mode == "ADD_MIRROR":
			for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].on_off:
				if ops.id == self.ops_id:
					if solo == False:
						ops.on_off = not ops.on_off
					else:
						ops.on_off = True # Inversed solo ?

			#special for motion path
			if on_off == False:
				idx = 0
				need_to_deselect = True
				for bonegroup in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
					for ops in bonegroup.on_off:
						if ops.id == self.ops_id:
							if ops.on_off == False:
								# All motion path are disabled by ops, need to reactivate all already active one.
								if idx != self.index:
									if ops.on_off == False:
										# deselect current
										if need_to_deselect == True:
											need_to_deselect = False
											for bone in armature.data.bones:
												if bone.select == True:
													bone.select = False

										# select bone from group
										for bone in bonegroup.bone_ids:
											armature.data.bones[bone.name].select = True

										# apply ops
										bpy.ops.pose.paths_calculate(start_frame=bpy.context.scene.frame_start, end_frame=bpy.context.scene.frame_end, bake_location='HEADS')

										# deselect
										for bone in bones:
											armature.data.bones[bone.name].select = False
					idx = idx + 1

				if need_to_deselect == False:
					# Some groups were re-activate : need to reselect right bones
					for bone in armature.data.bones:
						bone.select = False
						if bone.name in current_selection:
							bone.select = True


		return {'FINISHED'}
