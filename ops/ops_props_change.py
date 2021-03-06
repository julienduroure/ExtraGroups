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

class POSE_OT_jueg_props_change(Operator):
	"""Change Custom Properties"""
	bl_idname = "pose.jueg_props_change"
	bl_label = "Props"


	ops_id		 : StringProperty()
	index		 : IntProperty()
	reset_solo   : BoolProperty()
	force_mode   : StringProperty(default="")

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def invoke(self, context, event):
		wm = context.window_manager

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
			self.bones = armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids[self.index].bone_ids
		else:
			self.bones = []
			for bone in armature.pose.bones:
				if bone.bone.select == True:
					self.bones.append(bone)

		if mirror == True:
			self.bones = [armature.pose.bones[get_symm_name(bone.name)] for bone in self.bones ]

		return wm.invoke_props_dialog(self)

	def draw(self, context):
		layout = self.layout
		armature = context.object

		global_found = False
		for bone in self.bones:
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
				row.label(text=bone.name)
				for prop in armature.pose.bones[bone.name].keys():
					if prop != "_RNA_UI":
						row = box.row()
						row.prop(armature.pose.bones[bone.name], '["' + prop + '"]')
		if global_found == False:
			layout.label(text="No custom properties")

	def execute(self, context):
		return {'FINISHED'}
