import collections
import bpy, json, os
from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatVectorProperty
from bpy.types import (Operator)
from bpy_extras.io_utils import ImportHelper, ExportHelper
from rna_prop_ui import PropertyPanel
from os import listdir
from os.path import isfile, join
class RemoveLOD(bpy.types.Operator):
    bl_idname = "object.remove_lod"
    bl_label = "Remove LOD"
    bl_description = ("This button will remove LOD meshes and adjust the necessary values")
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.collections != "":
            return True
        else:
            return False
        
    def execute(self, context):
        
        colprop = bpy.context.scene.col_prop
        collection = bpy.data.collections[colprop.collections]
        armature_obj = bpy.data.objects[colprop.armatures]
            
        lod = {"_lod1", "_lod2", "lod01", "_LOD1", "_LOD2",
        "_shadow", "_blur0 shadow", "_blur0 shadow01"}

        #delete any mesh that contains any of the strings in the list above
        for obj in collection.objects:
            if any(x in obj.name for x in lod):
                bpy.data.objects.remove(obj)
            
        #set LOD levels to 1
        armature_obj.xfbin_clump_data.coord_flag0 = 1
        armature_obj.xfbin_clump_data.coord_flag1 = 1

        #Clear model groups then add 1 model group with the correct settings
        armature_obj.xfbin_clump_data.model_groups.clear()
        g = armature_obj.xfbin_clump_data.model_groups.add()
        g.name = 'Group'
        for child in armature_obj.children:
            gm = g.models.add()
            gm.object = child

        return {'FINISHED'}


class AddVertColors(Operator):
    bl_idname = "object.add_v_colors"
    bl_label = "Add Vertex Colors"
    bl_description = ('This button will add vertex colors to all the meshes\n'
    'in the active collection')
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.collections != "":
            return True
        else:
            return False
        
    def execute(self, context):
        
        collections = bpy.data.collections
        colprop = bpy.context.scene.col_prop
        for obj in collections[colprop.collections].objects:
            if obj.type == 'MESH' and len(obj.data.vertex_colors) == 0:
                    obj.data.vertex_colors.new('Colors')
            else:
                self.report({'INFO'}, f'{obj.name} Has at least 1 vertex colors layer')
        return {'FINISHED'}

class RemoveVertColors(Operator):
    bl_idname = "object.remove_v_colors"
    bl_label = "Clear Vertex Colors"
    bl_description = ('This button will remove all the vertex colors layers in meshes\n'
    "in the active collection")
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.collections != "":
            return True
        else:
            return False
        
    def execute(self, context):
        
        collections = bpy.data.collections
        colprop = bpy.context.scene.col_prop
        for obj in collections[colprop.collections].objects:
            if (obj.type == 'MESH'):
                for vc in obj.data.vertex_colors:
                    obj.data.vertex_colors.remove(vc)  
                    self.report({'INFO'}, f'Vertex Colors layers in {obj.name} are removed')
        return {'FINISHED'}

class PaintVertexColors(Operator):
    bl_idname = "object.paint_v_colors"
    bl_label = "Paint Vertex Colors"
    bl_description = ('This button will change the color of the active vertex color layer\n'
    'for meshes in the active collection using the color you choose.\n\n'
    "NOTE: A vertex color layer will be added if there isn't one already")
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.collections != "":
            return True
        else:
            return False
        
    def execute(self, context):
        
        collections = bpy.data.collections
        colprop = bpy.context.scene.col_prop
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in collections[colprop.collections].objects:
            if (obj.type == 'MESH') and obj.data.vertex_colors[0]:
                for vc in obj.data.vertex_colors[0].data:
                    color = colprop.VertColorPick
                    vc.color[0] = color[0]
                    vc.color[1] = color[1]
                    vc.color[2] = color[2]
                    vc.color[3] = 1
            
        return {'FINISHED'}        



class ApplyRestPose(Operator):
    bl_idname = "object.applypose"
    bl_label = "Apply Rest Pose"
    bl_description = ('This button will Apply the current pose as rest pose')
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.armatures != "":
            return True
        else:
            return False
        
    def execute(self, context):
        
        collections = bpy.data.collections
        colprop = bpy.context.scene.col_prop
        selected = bpy.context.selected_objects
        a_object = bpy.data.objects[colprop.armatures]
                        
        for obj in bpy.data.objects[colprop.armatures].children_recursive:
            if obj.type == 'MESH':
                mod = obj.modifiers.new(type='ARMATURE', name='ArmatureToApply')
                mod.object = bpy.data.objects[colprop.armatures]
                context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply( modifier = "ArmatureToApply" )

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.data.objects[colprop.armatures]
        bpy.ops.object.posemode_toggle()
        bpy.ops.pose.armature_apply(selected=False)
        bpy.ops.object.posemode_toggle()

        return {'FINISHED'}
        
        
class RemoveCharCode(Operator):
    bl_idname = "object.remove_char_code"
    bl_label = "Remove ID"
    bl_description = ('This button will remove character ID (XXXX0XT0) for all the bones\n'
    "Example: '2nrt00t0 spine' becomes 'Spine' this is useful for mirroring and weight painting")
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.armatures != "":
            return True
        else:
            return False
    
        
    def execute(self, context):
        colprop = bpy.context.scene.col_prop
        a_object = bpy.data.objects[colprop.armatures]
        armature = bpy.data.armatures[colprop.armatures]
        ab = bpy.data.objects[colprop.armatures].data.bones
        char_id = a_object.data.bones[1].name
        nl = len(armature.bones[1].name)
        nc = len(armature.bones[1].name[:-4])
        filtered_bones = [
        'asianimel01', 'asianimel02', 'asianimel03', 'asianimel04','asianimel',
        'asianimer01', 'asianimer02', 'asianimer03', 'asianimer04','asianimer',
        'udeanmr01', 'udeanmr02', 'udeanmr03', 'udeanmr04', 'udeanmr',
        'udeanml01', 'udeanml02', 'udeanml03', 'udeanml04', 'udeanml']  
        
        for bone in [*a_object.data.bones]:
            if any(x in bone.name for x in filtered_bones):
                i = bone.name.find('_')
                bone.name = bone.name[i:]
            
            elif bone.name[0:nl] == char_id and len(bone.name) > nl and bone.name:
                bone.name = bone.name[nl+1:]
                #self.report({'INFO'}, f'ID:{char_id} Removed from {bone.name}')
                
        #re-sets armatures modifier object to fix a bug in blender 3.0
        '''for obj in bpy.data.objects[colprop.armatures].children_recursive:
            if obj.type == 'MESH':
                mod = [m for m in obj.modifiers if m.type == 'ARMATURE']
                mod[0].object = bpy.data.objects[colprop.armatures]'''

        return {'FINISHED'}
    
class RenameBones(Operator, ImportHelper):
    bl_idname = "object.rename_script"
    bl_label = "Rename Bones"
    bl_description = ("Rename bone names using a bone name dictionary.\n"
    "This is useful when you want to transfer rigs")
    
    filter_glob: StringProperty(
    default='*.json;',
    options={'HIDDEN'}
)


    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.armatures != "":
            return True
        else:
            return False
        
    def execute(self, context):
        filename, extension = os.path.splitext(self.filepath)
        with open(self.filepath,'r') as dictionary: 
            bone_dict = json.load(dictionary)
        colprop = bpy.context.scene.col_prop
        a_object = bpy.data.objects[colprop.armatures]    
        for bone in [*a_object.data.bones]:
            if bone.name in bone_dict.keys():
                if bone_dict[bone.name] != '':
                    bone.name = bone_dict[bone.name]
        return {'FINISHED'}


class AddCharCode(Operator):
    bl_idname = "object.add_char_code"
    bl_label = "Add ID"
    bl_description = ('This button will add the character ID back after removing it')
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.armatures != "":
            return True
        else:
            return False
        
    def execute(self, context):
        colprop = bpy.context.scene.col_prop
        a_object = bpy.data.objects[colprop.armatures]
        armature = bpy.data.armatures[colprop.armatures]
        ab = bpy.data.objects[colprop.armatures].data.bones
        clumpdata = a_object.xfbin_clump_data
        char_id = a_object.data.bones[1].name
        nl = len(armature.bones[1].name)
        nc = len(armature.bones[1].name[:-4])
        filter_char_id = char_id[:4] + '_'
        filtered_bones = [
        'asianimel01', 'asianimel02', 'asianimel03', 'asianimel04','asianimel',
        'asianimer01', 'asianimer02', 'asianimer03', 'asianimer04','asianimer',
        'udeanmr01', 'udeanmr02', 'udeanmr03', 'udeanmr04', 'udeanmr',
        'udeanml01', 'udeanml02', 'udeanml03', 'udeanml04', 'udeanml']  
        #filtered_bones = [filter_char_id + x for x in filtered_bones]
        if ab[0].name[0:nl] == char_id and ab[0].name not in filtered_bones:
            self.report({'WARNING'}, "You need to remove the character ID first!")

        for bone in [*a_object.data.bones]:
            if any(x in bone.name for x in filtered_bones) and bone.name.split('_')[0] == '':
                bone.name = armature.name[:4] + "_" + bone.name
            elif any(x in bone.name for x in filtered_bones) and len(bone.name.split('_')[0]) == len(armature.name):
                bone.name = armature.name[:] + "_" + bone.name
            elif bone.name[0:nl] != char_id and bone.name:
                #self.report({'INFO'}, f"ID:({char_id}) added to ({bone.name})")
                bone.name = char_id + ' ' + bone.name
        
        return {'FINISHED'}

class Blend_Mode_Opaque(Operator):
    bl_idname = "object.opaque"
    bl_label = "Set blend mode to opaque"
    bl_description = ('This button will remove all the vertex colors layers in meshes\n'
    "in the active collection")
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.collections != "":
            return True
        else:
            return False
        
    def execute(self, context):
        
        collections = bpy.data.collections
        colprop = bpy.context.scene.col_prop
        bpy.ops.object.select_all(action='DESELECT')
        for obj in collections[colprop.collections].objects:
            if (obj.type == 'MESH'):
                obj.hide_set(False)
                obj.select_set(True)
    
        for obj in bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = obj
            bpy.context.object.active_material.blend_method = 'OPAQUE'
        return {'FINISHED'}

