import bpy, json
from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatVectorProperty, StringProperty, CollectionProperty, IntProperty, FloatProperty
from bpy.types import (Panel, Collection, PropertyGroup)

class Panel_Main(Panel):
    bl_space_type = "VIEW_3D"
    bl_idname = "HYDRA_PT_Panel_Main"
    bl_region_type = "UI"
    bl_label = "Main Panel"
    bl_category = "HydraTools"

    @classmethod
    def poll(cls, context):
        return context

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        colprop = bpy.context.scene.col_prop

        obj = context.object
        row = layout.row()
        layout.prop_search(colprop, 'collections', bpy.data, 'collections', text= 'Collection')
        row = layout.row()
        layout.prop(colprop, 'armatures')
        row = layout.row()
        row.operator("object.remove_lod")
        col = layout.column_flow(columns=2, align=True)
        col.operator("object.remove_char_code")
        col.operator("object.add_char_code")



class Panel_Armature(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "HYDRA_PT_Panel_Armature"
    bl_label = "Armature Tools"
    bl_category = "HydraTools"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return len(bpy.data.collections) > 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        colprop = bpy.context.scene.col_prop

        obj = context.object
        row = layout.row()
        row.operator("object.rename_script")
        
        
        row = layout.row()
        row.operator("object.applypose")

        row = layout.row()
        row.label(text= 'Copy bones position from a another armature')
        layout.prop_search(scene, 'armaturelist', bpy.data, 'objects', text= 'Copy from')
        row = layout.row()
        row.operator('object.copy_pos')

class Panel_Material(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "HYDRA_PT_Panel_Material"
    bl_label = "Material Tools"
    bl_category = "HydraTools"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return len(bpy.data.collections) > 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        colprop = bpy.context.scene.col_prop

        obj = context.object

        label = layout.label(text = 'XFBIN Materials and Material IDs:')
        row = layout.row()
        row.prop(colprop, 'AutoMatID')

        row = layout.row()
        if colprop.AutoMatID == True:
            if obj.type == 'MESH' and obj.xfbin_mesh_data is not None and len(obj.xfbin_mesh_data.materials.keys()) > 0:
                row.label(text= f"Main Material ID = {obj.xfbin_mesh_data.materials[0]['material_id']}")
            else:
                row.label(text= 'No Data')
        else:
            row.prop(colprop, 'Old_Material_ID')
        
        layout.prop(colprop, 'New_Material_ID')
        layout.operator("object.replace_mats")
        layout.prop(colprop, 'XFBIN_Mat')
        layout.operator("object.duplicate_mats")
        layout.operator("object.remake_shaders")

class Panel_Swap(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "HYDRA_PT_Panel_Swap"
    bl_label = "Swap and Clone Tools"
    bl_category = "HydraTools"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return len(bpy.data.collections) > 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        colprop = bpy.context.scene.col_prop

        obj = context.object

        row = layout.row()
        row.prop(colprop, 'TexMat')

        row = layout.row()
        layout.prop(colprop, 'PathCode')

        row = layout.row()
        layout.prop(colprop, 'CharacterCode')

        row = layout.row()
        layout.prop(colprop, 'ModelID')
        
        row = layout.row()
        row.operator("object.swap_code")

        #row = layout.row() 
        #col = layout.column_flow(columns=3, align=True)
        #col.operator('object.clone')
        #col.prop(colprop, 'BodID')
        #col.prop(colprop, 'CloneID')
        row = layout.row() 
        row.operator('object.dmg_bod')
        row = layout.row()
        row.operator("object.reg_bod")
        row = layout.row() 
        row.label(text= 'For Jojo models only')
        row = layout.row() 
        col = layout.column_flow(columns=2, align=True)
        col.prop(colprop, 'FlipMeshes')
        col.prop(colprop, 'FlipBones')
        row = layout.row()
        row.operator('object.bod1f')
        


class Panel_misc(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "HYDRA_PT_Panel_misc"
    bl_label = "Other Tools"
    bl_category = "HydraTools"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return len(bpy.data.collections) > 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        colprop = bpy.context.scene.col_prop

        obj = context.object
        row = layout.row()
        col = layout.column_flow(columns=2, align=True)
        col.operator("object.add_v_colors")
        col.operator("object.remove_v_colors")
        
        row = layout.row()
        col = layout.column_flow(columns=2, align=False)
        col.operator("object.paint_v_colors")
        col.prop(colprop, 'VertColorPick', text= "")

        label = layout.label(text = 'Posing and Animation ONLY:')
        row = layout.row()
        row.operator("object.ik")
        
        row = layout.row()
        row.operator("object.fix_names")
        row = layout.row()
        row.operator("object.add_armature_modifier")

'''
class Panel_dict(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "HYDRA_PT_Panel_dict"
    bl_label = "Dict Tool"
    bl_category = "HydraTools"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return len(bpy.data.collections) > 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        colprop = bpy.context.scene.col_prop
         
        row = layout.row()
        col = row.column_flow(columns=2, align=True)
        row = layout.row()
        row.operator('object.build_bone_list')
        col.prop_search(scene, 'main_armature', bpy.data, 'objects', text= 'Base')
        col.prop_search(scene, 'target_armature', bpy.data, 'objects', text= 'Target')
        
        obj = context.object
        box = layout.box()
        box.label(text = 'Dictionary:')
        row = box.row()
        row.template_list("DICT_UL_BoneList", "BoneList", colprop, "bone_dict", scene, "bone_index", rows=1, maxrows=10)
        row = layout.row()
        row.operator('object.export_dict')
'''

class BoneList(bpy.types.PropertyGroup):
    
    bone_main: StringProperty(
    name = 'Bone Main',
    )
    bone_target: StringProperty(
    name = 'Bone Target',
    )


class DICT_UL_BoneList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout = layout.split(factor=0.36, align=True)

        # Displays source bone
        layout.label(text=item.bone_main)

        # Displays target bone
        if context.scene.target_armature:
            layout.prop_search(item, 'bone_target', bpy.context.scene.target_armature.pose, "bones", text='')


class RETARGET_UL_AnimList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout = layout.split(factor=0.36, align=True)

        # Displays source bone
        layout.label(text=item.bone_main)

        # Displays target bone
        if context.scene.target_armature:
            layout.prop_search(item, 'bone_target', bpy.context.scene.target_armature.pose, "bones", text='')


class RetargetProperty(PropertyGroup):
    source_armature: StringProperty(
    name='Source Armature',
    )

    target_armature: StringProperty(
    name='Target Armature',
    )

    anims_object: StringProperty(
    name='Anims Object',
    )



class RetargetPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "HYDRA_PT_Panel_Retarget"
    bl_label = "Retarget Tools"
    bl_category = "HydraTools"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return len(bpy.data.collections) > 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        colprop = bpy.context.scene.col_prop
        reprop = bpy.context.scene.retarget_prop

        obj = context.object
        row = layout.row()
        row.prop_search(scene, 'main_armature', bpy.data, 'objects', text= 'Source')
        row = layout.row()
        row.prop_search(scene, 'target_armature', bpy.data, 'objects', text= 'Target')
        row = layout.row()
        row.prop_search(reprop, 'anims_object', bpy.data, 'objects', text= 'Anims Object')

        row = layout.row()
        row.operator("object.retarget_storm_anim")
        row.operator("object.retarget_all_storm_anims")
        row = layout.row()
        row.operator("object.clone_anm_object")
        row = layout.row()
        row.operator("object.correct_anm_names")




class ColProperty(PropertyGroup):

    def collection_list(self, context):
        
        items = []
        
        for collection in bpy.data.collections:
            ColName = (collection.name, collection.name, "")
            items.append(ColName)   
        return items 
    


    def armature_list(self, context):
        
        colprop = bpy.context.scene.col_prop

        collection = bpy.data.collections.get(colprop.collections)
        
        if collection:
            return [(ob.name, ob.name, "") for ob in collection.objects if ob.type == 'ARMATURE']
        else:
            return []        
        
    

    collections: StringProperty(
    name='Collection',
    description="The collection that's going to be used for all operations")
    
    armatures: EnumProperty(
    name = 'Armature',
    items = armature_list,
    description="The armature that's going to be used for armature related operations")

    target_armature: StringProperty(
    name='Copy from(Target) ',
    description="This will be the armature you're gonna copy bone positions from")

    VertColorPick: FloatVectorProperty(
    name= 'Color',
    description= ("The color that will be used to paint all meshes."),
    default= (0.5, 0.5, 0.5),
    subtype='COLOR_GAMMA',
    min=(0),
    max=(1))

    PathCode: StringProperty(
    name= 'Path Code',
    default= 'code',
    description= "This code will be used in textures, materials, clump and some meshes.\n"
    "Example (c/code/....)"
    )

    CharacterCode: StringProperty(
    name= 'Object Code',
    default= 'code',
    description= 'Character code can be 4, 6 or more characters depending on the model/game you want to use it for.\n'
    "FOR CODES THAT END WITH 01 FOR EXAMPLE, THE MODEL ID MUST ONLY BE (t0) and not 00t0"
    )

    ModelID: StringProperty(
    name= 'Model ID',
    default= 'xxtx',
    maxlen= 4,
    description= "00t0 for Naruto models and t0 for Jojo "
    )

    BodID: StringProperty(
    name= 'Bod ID',
    default= 'bod2',
    maxlen= 4,
    description= "first clone = bod2, second clone = bod3"
    )

    CloneID: StringProperty(
    name= 'Clone Model ID',
    default= '01t0',
    maxlen= 4,
    description= "first clone = 01t0, second clone = 02t0"
    )

    Old_Material_ID: StringProperty(
    name = 'Old Material ID',
    default = '00 00 00 00',
    maxlen= 11,
    description = "You put the material ID you want to replace here. EXAMPLE: (00 00 F0 0A)"
    )

    New_Material_ID: StringProperty(
    name = 'New Material ID',
    default = '00 00 00 00',
    maxlen= 11,
    description = "You put the new material ID here. EXAMPLE: (00 02 00 01)",
    )

    AutoMatID: BoolProperty(
    name = 'Auto Select Material ID',
    description = ''
    )

    XFBIN_Mat: StringProperty(
    name = 'XFBIN Material Name',
    description = "This is the name of the new material that will be created.\n"
    "If you leave this blank, a new material will be created with the word 'NEW' in it.",
    )
    
    TexMat: BoolProperty(
    name = 'Edit Texture and Material Paths',
    description = ''
    )

    FlipMeshes: BoolProperty(
    name = 'Flip Meshes',
    description = 'Flip meshes when creating the bod1_f model'
    )

    FlipBones: BoolProperty(
    name = 'Flip Bones',
    description = 'Flip bones when creating the bod1_f model'
    )
