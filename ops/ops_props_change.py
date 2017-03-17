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

class POSE_OT_jueg_props_change(Operator):
	"""Change Custom Properties"""
	bl_idname = "pose.jueg_props_change"
	bl_label = "Props"


	ops_id		 = StringProperty()
	index		 = IntProperty()
	reset_solo   = BoolProperty()
	force_mode   = StringProperty(default="")

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
