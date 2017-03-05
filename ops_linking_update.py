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
import uuid
import bpy_extras
from .globs import *
from .utils import *



class POSE_OT_jueg_reload_linked_data(bpy.types.Operator):
	"""Reload data from linked armature"""
	bl_idname = "pose.jueg_reload_linked_data"
	bl_label = "Reload linked data"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		proxy, filepath = lib_proxy_armature()
		if proxy == False:
			return False

		local = bpy.context.object

		#delete current data
		local.jueg_active_grouptype = -1
		while len(local.jueg_grouptypelist) > 0:
			local.jueg_grouptypelist.remove(0)
		while len(local.jueg_extragroups_ops) > 0:
			local.jueg_extragroups_ops.remove(0)

		#load linked data
		with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
			data_to.objects = data_from.objects

		#refill local data with linked data
		for obj in data_to.objects:
			if obj.name == bpy.context.object.proxy.name:
				for lib_grouptype in obj.jueg_grouptypelist:
					dst_grouptype = local.jueg_grouptypelist.add()
					dst_grouptype.name = lib_grouptype.name

					for lib_bonegroup in lib_grouptype.group_ids:
						dst_bonegroup                   = dst_grouptype.group_ids.add()
						dst_bonegroup.name              = lib_bonegroup.name
						dst_bonegroup.current_selection = lib_bonegroup.current_selection

						for lib_bone in lib_bonegroup.bone_ids:
							dst_bone = dst_bonegroup.bone_ids.add()
							dst_bone.name = lib_bone.name

						dst_bonegroup.keying      = lib_bonegroup.keying
						dst_bonegroup.manipulator = lib_bonegroup.manipulator
						dst_bonegroup.orientation = lib_bonegroup.orientation
						dst_bonegroup.active_bone = lib_bonegroup.active_bone
						dst_bonegroup.color       = lib_bonegroup.color

						for lib_on_off in lib_bonegroup.on_off:
							dst_on_off = dst_bonegroup.on_off.add()
							dst_on_off.id = lib_on_off.id
							dst_on_off.on_off = lib_on_off.on_off

						for lib_solo in lib_bonegroup.solo:
							dst_solo        = dst_bonegroup.solo.add()
							dst_solo.id     = lib_solo.id
							dst_solo.on_off = lib_solo.on_off

					dst_grouptype.active_bonegroup = lib_grouptype.active_bonegroup

					for lib_ops_display in lib_grouptype.ops_display:
						dst_ops_display = dst_grouptype.ops_display.add()
						dst_ops_display.id = lib_ops_display.id
						dst_ops_display.display = lib_ops_display.display

					dst_grouptype.active_ops = lib_grouptype.active_ops

				local.jueg_active_grouptype = obj.jueg_active_grouptype

				for lib_ops in obj.jueg_extragroups_ops:
					dst_ops = local.jueg_extragroups_ops.add()
					dst_ops.id = lib_ops.id
					dst_ops.name = lib_ops.name
					dst_ops.ops_exe = lib_ops.ops_exe
					dst_ops.ops_type = lib_ops.ops_type
					dst_ops.icon_on = lib_ops.icon_on
					dst_ops.icon_off = lib_ops.icon_off
					dst_ops.ok_for_current_sel = lib_ops.ok_for_current_sel
					dst_ops.ops_context = lib_ops.ops_context
					dst_ops.user_defined = lib_ops.user_defined
					dst_ops.event_manage = lib_ops.event_manage
					dst_ops.magic_nb    = lib_ops.magic_nb

					for ev in lib_ops.events:
						dst_ev = dst_ops.events.add()
						dst_ev.mode   = ev.mode
						dst_ev.event  = ev.event
						dst_ev.active = ev.active
						dst_ev.solo   = ev.solo
						dst_ev.label  = ev.label

				break
		return {'FINISHED'}

def register():
	bpy.utils.register_class(POSE_OT_jueg_reload_linked_data)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_reload_linked_data)	
