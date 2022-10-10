# Cheat Sheet

## From `gvxrPython3.utils`

```
compareWithGroundTruth(groundTruth: <built-in function array>, testImage: <built-in function array>, fname: str = None, figsize=(17, 7.5))
    Use Matplotlib to display (and save) the X-ray image using i) a linear scale, ii) a log scale, and iii) a power law.
    
    @param groundTruth: The image corresponding to the ground truth
    @param testImage: The test image
    @param fname: The file name to save the plot (default: None)
    @gamma figsize: the size of the figure (default: (17, 7.5))
```

```
interactPlotPowerLaw(xray_image: <built-in function array>, gamma: float = 0.5, figsize=(10, 5))
    Use Matplotlib and a Jupyter widget to display the X-ray image using a power law.
    The gamma value can be change interactively.
    
    @param xray_image: The image to display
    @gamma: the gamma value used in the Power law (default: 0.5)
    @gamma figsize: the size of the figure (default: (10, 5))
```

```
plotScreenshot()
    Display the 3D scene (offscreen rendering may be used in the background) using Matplotlib.
```

```
saveProjections(x_ray_image: <built-in function array>, fname: str = None, gamma=0.5, figsize=(17, 7.5))
    Use Matplotlib to display (and save) the X-ray image using i) a linear scale, ii) a log scale, and iii) a power law.
    
    @param x_ray_image: The image to display
    @param fname: The file name to save the plot (default: None)
    @gamma: the gamma value used in the Power law (default: 0.5)
    @gamma figsize: the size of the figure (default: (17, 7.5))
```
     
```
visualise(use_log=False, use_negative=False, sharpen_ksize=1, sharpen_alpha=0.0)
    Display the 3D scene using K3D (see https://github.com/K3D-tools/K3D-jupyter).
    
    @param use_log: Display the X-ray image using a log scale (default: False)
    @param use_negative: Display the X-ray image in negative (default: False)
    @sharpen_ksize: the radius of the Gaussian kernel used in the sharpening filter (default: 1)
    @sharpen_alpha: the alpha value used in the sharpening filter (default: 0.0)
```

## From `gvxrPython3.gvxr`

from gvxrPython3 import gvxr # Simulate X-ray images
