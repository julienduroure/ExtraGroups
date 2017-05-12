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

from .globs import *
from .utils import *


class POSE_OT_jueg_popup(bpy.types.Operator):
    bl_idname = "extragroups.popup"
    bl_label  = "ExtraGroups"

    def check(self, context):
        return True

    def draw(self, context):
        layout = self.layout
        armature = context.object

        jueg_active_grouptype = armature.jueg_grouptypelist[armature.jueg_active_grouptype]

        if addonpref().multitype ==  True and len(armature.jueg_grouptypelist) > 1:
            row = layout.row()
            if addonpref().xx_popup_display_multitype == False:
                row.operator("extragroups.popup_toggle_multitype", text='', icon='TRIA_RIGHT')
            else:
                row.operator("extragroups.popup_toggle_multitype", text='', icon='TRIA_DOWN')
                row = layout.row()
                row.template_list("POSE_UL_jueg_grouptype", "", armature, "jueg_grouptypelist", armature, "jueg_active_grouptype")

        row = layout.row()
        row.template_list("POSE_UL_jueg_bonegroup", "", jueg_active_grouptype, "group_ids", jueg_active_grouptype, "active_bonegroup", rows=armature.jueg_popup_lines_nb)

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)

    @classmethod
    def poll(self, context):
        armature = context.object
        return check_addon_update_needed() == False and addonpref().enable_popup == True and len(armature.jueg_grouptypelist) > 0 and len(armature.jueg_grouptypelist[armature.jueg_active_grouptype].group_ids) > 0

class POSE_OT_jueg_popup_toggle_multitype(bpy.types.Operator):
    bl_idname = "extragroups.popup_toggle_multitype"
    bl_label  = 'Toggle Multitype display in popup'

    def execute(self, context):
        addonpref().xx_popup_display_multitype = not addonpref().xx_popup_display_multitype
        return {'FINISHED'}


def register():
    bpy.utils.register_class(POSE_OT_jueg_popup_toggle_multitype)
    bpy.utils.register_class(POSE_OT_jueg_popup)

def unregister():
    bpy.utils.unregister_class(POSE_OT_jueg_popup)
    bpy.utils.unregister_class(POSE_OT_jueg_popup_toggle_multitype)
