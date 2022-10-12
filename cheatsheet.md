# Cheat Sheet

## From `gvxrPython3.json2gvxr`

```
    doCTScan(verbose: bool = False)
        Perform the CT scan acquisition as initialised with the JSON file.

    Returns
    ----------
    * The rotations angles in degrees
```

```
    initDetector(fname: str = '')
        Initialise the X-ray detector from a JSON file.

    Parameters
    ----------
    * fname: The file name of the JSON file. If no file name is provided, use the cached one. (default: "")
```

```
    initGVXR(fname: str, renderer: str = 'OPENGL', major: int = 3, minor: int = 2)
        Create a simulation environment from a JSON file.

    * fname: The file name of the JSON file. The filename will be cached for further use.
    * renderer: The renderer (e.g. OPENGL, or EGL) (default: "OPENGL")
    * major: The major version of the OpenGL context to create (default: 3)
    * minor: The minor version of the OpenGL context to create (default: 2)
```

```
    initSamples(fname: str = '', verbose: int = 0)
        Initialise the scanned objects from a JSON file.

    Parameters
    ----------
    * str fname: The file name of the JSON file. If no file name is provided, use the cached one. (default: "")
    * verbose: The level of verbosity (default: 0)
```

```
    initScan(fname: str = '')
        Initialise a CT scan acquisition from a JSON file.

    Parameters
    ----------
    * fname: The file name of the JSON file. If no file name is provided, use the cached one. (default: "")
```

```
    initSourceGeometry(fname: str = '')
        Initialise the X-ray source from a JSON file.

    Parameters
    ----------
    * fname: The file name of the JSON file. If no file name is provided, use the cached one. (default: "")
```

```
    initSpectrum(fname: str = '', verbose: int = 0)
        Initialise the X-ray spectrum from a JSON file.

    Parameters
    ----------
    * fname: The file name of the JSON file. If no file name is provided, use the cached one. (default: "")
    * verbose: The level of verbosity (default: 0)

    Returns
    ----------
    * spectrum
    * unit (e.g. "keV", "MeV")
    * k
    * f
```


## From `gvxrPython3.utils`

```
compareWithGroundTruth(groundTruth: <built-in function array>, testImage: <built-in function array>, fname: str = None, figsize=(17, 7.5))
    Use Matplotlib to display (and save) the X-ray image using i) a linear scale, ii) a log scale, and iii) a power law.

    Parameters
    ----------
    * groundTruth: The image corresponding to the ground truth
    * testImage: The test image
    * fname: The file name to save the plot (default: None)
    * figsize: the size of the figure (default: (17, 7.5))
```

```
interactPlotPowerLaw(xray_image: <built-in function array>, gamma: float = 0.5, figsize=(10, 5))
    Use Matplotlib and a Jupyter widget to display the X-ray image using a power law.
    The gamma value can be change interactively.

    * xray_image: The image to display
    * gamma: the gamma value used in the Power law (default: 0.5)
    * figsize: the size of the figure (default: (10, 5))
```

```
plotScreenshot()
    Display the 3D scene (offscreen rendering may be used in the background) using Matplotlib.
```

```
saveProjections(x_ray_image: <built-in function array>, fname: str = None, gamma=0.5, figsize=(17, 7.5))
    Use Matplotlib to display (and save) the X-ray image using i) a linear scale, ii) a log scale, and iii) a power law.

    * x_ray_image: The image to display
    * fname: The file name to save the plot (default: None)
    * gamma: the gamma value used in the Power law (default: 0.5)
    * gamma figsize: the size of the figure (default: (17, 7.5))
```

```
visualise(use_log=False, use_negative=False, sharpen_ksize=1, sharpen_alpha=0.0)
    Display the 3D scene using K3D (see https://github.com/K3D-tools/K3D-jupyter).

    * use_log: Display the X-ray image using a log scale (default: False)
    * use_negative: Display the X-ray image in negative (default: False)
    * sharpen_ksize: the radius of the Gaussian kernel used in the sharpening filter (default: 1)
    *sharpen_alpha: the alpha value used in the sharpening filter (default: 0.0)
```

