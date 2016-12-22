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
import uuid
import bpy_extras
from .text_ops_squel import TEMPLATE
from .globs import *
from .utils import *


class POSE_OT_jueg_operator_move(bpy.types.Operator):
	"""Move up or down the current operator in the list"""
	bl_idname = "pose.jueg_operator_move"
	bl_label = "Move Operator"
	bl_options = {'REGISTER'}

	direction = bpy.props.StringProperty()

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
				script = bpy.data.textx[textname]
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
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

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


class POSE_OT_jueg_update_to_new_addon_version(bpy.types.Operator):
	"""Update data to new addon version"""
	bl_idname = "pose.jueg_update_new_addon_version"
	bl_label = "Update data to new addon version"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
			context.object.type == 'ARMATURE' and
			context.mode == 'POSE'
			and check_addon_update_needed() == True)

	def execute(self, context):
		for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
			if len(obj.jueg_extragroups_ops) > 0:
				for id in get_default_ops_id().keys():
					if id not in [ops.id for ops in obj.jueg_extragroups_ops if ops.user_defined == False]:
						#A new operator is available, create it
						new_ops = obj.jueg_extragroups_ops.add()
						new_ops.name     = get_default_ops_id()[id]["name"]
						new_ops.id       = id
						new_ops.ops_type = get_default_ops_id()[id]["ops_type"]
						new_ops.ops_exe  = get_default_ops_id()[id]["ops_exe"]
						new_ops.icon_on = get_default_ops_id()[id]["icon_on"]
						new_ops.icon_off = get_default_ops_id()[id]["icon_off"]
						new_ops.ok_for_current_sel = get_default_ops_id()[id]["ok_for_current_sel"]
						new_ops.ops_context = get_default_ops_id()[id]["ops_context"]
						new_ops.display = get_default_ops_id()[id]["display"]
						new_ops.user_defined = get_default_ops_id()[id]["user_defined"]
						new_ops.magic_nb          = get_default_ops_id()[id]['magic_nb']

						#now add display info on each grouptype
						for grouptype in obj.jueg_grouptypelist:
							ope = grouptype.ops_display.add()
							ope.id = new_ops.id
							ope.display = False

						#now add on/off for each existing bone group of each type
						for grouptype in obj.jueg_grouptypelist:
							bonegroups = grouptype.group_ids
							for group in bonegroups:
								new_ = group.on_off.add()
								new_.id = new_ops.id
								new_.on_off = True

						#now add solo for each existing bone group of each type
						for grouptype in obj.jueg_grouptypelist:
							bonegroups = grouptype.group_ids
							for group in bonegroups:
								new_ = group.solo.add()
								new_.id = new_ops.id
								new_.on_off = False

				to_delete = []
				for ope in [ops for ops in obj.jueg_extragroups_ops if ops.user_defined == False]:
					if ope.id not in get_default_ops_id().keys():
						#This operator is now deleted, remove data
						for grouptype in obj.jueg_grouptypelist:
							context.scene.display_save.clear()
							for ops_display in grouptype.ops_display:
								new_ = context.scene.display_save.add()
								new_.id = ops_display.id
								new_.display = ops_display.display
							grouptype.ops_display.clear()
							for disp in context.scene.display_save:
								if disp.id != ope.id:
									new_ = grouptype.ops_display.add()
									new_.id = disp.id
									new_.display = disp.display
							context.scene.display_save.clear()
							grouptype.active_ops = 0

						for grouptype in obj.jueg_grouptypelist:
							bonegroups = grouptype.group_ids
							for group in bonegroups:
								context.scene.on_off_save.clear()
								for on_off in group.on_off:
									new_ = context.scene.on_off_save.add()
									new_.id = on_off.id
									new_.on_off = on_off.on_off
								group.on_off.clear()
								for on_off in context.scene.on_off_save:
									if on_off.id != ope.id:
										new_ = group.on_off.add()
										new_.id = on_off.id
										new_.on_off = on_off.on_off
								context.scene.on_off_save.clear()

								context.scene.solo_save.clear()
								for solo in group.solo:
									new_ = context.scene.solo_save.add()
									new_.id = solo.id
									new_.on_off = solo.on_off
								group.solo.clear()
								for solo in context.scene.solo_save:
									if solo.id != ope.id:
										new_ = group.solo.add()
										new_.id = solo.id
										new_.on_off = solo.on_off
								context.scene.solo_save.clear()

						to_delete.append(ope.name)
					else:
						if ope.magic_nb != get_default_ops_id()[ope.id]['magic_nb']:
							#Operator needs to be updated
							#Update only not editable fields
							ope.name               = get_default_ops_id()[ope.id]['name']
							ope.magic_nb          = get_default_ops_id()[ope.id]['magic_nb']
							ope.ops_type           = get_default_ops_id()[ope.id]['ops_type']
							ope.ops_exe            = get_default_ops_id()[ope.id]['ops_exe']
							ope.ok_for_current_sel = get_default_ops_id()[ope.id]['ok_for_current_sel']
							ope.ops_context = get_default_ops_id()[ope.id]['ops_context']
							ope.event_manage       = get_default_ops_id()[ope.id]['event_manage']
							ope.events.clear()
							for ev in get_default_ops_id()[ope.id]['events']:
								new_ = ope.events.add()
								new_.mode  = ev[0]
								new_.event = ev[1]
								new_.solo  = ev[2]

				for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
					if len(obj.jueg_extragroups_ops) > 0:
						doubles = {}
						for ope in [ops for ops in obj.jueg_extragroups_ops]:
							if ope.id not in doubles.keys():
								doubles[ope.id] = 1
							else:
								#remove this
								for grouptype in obj.jueg_grouptypelist:
									context.scene.display_save.clear()
									for ops_display in grouptype.ops_display:
										new_ = context.scene.display_save.add()
										new_.id = ops_display.id
										new_.display = ops_display.display
									grouptype.ops_display.clear()
									already_found = False
									for disp in context.scene.display_save:
										if disp.id != ope.id or (disp.id == ope.id and already_found == True):
											new_ = grouptype.ops_display.add()
											new_.id = disp.id
											new_.display = disp.display
										else:
											already_found = True
									context.scene.display_save.clear()
									grouptype.active_ops = 0

								for grouptype in obj.jueg_grouptypelist:
									bonegroups = grouptype.group_ids
									for group in bonegroups:
										context.scene.on_off_save.clear()
										for on_off in group.on_off:
											new_ = context.scene.on_off_save.add()
											new_.id = on_off.id
											new_.on_off = on_off.on_off
										group.on_off.clear()
										already_found = False
										for on_off in context.scene.on_off_save:
											if on_off.id != ope.id or (on_off.id == ope.id and already_found == True):
												new_ = group.on_off.add()
												new_.id = on_off.id
												new_.on_off = on_off.on_off
											else:
												already_found = True
										context.scene.on_off_save.clear()

										context.scene.solo_save.clear()
										for solo in group.solo:
											new_ = context.scene.solo_save.add()
											new_.id = solo.id
											new_.on_off = solo.on_off
										group.solo.clear()
										already_found = False
										for solo in context.scene.solo_save:
											if solo.id != ope.id or (solo.id == ope.id and already_found == True):
												new_ = group.solo.add()
												new_.id = solo.id
												new_.on_off = solo.on_off
											else:
												already_found = True
										context.scene.solo_save.clear()

								to_delete.append(ope.name)
								del doubles[ope.id]

				for del_ in to_delete:
					obj.jueg_extragroups_ops.remove(obj.jueg_extragroups_ops.find(del_))




		return {'FINISHED'}

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
						dst_bonegroup.color             = lib_bonegroup.color

						for lib_bone in lib_bonegroup.bone_ids:
							dst_bone = dst_bonegroup.bone_ids.add()
							dst_bone.name = lib_bone.name

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
						dst_ev.mode  = ev.mode
						dst_ev.event = ev.event
						dst_ev.solo  = ev.solo

				break
		return {'FINISHED'}


