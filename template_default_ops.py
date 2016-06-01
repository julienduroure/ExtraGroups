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

from bpy.props import (
	BoolProperty,
	StringProperty,
	IntProperty,
)

from bpy.types import (
	Operator,
)

class POSE_OT_jueg_changevisibility(Operator):
	"""Change visibility"""
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
			if on_off == True:
				armature.data.bones[bone.name].hide = True
			else:
				armature.data.bones[bone.name].hide = False
###################################################################################

		#No after

		if len(to_deleted) > 0:
			for i in to_deleted:
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids.remove(i)


		for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].on_off:
			if ops.id == self.ops_id:
				ops.on_off = not ops.on_off

		return {'FINISHED'}


class POSE_OT_jueg_bonemute(Operator):
	"""Mute action of bones / solo action (set event for detail)"""
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
					ops.on_off = True #TODO

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
								ops.on_off = False #TODO
							else:
								ops.on_off = True #TODO
				index = index + 1

		return {'FINISHED'}

class POSE_OT_jueg_restrict_select(Operator):
	"""Restrict/Allow selection"""
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
			armature.pose.bones[bone.name].bone.hide_select = on_off
################################################################################
		#No after
		#delete bones if any
		if len(to_delete) > 0:
			for i in to_delete:
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids.remove(i)

		 #switch on/off
		for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].on_off:
			if ops.id == self.ops_id:
				ops.on_off = not ops.on_off

		return {'FINISHED'}


class POSE_OT_jueg_select(Operator):
	"""Selection : See Event Management for more info"""
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
		if mode == "REPLACE":
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
			if mode == "REPLACE" or mode == "ADD":
				armature.data.bones[bone.name].select = True
			elif mode == "REMOVE":
				armature.data.bones[bone.name].select = False
################################################################################
		#No after

		#delete bones if any
		if len(to_delete) > 0:
			for i in to_delete:
				armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids.remove(i)

		 #switch on/off
		for ops in armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].on_off:
			if ops.id == self.ops_id:
				ops.on_off = not ops.on_off

		return {'FINISHED'}

def register():
	bpy.utils.register_class(POSE_OT_jueg_changevisibility)
	bpy.utils.register_class(POSE_OT_jueg_bonemute)
	bpy.utils.register_class(POSE_OT_jueg_restrict_select)
	bpy.utils.register_class(POSE_OT_jueg_select)


def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_changevisibility)
	bpy.utils.unregister_class(POSE_OT_jueg_bonemute)
	bpy.utils.unregister_class(POSE_OT_jueg_restrict_select)
	bpy.utils.unregister_class(POSE_OT_jueg_select)



if __name__ == "__main__":
	register()
