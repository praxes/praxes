import copy
import operator

import numpy
from PyMca import ConfigDict
from PyMca import ClassMcaTheory
from PyMca.ConcentrationsTool import ConcentrationsTool
import PyMca.Elements as PyMEl

from XRDdefaults import *


def getcfgdict_txt(cfgpath):
    return ConfigDict.ConfigDict(filelist=cfgpath)

def addElTrcfg(pymcacfg, eltr):
    if isinstance(eltr, str):
        elstr=[eltr]
    for et in eltr:
        el, garbage, tr=et.partition(' ')
        if el in pymcacfg['peaks'].keys():
            if isinstance(pymcacfg['peaks'][el], list):
                if not tr in pymcacfg['peaks'][el]:
                    pymcacfg['peaks'][el]+=[tr]
            else:
                if tr!=pymcacfg['peaks'][el]:
                    pymcacfg['peaks'][el]=[pymcacfg['peaks'][el], tr]
        else:
            pymcacfg['peaks'][el]=tr
    return pymcacfg

def FindXrays(elsym, energy=60.0, minenergy=1.0, maxenergy=35.0, minrate=0.00010):
    xr=['K', 'L', 'M']
#    chosenxr=[]
#    chosenxren=[]
    foundpeaks=[]
    allpeaksdictlist=[]
    eltr_quantels=[]
    for ele in elsym:
        ElDict={}
        PyMEl._updateElementDict(ele, ElDict, energy=energy, minenergy=minenergy, minrate=minrate)
        xray_en_rate=[[x, ElDict[tr]['energy'], ElDict[tr]['rate']] for x in xr for tr in ElDict['%s xrays' %x] if ElDict[tr]['energy']<maxenergy]
        xraytypes=set([xer[0] for xer in xray_en_rate])
        totyieldlist=[]
        eltrlist=[]
        for xt in xraytypes:
            totyield=numpy.float32([v for k, v in PyMEl.Element[ele].iteritems() if k.startswith('omega'+xt.lower())]).sum()
            totyieldlist+=[totyield]
            en_rate=[[xer[1], xer[2]] for xer in xray_en_rate if xer[0]==xt]
            en_rate=numpy.float32(en_rate)
            enofmaxrate=en_rate[numpy.argmax(en_rate[:, 1]), 0]
            eltrlist+=[' '.join((ele, xt))]
            dt={}
            dt['el']=ele
            dt['tr']=xt
            dt['eltr']=' '.join((ele, xt))
            dt['repen']=enofmaxrate
            dt['totyield']=totyield
            allpeaksdictlist+=[dt]

#        if len(xraytypes)>1:
#            tempstr=' and '.join(list(xraytypes))
#            print 'XRF ANALYSIS PROBLEM: ', tempstr, ' transitions can be fit but only one will be chosen for', ele
        if len(xraytypes)==0:
            print 'XRF ANALYSIS PROBLEM: no valid transitions could be found for ', ele
            foundpeaks+=[False]
        else:
            foundpeaks+=[True]
            eltr_quantels+=[eltrlist[numpy.argmax(numpy.float32(totyieldlist))]]

#            xray_en_rate=sorted(xray_en_rate, key=operator.itemgetter(2), reverse=True)
#            print xray_en_rate
#            chosenxr+=[' '.join((ele, xray_en_rate[0][0]))]
#            chosenxren+=[xray_en_rate[0][1]]
#    return chosenxr, chosenxren, foundpeaks
    return allpeaksdictlist, eltr_quantels, foundpeaks



