import bpy
import numpy as np
import os
import random


#Get all names of objects
lst_Names = [ob.name for ob in bpy.data.objects]

#Initialise Defaults:
bpy.ops.mesh.primitive_cube_add()
bpy.data.scenes[0].frame_start = 1
bpy.data.scenes[0].frame_end = 1048574

class Food:
    def __init__ (self,name, locx,locy,locz):
        self.name = name
        self.locx = locx
        self.locy = locy
        self.locz = locz
    
        bpy.ops.mesh.primitive_ico_sphere_add()
        bpy.context.active_object.name = name
        self.food = bpy.data.objects[name]
        self.food.location.x = locx
        self.food.location.y = locy
        self.food.location.z = locz
        
class Rock:
    def __init__ (self, name, locx,locy,locz):
        self.name = name
        self.locx = locx
        self.locy = locy
        self.locz = locz
        
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions = 1, location = (locx,locy,locz))
        bpy.context.active_object.name = name
        self.rock = bpy.data.objects[name]
        
class Floor:
    def __init__(self, name, width, height):
        
        if name not in lst_Names:
            print("creating floor")
            bpy.ops.mesh.primitive_plane_add(size=20)
            bpy.context.active_object.name = name
        
        self.floor = bpy.data.objects[name]
        self.name = name

        self.width = width
        self.height = height
        
    def scale(self, x, y, z=0):
        self.floor.scale = (x, y, z)
    
    def get_obj_name(self):
        return self.name
    
    def transform_to_origin(self):  
        self.floor.location.x = 0
        self.floor.location.y = 0
    
    def get_world_location(self):
        return self.floor.location.x, self.floor.location.y, self.floor.location.z
        
        
    def getEndSidesXWorldLocation(self):
        startPointx = self.floor.location.x - self.floor.dimensions.x/2
        endPointx = self.floor.location.x + self.floor.dimensions.x/2
        return startPointx, endPointx

    def setWorldLocation(self, worldx, worldy, worldz):
        self.floor.select_set(True)
        self.floor.location.x = worldx
        self.floor.location.y = worldy
        self.floor.location.z = worldz

    def getDimensions(self):
        return self.floor.dimensions.x, self.floor.dimensions.y, self.floor.dimensions.z
        
class CreateFish_Follows:
    def __init__(self, name, spawnX, spawnY, spawnZ):
        if name not in lst_Names:
            print("SphereFollow")
            bpy.ops.mesh.primitive_ico_sphere_add()
            bpy.context.active_object.location = (spawnX,spawnY,spawnZ)
            bpy.context.active_object.name = name
        
        self.Fish_Follow = bpy.data.objects[name]

        self.name = name
    
    def get_obj_name(self):
        return self.name
    
    def scale(self, value):
        self.Fish_Follow.scale = (1 * value, 1* value, 1* value)

    def animateFish_Follows(self,startloc,endloc,startingFrame,endingFrame, midframe, bsetCyclic=False):
        #bpy.context.scene.frame_current(frame=startingFrame)
        bpy.context.view_layer.objects.active = self.Fish_Follow
        self.Fish_Follow.select_set(True)
        #bpy.context.active_object.keyframe_insert(data_path="location", frame=startingFrame, index =-1)
        self.Fish_Follow.location.x += (endloc-startloc)
        print(self.Fish_Follow.location)
        bpy.context.scene.frame_set(frame=midframe)
        bpy.context.active_object.keyframe_insert(data_path="location", frame=midframe, index=-1)

        bpy.context.scene.frame_set(frame=endingFrame) 
        self.Fish_Follow.location.x = startloc+5
        print(self.Fish_Follow.location) 
        bpy.context.active_object.keyframe_insert(data_path= 'location', frame=endingFrame, index=-1)       

        bpy.context.scene.frame_set(frame=startingFrame)
        self.Fish_Follow.location.x = startloc
        print(self.Fish_Follow.location)
        bpy.context.active_object.keyframe_insert(data_path= 'location', frame=startingFrame, index=-1)

        if bsetCyclic == True:
            fc = self.Fish_Follow.animation_data.action.fcurves
            for fcurve in fc:
                modifiers = fcurve.modifiers

                if not len(modifiers):
                    modifier = modifiers.new('CYCLES')
                    modifier.mode_before = 'REPEAT'
                    modifier.mode_after = 'REPEAT'
                    continue
        
                if modifiers[0].type == 'CYCLES':
                    continue
        
                print(f'Cannot add Cycles modifier to {self.Fish_Follow.animation.action.name} F-curve {fcurve.data_path}[{fcurve.array_index}]')

