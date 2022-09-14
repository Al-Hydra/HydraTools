import bpy

#Materials
def F00A(self, meshmat, xfbin_mat, matname, nodegrp = 'F00A'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True

	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (330, 41)
	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Basic Cel-shader setup
	diffuse_bsdf = nodegroup.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
	diffuse_bsdf.location = (-393, 105)

	shader_rgb = nodegroup.node_tree.nodes.new('ShaderNodeShaderToRGB')
	shader_rgb.location = (-193, 156)

	math_greater = nodegroup.node_tree.nodes.new('ShaderNodeMath')
	math_greater.location = (2, 175)
	math_greater.operation = 'GREATER_THAN'
	math_greater.inputs[1].default_value = 0.15

	lighten = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	lighten.location = (192, 134)
	lighten.blend_type = 'LIGHTEN'
	lighten.inputs[0].default_value = 1

	multiply = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply.location = (407, 118)
	multiply.blend_type = 'MULTIPLY'
	multiply.inputs[0].default_value = 1

	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-126, -140)
	nodegroup.inputs.new('NodeSocketColor','Texture')
	nodegroup.inputs.new('NodeSocketColor','Alpha')

	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (638, 74)
	nodegroup.outputs.new('NodeSocketShader','Out')

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (-27, -23)
	tex1.name = 'F00A TEX'

	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (603, 85)

	#Link nodes
	nodegroup.node_tree.links.new(diffuse_bsdf.outputs['BSDF'], shader_rgb.inputs['Shader'])

	nodegroup.node_tree.links.new(shader_rgb.outputs['Color'], math_greater.inputs[0])

	nodegroup.node_tree.links.new(math_greater.outputs[0], lighten.inputs[1])

	nodegroup.node_tree.links.new(lighten.outputs[0], multiply.inputs[1])

	nodegroup.node_tree.links.new(multiply.outputs[0], mix_shader.inputs[2])

	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], multiply.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs['Alpha'], mix_shader.inputs[0])

	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs['Texture'])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[1])


	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])
	
	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)

	return material

def _02_F00A(self, meshmat, xfbin_mat, matname, nodegrp = '02F00A'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True
	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	#for node in bpy.data.node_groups:
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (330, 41)
	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Basic Cel-shader setup
	diffuse_bsdf = nodegroup.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
	diffuse_bsdf.location = (-393, 105)

	shader_rgb = nodegroup.node_tree.nodes.new('ShaderNodeShaderToRGB')
	shader_rgb.location = (-193, 156)

	math_greater = nodegroup.node_tree.nodes.new('ShaderNodeMath')
	math_greater.location = (2, 175)
	math_greater.operation = 'GREATER_THAN'
	math_greater.inputs[1].default_value = 0.15

	lighten = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	lighten.location = (192, 134)
	lighten.blend_type = 'LIGHTEN'
	lighten.inputs[0].default_value = 1

	multiply1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply1.location = (407, 118)
	multiply1.blend_type = 'MULTIPLY'
	multiply1.inputs[0].default_value = 1

	mix1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	mix1.location = (407, 158)
	mix1.blend_type = 'MIX'
	mix1.inputs[0].default_value = 1

	#This will be used for texture 2 visibility
	mix2 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	mix2.location = (407, 0)
	mix2.blend_type = 'MIX'
	mix2.inputs[1].default_value = (0, 0, 0, 1)

	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-126, -140)
	nodegroup.inputs.new('NodeSocketColor','Texture1')
	nodegroup.inputs.new('NodeSocketColor','Texture2')
	nodegroup.inputs.new('NodeSocketColor','Alpha1')
	nodegroup.inputs.new('NodeSocketColor','Alpha2')
	nodegroup.inputs.new('NodeSocketFloat','Texture2 Visibility')
	bpy.data.node_groups[nodegroup.name].inputs[4].min_value = 0.0
	bpy.data.node_groups[nodegroup.name].inputs[4].max_value = 1.0
	
	nodegroup.inputs[4].default_value = 1.0


	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (638, 74)
	nodegroup.outputs.new('NodeSocketShader','Out')

	uv1 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv1.location = (-77, -23)
	uv1.uv_map = 'UV_0'

	uv2 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv2.location = (-77, -23)
	uv2.uv_map = 'UV_1'

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (-27, -23)
	tex1.name = 'Texture1'

	tex2 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex2.location = (-27, -43)
	tex2.name = 'Texture2'

	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (603, 85)

	#Link nodes
	nodegroup.node_tree.links.new(diffuse_bsdf.outputs['BSDF'], shader_rgb.inputs['Shader'])

	nodegroup.node_tree.links.new(shader_rgb.outputs['Color'], math_greater.inputs[0])

	nodegroup.node_tree.links.new(math_greater.outputs[0], lighten.inputs[1])

	nodegroup.node_tree.links.new(lighten.outputs[0], multiply1.inputs[1])

	nodegroup.node_tree.links.new(mix1.outputs[0], multiply1.inputs[2])

	nodegroup.node_tree.links.new(group_input.outputs[0], mix1.inputs[1])

	nodegroup.node_tree.links.new(group_input.outputs[1], mix1.inputs[2])

	nodegroup.node_tree.links.new(group_input.outputs[2], mix_shader.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[3], mix2.inputs[2])

	nodegroup.node_tree.links.new(group_input.outputs[4], mix2.inputs[0])

	nodegroup.node_tree.links.new(mix2.outputs[0], mix1.inputs[0])

	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(multiply1.outputs[0], mix_shader.inputs[2])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	material.node_tree.links.new(uv1.outputs[0], tex1.inputs[0])
	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs['Texture1'])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs['Alpha1'])

	material.node_tree.links.new(uv2.outputs[0], tex2.inputs[0])
	material.node_tree.links.new(tex2.outputs[0], nodegroup.inputs['Texture2'])
	material.node_tree.links.new(tex2.outputs[1], nodegroup.inputs['Alpha2'])

	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])
	
	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)
		image_name2 = xfbin_mat.texture_groups[0].textures[1].name
		tex2.image = bpy.data.images.get(image_name2)

	return material

