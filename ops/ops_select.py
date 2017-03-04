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
from ..utils import *

from bpy.props import (
	BoolProperty,
	StringProperty,
	IntProperty,
)

from bpy.types import (
	Operator,
)

class POSE_OT_jueg_select(Operator):
	"""Selection (See events for more info)"""
	bl_idname = "pose.jueg_select"
	bl_label = "Magic Select"


	ops_id		 = StringProperty()
	index		 = IntProperty()
	reset_solo   = BoolProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def invoke(self, context, event):
		armature = context.object

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
		else:
			mode = "JUEG_DUMMY"

		if mode == "":
			self.report({'ERROR'}, "No event assigned")
			return {'CANCELLED'}

		if mode == "JUEG_DUMMY":
			mode = ""

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

		#check if this is a classic group or current selection
		current_selection = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].current_selection
		if current_selection == False:
			#retrieve bones from group
			bones = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids
		else:
			#retrieve bones from current selection
			bones = []
			for bone in armature.pose.bones:
				if bone.bone.select == True:
					bones.append(bone)

########################### Before ##############################
		if mode == "SELECT_HIDE_OTHER":
			# Check if solo mode is enabled on visibility ops
			solo_somewhere = False
			for grouptype in armature.jueg_grouptypelist:
				index_group = 0
				for other_groups in grouptype.group_ids:
					for solo_other in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[index_group].solo:
						if solo_other.id == 'b9eac1a0a2fd4dcd94140d05a6a3af86': #visibility
							if solo_other.on_off == True:
								solo_somewhere = True
								break
					index_group = index_group + 1
			if solo_somewhere == True:
				self.report({'ERROR'}, "visibility is on solo mode")
				return {'CANCELLED'}


		if mode == "REPLACE" or mode == "SELECT_HIDE_OTHER":
			for bone in armature.pose.bones:
				bone.bone.select = False
########################### End Before ##########################
		to_delete = []
		idx = -1
		for bone in bones:
			idx = idx + 1
			if bone.name not in armature.data.bones: #If bone no more exists
				to_delete.append(idx)
				continue
################################################################################
			if mode == "REPLACE" or mode == "ADD" or mode == "SELECT_HIDE_OTHER":
				armature.data.bones[bone.name].select = True
			elif mode == "REMOVE":
				armature.data.bones[bone.name].select = False

			if mode == 'SELECT_HIDE_OTHER':
				armature.data.bones[bone.name].hide = False

################################################################################
		#after
		if mode == "SELECT_OPPOSITE":
			for bone in armature.pose.bones:
				if bone.name in [b.name for b in bones]:
					armature.data.bones[bone.name].select = False
				else:
					armature.data.bones[bone.name].select = True

		# Set active bone
		if mode == "REPLACE" or mode == "ADD" or mode == "SELECT_HIDE_OTHER":
			if armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].active_bone != "":
				armature.data.bones.active = armature.data.bones[armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].active_bone]

		# KeyingSet
		if addonpref().use_keyingset == True:
			if mode == "REPLACE":
				if armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].keying != "":
					bpy.context.scene.keying_sets.active_index = bpy.context.scene.keying_sets.find(armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].keying)
				else:
					bpy.context.scene.keying_sets.active_index = -1
			if mode == "ADD":
				if context.scene.keying_sets_all.active:
					merge_keyingset(bpy.context.scene.keying_sets_all.active.bl_label, armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].keying )
					bpy.context.scene.keying_sets.active_index = bpy.context.scene.keying_sets.find(addonpref().internal_keyingset)
			elif mode == "REMOVE":
				self.report({'ERROR'}, "KeyingSet remove is not implemented yet")

		# Select and hide other
		if mode == "SELECT_HIDE_OTHER":
			# Toggle visibility of all other groups
			for grouptype in armature.jueg_grouptypelist:
				cpt_index = 0
				for group in grouptype.group_ids:
					# toogle on_off
					for ops in group.on_off:
						if ops.id == 'b9eac1a0a2fd4dcd94140d05a6a3af86': #visibility
							if cpt_index == self.index and grouptype == armature.jueg_grouptypelist[armature.jueg_active_grouptype]:
								ops.on_off = True
							else:
								ops.on_off = False
					# toogle visibility
					for bone in armature.pose.bones:
						if bone.name not in [bone.name for bone in bones]: # check for bones that are in multiple groups
							armature.data.bones[bone.name].hide = True
					cpt_index = cpt_index + 1

		# Gizmo Management
		if addonpref().use_manipulator:
			manip = []
			if armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].manipulator[0] == True:
				manip.append('TRANSLATE')
			if armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].manipulator[1] == True:
				manip.append('ROTATE')
			if armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].manipulator[2] == True:
				manip.append('SCALE')
			if mode == "REPLACE" or mode == "SELECT_HIDE_OTHER":
				bpy.context.space_data.transform_manipulators = set(manip)
			bpy.context.space_data.transform_orientation = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].orientation


		#delete bones if any
		if len(to_delete) > 0:
			for i in to_delete:
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids.remove(i)

		for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].on_off:
			if ops.id == self.ops_id:
				if solo == False:
					ops.on_off = not ops.on_off
				else:
					ops.on_off = True # Inversed solo ?

		if solo == True:

			#Toggle solo info or reset
			if self.reset_solo == False:
				for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo:
					if ops.id == self.ops_id:
						ops.on_off = not ops.on_off
			else:# move from one solo to another
				index = 0
				for bonegroup in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
					if index != self.index:
						for ops in bonegroup.solo:
							if ops.id == self.ops_id:
								ops.on_off = False
					else:
						for ops in bonegroup.solo:
							if ops.id == self.ops_id:
								ops.on_off = True

					index = index + 1

			#Toggle on_off info for other groups
			if self.reset_solo == False:
				index = 0
				for bonegroup in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
					if index != self.index:
						for ops in bonegroup.on_off:
							if ops.id == self.ops_id:
								if solo_already == False:
									ops.on_off = False
								else:
									ops.on_off = True
					index = index + 1

		else:
			if self.reset_solo == True:
				index = 0
				for bonegroup in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
					if index != self.index:
						for ops in bonegroup.solo:
							if ops.id == self.ops_id:
									ops.on_off = False
					index = index + 1


		return {'FINISHED'}
