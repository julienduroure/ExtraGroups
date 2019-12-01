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


class POSE_OT_jueg_text_display(bpy.types.Operator):
	"""Display current source code in text windows"""
	bl_idname = "pose.jueg_text_display"
	bl_label = "Display Text"
	bl_options = {'REGISTER'}

	text_id : bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):

		if self.text_id not in bpy.data.texts:
			return {'FINISHED'}
		text = bpy.data.texts[self.text_id]
		for area in bpy.context.screen.areas:
			if area.type == 'TEXT_EDITOR':
				area.spaces[0].text = text

				ctx = bpy.context.copy()
				ctx['edit_text'] = text
				ctx['area'] = area
				ctx['region'] = area.regions[-1]
				bpy.ops.text.jump(ctx)

		return {'FINISHED'}


class TEXT_OT_jueg_text_remove(bpy.types.Operator):
	"""Delete text from Blender"""
	bl_idname = "text.jueg_text_remove"
	bl_label = "Remove Text"
	bl_options = {'REGISTER'}

	text_id : bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):

		if self.text_id not in bpy.data.texts:
			return {'FINISHED'}
		text = bpy.data.texts[self.text_id]
		for area in bpy.context.screen.areas:
			if area.type == 'TEXT_EDITOR':
				area.spaces.active.text = text

				ctx = bpy.context.copy()
				ctx['edit_text'] = text
				ctx['area'] = area
				ctx['region'] = area.regions[-1]

				bpy.ops.text.unlink(ctx)
				break

		return {'FINISHED'}

def register():
	bpy.utils.register_class(POSE_OT_jueg_text_display)
	bpy.utils.register_class(TEXT_OT_jueg_text_remove)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_text_display)
	bpy.utils.unregister_class(TEXT_OT_jueg_text_remove)