def _01_F002(self, meshmat, xfbin_mat, matname, nodegrp = '01F002'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True
	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (721, 611)
	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Nodes
	multiply1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply1.location = (256, 131)
	multiply1.blend_type = 'MULTIPLY'
	multiply1.inputs[0].default_value = 1

	emission = nodegroup.node_tree.nodes.new('ShaderNodeEmission')

	multiply2 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply2.location = (256, 131)
	multiply2.blend_type = 'MULTIPLY'
	multiply2.inputs[0].default_value = 1

	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')
	transparent.location = (264, -261)

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')
	mix_shader.location = (696, -113)

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-56, -112)
	nodegroup.inputs.new('NodeSocketColor','Diffuse Texture')
	nodegroup.inputs.new('NodeSocketColor','Alpha')
	nodegroup.inputs.new('NodeSocketFloat','Light Strength')
	nodegroup.inputs[2].default_value = 2
	nodegroup.inputs.new('NodeSocketColor','Vertex Colors')
	nodegroup.inputs.new('NodeSocketColor','Vertex Alpha')

	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (886, 4)
	nodegroup.outputs.new('NodeSocketShader','Out')

	vcol = material.node_tree.nodes.new('ShaderNodeVertexColor')

	uv1 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv1.location = (-84, -552)
	uv1.uv_map = 'UV_0'

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (174, 720)
	tex1.name = 'Diffuse'

	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (1091, 520)

	#Link nodes
	nodegroup.node_tree.links.new(multiply1.outputs[0], emission.inputs[0])

	nodegroup.node_tree.links.new(emission.outputs[0], mix_shader.inputs[2])
	
	nodegroup.node_tree.links.new(multiply2.outputs[0], mix_shader.inputs[0])

	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], multiply1.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[1], multiply2.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[2], emission.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[3], multiply1.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[4], multiply2.inputs[2])

	material.node_tree.links.new(uv1.outputs[0], tex1.inputs[0])
	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs[0])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[1])

	material.node_tree.links.new(vcol.outputs[0], nodegroup.inputs[3])
	material.node_tree.links.new(vcol.outputs[1], nodegroup.inputs[4])

	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])

	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)

	return material

def _01_F003(self, meshmat, xfbin_mat, matname, nodegrp = '01F003'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True
	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (721, 611)
	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Nodes
	diffuse_bsdf = nodegroup.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
	diffuse_bsdf.location = (-519, 304)

	shader_rgb = nodegroup.node_tree.nodes.new('ShaderNodeShaderToRGB')
	shader_rgb.location = (-327, 305)

	math_greater = nodegroup.node_tree.nodes.new('ShaderNodeMath')
	math_greater.location = (-163, 320)
	math_greater.operation = 'GREATER_THAN'
	math_greater.inputs[1].default_value = 0.00

	lighten = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	lighten.location = (47, 300)
	lighten.blend_type = 'LIGHTEN'
	lighten.inputs[0].default_value = 1
	lighten.inputs[2].default_value = (0.2,0.2,0.2,1)

	multiply1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply1.location = (256, 131)
	multiply1.blend_type = 'MULTIPLY'
	multiply1.inputs[0].default_value = 1

	multiply2 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply2.location = (256, 131)
	multiply2.blend_type = 'MULTIPLY'
	multiply2.inputs[0].default_value = 1

	multiply3 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply3.location = (256, 131)
	multiply3.blend_type = 'MULTIPLY'
	multiply3.inputs[0].default_value = 1

	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')
	transparent.location = (264, -261)

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')
	mix_shader.location = (696, -113)

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-56, -112)
	nodegroup.inputs.new('NodeSocketColor','Diffuse Texture')
	nodegroup.inputs.new('NodeSocketColor','Alpha')
	nodegroup.inputs.new('NodeSocketColor','Vertex Colors')
	nodegroup.inputs.new('NodeSocketColor','Vertex Alpha')

	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (886, 4)
	nodegroup.outputs.new('NodeSocketShader','Out')

	vcol = material.node_tree.nodes.new('ShaderNodeVertexColor')

	uv1 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv1.location = (-84, -552)
	uv1.uv_map = 'UV_0'

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (174, 720)
	tex1.name = 'Diffuse'

	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (1091, 520)

	#Link nodes
	nodegroup.node_tree.links.new(diffuse_bsdf.outputs['BSDF'], shader_rgb.inputs['Shader'])

	nodegroup.node_tree.links.new(shader_rgb.outputs['Color'], math_greater.inputs[0])

	nodegroup.node_tree.links.new(math_greater.outputs[0], lighten.inputs[1])

	nodegroup.node_tree.links.new(lighten.outputs[0], multiply1.inputs[1])

	nodegroup.node_tree.links.new(multiply1.outputs[0], multiply2.inputs[1])

	nodegroup.node_tree.links.new(multiply2.outputs[0], mix_shader.inputs[2])

	nodegroup.node_tree.links.new(multiply3.outputs[0], mix_shader.inputs[0])

	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], multiply1.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[1], multiply3.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[2], multiply2.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[3], multiply3.inputs[2])

	material.node_tree.links.new(vcol.outputs[0], nodegroup.inputs[2])
	material.node_tree.links.new(vcol.outputs[1], nodegroup.inputs[3])

	material.node_tree.links.new(uv1.outputs[0], tex1.inputs[0])
	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs[0])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[1])

	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])

	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)

	return material