class ParticleSystems:
    def __init__(self,name,world_x,world_y,world_z):
        self.world_x = world_x
        self.world_y = world_y
        self.world_z = world_z
        self.name = name
        self.bpyOpsBoid = bpy.ops.boid
        self.bpyTypesBoidState = bpy.types.BoidState

        bpy.ops.mesh.primitive_plane_add(size=1,location=(self.world_x,self.world_y,self.world_z))
        bpy.context.active_object.name = name
        self.particlesystem = bpy.data.objects[name]
    
    def create_particle_system_modifier(self, _RENDERTYPE_, _INSTANCE_, _PHYSICSTYPE_, lifespan, spawn_amount, particle_size, particle_mass):
        self.particlesystem.modifiers.new("part",type='PARTICLE_SYSTEM')
        part = self.particlesystem.particle_systems[0]

        settings = part.settings
        self.settings = settings

        settings.emit_from = 'VERT'
        settings.physics_type = _PHYSICSTYPE_
        settings.particle_size = particle_size
        settings.render_type = _RENDERTYPE_
        settings.instance_collection = _INSTANCE_
        settings.lifetime = lifespan
        settings.count = spawn_amount
        settings.mass = particle_mass
        settings.frame_end = 100
        
        boid_part = settings.boids
        # #boids settings (default)
        boid_part.air_speed_max = 11.80
        boid_part.air_speed_min = .330
        boid_part.air_acc_max = .529
        boid_part.air_ave_max = .166
        boid_part.air_personal_space = 10.0
        boid_part.bank = 1.215
        boid_part.pitch = 0.0
        boid_part.height = 0.0

    def add_Rule_Follow_Leader(self, Rule_Type, context_override, Bpycontext):
        context_override["particle_settings"] = self.settings
        with Bpycontext.temp_override(**context_override):
            bpy.ops.boid.rule_add(type=Rule_Type)

    def add_Rule_Avoid(self, Rule_Type, context_override, Bpycontext):
        context_override["particle_settings"] = self.settings
        with Bpycontext.temp_override(**context_override):
            bpy.ops.boid.rule_add(type=Rule_Type)

    def Add_Rule_Flock(self, Rule_Type, context_override, Bpycontext):
        context_override["particle_settings"] = self.settings
        with Bpycontext.temp_override(**context_override):
            bpy.ops.boid.rule_add(type=Rule_Type)

    def add_Rule_Separate(self, Rule_Type, context_override, Bpycontext):
        context_override["particle_settings"] = self.settings
        with Bpycontext.temp_override(**context_override):
            bpy.ops.boid.rule_add(type=Rule_Type)

    def Add_Rule_Goal(self, Rule_Type, context_override, Bpycontext):
        context_override["particle_settings"] = self.settings
        with Bpycontext.temp_override(**context_override):
            bpy.ops.boid.rule_add(type=Rule_Type)

    def changeInteractiveObject(self,target, rule_index):
        state = self.settings.boids.active_boid_state #get last state --> the one just added
        rule = state.rules[rule_index]
        rule.object = target
        # print("follow leader rule")

    def DeleteAllRules(self, context_override, Bpycontext,addition):
        context_override["particle_settings"] = self.settings
        with Bpycontext.temp_override(**context_override):
            for i in range(0, 2+ addition):
                bpy.ops.boid.rule_del()

    def ChangeStartEndParticleDuration(self):
        self.settings.frame_end = 2000

    def deleteLastRule(self, context_override, Bpycontext):
        context_override["particle_settings"] = self.settings
        with Bpycontext.temp_override(**context_override):
            bpy.ops.boid.rule_del()

