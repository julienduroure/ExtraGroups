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
from .globs import *

#shortcut to prefs
def addonpref():
	user_preferences = bpy.context.user_preferences
	return user_preferences.addons[__package__].preferences

def get_default_ops_id():

	dict_ = {}

	dict_['f31027b2b65d4a90b610281ea09f08fb'] = {}
	dict_['f31027b2b65d4a90b610281ea09f08fb']['magic_nb'] = 4
	dict_['f31027b2b65d4a90b610281ea09f08fb']['name'] = "Mute"
	dict_['f31027b2b65d4a90b610281ea09f08fb']['ops_type'] = 'BOOL'
	dict_['f31027b2b65d4a90b610281ea09f08fb']['ops_exe'] = "pose.jueg_bonemute"
	dict_['f31027b2b65d4a90b610281ea09f08fb']['icon_on'] = "MUTE_IPO_OFF"
	dict_['f31027b2b65d4a90b610281ea09f08fb']['icon_off'] = "MUTE_IPO_ON"
	dict_['f31027b2b65d4a90b610281ea09f08fb']['ok_for_current_sel'] = True
	dict_['f31027b2b65d4a90b610281ea09f08fb']['ops_context'] = 'INVOKE_DEFAULT'
	dict_['f31027b2b65d4a90b610281ea09f08fb']['display'] = False
	dict_['f31027b2b65d4a90b610281ea09f08fb']['user_defined'] = False
	dict_['f31027b2b65d4a90b610281ea09f08fb']['event_manage'] = True
	dict_['f31027b2b65d4a90b610281ea09f08fb']['events'] = []
	dict_['f31027b2b65d4a90b610281ea09f08fb']['events'].append(['MUTE', 'Mute', 'NONE', True, False])
	dict_['f31027b2b65d4a90b610281ea09f08fb']['events'].append(['SOLO', 'Solo', 'CTRL', True, True])

	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86'] = {}
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['magic_nb'] = 4
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['name'] = "Toggle Visibility"
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['ops_type'] = 'BOOL'
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['ops_exe'] = "pose.jueg_change_visibility"
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['icon_on'] = "VISIBLE_IPO_ON"
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['icon_off'] = "VISIBLE_IPO_OFF"
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['ok_for_current_sel'] = False
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['ops_context'] = 'INVOKE_DEFAULT'
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['display'] = False
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['user_defined'] = False
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['event_manage'] = True
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['events'] = []
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['events'].append(['TOGGLE', 'Toggle', 'NONE', True, False])
	dict_['b9eac1a0a2fd4dcd94140d05a6a3af86']['events'].append(['SOLO', 'Solo', 'CTRL', True, True])

	dict_['9d5257bf3d6245afacabb452bf7a455e'] = {}
	dict_['9d5257bf3d6245afacabb452bf7a455e']['magic_nb'] = 4
	dict_['9d5257bf3d6245afacabb452bf7a455e']['name'] = "Restrict/Allow Selection"
	dict_['9d5257bf3d6245afacabb452bf7a455e']['ops_type'] = 'BOOL'
	dict_['9d5257bf3d6245afacabb452bf7a455e']['ops_exe'] = "pose.jueg_restrict_select"
	dict_['9d5257bf3d6245afacabb452bf7a455e']['icon_on'] = "RESTRICT_SELECT_OFF"
	dict_['9d5257bf3d6245afacabb452bf7a455e']['icon_off'] = "RESTRICT_SELECT_ON"
	dict_['9d5257bf3d6245afacabb452bf7a455e']['ok_for_current_sel'] = True
	dict_['9d5257bf3d6245afacabb452bf7a455e']['ops_context'] = 'INVOKE_DEFAULT'
	dict_['9d5257bf3d6245afacabb452bf7a455e']['display'] = False
	dict_['9d5257bf3d6245afacabb452bf7a455e']['user_defined'] = False
	dict_['9d5257bf3d6245afacabb452bf7a455e']['event_manage'] = True
	dict_['9d5257bf3d6245afacabb452bf7a455e']['events'] = []
	dict_['9d5257bf3d6245afacabb452bf7a455e']['events'].append(['TOGGLE', 'Toggle', 'NONE', True, False])
	dict_['9d5257bf3d6245afacabb452bf7a455e']['events'].append(['SOLO', 'Solo', 'CTRL', True, True])

	dict_['8102ad699e6d4af8a8f511e1283b995e'] = {}
	dict_['8102ad699e6d4af8a8f511e1283b995e']['magic_nb'] = 6
	dict_['8102ad699e6d4af8a8f511e1283b995e']['name'] = "Select"
	dict_['8102ad699e6d4af8a8f511e1283b995e']['ops_type'] = 'EXE'
	dict_['8102ad699e6d4af8a8f511e1283b995e']['ops_exe'] = "pose.jueg_select"
	dict_['8102ad699e6d4af8a8f511e1283b995e']['icon_on'] = "HAND"
	dict_['8102ad699e6d4af8a8f511e1283b995e']['icon_off'] = ""
	dict_['8102ad699e6d4af8a8f511e1283b995e']['ok_for_current_sel'] = False
	dict_['8102ad699e6d4af8a8f511e1283b995e']['ops_context'] = 'INVOKE_DEFAULT'
	dict_['8102ad699e6d4af8a8f511e1283b995e']['display'] = False
	dict_['8102ad699e6d4af8a8f511e1283b995e']['user_defined'] = False
	dict_['8102ad699e6d4af8a8f511e1283b995e']['event_manage'] = True
	dict_['8102ad699e6d4af8a8f511e1283b995e']['events'] = []
	dict_['8102ad699e6d4af8a8f511e1283b995e']['events'].append(['REPLACE', 'Select only', 'NONE', True, False])
	dict_['8102ad699e6d4af8a8f511e1283b995e']['events'].append(['ADD', 'Add to Selection', 'SHIFT', True, False])
	dict_['8102ad699e6d4af8a8f511e1283b995e']['events'].append(['REMOVE', 'Remove from Selection', 'ALT', True, False])
	dict_['8102ad699e6d4af8a8f511e1283b995e']['events'].append(['SELECT_HIDE_OTHER', 'Select only and hide others', 'CTRL', True, False])

	dict_['baeadde2d0594c5abfe083808b80d995'] = {}
	dict_['baeadde2d0594c5abfe083808b80d995']['magic_nb'] = 1
	dict_['baeadde2d0594c5abfe083808b80d995']['name'] = "Props"
	dict_['baeadde2d0594c5abfe083808b80d995']['ops_type'] = 'EXE'
	dict_['baeadde2d0594c5abfe083808b80d995']['ops_exe'] = "pose.jueg_props_change"
	dict_['baeadde2d0594c5abfe083808b80d995']['icon_on'] = "ANIM"
	dict_['baeadde2d0594c5abfe083808b80d995']['icon_off'] = ""
	dict_['baeadde2d0594c5abfe083808b80d995']['ok_for_current_sel'] = True
	dict_['baeadde2d0594c5abfe083808b80d995']['ops_context'] = 'INVOKE_DEFAULT'
	dict_['baeadde2d0594c5abfe083808b80d995']['display'] = False
	dict_['baeadde2d0594c5abfe083808b80d995']['user_defined'] = False
	dict_['baeadde2d0594c5abfe083808b80d995']['event_manage'] = False
	dict_['baeadde2d0594c5abfe083808b80d995']['events'] = []

	dict_['118c716214664d2890f1290fa984a6c9'] = {}
	dict_['118c716214664d2890f1290fa984a6c9']['magic_nb'] = 1
	dict_['118c716214664d2890f1290fa984a6c9']['name'] = "Lock"
	dict_['118c716214664d2890f1290fa984a6c9']['ops_type'] = 'BOOL'
	dict_['118c716214664d2890f1290fa984a6c9']['ops_exe'] = "pose.jueg_bonelock"
	dict_['118c716214664d2890f1290fa984a6c9']['icon_on'] = "UNLOCKED"
	dict_['118c716214664d2890f1290fa984a6c9']['icon_off'] = "LOCKED"
	dict_['118c716214664d2890f1290fa984a6c9']['ok_for_current_sel'] = True
	dict_['118c716214664d2890f1290fa984a6c9']['ops_context'] = 'INVOKE_DEFAULT'
	dict_['118c716214664d2890f1290fa984a6c9']['display'] = False
	dict_['118c716214664d2890f1290fa984a6c9']['user_defined'] = False
	dict_['118c716214664d2890f1290fa984a6c9']['event_manage'] = False
	dict_['118c716214664d2890f1290fa984a6c9']['events'] = []

	dict_['21ecdae49e174a8bb25f404fca0b6608'] = {}
	dict_['21ecdae49e174a8bb25f404fca0b6608']['magic_nb'] = 3
	dict_['21ecdae49e174a8bb25f404fca0b6608']['name'] = "Keyframing"
	dict_['21ecdae49e174a8bb25f404fca0b6608']['ops_type'] = 'EXE'
	dict_['21ecdae49e174a8bb25f404fca0b6608']['ops_exe'] = "pose.ope_keyframing"
	dict_['21ecdae49e174a8bb25f404fca0b6608']['icon_on'] = "KEYTYPE_KEYFRAME_VEC"
	dict_['21ecdae49e174a8bb25f404fca0b6608']['icon_off'] = ""
	dict_['21ecdae49e174a8bb25f404fca0b6608']['ok_for_current_sel'] = True
	dict_['21ecdae49e174a8bb25f404fca0b6608']['ops_context'] = 'INVOKE_DEFAULT'
	dict_['21ecdae49e174a8bb25f404fca0b6608']['display'] = False
	dict_['21ecdae49e174a8bb25f404fca0b6608']['user_defined'] = False
	dict_['21ecdae49e174a8bb25f404fca0b6608']['event_manage'] = True
	dict_['21ecdae49e174a8bb25f404fca0b6608']['events'] = []
	dict_['21ecdae49e174a8bb25f404fca0b6608']['events'].append(['DEFAULT', 'Default', 'NONE', True, False])
	dict_['21ecdae49e174a8bb25f404fca0b6608']['events'].append(['FORCED_MENU', 'Menu forced', 'CTRL', True, False])
	dict_['21ecdae49e174a8bb25f404fca0b6608']['events'].append(['KEYING_ONLY', 'Keying Only', 'SHIFT', True, False])

	return dict_

