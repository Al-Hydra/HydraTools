import bpy, json, os
from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatVectorProperty
from bpy.types import (Operator)
from bpy_extras.io_utils import ImportHelper


class RemoveLOD(bpy.types.Operator):
    bl_idname = "object.remove_lod"
    bl_label = "Remove LOD"
    bl_description = ('This button will remove LOD meshes, adjust LOD flags and\n'
    'delete the first and the third model groups for the active Armature.\n\n'
    "NOTE: if 'S1 Model?' is checked, all the objects in the remaining model group\n"
    "will be deleted to prevent crashes")
    
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
            
        lod = {"_lod1", "_lod2", "_LOD1", "_LOD2",
         "_shadow", "_blur0 shadow", "_blur0 shadow01"}
             
        for obj in collections[colprop.collections].all_objects:
            obj.hide_set(False) 
            if any(x in obj.name for x in lod):
                obj.select_set(True)
        bpy.ops.object.delete(use_global=True, confirm=True)
        bpy.context.scene.objects[colprop.armatures].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[colprop.armatures]
        bpy.context.object.xfbin_clump_data.coord_flag0 = 1
        bpy.context.object.xfbin_clump_data.coord_flag1 = 1
        model_group_array = bpy.context.object.xfbin_clump_data.model_groups
        if (len(model_group_array) != 1):
            model_group_array.remove(2)
            model_group_array.remove(0)
        if colprop.S1Model == True:
            bpy.context.object.xfbin_clump_data.model_groups[0].models.clear()
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
        bpy.ops.object.select_all(action='DESELECT')
        for obj in collections[colprop.collections].all_objects:
            obj.hide_set(False)
            obj.select_set(True)
    
        for i, obj in enumerate(bpy.context.selected_objects):
            if (obj.type == 'MESH'):
                if (len(obj.data.vertex_colors) == 0):
                    obj.data.vertex_colors.new()
                else:
                    self.report({'INFO'}, str(obj.name) + " Has at least 1 vertex colors layer")
        bpy.ops.object.select_all(action='DESELECT')
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
        bpy.ops.object.select_all(action='DESELECT')
        for obj in collections[colprop.collections].all_objects:
            if (obj.type == 'MESH'):
                obj.hide_set(False)
                obj.select_set(True)
    
        for obj in bpy.context.selected_objects:
                while obj.data.vertex_colors:
                    obj.data.vertex_colors.remove(obj.data.vertex_colors[0])
                self.report({'INFO'}, "Vertex Colors layers in" + str(obj.name) + " are removed")
        bpy.ops.object.select_all(action='DESELECT')
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
        
        for obj in collections[colprop.collections].all_objects:
            if (obj.type == 'MESH'):
                obj.hide_set(False)
                obj.select_set(True)
                
        for i, obj in enumerate(bpy.context.selected_objects):
            bpy.context.view_layer.objects.active = obj
            bpy.ops.paint.vertex_paint_toggle()
            bpy.context.scene.col_prop.VertColorPick
            bpy.data.brushes["Draw"].color = bpy.context.scene.col_prop.VertColorPick
            bpy.ops.paint.vertex_color_set()
            bpy.ops.paint.vertex_paint_toggle()
            
        bpy.ops.object.select_all(action='DESELECT')
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
        
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in collections[colprop.collections].all_objects:
            if (obj.type == 'MESH'):
                obj.hide_set(False)
                obj.select_set(True)
                
        for i, obj in enumerate(bpy.context.selected_objects):
            mod = obj.modifiers.new(type='ARMATURE', name='ArmatureToApply')
            mod.object = bpy.data.objects[colprop.armatures]
            #bpy.ops.object.select_all(action='DESELECT')

        for obj in bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = obj
            for mod in [m for m in obj.modifiers if m.type == 'ARMATURE']:
                bpy.ops.object.modifier_apply( modifier = "ArmatureToApply" )
                bpy.ops.object.select_all(action='DESELECT')
                
        bpy.context.scene.objects[colprop.armatures].select_set(True)
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
        charbone = a_object.data.bones[1]
        char_id = a_object.data.bones[1].name
        filter_char_id = char_id[:4] + '_'
        filtered_bones = [
        'asianimel01', 'asianimel02', 'asianimel03', 'asianimel04','asianimel',
        'asianimer01', 'asianimer02', 'asianimer03', 'asianimer04','asianimer',
        'udeanmr01', 'udeanmr02', 'udeanmr03', 'udeanmr04', 'udeanmr',
        'udeanml01', 'udeanml02', 'udeanml03', 'udeanml04', 'udeanml',]  
        filtered_bones = [filter_char_id + x for x in filtered_bones]
        for bone in [*a_object.data.bones]:
            if bone.name[0:8] == char_id and len(bone.name) > 8 and bone.name not in filtered_bones:
                bone.name = bone.name[9:]
                self.report({'INFO'}, "ID: (" + str(char_id) + ") Removed from (" + str(bone.name) + ")")
        
        bpy.ops.object.select_all(action='DESELECT')
        
        for c in bpy.data.objects[colprop.armatures].children:
            for child in c.children:
                if child.type == 'MESH':
                    child.hide_set(False)
                    child.select_set(True)
        for i, obj in enumerate(bpy.context.selected_objects):
            for mod in [m for m in obj.modifiers if m.type == 'ARMATURE']:
                mod.object = bpy.data.objects[colprop.armatures]
                
        bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}
    
class RenameBones(Operator, ImportHelper):
    bl_idname = "object.rename_script"
    bl_label = "Translate Bones"
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
        ab = bpy.data.objects[colprop.armatures].data.bones
        char_id = a_object.data.bones[1].name   
        filter_char_id = char_id[:4] + '_'
        filtered_bones = [
        'asianimel01', 'asianimel02', 'asianimel03', 'asianimel04','asianimel',
        'asianimer01', 'asianimer02', 'asianimer03', 'asianimer04','asianimer',
        'udeanmr01', 'udeanmr02', 'udeanmr03', 'udeanmr04', 'udeanmr',
        'udeanml01', 'udeanml02', 'udeanml03', 'udeanml04', 'udeanml', char_id]  
        filtered_bones = [filter_char_id + x for x in filtered_bones]

        if ab[0].name[0:8] == char_id and ab[0].name not in filtered_bones:
            self.report({'WARNING'}, "You need to remove the character ID first!")

        for bone in [*a_object.data.bones]:
            if bone.name[0:8] != char_id and bone.name not in filtered_bones:
                self.report({'INFO'}, "ID: (" + str(char_id) + ") added to (" + str(bone.name) + ")")
                bone.name = char_id + ' ' + bone.name
        
        bpy.ops.object.select_all(action='DESELECT')
        
        for c in bpy.data.objects[colprop.armatures].children:
            for child in c.children:
                if child.type == 'MESH':
                    child.hide_set(False)
                    child.select_set(True)
                    
        for i, obj in enumerate(bpy.context.selected_objects):
            for mod in [m for m in obj.modifiers if m.type == 'ARMATURE']:
                mod.object = bpy.data.objects[colprop.armatures]
        
        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}