class XRFanalyzer():
#counts is expected to be the full set of acquisisiont points in its first index. pointlist gives the subset of these indeces to use and all other arrays are only the length of pointlist.
#est_film_comp=None means use the cetner compisition for every estimate. if a value is passed the value must be a nxm array where n is the length of pointindlist and m is the number of elments AND est_film_nm bust be length n array
#if a suitable transition is not found for an element then that element is completely ignored - in composition, density and thickness
#if more than one suitable type of transition (K,L,M) is found then the one that has the transition with the highest rate is used and the other type is IGNORED so check the fits
# the defult flux in the .cfg will be used if pointind_fluxcal=None, flux=None. If pointind_fluxcal has a value that point will be used and the est_film_nm value will be used to make the flux consistent with that thickness. If If pointind_fluxcal=None and flux is passed a vlue, that value will be used.
# SecondaryAction currently accepts 'Ignore' or 'Notify'. The latter will use the converged compositions in one additional calculation where EVERY film element and the underlayer serve as secondary source and a message will be printed if any of the film compositions differ by SecondaryTol. Maybe a third 'Include' option can be added.
#POINT BY POINT LISTS OR ARRAYS ARE EITHER  ***THE LENGTH OF pointlist OR ***THE LENGTH OF counts AND INDEXED BY AN ELEMENT OF pointlist.
# if densfcn is None, the default function will be used. If a function is passed, that function will be used for all points. If a list of functions is passed, it should be the length of pointlist. the function argument must be  the composition array and ANY OTHER VARIABLES MUST BE ASSIGNED AS GLOBAL VARIBLES  BEFORE EXECUTING XRFanalyzer. same goes for mffcn
#EVERYTHING IS TYPE 1. EXCEPT FOR counts AND daqtime
#    def __init__(self, counts, gunpropdict, pointlist=None, beamenergy=60.0, est_film_comp=None, est_film_nm = 100.0, SecondaryAction='Ignore', SecondaryTol=0.01, Sicm=0.04, Underlayer_El_d_nm=('Ti', 4.5, 12.0), BckndCounts=None, pointind_fluxcal=None, flux=None, cfgpath=None, daqtime=1.0, mf_tol=0.0001, max_iter=20):
    def __init__(self, counts, elements, quantElTr, eld, elM, BckndCounts=None, RepEn=None, cfgpath=None,  otherElTr=[], pointlist=None, beamenergy=60., est_film_comp=None, est_film_nm = 100.0,  SecondaryAction='Ignore', Sicm=.04, Underlayer_El_d_nm=('Ti', 4.5, 12.0), pointind_fluxcal=None,  flux=None, daqtime=1., mf_tol=0.0005, max_iter=20, SecondaryTol=0.005, densfcn=None, mffcn=None):

        #gunpropdict must have 'symbols' and the rest will be filled in otherwise
        if pointlist is None:
            pointlist=range(counts.shape[0])

        self.peaks_quant=quantElTr
        if RepEn is None:
            self.peaks_representativenergy=numpy.zeros(len(self.peaks_quant))
        else:
            self.peaks_representativenergy=numpy.float32(RepEn)
        self.symb=elements
        self.dens=numpy.float32(eld)
        self.mass=numpy.float32(elM)