class Fish:
    def __init__ (self, file_path, inner_path,object_name):
        self.file_path = file_path
        self.inner_path = inner_path
        self.object_name = object_name

    def get_object_reference(self,object_name):
        self.objectInstance = bpy.data.objects[object_name]
    
    def append(self):
        bpy.ops.wm.append(
        filepath=os.path.join(self.file_path, self.inner_path, self.object_name),
        directory=os.path.join(self.file_path, self.inner_path),
        filename=self.object_name)

        self.objectInstance = bpy.data.objects[self.object_name]

        return self.objectInstance
    
    def get_name(self):
        return self.object_name
    
    def set_Location(self, worldx, worldy, worldz):
        self.objectInstance.select_set(True)
        self.objectInstance.location.x = worldx
        self.objectInstance.location.y = worldy
        self.objectInstance.location.z = worldz

    def scale(self, x, y, z=0):
        self.objectInstance.scale = (x, y, z)

    def get_world_Location(self):
        return self.objectInstance.location.x,self.objectInstance.location.y, self.objectInstance.location.z

class CreateMaterial:
    def __init__(self, name):
        bpy.data.materials.new(name = name)
        self.material = bpy.data.materials[name]
        self.material.use_nodes = True
        self.principled_BSDF = self.material.node_tree.nodes["Principled BSDF"]
        self.diffuse = self.principled_BSDF.inputs[0]
        self.metallic = self.principled_BSDF.inputs[1]
        self.roughness = self.principled_BSDF.inputs[2]
        self.alpha = self.principled_BSDF.inputs[4]

    def set_Default_Material_Colour(self, RGBVal):
        self.diffuse.default_value = RGBVal
    
    def set_Metallic(self,metallicVal):
        self.metallic.defauly_value = metallicVal

    def assign_To_Object(self, object_name):
        bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
        activeObj = bpy.context.active_object
        # Assign it to object
        if activeObj.data.materials:
        # assign to 1st material slot
            activeObj.data.materials[0] = self.material
        else:
        # no slots
            activeObj.data.materials.append(self.material)

    def add_Image_Texture(self, image_filepath):
        texImage = self.material.node_tree.nodes.new('ShaderNodeTexImage')
        # texImage.image = bpy.data.images.load("C:\\Users\\myName\\Downloads\\Textures\\Downloaded\\flooring5.jpg")
        self.material.node_tree.links.new(self.principled_BSDF.inputs['Base Color'], texImage.outputs['Color'])
        
class Spawn_Duplicate:
    def __init__(self,fish_object_ref_name):
        self.fish_object_ref_name = fish_object_ref_name
        fishObjToCopy  = bpy.data.objects.get(fish_object_ref_name)
        if fishObjToCopy:
            copiedFishObj = fishObjToCopy.copy()
        copiedFishObj.data =  fishObjToCopy.data.copy()
        copiedFishObj.animation_data_clear()
        self.objectInstance= copiedFishObj
        self.objectInstance.name = fish_object_ref_name + " Copy"
        bpy.context.collection.objects.link(self.objectInstance)
    
    def set_Location(self, worldx,worldy,worldz):
        self.objectInstance.location.x = worldx
        self.objectInstance.location.y = worldy
        self.objectInstance.location.z = worldz

    def get_World_Location(self):
        return self.objectInstance.location.x, self.objectInstance.location.y, self.objectInstance.location.z
    
class Fish_Rig:
    def __init__ (self, file_path, inner_path,armature_object_name,new_name):
        self.file_path = file_path
        self.inner_path = inner_path
        self.armature_object_name = armature_object_name
        self.new_name = new_name
   
    def append(self):
        bpy.ops.wm.append(
        filepath=os.path.join(self.file_path, self.inner_path, self.armature_object_name),
        directory=os.path.join(self.file_path, self.inner_path),
        filename=self.armature_object_name)

        self.armature_object = bpy.data.objects[self.armature_object_name]
        self.armature_object.name = self.new_name

        return self.armature_object
    
    def get_name(self):
        return self.armature_object_name
    
    def set_Location(self, worldx, worldy, worldz):
        self.armature_object.select_set(True)
        self.armature_object.location.x = worldx
        self.armature_object.location.y = worldy
        self.armature_object.location.z = worldz

    def get_world_Location(self):
        return self.armature_object.location.x,self.armature_object.location.y, self.armature_object.location.z
    
    def parent_to_object(self,child_object,parenting_protocol):
        #Be sure to deselect all objects first! 
        #Then, continue the process with a clean slate, selecting first the parent and then the object. 
        #Else, multiple parents may be selected --> throwing a "loop in parents error.""
        if len(bpy.context.selected_objects) > 0:
            bpy.ops.object.select_all(action="DESELECT")
        parent_object = self.armature_object
        morph_object = child_object
        parent_object.select_set(True)
        morph_object.select_set(True)
        bpy.context.view_layer.objects.active = parent_object
        bpy.ops.object.parent_set(type=parenting_protocol)

    def add_Follow_Path_Constraint(self, constraint_Path_Obj):
        constraint_mod = self.armature_object.constraints.new(type= "FOLLOW_PATH")
        constraint_mod.target = constraint_Path_Obj
        constraint_Path_Obj.data.use_path = True