## From `gvxrPython3.gvxr`

### OpenGL context


```
createOpenGLContext(aWindowID=-1, aRendererMajorVersion=3, aRendererMinorVersion=2)
    Create an OpenGL context (the window won't be shown).  

    Parameters
    ----------
    * `aWindowID` :  
        the numerical ID of the context to create (default value: -1, means that the
        ID will be automatically generated)
    * `aRendererMajorVersion` : OpenGL's major version (default: 3)
    * `aRendererMinorVersion` : OpenGL's minor version (default: 2)
```

```
createWindow(aWindowID, aVisibilityFlag, aBackend, aRendererMajorVersion, aRendererMinorVersion);
    Create an OpenGL context and display it in a window.  

    Parameters
    ----------
    * `aWindowID` :  
        the numerical ID of the context to create (default value: -1, means that the
        ID will be automatically generated)  
    * `aVisibilityFlag` :  
        flag controling if the window should be visible (1) or hidden (0). (default
        value: 0)
    * `aBackend` : The backend to create the rendering context: "OPENGL" or "EGL" (default: "OPENGL")
    * `aRendererMajorVersion` : OpenGL's major version (default: 3)
    * `aRendererMinorVersion` : OpenGL's minor version (default: 2)
```


```
terminate()
    Close and destroy all the windows and OpenGL contexts that have been created.
```


```
displayScene(aSceneRotationFlag=True, aWindowID=-1)
    3-D visualisation of the 3-D scene (source, detector, and scanned objects). Note
    that there is no interactive loop running.  

    Parameters
    ----------
    * `aSceneRotationFlag` :  
        true if the 3-D scene has to be rotated with the arc-ball method, false
        otherwise (default value: true)  
    * `aWindowID` :  
        the numerical ID of the corresponding context (default value: -1, means that
        the active context will be used)
```

```
computeXRayImage(anIntegrateEnergyFlag=True)
    Compute the X-ray projection corresponding to the environment that has
    previously been set, i.e.  

    *   Detector position  
    *   Detector orientation  
    *   Detector size and resolution  
    *   Source position  
    *   Source shape  
    *   Beam spectrum  
    *   Scanned object geometries  
    *   Scanned object material properties  

    Parameters
    ----------
    * `anIntegrateEnergyFlag` : if true, the returned image corresponds to the absorbed energy,
                                if false, it corresponds to the photon count (default: True)
    --------
    Returns:
    the corresponding X-ray image
```


```
saveLastXRayImage(aFileName, useCompression=True)
    Save the last X-ray image that has been computed.  

    Parameters
    ----------
    * `aFileName` :  
        the name of the output file (default: means that the filename will be
        automatically generated and the file saved in the current path)  
    * `useCompression` :  
        use data compression is possible (default: true)
```


```
setWindowBackGroundColour(R, G, B, aWindowID=-1)
    Set the background colour of a given window

    Parameters
    ----------
    * `R` :  
        red colour. A number between 0 and 1.
    * `G` :  
        green colour. A number between 0 and 1.
    * `B` :  
        red colour. A number between 0 and 1.
    * `aWindowID` :  
        The window's numerical ID (default: -1, means
        that the active context will be used)
```


```
takeScreenshot(aWindowID=-1)
    Take a screenshot of a given window.
    
    Parameters
    ----------
    * `aWindowID` :  
        The window's numerical ID (default: -1, means
        that the active context will be used)
```



```
renderLoop(aWindowID=-1)
    3-D visualisation of the 3-D scene (source, detector, and scanned objects). Note
    that there is interactive loop running. Keys are:  
    
    *   Q/Escape: to quit the event loop (does not close the window)  
    *   B: display/hide the X-ray beam  
    *   W: display the polygon meshes in solid or wireframe  
    *   N: display the X-ray image in negative or positive  
    *   L: switch lighting on/off  
    *   D: display/hide the X-ray detector  
    *   V: display/hide normal vectors  
    
    Parameters:  
    ----------
    * `aWindowID` :  
        the numerical ID of the corresponding context (default value: -1, means
        that the active context will be used)
```