def merge_keyingset(ks1_, ks2_):
    index = bpy.context.scene.keying_sets.find(addonpref().internal_keyingset)
    ks1 = bpy.context.scene.keying_sets.find(ks1_)
    ks2 = bpy.context.scene.keying_sets.find(ks2_)

    if index != -1:
        bpy.context.scene.keying_sets.active_index = index
        bpy.ops.anim.keying_set_remove()
    ks = bpy.context.scene.keying_sets.new("KeyingSet", addonpref().internal_keyingset)

    if ks1 != -1:
        for path in bpy.context.scene.keying_sets[ks1].paths:
            if path.use_entire_array == True:
                ksp = ks.paths.add(path.id, path.data_path, index=-1)
            else:
                ksp = ks.paths.add(path.id, path.data_path, index=path.array_index)
    if ks2 != -1:
        for path in bpy.context.scene.keying_sets[ks2].paths:
            if path.use_entire_array == True:
                ksp = ks.paths.add(path.id, path.data_path, index=-1)
            else:
                ksp = ks.paths.add(path.id, path.data_path, index=path.array_index)


def copy_data_ops(armature,index_grouptype):
	for ops in armature.jueg_extragroups_ops:
		if ops.id not in [display.id for display in armature.jueg_grouptypelist[index_grouptype].ops_display]:
			new = armature.jueg_grouptypelist[index_grouptype].ops_display.add()
			new.id = ops.id
			new.display = False