class Follow_Path:
    def __init__(self,object_name):
        self.object_name = object_name
        self.objectInstance = bpy.data.objects[object_name]

    def set_Location(self, worldx, worldy, worldz):
        self.objectInstance.select_set(True)
        self.objectInstance.location.x = worldx
        self.objectInstance.location.y = worldy
        self.objectInstance.location.z = worldz

    def get_world_Location(self):
        return self.objectInstance.location.x,self.objectInstance.location.y, self.objectInstance.location.z
    


#Add Fish Collection
fishCollection = bpy.ops.collection.create(name= "Fish Collection")
bpy.context.scene.collection.children.link(bpy.data.collections["Fish Collection"])
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[-1]
fish_path = "blender_fishes/Blender Scene Files/fishes.blend"
fish = Fish(file_path=fish_path, inner_path="Object", object_name="Fish1")
fish.objectInstance = fish.append()
fish2 = Fish(file_path=fish_path, inner_path="Object", object_name="Fish2")
fish2.objectInstance = fish2.append()
fish3 = Fish(file_path=fish_path, inner_path="Object", object_name="Fish3")
fish3.objectInstance = fish3.append()


Paths_Rigs_Collection = bpy.ops.collection.create(name = "Paths_and_Rigs")
bpy.context.scene.collection.children.link(bpy.data.collections["Paths_and_Rigs"])
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[-1]
bpy.data.collections["Paths_and_Rigs"].objects.unlink(bpy.data.objects[fish3.object_name])
# fish_path1 =  Fish(file_path="C:\\Users\\thnga\\Desktop\\BlenderPython\\fish_rigs.blend", inner_path="Object", object_name="Fish_Path1")
# fish_path1.append()
fish_rig_path = "blender_fishes/Blender Scene Files/fish_rigs.blend"
fish1_Rig = Fish_Rig(file_path=fish_rig_path, inner_path="Object", armature_object_name="Fish_Rig1", new_name="Fish_Rig1")
fish1_Rig.armature_object = fish1_Rig.append()
# fish_path2 =  Fish(file_path="C:\\Users\\thnga\\Desktop\\BlenderPython\\fish_rigs.blend", inner_path="Object", object_name="Fish_Path2")
# fish_path2.append()
fish2_Rig = Fish_Rig(file_path=fish_rig_path, inner_path="Object", armature_object_name="Fish_Rig2", new_name="Fish_Rig2")
fish2_Rig.armature_object = fish2_Rig.append()
# fish_path3 =  Fish(file_path="C:\\Users\\thnga\\Desktop\\BlenderPython\\fish_rigs.blend", inner_path="Object", object_name="Fish_Path3")
# fish_path3.append()
fish3_Rig = Fish_Rig(file_path=fish_rig_path, inner_path="Object", armature_object_name="Fish_Rig3", new_name="Fish_Rig3")
fish3_Rig.armature_object = fish3_Rig.append()

fish_path3 = Follow_Path(object_name="Fish_Path3")
fish_path2 = Follow_Path(object_name="Fish_Path2")
fish_path1 = Follow_Path(object_name="Fish_Path1")

#reset active collection to default scene collection
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[0]


#create struggling fish references
Fish1_Struggle_Instance = Spawn_Duplicate(fish_object_ref_name="Fish1")
chosenFish = bpy.data.objects[Fish1_Struggle_Instance.fish_object_ref_name]
worldLocation_X = chosenFish.location.x
worldLocation_Y = chosenFish.location.y
worldLocation_Z = chosenFish.location.z
duplicate_offset = 80
Fish1_Struggle_Instance.set_Location(worldx=worldLocation_X-duplicate_offset,worldy=worldLocation_Y,worldz=worldLocation_Z)

