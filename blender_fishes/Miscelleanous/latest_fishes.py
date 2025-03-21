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
        self.emission_colour = self.principled_BSDF.inputs[26]
        self.emission_strength = self.principled_BSDF.inputs[27]

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
            
    def add_to_class(self, material_name):
        self.material = bpy.data.materials[material_name]

    def add_Image_Texture(self, image_filepath):
        texImage = self.material.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image = bpy.data.images.load("C:\\Users\\myName\\Downloads\\Textures\\Downloaded\\flooring5.jpg")
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
fish_path = "C:\\Users\\ongxu\\Downloads\\BlenderPython (1)\\BlenderPython\\fishes.blend"
fish = Fish(file_path=fish_path, inner_path="Object", object_name="Fish1")
fish.objectInstance = fish.append()
fish2 = Fish(file_path=fish_path, inner_path="Object", object_name="Fish2")
fish2.objectInstance = fish2.append()
fish3 = Fish(file_path=fish_path, inner_path="Object", object_name="Fish3")
fish3.objectInstance = fish3.append()
# fish4 = Fish(file_path=fish_path, inner_path="Object", object_name="Fish4")
# fish4.objectInstance = fish4.append()

#Import Fish Materials
#with bpy.data.libraries.load(fish_path, link=False) as (data_from, data_to):
#    data_to.materials = data_from.materials


Paths_Rigs_Collection = bpy.ops.collection.create(name = "Paths_and_Rigs")
bpy.context.scene.collection.children.link(bpy.data.collections["Paths_and_Rigs"])
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[-1]
bpy.data.collections["Paths_and_Rigs"].objects.unlink(bpy.data.objects[fish3.object_name])
# fish_path1 =  Fish(file_path="C:\\Users\\thnga\\Desktop\\BlenderPython\\fish_rigs.blend", inner_path="Object", object_name="Fish_Path1")
# fish_path1.append()
fish_rig_path = "C:\\Users\\ongxu\\Downloads\\BlenderPython (1)\\BlenderPython\\fish_rigs.blend"
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

# fish4_Rig = Fish_Rig(file_path=fish_rig_path, inner_path="Object", armature_object_name="Fish_Rig4", new_name="Fish_Rig4")
# fish4_Rig.armature_object = fish3_Rig.append()


# fish_path4 = Follow_Path(object_name="Fish_Path4")
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

# Fish4_Struggle_Instance = Spawn_Duplicate(fish_object_ref_name="Fish4")
# chosenFish = bpy.data.objects[Fish4_Struggle_Instance.fish_object_ref_name]
# worldLocation_X = chosenFish.location.x
# worldLocation_Y = chosenFish.location.y
# worldLocation_Z = chosenFish.location.z
# duplicate_offset = 100
# Fish3_Struggle_Instance.set_Location(worldx=worldLocation_X-duplicate_offset,worldy=worldLocation_Y,worldz=worldLocation_Z)

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

width = 160
height = 80
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
fish_followGlobalYCornerHigh = floorGlobalY + floor.getDimensions()[1]/2
fish_followGlobalYCornerLow = floorGlobalY - floor.getDimensions()[1]/2
fish_followGlobalZ = floorGlobalZ
fish_followStartX,fish_followEndX = floor.getEndSidesXWorldLocation()



left_Offset = -10
right_Offset = -10