class StormIK(Operator):
    bl_idname = "object.ik"
    bl_label = "STORM IK"
    bl_description = ('Add IK bones and Constraints.\n'
    'WARNING: THIS WILL CAUSE YOUR MODEL TO LOOK DEFORMED IF EXPORTED AS XFBIN. THIS MUST ONLY BE USED FOR POSING AND ANIMATIONS ONLY.')
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.armatures != "":
            return True
        else:
            return False
        
    def execute(self, context):
        
        colprop = bpy.context.scene.col_prop

        bones = ['r forearm', 'r upperarm', 'r hand', 'r finger01', 'r finger02',
        'r finger11', 'r finger12', 'r finger21', 'r finger22', 'r finger31',
        'r finger32', 'r finger41', 'r finger42', 'l forearm', 'l upperarm',
        'l hand', 'l finger01', 'l finger02', 'l finger11', 'l finger12', 'l finger21',
        'l finger22', 'l finger31', 'l finger32', 'l finger41', 'l finger42',
        'left wearnub','front wearnub', 'back wearnub', 'right wearnub', 'l calf',
        'l foot', 'l toe0', 'r calf', 'r foot', 'r toe0', 'bustnub', 'scarfnub',
        'hair_bl02', 'hair_bc03', 'hair_br02', 'hair_fl02', 'hair_fr02', 'tongue04',
        'tongue03', 'tongue02', 'spine', 'spine1', 'neck']

        armature_data = bpy.data.objects[colprop.armatures].data
        armature = bpy.data.objects[colprop.armatures]
        collection = bpy.data.collections[colprop.collections]
        
        if armature_data.name != armature.name:
            armature_data.name = armature.name


        editbone = bpy.data.armatures[colprop.armatures].edit_bones

        bpy.ops.object.remove_char_code()
        bpy.context.view_layer.objects.active = bpy.data.objects[colprop.armatures]
        if bpy.context.mode != 'EDIT_ARMATURE':
            bpy.ops.object.editmode_toggle()

        for b in bones:
            if b in editbone:
                editbone[b].parent.tail = editbone[b].head
                editbone[b].use_connect = True
                print(f"Connected ({b}) bone")

        #Re-Parent bones
        #------------------------------------------------------------
        editbone['l clavicle'].parent = editbone['spine1']
        editbone['r clavicle'].parent = editbone['spine1']
        editbone['l thigh'].parent = editbone['pelvis']
        editbone['r thigh'].parent = editbone['pelvis']

        #Add IK bones
        #------------------------------------------------------------
        #Head
        head = editbone.new('HeadTrack')
        head.use_deform = False
        head.head.zx = editbone['head'].head.zx
        head.head.y = -0.55
        head.tail.zx = editbone['head'].head.zx
        head.tail.y = -0.65
        #------------------------------------------------------------
        #Feet
        l_foot = editbone.new('L Foot IK')
        l_foot.use_deform = False
        l_foot.head = editbone['l foot'].head
        l_foot.tail.zx = editbone['l foot'].head.zx
        l_foot.tail.y = editbone['l foot'].head.y + 0.1
        editbone['l foot'].use_connect = False
        editbone['l foot'].parent = editbone['L Foot IK']

        r_foot = editbone.new('R Foot IK')
        r_foot.use_deform = False
        r_foot.head = editbone['r foot'].head
        r_foot.tail.zx = editbone['r foot'].head.zx
        r_foot.tail.y = editbone['r foot'].head.y + 0.1
        editbone['r foot'].use_connect = False
        editbone['r foot'].parent = editbone['R Foot IK']
        #------------------------------------------------------------
        #Knees
        l_knee = editbone.new('L Knee IK')
        l_knee.use_deform = False
        l_knee.head.zx = editbone['l calf'].head.zx
        l_knee.head.y = -0.55
        l_knee.tail.zx = editbone['l calf'].head.zx
        l_knee.tail.y = -0.65
        editbone['L Knee IK'].parent = editbone['L Foot IK']
        r_knee = editbone.new('R Knee IK')
        r_knee.use_deform = False
        r_knee.head.zx = editbone['r calf'].head.zx
        r_knee.head.y = -0.55
        r_knee.tail.zx = editbone['r calf'].head.zx
        r_knee.tail.y = -0.65
        editbone['R Knee IK'].parent = editbone['R Foot IK']
        #------------------------------------------------------------
        #Elbows
        l_elbow = editbone.new('L Elbow IK')
        l_elbow.use_deform = False
        l_elbow.head.zx = editbone['l forearm'].head.zx
        l_elbow.head.y = 0.35
        l_elbow.tail.zx = editbone['l forearm'].head.zx
        l_elbow.tail.y = 0.45

        r_elbow = editbone.new('R Elbow IK')
        r_elbow.use_deform = False
        r_elbow.head.zx = editbone['r forearm'].head.zx
        r_elbow.head.y = 0.35
        r_elbow.tail.zx = editbone['r forearm'].head.zx
        r_elbow.tail.y = 0.45
        #-------------------------------------------------------------
        #Hands
        l_hand = editbone.new('L Hand IK')
        l_hand.use_deform = False
        l_hand.head = editbone['l hand'].head
        l_hand.tail.y = editbone['l hand'].head.y
        l_hand.tail.z = editbone['l hand'].head.z + -0.05
        l_hand.tail.x = editbone['l hand'].head.x + 0.05
        editbone['l hand'].tail.x += 0.015
        editbone['l hand'].tail.z += -0.015
        editbone['L Hand IK'].roll = editbone['l hand'].roll

        r_hand = editbone.new('R Hand IK')
        r_hand.use_deform = False
        r_hand.head= editbone['r hand'].head
        r_hand.tail.y = editbone['r hand'].head.y
        r_hand.tail.z = editbone['r hand'].head.z + -0.05
        r_hand.tail.x = editbone['r hand'].head.x + -0.05
        editbone['r hand'].tail.x += -0.015
        editbone['r hand'].tail.z += -0.015
        editbone['R Hand IK'].roll = editbone['r hand'].roll
        #-------------------------------------------------------------
        #Spine

        spine = editbone.new('Spine IK')
        spine.use_deform = False
        spine.head = editbone['spine1'].head
        spine.tail.xz = editbone['spine1'].head.xz
        spine.tail.y = editbone['spine1'].head.y + 0.1

        editbone['spine1'].use_connect = False
        editbone['spine1'].parent = editbone['Spine IK']

        bpy.ops.object.editmode_toggle()
        #-------------------------------------------------------------
        #IK Constraints
        bpy.ops.object.posemode_toggle()
        posebone = bpy.data.objects[colprop.armatures].pose.bones

        l_calf_ik = posebone['l calf'].constraints.new('IK')
        l_calf_ik.target = bpy.data.objects[colprop.armatures]
        l_calf_ik.subtarget = 'L Foot IK'
        l_calf_ik.pole_target = bpy.data.objects[colprop.armatures]
        l_calf_ik.pole_subtarget = 'L Knee IK'
        l_calf_ik.pole_angle = -0.462512
        l_calf_ik.chain_count = 2

        r_calf_ik = posebone['r calf'].constraints.new('IK')
        r_calf_ik.target = bpy.data.objects[colprop.armatures]
        r_calf_ik.subtarget = 'R Foot IK'
        r_calf_ik.pole_target = bpy.data.objects[colprop.armatures]
        r_calf_ik.pole_subtarget = 'R Knee IK'
        r_calf_ik.pole_angle = 0.462512
        r_calf_ik.chain_count = 2
        #-------------------------------------------------------------
        l_forearm_ik = posebone['l forearm'].constraints.new('IK')
        l_forearm_ik.target = bpy.data.objects[colprop.armatures]
        l_forearm_ik.subtarget = 'L Hand IK'
        l_forearm_ik.pole_target = bpy.data.objects[colprop.armatures]
        l_forearm_ik.pole_subtarget = 'L Elbow IK'
        l_forearm_ik.pole_angle = -3.14159
        l_forearm_ik.chain_count = 2

        r_forearm_ik = posebone['r forearm'].constraints.new('IK')
        r_forearm_ik.target = bpy.data.objects[colprop.armatures]
        r_forearm_ik.subtarget = 'R Hand IK'
        r_forearm_ik.pole_target = bpy.data.objects[colprop.armatures]
        r_forearm_ik.pole_subtarget = 'R Elbow IK'
        r_forearm_ik.pole_angle = 3.14159
        r_forearm_ik.chain_count = 2

        #Spine
        #-------------------------------------------------------------
        spine_ik = posebone['spine'].constraints.new('IK')
        spine_ik.target = bpy.data.objects[colprop.armatures]
        spine_ik.subtarget = 'Spine IK'
        spine_ik.chain_count = 1

        #-------------------------------------------------------------
        #DampedTrack

        head_const = posebone['head'].constraints.new('DAMPED_TRACK')
        head_const.target = bpy.data.objects[colprop.armatures]
        head_const.subtarget = 'HeadTrack'

        #-------------------------------------------------------------
        #Copy Location constraints

        l_foot_const = posebone['l foot'].constraints.new('COPY_LOCATION')
        l_foot_const.target = bpy.data.objects[colprop.armatures]
        l_foot_const.subtarget = 'l calf'
        l_foot_const.head_tail = 1

        r_foot_const = posebone['r foot'].constraints.new('COPY_LOCATION')
        r_foot_const.target = bpy.data.objects[colprop.armatures]
        r_foot_const.subtarget = 'r calf'
        r_foot_const.head_tail = 1

        spine1_const = posebone['spine1'].constraints.new('COPY_LOCATION')
        spine1_const.target = bpy.data.objects[colprop.armatures]
        spine1_const.subtarget = 'spine'
        spine1_const.head_tail = 1

        #-------------------------------------------------------------
        #Copy Rotation constraints
        l_forearm_const = posebone['l hand'].constraints.new('COPY_ROTATION')
        l_forearm_const.target = bpy.data.objects[colprop.armatures]
        l_forearm_const.subtarget = 'L Hand IK'

        r_forearm_const = posebone['r hand'].constraints.new('COPY_ROTATION')
        r_forearm_const.target = bpy.data.objects[colprop.armatures]
        r_forearm_const.subtarget = 'R Hand IK'
        #-------------------------------------------------------------
        l_finger02_const = posebone['l finger02'].constraints.new('COPY_ROTATION')
        l_finger02_const.target = bpy.data.objects[colprop.armatures]
        l_finger02_const.subtarget = 'l finger01'
        l_finger02_const.use_x = False
        l_finger02_const.use_y = False
        l_finger02_const.use_z = True
        l_finger02_const.mix_mode = 'ADD'
        l_finger02_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_finger02_const.owner_space = 'LOCAL'
        #-------------------------------------------------------------
        l_finger11_const = posebone['l finger11'].constraints.new('COPY_ROTATION')
        l_finger11_const.target = bpy.data.objects[colprop.armatures]
        l_finger11_const.subtarget = 'l finger1'
        l_finger11_const.use_x = True
        l_finger11_const.use_y = False
        l_finger11_const.use_z = False
        l_finger11_const.mix_mode = 'ADD'
        l_finger11_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_finger11_const.owner_space = 'LOCAL'

        l_finger12_const = posebone['l finger12'].constraints.new('COPY_ROTATION')
        l_finger12_const.target = bpy.data.objects[colprop.armatures]
        l_finger12_const.subtarget = 'l finger11'
        l_finger12_const.use_x = False
        l_finger12_const.use_y = False
        l_finger12_const.use_z = True
        l_finger12_const.mix_mode = 'ADD'
        l_finger12_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_finger12_const.owner_space = 'LOCAL'
        #-------------------------------------------------------------
        l_finger21_const = posebone['l finger21'].constraints.new('COPY_ROTATION')
        l_finger21_const.target = bpy.data.objects[colprop.armatures]
        l_finger21_const.subtarget = 'l finger2'
        l_finger21_const.use_x = True
        l_finger21_const.use_y = False
        l_finger21_const.use_z = False
        l_finger21_const.mix_mode = 'ADD'
        l_finger21_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_finger21_const.owner_space = 'LOCAL'

        l_finger22_const = posebone['l finger22'].constraints.new('COPY_ROTATION')
        l_finger22_const.target = bpy.data.objects[colprop.armatures]
        l_finger22_const.subtarget = 'l finger21'
        l_finger22_const.use_x = False
        l_finger22_const.use_y = False
        l_finger22_const.use_z = True
        l_finger22_const.mix_mode = 'ADD'
        l_finger22_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_finger22_const.owner_space = 'LOCAL'
        #-------------------------------------------------------------
        l_finger31_const = posebone['l finger31'].constraints.new('COPY_ROTATION')
        l_finger31_const.target = bpy.data.objects[colprop.armatures]
        l_finger31_const.subtarget = 'l finger3'
        l_finger31_const.use_x = True
        l_finger31_const.use_y = False
        l_finger31_const.use_z = False
        l_finger31_const.mix_mode = 'ADD'
        l_finger31_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_finger31_const.owner_space = 'LOCAL'

        l_finger32_const = posebone['l finger32'].constraints.new('COPY_ROTATION')
        l_finger32_const.target = bpy.data.objects[colprop.armatures]
        l_finger32_const.subtarget = 'l finger31'
        l_finger32_const.use_x = False
        l_finger32_const.use_y = False
        l_finger32_const.use_z = True
        l_finger32_const.mix_mode = 'ADD'
        l_finger32_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_finger32_const.owner_space = 'LOCAL'
        #-------------------------------------------------------------
        l_finger41_const = posebone['l finger41'].constraints.new('COPY_ROTATION')
        l_finger41_const.target = bpy.data.objects[colprop.armatures]
        l_finger41_const.subtarget = 'l finger4'
        l_finger41_const.use_x = True
        l_finger41_const.use_y = False
        l_finger41_const.use_z = False
        l_finger41_const.mix_mode = 'ADD'
        l_finger41_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_finger41_const.owner_space = 'LOCAL'

        l_finger42_const = posebone['l finger42'].constraints.new('COPY_ROTATION')
        l_finger42_const.target = bpy.data.objects[colprop.armatures]
        l_finger42_const.subtarget = 'l finger41'
        l_finger42_const.use_x = False
        l_finger42_const.use_y = False
        l_finger42_const.use_z = True
        l_finger42_const.mix_mode = 'ADD'
        l_finger42_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_finger42_const.owner_space = 'LOCAL'
        #-------------------------------------------------------------
        r_finger02_const = posebone['r finger02'].constraints.new('COPY_ROTATION')
        r_finger02_const.target = bpy.data.objects[colprop.armatures]
        r_finger02_const.subtarget = 'r finger01'
        r_finger02_const.use_x = False
        r_finger02_const.use_y = False
        r_finger02_const.use_z = True
        r_finger02_const.mix_mode = 'ADD'
        r_finger02_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_finger02_const.owner_space = 'LOCAL'
        #-------------------------------------------------------------
        r_finger11_const = posebone['r finger11'].constraints.new('COPY_ROTATION')
        r_finger11_const.target = bpy.data.objects[colprop.armatures]
        r_finger11_const.subtarget = 'r finger1'
        r_finger11_const.use_x = True
        r_finger11_const.use_y = False
        r_finger11_const.use_z = False
        r_finger11_const.mix_mode = 'ADD'
        r_finger11_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_finger11_const.owner_space = 'LOCAL'

        r_finger12_const = posebone['r finger12'].constraints.new('COPY_ROTATION')
        r_finger12_const.target = bpy.data.objects[colprop.armatures]
        r_finger12_const.subtarget = 'r finger11'
        r_finger12_const.use_x = False
        r_finger12_const.use_y = False
        r_finger12_const.use_z = True
        r_finger12_const.mix_mode = 'ADD'
        r_finger12_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_finger12_const.owner_space = 'LOCAL'
        #-------------------------------------------------------------
        r_finger21_const = posebone['r finger21'].constraints.new('COPY_ROTATION')
        r_finger21_const.target = bpy.data.objects[colprop.armatures]
        r_finger21_const.subtarget = 'r finger2'
        r_finger21_const.use_x = True
        r_finger21_const.use_y = False
        r_finger21_const.use_z = False
        r_finger21_const.mix_mode = 'ADD'
        r_finger21_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_finger21_const.owner_space = 'LOCAL'

        r_finger22_const = posebone['r finger22'].constraints.new('COPY_ROTATION')
        r_finger22_const.target = bpy.data.objects[colprop.armatures]
        r_finger22_const.subtarget = 'r finger21'
        r_finger22_const.use_x = False
        r_finger22_const.use_y = False
        r_finger22_const.use_z = True
        r_finger22_const.mix_mode = 'ADD'
        r_finger22_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_finger22_const.owner_space = 'LOCAL'
        #-------------------------------------------------------------
        r_finger31_const = posebone['r finger31'].constraints.new('COPY_ROTATION')
        r_finger31_const.target = bpy.data.objects[colprop.armatures]
        r_finger31_const.subtarget = 'r finger3'
        r_finger31_const.use_x = True
        r_finger31_const.use_y = False
        r_finger31_const.use_z = False
        r_finger31_const.mix_mode = 'ADD'
        r_finger31_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_finger31_const.owner_space = 'LOCAL'

        r_finger32_const = posebone['r finger32'].constraints.new('COPY_ROTATION')
        r_finger32_const.target = bpy.data.objects[colprop.armatures]
        r_finger32_const.subtarget = 'r finger31'
        r_finger32_const.use_x = False
        r_finger32_const.use_y = False
        r_finger32_const.use_z = True
        r_finger32_const.mix_mode = 'ADD'
        r_finger32_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_finger32_const.owner_space = 'LOCAL'
        #-------------------------------------------------------------
        r_finger41_const = posebone['r finger41'].constraints.new('COPY_ROTATION')
        r_finger41_const.target = bpy.data.objects[colprop.armatures]
        r_finger41_const.subtarget = 'r finger4'
        r_finger41_const.use_x = True
        r_finger41_const.use_y = False
        r_finger41_const.use_z = False
        r_finger41_const.mix_mode = 'ADD'
        r_finger41_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_finger41_const.owner_space = 'LOCAL'

        r_finger42_const = posebone['r finger42'].constraints.new('COPY_ROTATION')
        r_finger42_const.target = bpy.data.objects[colprop.armatures]
        r_finger42_const.subtarget = 'r finger41'
        r_finger42_const.use_x = False
        r_finger42_const.use_y = False
        r_finger42_const.use_z = True
        r_finger42_const.mix_mode = 'ADD'
        r_finger42_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_finger42_const.owner_space = 'LOCAL'
        #-------------------------------------------------------------
        #Arm Twist Bones
        l_twist06_const = posebone['l arm bone06'].constraints.new('COPY_ROTATION')
        l_twist06_const.target = bpy.data.objects[colprop.armatures]
        l_twist06_const.subtarget = 'l hand'
        l_twist06_const.use_x = True
        l_twist06_const.use_y = False
        l_twist06_const.use_z = False
        l_twist06_const.mix_mode = 'ADD'
        l_twist06_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_twist06_const.owner_space = 'LOCAL'
        l_twist06_const.influence = 0.8
        #-------------------------------------------------------------
        l_twist05_const = posebone['l arm bone05'].constraints.new('COPY_ROTATION')
        l_twist05_const.target = bpy.data.objects[colprop.armatures]
        l_twist05_const.subtarget = 'l arm bone06'
        l_twist05_const.use_x = True
        l_twist05_const.use_y = False
        l_twist05_const.use_z = False
        l_twist05_const.mix_mode = 'ADD'
        l_twist05_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_twist05_const.owner_space = 'LOCAL'
        l_twist06_const.influence = 0.7
        #-------------------------------------------------------------
        l_twist04_const = posebone['l arm bone04'].constraints.new('COPY_ROTATION')
        l_twist04_const.target = bpy.data.objects[colprop.armatures]
        l_twist04_const.subtarget = 'l arm bone05'
        l_twist04_const.use_x = True
        l_twist04_const.use_y = False
        l_twist04_const.use_z = False
        l_twist04_const.mix_mode = 'ADD'
        l_twist04_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_twist04_const.owner_space = 'LOCAL'
        l_twist04_const.influence = 0.65
        #-------------------------------------------------------------
        l_twist03_const = posebone['l arm bone03'].constraints.new('COPY_ROTATION')
        l_twist03_const.target = bpy.data.objects[colprop.armatures]
        l_twist03_const.subtarget = 'l arm bone04'
        l_twist03_const.use_x = True
        l_twist03_const.use_y = False
        l_twist03_const.use_z = False
        l_twist03_const.mix_mode = 'ADD'
        l_twist03_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_twist03_const.owner_space = 'LOCAL'
        l_twist03_const.influence = 0.6
        #-------------------------------------------------------------
        l_twist02_const = posebone['l arm bone02'].constraints.new('COPY_ROTATION')
        l_twist02_const.target = bpy.data.objects[colprop.armatures]
        l_twist02_const.subtarget = 'l arm bone03'
        l_twist02_const.use_x = True
        l_twist02_const.use_y = False
        l_twist02_const.use_z = False
        l_twist02_const.mix_mode = 'ADD'
        l_twist02_const.target_space = 'LOCAL_OWNER_ORIENT'
        l_twist02_const.owner_space = 'LOCAL'
        l_twist02_const.influence = 0.5
        #-------------------------------------------------------------
        r_twist06_const = posebone['r arm bone06'].constraints.new('COPY_ROTATION')
        r_twist06_const.target = bpy.data.objects[colprop.armatures]
        r_twist06_const.subtarget = 'r hand'
        r_twist06_const.use_x = True
        r_twist06_const.use_y = False
        r_twist06_const.use_z = False
        r_twist06_const.mix_mode = 'ADD'
        r_twist06_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_twist06_const.owner_space = 'LOCAL'
        r_twist06_const.influence = 0.8
        #-------------------------------------------------------------
        r_twist05_const = posebone['r arm bone05'].constraints.new('COPY_ROTATION')
        r_twist05_const.target = bpy.data.objects[colprop.armatures]
        r_twist05_const.subtarget = 'r arm bone06'
        r_twist05_const.use_x = True
        r_twist05_const.use_y = False
        r_twist05_const.use_z = False
        r_twist05_const.mix_mode = 'ADD'
        r_twist05_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_twist05_const.owner_space = 'LOCAL'
        r_twist06_const.influence = 0.7
        #-------------------------------------------------------------
        r_twist04_const = posebone['r arm bone04'].constraints.new('COPY_ROTATION')
        r_twist04_const.target = bpy.data.objects[colprop.armatures]
        r_twist04_const.subtarget = 'r arm bone05'
        r_twist04_const.use_x = True
        r_twist04_const.use_y = False
        r_twist04_const.use_z = False
        r_twist04_const.mix_mode = 'ADD'
        r_twist04_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_twist04_const.owner_space = 'LOCAL'
        r_twist04_const.influence = 0.65
        #-------------------------------------------------------------
        r_twist03_const = posebone['r arm bone03'].constraints.new('COPY_ROTATION')
        r_twist03_const.target = bpy.data.objects[colprop.armatures]
        r_twist03_const.subtarget = 'r arm bone04'
        r_twist03_const.use_x = True
        r_twist03_const.use_y = False
        r_twist03_const.use_z = False
        r_twist03_const.mix_mode = 'ADD'
        r_twist03_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_twist03_const.owner_space = 'LOCAL'
        r_twist03_const.influence = 0.6
        #-------------------------------------------------------------
        r_twist02_const = posebone['r arm bone02'].constraints.new('COPY_ROTATION')
        r_twist02_const.target = bpy.data.objects[colprop.armatures]
        r_twist02_const.subtarget = 'r arm bone03'
        r_twist02_const.use_x = True
        r_twist02_const.use_y = False
        r_twist02_const.use_z = False
        r_twist02_const.mix_mode = 'ADD'
        r_twist02_const.target_space = 'LOCAL_OWNER_ORIENT'
        r_twist02_const.owner_space = 'LOCAL'
        r_twist02_const.influence = 0.5
        #-------------------------------------------------------------
        #Spine
        spine_const = posebone['spine'].constraints.new('COPY_ROTATION')
        spine_const.target = bpy.data.objects[colprop.armatures]
        spine_const.subtarget = 'spine1'
        spine_const.use_x = False
        spine_const.use_y = False
        spine_const.use_z = True
        spine_const.mix_mode = 'REPLACE'
        spine_const.influence = 0.5

        return {'FINISHED'}

