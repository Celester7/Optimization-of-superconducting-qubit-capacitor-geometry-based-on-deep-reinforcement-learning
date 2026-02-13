import math
import re
import io
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Union
import pandas as pd
from pint import UnitRegistry
from pathlib import Path
ureg = UnitRegistry()

Lj=15e-9 
Ql=1e4 
Qi=1e5
e = 1.60217657e-19  # electron charge
h = 6.62606957e-34  # Plank's
hbar = 1.0545718E-34  # Plank's reduced
phinot = 2.067 * 1E-15  # magnetic flux quantum
phi0 = phinot / (2 * np.pi)  # reduced magnetic flux quantum



def transmon_props(Ic: float, Cq: float):
    """Properties of a transmon qubit.

    Calculate LJ, EJ, EC, wq, eps from Ic,Cq.

    Args:
        Ic (float): Junction Ic (in A)
        Cq (float): Junction capacitance (in F)

    Returns:
        tuple: [LJ, EJ, Zqp, EC, wq, wq0, eps1] -- Inductance
    """
    LJ = phi0 / Ic
    EJ = phi0**2 / LJ / hbar
    Zqp = np.sqrt(LJ / Cq)
    EC = e**2 / 2 / Cq / hbar
    wq0 = 1 / np.sqrt(LJ * Cq)
    wq = 1 / np.sqrt(LJ * Cq) - EC
    # charge dispersion
    eps1 = EC * 2**9 * (2/np.sqrt(np.pi)) * \
        (EJ/2/EC)**(1.25) * np.exp(-np.sqrt(8*EJ/EC))
    Rn = np.pi * 0.182e-3 /Ic /2
    return LJ, EJ, Zqp, EC, wq, wq0, eps1,Rn

def levels_vs_ng_real_units(Cq, IC, N=301, do_disp=0, do_plots=0):
    C = Cq * 1e-15
    IC = IC * 1e-9
    Ec = e**2 / 2 / C
    nmax = 40
    dim = 2 * nmax + 1
    nmat = np.zeros([dim, dim])
    V = nmat
    charge = np.linspace(-1., 1., N)
    # KE
    for ii in range(dim):
        nmat[ii, ii] = ii - nmax
    # PE
    V = np.diag(-0.5 * np.ones([dim - 1]), 1)
    V = (V + np.transpose(np.conj(V)))
    varphi = hbar / 2 / e
    EJ = IC * varphi
    elvls = np.zeros([dim, N])
    for iindex in range(N):
        ng = charge[iindex]
        H = 4 * Ec * (nmat - ng * np.eye(dim))**2 + EJ * V
        if (not np.array_equal(H, np.transpose(np.conj(H)))):
            raise ValueError('Matrix is not Hermitian')
        [d, v] = np.linalg.eig(H)
        sortIX = np.argsort(d)
        sorted_d = d[sortIX]
        elvls[:, iindex] = (sorted_d - sorted_d[0])
    if do_plots:
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.plot(charge,
                 elvls[0,] / h / 1e9,
                 'k',
                 charge,
                 elvls[1,] / h / 1e9,
                 'b',
                 charge,
                 elvls[2,] / h / 1e9,
                 'r',
                 charge,
                 elvls[3,] / h / 1e9,
                 'g',
                 LineWidth=2)
        plt.xlabel('Gate charge, n_g [2e]')
        plt.ylabel('Energy, E_n [GHz]')
        plt.subplot(1, 2, 2)
        plt.plot(charge, (-elvls[1, :] / h + elvls[1, 0] / h) / 1e3, 'k')
        plt.xlabel('Gate charge, n_g [2e]')
        plt.ylabel('Energy [kHz], ')
        plt.show()
        plt.figure(2)
        plt.subplot(1, 2, 1)
        plt.plot(
            charge, 1000 * (elvls[2,] / h / 1e9 - elvls[0,] / h / 1e9 -
                            2 * elvls[1,] / h / 1e9 - elvls[0,] / h / 1e9),
            charge, -charge * 0 - 1000 * Ec / h / 1e9)
        plt.xlabel('Gate charge, n_g [2e]')
        plt.ylabel('delta [MHZ] green theory, blue numerics ')
        plt.subplot(1, 2, 2)
        plt.plot(charge, elvls[1,] / h / 1e9 - elvls[0,] / h / 1e9, charge,
                 charge * 0 + (np.sqrt(8 * EJ * Ec) - Ec) / h / 1e9)
        plt.xlabel('Gate charge, n_g [2e]')
        plt.ylabel('F01 [GHZ] green theory, blue numerics ')
        plt.show()
    fqubitGHz = np.mean(elvls[1,] / h / 1e9)
    anharMHz = np.mean(1000 * (elvls[2,] / h / 1e9 - elvls[0,] / h / 1e9 -
                               2 * elvls[1,] / h / 1e9 - elvls[0,] / h / 1e9))

    disp = np.max(-elvls[1,] / h + elvls[1, 0] / h)
    tphi_ms = 2 / (2 * np.pi * disp * np.pi * 1e-4 * 1e-3)
    if do_disp:
        print('Mean Frequency %f [GHz]' % fqubitGHz)
        print('Anharmonicity %f [MHz]' % anharMHz)
        print('EC %f [GHz]' % (Ec / h / 1e9))
        print('Charge Dispersion %f [kHz]' % (disp / 1e3))
        print('Dephasing Time %f [ms]' % tphi_ms)

    return fqubitGHz, anharMHz, disp, tphi_ms

    # Capacitance matrix parsing