#        global d
#        global M
#        d=self.dens
#        M=self.mass

        if densfcn is None:
            densfcn=[None]*len(pointlist)
        elif isinstance(densfcn, list):
            if len(densfcn)!=len(pointlist):
                print 'WARNING: list of lambda functions for density not same length as pointlist'
        else:
            densfcn=[densfcn]*len(pointlist)

        if mffcn is None:
            mffcn=[None]*len(pointlist)
        elif isinstance(mffcn, list):
            if len(mffcn)!=len(pointlist):
                print 'WARNING: list of lambda functions for density not same length as pointlist'
        else:
            mffcn=[mffcn]*len(pointlist)

        if BckndCounts is None:
            self.BckndCounts=numpy.zeros(len(self.symb), dtype='float32')
        else:
            self.BckndCounts=BckndCounts


        if isinstance(daqtime, float):
            daqtime=numpy.ones(counts.shape[0], dtype='float32')*daqtime

        if est_film_comp is None:
            est_film_comp=numpy.ones(len(self.symb), dtype='float32')/len(self.symb)
        est_film_comp=numpy.float32(est_film_comp)


        if len(est_film_comp.shape)==1:
            est_mf=numpy.float32([est_film_comp*self.mass/(est_film_comp*self.mass).sum()]*len(pointlist))
            est_film_thickness = numpy.float32([est_film_nm*10.0**(-7.0)]*len(pointlist))
            est_film_density=[]
            for df in densfcn:
                if df is None:
                    est_film_density+= [(est_film_comp*self.dens).sum()]
                else:
                    est_film_density+= [df(est_film_comp)]
            est_film_density=numpy.float32(est_film_density)


        else:
            est_film_comp=est_film_comp.T[numpy.where(est_film_comp)].T#i don't know what it was for but should not be necessary
            temp=est_film_comp*self.mass
            est_mf=(temp.T/temp.sum(axis=1)).T

            est_film_thickness = est_film_nm*10.0**(-7.0)

            est_film_density=[]
            for df, estc in zip(densfcn, est_film_comp):
                if df is None:
                    est_film_density+= [(estc*self.dens).sum()]
                else:
                    est_film_density+= [df(estc)]
            est_film_density=numpy.float32(est_film_density)

        if cfgpath is None:
            cfgpath=PYMCACFGpath()

        self.pymca_config = ConfigDict.ConfigDict(filelist=cfgpath)

        self.pymca_config=addElTrcfg(self.pymca_config, quantElTr+otherElTr)

        if Underlayer_El_d_nm[2]>0: #even if not in the fit list, add the layer for mass attentuation
            self.pymca_config['multilayer']['Layer1'][1] = Underlayer_El_d_nm[0]+'1'
            self.pymca_config['multilayer']['Layer1'][2] = Underlayer_El_d_nm[1]
            self.pymca_config['multilayer']['Layer1'][3] = Underlayer_El_d_nm[2]*10.0**(-7.0)
            silayer='Layer2'
        else:
            self.pymca_config['multilayer']['Layer1'] = copy.deepcopy(self.pymca_config['multilayer']['Layer2'])
            del self.pymca_config['multilayer']['Layer2']
            silayer='Layer1'
        if Sicm>0:
            self.pymca_config['multilayer'][silayer][3] = Sicm
        else:
            del self.pymca_config['multilayer'][silayer]

        self.pymca_config['materials']['FILM']['CompoundList']=self.symb
        self.det_dist = self.pymca_config['concentrations']['distance']
        self.det_area = self.pymca_config['concentrations']['area']
        if not (pointind_fluxcal is None):
            i=pointlist.index(pointind_fluxcal)
            if counts[pointind_fluxcal][:].sum() > 1000:

                self.pymca_config['concentrations']['time']=daqtime[pointind_fluxcal]

                self.pymca_config['materials']['FILM']['CompoundFraction'] = list(est_mf[i])
                self.pymca_config['materials']['FILM']['Thickness'] = est_film_thickness[i]
                self.pymca_config['materials']['FILM']['Density'] = est_film_density[i]

                self.pymca_config['multilayer']['Layer0'][2] = est_film_density[i]
                self.pymca_config['multilayer']['Layer0'][3] = est_film_thickness[i]

                self.pymca_config['attenuators']['Matrix'][2] = est_film_density[i]
                self.pymca_config['attenuators']['Matrix'][3] = est_film_thickness[i]

#                TEST1=copy.deepcopy(self.pymca_config)
#                flux=self.FitProcessIterator(copy.deepcopy(self.pymca_config), counts[pointind_fluxcal][:], mf_tol, max_iter, FluxCalibration=True)

#Jan 2010 changed flux calibration. above works on massfrac but seems to give very different result thatn below, which just makes sure the thickness matches the calibration thickness in a self-consistent calculation where only the flux is updated on each iteration

                b=calcthick
                j=0
                print '!@!@', est_film_thickness[i]
                while numpy.abs(calcthick-est_film_thickness[i])/est_film_thickness[i]>.01 and j < max_iter:
                    print 'iteration,flux ',  j,  self.pymca_config['concentrations']['flux']
                    j+=1
                    garb, calcthick, garb, garb=self.FitProcessIterator(copy.deepcopy(self.pymca_config), counts[pointind_fluxcal][:], mf_tol, max_iter, SecondaryAction=SecondaryAction, SecondaryTol=SecondaryTol, densfcn=densfcn[i], mffcn=mffcn[i])
                    print 'est calc thickness',  est_film_thickness[i], calcthick
                    self.pymca_config['concentrations']['flux']*=calcthick/est_film_thickness[i]

                if j==max_iter:
                    print 'SUFFICIENT FLUX CALIBRATION NOT ATTAINED'
                print "Calibrated flux is ", self.pymca_config['concentrations']['flux'] ,"  flux*time=", daqtime[i]*self.pymca_config['concentrations']['flux']

        if not (flux is None):
            self.pymca_config['concentrations']['flux']=flux


        self.comp_res = numpy.zeros((len(counts), len(self.symb)), dtype='float32')
        self.thick_res = numpy.zeros(len(counts), dtype='float32')
        self.cfgstr=['']*len(counts)
        self.resultdict=[{} for garbage in range(len(counts))]

        for ind, emf, ethick, edens, df, mff in zip(pointlist, est_mf, est_film_thickness, est_film_density, densfcn, mffcn):
            print ind

            spectrum=counts[ind][:]
            if spectrum.sum() < 1000:
                continue

            self.pymca_config['concentrations']['time']=daqtime[ind]
            self.pymca_config['materials']['FILM']['CompoundFraction'] = list(emf)
            self.pymca_config['materials']['FILM']['Thickness'] = ethick
            self.pymca_config['materials']['FILM']['Density'] = edens

            self.pymca_config['multilayer']['Layer0'][2] = edens
            self.pymca_config['multilayer']['Layer0'][3] = ethick

            self.pymca_config['attenuators']['Matrix'][2] = edens
            self.pymca_config['attenuators']['Matrix'][3] = ethick

            resdict={}