class FixNames(Operator):
    bl_idname = "object.fix_names"
    bl_label = "Remove (.00x) from object names"
    bl_description = ("Self explanatory")
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.collections != "":
            return True
        else:
            return False

    def execute(self, context):
        colprop = bpy.context.scene.col_prop
        collection = bpy.data.collections[colprop.collections]
        armature = bpy.data.armatures

        #fix collection name
        if collection.name[-4:-2] == '.0':
            collection.name = collection.name[0:-4]
        #fix object names and remove all unused names in BlendData
        for o in collection.objects:
            if o.name[-4:-2] == '.0':
                o.name = o.name[0:-4]
            elif o.name.startswith('#XFBIN') and o.name[-5:-3] == '.0' :
                o.name = o.name[0:-5] + ']'
        for m in bpy.data.meshes:
            if m.users == 0:
                bpy.data.meshes.remove(m)
        #fix armature name
        for a in collection.objects:
            if a.type == 'ARMATURE':
                a.data.name = a.name

        #remove unused names in BlendData
        for a in armature:
            if a.name[-4:-2] == '.0' and a.users == 0:
                armature.remove(a)

        return {'FINISHED'}

class ArmatureModifier(Operator):
    bl_idname = "object.add_armature_modifier"
    bl_label = "Add armature modifier"
    bl_description = ("Add and corrects armature modifiers in meshes of a specific armature")
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.armatures != "":
            return True
        else:
            return False
        
    def execute(self, context):
        colprop = bpy.context.scene.col_prop

        for obj in bpy.data.objects[colprop.armatures].children_recursive:
            if obj.type == 'MESH':
                mod = [m for m in obj.modifiers if m.type == 'ARMATURE']
                if len(mod) == 0:
                    mod = obj.modifiers.new(bpy.data.objects[colprop.armatures].name, 'ARMATURE')
                    mod.object = bpy.data.objects[colprop.armatures]
                else:
                    mod[0].object = bpy.data.objects[colprop.armatures]

        return {'FINISHED'}


