"""Model and animate the Astro90 letter in Blender; render with Cycles.

Run with Blender --background --python assets/blender/build_identity.py.
Optional arguments after --: --preview or --render. The saved scene contains
all geometry, materials, lights and keyframes; no external textures are needed.
"""
from pathlib import Path
from math import radians, sin, pi
import json
import sys
import shutil
import bpy
from mathutils import Vector, kdtree

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / '.local/identity-frames'
OUTPUT.mkdir(parents=True, exist_ok=True)
DATA = json.loads((ROOT / 'assets/brand/monogram.json').read_text())
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.cycles.adaptive_threshold = .045
scene.cycles.transparent_max_bounces = 16
scene.cycles.max_bounces = 8
preferences = bpy.context.preferences.addons['cycles'].preferences
scene.cycles.device = 'CPU'
try:
    preferences.compute_device_type = 'METAL'
    preferences.get_devices()
    for device in preferences.devices:
        device.use = device.type == 'METAL'
        print('RENDER DEVICE:', device.name, device.type, device.use)
    if any(device.use and device.type == 'METAL' for device in preferences.devices):
        scene.cycles.device = 'GPU'
except Exception as error:
    print('Using CPU:', error)
scene.render.resolution_x = 960
scene.render.resolution_y = 960
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '8'
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 96
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'
scene.world.use_nodes = True
background = scene.world.node_tree.nodes['Background']
background.inputs[0].default_value = (.12, .15, .21, 1)
background.inputs[1].default_value = .32


def linear(value):
    return value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4


def alloy(name, hex_color, roughness, coat=.5, emission=0):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    links = material.node_tree.links
    output = nodes.new('ShaderNodeOutputMaterial')
    metal = nodes.new('ShaderNodeBsdfPrincipled')
    color = tuple(linear(int(hex_color[i:i + 2], 16) / 255) for i in (1, 3, 5)) + (1,)
    metal.inputs['Base Color'].default_value = color
    metal.inputs['Metallic'].default_value = 1
    metal.inputs['Roughness'].default_value = roughness
    metal.inputs['Coat Weight'].default_value = coat
    metal.inputs['Coat Roughness'].default_value = .12
    metal.inputs['Emission Color'].default_value = color
    metal.inputs['Emission Strength'].default_value = emission
    # Microscopic surface relief catches the softboxes without distorting the a.
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 160
    noise.inputs['Detail'].default_value = 2
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = .075
    bump.inputs['Distance'].default_value = .006
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], metal.inputs['Normal'])
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    mix = nodes.new('ShaderNodeMixShader')
    mix.name = 'Assembly visibility'
    links.new(transparent.outputs[0], mix.inputs[1])
    links.new(metal.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs[0])
    mix.inputs[0].default_value = 1
    return material, mix.inputs[0]


def key(socket, frame, value):
    socket.default_value = value
    socket.keyframe_insert(data_path='default_value', frame=frame)


gold, gold_visibility = alloy('Polished saffron / cast face', '#E8C15A', .18, .8)
core, core_visibility = alloy('Graphite titanium / deep core', '#536072', .22, .6)
wire, wire_visibility = alloy('Saffron construction filament', '#F4D988', .22, .5, .32)
for socket in [gold_visibility, core_visibility]:
    key(socket, 1, 0)
    key(socket, 36, 0)
    key(socket, 72, 1)
    key(socket, 96, 1)
key(wire_visibility, 1, 1)
key(wire_visibility, 59, 1)
key(wire_visibility, 82, 0)
key(wire_visibility, 96, 0)

contour = [Vector(((x / DATA['width'] - .5) * 4.6, (.5 - y / DATA['height']) * 4.05, 0)) for x, y in DATA['contours'][0]]
# Dense boundary samples give the actual front face a softly crowned profile.
boundary = []
for a, b in zip(contour, contour[1:] + contour[:1]):
    count = max(1, int((b - a).length / .018))
    boundary.extend(a.lerp(b, index / count) for index in range(count))
tree = kdtree.KDTree(len(boundary))
for index, point in enumerate(boundary):
    tree.insert(point, index)
tree.balance()
assembly = bpy.data.objects.new('ASTRO90 / fixed-scale assembly', None)
bpy.context.collection.objects.link(assembly)
assembly.rotation_euler = (radians(8), radians(-18), radians(-5))


def body(name, material, depth, z, scale=1, crown=.17):
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '2D'
    curve.fill_mode = 'BOTH'
    curve.extrude = depth
    curve.bevel_depth = .115
    curve.bevel_resolution = 8
    spline = curve.splines.new('POLY')
    spline.points.add(len(contour) - 1)
    for point, coordinate in zip(spline.points, contour):
        point.co = (*coordinate, 1)
    spline.use_cyclic_u = True
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    remesh = obj.modifiers.new('Even topology for the cast surface', 'REMESH')
    remesh.mode = 'VOXEL'
    remesh.voxel_size = .035
    remesh.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    smooth = obj.modifiers.new('Smooth the casting', 'SMOOTH')
    smooth.factor = .65
    smooth.iterations = 5
    bpy.ops.object.modifier_apply(modifier=smooth.name)
    for vertex in obj.data.vertices:
        coordinate = vertex.co
        if coordinate.z > depth * .65:
            _, _, distance = tree.find(Vector((coordinate.x, coordinate.y, 0)))
            weight = min(1, max(0, (coordinate.z - depth * .65) / .1))
            coordinate.z += crown * sin(min(distance / .8, 1) * pi / 2) * weight
    subdivision = obj.modifiers.new('Continuous surface curvature', 'SUBSURF')
    subdivision.levels = 1
    subdivision.render_levels = 1
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    obj.data.materials.append(material)
    obj.location.z = z
    obj.scale = (scale, scale, 1)
    obj.parent = assembly
    obj.select_set(False)
    return obj

