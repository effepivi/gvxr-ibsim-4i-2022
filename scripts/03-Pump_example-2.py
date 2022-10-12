import os
import math
import numpy as np # Who does not use Numpy?
from tifffile import imwrite
import matplotlib # To plot images
import matplotlib.pyplot as plt # Plotting
from matplotlib.colors import LogNorm # Look up table
from matplotlib.colors import PowerNorm # Look up table

font = {'family' : 'serif',
         'size'   : 10
       }
matplotlib.rc('font', **font)

from tifffile import imread, imwrite # Write TIFF files

import base64 # Save the visualisation

from gvxrPython3 import gvxr # Simulate X-ray images
from gvxrPython3.utils import saveProjections # Plot the X-ray image in linear, log and power law scales
from gvxrPython3.utils import compareWithGroundTruth # Plot the ground truth, the test image, and the relative error map in %
from gvxrPython3.utils import interactPlotPowerLaw # Plot the X-ray image using a Power law look-up table
from gvxrPython3.utils import visualise # Visualise the 3D environment if k3D is supported

print("Create an OpenGL context")

window_id = 0
opengl_major_version = 4
opengl_minor_version = 5

gvxr.createOpenGLContext(window_id, opengl_major_version, opengl_minor_version)

gvxr.setSourcePosition(0.0 ,-40.0,0.0,"cm")
gvxr.usePointSource()
gvxr.setMonoChromatic(0.5,"MeV",1000)
#gvxr.setMonoChromatic(0.8,"MeV",1000)
#gvxr.setDetectorNumberOfPixels(720,576)
gvxr.setDetectorNumberOfPixels(800,800)
gvxr.setDetectorPixelSize(0.7,0.7,"mm")
gvxr.setDetectorPosition(0.0,30.0,0.0,"cm")
gvxr.setDetectorUpVector(0,0,-1)

parts_list = ["internals","front_flange","rear_flange","housing","roller_bearing"]
part_files = ["input_data/TurboPump/internals.stl",
              #"input_data/TurboPump/coupler.stl",
              "input_data/TurboPump/front_flange.stl",
              "input_data/TurboPump/rear_flange.stl",
              "input_data/TurboPump/housing.stl",
              "input_data/TurboPump/ThrustRollerBearing.stl"]


elements = [12,25,14,24,28,26]
ammounts = [0.12,2.00,1.00,19.0,11.0,66.85]


materials = ["Ti","Al","Al","Fe","Ti"]

for i,name in enumerate(parts_list):
     gvxr.loadMeshFile(name,part_files[i],"mm")
     gvxr.setElement(name, materials[i])
     #gvxr.moveToCentre()
     gvxr.translateNode(name,-1.0,-13.0,-2.5,"cm")
     gvxr.scaleNode(name, 0.5, 0.5, 0.5)
     gvxr.rotateNode(name, -90, 1,0,0)
#gvxr.moveToCentre()
gvxr.displayScene()

# gvxr.setMixture(parts_list[4],elements,ammounts)
# gvxr.setDensity(parts_list[4], 8.0, "g/cm3")

#projections = [];
theta = [];
num_projections = 721
angular_step = 360/num_projections
# Compute the intial X-ray image (zeroth angle) and add it to the list of projections
xray_image = np.array(gvxr.computeXRayImage()).astype(np.single)
imwrite('output_data/pump_scan/03-Pump_0.tiff',xray_image)
# Update the 3D visualisation
gvxr.displayScene();
theta.append(0.0);
for i in range(1,num_projections):
 #    Rotate the model by angular_step degrees
     for n,label in enumerate(parts_list):
          gvxr.rotateNode(label, -1*angular_step, 0,1,0);
          # Compute an X-ray image and add it to the list of projections
          xray_image = np.array(gvxr.computeXRayImage()).astype(np.single)
          # Update the 3D visualisation
          gvxr.displayScene();
          theta.append(i * angular_step * math.pi / 180);
          imwrite(f'output_data/pump_scan/03-Pump_{i}.tiff',xray_image)

# file = open("GVXR_angles.txt", "w")
# file.write(f"angles = {theta} \n")
# file.close()
gvxr.terminate()