class Swap_Character_Code(Operator):
    bl_idname = "object.swap_code"
    bl_label = "Swap Character Code"
    bl_description = ("Swaps character code and model ID using the code you input")
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.armatures != "":
            return True
        else:
            return False
        
    def execute(self, context):
        colprop = bpy.context.scene.col_prop
        collection = bpy.data.collections[colprop.collections]
        armature = bpy.data.armatures[colprop.armatures]
        armature_obj = bpy.data.objects[colprop.armatures]

        #delete .001, .002 etc... to ensure no errors happen
        bpy.ops.object.fix_names()

        #change objects names
        nl = len(armature.bones[1].name) #code00t0 = 8
        nc = len(armature.bones[1].name[:-4]) #code = 4
        nc2 = len(armature.bones[1].name[:-2]) #code00 = 6
        clumpdata = armature_obj.xfbin_clump_data
        for o in collection.objects:
            
            #Armature object
            if o.name[:nc2] == armature.bones[1].name[:-2] and o.name.endswith('[C]'):
                o.name = colprop['CharacterCode'] + o.name[nc2:]
            elif o.name[:nc] == armature.bones[1].name[:-4] and o.name.endswith('[C]'):
                o.name = colprop['CharacterCode'] + o.name[nc:]
            
            #asianmel, asianmer etc... these meshes usually match chunk path code
            if len(o.name.split('_')[0]) == len(clumpdata.path.split('\\')[-3]):
                o.name = colprop['PathCode'] + o.name[len(clumpdata.path.split('\\')[-3]):]
            
            #All other objects
            if o.name[:nl] == armature.bones[1].name:
                o.name = colprop['CharacterCode'] + colprop['ModelID'] + o.name[nl:]
            
            
            '''if o.name[:nc2] == armature.bones[1].name[:-2]:
                o.name = colprop['CharacterCode'] + colprop['ModelID'][:2] + o.name[nc2:]
            elif o.name[:nl] == armature.bones[1].name:
                o.name = colprop['CharacterCode'] + colprop['ModelID'] + o.name[nl:]'''
            '''elif o.name[:nc] == armature.bones[1].name[:-4]:
            o.name = colprop['PathCode'] + o.name[nc:]'''

        #make sure that armature name = armature object name
            b = []
            if o.type == 'ARMATURE':
                b.append(o)
            for c in b:
                c.data.name = c.name

        #change texture chunks names
        tex = collection.objects[f'#XFBIN Textures [{collection.name}]'].xfbin_texture_chunks_data.texture_chunks
        if colprop.TexMat == True:
            for t in tex:
                print(t.texture_name)
                if t.texture_name[:nc2] == armature.bones[1].name[:-2]:
                    t.texture_name = colprop['CharacterCode'] + t.texture_name[nc2:]
                elif t.texture_name[:nc] == armature.bones[1].name[:-4]:
                    t.texture_name = colprop['CharacterCode'] + t.texture_name[nc:]
                else:
                    print(f"{t.texture_name} doesn't start with {armature.bones[1].name[:-4]}")
                
                #Determine Code and object locations in texture path
                code = t.path.split('/')[-3]
                pathob = t.path.split('/')[-1]

                #Change texture path code
                xfclump = armature_obj.xfbin_clump_data
                code = t.path.split('/')[-3]
                newcode = colprop['PathCode']
                t.path = t.path.replace(code, newcode)

                #Change clump path object
                pathob = t.path.split('/')[-1]
                newpathob = t.texture_name + pathob[-4:]
                t.path = t.path.replace(pathob, newpathob)

        #remove and add models and model groups
        armature_obj.xfbin_clump_data.models.clear()
        armature_obj.xfbin_clump_data.model_groups.clear()
        g = armature_obj.xfbin_clump_data.model_groups.add()
        g.name = 'Group'
        g.unk = '7F 7F FF FF'
        for child in armature_obj.children:
            m = armature_obj.xfbin_clump_data.models.add()
            #m.value = child.name
            m.empty = child
            gm = g.models.add()
            #gm.name = child.name
            gm.empty = child
            child.xfbin_nud_data.mesh_bone = child.name

        #Change clump path code
        xfclump = armature_obj.xfbin_clump_data
        code = xfclump.path.split('\\')[-3]
        newcode = colprop['PathCode']
        xfclump.path = xfclump.path.replace(code, newcode)

        #Change clump path object
        pathob = xfclump.path.split('\\')[-1]
        newpathob = colprop['CharacterCode'] + pathob[-8:]
        xfclump.path = xfclump.path.replace(pathob, newpathob)

        #Swap codes in clump materials
        if colprop.TexMat == True:
            for mat in xfclump.materials:
                for texg in mat.texture_groups:
                    for t in texg.textures:
                        if t.texture_name != 'celshade':
                            if t.texture_name[:nc2] == armature.bones[1].name[:-2]:
                                t.texture_name = colprop['CharacterCode'] + t.texture_name[nc2:]
                            elif t.texture_name[:nc] == armature.bones[1].name[:-4]:
                                t.texture_name = colprop['CharacterCode'] + t.texture_name[nc:]
                            else:
                                print(f"{t.texture_name} doesn't start with {armature.bones[1].name[:-4]}")
                            
                            #Determine Code and object locations in texture path
                            code = t.path.split('/')[-3]
                            pathob = t.path.split('/')[-1]

                            #Change clump path code
                            xfclump = armature_obj.xfbin_clump_data
                            code = t.path.split('/')[-3]
                            newcode = colprop['PathCode']
                            t.path = t.path.replace(code, newcode)

                            #Change clump path object
                            pathob = t.path.split('/')[-1]
                            newpathob = t.texture_name + pathob[-4:]
                            t.path = t.path.replace(pathob, newpathob)

                if mat.material_name[:nc2] == armature.bones[1].name[:-2]:
                    mat.material_name = colprop['CharacterCode'] + mat.material_name[nc2:]
                elif mat.material_name[:nc] == armature.bones[1].name[:-4]:
                    mat.material_name = colprop['CharacterCode'] + mat.material_name[nc:]

            #Reapply materials in meshes after changing the names

            for o in armature_obj.children:
                for c in o.children:
                    if c.xfbin_mesh_data.xfbin_material[:nc2] == armature.bones[1].name[:-2]:
                        c.xfbin_mesh_data.xfbin_material = colprop['CharacterCode'] + c.xfbin_mesh_data.xfbin_material[nc2:]
                    elif c.xfbin_mesh_data.xfbin_material[:nc] == armature.bones[1].name[:-4]:
                        c.xfbin_mesh_data.xfbin_material = colprop['CharacterCode'] + c.xfbin_mesh_data.xfbin_material[nc:]

        #change collection name and XFBIN Textures
        colname = armature.name[:-4]
        armname = armature.name
        collection.name = colname

        #make sure that the correct armature is selected
        colprop.collections = colname
        colprop.armatures = armname

        #correct XFBIN Textures name
        for o in collection.objects:
            if o.name.startswith('#XFBIN Textures') :
                o.name = o.name[0:16] + '[' + collection.name + ']'

        #change bone names
        bpy.ops.object.remove_char_code()
        armature.bones[1].name = colprop['CharacterCode'] + colprop['ModelID']
        bpy.ops.object.add_char_code()

        return {'FINISHED'}


