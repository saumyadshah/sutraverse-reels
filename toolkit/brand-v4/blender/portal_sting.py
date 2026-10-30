"""SutraVerse v4 reusable 3D asset: the Paper Portal (modern -> ancient world transition).
Concentric Mithila-pigment paper rings with hatched rims; camera dollies through the rings toward a chandan light.
Usage: python portal_sting.py OUTDIR [frames=48] [res_pct=67] [samples=16]
Render once; Reel runs reuse the frames (overlay with alpha-free plate, or crossfade at the centre light)."""
import sys, math, bpy
out = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 48
pct = int(sys.argv[3]) if len(sys.argv) > 3 else 67; spp = int(sys.argv[4]) if len(sys.argv) > 4 else 16
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, pct
sc.frame_start, sc.frame_end = 1, N; sc.render.fps = 30
def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + .055) / 1.055) ** 2.4 if x > .04045 else x / 12.92 for x in c)
def mat(name, rgb, rough=.85, emit=0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    if emit: b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    return m
cols = ["#1A1D47", "#D63E2A", "#F2B33D", "#137C77", "#EE7A2E", "#9E2348", "#F2B33D", "#1A1D47"]
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (*srgb("#100E17"), 1)
rings = []
for i, hx in enumerate(cols):
    y = i * 1.3; outer = 9.0; inner = 3.1 - i * 0.22
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y, 0)); p = bpy.context.object
    p.scale = (14, 24, 1); p.rotation_euler = (math.radians(90), 0, 0); bpy.ops.object.transform_apply(scale=True, rotation=True)
    bpy.ops.mesh.primitive_cylinder_add(radius=inner, depth=2, location=(0, y, 0), rotation=(math.radians(90), 0, 0), vertices=128)
    hole = bpy.context.object; md = p.modifiers.new("cut", "BOOLEAN"); md.object = hole; md.operation = "DIFFERENCE"
    bpy.context.view_layer.objects.active = p; bpy.ops.object.modifier_apply(modifier="cut"); bpy.data.objects.remove(hole)
    p.modifiers.new("t", "SOLIDIFY").thickness = 0.05
    p.data.materials.clear(); p.data.materials.append(mat(f"r{i}", srgb(hx)))
    # double rim line (Mithila double outline) as thin torus pair
    for k, rr in enumerate((inner + 0.10, inner + 0.26)):
        bpy.ops.mesh.primitive_torus_add(major_radius=rr, minor_radius=0.025, location=(0, y - 0.04, 0), rotation=(math.radians(90), 0, 0), major_segments=128)
        t = bpy.context.object; t.data.materials.append(mat(f"rim{i}{k}", srgb("#100E17"), .6))
    rings.append(p)
# glowing chandan core at the end
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, len(cols) * 1.3 + 1, 0), rotation=(math.radians(90), 0, 0))
bpy.context.object.data.materials.append(mat("core", srgb("#F4EADB"), emit=3.0))
bpy.ops.object.light_add(type="AREA", location=(-5, -6, 5)); k = bpy.context.object; k.data.energy = 600; k.data.size = 5; k.data.color = (1, .86, .66)
k.rotation_euler = (math.radians(55), 0, math.radians(-40))
bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(math.radians(90), 0, 0)); cam = bpy.context.object; sc.camera = cam; cam.data.lens = 32
cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = 2.0
# animation: ease-in dolly through the rings, slight roll; rings counter-rotate
for f in range(1, N + 1):
    t = (f - 1) / (N - 1); e = t * t * (3 - 2 * t)
    cam.location = (0, -10 + e * 18.5, 0); cam.rotation_euler = (math.radians(90), math.radians(e * 18), 0)
    cam.data.dof.focus_distance = max(1.0, 10 - e * 8)
    cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f); cam.data.keyframe_insert("dof.focus_distance", frame=f)
for i, r in enumerate(rings):
    r.rotation_euler = (0, 0, 0); r.keyframe_insert("rotation_euler", frame=1)
    r.rotation_euler = (0, math.radians((-1) ** i * 12), 0); r.keyframe_insert("rotation_euler", frame=N)
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = spp; sc.cycles.use_denoising = True
sc.view_settings.view_transform = "AgX"; sc.render.image_settings.file_format = "PNG"
sc.render.filepath = out.rstrip("/") + "/portal_"
bpy.ops.render.render(animation=True)
print("DONE")
