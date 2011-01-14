import operator

#import Elemental
import numpy
import PyMca.Elements as PyMEl

from .xrd_math_fcns import *
from .XRDdefaults import *


def GunPropertyDict(gunelements, getEtYstar=False):
#def xx(gunelements, getEtYstar=False):
    #elsymbols=[Elemental.table[i].symbol for i in range(len(Elemental.table))]

    szmd=[[l[0],l[1], l[5],l[6]/1000.] for l in PyMEl.ElementsInfo]
    elsymbols=map(operator.itemgetter(0),szmd)
    elnumber=map(operator.itemgetter(1),szmd)
    elmass=map(operator.itemgetter(2),szmd)
    eldens=map(operator.itemgetter(3),szmd)

    temp=[[i, el, elsymbols.index(el)] for i, el in enumerate(gunelements) if el in elsymbols]

    if len(temp)==0:
        return None
    guninds, elsym, elind = zip(*temp)
    #now these lists are only as long as the number of elements in guns. the guninds list knows which guns the elmenets were in with index 0 to 3 refering to guns 1 to 4

    #temp=[[Elemental.table[i].number, Elemental.table[i].atomic_mass.value, Elemental.table[i].density_solid.value] for i in elind]
    temp=[[elnumber[i], elmass[i], eldens[i]] for i in elind]

    elZ, elM, eld = zip(*temp)
    returndict={}
    returndict['guninds']=list(guninds)
    returndict['symbol']=list(elsym)
    returndict['Z']=list(elZ)
    returndict['M']=list(elM)
    returndict['d']=list(eld)
    if getEtYstar:
        f=ETHRESHYSTARTXT()
        lines=f.readlines()
        fel=[]
        fEt=[]
        fYs=[]
        for l in lines:
            a,b,c=l.partition('\t')
            fel+=[a]
            a,b,c=c.partition('\t')
            fEt+=[eval(a)]
            fYs+=[eval(stripbadcharsfromnumstr(c))]
        elEt=[]
        elYs=[]
        for el in elsym:
            if el in fel:
                elEt+=[fEt[fel.index(el)]]
                elYs+=[fYs[fel.index(el)]]
            else:
                elEt+=[-1]
                elYs+=[-1]
        returndict['Et']=elEt
        returndict['Ys']=elYs
        f.close()
    return returndict


def RespCoef(z_a, m_a, et_a, ys_a, z_b, m_b, et_b, ys_b, v_b):
    z_ar=18
    m_ar=40 #assume sputter gas is Ar
    z_pb=82
    m_pb=207.2
    et_pb=7.44
    ys_pb=4.37 #resputter algorithms are all calibrated with Pb and everything else is compared to Pb

    if et_b>v_b:
        return 0.0
    eps_b=0.0325*v_b*m_b/(m_ar+m_b)/z_ar/z_b/(z_ar**0.6667+z_b**0.6667)**0.5
    eps_pb=0.0325*v_b*m_pb/(m_ar+m_pb)/z_ar/z_pb/(z_ar**0.6667+z_pb**0.6667)**0.5

    neta_b=0.689*(m_b/m_ar)**0.2-0.877*eps_b**0.044/(m_b/m_ar)**0.0428
    eeta_b=0.207*(m_b/m_ar)-0.225*(m_b/m_ar)**0.938*eps_b**0.0144

    eeta_pb=0.207*(m_pb/m_ar)-0.225*(m_pb/m_ar)**0.938*eps_pb**0.0144

    y_b_ar=0.906*ys_b*v_b**0.402*(1-(et_b/v_b)**0.5)**2.8

    beta_b=2.35*neta_b/y_b_ar

    emax=0.56*v_b*eeta_b/eeta_pb

    if (emax**0.425)<5.0:
        return 0.0

    yy_a_ar=0.906*ys_a*236.0*numpy.exp(-1.0*(20.9+et_a)**0.529)*(emax**0.425-5.0)**(0.701+0.0328*et_a)
    yy_b_ar=0.906*ys_b*236.0*numpy.exp(-1.0*(20.9+et_b)**0.529)*(emax**0.425-5.0)**(0.701+0.0328*et_b)

    return (yy_a_ar*beta_b)/(1.0-yy_b_ar*beta_b)

def SortedRespCoef(gunpropdict):
    critrespcoef=0.1
    ABCF=[]
    for i, gunind1 in enumerate(gunpropdict['guninds']):
        for j, gunind2 in enumerate(gunpropdict['guninds']):
            if gunpropdict['Ys'][i]>0 and gunpropdict['Ys'][j]>0:
                rc=RespCoef(gunpropdict['Z'][i], gunpropdict['M'][i], gunpropdict['Et'][i], gunpropdict['Ys'][i], gunpropdict['Z'][j], gunpropdict['M'][j], gunpropdict['Et'][j], gunpropdict['Ys'][j], gunpropdict['voltages'][j])
                if rc>critrespcoef:
                    ABCF+=[[gunind1, gunind2, rc, 1.0]]
    return sorted(ABCF,key=operator.itemgetter(2), reverse=True)