Fish2_Struggle_Instance = Spawn_Duplicate(fish_object_ref_name="Fish2")
chosenFish = bpy.data.objects[Fish2_Struggle_Instance.fish_object_ref_name]
worldLocation_X = chosenFish.location.x
worldLocation_Y = chosenFish.location.y
worldLocation_Z = chosenFish.location.z
duplicate_offset = 90
Fish2_Struggle_Instance.set_Location(worldx=worldLocation_X-duplicate_offset,worldy=worldLocation_Y,worldz=worldLocation_Z)

Fish3_Struggle_Instance = Spawn_Duplicate(fish_object_ref_name="Fish3")
chosenFish = bpy.data.objects[Fish3_Struggle_Instance.fish_object_ref_name]
worldLocation_X = chosenFish.location.x
worldLocation_Y = chosenFish.location.y
worldLocation_Z = chosenFish.location.z
duplicate_offset = 100
Fish3_Struggle_Instance.set_Location(worldx=worldLocation_X-duplicate_offset,worldy=worldLocation_Y,worldz=worldLocation_Z)

#center fish path to fish dups
fish_path1.set_Location(worldx=Fish1_Struggle_Instance.get_World_Location()[0],worldy=Fish1_Struggle_Instance.get_World_Location()[1], worldz=Fish1_Struggle_Instance.get_World_Location()[2])
fish_path2.set_Location(worldx=Fish2_Struggle_Instance.get_World_Location()[0],worldy=Fish2_Struggle_Instance.get_World_Location()[1], worldz=Fish2_Struggle_Instance.get_World_Location()[2])
fish_path3.set_Location(worldx=Fish3_Struggle_Instance.get_World_Location()[0],worldy=Fish3_Struggle_Instance.get_World_Location()[1], worldz=Fish3_Struggle_Instance.get_World_Location()[2])

#Parent, with automatic weights
fish1_Rig.parent_to_object(child_object=Fish1_Struggle_Instance.objectInstance,parenting_protocol="ARMATURE_AUTO")
fish2_Rig.parent_to_object(child_object=Fish2_Struggle_Instance.objectInstance,parenting_protocol="ARMATURE_AUTO")
fish3_Rig.parent_to_object(child_object=Fish3_Struggle_Instance.objectInstance,parenting_protocol="ARMATURE_AUTO")

#move the escaping fish via eval time
sce = bpy.context.scene

width = 80
height = 40
SCALE_FACTOR = 0.05
floor = Floor('main_floor', width = width, height = height)
floor.transform_to_origin()
floor.scale(width*SCALE_FACTOR, height*SCALE_FACTOR)
floorplane = Floor("background", width=2000, height=2000)
floorplane.scale(width*10, height* 10)
floorplane.setWorldLocation(worldx=30,worldy=30,worldz=-30)

bpy.context.view_layer.objects.active = bpy.data.objects[floor.get_obj_name()]
bpy.data.objects[floor.get_obj_name()].select_set(True)
bpy.ops.object.transform_apply(scale=True)
floor.setWorldLocation(worldx= floor.getDimensions()[0]/2, worldy= floor.getDimensions()[1]/2, worldz=-10)
cube = bpy.ops.mesh.primitive_cube_add()

floorGlobalX, floorGlobalY, floorGlobalZ = floor.get_world_location()

#Create Fish Follows
fish_followGlobalY = floorGlobalY
fish_followGlobalZ = floorGlobalZ
fish_followStartX,fish_followEndX = floor.getEndSidesXWorldLocation()

left_Offset = -10
right_Offset = -10

fish_Follow1 = CreateFish_Follows("FishFollow1", fish_followStartX, fish_followGlobalY, fish_followGlobalZ)
fish_Follow2 = CreateFish_Follows("FishFollow2", fish_followEndX, fish_followGlobalY, fish_followGlobalZ)
fish_Follow1.scale(value=0.1)
fish_Follow2.scale(value=0.1)
fish_Follow1.animateFish_Follows(startloc=fish_followStartX - left_Offset, endloc=fish_followEndX + right_Offset,startingFrame=1,midframe=300, endingFrame=400,bsetCyclic=True)
fish_Follow2.animateFish_Follows(startloc=fish_followEndX + right_Offset, endloc=fish_followStartX - left_Offset,startingFrame=1,midframe=200, endingFrame=400,bsetCyclic=True)

