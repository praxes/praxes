import os
import h5py

def attrdict_def():
    return {
    'command':'mesh samx start stop numsteps samz ... counter', #this is the string entered to generate the dataset
    'elements':['', '', '', ''],
    'xgrid':(0.0,0.0,0), #mm of lowest horiztonal coordinate,  mm between point,  num of pts inrow=num columns, this is the fast scan axis
    'zgrid':(0.0,0.0,0), #same as xgrid, this is the slow scan axis
    'counter':0.0,#0.0 means unspecified. positive number is number of seconds of exposure per frame, negative number is number of fluorescence counts on XFlash (IC2)
    'cal':[1596.3, 1753.4, 558.9, .181, 272],#[horizontal pixel of beam, vertical, detector dist in mm, detector tilt in deg, tilt direction in deg], the origin for the beam center is upper left pixel=(0,0), fit2D uses lower left=(1,1), these numbers are all assumed to come from fit2D
    'alpha':50, #sample tilt in deg where 0 is substrate perpendicular to beam. this is 90deg??360 but depends on chi???-phi in the 4circle goniometer
    'bcknd':'min', #string for user to specify the type of background subtraction to be used in analysis
    'wavelength':0.02066, #x-ray wavelength in nm
    'xrdname':'mar345', 
    'psize':0.1, 
    }

#def attrdict_def():
#    return {
#    'command':'mesh samx start stop numsteps samz ... counter', #this is the string entered to generate the dataset
#    'elements':['', '', '', ''],
#    'xgrid':(0.0,0.0,0), #mm of lowest horiztonal coordinate,  mm between point,  num of pts inrow=num columns, this is the fast scan axis
#    'zgrid':(0.0,0.0,0), #same as xgrid, this is the slow scan axis
#    'counter':0.0,#0.0 means unspecified. positive number is number of seconds of exposure per frame, negative number is number of fluorescence counts on XFlash (IC2)
#    'cal':[1582.0, 1766.5, 549.9, 0.08, 125.0],#[horizontal pixel of beam, vertical, detector dist in mm, detector tilt in deg, tilt direction in deg], the origin for the beam center is upper left pixel=(0,0), fit2D uses lower left=(1,1), these numbers are all assumed to come from fit2D
#    'alpha':46.4, #sample tilt in deg where 0 is substrate perpendicular to beam. this is 90deg??360 but depends on chi???-phi in the 4circle goniometer
#    'bcknd':'minanom', #string for user to specify the type of background subtraction to be used in analysis
#    'wavelength':0.0207#x-ray wavelength in nm
#    }

#def attrdict_def():
#    return {
#    'command':'mesh samx start stop numsteps samz ... counter', #this is the string entered to generate the dataset
#    'elements':'AaXBb',#this is a string that should be element symbols in gun1,gun2,gun3 opt gun4 order with an X if that gun not used, e.g. TaXRu
#    'xgrid':(0.0,0.0,0), #mm of lowest horiztonal coordinate,  mm between point,  num of pts inrow=num columns, this is the fast scan axis
#    'zgrid':(0.0,0.0,0), #same as xgrid, this is the slow scan axis
#    'counter':0.0,#0.0 means unspecified. positive number is number of seconds of exposure per frame, negative number is number of fluorescence counts on XFlash (IC2)
#    'cal':[1535.3, 1704.5, 516.6, 0.0558, -170.3],#[horizontal pixel of beam, vertical, detector dist in mm, detector tilt in deg, tilt direction in deg], the origin for the beam center is upper left pixel=(0,0), fit2D uses lower left=(1,1), these numbers are all assumed to come from fit2D
#    'alpha':46.0, #sample tilt in deg where 0 is substrate perpendicular to beam. this is 90deg-phi in the 4circle goniometer
#    'bcknd':'minanom', #string for user to specify the type of background subtraction to be used in analysis
#    'wavelength':0.02068#x-ray wavelength in nm
#    }

#'piclist':[0]#list of ints, the point #s to be used in analysis, this must be a subset of the point #s for which files exist

# 'file0':'combi.20070101sub1mesh.1_000.mar3450', #example raw data file name with the mar3450 extension

def integration_params():
    qmin=16.0 #all values in 2pi/nm
    qmax=101.0
    qint=0.1
    return [qmin, qmax, qint]

def defaultdir(st):
    d={\
    'runlog' : 'C:/Users/JohnnyG/Documents/CHESS/CHESS2010/CHESS2010runlogs', \
    'h5' : 'C:/Users/JohnnyG/Documents/CHESS/CHESS2010/CHESS2010h5analysis', \
    'dataimport' : 'C:/Users/JohnnyG/Document/CHESS/CHESS2010/CHESS2010h5analysis',  \
    'otherdata' : 'C:/Users/JohnnyG/Documents/CHESS/CHESS2010',  \
    'pdfentries': 'C:/Users/JohnnyG/Documents/CHESS/CHESSANALYSISARRAYS' \
    }

    if st in d.keys() and os.path.isdir(d[st]):
        return d[st]
    else:
        return os.getcwd()

def chessrun_def():
    return '2010Mar'

def CHESSRUNFILE(mode='r', returnpathonly=False):
    if mode!='r':
        mode='r+'#to avoid 'w'
    path='C:/Users/JohnnyG/Documents/CHESS/CHESSANALYSISARRAYS/attrs_maps.h5'
    if returnpathonly:
        return path
    return h5py.File(path,mode=mode)

def WAVESET1dFILE(mode='r'):
    if mode!='r':
        mode='r+'#to avoid 'w'
    return h5py.File('C:/Users/JohnnyG/Documents/CHESS/CHESSANALYSISARRAYS/waveset1d.h5',mode=mode)

def DEPPROFILETXT():
    return open('C:/Users/JohnnyG/Documents/CHESS/CHESSANALYSISARRAYS/parameter database.txt', "r")


def PYMCACFGpath(temp=False):
    if temp:
        return 'C:/Users/JohnnyG/Documents/CHESS/CHESSANALYSISARRAYS/temppymca.cfg'
    else:
        return 'C:/Users/JohnnyG/Documents/CHESS/CHESSANALYSISARRAYS/pymca.cfg'

def ETHRESHYSTARTXT():
    return open('C:/Users/JohnnyG/Documents/CHESS/CHESSANALYSISARRAYS/ElementEthreshYstar.txt', "r")

def MINIPROGRAMpath():
    return 'C:/Users/JohnnyG/Documents/CHESS/CHESSANALYSISARRAYS/miniprogramdatabase.txt'

def XRFINFOpath():
    return 'C:/Users/JohnnyG/Documents/CHESS/CHESSANALYSISARRAYS/xrfinfodatabase.txt'
