"""Blender (bpy) test: a 3D paper-cut Mithila diorama with extruded type, Cycles CPU. Usage: python blender_test.py out.png [engine] [samples] [res_pct]"""
import sys, time, math, bpy

out = sys.argv[1]; engine = sys.argv[2] if len(sys.argv) > 2 else "CYCLES"
samples = int(sys.argv[3]) if len(sys.argv) > 3 else 48; pct = int(sys.argv[4]) if len(sys.argv) > 4 else 50
import os
FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts", "AnekLatin.ttf")

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, pct

def mat(name, rgb, rough=0.8, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    return m

def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)

neel, chandan, haldi, sindoor, mor, kajal = (srgb(x) for x in ("#1A1D47", "#F4EADB", "#F2B33D", "#D63E2A", "#137C77", "#100E17"))

# World: dark indigo
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (*neel, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.15

# Paper layers: cut-out planes (arches) at increasing depth, like a layered paper diorama
def paper_layer(z, y, color, hole_r, name):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y, z))
    p = bpy.context.object; p.scale = (8, 14, 1); p.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    bpy.ops.mesh.primitive_cylinder_add(radius=hole_r, depth=2, location=(0, y, z + 0.6), rotation=(math.radians(90), 0, 0), vertices=96)
    hole = bpy.context.object
    mod = p.modifiers.new("cut", "BOOLEAN"); mod.object = hole; mod.operation = "DIFFERENCE"
    bpy.context.view_layer.objects.active = p; bpy.ops.object.modifier_apply(modifier="cut")
    bpy.data.objects.remove(hole)
    sol = p.modifiers.new("thick", "SOLIDIFY"); sol.thickness = 0.04
    p.data.materials.clear(); p.data.materials.append(mat(name, color)); return p

paper_layer(0, 0.0, neel, 2.6, "l1")
paper_layer(0, 1.2, sindoor, 2.0, "l2")
paper_layer(0, 2.4, haldi, 1.7, "l3")
paper_layer(0, 3.6, mor, 1.4, "l4")
# back wall
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 5.0, 0), rotation=(math.radians(90), 0, 0))
bpy.context.object.data.materials.append(mat("back", chandan))

# Extruded 3D type
bpy.ops.object.text_add(location=(0, -1.6, -2.9), rotation=(math.radians(90), 0, 0))
t = bpy.context.object; t.data.body = "SUTRAVERSE"
try:
    t.data.font = bpy.data.fonts.load(FONT)
except Exception as e:
    print("font load failed", e)
t.data.align_x = "CENTER"; t.data.size = 0.95; t.data.extrude = 0.12; t.data.bevel_depth = 0.015
t.data.materials.append(mat("type", haldi, rough=0.35))

# Light: warm key from left above, cool rim
bpy.ops.object.light_add(type="AREA", location=(-4, -6, 6)); k = bpy.context.object; k.data.energy = 700; k.data.size = 4; k.data.color = (1, .85, .65)
k.rotation_euler = (math.radians(55), 0, math.radians(-35))
bpy.ops.object.light_add(type="SPOT", location=(3, 8, 3)); r = bpy.context.object; r.data.energy = 400; r.data.color = (.5, .8, 1)
r.rotation_euler = (math.radians(-70), 0, math.radians(160))

# Camera
bpy.ops.object.camera_add(location=(0, -13, 0.3), rotation=(math.radians(90), 0, 0))
cam = bpy.context.object; sc.camera = cam; cam.data.lens = 40
cam.data.dof.use_dof = True; cam.data.dof.focus_distance = 11.4; cam.data.dof.aperture_fstop = 2.8

if engine == "CYCLES":
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    try: sc.cycles.denoiser = "OPENIMAGEDENOISE"
    except Exception: pass
else:
    sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE"
sc.view_settings.view_transform = "AgX"
sc.render.filepath = out
t0 = time.time(); bpy.ops.render.render(write_still=True); print("RENDER_SECONDS", round(time.time() - t0, 1), engine, samples, pct)
