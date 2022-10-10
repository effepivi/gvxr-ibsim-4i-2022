import os
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
gvxr.setMonoChromatic(0.3,"MeV",1000)
#gvxr.setMonoChromatic(0.8,"MeV",1000)
#gvxr.setDetectorNumberOfPixels(720,576)
gvxr.setDetectorNumberOfPixels(800,800)
gvxr.setDetectorPixelSize(0.7,0.7,"mm")
gvxr.setDetectorPosition(0.0,30.0,0.0,"cm")
gvxr.setDetectorUpVector(0,0,-1)

parts_list = ["internals","coupler","front_flange","rear_flange","housing","roller_bearing"]
part_files = ["input_data/TurboPump/internals.stl",
               "input_data/TurboPump/coupler.stl",
               "input_data/TurboPump/front_flange.stl",
               "input_data/TurboPump/rear_flange.stl",
               "input_data/TurboPump/housing.stl",
               "input_data/TurboPump/ThrustRollerBearing.stl"]

stainless = "C0.12Mn2.00Si1.00Cr19.0Ni11.0Fe66.85"

elements = [12,25,14,24,28,26]
ammounts = [0.12,2.00,1.00,19.0,11.0,66.85]

#;

materials2 = [stainless,stainless,stainless,stainless,stainless,stainless]
materials = ["Fe","Fe","Fe","Fe","Fe","Fe"]
for i,name in enumerate(parts_list):
     gvxr.loadMeshFile(name,part_files[i],"mm")
     gvxr.setElement(name, materials[i])
     gvxr.translateNode(name,0.0,-20.0,0.0,"cm")
     gvxr.moveToCentre()
     #gvxr.scaleNode(name, 0.8, 0.8, 0.8)
     gvxr.displayScene()

xray_image_1 = np.array(gvxr.computeXRayImage()).astype(np.single)
# Create the output directory if needed
if not os.path.exists("output_data"):
     os.mkdir("output_data")
# write x-ray image to file
#gvxr.saveLastXRayImage('output_data/03-Pump_front.tiff')
imwrite('output_data/03-Pump_Iron.tiff',xray_image_1)

for i,name in enumerate(parts_list):
     gvxr.setMixture(name,elements,ammounts)
     gvxr.setDensity(name, 8.0, "g/cm3")
xray_image_2 = np.array(gvxr.computeXRayImage()).astype(np.single)
#gvxr.saveLastXRayImage('output_data/03-Pump_side.tiff')
imwrite('output_data/03-Pump_stainless.tiff',xray_image_2)
#gvxr.renderLoop()
compareWithGroundTruth(xray_image_1, xray_image_2, figsize=(12.5, 5))
gvxr.terminate()