class POSE_OT_jueg_select_icon(bpy.types.Operator):
	"""Select icon"""
	bl_idname = "jueg.select_icon"
	bl_label  = "Select Icon"

	icon_type = bpy.props.StringProperty(name="icon on or off")
	icon      = bpy.props.StringProperty(name="icon")

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

class POSE_OT_jueg_dummy_solo(bpy.types.Operator):
	bl_idname = "pose.jueg_dummy_solo"
	bl_label = "Dummy Solo"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return (context.object and
				context.object.type == 'ARMATURE' and
				context.mode == 'POSE')

	def execute(self, context):

		self.report({'ERROR'}, "Solo mode is enabled in another Group")

		return {'FINISHED'}

def register():
	bpy.utils.register_class(POSE_OT_jueg_ops_add)
	bpy.utils.register_class(POSE_OT_jueg_ops_remove)
	bpy.utils.register_class(POSE_OT_jueg_operator_move)
	bpy.utils.register_class(POSE_OT_jueg_dummy)
	bpy.utils.register_class(POSE_OT_jueg_dummy_solo)
	bpy.utils.register_class(POSE_OT_jueg_reload_linked_data)
	bpy.utils.register_class(POSE_OT_jueg_update_to_new_addon_version)
	bpy.utils.register_class(POSE_OT_jueg_select_icon)
	bpy.utils.register_class(POSE_OT_jueg_erase_data)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_ops_add)
	bpy.utils.unregister_class(POSE_OT_jueg_ops_remove)
	bpy.utils.unregister_class(POSE_OT_jueg_operator_move)
	bpy.utils.unregister_class(POSE_OT_jueg_dummy)
	bpy.utils.unregister_class(POSE_OT_jueg_dummy_solo)
	bpy.utils.unregister_class(POSE_OT_jueg_reload_linked_data)
	bpy.utils.unregister_class(POSE_OT_jueg_update_to_new_addon_version)
	bpy.utils.unregister_class(POSE_OT_jueg_select_icon)
	bpy.utils.unregister_class(POSE_OT_jueg_erase_data)