fish_Follow1 = CreateFish_Follows("FishFollow1", fish_followStartX, fish_followGlobalY, fish_followGlobalZ)
fish_Follow2 = CreateFish_Follows("FishFollow2", fish_followEndX, fish_followGlobalY, fish_followGlobalZ)
fish_Follow3 = CreateFish_Follows("FishFollow3", fish_followStartX, fish_followGlobalYCornerHigh, fish_followGlobalZ)
fish_Follow4 = CreateFish_Follows("FishFollow4", fish_followEndX, fish_followGlobalYCornerLow, fish_followGlobalZ)
fish_Follow1.scale(value=0.1)
fish_Follow2.scale(value=0.1)
fish_Follow1.animateFish_Follows(startloc=fish_followStartX - left_Offset, endloc=fish_followEndX + right_Offset,startingFrame=1,midframe=300, endingFrame=400,bsetCyclic=True)
fish_Follow2.animateFish_Follows(startloc=fish_followEndX + right_Offset, endloc=fish_followStartX - left_Offset,startingFrame=1,midframe=200, endingFrame=400,bsetCyclic=True)
fish_Follow3.animateFish_Follows(startloc=fish_followStartX - left_Offset, endloc=fish_followEndX + right_Offset,startingFrame=1,midframe=200, endingFrame=400,bsetCyclic=True)
fish_Follow4.animateFish_Follows(startloc=fish_followEndX  + right_Offset, endloc=fish_followStartX - left_Offset,startingFrame=1,midframe=200, endingFrame=400,bsetCyclic=True)


xoffset = 30
yoffset = 30

particleSystemSpawnLocation = (floorGlobalX - floor.getDimensions()[0]/2 + xoffset, floorGlobalY+floor.getDimensions()[1]/2 - yoffset, 0)
particleSystemSpawnLocation2 = (floorGlobalX + floor.getDimensions()[0]/2 - xoffset, floorGlobalY-floor.getDimensions()[1]/2 + yoffset, 0)
fish_spawn = ParticleSystems("Fish_Spawn1",particleSystemSpawnLocation[0],particleSystemSpawnLocation[1],particleSystemSpawnLocation[2])
fish_spawn.create_particle_system_modifier(_RENDERTYPE_ = 'COLLECTION',_INSTANCE_= bpy.context.scene.collection.children["Fish Collection"], _PHYSICSTYPE_ = 'BOIDS',lifespan=100000, spawn_amount=30, particle_size=2.0,particle_mass=0.2)

fish_spawn2 = ParticleSystems("Fish_Spawn2",particleSystemSpawnLocation2[0],particleSystemSpawnLocation2[1], particleSystemSpawnLocation2[2])
fish_spawn2.create_particle_system_modifier(_RENDERTYPE_ = 'COLLECTION',_INSTANCE_= bpy.context.scene.collection.children["Fish Collection"], _PHYSICSTYPE_ = 'BOIDS',lifespan=100000, spawn_amount=30, particle_size=2.0, particle_mass=0.2)

fish_spawn3 = ParticleSystems("Fish_Spawn3",particleSystemSpawnLocation2[0],particleSystemSpawnLocation2[1], particleSystemSpawnLocation2[2])
fish_spawn3.create_particle_system_modifier(_RENDERTYPE_ = 'COLLECTION',_INSTANCE_= bpy.context.scene.collection.children["Fish Collection"], _PHYSICSTYPE_ = 'BOIDS',lifespan=100000, spawn_amount=30, particle_size=2.0, particle_mass=0.2)

fish_spawn4 = ParticleSystems("Fish_Spawn4",particleSystemSpawnLocation2[0],particleSystemSpawnLocation2[1], particleSystemSpawnLocation2[2])
fish_spawn4.create_particle_system_modifier(_RENDERTYPE_ = 'COLLECTION',_INSTANCE_= bpy.context.scene.collection.children["Fish Collection"], _PHYSICSTYPE_ = 'BOIDS',lifespan=100000, spawn_amount=30, particle_size=2.0, particle_mass=0.2)

fish_spawn5 = ParticleSystems("Fish_Spawn5",particleSystemSpawnLocation2[0],particleSystemSpawnLocation2[1], particleSystemSpawnLocation2[2])
fish_spawn5.create_particle_system_modifier(_RENDERTYPE_ = 'COLLECTION',_INSTANCE_= bpy.context.scene.collection.children["Fish Collection"], _PHYSICSTYPE_ = 'BOIDS',lifespan=100000, spawn_amount=30, particle_size=2.0,particle_mass=0.2)