xoffset = 30
yoffset = 30

particleSystemSpawnLocation = (floorGlobalX - floor.getDimensions()[0]/2 + xoffset, floorGlobalY+floor.getDimensions()[1]/2 - yoffset, 0)
particleSystemSpawnLocation2 = (floorGlobalX + floor.getDimensions()[0]/2 - xoffset, floorGlobalY-floor.getDimensions()[1]/2 + yoffset, 0)
fish_spawn = ParticleSystems("Fish_Spawn1",particleSystemSpawnLocation[0],particleSystemSpawnLocation[1],particleSystemSpawnLocation[2])
fish_spawn.create_particle_system_modifier(_RENDERTYPE_ = 'COLLECTION',_INSTANCE_= bpy.context.scene.collection.children["Fish Collection"], _PHYSICSTYPE_ = 'BOIDS',lifespan=100000, spawn_amount=100, particle_size=1.5, particle_mass=0.2)

fish_spawn2 = ParticleSystems("Fish_Spawn2",particleSystemSpawnLocation2[0],particleSystemSpawnLocation2[1], particleSystemSpawnLocation2[2])
fish_spawn2.create_particle_system_modifier(_RENDERTYPE_ = 'COLLECTION',_INSTANCE_= bpy.context.scene.collection.children["Fish Collection"], _PHYSICSTYPE_ = 'BOIDS',lifespan=100000, spawn_amount=100, particle_size=1.5, particle_mass=0.2)
# Add Follow Leader Rule

#delete all rules
fish_spawn.DeleteAllRules(bpy.context.copy(),bpy.context,addition=0)
fish_spawn2.DeleteAllRules(bpy.context.copy(), bpy.context,addition=0)

#add default rules:
# Changed here
# fish_spawn.Add_Rule_Separate(Rule_Type="SEPARATE", context_override=bpy.context.copy(), Bpycontext=bpy.context)
# fish_spawn.Add_Rule_Follow_Leader(Rule_Type="FOLLOW_LEADER",context_override=bpy.context.copy(),Bpycontext=bpy.context)
# fish_spawn.Add_Rule_Separate(Rule_Type="SEPARATE", context_override=bpy.context.copy(), Bpycontext=bpy.context)
# fish_spawn.changeInteractiveObject(rule_index=1, leaderToFollow=fish_Follow1.Fish_Follow)


# fish_spawn2.Add_Rule_Separate(Rule_Type="SEPARATE", context_override=bpy.context.copy(), Bpycontext=bpy.context)
# fish_spawn2.Add_Rule_Follow_Leader(Rule_Type="FOLLOW_LEADER",context_override=bpy.context.copy(),Bpycontext=bpy.context)
# fish_spawn2.Add_Rule_Separate(Rule_Type="SEPARATE", context_override=bpy.context.copy(), Bpycontext=bpy.context)
# fish_spawn2.changeInteractiveObject(rule_index=1, leaderToFollow=fish_Follow2.Fish_Follow)

#fish_spawn.add_Rule_Avoid(Rule_Type="AVOID", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn.Add_Rule_Goal(Rule_Type="GOAL", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn.add_Rule_Separate(Rule_Type="SEPARATE", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn.add_Rule_Follow_Leader(Rule_Type="FOLLOW_LEADER",context_override=bpy.context.copy(),Bpycontext=bpy.context)
fish_spawn.changeInteractiveObject(rule_index=2, target=fish_Follow1.Fish_Follow)
fish_spawn.add_Rule_Separate(Rule_Type="AVOID_COLLISION", context_override=bpy.context.copy(), Bpycontext=bpy.context)

#fish_spawn2.add_Rule_Avoid(Rule_Type="AVOID", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn2.Add_Rule_Goal(Rule_Type="GOAL", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn2.add_Rule_Separate(Rule_Type="SEPARATE", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn2.add_Rule_Follow_Leader(Rule_Type="FOLLOW_LEADER",context_override=bpy.context.copy(),Bpycontext=bpy.context)
fish_spawn2.changeInteractiveObject(rule_index=2, target=fish_Follow2.Fish_Follow)
fish_spawn2.add_Rule_Separate(Rule_Type="AVOID_COLLISION", context_override=bpy.context.copy(), Bpycontext=bpy.context)