### Source

```
setSourcePosition(x,y,z,units)
```

```
usePointSource()
```

```
useParallelBeam()
```

```
setMonoChromatic(anEnergy, aUnitOfEnergy, aNumberOfPhotons)
    Use a monochromatic beam spectrum (i.e. one single energy).  

    Parameters
    ----------
    * `anEnergy` :  
        the incident photon energy  
    * `aUnitOfEnergy` :  
        the unit of energy corresponding to anEnergy. Acceptable values are:
        "electronvolt", "eV", "kiloelectronvolt", "keV",
        "megaelectronvolt", "MeV"  
    * `aNumberOfPhotons` :  
        the number of incident photons
```

```
resetBeamSpectrum()
    Empty the beam spectrum.
```


```
addEnergyBinToSpectrum(anEnergy, aUnitOfEnergy, aNumberOfPhotons)
    Add an energy bin to the beam spectrum (useful to generate polychromatism).  

    Parameters
    ----------
    * `anEnergy` :  
        the incident photon energy  
    * `aUnitOfEnergy` :  
        the unit of energy corresponding to anEnergy. Acceptable values are:
        "electronvolt", "eV", "kiloelectronvolt", "keV",
        "megaelectronvolt", "MeV"  
    * `aNumberOfPhotons` :  
        the number of incident photons
```

```
loadSpectrumFromTSV(aFileName, aUnitOfEnergy, aNormalisationFlag)
    Load the incident beam energy spectrum from a TSV file.  

    Parameters
    ----------
    * `aFileName` :  
        name of the file to load  
    * `aUnitOfEnergy` :  
        the unit of energy corresponding to anEnergy. Acceptable values are:
        "electronvolt", "eV", "kiloelectronvolt", "keV",
        "megaelectronvolt", "MeV"  
    * `aNormalisationFlag` :  
        true to normalise the total energy to 1, false otherwise
```


```
setFocalSpot()
```


```
getTotalEnergyWithDetectorResponse()
```


### Detector

```
setDetectorNumberOfPixels(Px,Py)
```

```
setDetectorPixelSize(width,height,units)
```

```
setDetectorPosition(x,y,z,units)
```

```
setDetectorUpVector(ix,jy,kz)
```


```
setLSF
```

```
loadDetectorEnergyResponse
```


```
clearDetectorEnergyResponse
```

### Sample

```
removePolygonMeshesFromSceneGraph
```


```
loadMeshFile(aLabel, aFileName, aUnitOfLength, addToRendererAsInnerSurface=True)
    Load a polygon mesh from a file, set its label in the scenegraph (i.e.
    identifier) and add it to the X-ray renderer.  

    Parameters
    ----------
    * `aLabel` :  
        the label in the scenegraph  
    * `aFileName` :  
        the file where the polygon mesh data is stored  
    * `aUnitOfLength` :  
        the unit of length corresponding to the data stored in the file. Acceptable
        values are: "um", "micrometre", "micrometer", "mm", "millimetre",
        "millimeter", "cm", "centimetre", "centimeter", "dm",
        "decimetre", "decimeter", "m", "metre", "meter", "dam",
        "decametre", "decameter", "hm", "hectometre", "hectometer",
        "km", "kilometre", "kilometer"
```

```
setElement(aLabel, aName)
    Set the chemical element (or element) corresponding to the material properties
    of a polygon mesh.  

    Parameters
    ----------
    * `aLabel` :  
        the label of the polygon mesh  
    * `aName` :  
        the symbol or name corresponding to the element
```

```
setElement(ID, 26)
```