def _01_F008(self, meshmat, xfbin_mat, matname, nodegrp = '01F008'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True
	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (721, 611)
	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Nodes
	mix1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	mix1.location = (256, 131)
	mix1.blend_type = 'MIX'
	mix1.inputs[0].default_value = 1

	multiply1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply1.location = (256, 131)
	multiply1.blend_type = 'MULTIPLY'
	multiply1.inputs[0].default_value = 1

	emission = nodegroup.node_tree.nodes.new('ShaderNodeEmission')

	multiply2 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply2.location = (256, 131)
	multiply2.blend_type = 'MULTIPLY'
	multiply2.inputs[0].default_value = 1

	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')
	transparent.location = (264, -261)

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')
	mix_shader.location = (696, -113)

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-56, -112)
	nodegroup.inputs.new('NodeSocketColor','Diffuse Texture')
	nodegroup.inputs.new('NodeSocketColor','Alpha')
	nodegroup.inputs.new('NodeSocketColor','Falloff Texture')
	nodegroup.inputs.new('NodeSocketFloat','Light Strength')
	nodegroup.inputs[3].default_value = 2
	nodegroup.inputs.new('NodeSocketFloat','Light Limit')
	bpy.data.node_groups[nodegroup.name].inputs[4].min_value = 0
	bpy.data.node_groups[nodegroup.name].inputs[4].max_value = 1
	nodegroup.inputs.new('NodeSocketColor','Vertex Colors')
	nodegroup.inputs.new('NodeSocketColor','Vertex Alpha')

	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (886, 4)
	nodegroup.outputs.new('NodeSocketShader','Out')

	vcol = material.node_tree.nodes.new('ShaderNodeVertexColor')

	uv1 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv1.location = (-84, -552)
	uv1.uv_map = 'UV_0'

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (174, 720)
	tex1.name = 'Diffuse'

	tex2 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex2.location = (174, 720)
	tex2.name = 'Falloff'

	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (1091, 520)

	#Link nodes
	nodegroup.node_tree.links.new(mix1.outputs[0], multiply1.inputs[1])

	nodegroup.node_tree.links.new(multiply1.outputs[0], emission.inputs[0])

	nodegroup.node_tree.links.new(emission.outputs[0], mix_shader.inputs[2])
	
	nodegroup.node_tree.links.new(multiply2.outputs[0], mix_shader.inputs[0])

	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], mix1.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[1], multiply2.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[2], mix1.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[3], emission.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[4], mix1.inputs[0])
	nodegroup.node_tree.links.new(group_input.outputs[5], multiply1.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[6], multiply2.inputs[2])

	material.node_tree.links.new(uv1.outputs[0], tex1.inputs[0])
	material.node_tree.links.new(uv1.outputs[0], tex2.inputs[0])
	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs[0])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[1])
	material.node_tree.links.new(tex2.outputs[0], nodegroup.inputs[2])

	material.node_tree.links.new(vcol.outputs[0], nodegroup.inputs[5])
	material.node_tree.links.new(vcol.outputs[1], nodegroup.inputs[6])

	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])

	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)
		image_name2 = xfbin_mat.texture_groups[0].textures[1].name
		tex2.image = bpy.data.images.get(image_name2)

	return material

