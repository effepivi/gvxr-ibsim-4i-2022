# [gVirtualXray](https://gvirtualxray.sourceforge.io/) user training day at [IBSim-4i](https://ibsim.co.uk/events/ibsim-4i/) 2022

- Session 1
    - [Notebook 0](00-warming-up.ipynb) -- Warming up
        - Log in;
        - Copy the training data;
        - Install the Python packages needed for this course;
        - Check that [gVirtualXray](https://gvirtualxray.sourceforge.io/) is working well;
        - Verify which version of [gVirtualXray](https://gvirtualxray.sourceforge.io/) is installed (software and hardware);
        - How to get help (during and after the training).
    - [Notebook 1](01-Introduction-to-Xray-attenuation.ipynb) -- Introduction to X-ray attenuation and its implementation in [gVirtualXray](https://gvirtualxray.sourceforge.io/)
        - Explain what gVXR is and why it has been developed;
        - Introduce projection X-ray imaging and how X-rays are produced;
        - Understand how X-rays interact with matter;
        - Become familiar with the Beer-Lambert law to compute the attenuation of X-rays by matter;
        - Describe how the Beer-Lambert law is implemented in [gVirtualXray](https://gvirtualxray.sourceforge.io/);
        - Compare images simulated using [gVirtualXray](https://gvirtualxray.sourceforge.io/) with ground truth images.
- Session 2
    - [Notebook 2](02-first_xray_simulation.ipynb) -- First X-ray radiograph simulations
        - Create our first X-ray simulation, step-by-step;
        - Save our X-ray image in a file format that preserves the original dynamic range;
        - Visualise the results with 3 different look-up tables;
        - Visualise the 3D environment.
    - [Notebook 3](03-multi_material_sample.ipynb) -- Multi-material samples
        - Chemical elements
        - Mixtures
        - Compounds
- Session 3
    - [Notebook 4](04-source_parameters.ipynb)
        - Parallel beam (synchrotron)
        - Cone-beam (X-ray tube)
        - Focal spot
        - Polychromatic spectrum
        - Pixel size, magnification
    - Preview: watch out for new release with photonic noise model
    - [Notebook 5](05-detector_parameters.ipynb)
        - Pixel size (revisited)
        - Point spread function
        - Energy response of the detector
- Session 4
    - [Notebook 6](06-CT_acquisition.ipynb)
        - Parallel beam
        - Cone beam
        - Monochromatic spectrum
        - Polychromatic spectrum
    - [Notebook 7](07-2D_registration_Xray_radiograph.ipynb)
<!--     - [Notebook 8](08-3D_registration_Xray_CT.ipynb) -->
<!--


- 12:30 – Lunch
- 13:30 – Session 3 (1 hour 15 minutes)
    - gVXR: More advanced simulations
            - Polychromatic spectrum  (faut parler de l'influence des kV et mA, de l'utilisation de filtres et du type d'anode (W, Mo, Cu...).)  Pour le 5 et 8, il serait bien de montrer à exposition constante (mAs) l'influence de la taille du pixel.
            - Photonic noise    
- 14:45 – Coffee
- 15:15 – Session 4 (1 hour 45 minutes)
    - gVXR: Simulation of tomography acquisition
        1. parallel
        2. cone beam
        3. monochromatic
        4. polychromatic
        5. noisy
        6. noiseless
    - gVXR: Image registration
- 17:00 – End -->