def check_if_current_selection_exists_in_group(grouptype):
	for group in grouptype.group_ids:
		if group.current_selection == True:
			return True
	return False

def check_if_current_selection_exists(grouptype_id):
	return check_if_current_selection_exists_in_group(bpy.context.object.jueg_grouptypelist[grouptype_id])

def lib_proxy_armature():
	if bpy.context.active_object != None and bpy.context.active_object.data.library == None:
		return False, ""
	else:
		return True, bpy.context.active_object.data.library.filepath

def check_ops_doubles():
	for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
		if len(obj.jueg_extragroups_ops) > 0:
			doubles = {}
			for ope in [ops for ops in obj.jueg_extragroups_ops]:
				if ope.id not in doubles.keys():
					doubles[ope.id] = 1
				else:
					doubles[ope.id] = doubles[ope.id] + 1
			for id_ in doubles.keys():
				if doubles[id_] != 1:
					return True
			return False
	return False

def check_ops_updated_in_new_addon_version():
	for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
		if len(obj.jueg_extragroups_ops) > 0:
			for ope in [ops for ops in obj.jueg_extragroups_ops if ops.user_defined == False]:
				if ope.id in get_default_ops_id().keys():
					if ope.magic_nb != get_default_ops_id()[ope.id]['magic_nb']:
						return True
			return False
	return False

