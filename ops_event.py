##########################################################################################
#   GPL LICENSE:
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
#   Copyright 2016 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################
import bpy
from .globs import *
from .utils import *

class POSE_OT_jueg_event_move(bpy.types.Operator):
	"""Move event up or down in the list"""
	bl_idname = "pose.jueg_event_move"
	bl_label = "Move Event"
	bl_options = {'REGISTER'}

	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
		context.object.type == 'ARMATURE' and
		context.mode == 'POSE')

	def execute(self, context):
		armature = context.object
		index   = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].active_event
		events  = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].events

		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index

		if new_index < len(events) and new_index >= 0:
			events.move(index, new_index)
			[e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].active_event = new_index

		return {'FINISHED'}

class POSE_OT_jueg_event_add(bpy.types.Operator):
	"""Add a new event"""
	bl_idname = "pose.jueg_event_add"
	bl_label = "Add Event"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
		context.object.type == 'ARMATURE' and
		context.mode == 'POSE')

	def execute(self, context):
		armature = context.object
		events = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].events
		event = events.add()
		event.name = "Event.%d" % len(armature.jueg_grouptypelist)
		event.mode = 'NONE'
		[e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].active_event = len([e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].events) - 1

		return {'FINISHED'}

class POSE_OT_jueg_event_remove(bpy.types.Operator):
	"""Remove the current event"""
	bl_idname = "pose.jueg_event_remove"
	bl_label = "Remove Event"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object

		[e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].events.remove([e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].active_event)
		len_ = len([e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].events)
		if ([e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].active_event > (len_ - 1) and len_ > 0):
			[e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].active_event = len([e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].events) - 1
		return {'FINISHED'}

def register():
	bpy.utils.register_class(POSE_OT_jueg_event_add)
	bpy.utils.register_class(POSE_OT_jueg_event_remove)
	bpy.utils.register_class(POSE_OT_jueg_event_move)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_event_add)
	bpy.utils.unregister_class(POSE_OT_jueg_event_remove)
	bpy.utils.unregister_class(POSE_OT_jueg_event_move)