#            TEST2=copy.deepcopy(self.pymca_config)
#            for k, v in TEST2.iteritems():
#                if TEST1[k]!=v:
#                    print k, ' is different'
#                    print 'TeST1', TEST1[k]
#                    print 'TeST1', v
            self.comp_res[ind, :], self.thick_res[ind],self.cfgstr[ind], resdict=self.FitProcessIterator(copy.deepcopy(self.pymca_config), spectrum, mf_tol, max_iter, SecondaryAction=SecondaryAction, SecondaryTol=SecondaryTol, densfcn=df, mffcn=mff)
            self.thick_res[ind]*=10.**7.
            for k in resdict['groups']:
                self.resultdict[ind][k]=copy.deepcopy(resdict[k])
#        if True:
#            del d
#            del M



    def FitProcessIterator(self, pymca_config, spectrum, mf_tol, max_iter, FluxCalibration=False, SecondaryAction='Ignore', SecondaryTol=0.01, mf_tol_multiplier_secondtry=20., densfcn=None, mffcn=None):
        tot_calc_mf = 0
        j = 0
        feedback=1. #level of feedback in changing the thickness for the next iteration. from 0 to 1
        missedhighbool=None
        mf_setpt=1.0

        while ((abs(tot_calc_mf - mf_setpt) > mf_tol) or j<2) and j < max_iter:

            calc_mf, result=self.FitProcessSpectrum(pymca_config, spectrum)

            tot_calc_mf=calc_mf.sum()
            norm_calc_mf=calc_mf/tot_calc_mf
            film_ave_mw = 1/(norm_calc_mf/self.mass).sum()
            calc_comp=film_ave_mw*norm_calc_mf/self.mass

            print 'iteration %d:' %j, calc_comp, tot_calc_mf, pymca_config['materials']['FILM']['Thickness']*1e7

            if missedhighbool is None:
                missedhighbool=tot_calc_mf>mf_setpt
            temp=missedhighbool
            missedhighbool=tot_calc_mf>mf_setpt
            if temp!=missedhighbool:#if alternating about the setpt, lower the gain of the feedback
                feedback*=.7



            if FluxCalibration:
                print 'itertion, totmassfrac,flux:', j, tot_calc_mf, pymca_config['concentrations']['flux']
                pymca_config['concentrations']['flux'] *= tot_calc_mf
            else:
                if numpy.any(calc_comp<0.):
                    print 'ABORTING THIS POINT - NEGATIVE COMPOSITIONS MADE ZERO'
                    NegCompFlag=True
                    calc_comp[calc_comp<0.]=0.
                    calc_comp/=calc_comp.sum()
                    tot_calc_mf=mf_setpt
                    j=max_iter
                    thickness = pymca_config['materials']['FILM']['Thickness']
                    continue
                else:
                    NegCompFlag=False

                if densfcn is None:
                    density = (calc_comp*self.dens).sum()
                else:
                    density=densfcn(calc_comp)

                if not mffcn is None:
                    mf_setpt=mffcn(calc_comp)

                pymca_config['materials']['FILM']['CompoundFraction'] = list(norm_calc_mf)
                pymca_config['materials']['FILM']['Density'] = density
                pymca_config['multilayer']['Layer0'][2] = density
                pymca_config['attenuators']['Matrix'][2] = density
                thickness = pymca_config['materials']['FILM']['Thickness'] * (1.-feedback*(mf_setpt-tot_calc_mf))
                pymca_config['materials']['FILM']['Thickness'] = thickness
                pymca_config['multilayer']['Layer0'][3] = thickness
                pymca_config['attenuators']['Matrix'][3] = thickness

            j += 1
            if j==max_iter:
                if not mf_tol_multiplier_secondtry is None:
                    mf_tol*=mf_tol_multiplier_secondtry
                    mf_tol_multiplier_secondtry=None
                    j=0
                    print  'XRF algorithm did not converge on first pass, increasing massfrac tolerance to ', mf_tol
        if j==max_iter:
            print 'PROBLEM!: XRF algorithm did not converge - it quit with a final tot mass frac of ', tot_calc_mf

        if not NegCompFlag:
            print 'd, setpt:', density, mf_setpt

        #for SecondaryAction=='Notify' it is important that this comes first but for 'Include' it should come after
        pymca_config.write(PYMCACFGpath(temp=True))
        f=open(PYMCACFGpath(temp=True),mode='r')
        cfgstr=f.read()
        f.close()
        return_result=copy.deepcopy(result)
        if not NegCompFlag and SecondaryAction=='Notify':
            pymca_config_2ndary=copy.deepcopy(pymca_config)
            #print self.peaks_quant, self.peaks_representativenergy
            eltr=numpy.array(self.peaks_quant)[self.peaks_representativenergy>0]
            repen=self.peaks_representativenergy[self.peaks_representativenergy>0]
            for i, (pk, en) in enumerate(zip(eltr, repen)):
                calc_counts = result[pk]['fitarea']
                calc_yield = calc_counts * 4. * numpy.pi * self.det_dist**2 / self.det_area
                pymca_config_2ndary['fit']['energy'][i+1]=en
                pymca_config_2ndary['fit']['energyweight'][i+1] = calc_yield / pymca_config_2ndary['concentrations']['flux']
                pymca_config_2ndary['fit']['energyflag'][i+1]=1
            sec_calc_mf, result=self.FitProcessSpectrum(pymca_config, spectrum)
            sec_tot_calc_mf=sec_calc_mf.sum()
            sec_norm_calc_mf=sec_calc_mf/sec_tot_calc_mf
            sec_film_ave_mw = 1/(sec_norm_calc_mf/self.mass).sum()
            sec_calc_comp=sec_film_ave_mw*sec_norm_calc_mf/self.mass
            if numpy.max(numpy.abs(numpy.float32(calc_comp)-numpy.float32(sec_calc_comp)))>SecondaryTol:
                print 'WARNING: Secondary Emissions changed compositions: ', self.symb, ' from ', calc_comp, ' to ', sec_calc_comp

        if FluxCalibration:
            return pymca_config['concentrations']['flux']
        else:
            #array of atomic fractions
            return numpy.float32(calc_comp), thickness, cfgstr, return_result




    def FitProcessSpectrum(self, pymca_config, spectrum):
        advancedFit = ClassMcaTheory.McaTheory(config=pymca_config)
        advancedFit.enableOptimizedLinearFit()
        mfTool = ConcentrationsTool(pymca_config)
        tconf = mfTool.configure()

        advancedFit.config['fit']['use_limit'] = 1
        advancedFit.setdata(y=spectrum)
        advancedFit.estimate()

        fitresult, tmpresult = advancedFit.startfit(digest=1)
        tmpresult = advancedFit.imagingDigestResult()

        temp = {}
        temp['fitresult'] = fitresult
        temp['result'] = tmpresult
        for bcts, pk in zip(self.BckndCounts, self.peaks_quant):
            tmpresult[pk]['fitarea']-=bcts
        temp['result']['config'] = advancedFit.config
        tconf.update(advancedFit.configure()['concentrations'])
        conc = mfTool.processFitResult(config=tconf, fitresult=temp,
                                       elementsfrommatrix=False,
                                       fluorates=advancedFit._fluoRates)

        calc_mf=numpy.float32([conc['mass fraction'][pk] for pk in self.peaks_quant])
        return calc_mf, tmpresult



#xa=XRFanalyzer(counts, gunpropdict, pointlist=pointlist, beamenergy=60.0, est_film_comp=None, est_film_nm = 100.0, SecondaryAction='Notify', SecondaryTol=0.001, Sicm=0.04, Underlayer_El_d_nm=('Ti', 4.5, 12.0), BckndCounts=None, pointind_fluxcal=None, flux=None, mf_tol=0.00001, max_iter=20)

#for i, (arrcomp, th) in enumerate(zip(xa.comp_res,  xa.thick_res)):
#    if i in pointlist:
#        print arrcomp, th
#print xa.resultdict[pointlist[0]]
#print len(xa.cfgstr[pointlist[0]])