def _05_F00D(self, meshmat, xfbin_mat, matname, nodegrp = '05F00D'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True
	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (721, 611)
	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Nodes
	normal = nodegroup.node_tree.nodes.new('ShaderNodeNormal')
	normal.location = (-696, 350)

	diffuse_bsdf = nodegroup.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
	diffuse_bsdf.location = (-519, 304)

	shader_rgb = nodegroup.node_tree.nodes.new('ShaderNodeShaderToRGB')
	shader_rgb.location = (-327, 305)

	math_greater = nodegroup.node_tree.nodes.new('ShaderNodeMath')
	math_greater.location = (-163, 320)
	math_greater.operation = 'GREATER_THAN'
	math_greater.inputs[1].default_value = 0.06

	lighten = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	lighten.location = (47, 300)
	lighten.blend_type = 'LIGHTEN'
	lighten.inputs[0].default_value = 1
	lighten.inputs[2].default_value = (0.2,0.2,0.2,1)

	multiply1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply1.location = (256, 131)
	multiply1.blend_type = 'MULTIPLY'
	multiply1.inputs[0].default_value = 1

	multiply2 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply2.location = (476, 81)
	multiply2.blend_type = 'MULTIPLY'
	multiply2.inputs[0].default_value = 1

	multiply3 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply3.location = (476, 81)
	multiply3.blend_type = 'MULTIPLY'
	multiply3.inputs[0].default_value = 1

	multiply4 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply4.location = (476, 81)
	multiply4.blend_type = 'MULTIPLY'
	multiply4.inputs[0].default_value = 1

	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')
	transparent.location = (264, -261)

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')
	mix_shader.location = (696, -113)

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-56, -112)
	nodegroup.inputs.new('NodeSocketColor','Diffuse Texture')
	nodegroup.inputs.new('NodeSocketColor','Shadow Texture')
	nodegroup.inputs.new('NodeSocketColor','Alpha')
	nodegroup.inputs.new('NodeSocketColor','Vertex Colors')
	nodegroup.inputs.new('NodeSocketColor','Vertex Alpha')

	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (886, 4)
	nodegroup.outputs.new('NodeSocketShader','Out')

	uv1 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv1.location = (-84, -552)
	uv1.uv_map = 'UV_0'

	uv2 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv2.location = (-78, -308)
	uv2.uv_map = 'UV_1'

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (174, 720)
	tex1.name = 'Diffuse'

	tex2 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex2.location = (178, 420)
	tex2.name = 'Shadow'

	vcol = material.node_tree.nodes.new('ShaderNodeVertexColor')


	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (1091, 520)

	#Link nodes
	nodegroup.node_tree.links.new(normal.outputs[0], diffuse_bsdf.inputs[2])

	nodegroup.node_tree.links.new(diffuse_bsdf.outputs['BSDF'], shader_rgb.inputs['Shader'])

	nodegroup.node_tree.links.new(shader_rgb.outputs['Color'], math_greater.inputs[0])

	nodegroup.node_tree.links.new(math_greater.outputs[0], lighten.inputs[1])

	nodegroup.node_tree.links.new(lighten.outputs[0], multiply1.inputs[1])

	nodegroup.node_tree.links.new(multiply1.outputs[0], multiply2.inputs[1])

	nodegroup.node_tree.links.new(multiply2.outputs[0], multiply3.inputs[1])

	nodegroup.node_tree.links.new(multiply3.outputs[0], mix_shader.inputs[2])

	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], multiply1.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[1], multiply2.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[2], multiply4.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[3], multiply3.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[4], multiply4.inputs[2])
	nodegroup.node_tree.links.new(multiply4.outputs[0], mix_shader.inputs[0])



	material.node_tree.links.new(uv1.outputs[0], tex1.inputs[0])
	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs[0])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[2])

	material.node_tree.links.new(uv2.outputs[0], tex2.inputs[0])
	material.node_tree.links.new(tex2.outputs[0], nodegroup.inputs[1])

	material.node_tree.links.new(vcol.outputs[0], nodegroup.inputs[3])
	material.node_tree.links.new(vcol.outputs[1], nodegroup.inputs[4])



	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])

	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)
		image_name2 = xfbin_mat.texture_groups[0].textures[1].name
		tex2.image = bpy.data.images.get(image_name2)

	return material

def _07_F00D(self, meshmat, xfbin_mat, matname, nodegrp = '07F00D'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True
	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (721, 611)
	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Nodes
	normal = nodegroup.node_tree.nodes.new('ShaderNodeNormal')
	normal.location = (-696, 350)

	diffuse_bsdf = nodegroup.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
	diffuse_bsdf.location = (-519, 304)

	shader_rgb = nodegroup.node_tree.nodes.new('ShaderNodeShaderToRGB')
	shader_rgb.location = (-327, 305)

	math_greater = nodegroup.node_tree.nodes.new('ShaderNodeMath')
	math_greater.location = (-163, 320)
	math_greater.operation = 'GREATER_THAN'
	math_greater.inputs[1].default_value = 0.00

	lighten = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	lighten.location = (47, 300)
	lighten.blend_type = 'LIGHTEN'
	lighten.inputs[0].default_value = 1
	lighten.inputs[2].default_value = (0.2,0.2,0.2,1)

	multiply1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply1.location = (256, 131)
	multiply1.blend_type = 'MULTIPLY'
	multiply1.inputs[0].default_value = 1

	add1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	add1.location = (256, 131)
	add1.blend_type = 'ADD'
	add1.inputs[0].default_value = 1

	multiply2 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply2.location = (476, 81)
	multiply2.blend_type = 'MULTIPLY'
	multiply2.inputs[0].default_value = 1

	multiply3 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply3.location = (476, 81)
	multiply3.blend_type = 'MULTIPLY'
	multiply3.inputs[0].default_value = 1

	multiply4 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply4.location = (476, 81)
	multiply4.blend_type = 'MULTIPLY'
	multiply4.inputs[0].default_value = 1

	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')
	transparent.location = (264, -261)

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')
	mix_shader.location = (696, -113)

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-56, -112)
	nodegroup.inputs.new('NodeSocketColor','Diffuse Texture')
	nodegroup.inputs.new('NodeSocketColor','Alpha 1')
	nodegroup.inputs.new('NodeSocketColor','Diffuse Texture')
	nodegroup.inputs.new('NodeSocketColor','Alpha 2')
	nodegroup.inputs.new('NodeSocketColor','Shadow Texture')
	nodegroup.inputs.new('NodeSocketColor','Vertex Colors')
	nodegroup.inputs.new('NodeSocketColor','Vertex Alpha')

	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (886, 4)
	nodegroup.outputs.new('NodeSocketShader','Out')

	uv1 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv1.location = (-84, -552)
	uv1.uv_map = 'UV_0'

	uv2 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv2.location = (-78, -308)
	uv2.uv_map = 'UV_1'

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (174, 720)
	tex1.name = 'Diffuse 1'

	tex2 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex2.location = (178, 420)
	tex2.name = 'Diffuse 2'

	tex3 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex3.location = (178, 420)
	tex3.name = 'Shadoow'

	vcol = material.node_tree.nodes.new('ShaderNodeVertexColor')

	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (1091, 520)

	#Link nodes
	nodegroup.node_tree.links.new(normal.outputs[0], diffuse_bsdf.inputs[2])

	nodegroup.node_tree.links.new(diffuse_bsdf.outputs['BSDF'], shader_rgb.inputs['Shader'])

	nodegroup.node_tree.links.new(shader_rgb.outputs['Color'], math_greater.inputs[0])

	nodegroup.node_tree.links.new(math_greater.outputs[0], lighten.inputs[1])

	nodegroup.node_tree.links.new(lighten.outputs[0], multiply1.inputs[1])

	nodegroup.node_tree.links.new(multiply1.outputs[0], add1.inputs[1])

	nodegroup.node_tree.links.new(add1.outputs[0], multiply2.inputs[1])

	nodegroup.node_tree.links.new(multiply2.outputs[0], multiply3.inputs[1])

	nodegroup.node_tree.links.new(multiply3.outputs[0], mix_shader.inputs[2])

	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(multiply4.outputs[0], mix_shader.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], multiply1.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[1], multiply4.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[2], add1.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[3], add1.inputs[0])
	nodegroup.node_tree.links.new(group_input.outputs[4], multiply2.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[5], multiply3.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[6], multiply4.inputs[2])

	material.node_tree.links.new(uv1.outputs[0], tex1.inputs[0])
	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs[0])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[1])
	material.node_tree.links.new(tex2.outputs[0], nodegroup.inputs[2])
	material.node_tree.links.new(tex2.outputs[1], nodegroup.inputs[3])

	material.node_tree.links.new(uv2.outputs[0], tex3.inputs[0])
	material.node_tree.links.new(tex3.outputs[0], nodegroup.inputs[4])

	material.node_tree.links.new(vcol.outputs[0], nodegroup.inputs[5])
	material.node_tree.links.new(vcol.outputs[1], nodegroup.inputs[6])


	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])

	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)
		image_name2 = xfbin_mat.texture_groups[0].textures[1].name
		tex2.image = bpy.data.images.get(image_name2)
		image_name3 = xfbin_mat.texture_groups[0].textures[2].name
		tex3.image = bpy.data.images.get(image_name3)

	return material

