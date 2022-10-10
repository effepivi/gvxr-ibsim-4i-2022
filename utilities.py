from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
#from tabletext import to_text
import xraylib as xrl
from xpecgen import xpecgen as xg

has_cil = True
try:
    from cil.recon import FBP
    from cil.framework import AcquisitionData, AcquisitionGeometry
except:
    has_cil = False
    
def GetDensity(material):
    if material=='H2C':
        cpH2C = xrl.GetCompoundDataNISTByName('Polyethylene')
        density = cpH2C['density']
    elif material=='H2O':
        density = 1.
    elif material=='C2F4':
        density = 2.25
    else:
        Z=xrl.SymbolToAtomicNumber(material)
        density = xrl.ElementDensity(Z)
    return density

def mu(material='H2C'):
    old_font_size  = mpl.rcParams['font.size']
    energy_range = np.arange(5.,800., 0.1, dtype=np.double)
    density = GetDensity(material)
    print(f'density {material} = {density}')
    mu_rho = [xrl.CS_Total_CP(material, E) * density for E in energy_range]
    mu_rho_Photo = [xrl.CS_Photo_CP(material, E) * density for E in energy_range]
    mu_rho_Compt = [xrl.CS_Compt_CP(material, E) * density for E in energy_range]
    mu_rho_Rayl = [xrl.CS_Rayl_CP(material, E) * density for E in energy_range]
    plt.close(1)
    fig = plt.figure(num=1,dpi=150,clear=True)
    mpl.rcParams.update({'font.size': 6})
    axMW = plt.subplot(111)
    axMW.plot(energy_range, mu_rho,color="black",linewidth=2.,linestyle="-",label='Total')
    axMW.plot(energy_range, mu_rho_Photo,color="red",linewidth=2.,linestyle="-",label='Photoelectric')
    axMW.plot(energy_range, mu_rho_Compt,color="blue",linewidth=2.,linestyle="-",label='Compton')
    axMW.plot(energy_range, mu_rho_Rayl,color="green",linewidth=2.,linestyle="-",label='Rayleigh')
    axMW.set_xscale('log')
    axMW.set_yscale('log')
    axMW.set_xlim(np.min(energy_range),np.max(energy_range))
    axMW.set_ylim(1e-2,1e4)
    plt.legend(loc='center right', frameon=True)
    plt.xlabel('Energy (keV)')
    plt.ylabel("Linear attenuation coefficient (cm$^{-1}$)")
    axMW.grid(which='major', axis='x', linewidth=0.5, linestyle='-', color='0.75')
    axMW.grid(which='minor', axis='x', linewidth=0.3, linestyle='-', color='0.75')
    axMW.grid(which='major', axis='y', linewidth=0.5, linestyle='-', color='0.75')
    axMW.grid(which='minor', axis='y', linewidth=0.3, linestyle='-', color='0.75')
    axMW.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter("%d"))
    #axMW.xaxis.set_minor_formatter(mpl.ticker.FormatStrFormatter("%d"))
    axMW.grid(True)
    #symbol=xrl.AtomicNumberToSymbol(material)
    axMW.set_title("%s" % material, va='bottom')
    #plt.savefig('mu_over_rho_W.pdf', format='PDF')
    text=axMW.text(np.min(energy_range),1e4, "", va="top", ha="left")
    def onclick(event):
        energy = np.round(event.xdata*10)*0.1
        energyidx = int(np.where(np.min(np.abs(energy_range-energy))==np.abs(energy_range-energy))[0])
        tx = 'The linear attnuation coefficient of ' + material + ' at %.1f keV is %1.4e cm$^{-1}$\n(Rayleigh %1.4e cm$^{-1}$, Photoelectric %1.4e cm$^{-1}$, Compton %1.4e cm$^{-1}$)'%(energy,mu_rho[energyidx],mu_rho_Rayl[energyidx],mu_rho_Photo[energyidx],mu_rho_Compt[energyidx])
        text.set_text(tx)
        text.set_x(axMW.get_xlim()[0])
        text.set_y(axMW.get_ylim()[1])
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    mpl.rcParams['font.size'] = old_font_size

