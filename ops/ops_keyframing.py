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

class POSE_OT_jueg_keyframing_after_menu(Operator):
	"""Add keyframes"""
	bl_idname = "pose.ope_keyframing_after_menu"
	bl_label = "keyframing"


	index   	 : IntProperty()
	data		 : StringProperty()
	event   	 : StringProperty()
	ops_id       : StringProperty()
	solo         : BoolProperty()
	reset_solo   : BoolProperty()
	mirror       : BoolProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object

		solo = self.solo

		#retrieve on_off
		on_off = False
		found = False
		for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].on_off:
			if ops.id == self.ops_id:
				on_off = ops.on_off
				found = True
				break

		if found == False:
			self.report({'ERROR'}, "Error retrieving data on_off")
			return {'CANCELLED'}

		solo_already = False
		found = False
		#add solo data if not exist already
		if len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo) == 0:
			for ops in armatuer.jueg_extragroups_ops:
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

		if self.mirror == True and len(addonpref().xx_sides) == 0:
			init_sides(context)

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

		if self.mirror == True:
			bones = [armature.pose.bones[get_symm_name(bone.name)] for bone in bones ]


		# store current keyingset if any
		current_keying_set = context.scene.keying_sets.active_index

		to_delete = []
		idx = -1
		for bone in bones:
			idx = idx + 1
			if bone.name not in armature.data.bones: #If bone no more exists
				to_delete.append(idx)
				continue

		# Set Keying set
		bpy.context.scene.keying_sets.active = context.scene.keying_sets_all[self.data]

		# Store current selection
		current_selection = []
		current_hide = {}
		for bone in armature.data.bones:
			if bone.select == True:
				current_selection.append(bone.name)
				bone.select = False

		#Select all bones of group / display bones
		for bone in bones:
			armature.data.bones[bone.name].select = True
			current_hide[bone.name] = armature.data.bones[bone.name].hide
			armature.data.bones[bone.name].hide = False

		# Insert Keyframe
		bpy.ops.anim.keyframe_insert(type='__ACTIVE__')

		# Restore keyframe
		context.scene.keying_sets.active_index = current_keying_set

		#Restore selection
		for bone in armature.data.bones:
			bone.select = False
			if bone.name in current_selection:
				bone.select = True
			#Restore hide/displayed
			if bone.name in current_hide.keys():
				bone.hide = current_hide[bone.name]

		# all "after" that can not be done on regular operator
		#delete bones if any
		if len(to_delete) > 0:
			for i in to_delete:
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids.remove(i)

		 #switch on/off
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


class POSE_MT_keyframing(bpy.types.Menu):
	bl_idname = "POSE_MT_keyframing"
	bl_label  = "Keyframe"

	def draw(self, context):
		layout = self.layout

		for ks in bpy.context.scene.keying_sets_all.keys():
			#TODO : delete composite KS created by ExtraGroups
			op = layout.operator("pose.ope_keyframing_after_menu", text=ks)
			op.data   = ks
			op.event  = bpy.context.object.jueg_menu_temp_data.event
			op.index  = bpy.context.object.jueg_menu_temp_data.index
			op.ops_id = bpy.context.object.jueg_menu_temp_data.ops_id
			op.solo   = bpy.context.object.jueg_menu_temp_data.solo
			op.mirror = bpy.context.object.jueg_menu_temp_data.mirror


class POSE_OT_jueg_keyframing(Operator):
	"""Add keyframe"""
	bl_idname = "pose.ope_keyframing"
	bl_label = "keyframing"


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
					break

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

		if mirror == True and len(addonpref().xx_sides) == 0:
			init_sides(context)

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

		if mirror == True:
			bones = [armature.pose.bones[get_symm_name(bone.name)] for bone in bones ]


		call_menu = False
		if mode == "FORCED_MENU" or mode == "FORCED_MENU_MIRROR":
			call_menu = True
		elif mode in ["DEFAULT",
					"KEYING_ONLY"]:
			#check if there is KS already set assigned to this group
			if addonpref().use_keyingset == True and armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].keying != "":
				# We are going to use this KeyingSet

				# store current keyingset if any
				current_keying_set = context.scene.keying_sets.active_index

				# Set Keying set
				bpy.context.scene.keying_sets.active = context.scene.keying_sets_all[armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].keying]

				# Store current selection
				current_selection = []
				for bone in armature.data.bones:
					if bone.select == True:
						current_selection.append(bone.name)
						bone.select = False

				#Select all bones of group
				for bone in bones:
					armature.data.bones[bone.name].select = True

				# Insert Keyframe
				bpy.ops.anim.keyframe_insert(type='__ACTIVE__')

				# Restore keyframe
				context.scene.keying_sets.active_index = current_keying_set

				#Restore selection
				for bone in armature.data.bones:
					bone.select = False
					if bone.name in current_selection:
						bone.select = True
			else:
				# No keying set --> call menu if default,
				# If keying only --> no call
				if mode == "DEFAULT":
					call_menu = True
		elif mode in ["DEFAULT_MIRROR",
					"KEYING_ONLY_MIRROR"]:
			self.report({'ERROR'}, "KeyingSet mirror is not implemented yet")

		to_delete = []
		idx = -1
		for bone in bones:
			idx = idx + 1
			if bone.name not in armature.data.bones: #If bone no more exists
				to_delete.append(idx)
				continue
			# Nothing to do here :
				# If call_menu == True : things will be done on other ops after popup
				# If call_menu == False : keyingSet is already done
			# But we have to keep this loop to delete unkown bones


		if call_menu == True:
			# set temp data to menu
			armature.jueg_menu_temp_data.event  = mode
			armature.jueg_menu_temp_data.index  = self.index
			armature.jueg_menu_temp_data.ops_id = self.ops_id
			armature.jueg_menu_temp_data.solo   = solo
			armature.jueg_menu_temp_data.mirror = mirror
			bpy.ops.wm.call_menu(name="POSE_MT_keyframing")


		# all after, in case menu was not called
		if call_menu == True:
			# already done by menu operator
			return {'FINISHED'}

		#delete bones if any
		if len(to_delete) > 0:
			for i in to_delete:
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids.remove(i)

		 #switch on/off
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
								if ops.on_off == True:
									# group that was solo before must be turn off
									for ops_ in bonegroup.on_off:
										if ops_.id == self.ops_id:
											ops_.on_off = False
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
