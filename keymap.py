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

from .ui_popup import *

KEYMAPS = []

def register():
	# register keymaps

	wm = bpy.context.window_manager
	km = wm.keyconfigs.active.keymaps['Pose']

	kmi = km.keymap_items.new(POSE_OT_jueg_popup.bl_idname, 'Q', 'PRESS', shift=True)
	KEYMAPS.append((km, kmi))

def unregister():
	for km, kmi in KEYMAPS:
		km.keymap_items.remove(kmi)
	KEYMAPS.clear()
