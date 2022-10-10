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

from gvxrPython3 import gvxr # Simulate X-ray images