def GunPosnDict(x, z): #assumes topview, mm      returns dict with rgun0 to 3, etc
    rgun_guncenter=[71.1, 71.1, 71.1, 0.0]
    gunanglefromz=[numpy.pi*4.0/3.0, 0.0, numpy.pi*2.0/3.0, 0.0]
    gunheightsubplane=[41.9, 41.9, 41.9, 0.0] #I don't know gun4
    returndict={}
    for i, (rgc, thg, hg) in enumerate(zip(rgun_guncenter, gunanglefromz, gunheightsubplane)):
        polr, polt=polar_cart(z, x)
        if i<3:
            rgun=numpy.sqrt(rgc**2+polr**2-2.0*rgc*polr*numpy.cos(thg-polt))
            returndict['rgun%d' %i]=rgun
            returndict['cosphigun%d' %i]=(rgc**2+rgun**2-polr**2)/(2.0*rgc*rgun)
        else:
            returndict['rgun%d' %i]=polr
            returndict['cosphigun%d' %i]=x*0.0+1.0
        returndict['rhogun%d' %i]=numpy.sqrt(returndict['rgun%d' %i]**2+hg**2)
        returndict['omegagun%d' %i]=1.91-0.0181*returndict['rhogun%d' %i]
    returndict['x']=x
    returndict['z']=z
    return returndict

def deprate_radialfcn(gunind, crate, pars, rgun):
    if gunind<3:
        return crate*(pars[0]*numpy.exp(-1.0*rgun*pars[1])+pars[2]*rgun**2.0)
    elif pars[2]==0:
        return crate*pars[0]*numpy.exp(-1.0*rgun*pars[1]**2.0)
    else:
        return crate*(1.0+pars[0]*rgun**2.0*numpy.exp(-1.0*rgun*pars[1])-pars[2]*rgun)

def DepRates(gunpropdict, gunposndict, resputter=True):
    rates=numpy.float32([numpy.sqrt(gunposndict['cosphigun%d' %guni])*deprate_radialfcn(guni, rt, prof, gunposndict['rgun%d' %guni]) for guni, rt, prof in zip(gunpropdict['guninds'], gunpropdict['CenterMolRates'], gunpropdict['ProfileParams'])])
    if not resputter:
        return rates
    ABCoef=[[a, b, c*f] for a, b, c, f in gunpropdict['RespAgunBgunCoef'] if c*f>0 and not numpy.isnan(c*f)]
    ABCoef=sorted(ABCoef,key=operator.itemgetter(2), reverse=True)
    print ABCoef
    print gunpropdict
    for agunind, bgunind, c in ABCoef:
        i=gunpropdict['guninds'].index(agunind)
        j=gunpropdict['guninds'].index(bgunind)
        omc=c*gunposndict['omegagun%d' %bgunind]
        omc[omc>0.9]=1.0-0.1*numpy.exp((0.9-omc[omc>0.9])**5.0)  #if omega f Coef is >1 thats a problem to attenuate it above .9
        pstar=rates[i, :]/rates.sum(axis=0)
        if i==j:
            pstar=pstar-1
        rates[i, :]-=pstar*omc*rates[j, :]
    return rates

def MappedDepQuantities(rates, gunpropdict):
    returndict={}

    totmass=numpy.zeros(rates.shape[1], dtype='float32')
    returndict['nmolcm2']=numpy.zeros(rates.shape[1], dtype='float32')
    returndict['nm']=numpy.zeros(rates.shape[1], dtype='float32')
    returndict['gcm3']=numpy.zeros(rates.shape[1], dtype='float32')

    for ratearr, guni, M, d in zip(rates, gunpropdict['guninds'], gunpropdict['M'], gunpropdict['d']):
        returndict['nmolscm2gun%d' %guni]=ratearr
        returndict['molfracgun%d' %guni]=ratearr/rates.sum(axis=0)
        returndict['gcm3']+=d*ratearr/rates.sum(axis=0)

        returndict['massfracgun%d' %guni]=returndict['molfracgun%d' %guni]*M
        totmass+=returndict['massfracgun%d' %guni]

        returndict['nmolcm2']+=ratearr*gunpropdict['DepTime']
        returndict['nm']+=ratearr*gunpropdict['DepTime']*M/d/100.0

    for guni in gunpropdict['guninds']:
        returndict['massfracgun%d' %guni]/=totmass

    return returndict


#pd={'d': [16.690000000000001, 12.41, 12.023], 'guninds': [0, 1, 2], 'CenterMolRates': [2.0, 2.0, 2.0], 'symbol': ['Ta', 'Rh', 'Pd'], 'M': [180.94788, 102.9055, 106.42], 'voltages': [349.0, 0.0, 0.0], 'Et': [29.25, 21.899999999999999, 14.699999999999999], 'Ys': [0.83999999999999997, 1.9099999999999999, 2.4700000000000002], 'Z': [73, 45, 46], 'ProfileParams': [[19.859999999999999, 0.043208661000000002, 1.5980500000000001e-05], [8.4914000000000005, 0.030349606000000001, 3.7991000000000002e-06], [9.1099999999999994, 0.031236219999999999, 2.3715000000000001e-06]]}
#
#
#SortedRespCoef(pd)