def check_new_default_ops_in_new_addon_version():
	for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
		if len(obj.jueg_extragroups_ops) > 0:
			for def_ops in get_default_ops_id().keys():
				if def_ops not in [ops.id for ops in obj.jueg_extragroups_ops if ops.user_defined == False]:
					return True
			return False
	return False

def check_ops_removed_in_new_addon_version():
	for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
		if len(obj.jueg_extragroups_ops) > 0:
			for ope in [ops for ops in obj.jueg_extragroups_ops if ops.user_defined == False]:
				if ope.id not in get_default_ops_id().keys():
					return True
			return False
	return False

def check_addon_update_needed():
	return check_new_default_ops_in_new_addon_version() or check_ops_removed_in_new_addon_version() or check_ops_updated_in_new_addon_version() or check_ops_doubles()

def check_multitype_not_display(active_index):
	armature = bpy.context.object
	cpt_index = 0
	for grouptype in armature.jueg_grouptypelist:
		if cpt_index == active_index:
			continue
		if len(grouptype.group_ids) > 0:
			return True
		cpt_index = cpt_index + 1
	return False

def check_duplicate_event(ops_index):
	events = []
	for event in [ev for ev in bpy.context.object.jueg_extragroups_ops[ops_index].events if ev.active == True]:
		if event.event in events:
			return True
		events.append(event.event)
	return False

