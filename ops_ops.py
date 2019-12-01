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
from .text_ops_squel import TEMPLATE
from .globs import *
from .utils import *


class POSE_OT_jueg_select_icon(bpy.types.Operator):
	"""Select icon"""
	bl_idname = "jueg.select_icon"
	bl_label  = "Select Icon"

	icon_type : bpy.props.StringProperty(name="icon on or off")
	icon      : bpy.props.StringProperty(name="icon")

	@classmethod
	def poll(self, context):
		return True

	def execute(self, context):
		armature = context.object
		jueg_active_grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype]
		ops = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == jueg_active_grouptype.ops_display[jueg_active_grouptype.active_ops].id][0]

		if self.icon_type == "icon_on":
			ops.icon_on =  self.icon
			ops.icons.icon_on.expand = False
		elif self.icon_type == "icon_off":
			ops.icon_off =  self.icon
			ops.icons.icon_off.expand = False

		return {'FINISHED'}

class POSE_OT_jueg_erase_data(bpy.types.Operator):
	bl_idname = "pose.jueg_erase_data"
	bl_label  = "Erase data"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return True

	def execute(self, context):
		for scene in bpy.data.scenes:
			scene.on_off_save.clear()
			scene.solo_save.clear()
			scene.display_save.clear()

		for obj in bpy.data.objects:
			obj.jueg_grouptypelist.clear()
			obj.jueg_extragroups_ops.clear()
			obj.jueg_active_grouptype = 0
			obj.jueg_menu_temp_data.event  = ""
			obj.jueg_menu_temp_data.index  = 0
			obj.jueg_menu_temp_data.ops_id = ""
			obj.jueg_menu_temp_data.solo   = False

		return {'FINISHED'}

class POSE_OT_jueg_dummy(bpy.types.Operator):
	bl_idname = "pose.jueg_dummy"
	bl_label = "Dummy"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):

		return {'FINISHED'}

def register():
	bpy.utils.register_class(POSE_OT_jueg_dummy)
	bpy.utils.register_class(POSE_OT_jueg_select_icon)
	bpy.utils.register_class(POSE_OT_jueg_erase_data)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_dummy)
	bpy.utils.unregister_class(POSE_OT_jueg_select_icon)
	bpy.utils.unregister_class(POSE_OT_jueg_erase_data)
