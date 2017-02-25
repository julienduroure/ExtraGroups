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
from .utils import *

from bpy.props import (
	BoolProperty,
	StringProperty,
	IntProperty,
)

from bpy.types import (
	Operator,
)

class POSE_OT_jueg_changevisibility(Operator):
	"""Change visibility / solo mode (see events for more info)"""
	bl_idname = "pose.jueg_change_visibility"
	bl_label = "Change visibility"


	ops_id		 = StringProperty()
	index			= IntProperty()

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
				events = ops.events
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

		current_selection = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].current_selection
		if current_selection == False:
			bones = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids
		else:
			bones = []
			for bone in armature.pose.bones:
				if bone.bone.select == True:
					bones.append(bone)

		#No Before

		to_deleted = []
		idx = -1
		for bone in bones:
			idx = idx + 1
			if bone.name not in armature.data.bones:
				to_deleted.append(idx)
				continue
################################## Insert your code here ##########################
			if solo == False:
				if on_off == True:
					armature.data.bones[bone.name].hide = True
				else:
					armature.data.bones[bone.name].hide = False
			else:
				armature.data.bones[bone.name].hide = False
###################################################################################
		if solo == True:
			for bone in armature.pose.bones:
				if bone.name not in [b.name for b in bones]:
					if solo_already == True:
						armature.data.bones[bone.name].hide = False
					else:
						armature.data.bones[bone.name].hide = True
###################################################################################

		if len(to_deleted) > 0:
			for i in to_deleted:
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids.remove(i)


		for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].on_off:
			if ops.id == self.ops_id:
				if solo == False:
					ops.on_off = not ops.on_off
				else:
					ops.on_off = True # Inversed solo ?

		if solo == True:

			#Toggle solo info
			for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo:
				if ops.id == self.ops_id:
					ops.on_off = not ops.on_off

			#Toggle on_off info for other groups
			index = 0
			for bonegroup in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
				if index != self.index:
					for ops in bonegroup.on_off:
						if ops.id == self.ops_id:
							if solo_already == False:
								ops.on_off = False # Inversed solo ?
							else:
								ops.on_off = True # Inversed solo ?
				index = index + 1

		return {'FINISHED'}


class POSE_OT_jueg_bonemute(Operator):
	"""Mute action of bones / solo mode (set events for more info)"""
	bl_idname = "pose.jueg_bonemute"
	bl_label = "Mute bones"


	ops_id		 = StringProperty()
	index			= IntProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def mute(self, bone, on_off, solo, solo_already):
		armature = bpy.context.object
		if solo == False:
			muting = on_off
		else:
			if solo_already == False:
				muting = False
			else:
				muting = False

		if on_off == True:
			if armature.animation_data and bone.name in armature.animation_data.action.groups:
				for channel in armature.animation_data.action.groups[bone.name].channels:
					channel.mute = muting
			if armature.animation_data:
				for fc in armature.animation_data.action.fcurves:
					if not fc.group:
						if fc.data_path.startswith("pose.bones"):
							tmp = fc.data_path.split("[", maxsplit=1)[1].split("]", maxsplit=1)
							bone_name = tmp[0][1:-1]
							if bone.name == bone_name:
								fc.mute = muting
		else:
			if armature.animation_data and bone.name in armature.animation_data.action.groups:
				for channel in armature.animation_data.action.groups[bone.name].channels:
					channel.mute = muting
			if armature.animation_data:
				for fc in armature.animation_data.action.fcurves:
					if not fc.group:
						if fc.data_path.startswith("pose.bones"):
							tmp = fc.data_path.split("[", maxsplit=1)[1].split("]", maxsplit=1)
							bone_name = tmp[0][1:-1]
							if bone.name == bone_name:
								fc.mute = muting

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
				events = ops.events
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

		current_selection = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].current_selection
		if current_selection == False:
			bones = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids
		else:
			bones = []
			for bone in armature.pose.bones:
				if bone.bone.select == True:
					bones.append(bone)

		#No before

		to_deleted = []
		idx = -1
		for bone in bones:
			idx = idx + 1
			if bone.name not in armature.data.bones:
				to_deleted.append(idx)
				continue
################################## Insert your code here ##########################
			self.mute(bone, on_off, solo, solo_already)
###################################################################################
# After
		if solo == True:
			for bone in armature.pose.bones:
				if bone.name not in [b.name for b in bones]:
					if solo_already == True:
						self.mute(bone, False, False, False)
					else:
						self.mute(bone, True, False, False)