body('01 / crowned saffron shell', gold, .20, .14)
body('02 / recessed titanium core', core, .25, -.28, .986, .06)

# Each physical filament draws around the exact logo path. The layers already
# occupy their final depth; neither the object nor camera changes scale.
for layer in range(8):
    curve = bpy.data.curves.new(f'Contour {layer + 1:02}', 'CURVE')
    curve.dimensions = '3D'
    curve.resolution_u = 1
    curve.bevel_depth = .012 if layer in (0, 7) else .008
    curve.bevel_resolution = 4
    spline = curve.splines.new('POLY')
    offset = (layer * 31) % len(contour)
    points = contour[offset:] + contour[:offset]
    points = points + points[:1]
    spline.points.add(len(points) - 1)
    for point, coordinate in zip(spline.points, points):
        point.co = (*coordinate, 1)
    obj = bpy.data.objects.new(f'Filament / contour {layer + 1:02}', curve)
    bpy.context.collection.objects.link(obj)
    obj.parent = assembly
    obj.location.z = .43 - layer * .14
    curve.materials.append(wire)
    curve.bevel_factor_end = 0
    curve.keyframe_insert(data_path='bevel_factor_end', frame=1 + layer * 2)
    curve.bevel_factor_end = 1
    curve.keyframe_insert(data_path='bevel_factor_end', frame=34 + layer * 2)

for index in range(0, len(boundary), 45):
    point = boundary[index]
    curve = bpy.data.curves.new(f'Depth bridge {index}', 'CURVE')
    curve.dimensions = '3D'
    curve.bevel_depth = .006
    curve.bevel_resolution = 3
    spline = curve.splines.new('POLY')
    spline.points.add(1)
    spline.points[0].co = (point.x, point.y, -.55, 1)
    spline.points[1].co = (point.x, point.y, .43, 1)
    obj = bpy.data.objects.new(f'Filament / depth bridge {index}', curve)
    bpy.context.collection.objects.link(obj)
    obj.parent = assembly
    curve.materials.append(wire)
    curve.bevel_factor_end = 0
    curve.keyframe_insert(data_path='bevel_factor_end', frame=15 + index % 9)
    curve.bevel_factor_end = 1
    curve.keyframe_insert(data_path='bevel_factor_end', frame=44 + index % 9)

bpy.ops.object.camera_add(location=(0, 0, 12))
scene.camera = bpy.context.object
scene.camera.name = 'Camera / locked orthographic framing'
scene.camera.data.type = 'ORTHO'
scene.camera.data.ortho_scale = 6.5
scene.camera.data.lens = 65
scene.camera.rotation_euler = (0, 0, 0)
for name, position, power, width, height, color in [
    ('01 / warm key softbox', (-4, 3, 6), 1050, 3, 7, (1, .95, .85)),
    ('02 / tall cool strip', (5, 1, 4), 1250, 1.1, 7, (.84, .91, 1)),
    ('03 / overhead rim', (0, 5, -1), 1500, 6, 2, (1, 1, 1)),
    ('04 / lower gold bounce', (-2, -5, 2), 600, 4, 1.5, (1, .88, .62)),
]:
    bpy.ops.object.light_add(type='AREA', location=position)
    light = bpy.context.object
    light.name = name
    light.data.energy = power
    light.data.shape = 'RECTANGLE'
    light.data.size = width
    light.data.size_y = height
    light.data.color = color
    light.rotation_euler = (-light.location).to_track_quat('-Z', 'Y').to_euler()

scene.timeline_markers.new('Trace the perimeter', frame=1)
scene.timeline_markers.new('Connect the depth', frame=24)
scene.timeline_markers.new('Form the cast surfaces', frame=40)
scene.timeline_markers.new('One finished object', frame=82)
scene.frame_set(96)
scene.render.filepath = '//../../.local/identity-frames/frame_'
# Open the native scene in a useful camera view with the whole timeline visible.
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.region_3d.view_perspective = 'CAMERA'
            area.spaces.active.shading.type = 'MATERIAL'
scene['animation_note'] = '3.2 s once on page load. Locked orthographic camera and fixed object scale. No scroll animation.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'assets/blender/astro90-identity.blend'))
if '--preview' in sys.argv:
    scene.render.resolution_percentage = 60
    scene.cycles.samples = 32
    for frame in [24, 45, 63, 96]:
        scene.frame_set(frame)
        scene.render.filepath = str(OUTPUT / f'preview_{frame:04}.png')
        bpy.ops.render.render(write_still=True)
elif '--render' in sys.argv:
    # Everything is stationary after frame 82; reuse that exact final frame.
    for frame in range(1, 83):
        scene.frame_set(frame)
        scene.render.filepath = str(OUTPUT / f'frame_{frame:04}.png')
        bpy.ops.render.render(write_still=True)
    for frame in range(83, 97):
        shutil.copy2(OUTPUT / 'frame_0082.png', OUTPUT / f'frame_{frame:04}.png')
