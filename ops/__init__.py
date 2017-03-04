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

if "bpy" in locals():
	import imp
	imp.reload(ops_bonelock)
	imp.reload(ops_bonemute)
	imp.reload(ops_changevisibility)
	imp.reload(ops_keyframing)
	imp.reload(ops_motionpath)
	imp.reload(ops_props_change)
	imp.reload(ops_restrict_select)
	imp.reload(ops_select)
else:
	from .ops_bonelock import *
	from .ops_bonemute import *
	from .ops_changevisibility import *
	from .ops_keyframing import *
	from .ops_motionpath import *
	from .ops_props_change import *
	from .ops_restrict_select import *
	from .ops_select import *


import bpy


def register():
	bpy.utils.register_class(POSE_OT_jueg_changevisibility)
	bpy.utils.register_class(POSE_OT_jueg_bonemute)
	bpy.utils.register_class(POSE_OT_jueg_restrict_select)
	bpy.utils.register_class(POSE_OT_jueg_select)
	bpy.utils.register_class(POSE_OT_jueg_props_change)
	bpy.utils.register_class(POSE_OT_jueg_bonelock)
	bpy.utils.register_class(POSE_MT_keyframing)
	bpy.utils.register_class(POSE_OT_jueg_keyframing_after_menu)
	bpy.utils.register_class(POSE_OT_jueg_keyframing)
	bpy.utils.register_class(POSE_OT_jueg_motionpath)

def unregister():
	bpy.utils.unregister_class(POSE_OT_jueg_changevisibility)
	bpy.utils.unregister_class(POSE_OT_jueg_bonemute)
	bpy.utils.unregister_class(POSE_OT_jueg_restrict_select)
	bpy.utils.unregister_class(POSE_OT_jueg_select)
	bpy.utils.unregister_class(POSE_OT_jueg_props_change)
	bpy.utils.unregister_class(POSE_OT_jueg_bonelock)
	bpy.utils.unregister_class(POSE_MT_keyframing)
	bpy.utils.unregister_class(POSE_OT_jueg_keyframing_after_menu)
	bpy.utils.unregister_class(POSE_OT_jueg_keyframing)
	bpy.utils.unregister_class(POSE_OT_jueg_motionpath)
