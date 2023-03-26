
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
import os
import glob

# open part module
Mdb()
a = mdb.models['Model-1'].rootAssembly
mdb.ModelFromInputFile(name='X5_3blade', inputFileName='X5_3blade.inp')
p = mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER']

# import layup file X5_3blade_ply_X.txt
region = []
thick = []
orientation = []
density = []

with open('X5_3blade_ply_X.txt', 'r') as file:

    for i in range(1, 7):
        line = file.readline().strip()
        if not line.startswith('#'):
            words = line.split()
            region.append(str('Q' + words[0]))
            thick.append(round(float(words[1]), 3))
            orientation.append(round(float(words[2]), 1))
    
    for i in range(7, 13):
        line = file.readline().strip()
        if not line.startswith('#'):
            words = line.split()
            region.append(str('L' + words[0]))
            thick.append(round(float(words[1]), 3))
            orientation.append(round(float(words[2]), 1))
    
    for i in range(13, 19):
        line = file.readline().strip()
        if not line.startswith('#'):
            words = line.split()
            region.append(str('H' + words[0]))
            thick.append(round(float(words[1]), 3))
            orientation.append(round(float(words[2]), 1))

    for i in range(19, 30):
        line = file.readline().strip()
        if not line.startswith('#'):
            words = line.split()
            thick.append(round(float(words[1]), 3))
            orientation.append(round(float(words[2]), 1))

    for i in range(30, 41):
        line = file.readline().strip()
        if not line.startswith('#'):
            words = line.split()
            thick.append(round(float(words[1]), 3))
            orientation.append(round(float(words[2]), 1))


# delete section define
del mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER'].sectionAssignments[4]
del mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER'].sectionAssignments[3]
del mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER'].sectionAssignments[2]
del mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER'].sectionAssignments[1]
del mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER'].sectionAssignments[0]

#delete section assignment
del mdb.models['X5_3blade'].sections['Section-1-COMPOSITELAYUP-3-5']
del mdb.models['X5_3blade'].sections['Section-2-COMPOSITELAYUP-3-4']
del mdb.models['X5_3blade'].sections['Section-3-COMPOSITELAYUP-3-2']
del mdb.models['X5_3blade'].sections['Section-4-COMPOSITELAYUP-3-3']
del mdb.models['X5_3blade'].sections['Section-5-COMPOSITELAYUP-3-1']

# composite layup
layupOrientation = None

region_skin=p.sets['SKIN']
region_tip=p.sets['TIP']
region_lei1=p.sets['LEI1']
region_lei2=p.sets['LEI2']

# parameter set[X] qianbu
region0=p.sets[region[0]]
region1=p.sets[region[1]]
region2=p.sets[region[2]]
region3=p.sets[region[3]]
region4=p.sets[region[4]]

# parameter set[X] zhongbu
region5=p.sets[region[5]]
region6=p.sets[region[6]]
region7=p.sets[region[7]]
region8=p.sets[region[8]]
region9=p.sets[region[9]]

# parameter set[X] houbu
region10=p.sets[region[10]]
region11=p.sets[region[11]]
region12=p.sets[region[12]]
region13=p.sets[region[13]]
region14=p.sets[region[14]]

# generate composite shell, skin
p = mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER']
p.DatumCsysByThreePoints(name='Datum csys-1', coordSysType=CARTESIAN, origin=(
    0.0, 0.0, 0.0), point1=(0.0, 1.0, 0.0), point2=(1.0, 1.0, 0.0))
layupOrientation = None
plySystem1 = mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER'].datums[131]
compositeLayup = mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER'].CompositeLayup(
    name='CompositeLayup-3', description='', elementType=SHELL, 
    offsetType=BOTTOM_SURFACE, symmetric=False, 
    thicknessAssignment=FROM_SECTION)
compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON, 
    thicknessType=UNIFORM, poissonDefinition=DEFAULT, temperature=GRADIENT, 
    useDensity=OFF)
compositeLayup.ReferenceOrientation(orientationType=GLOBAL, localCsys=None, 
    fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, axis=AXIS_3)