class Replace_Mats(Operator):
    bl_idname = "object.replace_mats"
    bl_label = "Replace Materials ID"
    bl_description = (f'Replace material IDs for the selected meshes, if no meshes were selected, the tool will attempt to replace materials for meshes in the selected collection')
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT':
            return True
        else:
            return False
    
    def execute(self, context):

        colprop = bpy.context.scene.col_prop

        collection_objects = [o for o in bpy.data.collections[colprop.collections].objects if o.type == 'MESH']

        if colprop.AutoMatID == True:
            Oldmat = context.object.xfbin_mesh_data['materials'][0]['material_id']
        else:
            Oldmat = str(colprop.Old_Material_ID.upper())

        
        if bpy.context.active_object.type == 'EMPTY':
            for m in [o for o in bpy.context.active_object.children]:
                if Oldmat in m.xfbin_mesh_data.materials:
                    m.xfbin_mesh_data.materials[Oldmat].material_id = colprop.New_Material_ID      

        elif len(bpy.context.selected_objects) > 0:
            for m in [o for o in bpy.context.selected_objects]:
                if Oldmat in m.xfbin_mesh_data.materials:
                    m.xfbin_mesh_data.materials[Oldmat].material_id = colprop.New_Material_ID
                else:
                    self.report({"WARNING"}, f"The material you're attempting to replace does not exist in {m.name}")

        else:
            self.report({"INFO"}, f"No meshes were selected, Attempting to replace materials for meshes in the whole collecton")
            for m in [o for o in collection_objects]:
                if Oldmat in m.xfbin_mesh_data.materials:
                    m.xfbin_mesh_data.materials[Oldmat].material_id = colprop.New_Material_ID
                else:
                    self.report({"WARNING"}, f"The material you're attempting to replace does not exist in {m.name}")
        
        return {'FINISHED'}

class Duplicate_XFBIN_Mat(Operator):
    bl_idname = "object.duplicate_mats"
    bl_label = "Create New XFBIN Mat"
    bl_description = (f"Creates a separate XFBIN material for the selected mesh and applies it. EXAMPLE: if a mesh has a material called body1, it will make a duplicate copy and applies it")
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT':
            return True
        else:
            return False
    
    def execute(self, context):

        colprop = bpy.context.scene.col_prop

        active = bpy.context.active_object

        mat = active.xfbin_mesh_data.xfbin_material

        matc = active.parent.parent.xfbin_clump_data.materials[mat]

        new = active.parent.parent.xfbin_clump_data.materials.add()
        if colprop.XFBIN_Mat != '':
            new.material_name = colprop.XFBIN_Mat
        else:
            new.material_name = matc.material_name + 'NEW'


        new.field02 = matc.field02

        new.field04 = matc.field04

        new.float_format = matc.float_format

        new.floats = matc.floats

        for i in range(len(matc.texture_groups)):
            tex = new.texture_groups.add()
            for t in range(len(matc.texture_groups[i].textures)):
                    tx = tex.textures.add()
                    

        for i, tg in enumerate(new.texture_groups):
            new.texture_groups[new['texture_groups'][i].name].name = matc['texture_groups'][i]['name']
            new['texture_groups'][i]['flag'] = matc['texture_groups'][i]['flag']
            for a, t in enumerate(new['texture_groups'][i]['textures']):
                new['texture_groups'][i]['textures'][a]['name'] = matc['texture_groups'][i]['textures'][a]['name']
                new['texture_groups'][i]['textures'][a]['path'] = matc['texture_groups'][i]['textures'][a]['path']
                new['texture_groups'][i]['textures'][a]['texture'] = matc['texture_groups'][i]['textures'][a]['texture']
                new['texture_groups'][i]['textures'][a]['texture_name'] = matc['texture_groups'][i]['textures'][a]['texture_name']
        if colprop.XFBIN_Mat != '':
            bpy.context.active_object.xfbin_mesh_data.xfbin_material = colprop.XFBIN_Mat
        else:
            bpy.context.active_object.xfbin_mesh_data.xfbin_material = bpy.context.active_object.xfbin_mesh_data.xfbin_material + 'NEW'


        return {'FINISHED'}

class Copy_Bone_Pos(Operator):
    bl_idname = "object.copy_pos"
    bl_label = "Copy Bone Positions"
    bl_description = (f"Copy bone positions from target armature to the armature at the top (Main aramture)")
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT':
            return True
        else:
            return False
    
    def execute(self, context):
        colprop = bpy.context.scene.col_prop
        armaturename = bpy.context.scene.armaturelist.name
        armature_obj = bpy.data.objects[colprop.armatures]
        target_obj = bpy.data.objects[armaturename]

        # A dictionary with the bones I want to edit
        target_bones = ['r clavicle', 'r upperarm', 'r forearm', 'r hand', 'r finger0', 'r finger1',
                'r finger2','r finger3', 'r finger4','r finger01', 'r finger02', 'r finger11',
                'r finger12', 'r finger21', 'r finger22', 'r finger31', 'r finger32', 'r finger41',
                'r finger42', 'l clavicle', 'l upperarm', 'l forearm', 'l hand', 'l finger0','l finger1',
                'l finger2','l finger3','l finger4', 'l finger01', 'l finger02', 'l finger11', 'l finger12',
                'l finger21', 'l finger22', 'l finger31', 'l finger32', 'l finger41', 'l finger42',
                'spine1', 'spine', 'pelvis', 'l thigh', 'l calf', 'l foot', 'l toe0', 'r thigh',
                'r calf', 'r foot', 'r toe0', 'l arm bone01', 'l arm bone02', 'l arm bone03'
                'l arm bone04', 'l arm bone05', 'l arm bone06', 'r arm bone01', 'r arm bone02',
                'r arm bone03', 'r arm bone04', 'r arm bone05', 'r arm bone06', 'l foot bone01',
                'l foot bone02', 'l foot bone03', 'l foot bone04', 'l foot bone05', 'r foot bone01',
                'r foot bone02', 'r foot bone03', 'r foot bone04', 'r foot bone05', 'left sleeve',
                'right sleeve']


        bpy.ops.object.remove_char_code()
        # A dictionary with bones from the base armature that matches the ones in target_bones
        #base_bones = [b.name for b in armature_obj.data.bones if b.name in target_bones]
        base_bones = [b.name for b in armature_obj.data.bones]

        # A dictionary with bone from the target armature that matches the ones from the base armature
        btoc = [b.name for b in target_obj.data.bones if b.name in base_bones]

        # Select the target armature and switch to edit mode
        bpy.context.view_layer.objects.active = target_obj
        bpy.ops.object.editmode_toggle()

        # Select matching bones
        for b in target_obj.data.edit_bones:
            if b.name in btoc:
                b.select_head = True
                b.select_tail = True
                b.select = True

        # Duplicate, separate and switch back to object mode
        bpy.ops.armature.duplicate()
        bpy.ops.armature.separate()
        bpy.ops.object.editmode_toggle()

        # Select both the new armature and the base armature
        bpy.ops.object.select_all(action='DESELECT')
        if bpy.data.objects.get(target_obj.name + '.001') is not None:
            bpy.data.objects[target_obj.name + '.001'].select_set(True)
            bpy.data.objects[armature_obj.name].select_set(True)
        else:
            self.report({'ERROR'}, f"Didn't find the temporary armature '{target_obj.name + '.001'}' make sure you have the correct armature selected"
            "\n and the bone names are correct")
            return {'CANCELLED'}

        # Merge both armatures then switch to edit mode
        bpy.context.view_layer.objects.active = armature_obj
        bpy.ops.object.join()
        bpy.ops.object.editmode_toggle()

        # Move bones from base armature to the positions of bones from target armature
        for b in armature_obj.data.edit_bones:
            if b.name in btoc:
                '''armature_obj.data.edit_bones[b.name].head.xyz = armature_obj.data.edit_bones[b.name + '.001'].head.xyz
                armature_obj.data.edit_bones[b.name].tail.xz = armature_obj.data.edit_bones[b.name + '.001'].head.xz
                armature_obj.data.edit_bones[b.name].tail.y = armature_obj.data.edit_bones[b.name + '.001'].head.y + 0.0001'''
                armature_obj.data.edit_bones[b.name].matrix = armature_obj.data.edit_bones[b.name + '.001'].matrix
                
        # Delete duplicate bones
            if b.name.endswith('.001'):
                b.select_head = True
                b.select_tail = True
                b.select = True
                bpy.ops.armature.delete()

        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class CreateClone(Operator):
    bl_idname = "object.clone"
    bl_label = "Create Clone"
    bl_description = (f"No description")
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT':
            return True
        else:
            return False
    
    def execute(self, context):

        colprop = bpy.context.scene.col_prop

        bpy.ops.object.add_char_code()

        bpy.data.objects[colprop.armatures].select_set(True)


        for o in bpy.data.objects[colprop.armatures].children_recursive:
            o.select_set(True)

        bpy.ops.object.duplicate()

        for o in bpy.context.selected_objects:
            o.name = 'xxxx' + o.name[4:]
            if o.name.startswith('xxxx') and o.name[-8:-4] == ' [C]':
                bpy.data.objects[o.name].data.bones[1].name = bpy.data.objects[o.name].data.bones[1].name[:-4] + colprop.CloneID
                for b in bpy.data.objects[o.name].data.bones:
                    if b != bpy.data.objects[o.name].data.bones[1]:
                        b.name = bpy.data.objects[o.name].data.bones[1].name + b.name[8:]
                o.name = bpy.data.objects[o.name].data.bones[1].name[:-4] + colprop.BodID + ' [C]'
        
        #dynamics
        if bpy.data.objects.get(f'#XFBIN Dynamics [{colprop.collections}]'):
            obj = bpy.data.objects[f'#XFBIN Dynamics [{colprop.collections}]']
            dyn_obj = bpy.data.objects.new(f'#XFBIN Dynamics [{colprop.collections[:-4]}{colprop.BodID}]', None)
            dyn_obj.empty_display_type = obj.empty_display_type
            dyn_obj.empty_display_size = obj.empty_display_size
            #link the object
            bpy.data.collections[colprop.collections].objects.link(dyn_obj)

            #copy props from old object
            bpy.context.view_layer.objects.active = obj
            bpy.ops.xfbin_panel.copy_group(prop_path='xfbin_dynamics_data', prop_name='Dynamics Properties')
            
            #paste props to the new object
            bpy.context.view_layer.objects.active = dyn_obj
            bpy.ops.xfbin_panel.paste_group(prop_path='xfbin_dynamics_data', prop_name='Dynamics Properties')
            
            #correct clump name and path
            clump_name = obj.xfbin_dynamics_data.clump_name
            path = obj.xfbin_dynamics_data.path
            dyn_obj.xfbin_dynamics_data.clump_name = obj.xfbin_dynamics_data.clump_name[:-4] + colprop.BodID
            dyn_obj.xfbin_dynamics_data.path = f'{obj.xfbin_dynamics_data.path[:-8]}{colprop.BodID}.max'

        #delete .001, .002 etc... to ensure no errors happen
        bpy.ops.object.fix_names()

        a = [o.name for o in bpy.context.selected_objects if o.name.endswith('[C]')]
       
        #make sure that armature data name = armature object name
        bpy.data.objects[a[0]].data.name = bpy.data.objects[a[0]].name
        
        for o in bpy.data.objects[a[0]].children:
            if o.name.startswith('xxxx') and o.name[:5] != 'xxxx_':
                o.name = bpy.data.objects[a[0]].data.bones[1].name + o.name[8:]

            if o.name.startswith('xxxx_'):
                for c in o.children:
                    bpy.data.objects.remove(bpy.data.objects[c.name])
                bpy.data.objects.remove(bpy.data.objects[o.name])
                
        bpy.data.objects[a[0]].xfbin_clump_data.models.clear()
        bpy.data.objects[a[0]].xfbin_clump_data.model_groups.clear()
        g = bpy.data.objects[a[0]].xfbin_clump_data.model_groups.add()
        g.name = 'Group'
        g.unk = '7F 7F FF FF'
        for child in bpy.data.objects[a[0]].children:
            m = bpy.data.objects[a[0]].xfbin_clump_data.models.add()
            m.empty = child
            gm = g.models.add()
            gm.empty = child
            child.xfbin_nud_data.mesh_bone = child.name

        bpy.ops.object.select_all(action='DESELECT')


        return {'FINISHED'}

