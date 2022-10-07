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
gvxr.setMonoChromatic(0.1,"MeV",1000)

gvxr.setDetectorNumberOfPixels(720,576)
gvxr.setDetectorPixelSize(0.75,0.75,"mm")
gvxr.setDetectorPosition(0.0,30.0,0.0,"cm")
gvxr.setDetectorUpVector(0,0,-1)

parts_list = ["internals","shaft","front_plate","back_plate","housing"]
part_files = ["input_data/TurboPump/Part3.stl",
               "input_data/TurboPump/Part4.stl",
               "input_data/TurboPump/Part5.stl",
               "input_data/TurboPump/Part6.stl",
               "input_data/TurboPump/Part7.stl"]

materials = ["Fe","Fe","Al","Al","Ti"]

for i,name in enumerate(parts_list):
     gvxr.loadMeshFile(name,part_files[i],"mm")
     gvxr.setElement(name, materials[i])
     gvxr.translateNode(name,0.0,5.0,0.0,"cm")
     gvxr.moveToCentre()
     gvxr.scaleNode(name, 0.8, 0.8, 0.8)
     gvxr.displayScene()

xray_image_front = np.array(gvxr.computeXRayImage()).astype(np.single)
# Create the output directory if needed
if not os.path.exists("output_data"):
     os.mkdir("output_data")
# write x-rayimage to file
#gvxr.saveLastXRayImage('output_data/03-Pump_front.tiff')
imwrite('output_data/03-Pump_front.tiff',xray_image_front)

for i,name in enumerate(parts_list):
     gvxr.moveToCentre()
     gvxr.translateNode(name,0.0,0.0,4.0,"cm")
     gvxr.rotateNode(name, 90, 1, 0, 0)
xray_image_side = np.array(gvxr.computeXRayImage()).astype(np.single)
#gvxr.saveLastXRayImage('output_data/03-Pump_side.tiff')
#imwrite('output_data/03-Pump_front.tiff',xray_image_front)
gvxr.renderLoop()
gvxr.terminate()