```
getNodeAndChildrenBoundingBox(aLabel, aUnitOfLength)
    Access the bounding box of a given node and all its children (if any). The
    bounding box is given in the world coordinate system.  

    Parameters
    ----------
    * `aLabel` :  
        the label in the scenegraph  
    * `aUnitOfLength` :  
        the unit of length corresponding to the bounding box. Acceptable values are:
        "um", "micrometre", "micrometer", "mm", "millimetre",
        "millimeter", "cm", "centimetre", "centimeter", "dm",
        "decimetre", "decimeter", "m", "metre", "meter", "dam",
        "decametre", "decameter", "hm", "hectometre", "hectometer",
        "km", "kilometre", "kilometer" (default value: "cm")  

    Returns
    -------
    the bounding box as: min_x, min_y, min_z, max_x, max_y, max_z
```

```
rotateNode(aLabel, anAngle, x, y, z)
    Rotate a polygon mesh.  

    Parameters
    ----------
    * `aLabel` :  
        the label of the polygon mesh to transform  
    * `anAngle` :  
        the rotation angle in degrees  
    * `x` :  
        the component of the rotation vector along the X-axis  
    * `y` :  
        the component of the rotation vector along the Y-axis  
    * `z` :  
        the component of the rotation vector along the Z-axis
```

```
translateNode(aLabel, x, y, z, aUnitOfLength)
    Translate a polygon mesh.  

    Parameters
    ----------
    * `aLabel` :  
        the label of the polygon mesh to transform  
    * `x` :  
        the component of the translation vector along the X-axis  
    * `y` :  
        the component of the translation vector along the Y-axis  
    * `z` :  
        the component of the translation vector along the Z-axis  
    * `aUnitOfLength` :  
        the unit of length corresponding to the x, y and z parameters. Acceptable
        values are: "um", "micrometre", "micrometer", "mm", "millimetre",
        "millimeter", "cm", "centimetre", "centimeter", "dm",
        "decimetre", "decimeter", "m", "metre", "meter", "dam",
        "decametre", "decameter", "hm", "hectometre", "hectometer",
        "km", "kilometre", "kilometer"
```

```
scaleNode(aLabel, x, y, z)
    Scale a polygon mesh.  

    Parameters
    ----------
    * `aLabel` :  
        the label of the polygon mesh to transform  
    * `x` :  
        the scaling factor along the X-axis  
    * `y` :  
        the scaling factor along the Y-axis  
    * `z` :  
        the scaling factor along the Z-axis  
```

```
moveToCenter
```


```
moveToCentre
```


```
getNodeWorldTransformationMatrix(ID)
```


```
setNodeTransformationMatrix(aLabel, aMatrix)
    Set the transformation matrix of a given node.  

    Parameters
    ----------
    * `aLabel` :  
        the label of the polygon mesh  
    * `aMatrix` :  
        the transformation matrix as a 4x4 array
```


```
setMixture
```



```
setCompound(aLabel, aCompound)
    Set the compound corresponding to the material properties of a polygon mesh.
    Don't forget to set the density of the material.  

    Parameters
    ----------
    * `aLabel` :  
        the label of the polygon mesh  
    * `aCompound` :  
        the details about the compound. It is given as a sequence of element symbol
        & number of atoms, e.g. H2O for water and SiC for silicon carbide.
```


```
setDensity(aLabel, aDensity, aUnit)
    Set the density corresponding to the material properties of a polygon mesh.  

    Parameters
    ----------
    * `aLabel` :  
        the label of the polygon mesh  
    * `aDensity` :  
        the density  
    * `aUnit` :  
        the unit corresponding to aDensity. Acceptable values are: "g/cm3" and
        "g.cm^-3"
```


```
setColour(aLabel, R, G, B, A)
    Set the colour of a given polygon mesh.  

    Parameters
    ----------
    * `aLabel` :  
        the label of the polygon mesh  
    * `R` :  
        the red channel  
    * `G` :  
        the green channel  
    * `B` :  
        the blue channel  
    * `A` :  
        the alpha channel
```


```
setColor(aLabel, R, G, B, A)
    Set the colour of a given polygon mesh.  

    Parameters
    ----------
    * `aLabel` :  
        the label of the polygon mesh  
    * `R` :  
        the red channel  
    * `G` :  
        the green channel  
    * `B` :  
        the blue channel  
    * `A` :  
        the alpha channel
```
