import creatureNames,newWorldGenerator
from random import randint,choice
from math import ceil


maintainPopulation = 5 #Wenn die Bevölkerung niedriger als der eingegebene Wert ist, werden neue Kreaturen gespawnt



def avg(a,b):
    return (a+b)/2

def random_rotation(rotation):
    if randint(0,100) < 5:
        if bool(randint(0,1)):
            return rotation + 45 #Zufällige Rotation
        else:
            return rotation - 45
        if rotation < 0 or rotation > 315:
            return 0
    return rotation

def newCreature(worldSize=[100,100]):
    bt = randint(100,400)
    col = [randint(0,255),randint(0,255),randint(0,255)]
    bnds = [255,255,255] if int(sum(col)/3) < 128 else [0,0,0]
    return {"name":creatureNames.continueName(creatureNames.continueName(creatureNames.continueName(creatureNames.continueName(creatureNames.newName())))),"energy":100,"parent":"None","x":randint(0,worldSize[0]-1),"reproduceTime":10,"rotation":choice([0,45,90,135,180,225,270,315]),"y":randint(0,worldSize[1]-1),"movementX":0,"movementY":0,"generation":0,"color":col,"boundaries":bnds,"age":0,"attributes":{"birthTreshold":bt,"birthEnergy":bt // 2,"eatState":randint(1,1000),"fleeState":randint(1,2),"walkSpeed":randint(1,5),"eatSpeed":randint(1,5),"fleeSpeed":randint(5,10),"avoidsWater":not bool(randint(0,100))}}

def initWorld(worldSizeX,worldSizeY, worldGeneration="new",smooth=8):
    return newWorldGenerator.makeWorld(worldSizeX,worldSizeY,smooth)


def createChildOf(creature):
    newCreature = creature.copy()
    newCreature["attributes"]["avoidsWater"] = not newCreature["attributes"]["avoidsWater"] if not bool(randint(0,100)) else newCreature["attributes"]["avoidsWater"]
    newCreature["parent"] = newCreature["name"][:]
    newCreature["name"] = creatureNames.alterName(newCreature["name"])
    newCreature["age"] = 0
    newCreature["rotation"] = choice([0,45,90,135,180,225,270,315])
    newCreature["generation"] += 1
    newCreature["attributes"]["birthTreshold"] = randint(100,400)
    newCreature["attributes"]["eatState"] += randint(-10,10) if (newCreature["attributes"]["eatState"] < 1000 and newCreature["attributes"]["eatState"] > 10) else randint(-10,0) if newCreature["attributes"]["eatState"] > 1000 else randint(0,10)
    if newCreature["attributes"]["walkSpeed"] in range(2,5):
        newCreature["attributes"]["walkSpeed"] += randint(-1,1)
    elif newCreature["attributes"]["walkSpeed"] == 1:
        newCreature["attributes"]["walkSpeed"] += randint(0,1)
    else:
        newCreature["attributes"]["walkSpeed"] -= randint(0,1)
    if newCreature["attributes"]["eatSpeed"] in range(2,5):
        newCreature["attributes"]["eatSpeed"] += randint(-1,1)
    elif newCreature["attributes"]["eatSpeed"] == 1:
        newCreature["attributes"]["eatSpeed"] += randint(0,1)
    else:
        newCreature["attributes"]["eatSpeed"] -= randint(0,1)
    if newCreature["attributes"]["fleeSpeed"] in range(6,10):
        newCreature["attributes"]["fleeSpeed"] += randint(-1,1)
    elif newCreature["attributes"]["fleeSpeed"] == 5:
        newCreature["attributes"]["fleeSpeed"] += randint(0,1)
    else:
        newCreature["attributes"]["fleeSpeed"] -= randint(0,1)
    newCreature["energy"] = newCreature["attributes"]["birthEnergy"]
    newCreature["attributes"]["birthEnergy"] = newCreature["attributes"]["birthTreshold"] // 2
    return newCreature
    
    

def initCreatures(count,worldSize=[100,100]):
    creatures:list = []
    for i in range(count):
        creatures += [newCreature(worldSize)]
    return creatures

def runIteration(creatures,world):
    #KREATURITERATION
    for creature in range(len(creatures)):
        if not "realFleeSpeed" in creatures[creature]["attributes"]:
            creatures[creature]["attributes"]["realFleeSpeed"] = creatures[creature]["attributes"]["fleeSpeed"]/15
            creatures[creature]["attributes"]["realWalkSpeed"] = creatures[creature]["attributes"]["walkSpeed"]/15
            creatures[creature]["attributes"]["realEatSpeed"] = creatures[creature]["attributes"]["eatSpeed"]/15

            
            
        creatures[creature]["age"] += 1 #Alter in Iterationen erhöhen
        creatures[creature]["reproduceTime"] -= 1 if creatures[creature]["reproduceTime"] > 0 else 0
        if creatures[creature]["attributes"]["fleeState"] == 1 and not world[0][int(creatures[creature]["x"])][int(creatures[creature]["y"])]:
            try:
                if creatures[creature]["attributes"]["avoidsWater"]:
                    #Alle Rotationsrichtungen nach bewohnbarem Land absuchen
                    if world[0][int(creatures[creature]["x"])][int(creatures[creature]["y"]-1)]:
                        creatures[creature]["rotation"] = 0
                    elif world[0][int(creatures[creature]["x"]+1)][int(creatures[creature]["y"]-1)]:
                        creatures[creature]["rotation"] = 45
                    elif world[0][int(creatures[creature]["x"]+1)][int(creatures[creature]["y"])]:
                        creatures[creature]["rotation"] = 90
                    elif world[0][int(creatures[creature]["x"]+1)][int(creatures[creature]["y"]+1)]:
                        creatures[creature]["rotation"] = 135
                    elif world[0][int(creatures[creature]["x"])][int(creatures[creature]["y"]+1)]:
                        creatures[creature]["rotation"] = 180
                    elif world[0][int(creatures[creature]["x"]-1)][int(creatures[creature]["y"]+1)]:
                        creatures[creature]["rotation"] = 225
                    elif world[0][int(creatures[creature]["x"]-1)][int(creatures[creature]["y"])]:
                        creatures[creature]["rotation"] = 270
                    elif world[0][int(creatures[creature]["x"]-1)][int(creatures[creature]["y"]-1)]:
                        creatures[creature]["rotation"] = 315
                    else:
                        creatures[creature]["rotation"] = random_rotation(creatures[creature]["rotation"])
                else:
                    creatures[creature]["rotation"] = random_rotation(creatures[creature]["rotation"])
                
            except:
                creatures[creature]["rotation"] = random_rotation(creatures[creature]["rotation"])
            
            if creatures[creature]["rotation"] in range(0,45) or creatures[creature]["rotation"] in range(314,360):
                creatures[creature]["movementY"] = (-creatures[creature]["attributes"]["realFleeSpeed"] + creatures[creature]["movementY"]*7)/8
                #creatures[creature]["y"] -= creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(134,226):
                creatures[creature]["movementY"] = (creatures[creature]["attributes"]["realFleeSpeed"] + creatures[creature]["movementY"]*7)/8 
                #creatures[creature]["y"] += creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(44,136):
                creatures[creature]["movementX"] = (creatures[creature]["attributes"]["realFleeSpeed"] + creatures[creature]["movementX"]*7)/8 
                #creatures[creature]["x"] += creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(224,316):
                creatures[creature]["movementX"] = (-creatures[creature]["attributes"]["realFleeSpeed"] + creatures[creature]["movementX"]*7)/8 
                #creatures[creature]["x"] -= creatures[creature]["attributes"]["realFleeSpeed"]
            creatures[creature]["energy"] -= ceil(creatures[creature]["attributes"]["fleeSpeed"]/3)
            #Bewegung nach Rotation und Geschwindigkeit
            #FleeStateReal
        elif creatures[creature]["attributes"]["fleeState"] == 2 and world[0][int(creatures[creature]["x"])][int(creatures[creature]["y"])]:
            creatures[creature]["rotation"] = random_rotation(creatures[creature]["rotation"])
            
            if creatures[creature]["rotation"] in range(0,45) or creatures[creature]["rotation"] in range(314,360):
                creatures[creature]["movementY"] = (-creatures[creature]["attributes"]["realFleeSpeed"] + creatures[creature]["movementY"]*7)/8
                #creatures[creature]["y"] -= creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(134,226):
                creatures[creature]["movementY"] = (creatures[creature]["attributes"]["realFleeSpeed"] + creatures[creature]["movementY"]*7)/8
                #creatures[creature]["y"] += creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(44,136):
                creatures[creature]["movementX"] = (creatures[creature]["attributes"]["realFleeSpeed"] + creatures[creature]["movementX"]*7)/8 
                #creatures[creature]["x"] += creatures[creature]["attributes"]["realFleeSpeed"]
            if creatures[creature]["rotation"] in range(224,316):
                creatures[creature]["movementX"] = (-creatures[creature]["attributes"]["realFleeSpeed"] + creatures[creature]["movementX"]*7)/8
                #creatures[creature]["x"] -= creatures[creature]["attributes"]["realFleeSpeed"]
            creatures[creature]["energy"] -= ceil(creatures[creature]["attributes"]["fleeSpeed"]/2)
            #Bewegung nach Rotation und Geschwindigkeit
            #FleeStateFake
        elif creatures[creature]["energy"]+randint(-150,50) < creatures[creature]["attributes"]["eatState"]:
            if world[1][int(creatures[creature]["x"])][int(creatures[creature]["y"])] > 1:
                #Essen, wenn mindestens eine Energieeinheit im Boden verfügbar
                world[1][int(creatures[creature]["x"])][int(creatures[creature]["y"])] -= 1
                creatures[creature]["energy"] += 7 #Essen pro Energieeinheit


            creatures[creature]["rotation"] = random_rotation(creatures[creature]["rotation"])
            
            
            if creatures[creature]["rotation"] in range(0,45) or creatures[creature]["rotation"] in range(314,360):
                creatures[creature]["movementY"] = (-creatures[creature]["attributes"]["realEatSpeed"] + creatures[creature]["movementY"]*7)/8
                #creatures[creature]["y"] -= creatures[creature]["attributes"]["realEatSpeed"]
            if creatures[creature]["rotation"] in range(134,226):
                creatures[creature]["movementY"] = (creatures[creature]["attributes"]["realEatSpeed"] + creatures[creature]["movementY"]*7)/8
                #creatures[creature]["y"] += creatures[creature]["attributes"]["realEatSpeed"]
            if creatures[creature]["rotation"] in range(44,136):
                creatures[creature]["movementX"] = (creatures[creature]["attributes"]["realEatSpeed"] + creatures[creature]["movementX"]*7)/8
                #creatures[creature]["x"] += creatures[creature]["attributes"]["realEatSpeed"]
            if creatures[creature]["rotation"] in range(224,316):
                creatures[creature]["movementX"] = (-creatures[creature]["attributes"]["realEatSpeed"] + creatures[creature]["movementX"]*7)/8 
                #creatures[creature]["x"] -= creatures[creature]["attributes"]["realEatSpeed"]
            #Bewegung nach Rotation und Geschwindigkeit

            creatures[creature]["energy"] -= ceil(creatures[creature]["attributes"]["eatSpeed"]/2)
            #EatState
        else:
            #WalkState
            creatures[creature]["rotation"] = random_rotation(creatures[creature]["rotation"])
            
            
            if creatures[creature]["rotation"] in range(0,45) or creatures[creature]["rotation"] in range(314,360):
                creatures[creature]["movementY"] = (-creatures[creature]["attributes"]["realWalkSpeed"] + creatures[creature]["movementY"]*7)/8
                #creatures[creature]["y"] -= creatures[creature]["attributes"]["realWalkSpeed"]
            if creatures[creature]["rotation"] in range(134,226):
                creatures[creature]["movementY"] = (creatures[creature]["attributes"]["realWalkSpeed"] + creatures[creature]["movementY"]*7)/8 
                #creatures[creature]["y"] += creatures[creature]["attributes"]["realWalkSpeed"]
            if creatures[creature]["rotation"] in range(44,136):
                creatures[creature]["movementX"] = (creatures[creature]["attributes"]["realWalkSpeed"] + creatures[creature]["movementX"]*7)/8 
                #creatures[creature]["x"] += creatures[creature]["attributes"]["realWalkSpeed"]
            if creatures[creature]["rotation"] in range(224,316):
                creatures[creature]["movementX"] = (-creatures[creature]["attributes"]["realWalkSpeed"] + creatures[creature]["movementX"]*7)/8 
                #creatures[creature]["x"] -= creatures[creature]["attributes"]["realWalkSpeed"]

            creatures[creature]["energy"] -= ceil(creatures[creature]["attributes"]["walkSpeed"]/2)
            
            
            if creatures[creature]["energy"] > creatures[creature]["attributes"]["birthTreshold"] and creatures[creature]["reproduceTime"] <= 0:
                creatures[creature]["energy"] -= creatures[creature]["attributes"]["birthEnergy"]
                if bool(randint(0,1)):
                    creatures+=[createChildOf(creatures[creature])]
                    creatures[creature]["reproduceTime"] = 60
                    #print("Reproduction")
        
        creatures[creature]["x"] += creatures[creature]["movementX"]
        creatures[creature]["y"] += creatures[creature]["movementY"]
        
        if creatures[creature]["rotation"] not in range(0,316):
            creatures[creature]["rotation"] = 0
            
        if creatures[creature]["x"]+1 > len(world[0]) or creatures[creature]["x"]-1 < 0:
            creatures[creature]["x"] = 1
            creatures[creature]["rotation"] = random_rotation(creatures[creature]["rotation"]) #Verhindern, dass Kreaturen sich außerhalb der x-Koordinaten der Welt bewegen
        if creatures[creature]["y"]+1 > len(world[0][0]) or creatures[creature]["y"]-1 < 0:
            creatures[creature]["y"] = 1 #Verhindern, dass Kreaturen sich außerhalb der y-Koordinaten der Welt bewegen
            creatures[creature]["rotation"] = random_rotation(creatures[creature]["rotation"]) #TODO: Kreaturen nicht immer an x/y = 1 teleportieren, sondern sie an die Grenzen stoßen lassen
        
        if not world[0][int(creatures[creature]["x"])][int(creatures[creature]["y"])]:
            creatures[creature]["energy"] -= ceil(creatures[creature]["energy"] / 100)
    creature = 0
    while creature < len(creatures):
        if creatures[creature]["energy"] < 0:
            del creatures[creature]
            creature -= 1
        creature += 1
    if maintainPopulation > len(creatures) or (randint(0,1000) == 420 and randint(0,100) == 69):
        creatures += [newCreature()]
    return [creatures,world]


def runWorldIteration(world):
                    
    #WELTITERATION
            
    for x in range(len(world[1])):
        for y in range(len(world[1][x])):
            if world[0][x][y] and world[1][x][y] < 10:
                world[1][x][y] = round(world[1][x][y] + 0.2,1)
                
    #print(time()-t)
    return world
