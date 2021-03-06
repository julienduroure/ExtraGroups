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
#	Copyright 2016-2021 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################
import bpy
import bpy_extras
import json
import sys
import datetime
from .utils import *

class POSE_OT_jueg_export_to_file(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    """Export to file"""
    bl_idname = "jueg.export_to_file"
    bl_label = "Export To File"

    @classmethod
    def poll(self, context):
        return (context.object and
            context.object.type == 'ARMATURE' and
            context.mode == 'POSE')

    filename_ext = ".txt"

    filter_glob : bpy.props.StringProperty(default="*.txt", options={'HIDDEN'}, maxlen=255,)


    def execute(self, context):
        armature = context.object
        data = {}
        data['version'] = sys.modules['ExtraGroups'].bl_info['version']
        data['rig_object'] = armature.name
        data['rig_armature'] = armature.data.name
        data['generation_date'] = str(datetime.datetime.now())
        data['options'] = {}
        data['options']['popup_line_nb'] = armature.jueg_popup_lines_nb
        data['options']['name_clickable'] = armature.jueg_clickable_name_data.name_clickable
        data['options']['clickable_name_ops'] = armature.jueg_clickable_name_data.clickable_ops
        data['options']['clickable_name_mode'] = armature.jueg_clickable_name_data.clickable_mode
        data['options']['clickable_name_events_on'] = armature.jueg_clickable_name_data.clickable_events_on
        data['GroupTypes'] = []
        cpt_index = 0
        for grouptype in armature.jueg_grouptypelist:
            grouptype_ = {}
            grouptype_["name"] = grouptype.name
            grouptype_["groups"] = []
            for group in grouptype.group_ids:
                group_ = {}
                group_["name"] = group.name
                group_["color"] = str(group.color[0]) + "/" + str(group.color[1]) + "/" + str(group.color[2])
                if group.current_selection == True:
                    group_["current_selection"] = True
                else:
                    group_["current_selection"] = False
                    group_["bones"] = []
                    for bone in group.bone_ids:
                        group_["bones"].append(bone.name)
                    group_["keying"] = group.keying
                    group_["active_bone"] = group.active_bone
                    group_["orientation"] = group.orientation
                    # Gizmo
                    first = True
                    gizmo = ""
                    if group.manipulator[0] == True:
                        gizmo = "TRANSLATE"
                        first = False
                    if group.manipulator[1] == True:
                        if first == True:
                            gizmo = "ROTATE"
                            first = False
                        else:
                            gizmo = gizmo + "/ROTATE"
                    if group.manipulator[2] == True:
                        if first == True:
                            gizmo = "SCALE"
                            first = False
                        else:
                            gizmo = gizmo + "/SCALE"
                    group_["manipulator"] = gizmo
                grouptype_["groups"].append(group_)

            grouptype_["ops"] = []
            for ops_d in armature.jueg_grouptypelist[armature.jueg_active_grouptype].ops_display:
                ops = [e for i,e in enumerate(armature.jueg_extragroups_ops) if e.id == ops_d.id][0]
                tmp = {}
                tmp["ops"] = ops.id
                tmp["label"] = ops.name
                tmp["active"] = ops_d.display
                # Event management
                tmp["events"] = []
                if ops.event_manage == True:
                    for event in ops.events:
                        ev = {}
                        ev["label"] = event.label
                        ev["mode"] = event.mode
                        ev["event"] = event.event
                        ev["solo"] = event.solo
                        ev["active"] = event.active
                        ev["mirror"] = event.mirror
                        tmp["events"].append(ev)
                grouptype_["ops"].append(tmp)

            data['GroupTypes'].append(grouptype_)
            cpt_index = cpt_index + 1

        f = open(self.filepath, 'w', encoding='utf-8')
        f.write(json.dumps(data))
        f.close()

        return {'FINISHED'}

def register():
    bpy.utils.register_class(POSE_OT_jueg_export_to_file)

def unregister():
    bpy.utils.unregister_class(POSE_OT_jueg_export_to_file)