###################################################################################
		if len(to_deleted) > 0:
			for i in to_deleted:
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids.remove(i)

		for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].on_off:
			if ops.id == self.ops_id:
				if solo == False:
					ops.on_off = not ops.on_off
				else:
					ops.on_off = True # Inversed solo ?

		if solo == True:

			#Toggle solo info
			for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo:
				if ops.id == self.ops_id:
					ops.on_off = not ops.on_off

			#Toggle on_off info for other groups
			index = 0
			for bonegroup in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
				if index != self.index:
					for ops in bonegroup.on_off:
						if ops.id == self.ops_id:
							if solo_already == False:
								ops.on_off = False # Inversed solo ?
							else:
								ops.on_off = True # Inversed solo ?
				index = index + 1

		return {'FINISHED'}

class POSE_OT_jueg_bonelock(Operator):
	"""Lock action of bones"""
	bl_idname = "pose.jueg_bonelock"
	bl_label = "Lock bones"


	ops_id		 = StringProperty()
	index			= IntProperty()

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
				events = ops.events
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

		to_delete = []
		idx = -1
		for bone in bones:
			idx = idx + 1
			if bone.name not in armature.data.bones: #If bone no more exists
				to_delete.append(idx)
				continue
			###################################################
			if armature.animation_data and bone.name in armature.animation_data.action.groups:
				for channel in armature.animation_data.action.groups[bone.name].channels:
					channel.mute = on_off
			if armature.animation_data:
				for fc in armature.animation_data.action.fcurves:
					if not fc.group:
						if fc.data_path.startswith("pose.bones"):
							tmp = fc.data_path.split("[", maxsplit=1)[1].split("]", maxsplit=1)
							bone_name = tmp[0][1:-1]
							if bone.name == bone_name:
								fc.mute = on_off
			###################################################

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

			#Toggle solo info
			for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo:
				if ops.id == self.ops_id:
					ops.on_off = not ops.on_off

			#Toggle on_off info for other groups
			index = 0
			for bonegroup in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
				if index != self.index:
					for ops in bonegroup.on_off:
						if ops.id == self.ops_id:
							if solo_already == False:
								ops.on_off = False # Inversed solo ?
							else:
								ops.on_off = True # Inversed solo ?
				index = index + 1

		return {'FINISHED'}

class POSE_OT_jueg_restrict_select(Operator):
	"""Restrict/Allow selection / solo mode (see events for more info)"""
	bl_idname = "pose.jueg_restrict_select"
	bl_label = "Restrict Select"


	ops_id		 = StringProperty()
	index			= IntProperty()

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
				events = ops.events
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

		#No before

		to_delete = []
		idx = -1
		for bone in bones:
			idx = idx + 1
			if bone.name not in armature.data.bones: #If bone no more exists
				to_delete.append(idx)
				continue
################################################################################
			if solo == False:
				armature.pose.bones[bone.name].bone.hide_select = on_off
			else:
				armature.pose.bones[bone.name].bone.hide_select = False
################################################################################
		if solo == True:
			for bone in armature.pose.bones:
				if bone.name not in [b.name for b in bones]:
					if solo_already == True:
						armature.pose.bones[bone.name].bone.hide_select = False
					else:
						armature.pose.bones[bone.name].bone.hide_select = True
################################################################################

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

			#Toggle solo info
			for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo:
				if ops.id == self.ops_id:
					ops.on_off = not ops.on_off

			#Toggle on_off info for other groups
			index = 0
			for bonegroup in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
				if index != self.index:
					for ops in bonegroup.on_off:
						if ops.id == self.ops_id:
							if solo_already == False:
								ops.on_off = False # Inversed solo ?
							else:
								ops.on_off = True # Inversed solo ?
				index = index + 1

		return {'FINISHED'}


class POSE_OT_jueg_props_change(Operator):
	"""Change Custom Properties"""
	bl_idname = "pose.jueg_props_change"
	bl_label = "Props"


	ops_id		 = StringProperty()
	index			= IntProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def draw(self, context):
		layout = self.layout

		armature = context.object
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

		global_found = False
		for bone in bones:
			#check if there is a prop for this bone
			found = False
			for prop in armature.pose.bones[bone.name].keys():
				if prop != "_RNA_UI":
					found = True
					global_found = True
					break
			if found == True:
				row_ = layout.row()
				box = row_.box()
				row = box.row()
				row.label(bone.name)
				for prop in armature.pose.bones[bone.name].keys():
					if prop != "_RNA_UI":
						row = box.row()
						row.prop(armature.pose.bones[bone.name], '["' + prop + '"]')
		if global_found == False:
			layout.label("No custom properties")

	def execute(self, context):
		return {'FINISHED'}