def spectrum(E0,Mat_Z,Mat_X):
    old_font_size  = mpl.rcParams['font.size']
    xrs=xg.calculate_spectrum(E0,12,3,100,epsrel=0.5,monitor=None,z=74)
    #Inherent filtration: 1.2mm Al + 100cm Air
    mu_Al=xg.get_mu(13)
    xrs.attenuate(0.12,mu_Al)
    xrs.attenuate(100,xg.get_mu("air"))
    fluence_to_dose=xg.get_fluence_to_dose()
    xrs.set_norm(value=0.146,weight=fluence_to_dose)
    #Attenuation
    if Mat_Z>0: #Atomic number
        dMat = xrl.ElementDensity(Mat_Z)
        fMat = xrl.AtomicNumberToSymbol(Mat_Z)
        xrs.attenuate(0.1*Mat_X,xg.get_mu(Mat_Z))
    else: #-1 == 'Water'
        mH2O = 2. * xrl.AtomicWeight(1) + xrl.AtomicWeight(8)
        wH = 0.1 * Mat_X * 2. * xrl.AtomicWeight(1) / (xrl.ElementDensity(1) * mH2O)
        wO = 0.1 * Mat_X * xrl.AtomicWeight(8) / (xrl.ElementDensity(8) * mH2O)
        xrs.attenuate(wH,xg.get_mu(1))
        xrs.attenuate(wO,xg.get_mu(8))
    #Get the figures
    Nr_Photons = "%.4g" % (xrs.get_norm())
    Average_Energy = "%.2f keV" % (xrs.get_norm(lambda x:x)/xrs.get_norm())
    Dose = "%.3g mGy" % (xrs.get_norm(fluence_to_dose))
    HVL_Al=xrs.hvl(0.5,fluence_to_dose,mu_Al)
    HVL_Al_text = "%.2f mm (Al)" % (10*HVL_Al)
    a = [["Dose at 1m", Dose],["Nr of photons", Nr_Photons],
         ["Average energy",Average_Energy],["Half-value Layer", HVL_Al_text]]
    #print(to_text(a))
    (x2,y2) = xrs.get_points()



    plt.close(2)
    plt.figure(num=2,dpi=150,clear=True)
    mpl.rcParams.update({'font.size': 6})
    axMW = plt.subplot(111)
    axMW.plot(x2,y2)
    axMW.set_xlim(3,E0)
    axMW.set_ylim(0,)
    plt.xlabel("Energy [keV]")
    plt.ylabel("Nr of photons per [keV·cm²·mGy] @ 1m")
    axMW.grid(which='major', axis='x', linewidth=0.5, linestyle='-', color='0.75')
    axMW.grid(which='minor', axis='x', linewidth=0.2, linestyle='-', color='0.85')
    axMW.grid(which='major', axis='y', linewidth=0.5, linestyle='-', color='0.75')
    axMW.grid(which='minor', axis='y', linewidth=0.2, linestyle='-', color='0.85')
    axMW.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter("%d"))
    axMW.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter("%.2g"))
    axMW.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
    axMW.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
    axMW.grid(True)
    plt.show()

    mpl.rcParams['font.size'] = old_font_size


def recon_parallel(projections:np.ndarray, pixel_size:float,final_angle:float) -> Optional[np.ndarray]:
    """Reconstruct a parallel CT scan using FBP.

    Args:
        projections (np.ndarray): A set of projections. First axis is angle.

    Returns:
        np.ndarray: Reconstructed slices.
    """
    
    result = None
    
    if has_cil:
        geo:AcquisitionGeometry = AcquisitionGeometry.create_Parallel3D()

        geo.set_panel(projections.shape[1:][::-1], pixel_size)
        angles = np.linspace(0, 1) * final_angle
        geo.set_angles(angles)
        geo.set_labels(["angle", "vertical", "horizontal"])

        acData:AcquisitionData = geo.allocate()
        acData.fill(projections)

        print("Running FBP Reconstruction")
        result = FBP(acData).run()

    return result