def _05_F002(self, meshmat,  xfbin_mat, matname, nodegrp = '05F002'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True
	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (721, 611)
	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Nodes

	multiply1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply1.location = (256, 131)
	multiply1.blend_type = 'MULTIPLY'
	multiply1.inputs[0].default_value = 1

	multiply2 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply2.location = (256, 131)
	multiply2.blend_type = 'MULTIPLY'
	multiply2.inputs[0].default_value = 1


	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')
	transparent.location = (264, -261)

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')
	mix_shader.location = (696, -113)

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-56, -112)
	nodegroup.inputs.new('NodeSocketColor','Diffuse Texture')
	nodegroup.inputs.new('NodeSocketColor','Alpha')
	nodegroup.inputs.new('NodeSocketColor','Vertex Colors')
	nodegroup.inputs.new('NodeSocketColor','Vertex Alpha')

	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (886, 4)
	nodegroup.outputs.new('NodeSocketShader','Out')

	vcol = material.node_tree.nodes.new('ShaderNodeVertexColor')

	uv1 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv1.location = (-84, -552)
	uv1.uv_map = 'UV_0'

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (174, 720)
	tex1.name = 'Diffuse'

	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (1091, 520)

	#Link nodes
	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], multiply1.inputs[1])

	nodegroup.node_tree.links.new(group_input.outputs[1], multiply2.inputs[1])

	nodegroup.node_tree.links.new(group_input.outputs[2], multiply1.inputs[2])

	nodegroup.node_tree.links.new(group_input.outputs[3], multiply2.inputs[2])

	nodegroup.node_tree.links.new(multiply1.outputs[0], mix_shader.inputs[2])

	nodegroup.node_tree.links.new(multiply2.outputs[0], mix_shader.inputs[0])

	material.node_tree.links.new(vcol.outputs[0], nodegroup.inputs[2])
	material.node_tree.links.new(vcol.outputs[1], nodegroup.inputs[3])

	material.node_tree.links.new(uv1.outputs[0], tex1.inputs[0])
	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs[0])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[1])

	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])

	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)

	return material

def _07_F002(self, meshmat,  xfbin_mat, matname, nodegrp = '07F002'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True
	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (721, 611)
	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Nodes

	multiply1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply1.location = (256, 131)
	multiply1.blend_type = 'MULTIPLY'
	multiply1.inputs[0].default_value = 1

	multiply2 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply2.location = (256, 131)
	multiply2.blend_type = 'MULTIPLY'
	multiply2.inputs[0].default_value = 1


	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')
	transparent.location = (264, -261)

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')
	mix_shader.location = (696, -113)

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-56, -112)
	nodegroup.inputs.new('NodeSocketColor','Diffuse Texture')
	nodegroup.inputs.new('NodeSocketColor','Shadow Texture')
	nodegroup.inputs.new('NodeSocketColor','Alpha')
	nodegroup.inputs.new('NodeSocketColor','Tweak Colors')
	material.node_tree.nodes[nodegrp].inputs['Tweak Colors'].default_value = (1,1,1,1)

	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (886, 4)
	nodegroup.outputs.new('NodeSocketShader','Out')

	uv1 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv1.location = (-84, -552)
	uv1.uv_map = 'UV_0'

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (174, 720)
	tex1.name = 'Diffuse'

	uv2 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv2.location = (-84, -552)
	uv2.uv_map = 'UV_1'

	tex2 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex2.location = (174, 720)
	tex2.name = 'Diffuse'


	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (1091, 520)

	#Link nodes
	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], multiply1.inputs[1])

	nodegroup.node_tree.links.new(group_input.outputs[1], multiply1.inputs[2])

	nodegroup.node_tree.links.new(group_input.outputs[2], mix_shader.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[3], multiply2.inputs[2])

	nodegroup.node_tree.links.new(multiply1.outputs[0], multiply2.inputs[1])

	nodegroup.node_tree.links.new(multiply2.outputs[0], mix_shader.inputs[2])

	material.node_tree.links.new(uv1.outputs[0], tex1.inputs[0])
	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs[0])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[2])

	material.node_tree.links.new(uv2.outputs[0], tex2.inputs[0])
	material.node_tree.links.new(tex2.outputs[0], nodegroup.inputs[1])

	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])

	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)
		image_name = xfbin_mat.texture_groups[0].textures[1].name
		tex2.image = bpy.data.images.get(image_name)

	return material


