"""Original Astro90 sculptures. Run with Blender --background --python this_file."""
from pathlib import Path
from math import radians
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'assets' / 'renders'
OUT.mkdir(parents=True, exist_ok=True)

def linear(value):
    return value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4

def color(hex_value):
    return tuple(linear(int(hex_value[i:i+2], 16) / 255) for i in (1, 3, 5)) + (1,)

def material(name, hex_value, metal=.0, rough=.35, emission=.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    node = m.node_tree.nodes.get('Principled BSDF')
    node.inputs['Base Color'].default_value = color(hex_value)
    node.inputs['Metallic'].default_value = metal
    node.inputs['Roughness'].default_value = rough
    if emission:
        node.inputs['Emission Color'].default_value = color(hex_value)
        node.inputs['Emission Strength'].default_value = emission
    return m

def setup():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1680
    scene.render.resolution_y = 1540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.16,.19,.24,1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value = .5
    scene.view_settings.view_transform = 'AgX'
    bpy.ops.object.camera_add(location=(6,-10,6))
    camera = bpy.context.object
    camera.rotation_euler = (Vector((0,0,0)) - camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 8.5
    scene.camera = camera
    for name,location,energy,size,tint in [
        ('warm key',(1,-5,8),1800,5,(1,.87,.65)),
        ('cold rim',(-5,2,5),2100,4,(.44,.63,1)),
        ('softbox',(5,4,1),1600,3,(1,.92,.76)),
        ('front fill',(0,-7,-2),650,4,(.55,.68,1))]:
        bpy.ops.object.light_add(type='AREA',location=location)
        light=bpy.context.object
        light.name=name
        light.data.energy=energy
        light.data.shape='DISK'
        light.data.size=size
        light.data.color=tint
        light.rotation_euler=(-light.location).to_track_quat('-Z','Y').to_euler()
    return scene

def torus(name,radius,thickness,rotation,mat,location=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_segments=144,minor_segments=32,major_radius=radius,minor_radius=thickness,location=location,rotation=tuple(radians(n) for n in rotation))
    obj=bpy.context.object
    obj.name=name
    obj.data.materials.append(mat)
    for face in obj.data.polygons:face.use_smooth=True
    return obj

def sphere(name,location,radius,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=40,radius=radius,location=location)
    obj=bpy.context.object
    obj.name=name
    obj.data.materials.append(mat)
    for face in obj.data.polygons:face.use_smooth=True
    return obj

scene=setup()
gold=material('Saffron anodised metal','#F4C84C',.72,.24)
ink=material('Ink navy ceramic','#1E293B',.6,.21)
dark=material('Dark graphite','#101722',.65,.28)
ivory=material('Frosted ivory','#EAE8DE',.28,.29)
signal=material('Saffron light','#F4C84C',.5,.2,.4)

sphere('Core',(0,0,0),1.34,ink)
torus('Primary orbit',2.25,.19,(65,10,-40),gold)
torus('Outer orbital rail',2.93,.036,(65,10,-40),gold)
torus('Cross orbit',1.80,.10,(120,15,55),dark)
torus('Inner brass detail',1.39,.035,(120,15,55),signal)
sphere('Moon 01',(-2.18,-1.04,.75),.46,gold)
sphere('Moon 02',(1.86,1.5,-.46),.30,ivory)
sphere('Moon 03',(.32,2.32,1.08),.15,signal)
sphere('Moon 04',(-.55,-2.32,-1.40),.17,ink)
scene.render.filepath='//../renders/orbit.png'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/blender/astro90-orbit.blend'))
bpy.ops.render.render(write_still=True)

# Social card: the same authored scene in a wide, opaque composition.
scene.render.resolution_x=1200
scene.render.resolution_y=630
scene.render.film_transparent=False
scene.world.node_tree.nodes['Background'].inputs[0].default_value=color('#101722')
scene.camera.data.ortho_scale=9.0
scene.render.filepath=str(ROOT/'static/media/social-cover.png')
bpy.ops.render.render(write_still=True)
scene.render.film_transparent=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.16,.19,.24,1)

# A second composition of the same materials for the studio chapter.
for obj in list(bpy.data.objects):
    if obj.type=='MESH':bpy.data.objects.remove(obj,do_unlink=True)
for index in range(5):
    torus('Interlocking link %s'%index,1.06,.22,(index*27,32+index*13,15+index*20),gold if index%2==0 else ink,((index-2)*.57,0,(index-2)*.24))
sphere('Orbiting idea',(2.45,-.15,1.1),.31,ivory)
scene.camera.data.ortho_scale=7.4
scene.render.resolution_x=1440
scene.render.resolution_y=1000
scene.render.filepath=str(OUT/'studio-sculpture.png')
bpy.ops.render.render(write_still=True)
