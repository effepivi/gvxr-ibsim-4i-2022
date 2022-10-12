"""Load and scan the turbopump from a json file"""

from pathlib import Path
from gvxrPython3 import gvxr, json2gvxr
import tifffile as tf

if __name__ == "__main__":
    # Setup scan from json
    json2gvxr.initGVXR("./JSON/Turbopump.json")
    json2gvxr.initDetector()
    json2gvxr.initSourceGeometry()
    json2gvxr.initSpectrum()
    json2gvxr.initSamples()
    json2gvxr.initScan()

    # Perform CT scan

    # To create a preview animation, add the following to the TurboPump json's
    # Scan key. This will dramatically slow down the scan!
    # "GifPath": "./input_data/TurboPump/scan/preview.gif"

    # Also; disabling verbosity will also speed up the scan. (But won't show
    # progress)
    angles = json2gvxr.doCTScan(verbose=False)
    print("Scan complete!")

    # Save angles to file
    with open("./input_data/TurboPump/scan/angles.csv", "w") as f:
        f.writelines([ f"{x}\n" for x in angles])

    # apply flatfields to files
    print("Performing flatfield correction...")
    for f in Path("./input_data/TurboPump/scan/").glob("*.tiff"):
        tf.imwrite(tf.imread(f) / gvxr.getTotalEnergyWithDetectorResponse())
