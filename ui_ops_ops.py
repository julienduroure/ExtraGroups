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
from .text_ops_squel import TEMPLATE
from .globs import *
from .utils import *


class POSE_OT_jueg_operator_move(bpy.types.Operator):
	"""Move up or down the current operator in the list"""
	bl_idname = "pose.jueg_operator_move"
	bl_label = "Move Operator"
	bl_options = {'REGISTER'}

	direction : bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		armature = context.object
		index	= armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops

		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index

		if new_index < len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display) and new_index >= 0:
			armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display.move(index, new_index)
			armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops = new_index

		return {'FINISHED'}

class POSE_OT_jueg_ops_add(bpy.types.Operator):
	"""Add a new operator"""
	bl_idname = "pose.jueg_ops_add"
	bl_label = "Add Ops"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):
		keep = False
		armature = context.object

		if len(armature.jueg_grouptypelist) > 0:

			ops = armature.jueg_extragroups_ops.add()
			ops.id   = uuid.uuid4().hex
			ops.name = "Ops.%d" % len(armature.jueg_extragroups_ops)
			ops.ops_exe = "pose.ope_" + ops.id
			ops.ops_type = 'EXE'
			ops.display = False
			ops.user_defined = True
			# now that id is generated, generate a new file
			textname = ops.id + ".py"
			if textname in bpy.data.texts:
				script = bpy.data.texts[textname]
				script.clear()
			else:
				script = bpy.data.texts.new(textname)
				script.use_module = True
				txt = TEMPLATE
				txt = txt.replace("###opsclass###",ops.id)
				script.write(txt)
				exec(script.as_string() + "\nregister()\n", {})


			#now add ops info on each object
			for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE' and j.name != armature.name]:
				new_ops = obj.jueg_extragroups_ops.add()
				new_ops.id = ops.id
				new_ops.name = ops.name
				new_ops.ops_exe = ops.ops_exe
				new_ops.ops_type = ops.ops_type
				new_ops.display = ops.display
				new_ops.user_defined = ops.user_defined

			#now add display info on each grouptype
			for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
				for grouptype in obj.jueg_grouptypelist:
					ope = grouptype.ops_display.add()
					ope.id = ops.id
					ope.display = False

			#now add on/off for each existing bone group of each type
			for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
				for grouptype in obj.jueg_grouptypelist:
					bonegroups = grouptype.group_ids
					for group in bonegroups:
						new_ = group.on_off.add()
						new_.id = ops.id
						new_.on_off = True

			#now add solo for each existing bone group of each type
			for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
				for grouptype in obj.jueg_grouptypelist:
					bonegroups = grouptype.group_ids
					for group in bonegroups:
						new_ = group.solo.add()
						new_.id = ops.id
						new_.on_off = False

			armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops = len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display) - 1

		return {'FINISHED'}

class POSE_OT_jueg_ops_remove(bpy.types.Operator):
	"""Remove the operator"""
	bl_idname = "pose.jueg_ops_remove"
	bl_label = "Remove Ops"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		armature = context.object
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE' and
				[e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id][0].user_defined == True)

	def execute(self, context):
		armature = context.object

		id_to_delete = armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display[armature.jueg_grouptypelist[armature.jueg_active_grouptype].active_ops].id
		if len(armature.jueg_grouptypelist) > 0 and len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display) > 0:
			if addonpref().textremove == True:
				file_ = id_to_delete + ".py"
				bpy.ops.text.jueg_text_remove(text_id=file_)

			armature.jueg_extragroups_ops.remove([i for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == id_to_delete][0])

			for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
				for grouptype in obj.jueg_grouptypelist:
					grouptype.ops_display.remove([i for i,e in enumerate(grouptype.ops_display) if e.id == id_to_delete][0])

					len_ = len(grouptype.ops_display)
					if (grouptype.active_ops > (len_ - 1) and len_ > 0):
						grouptype.active_ops = len(grouptype.ops_display) - 1

					#also remove on/off for each existing bonegroup of each type (of each armature)
					bonegroups = grouptype.group_ids
					for group in bonegroups:
						group.on_off.remove([i for i,j in enumerate(group.on_off) if j.id == id_to_delete][0])

					#also remove solo for each existing bonegroup of each type (of each armature)
					bonegroups = grouptype.group_ids
					for group in bonegroups:
						group.solo.remove([i for i,j in enumerate(group.solo) if j.id == id_to_delete][0])

		return {'FINISHED'}


def register():
	bpy.utils.register_class(POSE_OT_jueg_ops_add)
	bpy.utils.register_class(POSE_OT_jueg_ops_remove)
	bpy.utils.register_class(POSE_OT_jueg_operator_move)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_ops_add)
	bpy.utils.unregister_class(POSE_OT_jueg_ops_remove)
	bpy.utils.unregister_class(POSE_OT_jueg_operator_move)