class Create_bod1_f(Operator):
    bl_idname = "object.bod1f"
    bl_label = "Create bod1_f model"
    bl_description = (f"Makes a mirrored model to work with Jojo ASBR")
    
    @classmethod
    def poll(cls, context):
        if context.mode == 'OBJECT':
            return True
        else:
            return False
    
    def execute(self, context):

        colprop = context.scene.col_prop

        collection = bpy.data.collections[colprop.collections]

        new_col = bpy.data.collections.new(f'{collection.name}_f')

        bpy.context.collection.children.link(new_col)

        bpy.ops.object.remove_char_code()
        for obj in collection.objects:
            #Dynamics object
            if obj.name.startswith('#XFBIN Dynamics'):
                #create the object
                dyn_obj = bpy.data.objects.new(f'#XFBIN Dynamics [{collection.name}_f]', None)
                dyn_obj.empty_display_type = obj.empty_display_type
                dyn_obj.empty_display_size = obj.empty_display_size
                #link the object
                new_col.objects.link(dyn_obj)
                
                #copy props from old object
                bpy.context.view_layer.objects.active = obj
                bpy.ops.xfbin_panel.copy_group(prop_path='xfbin_dynamics_data', prop_name='Dynamics Properties')
                
                #paste props to the new object
                bpy.context.view_layer.objects.active = dyn_obj
                bpy.ops.xfbin_panel.paste_group(prop_path='xfbin_dynamics_data', prop_name='Dynamics Properties')
                
                #correct clump name and path
                clump_name = obj.xfbin_dynamics_data.clump_name
                path = obj.xfbin_dynamics_data.path
                dyn_obj.xfbin_dynamics_data.clump_name = obj.xfbin_dynamics_data.clump_name + '_f'
                dyn_obj.xfbin_dynamics_data.path = f'{obj.xfbin_dynamics_data.path[:-(len(clump_name) + 4)]}{clump_name}_f.max'
                
                spg = dyn_obj.xfbin_dynamics_data.spring_groups
                for i in (range(len(spg))):
                    print(spg[i].name)
                    spg[i].bone_spring += '_f'
                    spg[i].name = f'Spring Group [{spg[i].bone_spring}]'
                
                col = dyn_obj.xfbin_dynamics_data.collision_spheres
                for i in range(len((col))):
                    col[i].bone_collision += '_f'
                    col[i].name = f'Collision Sphere {i} [{col[i].bone_collision}]'
                    if col[i].attach_groups:
                        for spring in col[i].attached_groups:
                            spring.value = f'{spring.value[:-1]}_f]'

            
            #Textures object
            elif obj.name.startswith('#XFBIN Textures'):
                tex_obj = bpy.data.objects.new(f'#XFBIN Textures [{collection.name}_f]', None)
                tex_obj.empty_display_type = obj.empty_display_type
                tex_obj.empty_display_size = obj.empty_display_size
                #link the object
                new_col.objects.link(tex_obj)
                
                for tex in obj.xfbin_texture_chunks_data.texture_chunks:
                    t = tex_obj.xfbin_texture_chunks_data.texture_chunks.add()
                    t.texture_name = tex.texture_name
                    t.path = tex.path
            
            #Armature object
            elif obj.type == 'ARMATURE':
                #create a new object with the armature data
                data = obj.data.copy()
                
                arm_obj = bpy.data.objects.new(f'{obj.name[:-4]}_f [C]', data)
                arm_obj.data.name = arm_obj.name
                arm_obj.show_in_front = True
                
                #link the objects
                new_col.objects.link(arm_obj)
                
                #flip bones
                if colprop.FlipBones:
                
                    sfx_pfx = ('l ', 'r ', ' l', ' r', 'l_', 'r_', '_l', '_r')
                    
                    bpy.context.view_layer.objects.active = arm_obj
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.armature.select_all(action='DESELECT')
                    for bone in arm_obj.data.edit_bones:
                        if not any(x in bone.name for x in sfx_pfx) and bone.head.x > 0.01 or not any(x in bone.name for x in sfx_pfx) and bone.head.x < -0.01:
                            bone.head.x *= -1
                            bone.tail.x *= -1
                    bpy.ops.object.editmode_toggle()

                #copy props
                bpy.context.view_layer.objects.active = obj
                bpy.ops.xfbin_panel.copy_group(prop_path='xfbin_clump_data', prop_name='Xfbin Clump Data')
                
                bpy.context.view_layer.objects.active = arm_obj
                bpy.ops.xfbin_panel.paste_group(prop_path='xfbin_clump_data', prop_name='Xfbin Clump Data')

                arm_obj.xfbin_clump_data.path = obj.xfbin_clump_data.path[:-4] + '_f.max'
                
                #model group
                model_group = arm_obj.xfbin_clump_data.model_groups[0]
                
                #clear stuff
                arm_obj.xfbin_clump_data.models.clear()
                model_group.models.clear()
                
                
                for empty in obj.children:
                    new_empty = bpy.data.objects.new(f'{empty.name}_f', None)
                    new_empty.empty_display_type = empty.empty_display_type
                    new_empty.empty_display_size = empty.empty_display_size
                    
                    #link the object
                    new_col.objects.link(new_empty)
                    
                    #copy props
                    bpy.context.view_layer.objects.active = empty
                    bpy.ops.xfbin_panel.copy_group(prop_path='xfbin_nud_data', prop_name='Xfbin Nud Data')
                    
                    #paste props
                    bpy.context.view_layer.objects.active = new_empty
                    bpy.ops.xfbin_panel.paste_group(prop_path='xfbin_nud_data', prop_name='Xfbin Nud Data')
                    
                    #set the parent
                    new_empty.parent = arm_obj
                    new_empty.parent_type = empty.parent_type
                    if new_empty.parent_type == 'BONE':
                        new_empty.parent_bone = empty.parent_bone
                    
                    #set mesh bone
                    new_empty.xfbin_nud_data.mesh_bone = f'{empty.xfbin_nud_data.mesh_bone}_f'
                    
                    #add empties to models list
                    model = arm_obj.xfbin_clump_data.models.add()
                    model.empty = new_empty
                    
                    model2 = model_group.models.add()
                    model2.empty = new_empty
                    
                    
                    for mesh_obj in empty.children:
                        new_mesh = mesh_obj.data.copy()
                        new_mesh.name = mesh_obj.data.name + '_f'
                        
                        new_obj = bpy.data.objects.new(f'{mesh_obj.name}_f', new_mesh)
                        #link the object
                        new_col.objects.link(new_obj)
                        #set the parent
                        new_obj.parent = new_empty
                        
                        #add armature modifier
                        mod = new_obj.modifiers.new(arm_obj.name, 'ARMATURE')
                        mod.object = arm_obj
                        
                        #copy props
                        bpy.context.view_layer.objects.active = mesh_obj
                        bpy.ops.xfbin_panel.copy_group(prop_path='xfbin_mesh_data', prop_name='Xfbin Mesh Data')
                        
                        #paste props
                        bpy.context.view_layer.objects.active = new_obj
                        bpy.ops.xfbin_panel.paste_group(prop_path='xfbin_mesh_data', prop_name='Xfbin Mesh Data')
                        
                        #correct the culling settings
                        new_obj.xfbin_mesh_data.materials[0].cull_mode = 0
                        
                        if colprop.FlipMeshes == True:
                            #mirror active object
                            bpy.ops.object.select_all(action='DESELECT')
                            new_obj.select_set(True)
                            new_obj.scale[0] = new_obj.scale[0] * -1
                            bpy.ops.object.editmode_toggle()
                            bpy.ops.mesh.select_all(action='SELECT')
                            bpy.ops.mesh.flip_normals()
                            bpy.ops.object.editmode_toggle()
                            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

                            #mirror vertex groups
                            
                            sfx_pfx_dict = {
                                            'l ':'Left ',
                                            'r ':'Right ',
                                            '_l':'_Left',
                                            '_r':'_Right',
                                            }

                            
                            for v in new_obj.vertex_groups:
                                if v.name[:2] in sfx_pfx_dict:
                                    v.name = sfx_pfx_dict[v.name[:2]] + v.name[2:]
                                elif v.name[-2:] in sfx_pfx_dict:
                                    v.name = v.name[:-2] + sfx_pfx_dict[v.name[-2:]]
                                
                            for v in new_obj.vertex_groups:
                                if v.name.startswith('Left '):
                                    v.name = f'r {v.name[5:]}'
                                elif v.name.startswith('Right '):
                                    v.name = f'l {v.name[6:]}'
                                elif v.name.endswith('_Left'):
                                    v.name = f'{v.name[:-5]}_r'
                                elif v.name.endswith('_Right'):
                                    v.name = f'{v.name[:-6]}_l'
                if len(arm_obj.data.bones) > 2:
                    for b in arm_obj.data.bones:
                        if b.name != obj.data.bones[1].name:
                            b.name = f'{b.name}_f'
                else:
                    for b in arm_obj.data.bones:
                        b.name = f'{b.name}_f'

        bpy.ops.object.add_char_code()

        colprop.collections = collection.name + '_f'

        bpy.ops.object.add_char_code()


        return {'FINISHED'}

