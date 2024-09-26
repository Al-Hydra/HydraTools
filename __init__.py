# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Hydra Tools",
    "author" : "HydraBladeZ, Dei",
    "description" : "",
    "blender" : (4, 2, 0),
    "version" : (1, 1, 5),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy
from . Panels import (ColProperty, Panel_Main, Panel_Armature, Panel_Material, Panel_Swap,  Panel_misc,
                     RetargetProperty,RetargetPanel #Panel_dict, BoneList, DICT_UL_BoneList,
                     )

from . Operators import (RemoveLOD, AddVertColors, RemoveVertColors,
    PaintVertexColors, ApplyRestPose, RemoveCharCode, RenameBones, AddCharCode,
    StormIK, FixNames, ArmatureModifier, Swap_Character_Code,Replace_Mats,
    Duplicate_XFBIN_Mat, Copy_Bone_Pos, CreateClone, #CreateBoneList, ExportDict,
    RemakeShaders, Create_bod1_f, ToDmgBody,ToRegularBody, RetargetStormAnim, RetargetAllStormAnims, CloneAnmObject,
    CorrectAnmNames)

classes = (Panel_Main, Panel_Armature, Panel_misc, Panel_Swap,
    RemoveLOD, ColProperty, AddVertColors, RemoveVertColors,PaintVertexColors,
    ApplyRestPose, RemoveCharCode, RenameBones, AddCharCode, StormIK, FixNames,
    ArmatureModifier, Swap_Character_Code,Replace_Mats, Duplicate_XFBIN_Mat,
    Copy_Bone_Pos, CreateClone, # Panel_dict, BoneList, CreateBoneList, DICT_UL_BoneList, ExportDict,
    RemakeShaders, Create_bod1_f, ToDmgBody,ToRegularBody, RetargetProperty, RetargetPanel, RetargetStormAnim,
    RetargetAllStormAnims, CloneAnmObject, CorrectAnmNames)

def get_col_armatures(self, object):
    colprop = bpy.context.scene.col_prop
    collection = bpy.data.collections.get(colprop.collections)
    if collection is None:
        return []
    else:
        return [ob for ob in collection.objects if ob.type == 'ARMATURE']

def search_armature(self, object):
    colprop = bpy.context.scene.col_prop
    return object.type == 'ARMATURE' and object.name != colprop.armatures

def main_poll(self, object):
    
    return object.type == 'ARMATURE' and object != bpy.context.scene.target_armature

def target_poll(self, object):
    armature_main = bpy.context.scene.main_armature
    return object.type == 'ARMATURE' and object != armature_main

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.col_armatures = bpy.props.PointerProperty(type=bpy.types.Object, poll=get_col_armatures)
    bpy.types.Scene.armaturelist = bpy.props.PointerProperty(type=bpy.types.Object, poll=search_armature)
    bpy.types.Scene.main_armature = bpy.props.PointerProperty(type=bpy.types.Object, poll=main_poll)
    bpy.types.Scene.target_armature = bpy.props.PointerProperty(type=bpy.types.Object, poll=target_poll)
    bpy.types.Scene.bone_index = bpy.props.IntProperty()
    bpy.types.Scene.col_prop = bpy.props.PointerProperty(type = ColProperty)
    bpy.types.Scene.retarget_prop = bpy.props.PointerProperty(type = RetargetProperty)
    #bpy.types.Scene.bone_dict_props = bpy.props.PointerProperty(type = BoneList)
    #ColProperty.bone_dict = bpy.props.CollectionProperty(type = BoneList)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.armaturelist
    del bpy.types.Scene.main_armature
    del bpy.types.Scene.target_armature
    #del bpy.types.Scene.bone_index
    del bpy.types.Scene.col_prop
    del bpy.types.Scene.retarget_prop
    #del bpy.types.Scene.bone_dict_props
    #del ColProperty.bone_dict