def _07_F010(self, meshmat,  xfbin_mat, matname, nodegrp = '07F020'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True
	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (721, 611)
	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Nodes
	normal = nodegroup.node_tree.nodes.new('ShaderNodeNormal')
	normal.location = (-796, -394)

	diffuse_bsdf = nodegroup.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
	diffuse_bsdf.location = (-619, -440)

	shader_rgb = nodegroup.node_tree.nodes.new('ShaderNodeShaderToRGB')
	shader_rgb.location = (-427, -439)

	math_greater = nodegroup.node_tree.nodes.new('ShaderNodeMath')
	math_greater.location = (-263, -424)
	math_greater.operation = 'GREATER_THAN'
	math_greater.inputs[1].default_value = 0.06

	lighten = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	lighten.location = (-66, -421)
	lighten.blend_type = 'LIGHTEN'
	lighten.inputs[0].default_value = 1
	lighten.inputs[2].default_value = (0.2,0.2,0.2,1)

	multiply1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply1.location = (156, -397)
	multiply1.blend_type = 'MULTIPLY'
	multiply1.inputs[0].default_value = 1

	mix1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	mix1.location = (404, -321)
	mix1.blend_type = 'MIX'

	multiply2 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply2.location = (647, -235)
	multiply2.blend_type = 'MULTIPLY'
	multiply2.inputs[0].default_value = 1

	multiply3 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	multiply3.location = (867, -175)
	multiply3.blend_type = 'MULTIPLY'
	multiply3.inputs[0].default_value = 1

	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')
	transparent.location = (984, -449)

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')
	mix_shader.location = (1121, -151)

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-91, -133)
	nodegroup.inputs.new('NodeSocketColor','Texture 1')
	nodegroup.inputs.new('NodeSocketColor','Alpha')
	nodegroup.inputs.new('NodeSocketColor','Texture 2')
	nodegroup.inputs.new('NodeSocketColor','Mask Texture')
	nodegroup.inputs.new('NodeSocketColor','Shadow Texture')
	nodegroup.inputs.new('NodeSocketColor','Vertex Colors')
	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (1341, -137)
	nodegroup.outputs.new('NodeSocketShader','Out')

	uv1 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv1.location = (-1806, 328)
	uv1.uv_map = 'UV_0'

	uv2 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv2.location = (-1908, -197)
	uv2.uv_map = 'UV_1'

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (-1390, 545)
	tex1.name = 'Diffuse1'

	tex2 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex2.location = (-1390, 286)
	tex2.name = 'Diffuse2'

	tex3 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex3.location = (-1390, 24)
	tex3.name = 'Mask'

	tex4 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex4.location = (-1390, -241)
	tex4.name = 'Shadow'

	vcol = material.node_tree.nodes.new('ShaderNodeVertexColor')
	vcol.location = (-1349, -521)

	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (1091, 520)

	#Link nodes
	nodegroup.node_tree.links.new(normal.outputs[0], diffuse_bsdf.inputs[2])

	nodegroup.node_tree.links.new(diffuse_bsdf.outputs['BSDF'], shader_rgb.inputs['Shader'])

	nodegroup.node_tree.links.new(shader_rgb.outputs['Color'], math_greater.inputs[0])

	nodegroup.node_tree.links.new(math_greater.outputs[0], lighten.inputs[1])

	nodegroup.node_tree.links.new(lighten.outputs[0], multiply1.inputs[1])

	nodegroup.node_tree.links.new(multiply1.outputs[0], mix1.inputs[1])

	nodegroup.node_tree.links.new(mix1.outputs[0], multiply2.inputs[1])

	nodegroup.node_tree.links.new(multiply2.outputs[0], multiply3.inputs[1])

	nodegroup.node_tree.links.new(multiply3.outputs[0], mix_shader.inputs[2])

	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], multiply1.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[1], mix_shader.inputs[0])
	nodegroup.node_tree.links.new(group_input.outputs[2], mix1.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[3], mix1.inputs[0])
	nodegroup.node_tree.links.new(group_input.outputs[4], multiply2.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[5], multiply3.inputs[2])

	material.node_tree.links.new(uv1.outputs[0], tex1.inputs[0])
	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs[0])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[1])

	material.node_tree.links.new(uv2.outputs[0], tex2.inputs[0])
	material.node_tree.links.new(uv2.outputs[0], tex3.inputs[0])
	material.node_tree.links.new(uv2.outputs[0], tex4.inputs[0])
	material.node_tree.links.new(tex2.outputs[0], nodegroup.inputs[2])
	material.node_tree.links.new(tex3.outputs[0], nodegroup.inputs[3])
	material.node_tree.links.new(tex4.outputs[0], nodegroup.inputs[4])
	material.node_tree.links.new(vcol.outputs[0], nodegroup.inputs[5])

	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])

	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)
		image_name2 = xfbin_mat.texture_groups[0].textures[1].name
		tex2.image = bpy.data.images.get(image_name2)
		image_name3 = xfbin_mat.texture_groups[0].textures[3].name
		tex3.image = bpy.data.images.get(image_name3)
		image_name4 = xfbin_mat.texture_groups[0].textures[2].name
		tex4.image = bpy.data.images.get(image_name4)

	return material

