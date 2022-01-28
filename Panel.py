import bpy
from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatVectorProperty
from bpy.types import (Panel)

class Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_idname = "HYDRA_PT_Panel"
    bl_region_type = "UI"
    bl_label = "Hydra Tools"
    bl_category = "Hydra Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        colprop = scene.col_prop

        obj = context.object
        row = layout.row()
        layout.prop(colprop, 'collections')
        row = layout.row()
        layout.prop(colprop, 'armatures')
        row = layout.row()
        
        col = layout.column_flow(columns=2, align=False)
        col.prop(colprop, 'S1Model')
        col.operator("object.remove_lod")
        
        row = layout.row()
        col = layout.column_flow(columns=2, align=True)
        col.operator("object.add_v_colors")
        col.operator("object.remove_v_colors")
        
        row = layout.row()
        col = layout.column_flow(columns=2, align=False)
        col.operator("object.paint_v_colors")
        col.prop(colprop, 'VertColorPick', text= "")
        
        row = layout.row() 
        col = layout.column_flow(columns=3, align=True)
        col.operator("object.remove_char_code")
        col.operator("object.rename_script")
        col.operator("object.add_char_code")
        
        row = layout.row()
        row.operator("object.applypose")
    
class ColProperty(bpy.types.PropertyGroup):

    def collection_list(self, context):
        
        items = []
        
        for collection in bpy.data.collections:
            ColName = (collection.name, collection.name, "")
            items.append(ColName)   
        return items 
    


    def armature_list(self, context):
        
        collections = bpy.data.collections
        colprop = bpy.context.scene.col_prop
        
        items = []
        
        for a in collections[colprop.collections].all_objects:
            if a.type == 'ARMATURE':
                Name = (a.name, a.name, "")
                items.append(Name)
        return items

    collections: bpy.props.EnumProperty(
    items=collection_list,
    name='Collection',
    description="The collection that's going to be used for all operations")
    
    armatures: bpy.props.EnumProperty(
    items=armature_list,
    name='Armature',
    description="The armature that's going to be used for armature related operations")
    
    S1Model: BoolProperty(
    name='S1 Model?',
    description="This checkbox will change the behaviour of 'Remove LOD' function to \n"
    "prevent the model from crashing the game.\n\n"
    "NOTE: This only needed in Storm 1 models")
    
    VertColorPick: FloatVectorProperty(
    name= 'Color',
    description= ("The color that will be used to paint all meshes."),
    default= (0.5, 0.5, 0.5),
    subtype='COLOR_GAMMA',
    min=(0),
    max=(1))