class POSE_OT_jueg_select(Operator):
	"""Selection (See events for more info)"""
	bl_idname = "pose.jueg_select"
	bl_label = "Magic Select"


	ops_id  	 = StringProperty()
	index   		= IntProperty()

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
				events = ops.events
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

		# Set active bone
		if mode == "REPLACE" or mode == "ADD" or mode == "SELECT_HIDE_OTHER":
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

			#Toggle solo info
			for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo:
				if ops.id == self.ops_id:
					ops.on_off = not ops.on_off

			#Toggle on_off info for other groups
			index = 0
			for bonegroup in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
				if index != self.index:
					for ops in bonegroup.on_off:
						if ops.id == self.ops_id:
							if solo_already == False:
								ops.on_off = False # Inversed solo ?
							else:
								ops.on_off = True # Inversed solo ?
				index = index + 1

		return {'FINISHED'}


class POSE_OT_jueg_keyframing_after_menu(Operator):
	"""Add keyframes"""
	bl_idname = "pose.ope_keyframing_after_menu"
	bl_label = "keyframing"


	index   	 = IntProperty()
	data		 = StringProperty()
	event   	 = StringProperty()
	ops_id       = StringProperty()
	solo         = BoolProperty()

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

			#Toggle solo info
			for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo:
				if ops.id == self.ops_id:
					ops.on_off = not ops.on_off

			#Toggle on_off info for other groups
			index = 0
			for bonegroup in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
				if index != self.index:
					for ops in bonegroup.on_off:
						if ops.id == self.ops_id:
							if solo_already == False:
								ops.on_off = False # Inversed solo ?
							else:
								ops.on_off = True # Inversed solo ?
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


class POSE_OT_jueg_keyframing(Operator):
	"""Add keyframe"""
	bl_idname = "pose.ope_keyframing"
	bl_label = "keyframing"


	ops_id  	 = StringProperty()
	index   		= IntProperty()

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
				events = ops.events
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
		else:
			mode = "JUEG_DUMMY"

		if mode == "":
			self.report({'ERROR'}, "No event assigned")
			return {'CANCELLED'}

		if mode == "JUEG_DUMMY":
			mode = ""


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


		call_menu = False
		if mode == "FORCED_MENU":
			call_menu = True
		elif mode == "DEFAULT" or mode == "KEYING_ONLY":
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

			#Toggle solo info
			for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].solo:
				if ops.id == self.ops_id:
					ops.on_off = not ops.on_off

			#Toggle on_off info for other groups
			index = 0
			for bonegroup in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids:
				if index != self.index:
					for ops in bonegroup.on_off:
						if ops.id == self.ops_id:
							if solo_already == False:
								ops.on_off = False # Inversed solo ?
							else:
								ops.on_off = True # Inversed solo ?
				index = index + 1

		return {'FINISHED'}


def register():
	bpy.utils.register_class(POSE_OT_jueg_changevisibility)
	bpy.utils.register_class(POSE_OT_jueg_bonemute)
	bpy.utils.register_class(POSE_OT_jueg_restrict_select)
	bpy.utils.register_class(POSE_OT_jueg_select)
	bpy.utils.register_class(POSE_OT_jueg_props_change)
	bpy.utils.register_class(POSE_OT_jueg_bonelock)
	bpy.utils.register_class(POSE_MT_keyframing)
	bpy.utils.register_class(POSE_OT_jueg_keyframing_after_menu)
	bpy.utils.register_class(POSE_OT_jueg_keyframing)


def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_changevisibility)
	bpy.utils.unregister_class(POSE_OT_jueg_bonemute)
	bpy.utils.unregister_class(POSE_OT_jueg_restrict_select)
	bpy.utils.unregister_class(POSE_OT_jueg_select)
	bpy.utils.unregister_class(POSE_OT_jueg_props_change)
	bpy.utils.unregister_class(POSE_OT_jueg_bonelock)
	bpy.utils.unregister_class(POSE_MT_keyframing)
	bpy.utils.unregister_class(POSE_OT_jueg_keyframing_after_menu)
	bpy.utils.unregister_class(POSE_OT_jueg_keyframing)



if __name__ == "__main__":
	register()