def init_default_ops(armature):

	#first check if some objects have already data
	for obj in [j for i,j in enumerate(bpy.data.objects) if j.type == 'ARMATURE']:
		if obj.jueg_extragroups_ops and len(obj.jueg_extragroups_ops) > 0:
			for ops_src in obj.jueg_extragroups_ops:
				ops = armature.jueg_extragroups_ops.add()
				ops.id   = ops_src.id
				ops.name = ops_src.name
				ops.ops_exe = ops_src.ops_exe
				ops.ops_type = ops_src.ops_type
				ops.icon_on	= ops_src.icon_on
				ops.icon_off   = ops_src.icon_off
				ops.ok_for_current_sel = ops_src.ok_for_current_sel
				ops.ops_context = ops_src.ops_context
				ops.user_defined = ops_src.user_defined
				ops.event_manage = ops_src.event_manage
				ops.magic_nb    = ops_src.magic_nb

				for src_ev in ops_src.events:
					dst_ev = ops.events.add()
					dst_ev.mode   = src_ev.mode
					dst_ev.event  = src_ev.event
					dst_ev.label  = src_ev.label
					dst_ev.active = src_ev.active
					dst_ev.solo   = src_ev.solo

			copy_data_ops(armature, 0)
			armature.jueg_grouptypelist[0].active_ops = len(armature.jueg_extragroups_ops) - 1
			return True

	#if no data found, init with default ops
	for id in get_default_ops_id().keys():
		ops = armature.jueg_extragroups_ops.add()
		ops.name     = get_default_ops_id()[id]["name"]
		ops.id       = id
		ops.magic_nb = get_default_ops_id()[id]["magic_nb"]
		ops.ops_type = get_default_ops_id()[id]["ops_type"]
		ops.ops_exe  = get_default_ops_id()[id]["ops_exe"]
		ops.icon_on = get_default_ops_id()[id]["icon_on"]
		ops.icon_off = get_default_ops_id()[id]["icon_off"]
		ops.ok_for_current_sel = get_default_ops_id()[id]["ok_for_current_sel"]
		ops.ops_context = get_default_ops_id()[id]["ops_context"]
		ops.display = get_default_ops_id()[id]["display"]
		ops.user_defined = get_default_ops_id()[id]["user_defined"]
		ops.event_manage = get_default_ops_id()[id]["event_manage"]

		for src_ev in get_default_ops_id()[id]["events"]:
			dst_ev = ops.events.add()
			dst_ev.mode   = src_ev[0]
			dst_ev.label  = src_ev[1]
			dst_ev.event  = src_ev[2]
			dts_ev.active = src_ev[3]
			dst_ev.solo   = src_ev[4]

	copy_data_ops(armature,0)
	armature.jueg_grouptypelist[0].active_ops = len(armature.jueg_extragroups_ops) - 1

def get_all_icons():
	icons = bpy.types.UILayout.bl_rna.functions['prop'].parameters['icon'].enum_items.keys()
	icons.remove("NONE")
	return icons

def get_filter_icons(search):
	icons = get_all_icons()
	if search == "":
		pass
	else:
		icons = [key for key in icons if search in key.lower()]

	return icons

def init_sides(context):
	sides = addonpref().xx_sides
	side = sides.add()
	side.name_R = ".R"
	side.name_L = ".L"
	side = sides.add()
	side.name_R = ".r"
	side.name_L = ".l"
	side = sides.add()
	side.name_R = "-R"
	side.name_L = "-L"
	side = sides.add()
	side.name_R = "-r"
	side.name_L = "-l"
	side = sides.add()
	side.name_R = "_R"
	side.name_L = "_L"
	side = sides.add()
	side.name_R = "_r"
	side.name_L = "_l"
	side = sides.add()
	side.name_R = "right"
	side.name_L = "left"
	side = sides.add()
	side.name_R = "RIGHT"
	side.name_L = "LEFT"
	addonpref().xx_active_side = 7

def get_name(bone):
	return bone

def get_symm_name(bone):
	#first check if last digit are .xxx with [dot] and then xxx is integer
	end_name = ""
	if bone[len(bone)-4:len(bone)-3] == '.' and bone[len(bone)-3:].isdigit():
		end_pos = len(bone) - 4
		end_name = bone[len(bone)-4:]
	else:
		end_pos = len(bone)

	#construct dict for each length of potential side
	side_len = {}
	sides = addonpref().xx_sides
	for side in sides:
		if len(side.name_R) in side_len.keys():
			side_len[len(side.name_R)].append((side.name_R, side.name_L))
		else:
			side_len[len(side.name_R)] = []
			side_len[len(side.name_R)].append((side.name_R, side.name_L))
		if len(side.name_L) in side_len.keys():
			side_len[len(side.name_L)].append((side.name_L, side.name_R))
		else:
			side_len[len(side.name_L)] = []
			side_len[len(side.name_L)].append((side.name_L, side.name_R))

	for side_l in side_len.keys():
		if bone[end_pos-side_l:end_pos] in [name[0] for name in side_len[side_l]]:
			return bone[:end_pos-side_l] + side_len[side_l][[name[0] for name in side_len[side_l]].index(bone[end_pos-side_l:end_pos])][1] + end_name
	return bone


from .ui_panel import *
def update_panel():
	unregister_class_panels()
	change_panel_tab()
	register_panels()

def update_panel_cb(self, context):
	update_panel()