class ToDmgBody(Operator):
    bl_idname = "object.reg_bod"
    bl_label = "Regular to DMG" 
    bl_description = ('Creates a damage body from the selected model.')
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.collections != "":
            return True
        else:
            return False
        
    def execute(self, context):
        
        colprop = bpy.context.scene.col_prop

        armature = bpy.data.objects[colprop.armatures]

        old_col = bpy.data.collections[colprop.collections]

        new_col = bpy.data.collections.new(f'{armature.name[:-4]}_dmg01')

        bpy.context.collection.children.link(new_col)

        bpy.ops.object.remove_char_code()

        armobj = armature.copy()
        armobj.data = armature.data.copy()
        armobj.name = f"{armature.name[:-4]}dmg01_{armature.name[-4:]}"

        armobj.show_in_front = True
        armobj.data.name = armobj.name
        new_col.objects.link(armobj)
        armobj.data.bones[1].name = f"{armature.data.bones[1].name[:4]}dmg01_{armature.data.bones[1].name[4:]}"
        armobj['xfbin_clump'] = 1

        colprop.collections = new_col.name
        colprop.armatures = armobj.name

        bpy.ops.object.add_char_code()

        armobj.xfbin_clump_data.path = f"{armature.xfbin_clump_data.path[:-12]}{armobj.name}.max"


        #Dynamics
        dyn_Data = armobj.xfbin_dynamics_data
        
        spg = dyn_Data.spring_groups
        for i in (range(len(spg))):
            spg[i].init_done = False
            spg[i].bone_spring = f'{armobj.data.bones[1].name}{spg[i].bone_spring[8:]}'
            spg[i].name = spg[i].bone_spring
            spg[i].init_done = True
            #spg[i].name = f'Spring Group [{spg[i].bone_spring}]'
        
        col = dyn_Data.collision_spheres
        for i in range(len((col))):
            col[i].bone_collision = f'{armobj.data.bones[1].name}{col[i].bone_collision[8:]}'
            col[i].name = f'Collision Sphere {i} [{col[i].bone_collision}]'
            if col[i].attach_groups:
                for spring in col[i].attached_groups:
                    bone = spring.bone_spring
                    new_bone = f"{armobj.data.bones[1].name}{bone[8:]}"
                    spring.bone_spring = f'{new_bone}'
            
        #model group
        model_group = armobj.xfbin_clump_data.model_groups[0]
        
        #clear stuff
        armobj.xfbin_clump_data.models.clear()
        model_group.models.clear()
        exclude = [o for o in armature.children if not o.name.startswith(f"{armature.data.bones[1].name}{o.name[8:]}")]
        #exclude = ["asianimel", "asianimer", "udeanml", "udeanmr"]
        for obj in armature.children:
           
            if any(x.name == obj.name for x in exclude):
                object_name = obj.name
            else:
                object_name = f"{armobj.data.bones[1].name}{obj.name[8:]}"
            

            #duplicate the object
            new_object = obj.copy()
            new_object.data = obj.data.copy()
            new_object.name = object_name
            
            #link the object
            new_col.objects.link(new_object)
            
            #set the parent
            new_object.parent = armobj
            
            #set mesh bone
            new_object.xfbin_nud_data.mesh_bone = f'{armobj.data.bones[1].name}{obj.xfbin_nud_data.mesh_bone[8:]}'
            
            model2 = model_group.models.add()
            model2.object = new_object
            
            bpy.ops.object.remove_char_code()
            bpy.ops.object.add_char_code()

        return {'FINISHED'}


class ToRegularBody(Operator):
    bl_idname = "object.dmg_bod"
    bl_label = "DMG to Regular" 
    bl_description = ('Converts models that end with _dmg01 to a regular one.')
    
    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'OBJECT' and bpy.context.scene.col_prop.collections != "":
            return True
        else:
            return False
        
    def execute(self, context):
        
        colprop = bpy.context.scene.col_prop

        armature = bpy.data.objects[colprop.armatures]

        old_col = bpy.data.collections[colprop.collections]

        new_col = bpy.data.collections.new(f'{armature.name[:-4]}_dmg01')
        new_col = bpy.data.collections.new(f'{armature.name[:4]}{armature.name[10:]}')

        bpy.context.collection.children.link(new_col)

        bpy.ops.object.remove_char_code()

        armobj = armature.copy()
        armobj.data = armature.data.copy()
        armobj.name = f"{armature.name[:-4]}dmg01_{armature.name[-4:]}"
        armobj.name = f"{armature.name[:4]}{armature.name[10:]}"

        armobj.show_in_front = True
        armobj.data.name = armobj.name
        new_col.objects.link(armobj)
        armobj.data.bones[1].name = f"{armature.data.bones[1].name[:4]}{armature.data.bones[1].name[10:]}"
        armobj['xfbin_clump'] = 1

        colprop.collections = new_col.name
        colprop.armatures = armobj.name

        bpy.ops.object.add_char_code()

        armobj.xfbin_clump_data.path = armobj.xfbin_clump_data.path.replace(armature.xfbin_clump_data.path.split("\\")[-1], "") + f"{armobj.name}.max"


        #Dynamics
        dyn_Data = armobj.xfbin_dynamics_data
        
        spg = dyn_Data.spring_groups
        for i in (range(len(spg))):
            spg[i].init_done = False
            spg[i].bone_spring = f'{armobj.data.bones[1].name}{spg[i].bone_spring[14:]}'
            spg[i].name = spg[i].bone_spring
            spg[i].init_done = True
            #spg[i].name = f'Spring Group [{spg[i].bone_spring}]'
        
        col = dyn_Data.collision_spheres
        for i in range(len((col))):
            col[i].bone_collision = f'{armobj.data.bones[1].name}{col[i].bone_collision[14:]}'
            col[i].name = f'Collision Sphere {i} [{col[i].bone_collision}]'
            if col[i].attach_groups:
                for spring in col[i].attached_groups:
                    bone = spring.bone_spring
                    new_bone = f"{armobj.data.bones[1].name}{bone[14:]}"
                    spring.bone_spring = f'{new_bone}'
            
        #model group
        model_group = armobj.xfbin_clump_data.model_groups[0]
        
        #clear stuff
        armobj.xfbin_clump_data.models.clear()
        model_group.models.clear()
        exclude = [o for o in armature.children if not o.name.startswith(f"{armature.data.bones[1].name}{o.name[14:]}")]
        for obj in armature.children:
           
            if any(x.name == obj.name for x in exclude):
                object_name = obj.name
            else:
                object_name = f"{armobj.data.bones[1].name}{obj.name[14:]}"
            

            #duplicate the object
            new_object = obj.copy()
            new_object.data = obj.data.copy()
            new_object.name = object_name
            
            #link the object
            new_col.objects.link(new_object)
            
            #set the parent
            new_object.parent = armobj
            
            #set mesh bone
            new_object.xfbin_nud_data.mesh_bone = f'{armobj.data.bones[1].name}{obj.xfbin_nud_data.mesh_bone[14:]}'
            
            model2 = model_group.models.add()
            model2.object = new_object
            
            bpy.ops.object.remove_char_code()
            bpy.ops.object.add_char_code()

        return {'FINISHED'}



class CreateBoneList(bpy.types.Operator):
    bl_idname = "object.build_bone_list"
    bl_label = "Create Bone List"
    bl_description = "Builds the bone list from the animation and tries to automatically detect and match bones"

    def execute(self, context):
        colprop = bpy.context.scene.col_prop
        
        source = context.scene.main_armature
        target = context.scene.target_armature
        if source is None or target is None:
            self.report({'ERROR'}, "Please select both armatures")
            return {'CANCELLED'}

        # Clear the bone retargeting list
        colprop.bone_dict.clear()

        for bone in source.data.bones:
            add = colprop.bone_dict.add()
            add.bone_main = bone.name

            if bone.name in target.data.bones:
                add.bone_target = bone.name

        return {'FINISHED'}


class RetargetStormAnim(bpy.types.Operator):
    bl_idname = "object.retarget_storm_anim"
    bl_label = "Retarget Storm Anim"
    bl_description = "Retargets the animation from the source armature to the target armature"

    def execute(self, context):
        colprop = bpy.context.scene.col_prop
        reprop = bpy.context.scene.retarget_prop

        anims_object = bpy.data.objects[reprop.anims_object]
        
        source = context.scene.main_armature
        target = context.scene.target_armature
        if source is None or target is None:
            self.report({'ERROR'}, "Please select both armatures")
            return {'CANCELLED'}

        #get the source animation
        source_action = source.animation_data.action
        if source_action is None:
            self.report({'ERROR'}, "source armature has no animation")
            return {'CANCELLED'}
        
        #create a new action for the target armature
        target_action = source_action.copy()

        #rename the action
        target_action.name = source_action.name.replace(source.name[:4], target.name[:4])

        #rename groups
        for group in target_action.groups:
            group.name = group.name.replace(source.name[:4], target.name[:4])
        
        #rename fcurves
        for fcurve in target_action.fcurves:
            fcurve.data_path = fcurve.data_path.replace(source.name[:4], target.name[:4])
        
        #set the action to the target armature
        target.animation_data_create()
        target.animation_data.action = target_action

        return {'FINISHED'}


class RetargetAllStormAnims(bpy.types.Operator):
    bl_idname = "object.retarget_all_storm_anims"
    bl_label = "Retarget All Storm Anims"
    bl_description = "Retargets all the animations from the source armature to the target armature"

    def execute(self, context):
        colprop = bpy.context.scene.col_prop
        reprop = bpy.context.scene.retarget_prop
        
        source = context.scene.main_armature
        target = context.scene.target_armature

        anims_object = bpy.data.objects[reprop.anims_object]

        if source is None or target is None:
            self.report({'ERROR'}, "Please select both armatures")
            return {'CANCELLED'}
        
        for chunk in anims_object.xfbin_anm_chunks_data.anm_chunks:
            
            #action = bpy.data.actions.get(f'{chunk.name} ({clump.name[:-4]})')
            name = f"{chunk.name} ({source.name[:-4]})"
            #get the target action
            source_action =  bpy.data.actions.get(name)

            if source_action:
                #make a copy of the source action
                target_action = source_action.copy()

                #rename the action
                target_action.name = source_action.name.replace(source.name[:4], target.name[:4])

                #rename groups
                for group in target_action.groups:
                    group.name = group.name.replace(source.name[:4], target.name[:4])
                
                #rename fcurves
                for fcurve in target_action.fcurves:
                    fcurve.data_path = fcurve.data_path.replace(source.name[:4], target.name[:4])
                
                #set the action to the target armature
                target.animation_data_create()
                target.animation_data.action = target_action
            else:
                self.report({'WARNING'}, f"Action {chunk.name} not found, skipping...")
                continue

        return {'FINISHED'}