def calculate_capacitance_matrix(capMatrix,
                                         N: int, #pad number
                                         res_L4_corr: float = None,
                                         g_scale: float = 1.0,
                                         print_info: bool = False):
    fr=6.6
    fb=[6.6, 6.6]
    Cj_fF=2 #fF
    CJ = ureg(f'{Cj_fF} fF').to('farad').magnitude
    fr = ureg(f'{fr} GHz').to('GHz').magnitude
    fb = [ureg(f'{freq} GHz').to('GHz').magnitude for freq in fb]
    
    # make list of angular frequencies of resonators
    wr = np.zeros(N)  # angular freq of resonators (GHz-rad)
    for ii in range(N):
        if ii == 0:  # readout resonator
            wr[ii] = 2 * np.pi * fr * 1e9
        else:
            if isinstance(fb, (int, float)):  # just a single one
                wr[ii] = 2 * np.pi * fb * 1e9
            else:
                wr[ii] = 2 * np.pi * fb[ii - 1] * 1e9  # offset index by
    Zbus = 50
    Cr = 0.5 * np.pi / (wr * Zbus)
    Lr = 1 / wr**2 / Cr
    
    if res_L4_corr:
        Cr/= 2.0
        Lr*= 2.0

    ground_index = max([0, N - 1])
    qubit_index = [ground_index + 1, ground_index + 2]
    bus_index = np.zeros(N, dtype=int)
    for ii in range(N):
        if ii == 0:
            bus_index[ii] = len(capMatrix) - 1
        else:
            bus_index[ii] = ii - 1

    # Cg list of qubit pads to ground
    Cg = [
        -capMatrix[qubit_index[0], ground_index],
        -capMatrix[qubit_index[1], ground_index]
    ]

    # Cs qubit pads to each other
    Cs = -capMatrix[qubit_index[0], qubit_index[1]]

    # Cbus (qubit pads to coupling pads)
    # index is ordered as [readout,bus1,...]
    Cbus = np.zeros([2, N])
    for ii in range(2):
        for jj in range(N):
            Cbus[ii, jj] = -capMatrix[qubit_index[ii], bus_index[jj]]

    Cres = np.zeros([2])
    for ii in range(2):
        Cres[ii] = -capMatrix[qubit_index[ii], bus_index[0]]
    CRQ = Cres[0]
    CRR = Cr[0]

    # crosspad capacitance
    Cbusbus = np.zeros([N, N])
    for ii in range(N):
        for jj in range(N):
            if ii != jj:
                Cbusbus[ii, jj] = -capMatrix[bus_index[ii], bus_index[jj]]

    # sum of capacitances from each pad to ground
    # this assumes the bus couplers are at "ground"
    C1S = Cg[0] + np.sum(Cbus[0,])
    C2S = Cg[1] + np.sum(Cbus[1,])
    print('Cs:', Cs, 'C1S:', C1S, 'C2S:', C2S)
    # total capacitance between pads
    tCSq = Cs + C1S * C2S / (C1S + C2S)  # Key equation
    print('tCSq:', tCSq)
    # total capacitance of each pad to ground?
    # Note the + in the squared term below !!!
    tCSbus = np.zeros(N)
    for ii in range(N):
        tCSbus[ii] = Cr[ii] - (Cbus[0, ii]+Cbus[1, ii])**2 / \
            (C1S+C2S) + np.sum(Cbus[:, ii]) + np.sum(Cbusbus[ii, :])
    # qubit to coupling pad capacitance
    tCqbus = (C2S * Cbus[0,] - Cbus[1,] * C1S) / (C1S + C2S)

    # coupling pad to coupling pad capacitance
    tCqbusbus = np.zeros([N, N])
    for ii in range(N):
        for jj in range(N):
            tCqbusbus[ii, jj] = Cbusbus[ii, jj] + \
                (Cbus[0, ii]+Cbus[1, ii])*(Cbus[0, jj]+Cbus[1, jj])/(C1S+C2S)

    # voltage division ratio
    bbus = abs(C2S * Cbus[0,] - Cbus[1,] * C1S) / ((C1S + C2S) * Cs + C1S * C2S)
    # print('bbus:', bbus)
    # total qubit capacitance (including junction capacitance)
    Cq = tCSq + CJ
    print('Cq:', Cq)
    Zbus = np.sqrt(Lr / tCSbus)
    return Cq,bbus,Zbus,g_scale,wr,CRQ,CRR