def _01_F00F(self, meshmat, xfbin_mat, matname, nodegrp = '01F00F'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True

	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (226, 326)

	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Le Shader
	fresnel = nodegroup.node_tree.nodes.new('ShaderNodeFresnel')
	fresnel.location = (-280, -346)
	fresnel.inputs[0].default_value = 0.9

	mix1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	mix1.inputs[0].default_value = 0
	mix1.location = (-280, -142)

	mix2 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	mix2.location = (162, -61)

	emission = nodegroup.node_tree.nodes.new('ShaderNodeEmission')
	emission.inputs[1].default_value = 1.35
	emission.location = (399, -24)

	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')
	transparent.location = (326, 181)

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')
	mix_shader.location = (619, 96)

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-668, 8)
	nodegroup.inputs.new('NodeSocketColor','Diffuse Texture')
	nodegroup.inputs.new('NodeSocketColor','Diffuse Alpha')
	nodegroup.inputs.new('NodeSocketColor','Falloff Texture')
	nodegroup.inputs.new('NodeSocketColor','Falloff Alpha')
	nodegroup.inputs.new('NodeSocketFloat','Rim Light')
	nodegroup.inputs[4].default_value = 0.9
	nodegroup.inputs.new('NodeSocketFloat','Light Strength')
	nodegroup.inputs[5].default_value = 1.35


	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (862, 84)
	nodegroup.outputs.new('NodeSocketShader','Out')

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (-394, 443)
	tex1.name = 'Diffuse Texture'

	tex2 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex2.location = (-399, 141)
	tex2.name = 'Falloff Texture'

	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (772, 331)

	#Link nodes
	nodegroup.node_tree.links.new(mix1.outputs[0], mix2.inputs[2])

	nodegroup.node_tree.links.new(fresnel.outputs[0], mix2.inputs[0])

	nodegroup.node_tree.links.new(mix2.outputs[0], emission.inputs[0])

	nodegroup.node_tree.links.new(emission.outputs[0], mix_shader.inputs[2])

	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], mix2.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[1], mix_shader.inputs[0])
	nodegroup.node_tree.links.new(group_input.outputs[2], mix1.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[3], mix1.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[4], fresnel.inputs[0])
	nodegroup.node_tree.links.new(group_input.outputs[5], emission.inputs[1])

	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs[0])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[1])

	material.node_tree.links.new(tex2.outputs[0], nodegroup.inputs[2])
	material.node_tree.links.new(tex2.outputs[1], nodegroup.inputs[3])

	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])
	
	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)
		image_name2 = xfbin_mat.texture_groups[0].textures[1].name
		tex2.image = bpy.data.images.get(image_name2)

	return material

