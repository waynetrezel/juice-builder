"""Build a reusable Aloe vera leaf pilot asset and render it in the kitchen look.

Run from the project directory:
  blender -b --python blender/create_aloe_pilot.py

The geometry is procedural for iteration. It is an asset-quality study, not a
claim that procedural geometry alone meets the final hyper-real production bar.
"""
import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

random.seed(117)
ROOT = Path(r"C:\Coding\Applications\Ideas\juicebuilder")
OUT = ROOT / "renders" / "aloe-asset-pilot-v2.png"
BLEND = ROOT / "aloe-asset-pilot-v2.blend"
TEX = ROOT / "assets" / "aloe" / "aloe-skin-albedo.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = 1500
scene.render.resolution_y = 1050
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"

def material(name, color, roughness=.35, metallic=0, subsurface=0, transmission=0, coat=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Subsurface Weight"].default_value = subsurface
    bsdf.inputs["Transmission Weight"].default_value = transmission
    bsdf.inputs["Coat Weight"].default_value = coat
    return m

def aloe_skin():
    m = material("Aloe waxy cuticle with natural mottling", (.055,.16,.032), .48, subsurface=.035, coat=.035)
    n, l = m.node_tree.nodes, m.node_tree.links
    bsdf = n.get("Principled BSDF")
    texcoord = n.new("ShaderNodeTexCoord")
    image = bpy.data.images.load(str(TEX), check_existing=True)
    image.pack()
    tex = n.new("ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = "Cubic"
    tex.extension = "REPEAT"
    l.new(texcoord.outputs["UV"], tex.inputs["Vector"])
    l.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Specular IOR Level"].default_value = .24

    fine = n.new("ShaderNodeTexNoise")
    fine.inputs["Scale"].default_value = 155
    fine.inputs["Detail"].default_value = 2.4
    fine.inputs["Roughness"].default_value = .8
    bump = n.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = .09
    bump.inputs["Distance"].default_value = .006
    l.new(texcoord.outputs["Generated"], fine.inputs["Vector"])
    l.new(fine.outputs["Fac"], bump.inputs["Height"])
    l.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m

skin = aloe_skin()
edge_mat = material("Aloe edge and fine teeth", (.22,.36,.075), .32, subsurface=.04, coat=.1)
gel = material("Fresh cut translucent aloe gel", (.55,.76,.37), .16, subsurface=.24, transmission=.07, coat=.12)
dew_mat = material("Clear water beads", (.82,.93,.96), .035, transmission=.96, coat=.4)
counter = material("Dark honed kitchen stone", (.055,.060,.056), .27)
brick = material("Warm red brick", (.20,.065,.035), .86)
black = material("Blackened steel", (.018,.024,.027), .24, metallic=.72)
warm_metal = material("Warm pendant interior", (.72,.42,.16), .24, metallic=.35)

def smooth(obj):
    if obj.type == "MESH":
        for p in obj.data.polygons:
            p.use_smooth = True
    return obj

def box(name, loc, dims, mat, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    if bevel:
        b = o.modifiers.new("Small manufactured edge radii", "BEVEL")
        b.width = bevel
        b.segments = 3
        o.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return o

def sphere(name, loc, scale, mat, segments=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    o.data.materials.append(mat)
    return smooth(o)

# Detailed, cupped aloe blade: tapered cross-section, lifted edges and subtle ribs.
length, nx, ny = 3.55, 120, 48
top, bot, faces = [], [], []
for i in range(nx + 1):
    s = i / nx
    x = (s - .5) * length
    width = .22 * (1-s) + .018 * s + .47 * math.sin(math.pi*s) ** .72
    thickness = .085 + .105 * math.sin(math.pi*s) ** .6
    centre = .15 + .30 * math.sin(math.pi*s) + .13*s
    # A gentle sweeping bend keeps the leaf from reading as a flat ribbon.
    bend_y = .15 * math.sin(math.pi*s) + .06 * s
    edge_wave = 1 + .055 * math.sin(math.tau * 36 * s) * math.sin(math.pi*s)
    for j in range(ny + 1):
        u = j / ny * 2 - 1
        y = u * width * edge_wave + bend_y
        rib = .012 * math.cos(u * math.pi * 8) * math.sin(math.pi*s)
        ztop = centre - .045 + .15*u*u + rib
        zbot = ztop - thickness * (1 - .22*u*u)
        top.append((x,y,ztop))
        bot.append((x,y,zbot))

stride = ny + 1
top_count = len(top)
for i in range(nx):
    for j in range(ny):
        a = i*stride+j; b = a+stride; c = b+1; d = a+1
        faces.append((a,b,c,d))
        faces.append((top_count+d,top_count+c,top_count+b,top_count+a))
# Close both serrated sides and the pointed tip. Keep the base open for its cut face.
for i in range(nx):
    a=i*stride; b=(i+1)*stride
    faces.append((a,top_count+a,top_count+b,b))
    a=i*stride+ny; b=(i+1)*stride+ny
    faces.append((b,top_count+b,top_count+a,a))
for j in range(ny):
    a=nx*stride+j; b=a+1
    faces.append((a,b,top_count+b,top_count+a))

mesh = bpy.data.meshes.new("Sculpted aloe leaf surface")
mesh.from_pydata(top+bot, [], faces)
mesh.materials.append(skin)
uv_layer = mesh.uv_layers.new(name="Aloe skin UV")
for loop in mesh.loops:
    idx = loop.vertex_index if loop.vertex_index < top_count else loop.vertex_index - top_count
    i, j = divmod(idx, stride)
    uv_layer.data[loop.index].uv = (j/ny, i/nx)
leaf = bpy.data.objects.new("Aloe vera leaf | asset pilot", mesh)
bpy.context.collection.objects.link(leaf)
smooth(leaf)
sub = leaf.modifiers.new("Fine surface smoothing", "SUBSURF")
sub.levels = 1
leaf.rotation_euler[2] = math.radians(36)
leaf.location = (-.05,-.30,0)
bpy.context.view_layer.update()

# Tapered triangular teeth sit on the blade edges, with their tips pointing outwards.
for side in (-1,1):
    for k in range(4,116,4):
        s=k/nx
        width=.22*(1-s)+.018*s+.47*math.sin(math.pi*s)**.72
        thickness=.085+.105*math.sin(math.pi*s)**.6
        centre=.15+.30*math.sin(math.pi*s)+.13*s
        bend_y=.15*math.sin(math.pi*s)+.06*s
        u=side
        y=u*width+bend_y
        z=centre-.045+.15*u*u-thickness*.12
        local=Vector(((s-.5)*length,y,z))
        pos=leaf.matrix_world @ local
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=.014, radius2=.001, depth=.045, location=pos)
        tooth=bpy.context.object
        tooth.name="Aloe marginal tooth"
        # Lean each little tooth away from the blade edge.
        tooth.rotation_euler=(math.radians(-side*72), 0, leaf.rotation_euler.z)
        tooth.data.materials.append(edge_mat)
        smooth(tooth)

# Elliptical layered cut face, facing outward from the thick leaf base.
cut_x=-length*.5-.008
cut_center_z=.105
ring_verts=[]
ring_faces=[]
for radius_y,radius_z in ((.205,.082),(.157,.059)):
    for j in range(64):
        a=math.tau*j/64
        ring_verts.append((cut_x, .15*0 + radius_y*math.cos(a), cut_center_z+radius_z*math.sin(a)))
ring_verts.append((cut_x,0,cut_center_z))
for j in range(64):
    ring_faces.append((j,(j+1)%64,64+(j+1)%64,64+j))
    ring_faces.append((128,64+j,64+(j+1)%64))
cut_mesh=bpy.data.meshes.new("Aloe cut gel and rind rings")
cut_mesh.from_pydata(ring_verts,[],ring_faces)
cut_mesh.materials.append(edge_mat)
cut_mesh.materials.append(gel)
for i,p in enumerate(cut_mesh.polygons):
    p.material_index=0 if i%2==0 else 1
cut_face=bpy.data.objects.new("Aloe cut face | translucent gel",cut_mesh)
bpy.context.collection.objects.link(cut_face)
cut_face.location=leaf.location
cut_face.rotation_euler=leaf.rotation_euler
for p in cut_face.data.polygons: p.use_smooth=True

# Sparse droplets, varied in size and clustered where the leaf cups.
for _ in range(42):
    s=random.uniform(.10,.90)
    u=random.uniform(-.62,.62)
    width=.22*(1-s)+.018*s+.47*math.sin(math.pi*s)**.72
    centre=.15+.30*math.sin(math.pi*s)+.13*s
    z=centre-.045+.15*u*u+.035
    y=u*width+.15*math.sin(math.pi*s)+.06*s
    pos=leaf.matrix_world @ Vector(((s-.5)*length,y,z))
    r=random.uniform(.008,.021)
    sphere("Aloe dew bead",pos,(r,r*.74,r*1.25),dew_mat,16,10)

# Minimal industrial prep-kitchen context: brick, charcoal island and pendants.
box("Dark stone work island",(0,0,-.24),(7.5,4.5,.34),counter,.035)
box("Kitchen cabinet base",(0,1.38,-.75),(7.2,.72,.75),black,.025)
box("Brick wall",(0,2.42,2.25),(11,.15,4.8),brick)

# Brick joints via a procedurally generated normal-height texture.
brick.use_nodes=True
n=brick.node_tree.nodes; l=brick.node_tree.links; bsdf=n.get("Principled BSDF")
texcoord=n.new("ShaderNodeTexCoord")
bricktex=n.new("ShaderNodeTexBrick")
bricktex.inputs["Color1"].default_value=(.25,.075,.04,1)
bricktex.inputs["Color2"].default_value=(.14,.04,.025,1)
bricktex.inputs["Mortar"].default_value=(.035,.03,.025,1)
bricktex.inputs["Scale"].default_value=4.5
bricktex.inputs["Mortar Size"].default_value=.025
separate=n.new("ShaderNodeSeparateXYZ")
combine=n.new("ShaderNodeCombineXYZ")
l.new(texcoord.outputs["Object"],separate.inputs["Vector"])
l.new(separate.outputs["X"],combine.inputs["X"])
l.new(separate.outputs["Z"],combine.inputs["Y"])
l.new(combine.outputs["Vector"],bricktex.inputs["Vector"])
l.new(bricktex.outputs["Color"],bsdf.inputs["Base Color"])
bb=n.new("ShaderNodeBump"); bb.inputs["Strength"].default_value=.28; bb.inputs["Distance"].default_value=.05
l.new(bricktex.outputs["Fac"],bb.inputs["Height"]); l.new(bb.outputs["Normal"],bsdf.inputs["Normal"])

def area(name,loc,target,energy,size,color):
    data=bpy.data.lights.new(name,"AREA"); data.energy=energy; data.shape="DISK"; data.size=size; data.color=color
    o=bpy.data.objects.new(name,data); bpy.context.collection.objects.link(o); o.location=loc
    o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler(); return o

for x,power in ((-1.5,240),(.6,290),(2.4,210)):
    # Down-facing practical area light, paired with a visible pendant shade.
    area("Warm kitchen downlight",(x,.25,4.2),(x*.6,-.15,.2),power,1.25,(1.0,.70,.43))
    bpy.ops.mesh.primitive_cone_add(vertices=40,radius1=.34,radius2=.10,depth=.24,location=(x,.25,4.04))
    shade=bpy.context.object; shade.name="Industrial pendant shade"; shade.data.materials.append(black)
    shade.data.materials.append(warm_metal)
area("Soft cool camera fill",(0,-4.5,3.0),(0,0,.5),75,4.0,(.75,.84,1.0))

world=bpy.data.worlds.new("Industrial kitchen ambience") if not bpy.data.worlds else bpy.data.worlds[0]
scene.world=world; world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.10,.075,.052,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=.22

camdata=bpy.data.cameras.new("Aloe close-up camera")
camera=bpy.data.objects.new("Aloe close-up camera",camdata); bpy.context.collection.objects.link(camera)
camera.location=(-2.9,-6.0,3.05)
target=Vector((0,0,.55)); camera.rotation_euler=(target-camera.location).to_track_quat("-Z","Y").to_euler()
camdata.lens=53; camdata.dof.use_dof=True; camdata.dof.focus_object=leaf; camdata.dof.aperture_fstop=5.0
scene.camera=camera
scene.render.filepath=str(OUT)

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
bpy.ops.render.render(write_still=True)
print("Saved aloe pilot asset:",BLEND)
print("Rendered aloe pilot frame:",OUT)