class CloneAnmObject(bpy.types.Operator):
    bl_idname = "object.clone_anm_object"
    bl_label = "Clone Anm Object"
    bl_description = "Clones the selected anm object"

    def execute(self, context):
        colprop = bpy.context.scene.col_prop
        reprop = bpy.context.scene.retarget_prop
        
        source = context.scene.main_armature
        target = context.scene.target_armature

        source_anims_object = bpy.data.objects[reprop.anims_object]

        target_anims_object = source_anims_object.copy()
        target_anims_object.name = source_anims_object.name.replace(source.name[:4], target.name[:4])

        #get source anims object collection
        source_col = source_anims_object.users_collection[0]

        #make a new collection for the target anims object
        target_col = bpy.data.collections.new(target_anims_object.name)
        bpy.context.collection.children.link(target_col)

        #link the target anims object to the new collection
        target_col.objects.link(target_anims_object)

        #rename the anim chunks in the target anims object
        for chunk in target_anims_object.xfbin_anm_chunks_data.anm_chunks:
            
            #get the target action
            source_action =  bpy.data.actions.get(f'{chunk.name} ({source.name})')

            if source_action:
                #make a copy of the source action
                target_action = source_action.copy()

                #rename the action
                target_action.name = source_action.name.replace(source.name[:4], target.name[:4])

                #rename the anm chunk
                chunk.name = chunk.name.replace(source.name[:4], target.name[:4])

                #rename clumps
                for clump in chunk.anm_clumps:
                    if clump.name.startswith(source.name[:4]):

                        #rename bones
                        for bone in clump.bones:
                            if f"{source.name[:4]}" in bone.name:
                                bone.name = bone.name.replace(source.name[:4], target.name[:4])
                        
                        #rename models
                        for model in clump.models:
                            if f"{source.name[:4]}" in model.name:
                                model.name = model.name.replace(source.name[:4], target.name[:4])
                        
                        #rename clump
                        clump.name = clump.name.replace(source.name[:4], target.name[:4])
                        

                #rename groups
                for group in target_action.groups:
                    group.name = group.name.replace(source.name[:4], target.name[:4])
                
                #rename fcurves
                for fcurve in target_action.fcurves:
                    fcurve.data_path = fcurve.data_path.replace(source.name[:4], target.name[:4])
                
                #rename yo mama

                #remove groups and fcurves that don't exist in the target armature
                for group in target_action.groups:
                    if group.name not in target.data.bones:
                        target_action.groups.remove(group)

                for fcurve in target_action.fcurves:
                    pose_curve = fcurve.data_path.split('"')[1]
                    if pose_curve not in target.pose.bones:
                        target_action.fcurves.remove(fcurve)
                
                #set the action to the target armature
                target.animation_data_create()
                target.animation_data.action = target_action

            

        return {'FINISHED'}


class CorrectAnmNames(bpy.types.Operator):
    bl_idname = "object.correct_anm_names"
    bl_label = "Correct Anm Names"
    bl_description = "Corrects the names of the anm chunks and clumps"

    def execute(self, context):
        colprop = bpy.context.scene.col_prop
        reprop = bpy.context.scene.retarget_prop
        
        source = context.scene.main_armature
        target = context.scene.target_armature

        anims_object = bpy.data.objects[reprop.anims_object]

        if source is None or target is None:
            self.report({'ERROR'}, "Please select both armatures")
            return {'CANCELLED'}
        
        for chunk in anims_object.xfbin_anm_chunks_data.anm_chunks:
            clump = chunk.anm_clumps[0]
            action =  bpy.data.actions.get(f'{chunk.name} ({clump.name})')

            if action:
                action.name = chunk.name

        
        return {'FINISHED'}

        


class ExportDict(bpy.types.Operator, ExportHelper):
    bl_idname = "object.export_dict"
    bl_label = "Export Bones Dict"
    bl_description = "Export your bone dictionary to a json file"

    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default='*.json;', options={'HIDDEN'})

    def execute(self, context):
        
        bone_dictionary = {}
        for i in range(len(context.scene.col_prop.bone_dict)):
            bone_dictionary[context.scene.col_prop.bone_dict[i].bone_main] = context.scene.col_prop.bone_dict[i].bone_target
        
        #save the dictionary to a json file
        with open(self.filepath, 'w') as f:
            json.dump(bone_dictionary, f, indent=4)
        
        self.report({'INFO'}, "Saved bone dictionary to " + self.filepath)
        return {'FINISHED'}

class RemakeShaders(bpy.types.Operator):
    bl_idname = "object.remake_shaders"
    bl_label = "Remake XFBIN Shaders"
    bl_description = 'Delete the current shaders and remake them, this is useful for when you import a texture file'
    @classmethod
    def poll(cls, context):
        return bpy.context.mode == 'OBJECT'
    
    def execute(self, context):
        #Shader functions
        shaders_dict = {'00 00 F0 0A': F00A, '00 01 F0 0A': F00A, '00 02 F0 0A': _02_F00A, '00 05 F0 0D': _05_F00D,
        '00 01 F0 0D': _05_F00D, '00 01 F0 03': _01_F003, '00 05 F0 03': _01_F003, '00 05 F0 02': _05_F002, '00 07 F0 02':_07_F002,
        '00 00 E0 02': E002, '00 07 F0 10':_07_F010, '00 03 F0 10':_07_F010, '00 07 F0 0D':_07_F00D, '00 01 F0 02':_01_F002,
        '00 01 F0 08':_01_F008, '00 01 F0 0F':_01_F00F, '00 03 F0 0F':_03_F00F}
        objects = [o for o in context.object.users_collection[0].objects if o.type == 'MESH']
        for o in objects:
            parent = o.parent.parent
            xfbin_mat = parent.xfbin_clump_data.materials[o.xfbin_mesh_data.xfbin_material]
            if f'[XFBIN] {xfbin_mat.name}' in bpy.data.materials:
                bpy.data.materials.remove(bpy.data.materials.get(f'[XFBIN] {xfbin_mat.name}'))


        for o in objects:
            parent = o.parent.parent
            if o.xfbin_mesh_data.materials[0].name in shaders_dict:
                meshmat = o.xfbin_mesh_data.materials[0]
                xfbin_mat = parent.xfbin_clump_data.materials[o.xfbin_mesh_data.xfbin_material]
                if f'[XFBIN] {xfbin_mat.name}' not in bpy.data.materials:
                    material = shaders_dict.get(o.xfbin_mesh_data.materials[0].name)(self, meshmat, xfbin_mat, f'[XFBIN] {xfbin_mat.name}', xfbin_mat.name)
                    o.material_slots[0].material = material
                else:
                    o.material_slots[0].material = bpy.data.materials[f'[XFBIN] {xfbin_mat.name}']
            else:
                xfbin_mat = parent.xfbin_clump_data.materials[o.xfbin_mesh_data.xfbin_material]

                material = bpy.data.materials.new(f'[XFBIN] {xfbin_mat.name}')
                material.use_nodes = True
                material.blend_method = 'CLIP'
                material.shadow_method = 'CLIP'

                #remove node groups with the same name to prevent issues with min and max values of some nodes
                if bpy.data.node_groups.get(xfbin_mat.name):
                    bpy.data.node_groups.remove(bpy.data.node_groups.get(xfbin_mat.name))
                

                if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
                    #texcount = len(xfbin_mat.texture_groups[0].textures)
                    not_included = ['celshade', 'haching', 'haching1', 'haching2', 'haching_n', '1efc_pro_noise01']
                    prev_index = 0
                    for i in range(len(xfbin_mat.texture_groups[0].textures)):
                        if i == 0:
                            globals()[f'image_name_{i}'] = xfbin_mat.texture_groups[0].textures[i].texture
                            globals()[f'uv_{i}'] = material.node_tree.nodes.new('ShaderNodeUVMap')
                            globals()[f'uv_{i}'].uv_map = f'UV_{i}'
                            globals()[f'tex_{i}'] = material.node_tree.nodes.new('ShaderNodeTexImage')
                            globals()[f'tex_{i}'].name = f'Texture_{i}'
                            globals()[f'tex_{i}'].image = bpy.data.images.get(globals()[f'image_name_{i}'])
                            material.node_tree.links.new(globals()[f'uv_{i}'].outputs[0], globals()[f'tex_{i}'].inputs[0])
                            pBSDF = material.node_tree.nodes.get('Principled BSDF')
                            material.node_tree.links.new(globals()[f'tex_{i}'].outputs[0], pBSDF.inputs['Base Color'])
                            material.node_tree.links.new(globals()[f'tex_{i}'].outputs[1], pBSDF.inputs['Alpha'])
                            prev_index = i
                            print(prev_index)
                        if i > 0 and xfbin_mat.texture_groups[0].textures[i].texture_name not in not_included:
                            globals()[f'image_name_{i}'] = xfbin_mat.texture_groups[0].textures[i].texture
                            globals()[f'uv_{i}'] = material.node_tree.nodes.new('ShaderNodeUVMap')
                            globals()[f'uv_{i}'].uv_map = f'UV_{i}'
                            globals()[f'tex_{i}'] = material.node_tree.nodes.new('ShaderNodeTexImage')
                            globals()[f'tex_{i}'].name = f'Texture_{i}'
                            globals()[f'tex_{i}'].image = bpy.data.images.get(globals()[f'image_name_{i}'])
                            globals()[f'mix_{i}'] = material.node_tree.nodes.new('ShaderNodeMixRGB')
                            globals()[f'mix_{i}'].blend_type = 'MIX'
                            globals()[f'mix_{i}'].inputs[0].default_value = 1
                            material.node_tree.links.new(globals()[f'uv_{i}'].outputs[0], globals()[f'tex_{i}'].inputs[0])
                            material.node_tree.links.new(globals()[f'tex_{i}'].outputs[1], globals()[f'mix_{i}'].inputs[0])
                            material.node_tree.links.new(globals()[f'tex_{prev_index}'].outputs[0], globals()[f'mix_{i}'].inputs[1])
                            material.node_tree.links.new(globals()[f'tex_{i}'].outputs[0], globals()[f'mix_{i}'].inputs[2])
                            material.node_tree.links.new(globals()[f'mix_{i}'].outputs[0], pBSDF.inputs['Base Color'])
                            prev_index += 1
                            print(prev_index)
                o.material_slots[0].material = material
            
        return {'FINISHED'}