fishMaterial_1 = CreateMaterial(name="FishMaterial")
fishMaterial_2 = CreateMaterial(name="FishMaterial2")
fishMaterial_3 = CreateMaterial(name="FishMaterial3")
fishMaterial_1.assign_To_Object(object_name=fish.get_name())
fishMaterial_2.assign_To_Object(object_name=fish2.get_name())
fishMaterial_3.assign_To_Object(object_name=fish3.get_name())

fishMaterial_1.set_Default_Material_Colour(RGBVal=(0.109, 0.800, 0.105,1.00))
fishMaterial_2.set_Default_Material_Colour(RGBVal=(0.713, 0.802, 0.800,1.00))
fishMaterial_3.set_Default_Material_Colour(RGBVal=(0.800, 0.556, 0.105,1.00))


#Create the Floor Material
floorMaterial = CreateMaterial(name= "FloorMaterial")
floorMaterial.assign_To_Object(object_name=floor.get_obj_name())
floorMaterial.set_Default_Material_Colour(RGBVal=(0,0,0,0))

cubematerial = CreateMaterial(name="CubeMat")
cubematerial.assign_To_Object(object_name="Cube")

floorplaneat = CreateMaterial(name="planeMat")
cubematerial.set_Default_Material_Colour(RGBVal=(1.0,0.089,0.058,1.0))
floorplaneat.set_Default_Material_Colour(RGBVal=(0,0,0,1))

bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1,1,1,1)


fishPath1_backupLoc = fish_path1.get_world_Location()
fishPath2_backupLoc = fish_path2.get_world_Location()
fishPath3_backupLoc = fish_path3.get_world_Location()
lst_backups = [fishPath1_backupLoc,fishPath2_backupLoc,fishPath3_backupLoc]
lst_fish_paths = [fish_path1, fish_path2, fish_path3]


path_eval_value = 0
chosenIndex = 0
def spawn_struggling_fish(userxCoord, useryCoord, lst_fish: list):
    global chosenIndex
    chosenFish= lst_fish[chosenIndex]
    chosenFish.set_Location(worldx= userxCoord, worldy = useryCoord, worldz = 0)

def move_struggling_fish_back(_lst_backups: list, lst_fish):
    global chosenIndex
    backuploc = _lst_backups[chosenIndex]
    chosenFish = lst_fish[chosenIndex]
    chosenFish.set_Location(worldx = backuploc[0], worldy = backuploc[1], worldz = backuploc[2])

    curveindex = chosenIndex-3
    nurbs_path_ref = bpy.data.curves[curveindex]
    nurbs_path_ref.eval_time = 0

def update_curve_evaluation_time(curve_index, fps):
    global path_eval_value
    nurbs_path_ref = bpy.data.curves[curve_index]
    path_eval_value += (sce.frame_current-sce.frame_current+1)/fps
    if path_eval_value == 100:
        path_eval_value = 0
    nurbs_path_ref.eval_time = path_eval_value



import time

from pathlib import Path
coor_path = "blender_fishes/Run Simulation/coords.txt"
f = Path(bpy.path.abspath(coor_path))
# plane = bpy.data.objects["Plane"]
cube = bpy.data.objects["Cube"]
bHasStrugglingFish = False

class OpenCVAnimOperator(bpy.types.Operator):
    
    bl_idname = "wm.opencv_operator"
    bl_label = "OpenCV Animation Operator"
    
    _timer = None
    _cap  = None
    stop = False

    def __init__(self):
        self.food_timer = time.time()
        self.rock_timer = time.time()
        self.struggle_timer = time.time()
        self.point_timer = time.time()

    def modal(self, context, event):
        global chosenIndex
        global path_eval_value
        global bHasStrugglingFish
        if (event.type in {
            'ESC'}) or self.stop == True:
            self.cancel(context)
            return {'CANCELLED'}
        
        if event.type == 'TIMER':

            try:
                user_input = list(map(int, f.read_text().split()))