fish_spawn6 = ParticleSystems("Fish_Spawn6",particleSystemSpawnLocation2[0],particleSystemSpawnLocation2[1], particleSystemSpawnLocation2[2])
fish_spawn6.create_particle_system_modifier(_RENDERTYPE_ = 'COLLECTION',_INSTANCE_= bpy.context.scene.collection.children["Fish Collection"], _PHYSICSTYPE_ = 'BOIDS',lifespan=100000, spawn_amount=30, particle_size=2.0, particle_mass=0.2)

# Add Follow Leader Rule

#delete all rules
fish_spawn.DeleteAllRules(bpy.context.copy(),bpy.context,addition=0)
fish_spawn2.DeleteAllRules(bpy.context.copy(), bpy.context,addition=0)
fish_spawn3.DeleteAllRules(bpy.context.copy(), bpy.context,addition=0)
fish_spawn4.DeleteAllRules(bpy.context.copy(), bpy.context,addition=0)
fish_spawn5.DeleteAllRules(bpy.context.copy(), bpy.context,addition=0)
fish_spawn6.DeleteAllRules(bpy.context.copy(), bpy.context,addition=0)

# General functions for six hands
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

fish_spawn3.Add_Rule_Goal(Rule_Type="GOAL", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn3.add_Rule_Separate(Rule_Type="SEPARATE", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn3.add_Rule_Follow_Leader(Rule_Type="FOLLOW_LEADER",context_override=bpy.context.copy(),Bpycontext=bpy.context)
fish_spawn3.changeInteractiveObject(rule_index=2, target=fish_Follow3.Fish_Follow)
fish_spawn3.add_Rule_Separate(Rule_Type="AVOID_COLLISION", context_override=bpy.context.copy(), Bpycontext=bpy.context)

fish_spawn4.Add_Rule_Goal(Rule_Type="GOAL", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn4.add_Rule_Separate(Rule_Type="SEPARATE", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn4.add_Rule_Follow_Leader(Rule_Type="FOLLOW_LEADER",context_override=bpy.context.copy(),Bpycontext=bpy.context)
fish_spawn4.changeInteractiveObject(rule_index=2, target=fish_Follow3.Fish_Follow)
fish_spawn4.add_Rule_Separate(Rule_Type="AVOID_COLLISION", context_override=bpy.context.copy(), Bpycontext=bpy.context)

fish_spawn5.Add_Rule_Goal(Rule_Type="GOAL", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn5.add_Rule_Separate(Rule_Type="SEPARATE", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn5.add_Rule_Follow_Leader(Rule_Type="FOLLOW_LEADER",context_override=bpy.context.copy(),Bpycontext=bpy.context)
fish_spawn5.changeInteractiveObject(rule_index=2, target=fish_Follow4.Fish_Follow)
fish_spawn5.add_Rule_Separate(Rule_Type="AVOID_COLLISION", context_override=bpy.context.copy(), Bpycontext=bpy.context)

fish_spawn6.Add_Rule_Goal(Rule_Type="GOAL", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn6.add_Rule_Separate(Rule_Type="SEPARATE", context_override=bpy.context.copy(), Bpycontext=bpy.context)
fish_spawn6.add_Rule_Follow_Leader(Rule_Type="FOLLOW_LEADER",context_override=bpy.context.copy(),Bpycontext=bpy.context)
fish_spawn6.changeInteractiveObject(rule_index=2, target=fish_Follow4.Fish_Follow)
fish_spawn6.add_Rule_Separate(Rule_Type="AVOID_COLLISION", context_override=bpy.context.copy(), Bpycontext=bpy.context)

fish_spawns = [fish_spawn, fish_spawn2, fish_spawn3, fish_spawn4, fish_spawn5, fish_spawn6]


fishMaterial_1 = CreateMaterial(name="FishMaterial")
fishMaterial_2 = CreateMaterial(name="FishMaterial2")
fishMaterial_3 = CreateMaterial(name="FishMaterial3")
fishMaterial_1.assign_To_Object(object_name=fish.get_name())
fishMaterial_2.assign_To_Object(object_name=fish2.get_name())
fishMaterial_3.assign_To_Object(object_name=fish3.get_name())

fishMaterial_1.set_Default_Material_Colour(RGBVal=(0.109, 0.800, 0.105,1.00))
fishMaterial_2.set_Default_Material_Colour(RGBVal=(0.713, 0.802, 0.800,1.00))
fishMaterial_3.set_Default_Material_Colour(RGBVal=(0.800, 0.556, 0.105,1.00))

fishMaterial_1.emission_colour.default_value = (0.109, 0.800, 0.105,1.00)
fishMaterial_2.emission_colour.default_value = (0.713, 0.802, 0.800,1.00)
fishMaterial_3.emission_colour.default_value = (0.800, 0.556, 0.105,1.00)

fishMaterial_1.emission_strength.default_value = 1.0
fishMaterial_2.emission_strength.default_value = 1.0
fishMaterial_3.emission_strength.default_value = 1.0
# fishMaterial_4.set_Default_Material_Colour(RGBVal=(0.800, 0.556, 0.105,1.00))

'''
bpy.ops.wm.append(
    filepath=os.path.join(file_path, inner_path, material_name),
    directory=os.path.join(file_path, inner_path),
    filename=material_name
    )
    
file_path =  fish_path  # blend file name
inner_path = 'Material'   # type 
material_name = 'fishshader2' # name

bpy.ops.wm.append(
    filepath=os.path.join(file_path, inner_path, material_name),
    directory=os.path.join(file_path, inner_path),
    filename=material_name
    )

file_path =  fish_path  # blend file name
inner_path = 'Material'   # type 
material_name = 'fishshader3' # name

bpy.ops.wm.append(
    filepath=os.path.join(file_path, inner_path, material_name),
    directory=os.path.join(file_path, inner_path),
    filename=material_name
    )
    
fish_shader1 = CreateMaterial(name="fishshader")
fish_shader2 = CreateMaterial(name="fishshader2")
fish_shader3 = CreateMaterial(name="fishshader3")

fish_shader1.assign_To_Object(object_name=fish.get_name())
fish_shader1.assign_To_Object(object_name=fish2.get_name())
fish_shader1.assign_To_Object(object_name=fish3.get_name())
'''

#Create the Floor Material

floorMaterial = CreateMaterial(name= "FloorMaterial")
floorMaterial.assign_To_Object(object_name=floor.get_obj_name())
floorMaterial.set_Default_Material_Colour(RGBVal=(0,0,0,0))

cubematerial = CreateMaterial(name="CubeMat")
cubematerial.assign_To_Object(object_name="Cube")

floorplaneat = CreateMaterial(name="planeMat")
cubematerial.set_Default_Material_Colour(RGBVal=(1.0,0.089,0.058,1.0))
floorplaneat.set_Default_Material_Colour(RGBVal=(0,0,0,1))
floorplaneat.assign_To_Object(object_name="background")

lovefishmat1 = CreateMaterial(name="lovefish_mat")
lovefishmat2 = CreateMaterial(name="lovefish_mat")
lovefishmat3 = CreateMaterial(name="lovefish_mat")

lovefishmat1.set_Default_Material_Colour(RGBVal=(.80,.111,.745,1.0))
lovefishmat2.set_Default_Material_Colour(RGBVal=(.364,.163,.80,1.0))
lovefishmat3.set_Default_Material_Colour(RGBVal=(.80,.085,.151,1.0))

lovefishmat1.assign_To_Object(object_name="Fish1 Copy")
lovefishmat2.assign_To_Object(object_name="Fish2 Copy")
lovefishmat2.assign_To_Object(object_name="Fish3 Copy")

#assign emission
lovefishmat1.emission_colour.default_value = (.80,.111,.745,1.0)
lovefishmat1.emission_strength.default_value = 3.0

lovefishmat2.emission_colour.default_value = (.364,.163,.80,1.0)
lovefishmat2.emission_strength.default_value = 3.0

lovefishmat3.emission_colour.default_value = (.80,.085,.151,1.0)
lovefishmat3.emission_strength.default_value = 3.0



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
    path_eval_value += (sce.frame_current-sce.frame_current+10)/fps
    if path_eval_value == 100:
        path_eval_value = 0
    nurbs_path_ref.eval_time = path_eval_value

import time

from pathlib import Path
coor_path = 'C:\\Users\\ongxu\\OneDrive\\Documents\\coding\\projects\\python_projects\\flock\\coords.txt'
f = Path(bpy.path.abspath(coor_path))
# plane = bpy.data.objects["Plane"]
#cube = bpy.data.objects["Cxxube"]
bHasStrugglingFish = False


from typing import Literal, List

class Hand:

    timer_duration = 5

    def __init__(self, hand_index):
        '''
        love_ing (bool): in love fish animation
        left_love_gestur_ing (bool): user making left love gesture
        right_love_gestur_ing (bool): user making right love gesture
        '''
        self.fish_spawn = fish_spawns[hand_index] # TO BE CHANGED
        self.food = None

        self.food_ing = False
        self.food_timer = time.time()

        self.struggle_ing = False
        self.struggle_timer = time.time()

        self.attract_ing = False
        self.attract_timer = time.time()

        self.love_ing = False
        self.love_timer = time.time()

        self.left_love_gesture_ing = False
        self.right_love_gesture_ing = False

        self.x = -100
        self.y = -100
        self.chosen_this_round = False
        self.chosen_last_round = False
        self.same_pos_timer = time.time()
        
        self.hand_index = hand_index
        bpy.ops.mesh.primitive_cube_add(location = (0, 0, 20))
        bpy.context.active_object.name = f'Hand {hand_index}'
        self.cube: bpy.types.Object = bpy.data.objects[f'Hand {hand_index}']
        self.cubematerial = CreateMaterial(name=f'{self.cube.name} material')
        self.cubematerial.assign_To_Object(object_name=self.cube.name)

    def update(self, gestures: List[bool]):
        '''
        gestures[0]: give_food
        gestures[1]: struggle
        gestures[2]: attract
        gestures[3]: left_love
        gestures[4]: right_love
        '''
        
        self.cube.select_set(True)
        self.cube.location.x = self.x
        self.cube.location.y = self.y
        self.cube.select_set(False)

        self.left_love_gesture_ing = gestures[3]
        self.right_love_gesture_ing = gestures[4]

        self.give_food(gestures[0])
        self.struggle(gestures[1])
        self.attract(gestures[2])
        self.love(gestures[3], gestures[4])
    
    def give_food(self, execute_gesture):
        if self.food_ing and time.time() - self.food_timer > self.timer_duration:
            if f'food {self.hand_index}' in bpy.data.objects:
                bpy.ops.object.select_all(action="DESELECT")
                bpy.data.objects[f'food {self.hand_index}'].select_set(True)
                bpy.ops.object.delete()
            self.fish_spawn.changeInteractiveObject(rule_index = 0, target = None)
            self.food_ing = False

        if execute_gesture and not self.food_ing:
            self.food_timer = time.time()
            self.food_ing = True
            self.food = Food(f'food {self.hand_index}', self.x, self.y, 0)
            self.fish_spawn.changeInteractiveObject(rule_index = 0, target = self.food.food)

    def struggle(self, execute_gesture):
        pass

    def attract(self, execute_gesture):
        if self.attract_ing and time.time() - self.attract_timer > self.timer_duration:
            self.fish_spawn.changeInteractiveObject(rule_index=0,target=None)
            self.cubematerial.set_Default_Material_Colour(RGBVal=(1.0,0.089,0.058,1.0))
            self.attract_ing = False
        
        if execute_gesture and not self.attract_ing:
            self.attract_timer = time.time()
            self.fish_spawn.changeInteractiveObject(rule_index=0,target=self.cube)
            self.cubematerial.set_Default_Material_Colour(RGBVal=(1.0,0.089,0.700,1.0))
            self.attract_ing = True

    def love(self, left_love, right_love):
        #global bHasStrugglingFish
        global chosenIndex, path_eval_value
        if self.love_ing and time.time() - self.love_timer > self.timer_duration:
            #print(f'{self.hand_index} is no more in LOVE! :"(')
            move_struggling_fish_back(_lst_backups=lst_backups,lst_fish=lst_fish_paths)
            self.love_ing = False
            path_eval_value = 0

        if self.love_ing:
            update_curve_evaluation_time(curve_index=chosenIndex-3, fps=60)

        if not self.love_ing:
            for other_hand in hands:
                other_hand: Hand
                if other_hand == self: continue

                in_love = (left_love and other_hand.right_love_gesture_ing and not other_hand.love_ing) or \
                          (right_love and other_hand.left_love_gesture_ing and not other_hand.love_ing)

                if in_love:
                    self.love_timer = time.time()
                    other_hand.love_timer = time.time()
                    other_hand.love_ing = True
                    self.love_ing = True
                    print(f'{self.hand_index} and {other_hand.hand_index} is in LOVE! <3')
                    chosenIndex = random.randint(0,2) 
                    spawn_struggling_fish(userxCoord=self.x, useryCoord=self.y,lst_fish=lst_fish_paths)
                    break

    def get_distance(self, x, y):
        return ( (x-self.x)**2 + (y-self.y)**2 ) ** 0.5

hands : List[Hand] = [Hand(i) for i in range(6)]

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
                rows = list(f.read_text().split('\n'))
                
                user_inputs = []
                for row in rows:
                    if not row: 
                        continue
                    temp = list(map(int, row.split(' ')))
                    user_inputs.append(temp)
                
                for user_input in user_inputs:
                    # print(user_input)
                    user_x = max(user_input[0], 0)
                    user_y = max(user_input[1], 0)
                    giving_food = user_input[2]
                    ok_gesture = user_input[3]
                    point_gesture = user_input[4]
                    love_left = user_input[5]
                    love_right = user_input[6]
#                    cube.location.x = user_x/1400*floor.getDimensions()[0]
#                    cube.location.y = (1-user_y/700)*floor.getDimensions()[1] #marked as flipped (1-user_y/700) originally, (user_y/700) after

                    # Start processing multiple hands here
                    min_distance = float('inf')
                    chosen_hand = None
                    for hand in hands:
                        hand: Hand
                        cur_distance = hand.get_distance(user_x, user_y)
                        if not hand.chosen_this_round and cur_distance < min_distance:
                            min_distance = cur_distance
                            chosen_hand = hand
                    
                    if chosen_hand:
                        chosen_hand.x = user_x/1400*floor.getDimensions()[0]
                        chosen_hand.y = (1-user_y/700)*floor.getDimensions()[1]
                        chosen_hand.chosen_this_round = True
                        # update with gesture states
                        chosen_hand.update([giving_food, ok_gesture, point_gesture, love_left, love_right])

                to_be_removed = [] # list of hands not chosen for > n seconds and to be removed
                for hand in hands:
                    # update without gesture states
                    # without this line the hands will not update when not moved
                    hand.update([0,0,0,0,0])

                    if not hand.chosen_this_round:
                        if hand.chosen_last_round:
                            hand.same_pos_timer = time.time()
                        elif time.time() - hand.same_pos_timer > 2:
                            to_be_removed.append(hand)
                    
                    hand.chosen_last_round = hand.chosen_this_round
                    hand.chosen_this_round = False

                for hand in to_be_removed:
                    # reset to default hand position (out of map)
                    hand.x = -100
                    hand.y = -100

            except Exception as e:
                print(e)
                return {'PASS_THROUGH'}
        
        return {'PASS_THROUGH'}
    
    def stop_playback(self, scene, _):
        # print(format(scene.frame_current) + " / " + format(scene.frame_end))
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