## skin
compositeLayup.CompositePly(suppressed=False, plyName='P1', region=region_skin, 
    material='T300_TEX', thicknessType=SPECIFY_THICKNESS, thickness=0.2, 
    orientationType=CSYS, orientation=plySystem1, axis=AXIS_3, angle=0.0, 
    additionalRotationField='', additionalRotationType=ROTATION_NONE, 
    numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P2', region=region_skin, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=0.15, 
    orientationType=CSYS, orientation=plySystem1, axis=AXIS_3, angle=45.0, 
    additionalRotationField='', additionalRotationType=ROTATION_NONE, 
    numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P3', region=region_skin, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=0.15, 
    orientationType=CSYS, orientation=plySystem1, axis=AXIS_3, angle=90.0, 
    additionalRotationField='', additionalRotationType=ROTATION_NONE, 
    numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P4', region=region_skin, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=0.15, 
    orientationType=CSYS, orientation=plySystem1, axis=AXIS_3, angle=0.0, 
    additionalRotationField='', additionalRotationType=ROTATION_NONE, 
    numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P5', region=region_skin, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=0.15, 
    orientationType=CSYS, orientation=plySystem1, axis=AXIS_3, angle=0.0, 
    additionalRotationField='', additionalRotationType=ROTATION_NONE, 
    numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P6', region=region_skin, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=0.15, 
    orientationType=CSYS, orientation=plySystem1, axis=AXIS_3, angle=90.0, 
    additionalRotationField='', additionalRotationType=ROTATION_NONE, 
    numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P7', region=region_skin, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=0.15, 
    orientationType=CSYS, orientation=plySystem1, axis=AXIS_3, angle=-45.0, 
    additionalRotationField='', additionalRotationType=ROTATION_NONE, 
    numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P8', region=region_skin, 
    material='T300_TEX', thicknessType=SPECIFY_THICKNESS, thickness=0.15, 
    orientationType=CSYS, orientation=plySystem1, axis=AXIS_3, angle=0.0, 
    additionalRotationField='', additionalRotationType=ROTATION_NONE, 
    numIntPoints=3)

## qianbu, optimize
compositeLayup.CompositePly(suppressed=False, plyName='P9', region=region0, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[0], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[0], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P10', region=region1, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[1], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[1], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P11', region=region2, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[2], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[2], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P12', region=region3, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[3], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[3], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P13', region=region4, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[4], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[4], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)

## zhongbu, optimize
compositeLayup.CompositePly(suppressed=False, plyName='P14', region=region5, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[5], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[5], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P15', region=region6, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[6], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[6], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P16', region=region7, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[7], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[7], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P17', region=region8, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[8], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[8], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P18', region=region9, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[9], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[9], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)

## houbu, optimize
compositeLayup.CompositePly(suppressed=False, plyName='P19', region=region10, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[10], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[10], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P20', region=region11, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[11], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[11],  
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P21', region=region12, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[12], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[12], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P22', region=region13, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[13], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[13], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P23', region=region14, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[14], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[14], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)

## tip
compositeLayup.CompositePly(suppressed=False, plyName='P24', region=region_tip, 
    material='T300_TEX', thicknessType=SPECIFY_THICKNESS, thickness=0.2, 
    orientationType=CSYS, orientation=plySystem1, axis=AXIS_3, angle=0.0, 
    additionalRotationField='', additionalRotationType=ROTATION_NONE, 
    numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P25', region=region_tip, 
    material='T300_TEX', thicknessType=SPECIFY_THICKNESS, thickness=0.2, 
    orientationType=CSYS, orientation=plySystem1, axis=AXIS_3, angle=0.0, 
    additionalRotationField='', additionalRotationType=ROTATION_NONE, 
    numIntPoints=3)

p = mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER']

# creat composite layup, lei
del mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER'].compositeLayups['COMPOSITELAYUP-1']
del mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER'].compositeLayups['COMPOSITELAYUP-2']

## creat coordinate system
p.DatumCsysByThreePoints(name='Datum csys-2', coordSysType=CARTESIAN, origin=(
    0.0, 0.0, 0.0), point1=(0.0, 1.0, 0.0), point2=(0.0, 1.0, 1.0))
layupOrientation = None
plySystem1 = mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER'].datums[132]
compositeLayup = mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER'].CompositeLayup(
    name='CompositeLayup-1', description='', elementType=SHELL, 
    offsetType=MIDDLE_SURFACE, symmetric=False, 
    thicknessAssignment=FROM_SECTION)
compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON, 
    thicknessType=UNIFORM, poissonDefinition=DEFAULT, temperature=GRADIENT, 
    useDensity=OFF)
compositeLayup.ReferenceOrientation(orientationType=GLOBAL, localCsys=None, 
    fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, axis=AXIS_3)

## lei1
compositeLayup.CompositePly(suppressed=False, plyName='P1', region=region_lei1, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[15], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[15], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P2', region=region_lei1, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[16], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[16], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P3', region=region_lei1, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[17], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[17], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P4', region=region_lei1, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[18], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[18], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P5', region=region_lei1, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[19], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[19], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P6', region=region_lei1, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[20], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[20], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P7', region=region_lei1, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[21], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[21], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P8', region=region_lei1, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[22], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[22], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P9', region=region_lei1, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[23], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[23], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P10', region=region_lei1, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[24], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[24], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)

## lei2
compositeLayup.CompositePly(suppressed=False, plyName='P11', region=region_lei2, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[25], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[25], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P12', region=region_lei2, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[26], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[26], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P13', region=region_lei2, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[27], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[27], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P14', region=region_lei2, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[28], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[28], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P15', region=region_lei2, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[29], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[29], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P16', region=region_lei2, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[30], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[30], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P17', region=region_lei2, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[31], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[31], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P18', region=region_lei2, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[32], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[32], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P19', region=region_lei2, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[33], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[33], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)
compositeLayup.CompositePly(suppressed=False, plyName='P20', region=region_lei2, 
    material='T700_DANXIANG', thicknessType=SPECIFY_THICKNESS, thickness=thick[34], 
    orientationType=CSYS, orientation=plySystem1, angle=orientation[34], 
    additionalRotationType=ROTATION_NONE, additionalRotationField='', 
    axis=AXIS_3, numIntPoints=3)

p = mdb.models['X5_3blade'].parts['P168M-3BLADE-V3-HOVER']

## change job define
mdb.models['X5_3blade'].steps['Step-2'].setValues(maxNumInc=10000, 
    initialInc=0.1, minInc=1e-15)
mdb.models['X5_3blade'].steps['Step-3'].setValues(maxNumInc=10000, 
    initialInc=0.1, minInc=1e-15)
mdb.models['X5_3blade'].steps['Step-4'].setValues(maxNumInc=10000, 
    initialInc=0.1, minInc=1e-15)
mdb.models['X5_3blade'].steps['Step-5'].setValues(maxNumInc=10000, 
    initialInc=0.1, minInc=1e-15)
mdb.models['X5_3blade'].steps['Step-7'].setValues(maxNumInc=10000, 
    initialInc=0.1, minInc=1e-15)
mdb.models['X5_3blade'].steps['Step-9'].setValues(maxNumInc=10000, 
    initialInc=0.1, minInc=1e-15)

# open job module
a = mdb.models['X5_3blade'].rootAssembly
a.regenerate()

# creat job
myJob = mdb.Job(name='X5_3blade_cal', model='X5_3blade', description='', 
    type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
    memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4, 
    numDomains=4, numGPUs=0)

# submit job
myJob.submit()
myJob.waitForCompletion()

# open odb
odb = session.openOdb('X5_3blade_cal.odb',readOnly=True)
All = odb.rootAssembly.instances['P168M-3BLADE-V3-HOVER-1'].elementSets['JIANCE']

# flap max_inPlanePrincipal
strainField = odb.steps['Step-2'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_flap = max(inPlanePrincipal)

# lead max_inPlanePrincipal
strainField = odb.steps['Step-3'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_lead = max(inPlanePrincipal)

# torque max_inPlanePrincipal
strainField = odb.steps['Step-4'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_torque = max(inPlanePrincipal)

# max_centrifugal_force max_inPlanePrincipal
strainField = odb.steps['Step-9'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_centrifugal_force = max(inPlanePrincipal)

# max_inPlanePrincipal write to file
with open('poemout.txt', 'w') as f:
    f.write('# stiff_hub_rotate_0deg \n')
    f.write('## load: 2739.2N 400N 60N.m 2215RPM\n')
    f.write(str(max_inPlanePrincipal_flap) + '\n')
    f.write(str(max_inPlanePrincipal_lead) + '\n')
    f.write(str(max_inPlanePrincipal_torque) + '\n')
    f.write(str(max_centrifugal_force) + '\n')

# modal frequency 0rpm
step = odb.steps['Step-6']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 0rpm\n')
for t in frames:
    f.write('%10.5s\n' % (t.frequency)) 
f.close()

# modal frequency 1107.5rpm
step = odb.steps['Step-8']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 1107.50rpm\n')
for t in frames:
    modal_freq = t.frequency / 18.46
    f.write('%10.5s %10.5s\n' % (t.frequency, modal_freq)) 
f.close()

# modal frequency 2215rpm
step = odb.steps['Step-10']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 2215rpm\n')
for t in frames:
    modal_freq = t.frequency / 36.92
    f.write('%10.5s %10.5s\n' % (t.frequency, modal_freq)) 
f.close()

# write
print('JOB1 COMPLETE')

# job2 rotate instance
mdb.ModelFromInputFile(name='X5_3blade_cal_rotate10',inputFileName='X5_3blade_cal.inp')
a = mdb.models['X5_3blade_cal_rotate10'].rootAssembly

## rotate 10 deg
a.rotate(instanceList=('P168M-3BLADE-V3-HOVER-1', ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 0.01, 0.0), angle=10.0)
## change 2739.2N to 2000N
mdb.models['X5_3blade_cal_rotate10'].loads['CFORCE-1'].setValues(cf3=-2000.0, 
    distributionType=UNIFORM, field='')
## change 400N to 200N
mdb.models['X5_3blade_cal_rotate10'].loads['CFORCE-2'].setValues(cf1=200.0, 
    distributionType=UNIFORM, field='')
## change 60N.m to 40N.m
mdb.models['X5_3blade_cal_rotate10'].loads['CFORCE-3'].setValues(cm1=40000.0, 
    distributionType=UNIFORM, field='')

## open job module
a.regenerate()

## creat job
myJob = mdb.Job(name='X5_3blade_cal_rotate10', model='X5_3blade_cal_rotate10', description='', 
    type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
    memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4, 
    numDomains=4, numGPUs=0)

## submit job
myJob.submit()
myJob.waitForCompletion()

## open odb
odb = session.openOdb('X5_3blade_cal_rotate10.odb',readOnly=True)
All = odb.rootAssembly.instances['P168M-3BLADE-V3-HOVER-1'].elementSets['JIANCE']

# flap max_inPlanePrincipal
strainField = odb.steps['Step-2'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_flap = max(inPlanePrincipal)

# lead max_inPlanePrincipal
strainField = odb.steps['Step-3'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_lead = max(inPlanePrincipal)

# torque max_inPlanePrincipal
strainField = odb.steps['Step-4'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_torque = max(inPlanePrincipal)

# max_centrifugal_force max_inPlanePrincipal
strainField = odb.steps['Step-9'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_centrifugal_force = max(inPlanePrincipal)

# max_inPlanePrincipal write to file
with open('poemout.txt', 'a') as f:
    f.write('# rotate_10deg \n')
    f.write('## load: 2000N 200N 40N.m 2215RPM\n')
    f.write(str(max_inPlanePrincipal_flap) + '\n')
    f.write(str(max_inPlanePrincipal_lead) + '\n')
    f.write(str(max_inPlanePrincipal_torque) + '\n')
    f.write(str(max_centrifugal_force) + '\n')

# modal frequency 0rpm
step = odb.steps['Step-6']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 0rpm\n')
for t in frames:
    f.write('%10.5s\n' % (t.frequency)) 
f.close()

# modal frequency 1107.5rpm
step = odb.steps['Step-8']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 1107.50rpm\n')
for t in frames:
    modal_freq = t.frequency / 18.46
    f.write('%10.5s %10.5s\n' % (t.frequency, modal_freq)) 
f.close()

# modal frequency 2215rpm
step = odb.steps['Step-10']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 2215rpm\n')
for t in frames:
    modal_freq = t.frequency / 36.92
    f.write('%10.5s %10.5s\n' % (t.frequency, modal_freq)) 
f.close()

# write
print('JOB2 COMPLETE')

# job3 rotate instance
mdb.ModelFromInputFile(name='X5_3blade_cal_rotate30',inputFileName='X5_3blade_cal.inp')
a = mdb.models['X5_3blade_cal_rotate30'].rootAssembly

## rotate 10 deg
a.rotate(instanceList=('P168M-3BLADE-V3-HOVER-1', ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 0.01, 0.0), angle=30.0)
## change 2739.2N to 2000N
mdb.models['X5_3blade_cal_rotate30'].loads['CFORCE-1'].setValues(cf3=-2000.0, 
    distributionType=UNIFORM, field='')
## change 400N to 200N
mdb.models['X5_3blade_cal_rotate30'].loads['CFORCE-2'].setValues(cf1=200.0, 
    distributionType=UNIFORM, field='')
## change 60N.m to 40N.m
mdb.models['X5_3blade_cal_rotate30'].loads['CFORCE-3'].setValues(cm1=40000.0, 
    distributionType=UNIFORM, field='')

## open job module
a.regenerate()

## creat job
myJob = mdb.Job(name='X5_3blade_cal_rotate30', model='X5_3blade_cal_rotate30', description='', 
    type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
    memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4, 
    numDomains=4, numGPUs=0)

## submit job
myJob.submit()
myJob.waitForCompletion()

## open odb
odb = session.openOdb('X5_3blade_cal_rotate30.odb',readOnly=True)
All = odb.rootAssembly.instances['P168M-3BLADE-V3-HOVER-1'].elementSets['JIANCE']

# flap max_inPlanePrincipal
strainField = odb.steps['Step-2'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_flap = max(inPlanePrincipal)

# lead max_inPlanePrincipal
strainField = odb.steps['Step-3'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_lead = max(inPlanePrincipal)

# torque max_inPlanePrincipal
strainField = odb.steps['Step-4'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_torque = max(inPlanePrincipal)

# max_centrifugal_force max_inPlanePrincipal
strainField = odb.steps['Step-9'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_centrifugal_force = max(inPlanePrincipal)

# max_inPlanePrincipal write to file
with open('poemout.txt', 'a') as f:
    f.write('# rotate_30deg \n')
    f.write('## load: 2000N 200N 40N.m 2215RPM\n')
    f.write(str(max_inPlanePrincipal_flap) + '\n')
    f.write(str(max_inPlanePrincipal_lead) + '\n')
    f.write(str(max_inPlanePrincipal_torque) + '\n')
    f.write(str(max_centrifugal_force) + '\n')

# modal frequency 0rpm
step = odb.steps['Step-6']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 0rpm\n')
for t in frames:
    f.write('%10.5s\n' % (t.frequency)) 
f.close()

# modal frequency 1107.5rpm
step = odb.steps['Step-8']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 1107.50rpm\n')
for t in frames:
    modal_freq = t.frequency / 18.46
    f.write('%10.5s %10.5s\n' % (t.frequency, modal_freq)) 
f.close()

# modal frequency 2215rpm
step = odb.steps['Step-10']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 2215rpm\n')
for t in frames:
    modal_freq = t.frequency / 36.92
    f.write('%10.5s %10.5s\n' % (t.frequency, modal_freq)) 
f.close()

print('JOB3 COMPLETE')

# job4 rotate instance
mdb.ModelFromInputFile(name='X5_3blade_cal_rotate45',inputFileName='X5_3blade_cal.inp')
a = mdb.models['X5_3blade_cal_rotate45'].rootAssembly

## rotate 45 deg
a.rotate(instanceList=('P168M-3BLADE-V3-HOVER-1', ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 0.01, 0.0), angle=30.0)
## change 2739.2N to 2000N
mdb.models['X5_3blade_cal_rotate45'].loads['CFORCE-1'].setValues(cf3=-2000.0, 
    distributionType=UNIFORM, field='')
## change 400N to 200N
mdb.models['X5_3blade_cal_rotate45'].loads['CFORCE-2'].setValues(cf1=200.0, 
    distributionType=UNIFORM, field='')
## change 60N.m to 40N.m
mdb.models['X5_3blade_cal_rotate45'].loads['CFORCE-3'].setValues(cm1=40000.0, 
    distributionType=UNIFORM, field='')
## change rotation speed to 570 % 700
mdb.models['X5_3blade_cal_rotate45'].loads['CENTRIF-1'].setValues(
    magnitude=59.7)
mdb.models['X5_3blade_cal_rotate45'].loads['CENTRIF-2'].setValues(
    magnitude=73.3)

## open job module
a.regenerate()

## creat job
myJob = mdb.Job(name='X5_3blade_cal_rotate45', model='X5_3blade_cal_rotate45', description='', 
    type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
    memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4, 
    numDomains=4, numGPUs=0)

## submit job
myJob.submit()
myJob.waitForCompletion()

## open odb
odb = session.openOdb('X5_3blade_cal_rotate45.odb',readOnly=True)
All = odb.rootAssembly.instances['P168M-3BLADE-V3-HOVER-1'].elementSets['JIANCE']

# flap max_inPlanePrincipal
strainField = odb.steps['Step-2'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_flap = max(inPlanePrincipal)

# lead max_inPlanePrincipal
strainField = odb.steps['Step-3'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_lead = max(inPlanePrincipal)

# torque max_inPlanePrincipal
strainField = odb.steps['Step-4'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_inPlanePrincipal_torque = max(inPlanePrincipal)

# max_centrifugal_force max_inPlanePrincipal
strainField = odb.steps['Step-9'].frames[-1].fieldOutputs['EE']
field = strainField.getSubset(region=All)
fieldValues = field.values
inPlanePrincipal = []
for i in range(len(fieldValues)):
    temp = fieldValues[i].maxInPlanePrincipal
    inPlanePrincipal.append(temp)
max_centrifugal_force = max(inPlanePrincipal)

# max_inPlanePrincipal write to file
with open('poemout.txt', 'a') as f:
    f.write('# rotate_45deg \n')
    f.write('## load: 2000N 200N 40N.m 2215RPM\n')
    f.write(str(max_inPlanePrincipal_flap) + '\n')
    f.write(str(max_inPlanePrincipal_lead) + '\n')
    f.write(str(max_inPlanePrincipal_torque) + '\n')
    f.write(str(max_centrifugal_force) + '\n')

# modal frequency 570rpm
step = odb.steps['Step-6']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 570rpm\n')
for t in frames:
    modal_freq = t.frequency / 9.5
    f.write('%10.5s %10.5s\n' % (t.frequency, modal_freq)) 
f.close()

# modal frequency 700rpm
step = odb.steps['Step-8']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 700rpm\n')
for t in frames:
    modal_freq = t.frequency / 11.67
    f.write('%10.5s %10.5s\n' % (t.frequency, modal_freq)) 
f.close()

# modal frequency 2215rpm
step = odb.steps['Step-10']
frames = tuple(step.frames)[0:]
f = open('poemout.txt', 'a')
f.write('## 2215rpm\n')
for t in frames:
    modal_freq = t.frequency / 36.92
    f.write('%10.5s %10.5s\n' % (t.frequency, modal_freq)) 
f.close()

print('JOB4 COMPLETE')

# delete odbs
folder_path = '.'

odb_files = glob.glob(os.path.join(folder_path, '*.odb'))

for file_path in odb_files:
    os.remove(file_path)