#                print(user_input)
                if user_input:
                    user_x = max(user_input[0], 0)
                    user_y = max(user_input[1], 0)
                    giving_food = user_input[2]
                    throwing_rock = user_input[3]
                    ok_gesture = user_input[4]
                    point_gesture = user_input[5]
                    cube.location.x = user_x/1400*floor.getDimensions()[0]
                    cube.location.y = (user_y/700)*floor.getDimensions()[1] #marked as flipped (1-user_y/700) originally

                    # if throwing_rock and 'rock' not in lst_Names:
                    #     rock = Rock('rock', cube.location.x, cube.location.y, 0)
                    #     lst_Names.append('rock')

                    #     fish_spawn.changeInteractiveObject(rule_index=0, target=rock.rock)
                    #     fish_spawn2.changeInteractiveObject(rule_index=0, target=rock.rock)
                        
                    if giving_food and 'food' not in lst_Names:
                        # initialize food
                        food = Food('food', cube.location.x, cube.location.y, 0)
                        lst_Names.append('food')
                        
                        # change leader of the fishes to food
                        fish_spawn.changeInteractiveObject(rule_index=0, target=food.food)
                        fish_spawn2.changeInteractiveObject(rule_index=0, target=food.food)

                    #print(ok_gesture)
                    if ok_gesture and 'struggle' not in lst_Names and bHasStrugglingFish == False:
                        path_eval_value = 0
                        chosenIndex = random.randint(0,2) 
                        lst_Names.append('struggle')
                        bHasStrugglingFish = True
                        spawn_struggling_fish(userxCoord=cube.location.x, useryCoord=cube.location.y,lst_fish=lst_fish_paths)

                    if point_gesture and 'follow_cube' not in lst_Names:
                        fish_spawn.changeInteractiveObject(rule_index=0, target=cube)
                        fish_spawn2.changeInteractiveObject(rule_index=0,target=cube)
                        lst_Names.append('follow_cube')
                        cubematerial.set_Default_Material_Colour(RGBVal=(1.0,0.089,0.700,1.0))
                        
                # if 'rock' in lst_Names:
                #    if time.time() - self.rock_timer > 1.2:
                #         lst_Names.remove('rock')
                #         bpy.data.objects['rock'].select_set(True)
                #         bpy.ops.object.delete()
                #         self.rock_timer = time.time()
               
                #         fish_spawn.changeInteractiveObject(rule_index=0, target=None)
                #         fish_spawn2.changeInteractiveObject(rule_index=0, target=None)
               
                if 'food' in lst_Names:
                    if time.time() - self.food_timer > 5:
                        # after n seconds, remove food
                        lst_Names.remove('food')
                        bpy.data.objects['food'].select_set(True)
                        bpy.ops.object.delete()
                        self.food_timer = time.time()
                        
                        # change the leader back to FishFollow
                        fish_spawn.changeInteractiveObject(rule_index=0, target=None)
                        fish_spawn2.changeInteractiveObject(rule_index=0, target=None)
                
                if 'struggle' in lst_Names:
                    if time.time() - self.struggle_timer > 10:
                        self.struggle_timer = time.time()
                        lst_Names.remove('struggle')
                        move_struggling_fish_back(_lst_backups=lst_backups,lst_fish=lst_fish_paths)
                        bHasStrugglingFish = False

                    elif time.time() - self.struggle_timer > 5:
                        curveIndex = chosenIndex -3
                        update_curve_evaluation_time(curve_index=curveIndex,fps=2)

                if 'follow_cube' in lst_Names:
                    if time.time() - self.point_timer > 5:
                        fish_spawn.changeInteractiveObject(rule_index=0, target=None)
                        fish_spawn2.changeInteractiveObject(rule_index=0,target=None)
                        cubematerial.set_Default_Material_Colour(RGBVal=(1.0,0.089,0.058,1.0))
                        lst_Names.remove('follow_cube')
                        self.point_timer = time.time()


            except Exception as e:
                print(e)
                return {'PASS_THROUGH'}
        
        return {'PASS_THROUGH'}
    
    def stop_playback(self, scene, _):
        print(format(scene.frame_current) + " / " + format(scene.frame_end))
        if scene.frame_current == scene.frame_end:
            bpy.ops.screen.animation_cancel(restore_frame=False)
        
    def execute(self, context):
        bpy.app.handlers.frame_change_pre.append(self.stop_playback)


        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}
    
    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        self._cap.release()
        self._cap = None

def register():
    bpy.utils.register_class(OpenCVAnimOperator)

def unregister():
    bpy.utils.unregister_class(OpenCVAnimOperator)

# if __name__ == '__main__':
try:
    register()
    bpy.ops.wm.opencv_operator()
except Exception as e:
    print(e)
    