def df_cmat_style_print(df_cmat: pd.DataFrame):
    """Display the dataframe in the cmat style.

    Args:
        df_cmat (dataframe): Dataframe to display
    """
    from IPython.display import display
    display(df_cmat.style.format("{:.2f}").bar(color='#5fba7d', width=100))
    
def readin_q3d_matrix(path: str, delim_whitespace=True):
    text = Path(path).read_text()

    s1 = text.split('Capacitance Matrix')
    assert len(s1) == 2, "Copuld not split text to `Capacitance Matrix`"

    s2 = s1[1].split('Conductance Matrix')

    df_cmat = pd.read_csv(io.StringIO(s2[0].strip()),
                          delim_whitespace=delim_whitespace,
                          skipinitialspace=True,
                          index_col=0)
    if len(s2) > 1:
        df_cond = pd.read_csv(io.StringIO(s2[1].strip()),
                              delim_whitespace=delim_whitespace,
                              skipinitialspace=True,
                              index_col=0)
    else:
        df_cond = None

    if delim_whitespace == False and len(df_cmat.columns):
        df_cmat = df_cmat.drop(df_cmat.columns[-1], axis=1)

    units = re.findall(r'C Units:(.*?),', text)[0]
    design_variation = re.findall(r'DesignVariation:(.*?)\n', text)
    if len(design_variation) == 0:
        design_variation = re.findall(r'Design Variation:(.*?)\n', text)
        if design_variation:
            design_variation = design_variation[0]
        else:
            design_variation = ''
    else:
        design_variation = design_variation[0]

    return df_cmat, units, design_variation, df_cond

def load_q3d_capacitance_matrix(path, user_units='fF', _disp=False):
    df_cmat, Cunits, design_variation, df_cond = readin_q3d_matrix(path)

    # Unit convert
    ureg = UnitRegistry()
    q = ureg.parse_expression(Cunits).to(user_units)
    df_cmat = df_cmat * q.magnitude  # scale to user units

    # Report
    if _disp:
        print(
            "Imported capacitance matrix with UNITS: [%s] now converted to USER UNITS:[%s] \
                from file:\n\t%s" % (Cunits, user_units, path))
        df_cmat_style_print(df_cmat)

    return df_cmat, user_units, design_variation, df_cond


def T1_purcell(path):
    capMatrix, user_units, _, _, = load_q3d_capacitance_matrix(path) 
    c_units = ureg(user_units).to('farads').magnitude
    Ic=phi0/Lj  
    Cq, bbus, Zbus, g_scale,wr,CRQ,CRR = calculate_capacitance_matrix(capMatrix.values * c_units, N=2, res_L4_corr=1)
    LJ, EJ, Zqp, EC, wq, wq0, eps1,Rn = transmon_props(Ic, Cq)
    fq, alpha, disp, tphi_ms = levels_vs_ng_real_units(Cq / 1e-15,
                                                        Ic / 1e-9,
                                                        N=51, do_disp=0, do_plots=0)

    wq = 2 * np.pi *fq * 1e9   
    gqbus = 0.5 * wr * bbus * np.sqrt(Zbus / Zqp) * g_scale  
    gbus_in_MHz = gqbus / 1e6 / 2 / np.pi  

    Qreadout = 1e4
    Qcouplingbus = 1e5
    Qbus = np.zeros(2)
    for ii in range(2):
        if ii == 0:
            Qbus[ii] = Qreadout
        else:
            Qbus[ii] = Qcouplingbus
    kbus = wr / Qbus

    #T1
    Ec = e**2/2/Cq    
    Ej = phi0**2 / Lj
    w10=(math.sqrt(8*(Ej/2/math.pi)/(Ec/2/math.pi))-1)*(Ec/2/math.pi)/hbar
    wr=wr/2/np.pi
    gamma=wr/Qbus 
    g = 0.5 * wr[0] * bbus[0] * np.sqrt(Zbus[0] / Zqp)

    T1 = (w10*2*math.pi-wr[0]*2*math.pi)**2/(g*2*math.pi)**2/(gamma[0]*2*math.pi) 

    return T1/1E-6, g/1e6, w10/1e9, Cq

