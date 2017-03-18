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
				for id in sorted(get_default_ops_id(), key= lambda name: get_default_ops_id()[name]["sort_order"]):
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
						new_ops.event_manage       = get_default_ops_id()[id]['event_manage']
						new_ops.events.clear()
						for ev in get_default_ops_id()[id]['events']:
							new_ = new_ops.events.add()
							new_.mode   = ev[0]
							new_.label  = ev[1]
							new_.event  = ev[2]
							new_.active = ev[3]
							new_.solo   = ev[4]


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
								new_.mode   = ev[0]
								new_.label  = ev[1]
								new_.event  = ev[2]
								new_.active = ev[3]
								new_.solo   = ev[4]

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

def register():
	bpy.utils.register_class(POSE_OT_jueg_update_to_new_addon_version)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_update_to_new_addon_version)
