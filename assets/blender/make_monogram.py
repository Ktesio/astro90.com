"""The selected Astro90 a as an original extruded studio object."""
from pathlib import Path
from math import radians
import json
import bpy

ROOT=Path(__file__).resolve().parents[2]
data=json.loads((ROOT/'assets/brand/monogram.json').read_text())
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.samples=48
scene.cycles.use_denoising=True
scene.render.resolution_x=1500
scene.render.resolution_y=1500
scene.render.resolution_percentage=100
scene.render.film_transparent=True
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGBA'
scene.view_settings.view_transform='AgX'
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.1,.12,.18,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.35

def linear(x): return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
def material(name,hex_value,metal,rough):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=tuple(linear(int(hex_value[i:i+2],16)/255) for i in (1,3,5))+(1,)
    p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    return m
gold=material('Saffron satin alloy','#F4C84C',.82,.27)
navy=material('Midnight inset','#101925',.7,.28)
def letter(name,mat,depth,z,scale=1):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='2D';curve.resolution_u=2
    curve.fill_mode='BOTH';curve.extrude=depth;curve.bevel_depth=.085;curve.bevel_resolution=5
    for contour in data['contours']:
        spline=curve.splines.new('POLY');spline.points.add(len(contour)-1)
        for p,(x,y) in zip(spline.points,contour):p.co=((x/data['width']-.5)*4.6*scale,(.5-y/data['height'])*4.05*scale,0,1)
        spline.use_cyclic_u=True
    obj=bpy.data.objects.new(name,curve);bpy.context.collection.objects.link(obj)
    obj.location.z=z;obj.data.materials.append(mat)
    return obj
letter('Astro90 a / saffron face',gold,.22,.15)
letter('Astro90 a / navy core',navy,.30,-.30,.98)
bpy.ops.object.camera_add(location=(0,-4.8,11))
scene.camera=bpy.context.object
scene.camera.rotation_euler=(-scene.camera.location).to_track_quat('-Z','Y').to_euler()
scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=7.5
for loc,power,size,tint in [((-4,-2,8),1600,6,(1,.93,.76)),((5,3,6),1900,4,(.61,.75,1)),((1,-6,-1),1100,3,(1,.79,.4)),((-4,4,2),1200,3,(1,1,1))]:
    bpy.ops.object.light_add(type='AREA',location=loc)
    light=bpy.context.object;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.data.color=tint
    light.rotation_euler=(-light.location).to_track_quat('-Z','Y').to_euler()
scene.render.filepath='//../renders/monogram.png'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/blender/astro90-monogram.blend'))
bpy.ops.render.render(write_still=True)

# Sharing card: the same letter and the selected wordmark, without orbital art.
scene.render.resolution_x=1200;scene.render.resolution_y=630
scene.render.film_transparent=False
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.003,.005,.009,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=1
scene.camera.location=(0,0,16);scene.camera.rotation_euler=(0,0,0)
scene.camera.data.ortho_scale=12.5
for obj in [o for o in scene.objects if o.type=='CURVE']:
    obj.location.x=3.25;obj.rotation_euler=(radians(15),radians(-22),radians(-9))
    obj.scale=(.9,.9,.9)
mesh=bpy.data.meshes.new('Selected wordmark quad')
mesh.from_pydata([(-5.15,.1,1),(-.15,.1,1),(-.15,1.024,1),(-5.15,1.024,1)],[],[(0,1,2,3)])
mesh.update();uv=mesh.uv_layers.new()
for loop,coord in zip(uv.data,[(108/1536,1-533/1024),(1428/1536,1-533/1024),(1428/1536,1-289/1024),(108/1536,1-289/1024)]):loop.uv=coord
wordmark=bpy.data.objects.new('Selected studio wordmark',mesh);bpy.context.collection.objects.link(wordmark)
mat=bpy.data.materials.new('Flat saffron wordmark');mat.use_nodes=True
nodes=mat.node_tree.nodes;nodes.clear()
output=nodes.new('ShaderNodeOutputMaterial');mix=nodes.new('ShaderNodeMixShader')
transparent=nodes.new('ShaderNodeBsdfTransparent');emission=nodes.new('ShaderNodeEmission')
emission.inputs[0].default_value=tuple(linear(v/255) for v in (244,200,76))+(1,)
texture=nodes.new('ShaderNodeTexImage');texture.image=bpy.data.images.load(str(ROOT/'output/branding/logo-options-v1/04-wordmark.png'))
links=mat.node_tree.links;links.new(texture.outputs['Alpha'],mix.inputs[0]);links.new(transparent.outputs[0],mix.inputs[1]);links.new(emission.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],output.inputs[0]);mesh.materials.append(mat)
text_curve=bpy.data.curves.new('Studio description','FONT');text_curve.body='Games. Agentic AI. Open source.';text_curve.size=.22
text_curve.font=bpy.data.fonts.load(str(ROOT/'assets/source/fonts/Manrope.ttf'))
text_curve.space_character=1.1
description=bpy.data.objects.new('Studio description',text_curve);bpy.context.collection.objects.link(description);description.location=(-5.1,-.48,1)
text_mat=bpy.data.materials.new('Slate text');text_mat.use_nodes=True
text_mat.node_tree.nodes.clear();shader=text_mat.node_tree.nodes.new('ShaderNodeEmission');shader.inputs[0].default_value=(.4,.45,.53,1)
output=text_mat.node_tree.nodes.new('ShaderNodeOutputMaterial');text_mat.node_tree.links.new(shader.outputs[0],output.inputs[0])
text_curve.materials.append(text_mat)
scene.render.filepath=str(ROOT/'static/media/social-cover.png')
bpy.ops.render.render(write_still=True)