def _03_F00F(self, meshmat, xfbin_mat, matname, nodegrp = '03F00F'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True

	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (226, 326)

	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Le Shader
	fresnel = nodegroup.node_tree.nodes.new('ShaderNodeFresnel')
	fresnel.location = (-280, -346)
	fresnel.inputs[0].default_value = 0.9

	mix1 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	mix1.location = (-280, -142)

	mix2 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	mix2.inputs[0].default_value = 0
	mix2.location = (162, -61)

	mix3 = nodegroup.node_tree.nodes.new('ShaderNodeMixRGB')
	mix3.location = (162, -61)

	emission = nodegroup.node_tree.nodes.new('ShaderNodeEmission')
	emission.inputs[1].default_value = 1.35
	emission.location = (399, -24)

	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')
	transparent.location = (326, 181)

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')
	mix_shader.location = (619, 96)

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-668, 8)
	nodegroup.inputs.new('NodeSocketColor','Diffuse Texture')
	nodegroup.inputs.new('NodeSocketColor','Diffuse Alpha')
	nodegroup.inputs.new('NodeSocketColor','Diffuse2 Texture')
	nodegroup.inputs.new('NodeSocketColor','Diffuse2 Alpha')
	nodegroup.inputs.new('NodeSocketColor','Falloff Texture')
	nodegroup.inputs.new('NodeSocketColor','Falloff Alpha')
	nodegroup.inputs.new('NodeSocketFloat','Rim Light')
	nodegroup.inputs[6].default_value = 0.9
	nodegroup.inputs.new('NodeSocketFloat','Light Strength')
	nodegroup.inputs[7].default_value = 1.35


	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (862, 84)
	nodegroup.outputs.new('NodeSocketShader','Out')

	uv1 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv1.location = (-84, -552)
	uv1.uv_map = 'UV_0'

	uv2 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv2.location = (-84, -552)
	uv2.uv_map = 'UV_1'

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (-394, 443)
	tex1.name = 'Diffuse Texture'

	tex2 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex2.location = (-399, 141)
	tex2.name = 'Diffuse2 Texture'

	tex3 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex3.location = (-399, 141)
	tex3.name = 'Falloff Texture'

	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (772, 331)

    #Link nodes
	nodegroup.node_tree.links.new(mix1.outputs[0], mix3.inputs[1])

	nodegroup.node_tree.links.new(mix2.outputs[0], mix3.inputs[2])

	nodegroup.node_tree.links.new(fresnel.outputs[0], mix3.inputs[0])

	nodegroup.node_tree.links.new(mix3.outputs[0], emission.inputs[0])

	nodegroup.node_tree.links.new(emission.outputs[0], mix_shader.inputs[2])

	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], mix1.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[1], mix_shader.inputs[0])
	nodegroup.node_tree.links.new(group_input.outputs[2], mix1.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[3], mix1.inputs[0])
	nodegroup.node_tree.links.new(group_input.outputs[4], mix2.inputs[1])
	nodegroup.node_tree.links.new(group_input.outputs[5], mix2.inputs[2])
	nodegroup.node_tree.links.new(group_input.outputs[6], fresnel.inputs[0])
	nodegroup.node_tree.links.new(group_input.outputs[7], emission.inputs[1])

	material.node_tree.links.new(uv1.outputs[0], tex1.inputs[0])

	material.node_tree.links.new(uv2.outputs[0], tex2.inputs[0])

	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs[0])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[1])

	material.node_tree.links.new(tex2.outputs[0], nodegroup.inputs[2])
	material.node_tree.links.new(tex2.outputs[1], nodegroup.inputs[3])

	material.node_tree.links.new(tex3.outputs[0], nodegroup.inputs[4])
	material.node_tree.links.new(tex3.outputs[1], nodegroup.inputs[5])

	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])

	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)
		image_name2 = xfbin_mat.texture_groups[0].textures[1].name
		tex2.image = bpy.data.images.get(image_name2)
		image_name3 = xfbin_mat.texture_groups[0].textures[2].name
		tex3.image = bpy.data.images.get(image_name3)
	
	return material

def E002(self, meshmat, xfbin_mat, matname, nodegrp = 'E002'):

	material = bpy.data.materials.new(matname)
	material.use_nodes = True
	# Alpha Mode
	if meshmat.source_factor == 2:
		material.blend_method = 'CLIP'
	elif meshmat.source_factor == 1 or meshmat.source_factor == 5:
		material.blend_method = 'BLEND'
	material.shadow_method = 'NONE'
	
	# Culling Mode
	if meshmat.cull_mode == 1028 or meshmat.cull_mode == 1029:
		material.use_backface_culling = True
	else:
		material.use_backface_culling = False

	#Remove Unnecessary nodes
	material.node_tree.nodes.remove(material.node_tree.nodes['Principled BSDF'])
	material.node_tree.nodes.remove(material.node_tree.nodes['Material Output'])

	#remove node groups with the same name to prevent issues with min and max values of some nodes
	if bpy.data.node_groups.get(nodegrp):
		bpy.data.node_groups.remove(bpy.data.node_groups.get(nodegrp))

	#Create a new node tree to be used later
	nodetree = bpy.data.node_groups.new(nodegrp, 'ShaderNodeTree')

	#Create a node group to organize nodes and inputs
	nodegroup = material.node_tree.nodes.new('ShaderNodeGroup')
	nodegroup.name = nodegrp
	nodegroup.location = (721, 611)
	#use the node tree we made earlier for our node group
	material.node_tree.nodes[nodegrp].node_tree = nodetree

	#Nodes
	transparent = nodegroup.node_tree.nodes.new('ShaderNodeBsdfTransparent')

	mix_shader = nodegroup.node_tree.nodes.new('ShaderNodeMixShader')

	group_input = nodegroup.node_tree.nodes.new('NodeGroupInput')
	group_input.location = (-56, -112)
	nodegroup.inputs.new('NodeSocketColor','Texture')
	nodegroup.inputs.new('NodeSocketColor','Alpha')

	group_output = nodegroup.node_tree.nodes.new('NodeGroupOutput')
	group_output.location = (886, 4)
	nodegroup.outputs.new('NodeSocketShader','Out')

	uv1 = material.node_tree.nodes.new('ShaderNodeUVMap')
	uv1.location = (-84, -552)
	uv1.uv_map = 'UV_0'

	tex1 = material.node_tree.nodes.new('ShaderNodeTexImage')
	tex1.location = (174, 720)
	tex1.name = 'Diffuse'

	output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
	output.location = (1091, 520)

	#Link nodes
	nodegroup.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])

	nodegroup.node_tree.links.new(mix_shader.outputs[0], group_output.inputs[0])

	nodegroup.node_tree.links.new(group_input.outputs[0], mix_shader.inputs[2])

	nodegroup.node_tree.links.new(group_input.outputs[1], mix_shader.inputs[0])

	material.node_tree.links.new(uv1.outputs[0], tex1.inputs[0])
	material.node_tree.links.new(tex1.outputs[0], nodegroup.inputs[0])
	material.node_tree.links.new(tex1.outputs[1], nodegroup.inputs[1])

	material.node_tree.links.new(nodegroup.outputs[0], output.inputs[0])

	if xfbin_mat.texture_groups and xfbin_mat.texture_groups[0].textures:
		image_name = xfbin_mat.texture_groups[0].textures[0].name
		tex1.image = bpy.data.images.get(image_name)

	return material

