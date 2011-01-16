global XRFALLOWED
try:
    from xrf_analysis import *
    XRFALLOWED=True
except:
    XRFALLOWED=False

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from XRDdefaults import *
from xrd_fileIO_fcns import *
from xrd_math_fcns import *
from xrdPLOT import *
from xrd_diffraction_conversion_fcns import *
from xrf_depprof import *

import numpy, scipy.interpolate, pylab, operator, sys, os, time, copy, h5py, matplotlib, matplotlib.cm
import ui_mainmenu
import ui_message_box
import ui_import_image
import ui_import_attr
import ui_chessrunattr
import ui_get_group
import ui_int_params
import ui_chi_params
import ui_qq_params
import ui_h5file_info
import ui_analyze_qq
import ui_wavepeak_1d
import ui_associate_pkqq
import ui_associationtree
import ui_make_phases_menu
import ui_spatial_phases_menu
import ui_highlowDialog
import ui_bmin_menu
import ui_chiqDialog
import ui_plotsomenu
import ui_XRDSuite_params
import ui_h5scanDialog
import ui_pdfDialog
import ui_waveset1d_params
import ui_dep_prof
import ui_xrf_analysis
import ui_test
import ui_buildnewscan
import ui_mini_program_dialog
import ui_pdfsearch
import ui_LinBckndDialog
import ui_bckndinventoryDialog
import ui_editrawxrdDialog
#import ui_emptydialog


#def dummytask(secs):
#    print 'dummy task exectued'
#    time.sleep(secs)

def printtime():
    print time.ctime()
    
def mygetopenfile(parent=None, xpath="%s" % os.getcwd(),markstr='', filename='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getOpenFileName(xparent,''.join(['Select file to open:', markstr]),os.path.join(xpath, filename).replace('\\','/')))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getOpenFileName(parent,''.join(['Select file to open: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))

def mygetsavefile(parent=None, xpath="%s" % os.getcwd(),markstr='', filename='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getSaveFileName(xparent,''.join(['Select file for save: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getSaveFileName(parent,''.join(['Select file for save: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))

def mygetdir(parent=None, xpath="%s" % os.getcwd(),markstr='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getExistingDirectory(xparent,''.join(['Select directory:', markstr]), xpath))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getExistingDirectory(parent,''.join(['Select directory:', markstr]), xpath))

class MainMenu(QMainWindow,
        ui_mainmenu.Ui_MainMenu):

    def __init__(self, parent=None, datpath="%s" % os.getcwd(), h5path="%s" % os.getcwd(), runpath="%s" % os.getcwd()):
        super(MainMenu, self).__init__(parent)
        self.setupUi(self)
        self.datpath = datpath
        self.h5path = h5path
        self.runpath = runpath
        self.activepathcompare='xxxxxxxxx'
        self.setallowedtasks()

    def updateactivepath(self):
        self.activepathcompare=''.join((os.path.split(self.h5path)[1], '  ', self.h5groupstr))
        self.active_file_lineEdit.setText(self.activepathcompare)

    def clearactivepath(self):
        self.activepathcompare='xxxxxxxxx'
        self.active_file_lineEdit.setText('')

    def setallowedtasks(self):
        self.actionXRF_analysis.setEnabled(XRFALLOWED)

    @pyqtSignature("")
    def on_performPushButton_clicked(self):
        self.tasktext=unicode(self.taskTextBrowser.toPlainText())
        self.tasktext=self.tasktext.strip()
        self.tasktext=''.join((self.tasktext, '\n'))
        self.performtasks()

    def performtasks(self):
        errorstr=''
        try:
            ACTIVEPATH=self.h5path
            ACTIVEGRP=self.h5groupstr
        except:
            print 'NO ACTIVE PATH AND GROUP HAVE BEEN DEFINED'
        self.lineendlist=[-1]
        i=0
        while i!=-1:
            i=self.tasktext.find('\n', i+1)
            if i!=-1:
                self.lineendlist+=[i]
        for i in range(len(self.lineendlist)-1):
#            self.taskTextBrowser.setPlainText(''.join((self.tasktext[0:self.lineendlist[i]+1], '*', self.tasktext[self.lineendlist[i]+1:])))
#            self.repaint()
            cmdstr=self.tasktext[self.lineendlist[i]+1:self.lineendlist[i+1]]
            print 'performing: ', cmdstr
            if cmdstr.startswith('ACTIVEPATH='):
                ACTIVEPATH=eval(cmdstr.partition('ACTIVEPATH=')[2])
            elif cmdstr.startswith('ACTIVEGRP='):
                temp=cmdstr.partition('ACTIVEGRP=')[2]
                if 'DEFAULT' in temp:
                    ACTIVEGRP=getdefaultscan(ACTIVEPATH)
                else:
                    ACTIVEGRP=eval(temp)
            else:
                errormsg=eval(cmdstr)
                if not errormsg is None:
                    errorstr+='ERROR in '+cmdstr+ '\n\n'+errormsg
        if len(errorstr)>0:
            QMessageBox.warning(self,"ERROR REPORT",  errorstr)

        else:
            QMessageBox.information(self, 'tasks Complete!', 'click "OK" to clear task list and continue program')
            self.taskTextBrowser.setPlainText('')
        self.setallowedtasks()

    @pyqtSignature("")
    def on_action_mini_program_txt_triggered(self):
        idialog=mini_program_dialog(self)
        if idialog.exec_():
            self.addtask(idialog.cmdtext)

    @pyqtSignature("")
    def on_action_synthimport_triggered(self):
        synthpath=mygetopenfile(parent=self, markstr='synth txt file')
        if len(synthpath)==0:
            return

        h5dir=mygetdir(parent=self, markstr='h5 save dir')
        if len(h5dir)==0:
            return
        print len(synthpath), len(h5dir)
        h5name=os.path.split(synthpath)[1]+'.h5'
        h5path=os.path.join(h5dir, h5name).replace('\\','/')
        self.addtask("createsynthetich5_peaktxt('"+h5path+"', '"+ synthpath+ "', elstr='ABC')")

    @pyqtSignature("")
    def on_action_import_txt_XRD_data_triggered(self):
        synthpath=mygetopenfile(parent=self, markstr='first of txt files')
        if len(synthpath)==0:
            return

        h5dir=mygetdir(parent=self, markstr='h5 save dir')
        if len(h5dir)==0:
            return
        print len(synthpath), len(h5dir)
        h5name=os.path.split(synthpath)[1]+'.h5'
        h5path=os.path.join(h5dir, h5name).replace('\\','/')
        self.addtask("createh5_txtfiles('"+h5path+"', '"+ synthpath+ "', headerlines=0, elstr='ABC')")

    @pyqtSignature("")
    def on_action_exportpeak_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for peak export')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            exportpeaklist(self.h5path, self.h5groupstr, self.runpath)

    @pyqtSignature("")
    def on_action_bckndinventory_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for peak export')
            if temp!='':
                h5pathtemp=temp
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        #QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=bckndinventoryDialog(self, self.h5path, h5groupstr=self.h5groupstr)
        else:#if didn't find a groupstr the traditional way then find any group that has XRD data
            h5file=h5py.File(h5pathtemp, mode='r')
            grpnames=[]
            for group in h5file.iterobjects():
                if isinstance(group,h5py.Group)  and 'measurement' in group:
                    group=group['measurement']
                    for xrdgrp in XRDgroupnames():
                        if xrdgrp in group and isinstance(group[xrdgrp],h5py.Group) and 'counts' in group[xrdgrp]:
                            grpnames+=[group[xrdgrp].name]
            h5file.close()
            perform=len(grpnames)>0
            if not perform:
                print 'no XRD data found in .h5 file'

            if perform:
                idialog=selectorDialog(self, grpnames, title='Select an experiment group')
                perform=idialog.exec_()
                
            if perform:
                h5grppath=str(idialog.groupsComboBox.currentText())
                idialog=bckndinventoryDialog(self, h5pathtemp, h5grppath=h5grppath)
                idialog.exec_()
            
    @pyqtSignature("")
    def on_action_neighbor_calculation_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for neighbor calculation')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=neighborwindow(self, self.h5path, self.h5groupstr, self.runpath)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_plot_sample_info_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for sample info plotting')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plotinterpimageof1ddatawindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex(), style='info')
            idialog.exec_()

    @pyqtSignature("")
    def on_action_textureanalysis_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for texture analysis')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plotinterpimageof1ddatawindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex(), style='texture')
            idialog.exec_()

    @pyqtSignature("")
    def on_action_import_sample_info_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for sample info import')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            importfilepath = mygetopenfile(self, xpath=defaultdir('otherdata'), markstr='pointind, number data', filename='.txt' )
            perform=importfilepath!=''
        if perform:
            importsampleinfotoh5(self.h5path, self.h5groupstr, importfilepath)


    @pyqtSignature("")
    def on_action_export_XRDSuite_files_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for 1d->.plt')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]

            perform=('icounts' in h5mar)
            if not perform:
                QMessageBox.warning(self,"failed",  'ABORTED: cannot find necessary data')
        if perform:
            pointlist=h5analysis.attrs['pointlist']
            qgrid=h5mar['icounts'].attrs['qgrid']
            qvals=q_qgrid_ind(qgrid)

            xtypelist=['q 1/nm','2th (deg)','d (nm)','pixels']

            opts=['icounts']
            if 'ifcounts' in h5mar:
                opts+=['ifcounts (processed)']

            idialog=XRDSuiteDialog(self, xtypelist, 'select a scattering variable',  opts, 'select a type of 1d intensity array', qvals[0], qvals[-1])

            if idialog.exec_():   #no exec_ if perform False
                scale=idialog.scaleCheckBox.isChecked()
                dpbool=idialog.CompComboBox.currentIndex()==1
                xrfbool=idialog.CompComboBox.currentIndex()==1
                imtype=unicode(idialog.imtypeComboBox.currentText()).partition(' ')[0]
                if imtype.startswith('if'):
                    counts=readh5pyarray(h5mar['ifcounts'])
                else:
                    counts=readh5pyarray(h5mar['icounts'])

                xtype=unicode(idialog.xtypeComboBox.currentText())
                low=idialog.qminSpinBox.value()
                high=idialog.qmaxSpinBox.value()
                lowind=numpy.where(qvals>=low)[0][0]
                highind=qvals.shape[0]-numpy.where(qvals[-1:0:-1]<=high)[0][0]
                qvals=qvals[lowind:highind]
                attrdict=getattr(self.h5path, self.h5groupstr)
                L=attrdict['cal'][2]
                wl=attrdict['wavelength']
                psize=attrdict['psize']
                elstr=attrdict['elements']

                types=['x(mm)', 'z(mm)']
                if scale:
                    types+=['DPnmolcm2']
                if xrfbool:
                    comptype='XRFmolfracALL'
                elif dpbool:
                    comptype='DPmolfracALL'
                else:
                    comptype=None

                if not comptype is None:
                    elstrlist, compsarr=getternarycomps(self.h5path, self.h5groupstr, elstr=elstr, infotype=comptype)
                    elstr='\t'.join(elstrlist)
                    compsstr=elstr

                infodict, success=getpointinfo(self.h5path, self.h5groupstr, types=types)
                if not success or (not comptype is None and compsarr is None):
                    print 'ABORTING: not all info could be found'
                    return

                if scale:
                    scalearr=1/infodict['DPnmolcm2']
                else:
                    scalearr=numpy.ones(len(infodict['x(mm)']), dtype='float32')
                coordsarr=numpy.array([infodict['x(mm)'], infodict['z(mm)']]).T


                if 'pix' in xtype:
                    xvals=pix_q(qvals, L, wl, psize=psize)
                    t1='pix'
                elif '(nm)' in xtype:
                    xvals=d_q(qvals)
#                    plotarr=numpy.array([plotarr[-1*i-1] for i in range(plotarr.size)])
#                    xvals=numpy.array([xvals[-1*i-1] for i in range(xvals.size)])
                    t1='d'
                elif '2' in xtype:
                    xvals=twotheta_q(qvals, wl)
                    t1='2th'
                else:
                    t1='q'
                    xvals=qvals
                savename='_'.join((os.path.split(self.h5path)[1][0:-3], self.h5groupstr))
                coordsfilename=os.path.join(self.runpath,''.join((savename, '_coords.txt'))).replace('\\','/')
                compsfilename=os.path.join(self.runpath,''.join((savename, '_comps.txt'))).replace('\\','/')
                countsfilename=os.path.join(self.runpath,''.join((savename, '_', imtype, '_', t1, '_counts.txt'))).replace('\\','/')
                coordsstr='x\tz'

                countsstr=''
                for x in xvals:
                    countsstr='\t'.join((countsstr, numtostring(x, 4)))
                countsstr=countsstr[1:]

                for ind in pointlist:

                    yvals=counts[ind, lowind:highind]

                    yvals*=scalearr[ind]
                    temp=''
                    for y in yvals:
                        temp='\t'.join((temp, numtostring(y, 7)))
                    countsstr='\n'.join((countsstr, temp[1:]))

                    temp=''
                    for c in coordsarr[ind]:
                        temp='\t'.join((temp, numtostring(c, 3)))
                    coordsstr='\n'.join((coordsstr, temp[1:]))

                    if not comptype is None:
                        temp=''
                        if len(compsarr[ind])==1:
                            temp='100.0'
                        else:
                            numstr=[numtostring(num*100.0, 4) for num in compsarr[ind][:-1]]
                            rest=100.0
                            for ns in numstr:
                                rest-=eval(ns)
                            numstr+=[numtostring(rest, 4)]
                            temp='\t'.join(numstr)

                            compsstr='\n'.join((compsstr, temp))

                fout=open(coordsfilename, "w")
                fout.write(coordsstr)
                fout.close()

                if not comptype is None:
                    fout=open(compsfilename, "w")
                    fout.write(compsstr)
                    fout.close()

                fout=open(countsfilename, "w")
                fout.write(countsstr)
                fout.close()
            h5file.close()


    @pyqtSignature("")
    def on_action_change_active_scan_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
            temp=self.h5path
        else:
            temp = mygetopenfile(self, xpath=self.h5path, markstr='.h5 file for changing active scan')
            perform=(temp!='')
        if perform:
            idialog=getgroupDialog(self, temp)
            if idialog.exec_():
                self.h5path=temp
                self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                self.updateactivepath()
                h5file=h5py.File(self.h5path, mode='r+')
                h5file.attrs['defaultscan']=str(self.h5groupstr)
                h5file.close()


    @pyqtSignature("")
    def on_action_initialize_scan_triggered(self):
        self.importdatadialogcontrol()

    @pyqtSignature("")
    def on_action_edit_DAQ_params_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for scan attribute edit')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            attrdicttemp = self.importattrDialogcaller(self, self.h5path, self.h5groupstr)
            if attrdicttemp is not None:
                writeattr(self.h5path, self.h5groupstr, attrdicttemp)

    @pyqtSignature("")
    def on_action_buildnewscan_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for scan attribute edit')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=buildnewscanDialog(self, self.h5path, self.h5groupstr)
            if idialog.exec_():
                destname=str(unicode(idialog.newnameLineEdit.text()))
                h5file=h5py.File(self.h5path, mode='r')
                if destname in h5file:
                    h5file.close()
                    QMessageBox.warning(self,"failed",  "Aborting because new scan name already exists")
                    return None
                h5file.close()
                self.h5groupstr=destname
                newscandict=idialog.createnewscandict()
                if not newscandict is None:
                    buildnewscan(self.h5path, self.h5groupstr, newscandict)
                    self.updateactivepath()
                    self.importdatadialogcontrol(h5path=self.h5path, h5groupstr=self.h5groupstr, command='USER-COMPILED')


    @pyqtSignature("")
    def on_actionXRF_analysis_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for XRF analysis')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=xrfanalysisDialog(self, self.h5path, self.h5groupstr)
            if idialog.exec_():
                if idialog.parstr=='' or idialog.parstr is None:
                    print 'ABORTING XRF ANALYSIS: some error'
                    return

                self.addtask(", ".join(("XRFanalysis(h5path='"+self.h5path+"'", "h5groupstr='"+self.h5groupstr+"'", idialog.parstr))+")")



    @pyqtSignature("")
    def on_actionDeposition_Profiling_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for Deposition Profile calculation')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            attrdict=getattr(self.h5path, self.h5groupstr)
            idialog=depprofDialog(self, attrdict['elements'])
            if idialog.exec_():
                gunpropdict=idialog.propdict
                xcoords=attrdict['x']
                zcoords=attrdict['z']
                mdq=MappedDepQuantities(DepRates(gunpropdict, GunPosnDict(xcoords, zcoords)), gunpropdict)
                for vals in mdq.itervalues():
                    if numpy.any(numpy.isnan(vals)):
                        print mdq
                        QMessageBox.warning(self,"failed",  'Deposition profiling aborted, NaN results. The dictionary of results was printed.')
                        return
                writedepprof(self.h5path, self.h5groupstr, gunpropdict, mdq)




    @pyqtSignature("")
    def on_action_calc_bcknd_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for background calculation')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            attrdicttemp=getattr(self.h5path, self.h5groupstr)
            if attrdicttemp is None:
                QMessageBox.warning(self,"failed",  "calc cancelled: cannot find scan attributes")
            else:
                bcknd=attrdicttemp['bcknd']
                h5file=h5py.File(self.h5path, mode='r')
                h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
                h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
                if ''.join(('b',bcknd[:3])) in h5mar:
                    tempstr=''.join((' - previous ',bcknd[:3],' background will be overwritten'))
                else:
                    tempstr=''
                h5file.close() #it i imperative thatthis be closed before LinBckndDialog executes, as 'r+' is used within
                if 'min' in bcknd:
                    idialog=bminDialog(self)
                    if not idialog.exec_():
                        return
                    othparstr=', critfrac=%0.3f' %idialog.bminpercSpinBox.value()
                elif 'lin' in bcknd:
                    idialog=LinBckndDialog(self, self.h5path, self.h5groupstr)
                    if not (idialog.exec_() and idialog.perform):
                        return
                    othparstr=', critfrac=%0.3f' %idialog.zerofracSpinBox.value()
                    othparstr+=', weightprecision=%0.3f, normrank=%0.3f' %(idialog.precisionSpinBox.value(), idialog.normrankSpinBox.value())
                else:
                    othparstr=''
                idialog=messageDialog(self, ''.join((bcknd, ' background will be calculated', tempstr)))
                if 'bin' in attrdicttemp.keys():
                    binstr='%d' %attrdicttemp['bin']
                else:
                    binstr='3'
                if idialog.exec_():
                    self.addtask(''.join(("calcbcknd(h5path='", self.h5path, "', h5groupstr='", self.h5groupstr, "', bcknd='", bcknd, "', bin=", binstr, othparstr,  ")")))
                

    @pyqtSignature("")
    def on_action_copy_lin_bcknd_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for destination')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            perform=False
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 source file: from which blin will be copied')
            if temp!='':
                idialog=getgroupDialog(self, temp)
                if idialog.exec_():
                    h5path_from=temp
                    h5groupstr_from=str(unicode(idialog.groupsComboBox.currentText()))
                    perform=True
        if perform:
            self.addtask('CopyLinBckndData(%s, %s, %s, %s)' %(h5path, h5groupstr, h5path_from, h5groupstr_from))

    @pyqtSignature("")
    def on_action_process_1d_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for background calculation')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=messageDialog(self, 'any existing processed 1D intensities will be overwritten')
            if idialog.exec_():
                self.addtask(''.join(("process1dint(h5path='", self.h5path, "', h5groupstr='", self.h5groupstr, "', maxcurv=16.2)")))

    @pyqtSignature("")
    def on_action_process_texture_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for background calculation')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            if 'texture' in h5mar:
                texgrplist=[]
                h5tex=h5mar['texture']
                for grp in h5tex.iterobjects():
                    if isinstance(grp, h5py.Group) and 'icounts' in grp:
                        texgrplist+=[grp.name.rpartition('/')[2]]
                idialog=selectorDialog(self, texgrplist, title='select texture dataset')
                h5file.close()
            else:
                h5file.close()
                print 'cannot calculate wave trans without texture data'
                return
            if len(texgrplist)>0 and idialog.exec_():
                h5texgrpname=str(idialog.groupsComboBox.currentText())
                self.addtask(''.join(("process1dint(h5path='", self.h5path, "', h5groupstr='", self.h5groupstr, "', maxcurv=16.2, type='h5tex:", h5texgrpname, "')")))


    @pyqtSignature("")
    def on_actionBinImapChimap_triggered(self):
        h5chess=CHESSRUNFILE()
        itemnames=[]
        for group in h5chess.iterobjects():
            if isinstance(group, h5py.Group):
                itemnames+=[group.name.rpartition('/')[2]]
        h5chess.close()
        idialog=selectorDialog(self, itemnames, title='select a CHESSrun group')
        if idialog.exec_():
            self.addtask(''.join(("binmapsinh5chess('",str(unicode(idialog.groupsComboBox.currentText())),"', bin=3)")))


    @pyqtSignature("")
    def on_action_plot_chessrun_arrays_triggered(self):
        perform=False
        path = mygetopenfile(self, xpath=CHESSRUNFILE(returnpathonly=True),markstr='chessrun .h5 file for background calculation')
        if path!='':
            idialog=plot2dchessrunwindow(self, path, self.runpath)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_choose_data_subset_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for background calculation')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plot2dintwindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex(), navkill=True)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_build_integration_map_triggered(self):
        h5chess=CHESSRUNFILE()
        itemnames=[]
        for group in h5chess.iterobjects():
            if isinstance(group, h5py.Group):
                itemnames+=[group.name.rpartition('/')[2]]
        h5chess.close()
        idialog=selectorDialog(self, itemnames, title='select a CHESSrun group')
        if idialog.exec_():
            idialog2=intparamDialog(self)
            if idialog2.exec_():
                qmin=idialog2.qminSpinBox.value()
                qmax=idialog2.qmaxSpinBox.value()
                qint=idialog2.qintSpinBox.value()
                qgridstr='['+','.join(tuple([labelnumberformat(num) for num in qgrid_minmaxint(qmin, qmax, qint)]))+']'
                self.addtask(''.join(("buildintmap('",str(unicode(idialog.groupsComboBox.currentText())),"',", qgridstr, ",bin=3)")))


    @pyqtSignature("")
    def on_action_build_chi_map_triggered(self):
        h5chess=CHESSRUNFILE()
        itemnames=[]
        for group in h5chess.iterobjects():
            if isinstance(group, h5py.Group):
                itemnames+=[group.name.rpartition('/')[2]]
        h5chess.close()
        idialog=selectorDialog(self, itemnames, title='select a CHESSrun group')
        if idialog.exec_():
            idialog2=chiparamDialog(self, str(unicode(idialog.groupsComboBox.currentText())))
            if idialog2.exec_():
                chimin=idialog2.chiminSpinBox.value()
                chimax=idialog2.chimaxSpinBox.value()
                chiint=idialog2.chiintSpinBox.value()
                chigridstr='['+','.join(tuple([labelnumberformat(num) for num in qgrid_minmaxint(chimin, chimax, chiint)]))+']'
                self.addtask(''.join(("buildchimap('",str(unicode(idialog.groupsComboBox.currentText())),"',", chigridstr, ",bin=3)")))

    @pyqtSignature("")
    def on_action_plot_imap_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for integration map')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plotimapwindow(self, self.h5path, self.h5groupstr, self.runpath)
            idialog.exec_()


    @pyqtSignature("")
    def on_action_plot_1D_texture_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for texture plotting ')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plotimapwindow(self, self.h5path, self.h5groupstr, self.runpath, texture=True)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_plot1dwavetrans_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for plotting 1d wave transform')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            typelist=[]
            if 'wavetrans1d' in h5mar:
                type='h5mar:icounts'
                typelist+=['h5mar:icounts']
            if 'texture' in h5mar:
                h5tex=h5mar['texture']
                for grp in h5tex.iterobjects():
                    if isinstance(grp, h5py.Group) and 'icounts' in grp:
                        typelist+=['h5tex:'+grp.name.rpartition('/')[2]]
                idialog=selectorDialog(self, typelist, title='select type of 1d dataset')
                if idialog.exec_():
                    type=str(idialog.groupsComboBox.currentText())
                else:
                    return
            idialog=plotwavetrans1dwindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex(), type=type)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_plotinterpimageof1ddata_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for plotting interpolation maps')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            typelist=[]
            if 'icounts' in h5mar:
                type='h5mar'
                typelist+=['h5mar']
            if 'texture' in h5mar:
                h5tex=h5mar['texture']
                for grp in h5tex.iterobjects():
                    if isinstance(grp, h5py.Group) and 'icounts' in grp:
                        typelist+=['h5tex:'+grp.name.rpartition('/')[2]]
                idialog=selectorDialog(self, typelist, title='select type of 1d dataset')
                if idialog.exec_():
                    type=str(idialog.groupsComboBox.currentText())
                else:
                    return
            idialog=plotinterpimageof1ddatawindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex(), type=type)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_integrate_single_image_triggered(self):
        self.integratecontrol(single=True)

    @pyqtSignature("")
    def on_action_integrate_entire_dataset_triggered(self):
        self.integratecontrol(single=False)

    @pyqtSignature("")
    def on_action_plot_dat_triggered(self):
        idialog=plotdatwindow(self, self.runpath)
        idialog.exec_()

    @pyqtSignature("")
    def on_action_calcqq_triggered(self):
        self.qqcalccontrol()

    @pyqtSignature("")
    def on_action_analyze_qq_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for analyzing qq')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=qqanalysisDialog(self)
            if idialog.exec_():
                curve='%d' %idialog.curve_spinBox.value()
                counts='%d' %idialog.cts_spinBox.value()
                clust='%.2f' %idialog.clust_spinBox.value()
                self.addtask(''.join(("qqanalyze(h5path='", self.h5path, "',  h5groupstr='", self.h5groupstr,"', pkmincurve=",curve, ", pkminsqcts=", counts, ", qclusterradius=", clust, ")")))

    @pyqtSignature("")
    def on_action_1d_peak_search_single_triggered(self):
        self.peak1dcontrol(single=True)

    @pyqtSignature("")
    def on_action_1d_peak_search_all_triggered(self):
        self.peak1dcontrol(single=False)

    @pyqtSignature("")
    def on_action_1d_peak_search_tex_triggered(self):
        self.peak1dcontrol(single=False, type='h5tex')

    @pyqtSignature("")
    def on_action_fit_1d_peaks_triggered(self):
        self.peakfitcontrol()

    @pyqtSignature("")
    def on_action_fit_1d_peaks_tex_triggered(self):
        self.peakfitcontrol(type='h5tex')

    @pyqtSignature("")
    def on_action_associate_1d_qqpeaks_single_triggered(self):
        self.pkassociatecontrol(single=True)

    @pyqtSignature("")
    def on_action_associate_1d_qqpeaks_all_triggered(self):
        self.pkassociatecontrol(single=False)

    @pyqtSignature("")
    def on_action_group_into_phases_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for phase grouping')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=makephasesDialog(self)
            if idialog.exec_():
                critqqnorm='%.2f' %idialog.critqqnormSpinBox.value()
                critnumqqpks='%d' %idialog.numqqpksSpinBox.value()
                critnumipks='%d' %idialog.numipksSpinBox.value()
                self.addtask(''.join(("makephases(h5path='", self.h5path, "',  h5groupstr='", self.h5groupstr,"', critqqnorm=",critqqnorm, ", critnumqqpks=", critnumqqpks, ", critnumipks=", critnumipks, ")")))

    @pyqtSignature("")
    def on_action_spatial_phases_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for spatial analysis of phases')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=spatialphasesDialog(self)
            if idialog.exec_():
                critblobsep='%.2f' %idialog.critblobsepSpinBox.value()
                critnumqqpks='%d' %idialog.numqqpksSpinBox.value()
                critnumpts='%d' %idialog.numptsSpinBox.value()
                self.addtask(''.join(("spatialanalysisofphases(h5path='", self.h5path, "',  h5groupstr='", self.h5groupstr,"', critnumqqpks=",critnumqqpks, ", critblobsep=", critblobsep, ', minptsinblob=', critnumpts,")")))




    @pyqtSignature("")
    def on_action_plot_2D_intensity_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for 2d intensity plotting')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plot2dintwindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex())
            idialog.exec_()

    @pyqtSignature("")
    def on_action_plot_1D_intensity_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for 1d intensity plotting')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')            
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            typelist=[]
            if 'icounts' in h5mar:
                type='h5mar'
                typelist+=['h5mar']
            if 'texture' in h5mar:
                h5tex=h5mar['texture']
                for grp in h5tex.iterobjects():
                    if isinstance(grp, h5py.Group) and 'icounts' in grp:
                        typelist+=['h5tex:'+grp.name.rpartition('/')[2]]
                idialog=selectorDialog(self, typelist, title='select type of 1d dataset')
                if idialog.exec_():
                    type=str(idialog.groupsComboBox.currentText())
                else:
                    return
            idialog=plot1dintwindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex(), type=type)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_fix1dbcknd_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for 1d intensity plotting')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plot1dintwindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex(), bckndedit=True)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_addpeaks_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for 1d intensity plotting')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plot1dintwindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex(), addpeaks=True)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_removepeaks_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for 1d intensity plotting')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plot1dintwindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex(), removepeaks=True)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_association_trees_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for association tree')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=associationtreedialog(self, self.h5path, self.h5groupstr)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_plot_qq_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for qq plotting')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plotqqwindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex())
            idialog.exec_()

    @pyqtSignature("")
    def on_action_association_trees_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for qq plotting')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plotqqwindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex(), displaytrees=True)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_save_all_1d_plt_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for 1d->.plt')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r+')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            qgrid=h5mar['icounts'].attrs['qgrid']
            qvals=q_qgrid_ind(qgrid)
            pointlist=h5analysis.attrs['pointlist']
            xtypelist=['q 1/nm','2th (deg)','d (nm)','pixels']
            idialog=plotsoDialog(self, xtypelist, qvals[0], qvals[-1], title='select a scattering variable')
            if idialog.exec_():
                scale=idialog.densityCheckBox.isChecked()
                xtype=unicode(idialog.typeComboBox.currentText())
                low=idialog.lowSpinBox.value()
                high=idialog.highSpinBox.value()
                lowind=numpy.where(qvals>=low)[0][0]
                highind=qvals.shape[0]-numpy.where(qvals[-1:0:-1]<=high)[0][0]
                qvals=qvals[lowind:highind]
                attrdict=getattr(self.h5path, self.h5groupstr)
                L=attrdict['cal'][2]
                wl=attrdict['wavelength']
                psize=attrdict['psize']
                if scale:
                    infodict, success=getpointinfo(self.h5path, self.h5groupstr, types=['DPnmolcm2'])
                    if not success:
                        print 'ABORTING: not all info could be found'
                        return
                    scalearr=1/infodict['DPnmolcm2']

                else:
                    scalearr=numpy.ones(max(pointlist)+1, dtype='float32')
                if 'pix' in xtype:
                    xvals=pix_q(qvals, L, wl, psize=psize)
                    t1='pix'
                elif '(nm)' in xtype:
                    xvals=d_q(qvals)
#                    plotarr=numpy.array([plotarr[-1*i-1] for i in range(plotarr.size)])
#                    xvals=numpy.array([xvals[-1*i-1] for i in range(xvals.size)])
                    t1='d'
                elif '2' in xtype:
                    xvals=twotheta_q(qvals, wl)
                    t1='2th'
                else:
                    t1='q'
                    xvals=qvals
                if scale:
                    scalestr='scaledIvs'
                else:
                    scalestr='Ivs'
                savename1='_'.join((os.path.split(self.h5path)[1][0:-3], self.h5groupstr, scalestr, t1, ''))

                pointers=[h5mar['icounts']]
                if 'ifcounts' in h5mar:
                    pointers+=[h5mar['ifcounts']]
                for pnt in pointers:
                    for pointind in pointlist:
                        yvals=pnt[pointind, lowind:highind]*scalearr[pointind]#index out of bounds
                        writeplotso(self.runpath, xvals, yvals, attrdict, t1, ''.join((savename1, pnt.name.rpartition('/')[2], `pointind`)))
            h5file.close()

    @pyqtSignature("")
    def on_action_save_2d_image_dataset_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for 2d data->.png')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            typelist=['raw','bckndsubtracted', 'banom', 'totalbcknd',  'singlebcknd']
            idialog=selectorDialog(self, typelist, title='select a 2d image type')
            if idialog.exec_():
                typestr=str(unicode(idialog.groupsComboBox.currentText()))
                type=typelist.index(typestr)

                savetypelist=['png from binned data', 'png with x2 furhter binning',  'png with x10 furhter binning', 'dat from binned data', 'dat with x2 furhter binning',  'dat with x10 furhter binning' ]
                idialog=selectorDialog(self, savetypelist, title='select a save type')
                if idialog.exec_():
                    saveind=savetypelist.index(str(unicode(idialog.groupsComboBox.currentText())))
                    extrabin=[1, 2, 10][saveind%3]
                    datsave=bool(saveind//3)
                    if not datsave:
                        idialog=highlowDialog(self, "Enter range for colorbar - cancel for auto")
                        if idialog.exec_():
                            colorrange=(idialog.lowSpinBox.value(), idialog.highSpinBox.value())
                        else:
                            colorrange=None
                    writeall2dimages(self.runpath, self.h5path,  self.h5groupstr, type, typestr, colorrange=colorrange, datsave=datsave,  extrabin=extrabin)

    @pyqtSignature("")
    def on_action_export_cfg_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for 2d data->.png')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]

            if 'depprof' in h5analysis:
                h5depprof=h5analysis['depprof']
                gunpropdict=ReadGunPropDict(h5analysis)
            if not 'xrf/cfg' in h5analysis:
                QMessageBox.warning(self,"failed",  'ABORTED: XRF data not found')
                return
            h5xrf=h5analysis['xrf']
            cfg=readh5pyarray(h5xrf['cfg'])
            inds=list(numpy.where(cfg!='')[0])
            inds=[`i` for i in inds]
            idialog=selectorDialog(self, inds, title='select a pointind')
            if idialog.exec_():
                indstr=str(unicode(idialog.groupsComboBox.currentText()))
                ind=inds.index(indstr)
                cfgpath=os.path.join(self.runpath, ''.join((os.path.split(self.h5path)[1][0:-3], '_', self.h5groupstr.rpartition('.')[2], '_', indstr, '.cfg'))).replace('\\','/').encode()
                f=open(cfgpath,mode='w')
                f.write(cfg[ind])
                f.close()

    @pyqtSignature("")
    def on_action_edit_raw_diff_data_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
            h5path=self.h5path
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for editing raw XRD')
            if temp!='':
                h5path=temp
                perform=True
        
        if perform:
            h5file=h5py.File(h5path, mode='r')
            grpnames=[]
            for group in h5file.iterobjects():
                if isinstance(group,h5py.Group)  and 'measurement' in group:
                    group=group['measurement']
                    for xrdgrp in XRDgroupnames():
                        if xrdgrp in group and isinstance(group[xrdgrp],h5py.Group) and 'counts' in group[xrdgrp]:
                            grpnames+=[group[xrdgrp].name]
            h5file.close()
            perform=len(grpnames)>0
            if not perform:
                print 'no XRD data found in .h5 file'

        if perform:
            idialog=selectorDialog(self, grpnames, title='Select an experiment group')
            perform=idialog.exec_()
            
        if perform:
            h5grppath=str(idialog.groupsComboBox.currentText())
            idialog=editrawxrdwindow(self, h5path, h5grppath=h5grppath) #these are not self.h5path because this fcn can run on any group with xrd data (no itinilization necessary)
            if idialog.exec_():
                QMessageBox.warning(self,"Only Raw data modified",  'The "edit raw data" has successfully completed but\nany existing binned images, background calculations, etc.\ndo not yet reflect this edit. The cleanest way to edit raw data\nis to run "initialize.." and restart XRD analysis.')

    @pyqtSignature("")
    def on_action_image_histogram_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for histogram plotting')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=plothistwindow(self, self.h5path, self.h5groupstr, self.runpath, self.navchoiceComboBox.currentIndex())
            idialog.exec_()

    @pyqtSignature("")
    def on_action_H5file_info_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for file info retrieval')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            idialog=h5fileinfoDialog(self, self.h5path, self.h5groupstr)
            idialog.exec_()

    @pyqtSignature("")
    def on_action_calcqchiimages_triggered(self):
        h5chess=CHESSRUNFILE()
        itemnames=[]
        for group in h5chess.iterobjects():
            if isinstance(group, h5py.Group):
                itemnames+=[group.name.rpartition('/')[2]]
        h5chess.close()
        idialog=selectorDialog(self, itemnames, title='select a CHESSrun group')

        if idialog.exec_():
            self.addtask(''.join(("calcqchiimages('", unicode(idialog.groupsComboBox.currentText()), "', alsocalcbin=3)")))

    @pyqtSignature("")
    def on_action_createchessrun_triggered(self):
        idialog = chessrunattrDialog(self)
        if idialog.exec_():
            attrdict={
            'wavelength':idialog.wavelengthSpinBox.value(),
            'cal':[idialog.xcenSpinBox.value(), idialog.ycenSpinBox.value(), idialog.LSpinBox.value(), idialog.martiltSpinBox.value(), idialog.tiltrotSpinBox.value()],
            'alpha':idialog.alphaSpinBox.value(),
            'detectorshape':(idialog.shape0SpinBox.value(),idialog.shape1SpinBox.value()), #also fit2D style horixzontal,vertical which is transpose of indeces
            'tiltdirection':str(idialog.tiltdirectionComboBox.currentText()), 
            'xrdname':str(idialog.xrdnameLineEdit.text()), 
            'psize':idialog.psizeSpinBox.value(), 
            }
            h5chess=CHESSRUNFILE('r+')
            grpname=str(unicode(idialog.nameLineEdit.text()))
            if grpname in h5chess:
                del h5chess[grpname]
            group=h5chess.create_group(grpname)
            for key, val in attrdict.iteritems():
                group.attrs[key]=val
            group.create_group('imap')
            group.create_group('chimap')
            group.create_group('killmap')
            h5chess.close()


    @pyqtSignature("")
    def on_action_calc_waveset1d_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for file info retrieval')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]

            itemlist=['qgrid for powder patterns','chigrid for texture analysis']
            idialog=selectorDialog(self, itemlist, title='select an application,  i.e. a type of data for extracting design parameters')
            if idialog.exec_():
                selection=itemlist.index(str(idialog.groupsComboBox.currentText()))
                if selection==0:
                    grid=getimapqgrid(h5analysis.attrs['imapstr'], imap=False)
                else:
                    grid=getchimapchigrid(h5analysis.attrs['chimapstr'], chimap=False)
            else:
                grid=None
            h5file.close()
        else:
            grid=None

        idialog=waveset1dparamDialog(self, grid)
        if idialog.exec_():
            qsmin=idialog.qsminSpinBox.value()
            qsmax=idialog.qsmaxSpinBox.value()
            qsint=idialog.qsintSpinBox.value()
            qsgridstr='['+','.join(tuple([labelnumberformat(num) for num in scalegrid_minmaxint(qsmin, qsmax, qsint)]))+']'

            qpmin=idialog.qpminSpinBox.value()
            qpmax=idialog.qpmaxSpinBox.value()
            qpint=idialog.qpintSpinBox.value()
            qpgridstr='['+','.join(tuple([labelnumberformat(num) for num in qgrid_minmaxint(qpmin, qpmax, qpint)]))+']'

            qmin=idialog.qminSpinBox.value()
            qmax=idialog.qmaxSpinBox.value()
            qint=idialog.qintSpinBox.value()
            qgridstr='['+','.join(tuple([labelnumberformat(num) for num in qgrid_minmaxint(qmin, qmax, qint)]))+']'

            self.addtask(''.join(("buildwaveset1d(qscalegrid=", qsgridstr, ", qposngrid=", qpgridstr, ", qgrid=", qgridstr, ",maxfixenfrac=",`idialog.fixenSpinBox.value()`,")")))


    @pyqtSignature("")
    def on_action_wavetrans1d_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for wavelet transform calculation')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            if 'icounts' in h5mar:
                qgrid=h5mar['icounts'].attrs['qgrid']
                h5file.close()

                h5wave=WAVESET1dFILE()
                selectlist=[]
                namedict={}
                for grp in h5wave.iterobjects():
                    if isinstance(grp, h5py.Group):
                        selstr, garb, qgridstr=(grp.name.rpartition('/')[2]).replace('_', 'qposngrid:', 1).partition('_')
                        waveqgrid=grp.attrs['qgrid']
                        if set(q_qgrid_ind(waveqgrid)).issubset(set(q_qgrid_ind(qgrid))):
                            selstr='qscalegrid:'+selstr
                            namedict[selstr]=grp.name.rpartition('/')[2]
                            selectlist+=[selstr]
                idialog=selectorDialog(self, selectlist, title='select wavelet set to use')
                if idialog.exec_():
                    namestr=str(unicode(idialog.groupsComboBox.currentText()))
                    self.addtask(''.join(("wavetrans1d('", self.h5path, "','", self.h5groupstr, "','", namedict[namestr],"')")))
            else:
                h5file.close()
                print 'cannot calculate wave trans without icounts'


    @pyqtSignature("")
    def on_action_wavetranstex_triggered(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for wavelet transform calculation')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            if 'texture' in h5mar:
                texgrplist=[]
                h5tex=h5mar['texture']
                for grp in h5tex.iterobjects():
                    if isinstance(grp, h5py.Group) and 'icounts' in grp:
                        texgrplist+=[grp.name.rpartition('/')[2]]
                idialog=selectorDialog(self, texgrplist, title='select texture dataset')
            else:
                h5file.close()
                print 'cannot calculate wave trans without texture data'
                return
            if len(texgrplist)>0 and idialog.exec_():
                h5texgrpname=str(idialog.groupsComboBox.currentText())
                h5texgrp=h5tex[h5texgrpname]
                qgrid=h5texgrp.attrs['chigrid']
                h5file.close()
                h5wave=WAVESET1dFILE()
                selectlist=[]
                namedict={}
                for grp in h5wave.iterobjects():
                    if isinstance(grp, h5py.Group):
                        selstr, garb, qgridstr=(grp.name.rpartition('/')[2]).replace('_', 'qposngrid:', 1).partition('_')
                        waveqgrid=grp.attrs['qgrid']
                        if set(q_qgrid_ind(waveqgrid)).issubset(set(q_qgrid_ind(qgrid))):
                            selstr='qscalegrid:'+selstr
                            namedict[selstr]=grp.name.rpartition('/')[2]
                            selectlist+=[selstr]
                idialog=selectorDialog(self, selectlist, title='select wavelet set to use')
                if idialog.exec_():
                    namestr=str(unicode(idialog.groupsComboBox.currentText()))
                    self.addtask(''.join(("wavetrans1d('", self.h5path, "','", self.h5groupstr, "','", namedict[namestr],"', type='h5tex:", h5texgrpname, "')")))

    @pyqtSignature("")
    def on_actionExit_triggered(self):
        raise SystemExit

    def importdatadialogcontrol(self, h5path=None, h5groupstr=None, command=None, markstr=''):
        """data is automatically binned at 3. uses gui for getting parametrs, but chessrun parameters taken from chessrun h5 group attrs"""
        if h5path is None or h5groupstr is None:
            self.clearactivepath()
            self.h5path=mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for scan initialization')
            command=None
            idialog2=importh5scanDialog(self, self.h5path)
            if not idialog2.exec_():
                return
            temp=unicode(idialog2.scanComboBox.currentText())
            self.h5groupstr, temp, command=temp.partition(':')
            self.h5groupstr=str(self.h5groupstr)
        else:
            self.h5path=h5path
            self.h5groupstr=h5groupstr
        self.updateactivepath()
        
        
        h5file=h5py.File(self.h5path, mode='r+')
        if not 'analysis' in h5file[self.h5groupstr]:
            h5file[self.h5groupstr].create_group('analysis')
        h5file.close()

        attrdicttemp = self.importattrDialogcaller(self, self.h5path, self.h5groupstr, command=command)
        if attrdicttemp is None:
            return
        
        writeattr(self.h5path, self.h5groupstr, attrdicttemp)
        h5file=h5py.File(self.h5path, mode='r+')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        xrdname=getxrdname(h5analysis)
        if not xrdname in h5analysis:
            h5analysis.create_group(xrdname)
        h5file.close()
        
        idialog=editrawxrdwindow(self, self.h5path, h5groupstr=self.h5groupstr)
        idialog.exec_()
        self.addtask(''.join(("initializescan('", self.h5path, "','", self.h5groupstr, "',bin=3)")))


    def integratecontrol(self, single=True):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for integration')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            pointlist=h5analysis.attrs['pointlist']
            namelist=[]
            namelist+=['%d' %p for p in pointlist]
            namelist+=['raw%d' %p for p in pointlist]
            namelist+=['banom%d' %p for p in pointlist]
            for dset in h5mar.iterobjects():
                if isinstance(dset, h5py.Dataset) and len(dset.shape)==2 and not ('bin' in dset.name.rpartition('/')[2]) and (dset.name.rpartition('/')[2]).startswith('b'):
                    namelist+=[dset.name.rpartition('/')[2]]


            h5file.close()
            perform=False
            bckndbool=True
            if len(namelist)>0:
                singlecommand=''
                if single:
                    idialog=selectorDialog(self, namelist, title='select an image to integrate')
                    if idialog.exec_():
                        imname=str(unicode(idialog.groupsComboBox.currentText()))
                        singlecommand=''.join((", singleimage='", imname,"'"))
                        perform=True
                        if imname.startswith('b') or ('raw' in imname):
                            bckndbool=False
                else:
                    perform=True
                if perform:
                    self.addtask(''.join(("integrate(h5path='", self.h5path, "', h5groupstr='", self.h5groupstr,"'", singlecommand, ", bckndbool=", `bckndbool`, ")")))
            else:
                QMessageBox.warning(self,"failed",  "no images found")

    def qqcalccontrol(self):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for calculating qq')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r+')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            if not ('icounts' in h5mar):
                h5file.close()
                print 'cannot perform qqcalc due to absence of icounts'
                return
            defqgrid=h5mar['icounts'].attrs['qgrid']


            opts=[]
            if 'ifcounts' in h5mar:
                opts+=['ifcounts (processed)']
            opts+=['icounts']

            h5file.close()
            idialog=qqparamDialog(self, defqgrid, opts, 'select a type of 1d intensity array')
            if idialog.exec_():
                imagecommand=unicode(idialog.typeComboBox.currentText()).partition(' ')[0]
                imagecommand=''.join((", image='", imagecommand,"'"))
                qmin=idialog.qminSpinBox.value()
                qmax=idialog.qmaxSpinBox.value()
                qint=idialog.qintSpinBox.value()
                qgridstr='[%.2f, %.2f, %.2f]' %tuple(qgrid_minmaxint(qmin, qmax, qint))
                self.addtask(''.join(("qqcalc(h5path='", self.h5path, "', h5groupstr='", self.h5groupstr,"', qgrid=", qgridstr,  imagecommand, ")")))

    def peakfitcontrol(self, type='h5mar'):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for finding peaks in 1d intensity')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            namelist=[]
            if ('h5mar' in type) and ('ifcounts' in h5mar) and ('wavetrans1d' in h5mar) and ('peaks' in h5mar['wavetrans1d']):
                if ('additionalpeaks' in h5mar) and h5mar['additionalpeaks'].attrs['usedinfitting']==0:
                    peakfitstr=', use_added_peaks=True'
                else:
                    peakfitstr=''
                namelist=['ifcounts']
            elif ('h5tex' in type) and 'texture' in h5mar:
                h5tex=h5mar['texture']
                namelist=[]
                for grp in h5tex.iterobjects():
                    if isinstance(grp, h5py.Group) and 'wavetrans1d' in grp and ('peaks' in grp['wavetrans1d']):
                        namelist+=[grp.name.rpartition('/')[2]]
            if len(namelist)==0:
                h5file.close()
                print 'cannot calculate wave trans without texture data'
                return
            else:
                idialog=selectorDialog(self, namelist, title='select texture dataset')
            if idialog.exec_():
                grpstr=str(idialog.groupsComboBox.currentText())
                if ('h5tex' in type):
                    if ('additionalpeaks' in h5tex[grpstr]) and h5tex[grpstr]['additionalpeaks'].attrs['usedinfitting']==0:
                        peakfitstr=', use_added_peaks=True'
                    else:
                        peakfitstr=''
                h5file.close()
                typecommand=''.join((", type='", type, ':', grpstr,"'"))
                self.addtask(''.join(("peakfit1d(h5path='", self.h5path, "', h5groupstr='", self.h5groupstr, "'",  typecommand,", windowextend_hwhm=3, peakshape='Gaussian', critresidual=.2",peakfitstr,")")))
            else:
                h5file.close()


    def peak1dcontrol(self, single=True, type='h5mar'):
        perform=False
        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
            perform=True
        else:
            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for finding peaks in 1d intensity')
            if temp!='':
                if self.default_scan_checkBox.isChecked():
                    tempgrp=getdefaultscan(temp)
                    if tempgrp is None:
                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
                        perform=False
                    else:
                        self.h5path=temp
                        self.h5groupstr=tempgrp
                        self.updateactivepath()
                        perform=True
                else:
                    idialog=getgroupDialog(self, temp)
                    if idialog.exec_():
                        self.h5path=temp
                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
                        self.updateactivepath()
                        perform=True
        if perform:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            namelist=[]
            if ('h5mar' in type) and ('wavetrans1d' in h5mar) and ('wavetrans' in h5mar['wavetrans1d']):
                h5file.close()
                namelist=['icounts']
            elif ('h5tex' in type) and 'texture' in h5mar:
                h5tex=h5mar['texture']
                namelist=[]
                for grp in h5tex.iterobjects():
                    if isinstance(grp, h5py.Group) and 'wavetrans1d' in grp:
                        namelist+=[grp.name.rpartition('/')[2]]
            if len(namelist)==0:
                h5file.close()
                print 'cannot perform peak search because cannot find wavelet transformation'

            idialog=wavepeak1dDialog(self, namelist, 'select a type of 1d intensity array for peak search')
            if idialog.exec_():
                typecommand=''.join((", type='", type, ':', str(idialog.typeComboBox.currentText()),"'"))
                minridgelength='%d' %idialog.minridgelength_spinBox.value()
                minchildlength='%d' %idialog.minchildlength_spinBox.value()
                minridgewtsum='%.2f' %idialog.minridgewtsum_spinBox.value()
                minchildwtsum='%.2f' %idialog.minchildwtsum_spinBox.value()
                wavenoisecutoff='%.2f' %idialog.wavenoisecutoff_spinBox.value()
                maxqs='%.2f' %idialog.maxqs_spinBox.value()
                self.addtask(''.join(("wavepeaksearch1d(h5path='", self.h5path, "',  h5groupstr='", self.h5groupstr, "'",  typecommand,", minridgelength=", minridgelength, ", minchildlength=", minchildlength, ", minridgewtsum=", minridgewtsum, ", minchildwtsum=", minchildwtsum,", maxqscale_localmax=", maxqs, ", wavenoisecutoff=", wavenoisecutoff, ")")))


#this was written to allow peak searching in single spectra and in ifcounts but not currently supported
#    def peak1dcontrol(self, single=True):
#        perform=False
#        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
#            perform=True
#        else:
#            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for finding peaks in 1d intensity')
#            if temp!='':
#                if self.default_scan_checkBox.isChecked():
#                    tempgrp=getdefaultscan(temp)
#                    if tempgrp is None:
#                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
#                        perform=False
#                    else:
#                        self.h5path=temp
#                        self.h5groupstr=tempgrp
#                        self.updateactivepath()
#                        perform=True
#                else:
#                    idialog=getgroupDialog(self, temp)
#                    if idialog.exec_():
#                        self.h5path=temp
#                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
#                        self.updateactivepath()
#                        perform=True
#        if perform:
#            h5file=h5py.File(self.h5path, mode='r')
#           h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
#            h5mar=h5file['/'.join((self.h5groupstr, 'analysis/mar345'))]
#
#            pointlist=h5analysis.attrs['pointlist']
#
#            namelist=[]
#            if 'icounts' in h5mar:
#                if single:
#                    namelist+=['i%d' %p for p in pointlist]
#                else:
#                    namelist+=['icounts']
#            if 'ifcounts' in h5mar:
#                if single:
#                    namelist+=['if%d' %p for p in pointlist]
#                else:
#                    namelist+=['ifcounts']
#
#            if single:
#                for node in h5mar.iterobjects():
#                    if node.name.startswith('i') and isinstance(node, h5py.Dataset) and len(node.shape)==1:
#                        namelist+=[node.name]
#
#            h5file.close()
#            perform=False
#            if len(namelist)>0:
#                idialog=wavepeak1dDialog(self, namelist, 'select a type of 1d intensity array for peak search')
#                if idialog.exec_():
#                    imagecommand=''.join((", image='", unicode(idialog.typeComboBox.currentText()).partition(' '),"'"))
#                    perform=True
#                if perform:
#                    minridgelength='%d' %idialog.minridgelength_spinBox.value()
#                    wavenoisecutoff='%.2f' %idialog.wavenoisecutoff_spinBox.value()
#                    self.addtask(''.join(("wavepeaksearch1d(h5path='", self.h5path, "',  h5groupstr='", self.h5groupstr,"', minridgelength=",minridgelength, ", wavenoisecutoff=", wavenoisecutoff, imagecommand, ")")))
#            else:
#                QMessageBox.warning(self,"failed",  "no intensity arrays found")

#    def pkassociatecontrol(self, single=True):
#        perform=False
#        if self.activepathcheckBox.isChecked() and unicode(self.active_file_lineEdit.text())==self.activepathcompare:
#            perform=True
#        else:
#            temp = mygetopenfile(self, xpath=self.h5path,markstr='.h5 file for associating 1d peaks with qqpeaks')
#            if temp!='':
#                if self.default_scan_checkBox.isChecked():
#                    tempgrp=getdefaultscan(temp)
#                    if tempgrp is None:
#                        QMessageBox.warning(self,"failed",  'No default grp found - run initialize')
#                        perform=False
#                    else:
#                        self.h5path=temp
#                        self.h5groupstr=tempgrp
#                        self.updateactivepath()
#                        perform=True
#                else:
#                    idialog=getgroupDialog(self, temp)
#                    if idialog.exec_():
#                        self.h5path=temp
#                        self.h5groupstr=str(unicode(idialog.groupsComboBox.currentText()))
#                        self.updateactivepath()
#                        perform=True
#        if perform:
#            singlecommand=''
#            perform=False
#            fulldergrpstr=''.join(('h5file',self.h5groupstr, '.Derived'))
#            h5file=tables.openFile(self.h5path, mode='r')
#            dergrp=eval(fulldergrpstr)
#            namelist=[]
#            for node in dergrp:
#                if node.name.startswith('k') and node.name[1:].isdigit():
#                    namelist+=[node.name]
#            h5file.close()
#            if len(namelist)>0:
#                namelist.sort()
#                if single:
#                    idialog=selectorDialog(self, namelist, title='select peak list for qq association')
#                    if idialog.exec_():
#                        imname=str(unicode(idialog.groupsComboBox.currentText()))
#                        singlecommand=''.join((", singleimage='", imname,"'"))
#                        perform=True
#                else:
#                    perform=True
#            else:
#                QMessageBox.warning(self,"failed",  "no intensity arrays found")
#            if perform:
#                idialog=peakqqassociationDialog(self)
#                if idialog.exec_():
#                    qqaaft='(%.2f,%.2f)' %(idialog.qanisofrac_spinBox.value(), idialog.qalloyfrac_spinBox.value())
#                    qqsigcritsep='%.2f' %idialog.qqsig_spinBox.value()
#                    qqnormcritval='%.2f' %idialog.qqnorm_spinBox.value()
#                    self.addtask(''.join(("peak1dassociation(h5path='", self.h5path, "',  h5groupstr='", self.h5groupstr,"', qqanisoalloyfractup=",qqaaft, ", qqsigcritsep=", qqsigcritsep, ", qqnormcritval=", qqnormcritval, singlecommand,")")))

    def addtask(self, cmdstr):
        #self.taskTextBrowser.append(''.join((cmdstr, '\n')))
        self.taskTextBrowser.append(cmdstr)

    def importattrDialogcaller(self, p1, p2, p3, command=None):
        idialog = importattrDialog(p1, p2, p3, command=command)
        if idialog.exec_():
            ellineditlist=[idialog.el1LineEdit, idialog.el2LineEdit, idialog.el3LineEdit, idialog.el4LineEdit]
            ellist=[str(unicode(le.text())) for le in ellineditlist]
            xgrid=(idialog.xstartSpinBox.value(), idialog.xintSpinBox.value(), idialog.xptsSpinBox.value())
            zgrid=(idialog.zstartSpinBox.value(), idialog.zintSpinBox.value(), idialog.zptsSpinBox.value())
            returndict ={
            'wavelength':idialog.wavelengthSpinBox.value(),
            'command':str(unicode(idialog.cmdLineEdit.text())),
            'elements':ellist,
            'xgrid':xgrid,
            'zgrid':zgrid,
            'counter':idialog.inttimeSpinBox.value(),
            'cal':[idialog.xcenSpinBox.value(), idialog.ycenSpinBox.value(), idialog.LSpinBox.value(), idialog.martiltSpinBox.value(), idialog.tiltrotSpinBox.value()],
            'alpha':idialog.alphaSpinBox.value(),
            'bcknd':str(unicode(idialog.bckndComboBox.currentText())),
            'chessrunstr':'/'.join(('', str(unicode(idialog.chessruncomboBox.currentText())))),
            'imapstr':'/'.join(('', str(unicode(idialog.chessruncomboBox.currentText())), 'imap', str(unicode(idialog.imapcomboBox.currentText())))),
            'chimapstr':'/'.join(('', str(unicode(idialog.chessruncomboBox.currentText())), 'chimap', str(unicode(idialog.chimapcomboBox.currentText())))),
            'killmapstr':'/'.join(('', str(unicode(idialog.chessruncomboBox.currentText())), 'killmap', str(unicode(idialog.killmapcomboBox.currentText())))),
            'qimagestr':'/'.join(('', str(unicode(idialog.chessruncomboBox.currentText())), 'qimage')),
            'chiimagestr':'/'.join(('', str(unicode(idialog.chessruncomboBox.currentText())), 'chiimage')),
            'dqchiimagestr':'/'.join(('', str(unicode(idialog.chessruncomboBox.currentText())), 'dqchiimage')),
            'xrdname':str(idialog.xrdnameLineEdit.text()), 
            'psize':idialog.psizeSpinBox.value(), 
            }
            if returndict['command']!='USER-COMPILED':
                if idialog.usespecCheckBox.isChecked():
                    for k, v in idialog.fromspecattr.iteritems():
                        returndict[k]=v
                else:
                    for k, v in specattr_xzgrid(xgrid, zgrid, 'mesh' in returndict['command']).iteritems():
                        returndict[k]=v
            return returndict
        else:
            return None

class bckndinventoryDialog(QDialog,
        ui_bckndinventoryDialog.Ui_bckndinventoryDialog):
    #***
    def __init__(self, parent, h5path, h5groupstr=None, h5grppath=None):
        super(bckndinventoryDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.h5path=h5path
        self.h5file=h5py.File(self.h5path, mode='r')
        
        if not h5groupstr is None:
            self.h5groupstr=h5groupstr
            self.h5analysis=self.h5file['/'.join((self.h5groupstr, 'analysis'))]
            self.h5mar=self.h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            self.h5marcounts=self.h5file['/'.join((self.h5groupstr,'measurement/'+getxrdname(h5analysis)+'/counts'))]
            self.attrdict=getattr(self.h5path, self.h5groupstr)
            chessrungrpname=self.attrdict['chessrunstr']
        else:
            self.h5mar=None
            self.h5marcounts=self.h5file[h5grppath]['counts']
            chessrungrpname=''
            
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
        QObject.connect(self.copyPushButton,SIGNAL("pressed()"),self.performcopy)
        
        
        self.h5chess=CHESSRUNFILE(mode='r+')

        grpnames=[]
        for group in self.h5chess.iterobjects():
            if isinstance(group,h5py.Group):
                grpnames+=[group.name]
        perform=len(grpnames)>0
        if not perform:
            print 'no chess groups found in .h5 file'
        if perform:
            if chessrungrpname in grpnames:
                setindex=grpnames.index(chessrungrpname)
            else:
                setindex=0
            idialog=selectorDialog(self, grpnames, title='Select an h5chess group to store Bcknd images', setindex=setindex)
            perform=idialog.exec_()
        if perform:
            chessrungrpname=str(idialog.groupsComboBox.currentText())
            self.h5chessgrp=self.h5chess[chessrungrpname]
            if 'BckndInventory' in self.h5chessgrp:
                self.h5chessgrp=self.h5chessgrp['BckndInventory']
            else:
                self.h5chessgrp=self.h5chessgrp.create_group('BckndInventory')

            self.imagepointlist=[]
            self.imagenamelist=[]
            
            for counter, c in enumerate(self.h5marcounts):
                if numpy.max(c[:, :])>0:
                    self.imagepointlist+=[(self.h5marcounts, counter)]
                    self.imagenamelist+=['image index %d' %counter]
            for bname in ['bmin', 'bave', 'blin0', 'blin1']:#blin0 and blin1 have to be last so when they are omitted that doesn't change the indexing of imagepointlist
                if (not self.h5mar is None) and bname in self.h5mar:
                    self.imagepointlist+=[self.h5mar[bname]]
                    self.imagenamelist+=[bname]
            for counter, nam in enumerate(self.imagenamelist):
                self.imageComboBox.insertItem(counter, nam)
        else:
            self.ExitRoutine()
    
    def performcopy(self):
        
        nam=str(self.newnameLineEdit.text())
        if nam in self.h5chessgrp and not (self.overwriteCheckBox.isChecked()):
            self.MsgLabel.setText('FAILED: Bcknd Image with that name already exists')
            return
        try:
            pnt=self.imagepointlist[self.imageComboBox.currentIndex()]
            d={}
            if isinstance(pnt, tuple):
                print pnt
                arr=pnt[0][pnt[1]]
                print arr.shape
                print pnt[0].file.filename
                d['sourcefile']=pnt[0].file.filename
                print pnt[0].name
                d['sourcename']=pnt[0].name
                print pnt[1]
                d['sourcearrayindex']=pnt[1]
            else:
                print pnt
                arr=readh5pyarray(pnt)
                d['sourcefile']=arr.file.filename
                d['sourcename']=arr.name
                d['sourcearrayindex']=''
            if nam in self.h5chessgrp:
                del self.h5chessgrp[nam]
            h5ds=self.h5chessgrp.create_dataset(nam, data=arr)
            for key, val in d.iteritems():
                h5ds.attrs[key]=val
            self.MsgLabel.setText('%s successfully added to inventory' %nam)
        except:
            self.MsgLabel.setText('FAILED: fatal error, probably problem with name')
            
    def ExitRoutine(self):
        self.h5file.close()
        self.h5chess.close()
        
class LinBckndDialog(QDialog,
        ui_LinBckndDialog.Ui_LinBckndDialog):

    def __init__(self, parent, h5path, h5groupstr):
        super(LinBckndDialog, self).__init__(parent)
        self.setupUi(self)
        #***
        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.h5file=h5py.File(self.h5path, mode='r+')
        h5analysis=self.h5file['/'.join((self.h5groupstr, 'analysis'))]
        self.h5mar=self.h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        h5marcounts=self.h5file['/'.join((self.h5groupstr,'measurement/'+getxrdname(h5analysis)+'/counts'))]
        attrdict=getattr(self.h5path, self.h5groupstr)
        
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
        QObject.connect(self.buttonBox,SIGNAL("rejected()"),self.CancelledExitRoutine)

        self.imagepointlist=[]
        self.imagenamelist=[]
        self.h5chess=CHESSRUNFILE()
        h5chessrun=self.h5chess[attrdict['chessrunstr']]
        if 'BckndInventory' in h5chessrun:
            bckndgrppoint=h5chessrun['BckndInventory']
            for dset in bckndgrppoint.iterobjects():
                if isinstance(dset,h5py.Dataset):
                    self.imagepointlist+=[dset]
                    self.imagenamelist+=['bcknd inventory: '+dset.name.rpartition('/')[2]]
        for counter, c in enumerate(h5marcounts):
            if numpy.max(c[:, :])>0:
                self.imagepointlist+=[(h5marcounts, counter)]
                self.imagenamelist+=['this data, image index %d' %counter]
        for bname in ['bmin', 'bave', 'blin0', 'blin1']:#blin0 and blin1 have to be last so when they are omitted that doesn't change the indexing of imagepointlist
            if bname in self.h5mar:
                self.imagepointlist+=[self.h5mar[bname]]
                self.imagenamelist+=[bname]
        for counter, nam in enumerate(self.imagenamelist):
            for cb, notallowed in zip([self.imageComboBox0, self.imageComboBox1], ['blin0', 'blin1']):
                if nam!=notallowed:
                    cb.insertItem(counter, nam)
        self.perform=False
    
    def CancelledExitRoutine(self):
        self.h5file.close()
        self.h5chess.close()

    def ExitRoutine(self):
        
        for cb, nam, twle in zip([self.imageComboBox0, self.imageComboBox1], ['blin0', 'blin1'], [self.imagefracLineEdit0, self.imagefracLineEdit1]):
            d={}
            try:
                d['trialimageweights']=numpy.float32(eval('['+str(twle.text())+']'))
            except:
                h5file.close()
                if not self.h5chess is None:
                    self.h5chess.close()
                print
                QMessageBox.warning(self,"syntax error",  "Aborting because the list of trial wieghts did not convert to array correctly.\nThe enetered string has been printed.\nSome blin data in .h5 may have been deleted.")
                self.perform=False
                return
            pnt=self.imagepointlist[cb.currentIndex()]
            
            if isinstance(pnt, tuple):
                print 'reading ', pnt[0].name
                arr=pnt[0][pnt[1]]
                d['sourcefile']=pnt[0].file .filename
                d['sourcename']=pnt[0].name
                d['sourcearrayindex']=pnt[1]
            else:
                print 'reading ', pnt.name
                arr=readh5pyarray(pnt)
                d['sourcefile']=pnt.file.filename
                d['sourcename']=pnt.name
                d['sourcearrayindex']=''
            dellist=[]
            if nam in self.h5mar:
                for pnt in self.h5mar.itervalues():
                    if isinstance(pnt,h5py.Dataset):
                        print pnt.name
                        print pnt.name.rpartition('/')[2]
                        temp=pnt.name.rpartition('/')[2]
                        if nam in temp:#this gets rid of all the blin0bin$
                            dellist+=[temp]
            print dellist
            for temp in dellist:
                del self.h5mar[temp]
                
            h5ds=self.h5mar.create_dataset(nam, data=arr)
            for key, val in d.iteritems():
                h5ds.attrs[key]=val
            
        self.h5file.close()
        self.h5chess.close()
        self.perform=True


class highlowDialog(QDialog,
        ui_highlowDialog.Ui_highlowDialog):

    def __init__(self, parent, title):
        super(highlowDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)

class bminDialog(QDialog,
        ui_bmin_menu.Ui_bmin_menu):

    def __init__(self, parent):
        super(bminDialog, self).__init__(parent)
        self.setupUi(self)


class importh5scanDialog(QDialog,
        ui_h5scanDialog.Ui_h5scanDialog):
    def __init__(self, parent, h5path):
        super(importh5scanDialog, self).__init__(parent)
        self.setupUi(self)
        h5file=h5py.File(h5path, mode='r')
        for grp in h5file.iterobjects():
            print grp.name.rpartition('/')[2]
            if isinstance(grp,h5py.Group):
                #the below conditions means that the data must have this h5 format to analyze the data. if these conditions need to be loosened, the importattrDialog routines should allow user entry of the spec info
                if ('samx' in grp['measurement/scalar_data'] and len(grp['measurement/scalar_data/samx'].shape)==1) or ('samz' in grp['measurement/scalar_data/'] and len(grp['measurement/scalar_data/samz'].shape)==1):
                    if 'acquisition_command' in grp.attrs:
                        self.scanComboBox.insertItem(99,':'.join((grp.name.rpartition('/')[2], grp.attrs['acquisition_command'])))

#    def numcvt(self, num):
#        if numpy.abs(num-round(num))<0.005:
#            return '%d' %int(round(num))
#        if numpy.abs(num*10-round(num*10))<0.05:
#            return '%.1f' %num
#        return '%.2f' %num
#
#    def makecommand(self, grp):
#        samx=None
#        samz=None
#        if 'samx' in grp['scalar_data']:
#            samx=grp['scalar_data/samx'][:]
#        if 'samz' in grp['scalar_data']:
#            samz=grp['scalar_data/samz'][:]
#        if samx is None:
#            samx=numpy.ones(samz.size, dtype='float32')*grp['positioners/samx'].value
#        if samz is None:
#            samz=numpy.ones(samx.size, dtype='float32')*grp['positioners/samz'].value
#
#        startstr=''
#        endstr=''
#
#        if numpy.all(samx==samx[0]):
#            endstr=''.join(('  samx=', self.numcvt(samx[0])))
#            startstr='ascan samz %s %s %d' %(self.numcvt(samz[0]), self.numcvt(samz[-1]), len(samz)-1)
#        elif numpy.all(samz==samz[0]):
#            endstr=''.join(('  samz=', self.numcvt(samz[0])))
#            startstr='ascan samx %s %s %d' %(self.numcvt(samx[0]), self.numcvt(samx[-1]), len(samx)-1)
#        elif len(samz)==len(set(samz)):
#            startstr='a2scan samx %s %s samz %s %s %d' %(self.numcvt(samx[0]), self.numcvt(samx[-1]), self.numcvt(samz[0]), self.numcvt(samz[-1]), len(samz)-1)
#        else:
#            startstr='mesh samx %s %s %d samz %s %s %d' %(self.numcvt(samx[0]), self.numcvt(samx[-1]), len(set(samx))-1, self.numcvt(samz[0]), self.numcvt(samz[-1]), len(set(samz))-1)
#
#        icstr=''
#        for item in grp['scalar_data'].iterobjects():
#            if ('IC' in item.name.rpartition('/')[2]) and isinstance(item,h5py.Dataset):
#                ic=item[:]
#                if numpy.all(ic[(ic.max()-ic)<0.5*ic.max()]==ic.max()):#all elements bigger than half the max are equal to the max. this will exclude the near zero values corresponding to skipped points
#                    icstr=' -%d' %ic.max()
#        if icstr=='':
#            icstr=' %s' %self.numcvt(grp['scalar_data/Seconds'][0])
#
#        return ''.join((startstr, icstr, endstr))



class chessrunattrDialog(QDialog,
        ui_chessrunattr.Ui_chessrunattrDialog):
    def __init__(self, parent):
        super(chessrunattrDialog, self).__init__(parent)
        self.setupUi(self)


        self.attrdict=attrdict_def()

        self.setvalues()


    def setvalues(self):
        self.tiltdirectionComboBox.insertItem(0, 'top')
        self.tiltdirectionComboBox.insertItem(1, 'bottom')
        self.tiltdirectionComboBox.insertItem(2, 'left')
        self.tiltdirectionComboBox.insertItem(3, 'right')
        self.tiltdirectionComboBox.setCurrentIndex(3)

        self.xcenSpinBox.setValue(self.attrdict['cal'][0])
        self.ycenSpinBox.setValue(self.attrdict['cal'][1])
        self.LSpinBox.setValue(self.attrdict['cal'][2])
        self.martiltSpinBox.setValue(self.attrdict['cal'][3])
        self.tiltrotSpinBox.setValue(self.attrdict['cal'][4])
        self.alphaSpinBox.setValue(self.attrdict['alpha'])
        self.wavelengthSpinBox.setValue(self.attrdict['wavelength'])
        self.existingTextBrowser.setPlainText('')
        h5chess=CHESSRUNFILE()
        for count, group in enumerate(h5chess.iterobjects()):
            if isinstance(group, h5py.Group):
                self.existingTextBrowser.append(group.name.rpartition('/')[2])
        h5chess.close()


class importattrDialog(QDialog,
        ui_import_attr.Ui_importattrDialog):
    """h5path and h5groupstr already exist, if attrdict doesn't exist use defaults otherwise display the current values and set self.attrdict to entered values"""
    def __init__(self, parent, h5path, h5groupstr, command=None):
        super(importattrDialog, self).__init__(parent)
        self.setupUi(self)
        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.chessruncomboBox.clear()
        self.imapcomboBox.clear()
        self.chimapcomboBox.clear()
        self.killmapcomboBox.clear()


        self.attrdict=getattr(h5path, h5groupstr)
        if 'cal' in self.attrdict.keys():
            self.chessrun=self.attrdict['chessrunstr'][1:]
            imapstr=self.attrdict['imapstr'][::-1].partition('/')[0][::-1]
            chimapstr=self.attrdict['chimapstr'][::-1].partition('/')[0][::-1]
            killmapstr=self.attrdict['killmapstr'][::-1].partition('/')[0][::-1]
        else:
            self.attrdict=attrdict_def()
            self.chessrun=chessrun_def()
            self.getchessrunattrs()
            imapstr=None
            chimapstr=None
            killmapstr=None
        if not (command is None):
            self.attrdict['command']=str(command)

        self.usespecCheckBox.setChecked(True)

        self.fromspecattr={}
        try:
            h5file=h5py.File(self.h5path, mode='r')
            h5root=h5file[self.h5groupstr]

            self.fromspecattr['acquisition_time']=h5root['measurement/scalar_data/Seconds'][:]
            self.fromspecattr['command']=h5root.attrs['acquisition_command']
            temp_acsh=h5root.attrs['acquisition_shape']
            if isinstance(temp_acsh, str):
                temp_acsh=eval(temp_acsh)
            self.fromspecattr['acquisition_shape']=temp_acsh
            npts=numpy.prod(numpy.int16(temp_acsh))

            samx=None
            samz=None
            if 'samx' in h5root['measurement/scalar_data']:
                samx=h5root['measurement/scalar_data/samx'][:]
            if 'samz' in h5root['measurement/scalar_data']:
                samz=h5root['measurement/scalar_data/samz'][:]

            if samx is None:
                samx=numpy.ones(npts, dtype='float32')*h5root['measurement/positioners/samx'].value
            if samz is None:
                samz=numpy.ones(npts, dtype='float32')*h5root['measurement/positioners/samz'].value

            self.fromspecattr['x']=samx
            self.fromspecattr['z']=samz


            h5file.close()

        except:
            self.usespecCheckBox.setChecked(False)
            self.usespecCheckBox.setDisabled(True)

        self.manualgriditems=[self.cmdLineEdit, self.inttimeSpinBox, self.xstartSpinBox, self.xintSpinBox, self.xptsSpinBox, self.zstartSpinBox, self.zintSpinBox, self.zptsSpinBox]
        if self.attrdict['command']=='USER-COMPILED':
            self.usespecCheckBox.setChecked(False)
            self.usespecCheckBox.setDisabled(True)
            for it in self.manualgriditems:
                it.setDisabled(True)

        self.setmapchoices(imapstr, chimapstr, killmapstr)
        self.setvalues()
        self.usespecprocess()


    @pyqtSignature("")
    def on_usespecCheckBox_clicked(self):
        self.usespecprocess()
    def usespecprocess(self):
        usespec=self.usespecCheckBox.isChecked()

        if usespec:
            self.cmdLineEdit.setText(self.fromspecattr['command'])
            self.calcfromcommand()
        for it in self.manualgriditems:
            it.setDisabled(usespec)

    def setchessrunvalues(self):
        self.xcenSpinBox.setValue(self.attrdict['cal'][0])
        self.ycenSpinBox.setValue(self.attrdict['cal'][1])
        self.LSpinBox.setValue(self.attrdict['cal'][2])
        self.martiltSpinBox.setValue(self.attrdict['cal'][3])
        self.tiltrotSpinBox.setValue(self.attrdict['cal'][4])
        self.alphaSpinBox.setValue(self.attrdict['alpha'])
        self.wavelengthSpinBox.setValue(self.attrdict['wavelength'])
        if 'xrdname' in self.attrdict.keys():
            self.xrdnameLineEdit.setText(self.attrdict['xrdname'])
        if 'psize' in self.attrdict.keys():
            self.psizeSpinBox.setValue(self.attrdict['psize']), 

    def setvalues(self):
        self.setchessrunvalues()
        ellineditlist=[self.el1LineEdit, self.el2LineEdit, self.el3LineEdit, self.el4LineEdit]
        for le, els in zip(ellineditlist, self.attrdict['elements']):
            le.setText(els)
        self.cmdLineEdit.setText(self.attrdict['command'])
        self.xstartSpinBox.setValue(self.attrdict['xgrid'][0])
        self.xintSpinBox.setValue(self.attrdict['xgrid'][1])
        self.xptsSpinBox.setValue(self.attrdict['xgrid'][2])
        self.zstartSpinBox.setValue(self.attrdict['zgrid'][0])
        self.zintSpinBox.setValue(self.attrdict['zgrid'][1])
        self.zptsSpinBox.setValue(self.attrdict['zgrid'][2])
        if self.attrdict['bcknd']=='lin':
            self.bckndComboBox.setCurrentIndex(3)
        elif self.attrdict['bcknd']=='ave':
            self.bckndComboBox.setCurrentIndex(2)
        elif self.attrdict['bcknd']=='min':
            self.bckndComboBox.setCurrentIndex(1)
        else:
            self.bckndComboBox.setCurrentIndex(0)

    def setmapchoices(self, istr, cstr, kstr):
        index=-1
        h5chess=CHESSRUNFILE()
        count=0
        for group in h5chess.iterobjects():
            if isinstance(group, h5py.Group):
                self.chessruncomboBox.insertItem(count, group.name.rpartition('/')[2])
                if group.name.rpartition('/')[2]==self.chessrun:
                    index=count
                count+=1
        if index<0:
            print 'PROBLEM FINDING A CHESSRUN THAT SHOULD EXIST'
            return

        self.chessruncomboBox.setCurrentIndex(index)

        group=h5chess[self.chessrun]

        index=0
        count=0
        subgrp=group['imap']
        for dset in subgrp.iterobjects():
            if isinstance(dset, h5py.Dataset) and not ('bin' in dset.name.rpartition('/')[2]):
                self.imapcomboBox.insertItem(count, dset.name.rpartition('/')[2])
                if dset.name.rpartition('/')[2]==istr:
                    index=count
                count+=1
        self.imapcomboBox.setCurrentIndex(index)
        index=0
        count=0
        subgrp=group['chimap']
        for dset in subgrp.iterobjects():
            if isinstance(dset, h5py.Dataset) and not ('bin' in dset.name.rpartition('/')[2]):
                self.chimapcomboBox.insertItem(count, dset.name.rpartition('/')[2])
                if dset.name.rpartition('/')[2]==cstr:
                    index=count
                count+=1
        self.chimapcomboBox.setCurrentIndex(index)
        index=0
        count=0
        subgrp=group['killmap']
        for dset in subgrp.iterobjects():
            if isinstance(dset, h5py.Dataset) and not ('bin' in dset.name.rpartition('/')[2]):
                self.killmapcomboBox.insertItem(count, dset.name.rpartition('/')[2])
                if dset.name.rpartition('/')[2]==kstr:
                    index=count
                count+=1
        self.killmapcomboBox.setCurrentIndex(index)

        h5chess.close()

    def getchessrunattrs(self):
        h5chess=CHESSRUNFILE()
        node=h5chess[self.chessrun]
        for key, val in node.attrs.iteritems():
            if key in self.attrdict.keys():
                self.attrdict[key]=val
        h5chess.close()

    @pyqtSignature("")
    def on_getchessruninfoButton_clicked(self):
        self.chessrun=str(unicode(self.chessruncomboBox.currentText()))

        self.chessruncomboBox.clear()
        self.imapcomboBox.clear()
        self.chimapcomboBox.clear()
        self.killmapcomboBox.clear()

        self.getchessrunattrs()
        self.setmapchoices(None, None, None)
        self.setchessrunvalues()

    @pyqtSignature("")
    def on_calcButton_clicked(self):
        self.calcfromcommand()
    def calcfromcommand(self):
        a=unicode(self.cmdLineEdit.text()).encode()
        b=('','',a)
        c=[]

        while len(b[2])>0:
            b=b[2].partition(' ')
            if b[0]!='':
                c+=[b[0]]

        if ('mesh' in c[0]) or ('a2scan' in c[0]):
            i=2
            j=6
            if 'samz' in c[1]:
                i=6
                j=2
            if 'sam' not in c[1]:
                i=1
                if 'sam' not in c[4]:
                    j=4
            if 'a2scan' in c[0]:
                c=c[:min(i, j)+2]+[c[-2]]+c[min(i, j)+2:]
        if 'ascan' in c[0]:
            if c[1]=='samx':
                i=2
                j=len(c)
                if 'samz=' in c[-1]:
                    c+=[c[-1].partition('=')[2], c[-1].partition('=')[2], '0']
                else:
                    c+=['0', '0', '0']
            if c[1]=='samz':
                j=2
                i=len(c)
                if 'samx=' in c[-1]:
                    c+=[c[-1].partition('=')[2], c[-1].partition('=')[2], '0']
                else:
                    c+=['0', '0', '0']
        try:
            xgrid=(numpy.float32(eval(c[i])),numpy.float32(eval(c[i+1])),numpy.uint16(eval(c[i+2])))
            zgrid=(numpy.float32(eval(c[j])),numpy.float32(eval(c[j+1])),numpy.uint16(eval(c[j+2])))
            if xgrid[2]==0:
                temp=0
            else:
                temp=(xgrid[1]-xgrid[0])/(xgrid[2])
            xgrid=(xgrid[0], temp, xgrid[2]+1)
            self.xstartSpinBox.setValue(xgrid[0])
            self.xintSpinBox.setValue(xgrid[1])
            self.xptsSpinBox.setValue(xgrid[2])
            if zgrid[2]==0:
                temp=0
            else:
                temp=(zgrid[1]-zgrid[0])/(zgrid[2])
            zgrid=(zgrid[0], temp, zgrid[2]+1)
            self.zstartSpinBox.setValue(zgrid[0])
            self.zintSpinBox.setValue(zgrid[1])
            self.zptsSpinBox.setValue(zgrid[2])
            if len(c)>max(i, j)+2:
                counter=eval(c[max(i, j)+3])
            else:
                counter=0
            self.inttimeSpinBox.setValue(counter)
            if counter<0:
                self.integLabel.setText('integration\nXflash cts')
            else:
                self.integLabel.setText('integration\ntime (s)')
        except (SyntaxError, NameError, IndexError):
            QMessageBox.warning(self,"syntax error",  "grid values were not generated")
            pass


class getgroupDialog(QDialog,
        ui_get_group.Ui_getgroupDialog):
    def __init__(self, parent, h5path):
        super(getgroupDialog, self).__init__(parent)
        self.setupUi(self)
        self.h5path=h5path
        self.groupsComboBox.clear()
        h5file=h5py.File(self.h5path, mode='r')
        dfltgrp=getdefaultscan(self.h5path)
        dfltind=None
        count=0
        for group in h5file.iterobjects():
            if isinstance(group,h5py.Group)  and 'analysis' in group:
                xrdname=getxrdname(group['analysis'])
                if ('measurement/'+xrdname in group) and ('analysis/'+xrdname in group):
                    self.groupsComboBox.insertItem(count,group.name.rpartition('/')[2])
                    if dfltgrp==group.name.rpartition('/')[2]:
                        dfltind=count
                    count+=1
        h5file.close()
        if not dfltind is None:
            self.groupsComboBox.setCurrentIndex(dfltind)

class selectorDialog(QDialog,
        ui_get_group.Ui_getgroupDialog):

    def __init__(self, parent, itemnames, title='Select an item', setindex=0):
        super(selectorDialog, self).__init__(parent)
        self.setupUi(self)
        self.groupsComboBox.clear()
        for count, item in enumerate(itemnames):
            self.groupsComboBox.insertItem(count,item)
        self.groupsComboBox.setCurrentIndex(setindex)
        self.setWindowTitle(title)

class plotsoDialog(QDialog,
        ui_plotsomenu.Ui_plotsoDialog):

    def __init__(self, parent, itemnames, low, high, title='Select an item'):
        super(plotsoDialog, self).__init__(parent)
        self.setupUi(self)
        self.lowSpinBox.setValue(low)
        self.highSpinBox.setValue(high)
        self.typeComboBox.clear()
        for item in itemnames:
            self.typeComboBox.insertItem(999,item)
        self.typeComboBox.setCurrentIndex(0)
        self.typeComboBox.setWindowTitle(title)

class pdfDialog(QDialog,
        ui_pdfDialog.Ui_pdfDialog):
    def __init__(self, parent, filename='PDFentries.txt', cvtfcn=lambda x:d_q(x/10.0)):
        super(pdfDialog, self).__init__(parent)
        self.setupUi(self)
        names, pdflist=readpdffile(os.path.join(defaultdir('pdfentries'), filename))
        self.pdflist=[[[cvtfcn(d), h] for d, h in pdf] for pdf in pdflist[::-1]]

        for name in names:
            self.pdfcomboBox.insertItem(0, name)

        self.labellineEdit.setText('')
        self.colorlineEdit.setText('r')

class messageDialog(QDialog,
        ui_message_box.Ui_messageDialog):

    def __init__(self, parent, msg):
        super(messageDialog, self).__init__(parent)
        self.setupUi(self)
        self.messageLabel.setText(msg)

class qqanalysisDialog(QDialog,
        ui_analyze_qq.Ui_qqanalysisDialog):
    def __init__(self, parent):
        super(qqanalysisDialog, self).__init__(parent)
        self.setupUi(self)


class peakqqassociationDialog(QDialog,
        ui_associate_pkqq.Ui_peakqqassociationDialog):
    def __init__(self, parent):
        super(peakqqassociationDialog, self).__init__(parent)
        self.setupUi(self)

class makephasesDialog(QDialog,
        ui_make_phases_menu.Ui_makephasesDialog):
    def __init__(self, parent):
        super(makephasesDialog, self).__init__(parent)
        self.setupUi(self)

class spatialphasesDialog(QDialog,
        ui_spatial_phases_menu.Ui_spatialphasesDialog):
    def __init__(self, parent):
        super(spatialphasesDialog, self).__init__(parent)
        self.setupUi(self)

class chiqDialog(QDialog,
        ui_chiqDialog.Ui_chiqDialog):
    def __init__(self, parent, qgrid, chigrid):
        super(chiqDialog, self).__init__(parent)
        self.setupUi(self)
        self.gridLabel.setText('Q is currently starting at %0.2f with %0.2f interval. Approximately %0.2f pts\nChi is currently starting at %0.2f, with %0.2f interval. Approximately %0.2f pts' %tuple(qgrid+chigrid))

class plot2dintwindow(QDialog):
    def __init__(self, parent, h5path, h5groupstr, runpath, navchoice, navkill=False):
        super(plot2dintwindow, self).__init__(parent)

        self.navchoice=navchoice
        self.critradius=36 #2mm of edge of 3" wafer off limits
        
        self.navkill=navkill
        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.runpath=runpath

        self.savename1=''.join((os.path.split(self.h5path)[1][0:-3], self.h5groupstr.rpartition('.')[2], '_'))
        self.imnamelist=[]


        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        attrdict=getattr(self.h5path, self.h5groupstr)
        self.pointlist=h5analysis.attrs['pointlist']
        
        self.bin=getbin(h5analysis)

        self.killmap=getkillmap(h5analysis.attrs['killmapstr'])
        self.killmapbin=getkillmap(h5analysis.attrs['killmapstr'], bin=self.bin)
        self.imagewidth=self.killmap.shape[0]
        
#for display killmap also takes out pixels not in imap - for editing killmap, don't involve imap
        self.imap, self.qgrid=getimapqgrid(h5analysis.attrs['imapstr'])
        self.imapbin=getimapqgrid(h5analysis.attrs['imapstr'], qgrid=False, bin=self.bin)

        self.imapkillmap=self.killmap*(self.imap!=0)
        self.imapkillmapbin=self.killmapbin*(self.imapbin!=0)


        self.chimap, self.chigrid=getchimapchigrid(h5analysis.attrs['chimapstr'])
        self.chimapbin=getchimapchigrid(h5analysis.attrs['chimapstr'], chigrid=False, bin=self.bin)

        self.bcknd=attrdict['bcknd']
        if 'lin' in self.bcknd:
            self.bckndarr, self.blinwts=readblin(h5mar)
            self.bckndarrbin, self.blinwts=readblin(h5mar, bin=self.bin)
        else:
            bstr=''.join(('b', self.bcknd[:3]))
            self.bckndarr=readh5pyarray(h5mar[bstr])
            bstr=''.join((bstr, 'bin%d' %self.bin))
            self.bckndarrbin=readh5pyarray(h5mar[bstr])

        if self.bcknd=='minanom':
            if 'bimap' in h5mar:
                bimap=readh5pyarray(h5mar['bimap'])
                bqgrid=h5mar['bimap'].attrs['bqgrid']
            else:
                bimap=None
                bqgrid=None
            self.banomcalc=(self.imapbin, self.qgrid, attrdict, bimap, bqgrid)
            self.bminanomf=readh5pyarray(h5mar['bminanomf'])

        h5file.close()

        self.imnumlist=self.pointlist[:]
        self.imnamelist=['%d' %p for p in self.pointlist]

        self.bcknd=attrdict['bcknd']

        self.xgrid=attrdict['xgrid']
        self.zgrid=attrdict['zgrid']
        self.xcoords=attrdict['x']
        self.zcoords=attrdict['z']
        self.L=attrdict['cal'][2]
        self.wl=attrdict['wavelength']
        self.psize=attrdict['psize']

        self.setWindowTitle('Plot 2D Intensity')

        self.logCheckBox=QCheckBox()
        self.logCheckBox.setText('logarithmic\nintensity')
        self.logCheckBox.setChecked(False)

        self.killCheckBox=QCheckBox()
        self.killCheckBox.setText('apply kill map\nin main image')
        self.killCheckBox.setChecked(True)


        self.binCheckBox=QCheckBox()
        self.binCheckBox.setText('use binned data')
        self.binCheckBox.setChecked(True)
        QObject.connect(self.binCheckBox,SIGNAL("stateChanged()"),self.fillimComboBox)


        self.bckndCheckBox=QCheckBox()
        self.bckndCheckBox.setText('subtract background')
        self.bckndCheckBox.setChecked(True)
        self.drawbckndButton=QPushButton()
        self.drawbckndButton.setText('draw bcknd')
        QObject.connect(self.drawbckndButton,SIGNAL("pressed()"),self.drawbcknd)
        self.imComboBox=QComboBox()
        self.imComboBox.setToolTip('spec index of image to be plotted')
        self.drawButton=QPushButton()
        self.drawButton.setText('draw image')
        QObject.connect(self.drawButton,SIGNAL("pressed()"),self.draw)
        self.saveButton=QPushButton()
        self.saveButton.setText('save .png')
        QObject.connect(self.saveButton,SIGNAL("pressed()"),self.save)
        chiqButton=QPushButton()
        if self.chimapbin is None:
            chiqButton.setText('build chimapbin\nfor Chi-Q plot')
        else:
            chiqButton.setText('Chi-Q plot\n(time intensive)')
            QObject.connect(chiqButton,SIGNAL("pressed()"),self.chiqplot)

        rangelayout=QVBoxLayout()
        rangelabel=QLabel()
        rangelabel.setText('Range for cbar:')
        self.rangeLineEdit=QLineEdit()
        self.rangeLineEdit.setToolTip('two comma-delimited\nnumbers for min and max')
        rangelayout.addWidget(rangelabel)
        rangelayout.addWidget(self.rangeLineEdit)

        toplayout=QGridLayout()
        toplayout.addWidget(self.logCheckBox, 0, 0)
        toplayout.addWidget(self.killCheckBox, 0, 1)
        toplayout.addWidget(self.binCheckBox, 0, 2)
        toplayout.addWidget(self.bckndCheckBox, 0, 3)
        toplayout.addWidget(self.drawbckndButton, 0, 4)
        toplayout.addWidget(self.imComboBox, 1, 0)
        toplayout.addWidget(self.drawButton, 1, 1)
        toplayout.addLayout(rangelayout, 1, 2)
        toplayout.addWidget(self.saveButton, 1, 3)
        if self.bcknd=='minanom' and not self.navkill:
            self.banomButton=QPushButton()
            self.banomButton.setText('plot\nbanom')
            QObject.connect(self.banomButton,SIGNAL("pressed()"),self.drawbanom)
            toplayout.addWidget(self.banomButton, 0, 5)
        toplayout.addWidget(chiqButton, 1, 4)
        layout=QVBoxLayout()
        layout.addLayout(toplayout)
        self.imgLabel=QLabel()
        layout.addWidget(self.imgLabel)
        self.plotw = plotwidget(self, width=5, height=5, dpi=100)
        layout.addWidget(self.plotw)



        self.savenavimageButton=QPushButton()
        self.savenavimageButton.setText('save .png\nnavigator')
        QObject.connect(self.savenavimageButton,SIGNAL("pressed()"),self.savenavimage)

        if self.navchoice==0:
            self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
        else:
            elstr=attrdict['elements']

            if self.navchoice==1:
                infotype='DPmolfracALL'
            else:
                infotype='XRFmolfracALL'
            self.elstrlist, self.compsarr=getternarycomps(self.h5path, self.h5groupstr, elstr=elstr, infotype=infotype)
            if self.compsarr is None:
                print 'NO COMPOSITION NAVIGATOR WINDOW BECAUSE PROBLEM CALCULATING COMPOSITIONS'
                self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
            else:
                print 'COMPS:', self.compsarr
                self.navw = compnavigatorwidget(self, self.compsarr, self.elstrlist)
        QObject.connect(self.navw, SIGNAL("picclicked"), self.picclickprocess)

        if self.navkill:
            self.savekillmapimageButton=QPushButton()
            self.savekillmapimageButton.setText('save .png\nkillmap')
            QObject.connect(self.savekillmapimageButton,SIGNAL("pressed()"),self.savekillmapimage)

            self.savekillmapButton=QPushButton()
            self.savekillmapButton.setText('save kill map\nfor analysis')
            QObject.connect(self.savekillmapButton,SIGNAL("pressed()"),self.savekillmap)

            self.clearkillButton=QPushButton()
            self.clearkillButton.setText('clear\nkill map')
            QObject.connect(self.clearkillButton,SIGNAL("pressed()"),self.clearkill)

            self.clickkillButton=QPushButton()
            self.clickkillButton.setText("click kill\nregions")
            QObject.connect(self.clickkillButton,SIGNAL("pressed()"),self.clickkill)

            self.clickkillregionsSpinBox=QSpinBox()
            self.clickkillregionsSpinBox.setValue(1)
            self.clickkillregionsSpinBox.setRange(1, 10)

            self.radkillButton=QPushButton()
            self.radkillButton.setText("rad kill\nbeyond mm")
            QObject.connect(self.radkillButton,SIGNAL("pressed()"),self.radkill)

            self.radkillmmSpinBox=QSpinBox()
            self.radkillmmSpinBox.setValue(173)
            self.radkillmmSpinBox.setRange(1, 173)

            radkilllayout=QHBoxLayout()
            radkilllayout.addWidget(self.radkillButton)
            radkilllayout.addWidget(self.radkillmmSpinBox)

            clickkilllayout=QHBoxLayout()
            clickkilllayout.addWidget(self.clickkillButton)
            clickkilllayout.addWidget(self.clickkillregionsSpinBox)


#            killcontrollayout.addWidget(self.savekillmapimageButton)
#            killcontrollayout.addWidget(self.savekillmapButton)
#            killcontrollayout.addWidget(self.clearkillButton)
#            killcontrollayout.addWidget(self.clickkillButton)
#            killcontrollayout.addWidget(self.clickkillapplyCheckBox)

#            navcontrollayout=QHBoxLayout()



            self.savepointlistButton=QPushButton()
            self.savepointlistButton.setText('save image set\nfor analysis')
            QObject.connect(self.savepointlistButton,SIGNAL("pressed()"),self.savepointlist)

            self.removeedgeButton=QPushButton()
            self.removeedgeButton.setText('remove images at\nsubstrate edge')
            QObject.connect(self.removeedgeButton,SIGNAL("pressed()"),self.removeedge)

            self.togglepointButton=QPushButton()
            self.togglepointButton.setText('             \n             ')
            QObject.connect(self.togglepointButton,SIGNAL("pressed()"),self.togglepoint)
            self.toggleaction=-1 #=0->in lis, action is to remove from list, =1->vice versa

#            navcontrollayout.addWidget(self.savenavimageButton)
#            navcontrollayout.addWidget(self.savepointlistButton)
#            navcontrollayout.addWidget(self.removeedgeButton)
#            navcontrollayout.addWidget(self.togglepointButton)
#            navcontrollayout.addWidget(self.killCheckBox)
            killnavbuttonlayout=QVBoxLayout()
            killnavbuttonlayout.addLayout(radkilllayout)
            killnavbuttonlayout.addLayout(clickkilllayout)
            killnavbuttonlayout.addWidget(self.clearkillButton)
            killnavbuttonlayout.addWidget(self.savekillmapimageButton)
            killnavbuttonlayout.addWidget(self.savekillmapButton)
            killnavbuttonlayout.addWidget(self.savenavimageButton)
            killnavbuttonlayout.addWidget(self.savepointlistButton)
            killnavbuttonlayout.addWidget(self.removeedgeButton)
            killnavbuttonlayout.addWidget(self.togglepointButton)

            leftlayout=QVBoxLayout()
            QObject.connect(self.plotw, SIGNAL("clicksdone"), self.clickkillcont)

#            leftlayout.addLayout(navcontrollayout)
#            leftlayout.addLayout(killcontrollayout)
            self.killw = plotwidget(self, width=3, height=3, dpi=100, showcolbar=False)
            leftlayout.addWidget(self.killw)
            leftlayout.addWidget(self.navw)
            xlayout=QHBoxLayout()
            xlayout.addLayout(leftlayout)
            xlayout.addLayout(killnavbuttonlayout)
            xlayout.addLayout(layout)
            self.setLayout(xlayout)
            self.drawkillmap()
        else:
            leftlayout=QVBoxLayout()
            leftlayout.addWidget(self.savenavimageButton)
            leftlayout.addWidget(self.navw)
            xlayout=QHBoxLayout()
            xlayout.addLayout(leftlayout)
            xlayout.addLayout(layout)
            self.setLayout(xlayout)


            self.killbool=False


        self.navw.plotpoints(self.pointlist, list(set(self.imnumlist)-set(self.pointlist)))
        self.chiqplotbool=False
        self.fillimComboBox()
        self.imname=unicode(self.imComboBox.currentText())

        try:
            self.imnum=eval(self.imname)
        except:
            print 'abortng plot2d because some error in point selections'
            return



    def fillimComboBox(self):
        self.imComboBox.clear()
        if len(self.imnamelist)>0:
            for name in self.imnamelist:
                self.imComboBox.insertItem(999, name)
        else:
            self.imComboBox.insertItem(0, 'err')
        self.imComboBox.setCurrentIndex(0)

    def chiqplot(self):
        idialog=chiqDialog(self, self.qgrid, self.chigrid)
        if idialog.exec_():
            self.chiq_imagebin=idialog.imagebinSpinBox.value()
            self.chiq_chibin=idialog.qbinSpinBox.value()
            self.chiq_qbin=idialog.chibinSpinBox.value()
            self.chiq_solidanglebool=idialog.solidangleCheckBox.isChecked()
            self.chiqplotbool=True
            self.draw()
            self.chiqplotbool=False

    def draw(self):
        self.binbool=self.binCheckBox.isChecked()
        self.bckndbool=self.bckndCheckBox.isChecked()
        self.killbool=self.killCheckBox.isChecked() and (not self.bckndbool)
#        if self.navkill:
#            self.killbool=self.killCheckBox.isChecked()
        rangestr=unicode(self.rangeLineEdit.text())
        try:
            range=eval(rangestr)
            if isinstance(range,(int,float)):
                range=(0., 1.*range)
            if len(range)==1:
                range=(0., range[0])
        except:
            range=None
        self.imname=unicode(self.imComboBox.currentText())
        self.imnum=eval(self.imname)
        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        if self.binbool:
            h5arr=h5file['/'.join((self.h5groupstr, 'analysis/'+getxrdname(h5analysis)+'/countsbin%d' %self.bin))]
        else:
            h5arr=h5file['/'.join((self.h5groupstr,'measurement/'+getxrdname(h5analysis)+'/counts'))]
        plotarr=h5arr[self.imnum, :, :]
        h5file.close()
        if self.bckndbool:
            if self.binbool:
                if self.bckndarrbin is None:
                    QMessageBox.warning(self,"failed",  "binned background not found")
                else:
                    if self.bcknd=='minanom':
                        if self.bminanomf[self.imnum, 0]<0:
                            QMessageBox.warning(self,"failed",  "minanom background not available and will not be calculated with binning\n try again without binning but it will take while")
                            self.bckndbool=False
                        else:
                            h5file=h5py.File(self.h5path, mode='r')
                            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
                            banom=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'banom'))][self.imnum, :, :]
                            h5file.close()
                            plotarr=bckndsubtract(plotarr, self.bckndarrbin, self.imapkillmapbin, btype=self.bcknd, banom_f_f=(banom, self.bminanomf[self.imnum, 0], self.bminanomf[self.imnum, 1]))[0]
                    elif 'lin' in self.bcknd:
                            plotarr=bckndsubtract(plotarr, self.bckndarrbin, self.imapkillmapbin, btype=self.bcknd, linweights=self.blinwts[self.imnum])[0]
                    else:
                        plotarr=bckndsubtract(plotarr, self.bckndarrbin, self.imapkillmapbin, btype=self.bcknd)[0]

            else:
                if self.bckndarr is None:
                    QMessageBox.warning(self,"failed",  "background not found")
                    self.bckndbool=False
                else:
                    if self.bcknd=='minanom':
                        if self.bminanomf[self.imnum, 0]<0:
                            print 'WARNING: calculating bminanom background (for histogram analysis) on the fly: INEFFICIENT'
                            temp=bckndsubtract(plotarr, self.bckndarr, self.imapkillmap, btype=self.bcknd, banomcalc=self.banomcalc)
                            plotarr=temp[0]
                        else:
                            h5file=h5py.File(self.h5path, mode='r')
                            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
                            banom=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'banom'))][self.imnum, :, :]
                            h5file.close()
                            plotarr=bckndsubtract(plotarr, self.bckndarr, self.imapkillmap, btype=self.bcknd, banom_f_f=(banom, self.bminanomf[self.imnum, 0], self.bminanomf[self.imnum, 1]))[0]
                    elif 'lin' in self.bcknd:
                        plotarr=bckndsubtract(plotarr, self.bckndarr, self.imapkillmap, btype=self.bcknd, linweights=self.blinwts[self.imnum])[0]
                    else:
                        plotarr=bckndsubtract(plotarr, self.bckndarr, self.imapkillmap, btype=self.bcknd)[0]
        elif self.killbool:
            if self.binbool:
                plotarr*=self.imapkillmapbin
            else:
                plotarr*=self.imapkillmap
        if self.chiqplotbool:
            if self.binbool:
                imap=self.imapbin
                chimap=self.chimapbin
                killmap=self.imapkillmapbin
            else:
                imap=self.imap
                chimap=self.chimap
                killmap=self.imapkillmap

            if self.chiq_imagebin>1:
                killmap=binboolimage(killmap, bin=self.chiq_imagebin)
                chimap=binimage(chimap, zerokill=True, bin=self.chiq_imagebin, mapbin=self.chiq_chibin)
                imap=binimage(imap, zerokill=True, bin=self.chiq_imagebin, mapbin=self.chiq_qbin)
                plotarr=binimage(plotarr, bin=self.chiq_imagebin)*killmap
            else:
                chimap=mapbin(chimap, mapbin=self.chiq_chibin)
                imap=mapbin(imap, mapbin=self.chiq_qbin)

            qgrid=bingrid_grid(self.qgrid, mapbin=self.chiq_qbin)
            chigrid=bingrid_grid(self.chigrid, mapbin=self.chiq_chibin)
            chivals=q_qgrid_ind(chigrid, range(numpy.max(chimap)))
            qvals=q_qgrid_ind(qgrid, range(numpy.max(imap)))

            datamask=numpy.bool_([[(ch in chimap) and (i in imap)  for ch in xrange(1, numpy.max(chimap)+1)] for i in xrange(1, numpy.max(imap)+1)])
            plotarr=numpy.array([[(plotarr[(chimap==ch)&(imap==i)]).mean(dtype='float32')  for ch in xrange(1, numpy.max(chimap)+1)] for i in xrange(1, numpy.max(imap)+1)], dtype=plotarr.dtype)
            plotarr*=datamask
            if self.chiq_solidanglebool:
                plotarr=numpy.array([row/(1.0*powdersolidangle_q(qvals[count], self.L, self.wl, psize=self.psize)) for count, row in enumerate(plotarr)], dtype=plotarr.dtype)
            self.plotw.performplot(plotarr, upperorigin=False, axesformat='chiq', qvals=qvals, chivals=chivals, log=self.logCheckBox.isChecked(), colrange=range)
            self.savename2=''.join(('ChiQ', self.imname))
        else:
            self.plotw.performplot(plotarr, log=self.logCheckBox.isChecked(), colrange=range)
            self.savename2=self.imname

        self.plotimagewidth=plotarr.shape[0]
        self.plotw.fig.canvas.draw()

        if self.binbool:
            t1=', binned'
            self.savename2=''.join((self.savename2, '_bin'))
        else:
            t1=''
        if self.bckndbool:
            t2=', background subtracted'
            self.savename2=''.join((self.savename2, '_b', self.bcknd))
        else:
            t2=''
        if self.killbool:
            t3=', kill pixels ->0'
            self.savename2=''.join((self.savename2, '_kill'))
        else:
            t3=''
        self.imgLabel.setText(''.join(('plot of image ',self.imname, t1, t2, t3)))


    def drawbcknd(self):
        self.binbool=self.binCheckBox.isChecked()
        self.killbool=self.killCheckBox.isChecked()
        self.imname=unicode(self.imComboBox.currentText())
        self.imnum=eval(self.imname)

        if self.bcknd=='minanom':
            self.binbool=True
            self.killbool=True
            if self.bminanomf[self.imnum, 0]<0:
                QMessageBox.warning(self,"failed",  "banom not available for this image")
            else:
                h5file=h5py.File(self.h5path, mode='r')
                h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
                banom=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'banom'))][self.imnum, :, :]
                h5file.close()
                plotarr=(self.bckndarrbin*self.bminanomf[self.imnum, 0]+banom*self.bminanomf[self.imnum, 0])*self.imapkillmapbin
        elif 'lin' in self.bcknd:
            if self.binbool:
                plotarr=combineimageswithwieghts(self.blinwts[self.imnum], self.bckndarrbin)
            else:
                plotarr=combineimageswithwieghts(self.blinwts[self.imnum], self.bckndarr)
            if self.killbool:
                if self.binbool:
                    plotarr*=self.imapkillmapbin
                else:
                    plotarr*=self.imapkillmap

        else:
            if self.binbool:
                plotarr=self.bckndarrbin
            else:
                plotarr=self.bckndarr
            if self.killbool:
                if self.binbool:
                    plotarr*=self.imapkillmapbin
                else:
                    plotarr*=self.imapkillmap

        self.plotw.performplot(plotarr, log=self.logCheckBox.isChecked())
        self.plotimagewidth=plotarr.shape[0]
        self.repaint()
        self.savename2=self.bcknd
        if self.bcknd=='minanom':
            self.savename2=''.join((self.savename2, self.imname))
            t1=''.join((' for ', self.imname))
        elif self.binbool:
            t1=', binned'
            self.savename2=''.join((self.savename2, '_bin'))
        else:
            t1=''
        self.imgLabel.setText(''.join(('plot of ',self.bcknd,' background image', t1)))
        self.plotw.fig.canvas.draw()

    def drawbanom(self):
        self.imname=unicode(self.imComboBox.currentText())
        temp=self.imname
        while temp.startswith('0'):
            temp=temp[1:]
        if temp=='':
            temp='0'
        self.imnum=eval(temp)
        if self.bminanomf[self.imnum, 0]<0:
            QMessageBox.warning(self,"failed",  "banom not available for this image")
        else:
            h5file=h5py.File(self.h5path, mode='r')
            analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            banom=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'banom'))][self.imnum, :, :]
            h5file.close()
            self.plotw.performplot(banom*self.imapkillmapbin, log=self.logCheckBox.isChecked())
            self.plotimagewidth=banom.shape[0]
            self.repaint()
            self.savename2=''.join(('banom', self.imname))
            self.imgLabel.setText(''.join(('plot of banom for ', self.imname)))
        self.plotw.fig.canvas.draw()

    def drawkillmap(self):
        self.binbool=self.binCheckBox.isChecked()
        if self.binbool:
            self.killw.performplot(self.killmapbin)
        else:
            self.killw.performplot(self.killmap)
        self.killw.fig.canvas.draw()

    def picclickprocess(self, picnum):
        picname='%d' %picnum
        if picname in self.imnamelist:
            for i in range(len(self.imnamelist)):
                if self.imnamelist[i]==picname:
                    self.imComboBox.setCurrentIndex(i)
                    break
        if self.navkill:
            if picnum in self.pointlist:
                self.toggleaction=0
                self.togglepointButton.setText('exclude point\nfrom analysis')
            else:
                self.toggleaction=1
                self.togglepointButton.setText('include point\nin analysis')

        self.draw()

        self.navw.plotpoints(self.pointlist, list(set(self.imnumlist)-set(self.pointlist)), select=[self.imnum])
        self.navw.fig.canvas.draw()


    def togglepoint(self):
        if self.toggleaction>=0: #delete the point and then add it if it was supposed to be added - ensures no duplicates
            pt=self.imnum
            temp=[]
            for i in self.pointlist:
                if i!=pt:
                    temp+=[i]
            self.pointlist=temp
            if self.toggleaction==1:
                self.pointlist+=[pt]
                self.pointlist.sort()
            self.navw.plotpoints(self.pointlist, list(set(self.imnumlist)-set(self.pointlist)), select=[pt])
            self.navw.fig.canvas.draw()

    def save(self):
        self.plotw.save(os.path.join(self.runpath, ''.join((self.savename1, self.savename2))).replace('\\','/').encode())

    def savekillmapimage(self):
        self.killw.save(os.path.join(self.runpath, ''.join((self.savename1, '_killmap'))).replace('\\','/').encode())

    def savenavimage(self):
        self.navw.save(os.path.join(self.runpath, ''.join((self.savename1, '_points'))).replace('\\','/').encode())

    def savekillmap(self):
        h5file=h5py.File(self.h5path, mode='r+')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        killmapgrpstr=h5analysis.attrs['killmapstr']
        chessh5grpstr=killmapgrpstr.rpartition('/')[0]
        h5chess=CHESSRUNFILE('r+')
        h5chesskillgrp=h5chess[chessh5grpstr]
        maxkill=0
        for dset in h5chesskillgrp.iterobjects():
            if isinstance(dset, h5py.Dataset) and (dset.name.rpartition('/')[2]).startswith('killmap') and (dset.name.rpartition('/')[2]).partition('killmap')[2].isdigit():
                maxkill=max(maxkill, eval((dset.name.rpartition('/')[2]).partition('killmap')[2]))
                print 'maxkill', maxkill
        newkillname='killmap%d' %(maxkill+1)
        dset=h5chesskillgrp.create_dataset(newkillname, data=self.killmap)
        dset.attrs['h5createdpath']=str(self.h5path)
        h5chesskillgrp.create_dataset(newkillname+'bin%d' %self.bin,data=self.killmapbin)
        h5chess.close()

        h5analysis.attrs['killmapstr']='/'.join((chessh5grpstr, newkillname))
        updatelog(h5analysis, ''.join(('new killmap created. finished ', time.ctime())))
        h5file.close()


    def clearkill(self):
        shape=self.killmap.shape
        shapebin=self.killmapbin.shape
        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5chess=CHESSRUNFILE()
        self.killmap=readh5pyarray(h5chess[getxrdname(h5analysis)+'killmap'])
        self.killmapbin=readh5pyarray(h5chess[getxrdname(h5analysis)+('killmapbin%d' %self.bin)])
        h5chess.close()
        h5file.close()
        self.imapkillmap=self.killmap*(self.imap!=0)
        self.imapkillmapbin=self.killmapbin*(self.imapbin!=0)
        self.drawkillmap()

    def radkill(self):
        radmm=self.radkillmmSpinBox.value()
        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5chess=CHESSRUNFILE()
        radmap=readh5pyarray(h5chess[getxrdname(h5analysis)+'radiusmap'])
        h5chess.close()
        h5file.close()

        self.killmap[radmap>radmm]=0
        self.killmapbin=binboolimage(self.killmap, bin=self.bin)
        self.imapkillmap=self.killmap*(self.imap!=0)
        self.imapkillmapbin=self.killmapbin*(self.imapbin!=0)
        self.drawkillmap()

    def clickkill(self):
        clicks=self.clickkillregionsSpinBox.value()*2
        self.plotw.countclicks(clicks)
        QMessageBox.information(self, 'INSTRUCTIONS', ''.join(("Click center and then radius of each\ncircle you want to add to kill map.\nTotal of ", "%d" %clicks, " clicks needed.")))

    def clickkillcont(self, ptlist):
        clicklist=numpy.round(numpy.float32(ptlist)*self.imagewidth/self.plotimagewidth)
        print clicklist
        cen=[]
        rad=[]
        for i in range(clicklist.shape[0]//2):
            cen=[clicklist[2*i, 0], clicklist[2*i, 1]]
            rad=numpy.uint16(numpy.ceil(numpy.sqrt((clicklist[2*i, 0]-clicklist[2*i+1, 0])**2+(clicklist[2*i, 1]-clicklist[2*i+1, 1])**2)))

            temp=0
            for pix in range(2*rad+1):
                if 0<=cen[0]+pix-rad<self.imagewidth:
                    d=numpy.uint16(numpy.sqrt(rad**2-(pix-rad)**2))
                    d1=max(0,cen[1]-d)
                    d2=min(self.imagewidth,cen[1]+d+1)
                    self.killmap[cen[0]+pix-rad,d1:d2]=False
                    temp+=d2-d1

        self.killmapbin=binboolimage(self.killmap)
        self.imapkillmap=self.killmap*(self.imap!=0)
        self.imapkillmapbin=binboolimage(self.imapkillmap, bin=self.bin)
        self.drawkillmap()
#
#    def clicklogger(self, posn):
#        #posn is list [x,y] pixels wrt to top left pixel=(0,0) and x,y are fractions of image width
#        if self.countclicks:
#            clicklist+=[[posn[0]*self.imagewidth, posn[1]*self.imagewidth]]
#
    def savepointlist(self):
        h5file=h5py.File(self.h5path, mode='r+')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        h5analysis.attrs['pointlist']=self.pointlist
        updatelog(h5analysis,  ''.join(('user-defined pointlist saved. finished ', time.ctime())))
        h5file.close()

    def removeedge(self):
        temp=[]
        for pt in self.imnumlist:
            if pt in self.pointlist and (self.xcoords[pt]**2+self.zcoords[pt]**2)<self.critradius**2:
                temp+=[pt]
        self.pointlist=temp
        self.navw.plotpoints(self.pointlist, list(set(self.imnumlist)-set(self.pointlist)), select=[self.imnum])
        self.navw.fig.canvas.draw()



class depprofDialog(QDialog,
        ui_dep_prof.Ui_DepProfDialog):

    def __init__(self, parent, elstr=None):

        super(depprofDialog, self).__init__(parent)
        self.setupUi(self)

        self.elLineEdit=[self.lineEditgun0, self.lineEditgun1, self.lineEditgun2, self.lineEditgun3]
        self.rateSpinBox=[self.doubleSpinBoxrate0, self.doubleSpinBoxrate1, self.doubleSpinBoxrate2, self.doubleSpinBoxrate3]
        self.voltSpinBox=[self.doubleSpinBoxvolt0, self.doubleSpinBoxvolt1, self.doubleSpinBoxvolt2, self.doubleSpinBoxvolt3]
        self.dpComboBox=[self.comboBoxdp0, self.comboBoxdp1, self.comboBoxdp2, self.comboBoxdp3]
        self.respLineEdit=[self.lineEditresp0, self.lineEditresp1, self.lineEditresp2, self.lineEditresp3]
        self.fracSpinBox=[self.doubleSpinBoxfrac0, self.doubleSpinBoxfrac1, self.doubleSpinBoxfrac2, self.doubleSpinBoxfrac3]

        for le in  self.elLineEdit:
            le.setText(' ')#to make sure the upcoming update counts as "changed"

        QObject.connect(self.lineEditgun0,SIGNAL("textChanged()"),self.elchanged0)
        QObject.connect(self.lineEditgun1,SIGNAL("textChanged()"),self.elchanged1)
        QObject.connect(self.lineEditgun2,SIGNAL("textChanged()"),self.elchanged2)
        QObject.connect(self.lineEditgun3,SIGNAL("textChanged()"),self.elchanged3)

        QObject.connect(self.pushButtonRespCoef,SIGNAL("pressed()"),self.CalcRespCoef)
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)


        self.readdepprof() #important that ths comes first

        self.propdict={}

        if isinstance(elstr, str):
            elsymlist=self.DecipherElementStr(elstr)
        else:
            elsymlist=elstr

        for elsym, le in zip(elsymlist, self.elLineEdit):
            le.setText(elsym)

        #the above signals are not working so for now at least call the functions for an intial run
        self.elchanged0()
        self.elchanged1()
        self.elchanged2()
        self.elchanged3()



    def DecipherElementStr(self, elstr):
        #elsymbols=[Elemental.table[i].symbol for i in range(len(Elemental.table))]+['X', 'x']
        elsymbols=['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Uub', 'Uut', 'Uuq', 'Uup', 'Uuh', 'Uus', 'Uuo', 'X', 'x']

        foundel=[[el, elstr.find(el)] for el in elsymbols if el in elstr]

        #this next section says if 2 elements matched at the same place take the longer named element. i/e/ if P and Pt found, use Pt
        startinds=set([fe[1] for fe in foundel])
        def strlencmp(a,b):
            return (len(a)>len(b))*2-1
        temp=[]
        for si in startinds:
            temp+=[sorted([fe for fe in foundel if fe[1]==si],key=operator.itemgetter(0),cmp=strlencmp, reverse=True)[0]]
        foundel=temp

        foundel=sorted(foundel,key=operator.itemgetter(1))
        fourelstr=[]
        for i in range(4):
            if i<len(foundel) and not (foundel[i][0] in ['X', 'x']):
                fourelstr+=[foundel[i][0]]
            else:
                fourelstr+=['']
        return fourelstr

    def CalcRespCoef(self):
        elstrlist=[str(le.text()) for le in self.elLineEdit]
        for k, v in GunPropertyDict(elstrlist,True).iteritems():
            self.propdict[k]=v
        self.propdict['ProfileParams']=[self.profiles[cbox.currentIndex()][1] for i, cbox in enumerate(self.dpComboBox) if i in self.propdict['guninds']]
        self.propdict['voltages']=[sb.value() for i, sb in enumerate(self.voltSpinBox) if i in self.propdict['guninds']]
        self.propdict['CenterMolRates']=[sb.value() for i, sb in enumerate(self.rateSpinBox) if i in self.propdict['guninds']]
        print 'propdict'
        print self.propdict
        self.propdict['RespAgunBgunCoef']=SortedRespCoef(self.propdict)
        for le, sb, (a, b, c, f) in zip(self.respLineEdit, self.fracSpinBox, self.propdict['RespAgunBgunCoef']): #will only write as many as are there and only 6 if there are more
            le.setText('%s by %s : %.2f' %(self.propdict['symbol'][self.propdict['guninds'].index(a)], self.propdict['symbol'][self.propdict['guninds'].index(b)], c))
            sb.setValue(f)

    def ExitRoutine(self):
        self.propdict['DepTime']=self.doubleSpinBoxdeptime.value()
        if 'RespAgunBgunCoef' in self.propdict.keys(): #if resputter coef calculations done then don't re-read info even if it has been changed
            for i, (sb, notused) in enumerate(zip(self.fracSpinBox, self.propdict['RespAgunBgunCoef'])):
                self.propdict['RespAgunBgunCoef'][i][3]=sb.value()
            return
        self.propdict['RespAgunBgunCoef']=[]
        elstrlist=[str(le.text()) for le in self.elLineEdit]
        for k, v in GunPropertyDict(elstrlist,True).iteritems():
            self.propdict[k]=v
        self.propdict['ProfileParams']=[self.profiles[cbox.currentIndex()][1] for i, cbox in enumerate(self.dpComboBox) if i in self.propdict['guninds']]
        self.propdict['voltages']=[sb.value() for i, sb in enumerate(self.voltSpinBox) if i in self.propdict['guninds']]
        self.propdict['CenterMolRates']=[sb.value() for i, sb in enumerate(self.rateSpinBox) if i in self.propdict['guninds']]

    def readdepprof(self):
        f=DEPPROFILETXT()
        lines=f.readlines()
        self.profiles=[]
        for l in lines:

            EGDabc=[]
            c=l
            for temp in range(5):
                a,b,c=c.partition('\t')
                EGDabc+=[a]
            EGDabc+=[stripbadcharsfromnumstr(c)]
            nam='_'.join(EGDabc[:3])
            try:
                self.profiles+=[[nam, [eval(EGDabc[3]), eval(EGDabc[4]), eval(EGDabc[5])]]]
                for cbox in self.dpComboBox:
                    cbox.insertItem(99, nam)
            except:
                continue
        f.close()


    def elchanged0(self):
        self.pickprofile(0)
    def elchanged1(self):
        self.pickprofile(1)
    def elchanged2(self):
        self.pickprofile(2)
    def elchanged3(self):
        self.pickprofile(3)

    def pickprofile(self, gunind):
        elstr=str(self.elLineEdit[gunind].text())
        if elstr=='':
            temp=[i for i, prof in enumerate(self.profiles) if 'none' in prof[0]]
            if len(temp)>0:
                self.dpComboBox[gunind].setCurrentIndex(temp[0])
            return

        if gunind==0:
            gunpref=[1, 3] #gun  pref uses gun1to4 not the index 0 to 3
        elif gunind==1:
            gunpref=[1, 3]
        elif gunind==2:
            gunpref=[3, 1]
        else:
            gunpref=[4]
        searchstr=['%s_%d_' %(elstr, gp) for gp in gunpref]+['Pt_%d_' %gunpref[0], '_%d_' %gunpref[0]]
        for sstr in searchstr:
            temp=[[i, prof[0].partition(sstr)[2]] for i, prof in enumerate(self.profiles) if sstr in prof[0]]

            if len(temp)>0:
                temp=sorted(temp, key=operator.itemgetter(1))
                self.dpComboBox[gunind].setCurrentIndex(temp[0][0])
                return


class mini_program_dialog(QDialog,
        ui_mini_program_dialog.Ui_mini_program_dialog):

    def __init__(self, parent, qgrid=None):
        super(mini_program_dialog, self).__init__(parent)
        self.setupUi(self)
        self.cmdtext=''
        self.txtpath=MINIPROGRAMpath()
        self.initfromtxt()

    @pyqtSignature("")
    def on_appendPushButton_clicked(self):
        if self.cmdtext=='':
            self.cmdtext=str(self.programComboBox.currentText())
        else:
            self.cmdtext='\n'.join((self.cmdtext, str(self.programComboBox.currentText())))

    @pyqtSignature("")
    def on_opentxtPushButton_clicked(self):
        temp=mygetopenfile(self, xpath=self.txtpath, markstr='.txt file of mini program database')
        if temp!='':
            self.txtpath=temp
            self.initfromtxt()

    def initfromtxt(self):
        fin = open(self.txtpath, "r")
        lines=fin.readlines()
        fin.close()

        self.programComboBox.clear()
        currentprogram=''
        for l in lines:
            if l.startswith('\n'):
                self.programComboBox.insertItem(99,currentprogram)
                currentprogram=''
            else:
                currentprogram+=l
        if currentprogram!='':
            self.programComboBox.insertItem(99,currentprogram)

class waveset1dparamDialog(QDialog,
        ui_waveset1d_params.Ui_waveset1d_params_Dialog):

    def __init__(self, parent, qgrid=None):
        super(waveset1dparamDialog, self).__init__(parent)
        self.setupUi(self)
        if not (qgrid is None):
            defintpar=minmaxint_qgrid(qgrid)
            self.qminSpinBox.setValue(defintpar[0])
            self.qmaxSpinBox.setValue(defintpar[1])
            self.qintSpinBox.setValue(defintpar[2])


class intparamDialog(QDialog,
        ui_int_params.Ui_intparamDialog):

    def __init__(self, parent):
        super(intparamDialog, self).__init__(parent)
        self.setupUi(self)
        defintpar=integration_params()
        self.qminSpinBox.setValue(defintpar[0])
        self.qmaxSpinBox.setValue(defintpar[1])
        self.qintSpinBox.setValue(defintpar[2])

class chiparamDialog(QDialog,
        ui_chi_params.Ui_chiparamDialog):

    def __init__(self, parent, chessh5grpstr):
        super(chiparamDialog, self).__init__(parent)
        self.setupUi(self)
        chimin, chimax=getchiminmax(chessh5grpstr)
        self.chiminSpinBox.setValue(chimin)
        self.chimaxSpinBox.setValue(chimax)

class qqparamDialog(QDialog,
        ui_qq_params.Ui_qqparamDialog):

    def __init__(self, parent, qgrid, opts, optslabel):
        super(qqparamDialog, self).__init__(parent)
        self.setupUi(self)
        a, b, c=minmaxint_qgrid(qgrid)
        self.qminSpinBox.setValue(a)
        self.qmaxSpinBox.setValue(b)
        self.qintSpinBox.setValue(c)
        self.typeLabel.setText(optslabel)
        for item in opts:
            self.typeComboBox.insertItem(99,item)

class XRDSuiteDialog(QDialog,
        ui_XRDSuite_params.Ui_XRDSuite_params):

    def __init__(self, parent, xtypelist, xtypelabel, imtypelist, imtypelabel, qlow, qhigh):
        super(XRDSuiteDialog, self).__init__(parent)
        self.setupUi(self)

        self.qminSpinBox.setValue(qlow)
        self.qmaxSpinBox.setValue(qhigh)
        self.xtypeLabel.setText(xtypelabel)
        for item in xtypelist:
            self.xtypeComboBox.insertItem(99,item)

        self.imtypeLabel.setText(imtypelabel)
        for item in imtypelist:
            self.imtypeComboBox.insertItem(99,item)

class wavepeak1dDialog(QDialog,
        ui_wavepeak_1d.Ui_wavepeak1dDialog):

    def __init__(self, parent, opts, optslabel, defvals=[2, 100., 20., 1.5]):
        super(wavepeak1dDialog, self).__init__(parent)
        self.setupUi(self)
        self.typeLabel.setText(optslabel)
        self.minridgelength_spinBox.setValue(defvals[0])
        self.minridgewtsum_spinBox.setValue(defvals[1])
        self.wavenoisecutoff_spinBox.setValue(defvals[2])
        self.maxqs_spinBox.setValue(defvals[3])
        for item in opts:
            self.typeComboBox.insertItem(99,item)

class h5fileinfoDialog(QDialog,
        ui_h5file_info.Ui_h5infoDialog):

    def __init__(self, parent, h5path, h5groupstr, showattrs=True):
        super(h5fileinfoDialog, self).__init__(parent)
        self.setupUi(self)
        self.showattrs=showattrs
        h5file=h5py.File(h5path, mode='r')
        h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]
        h5root=h5file[h5groupstr]
        h5mar=h5file['/'.join((h5groupstr, 'analysis', getxrdname(h5analysis)))]
        self.treeWidget=QTreeWidget() #added without knowing if it is necessary
        mainitem=QTreeWidgetItem([h5groupstr],  0)
        self.treeWidget.addTopLevelItem(mainitem)
        self.createTree(h5root, mainitem)
        self.logBrowser.setText(unicode(h5analysis.attrs['modifiedlog']))
        h5file.close()
        self.logLabel.setText(''.join(('log of modifications on ', h5groupstr)))

    def createTree(self, startnode, parentitem):
        print startnode
        print startnode.listobjects()
        for node in startnode.iterobjects():
            if isinstance(node, h5py.Dataset):
                item=QTreeWidgetItem([node.name.rpartition('/')[2]+`node.shape`],  0)
                parentitem.addChild(item)
                if self.showattrs:
                    for attrname, attrval in node.attrs.iteritems():
                        attritem=QTreeWidgetItem([self.attrstring(attrname, attrval)],  0)
                        item.addChild(attritem)
            elif isinstance(node, h5py.Group):
                item=QTreeWidgetItem([node.name.rpartition('/')[2]],  0)
                parentitem.addChild(item)
                self.createTree(node, item)
                if self.showattrs:
                    for attrname, attrval in node.attrs.iteritems():
                        attritem=QTreeWidgetItem([self.attrstring(attrname, attrval)],  0)
                        item.addChild(attritem)

    def attrstring(self, attrname, attrval):
        s="'"+attrname+"':"
        try:
            if isinstance(attrval, str):
                if len(attrval)>100:
                    s+=attrval[:20]+' ... '+attrval[-20:]
                else:
                    s+=attrval
            elif isinstance(attrval, int) or isinstance(attrval, float):
                s+=self.numfmt(attrval)
            elif isinstance(attrval, list) or isinstance(attrval, numpy.ndarray):
                temp=attrval
                temp2=attrval
                ndim=0
                while isinstance(temp, list) or isinstance(temp, numpy.ndarray):
                    if len(temp)==0 or len(temp2)==0:
                        s+='contains empty list'
                        return s
                    temp=temp[0]
                    temp2=temp2[-1]
                    ndim+=1

                    if isinstance(temp, str):
                        attrvalstr=`attrval`
                        attrvalstr=attrvalstr.partition('(')[2].rpartition(',')[0]
                        if len(attrvalstr)>100:
                            s+=attrvalstr[:20]+' ... '+attrvalstr[-20:]
                        else:
                            s+=attrvalstr
                        return s
                if ndim==1:
                    if len(attrval)<10:
                        s+='['+','.join([self.numfmt(attrel) for attrel in attrval])+']'
                    else:
                       s+= '['+',...,'.join([self.numfmt(attrel) for attrel in [temp, temp2]])+']'
                elif ndim==2:
                    s+= '[]'+',..][..,'.join([self.numfmt(attrel) for attrel in [temp, temp2]])+']]'
                else:
                    s+='%d' %ndim +' dimmension structure with first value of '+self.numfmt(temp)
            else:
                raise
        except:
            s+='type is '+`type(attrval)`
        return s

    def numfmt(self, num):
        if isinstance(num, int):
            s='%d' %num
        elif num==0.:
            s='0.0'
        elif numpy.abs(num)<100 and numpy.abs(num)>=.01:
            s='%.4f' %num
        else:
            s=myexpformat(num)
        return s


class plotimapwindow(QDialog):
    def __init__(self, parent, h5path, h5groupstr, runpath, texture=False):
        super(plotimapwindow, self).__init__(parent)


        self.texturebool=texture
        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.runpath=runpath

        self.savename1='_'.join((os.path.split(self.h5path)[1][0:-3], self.h5groupstr, ''))

        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]

        attrdict=getattr(self.h5path, self.h5groupstr)

        self.bin=getbin(h5analysis)
        
        self.pointlist=h5analysis.attrs['pointlist']

        self.killmap=getkillmap(h5analysis.attrs['killmapstr'])
        self.killmapbin=getkillmap(h5analysis.attrs['killmapstr'], bin=self.bin)

#for display killmap also takes out pixels not in imap - for editing killmap, don't involve imap
        self.imap, self.qgrid=getimapqgrid(h5analysis.attrs['imapstr'])
        self.imapbin=getimapqgrid(h5analysis.attrs['imapstr'], qgrid=False, bin=self.bin)

        self.imapkillmap=self.killmap*(self.imap!=0)
        self.imapkillmapbin=self.killmapbin*(self.imapbin!=0)

        if self.texturebool:
            self.chimap, self.chigrid=getchimapchigrid(h5analysis.attrs['chimapstr'])
            self.chimapbin=getchimapchigrid(h5analysis.attrs['chimapstr'], chigrid=False, bin=self.bin)
            self.dqchiimage=getdqchiimage(h5analysis.attrs['dqchiimagestr'])
            self.dqchiimagebin=getdqchiimage(h5analysis.attrs['dqchiimagestr'], bin=self.bin)

        self.bcknd=attrdict['bcknd']
        if 'lin' in self.bcknd:
            self.bckndarr, self.blinwts=readblin(h5mar)
            self.bckndarrbin, self.blinwts=readblin(h5mar, bin=self.bin)
        else:
            bstr=''.join(('b', self.bcknd[:3]))
            self.bckndarr=readh5pyarray(h5mar[bstr])
            bstr=''.join((bstr, 'bin%d' %self.bin))
            self.bckndarrbin=readh5pyarray(h5mar[bstr])


        if self.bcknd=='minanom':
            if 'bimap' in h5mar:
                bimap=readh5pyarray(h5mar['bimap'])
                bqgrid=h5mar['bimap'].attrs['bqgrid']
            else:
                bimap=None
                bqgrid=None
            self.banomcalc=(self.imapbin, self.qgrid, attrdict, bimap, bqgrid)
            self.bminanomf=readh5pyarray(h5mar['bminanomf'])

        self.imnumlist=self.pointlist[:]
        self.imnamelist=['%d' %p for p in self.pointlist]
        for dset in h5mar.iterobjects():
            if isinstance(dset, h5py.Dataset) and len(dset.shape)==2 and (dset.name.rpartition('/')[2]).startswith('b'):
                self.imnamelist+=[dset.name.rpartition('/')[2]]
        h5file.close()

        self.setWindowTitle('Plot integration mapping')
        self.bckndCheckBox=QCheckBox()
        self.bckndCheckBox.setText('subtract background\napply killmap')
        self.bckndCheckBox.setChecked(True)
        self.binCheckBox=QCheckBox()
        self.binCheckBox.setText('use binned data')
        self.binCheckBox.setChecked(True)
        self.drawimapButton=QPushButton()
        self.drawimapButton.setText('draw imap')
        QObject.connect(self.drawimapButton,SIGNAL("pressed()"),self.drawimap)
        self.imComboBox=QComboBox()


        lolabel=QLabel()
        lolabel.setText('low q')
        hilabel=QLabel()
        hilabel.setText('high q')
        qmin, qmax, qint=minmaxint_qgrid(self.qgrid)
        self.lowbinSpinBox=QDoubleSpinBox()
        self.lowbinSpinBox.setDecimals(2)
        self.lowbinSpinBox.setSingleStep(qint)
        self.lowbinSpinBox.setValue(qmin)
        self.lowbinSpinBox.setRange(qmin, qmax)
        self.highbinSpinBox=QDoubleSpinBox()
        self.highbinSpinBox.setDecimals(2)
        self.highbinSpinBox.setSingleStep(qint)
        self.highbinSpinBox.setValue(qmax)
        self.highbinSpinBox.setRange(qmin, qmax)
        spinlayout=QGridLayout()
        spinlayout.addWidget(lolabel, 0, 0)
        spinlayout.addWidget(hilabel, 1, 0)
        spinlayout.addWidget(self.lowbinSpinBox, 0, 1)
        spinlayout.addWidget(self.highbinSpinBox, 1, 1)

        self.drawButton=QPushButton()
        self.drawButton.setText('draw image')
        QObject.connect(self.drawButton,SIGNAL("pressed()"),self.draw)
        self.saveButton=QPushButton()
        self.saveButton.setText('save .png')
        QObject.connect(self.saveButton,SIGNAL("pressed()"),self.save)
        toplayout=QHBoxLayout()
        toplayout.addWidget(self.bckndCheckBox)
        toplayout.addWidget(self.binCheckBox)
        toplayout.addWidget(self.drawimapButton)
        toplayout.addWidget(self.imComboBox)
        toplayout.addLayout(spinlayout)

        buttonlayout=QVBoxLayout()
        buttonlayout.addWidget(self.drawButton)
        buttonlayout.addWidget(self.saveButton)
        toplayout.addLayout(buttonlayout)
        layout=QVBoxLayout()
        layout.addLayout(toplayout)
        self.imgLabel=QLabel()
        layout.addWidget(self.imgLabel)
        self.plotw = plotwidget(self, width=5, height=5, dpi=100)
        layout.addWidget(self.plotw)
        if self.texturebool:
            layout2=QHBoxLayout()
            texturelayout=QVBoxLayout()
            texbuttonlayout=QGridLayout()

            drawchimapButton=QPushButton()
            drawchimapButton.setText('draw chimap')
            QObject.connect(drawchimapButton,SIGNAL("pressed()"),self.drawchimap)
            genpeakButton=QPushButton()
            genpeakButton.setText('list peaks')
            QObject.connect(genpeakButton,SIGNAL("pressed()"),self.fillpeakSpinBox)
            self.peakComboBox=QComboBox()
            peaklabel=QLabel()
            peaklabel.setText('peak q, counts  ')
            self.qwidthSpinBox=QDoubleSpinBox()
            self.qwidthSpinBox.setValue(0.2)
            widthlabel=QLabel()
            widthlabel.setText('annulus q-width')
            self.fulltexplotComboBox=QComboBox()
            self.fulltexplotComboBox.clear()
            self.fulltexplotComboBox.insertItem(0, 'LHS and RHS')
            self.fulltexplotComboBox.insertItem(1, 'ave LHS+RHS')
            self.fulltexplotComboBox.insertItem(2, 'only LHS')
            self.fulltexplotComboBox.insertItem(3, 'only RHS')
            self.fulltexplotComboBox.setCurrentIndex(0)
            self.overlayCheckBox=QCheckBox()
            self.overlayCheckBox.setText('overlay')
            self.overlayCheckBox.setChecked(False)
            self.rawplotCheckBox=QCheckBox()
            self.rawplotCheckBox.setText('Plot raw')
            self.rawplotCheckBox.setChecked(False)
            texdrawButton=QPushButton()
            texdrawButton.setText('draw texture')
            QObject.connect(texdrawButton,SIGNAL("pressed()"),self.drawtexture)

            texdrawfromfileButton=QPushButton()
            texdrawfromfileButton.setText('draw texture\nfrom file')
            QObject.connect(texdrawfromfileButton,SIGNAL("pressed()"),self.drawtexturefromfile)

            texgrpLabel=QLabel()
            texgrpLabel.setText('saved texture name, index')

            self.texgrpComboBox=QComboBox()
            QObject.connect(self.texgrpComboBox,SIGNAL("activated(QString)"),self.filltexgrpcombobox)

            self.fromfileimComboBox=QComboBox()

            texsaveButton=QPushButton()
            texsaveButton.setText('save .png')
            QObject.connect(texsaveButton,SIGNAL("pressed()"),self.savetexpng)

            texbuttonlayout.addWidget(drawchimapButton, 0, 0, 2, 1)
#            texbuttonlayout.addWidget(texgrpLabel, 0, 1, 1, 2)
#            texbuttonlayout.addWidget(self.texgrpComboBox, 1, 1, 1, 2)
#            texbuttonlayout.addWidget(self.fromfileimComboBox, 1, 2, 1, 1)
            texbuttonlayout.addWidget(texdrawfromfileButton, 0, 1, 2, 1)
            texgrplayout=QGridLayout()
            texgrplayout.addWidget(texgrpLabel, 0, 0, 1, 2)
            texgrplayout.addWidget(self.texgrpComboBox, 1, 0, 1, 1)
            texgrplayout.addWidget(self.fromfileimComboBox, 1, 1, 1, 1)
            texbuttonlayout.addLayout(texgrplayout, 0, 2, 2, 1)
            texbuttonlayout.addWidget(genpeakButton, 0, 3, 2, 1)

            texbuttonlayout.addWidget(self.peakComboBox, 1, 4)
            texbuttonlayout.addWidget(peaklabel, 0, 4)
            texbuttonlayout.addWidget(self.qwidthSpinBox, 1, 5)
            texbuttonlayout.addWidget(widthlabel, 0, 5)
            texbuttonlayout.addWidget(self.fulltexplotComboBox, 0, 6, 2, 1)
            texbuttonlayout.addWidget(self.overlayCheckBox, 0, 7, 1, 1)
            texbuttonlayout.addWidget(self.rawplotCheckBox, 1, 7, 1, 1)
            texbuttonlayout.addWidget(texdrawButton, 0, 8, 1, 1)
            texbuttonlayout.addWidget(texsaveButton, 1, 8, 1, 1)

            texturelayout.addLayout(texbuttonlayout)
            self.texplotw = plotwidget(self, width=5, height=5, dpi=100)
            texturelayout.addWidget(self.texplotw)

            layout2.addLayout(layout)
            layout2.addLayout(texturelayout)
            self.setLayout(layout2)

            self.peakComboBox.clear()
            self.peakComboBox.insertItem(999, 'from2D')

            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]



            anyfromfile=False
            if 'texture' in h5mar:
                h5tex=h5mar['texture']
                for grp in h5tex.iterobjects():
                    if isinstance(grp, h5py.Group) and 'icounts' in grp:
                        self.texgrpComboBox.insertItem(999, grp.name.rpartition('/')[2])
                        anyfromfile=True
            h5file.close()
            if anyfromfile:
                self.texgrpComboBox.setCurrentIndex(0)
                self.filltexgrpcombobox()
            else:
                self.texgrpComboBox.setDisabled(True)
                self.fromfileimComboBox.setDisabled(True)
                texdrawfromfileButton.setDisabled(True)
        else:
            self.setLayout(layout)
        self.fillimComboBox()
        self.imname=unicode(self.imComboBox.currentText())

        if self.imname.isdigit():
            self.imnum=eval(self.imname)
        else:
            QMessageBox.warning(self,"failed",  "did not find any diffraction images")
            return
        self.imnum=eval(self.imname)


    def fillimComboBox(self):
        self.imComboBox.clear()
        if len(self.imnamelist)>0:
            for name in self.imnamelist:
                self.imComboBox.insertItem(999, name)
        else:
            self.imComboBox.insertItem(0, 'err')
        self.imComboBox.setCurrentIndex(0)

    def fillpeakSpinBox(self):
        if self.imname.isdigit():
            self.imnum=eval(self.imname)
        else:
            QMessageBox.warning(self,"failed",  "cannot extract peaks for that type of image")
            return

        self.peakComboBox.clear()

        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        if 'pkcounts' in h5mar:
            peaks, garb, heights=peakinfo_pksavearr(h5mar['pkcounts'][self.imnum, :,:])
            for tup in zip(peaks, heights):
                self.peakComboBox.insertItem(999, '%.2f,%.0f' %tup)
        h5file.close()
        self.peakComboBox.insertItem(999, 'from2D')

    def filltexgrpcombobox(self):
        self.fromfileimComboBox.clear()
        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]

        h5tex=h5mar['texture']
        h5texgrp=h5tex[str(self.texgrpComboBox.currentText())]
        pointlist=h5texgrp.attrs['pointlist']
        #counts=readh5pyarray(h5texgrp['icounts'])
        h5file.close()
        for ind in pointlist:
            self.fromfileimComboBox.insertItem(999, '%d' %ind)

    def drawtexturefromfile(self):
        self.imname=unicode(self.fromfileimComboBox.currentText())
        try:
            self.imComboBox.setCurrentIndex(self.imnamelist.index(self.imname))
            pointind=eval(self.imname)#could support bin images but not yet supported
        except:
            QMessageBox.warning(self,"failed",  "cannot find that image")
            return
        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]

        h5tex=h5mar['texture']
        h5texgrp=h5tex[str(self.texgrpComboBox.currentText())]

        self.binCheckBox.setChecked(h5texgrp.attrs['bin']>1)
        self.bckndCheckBox.setChecked(h5texgrp.attrs['bckndbool']>0)

        q=h5texgrp.attrs['q_peaks'][pointind]
        dq=h5texgrp.attrs['qhalfwidth'][pointind]

        self.highbinSpinBox.setValue(q+dq)
        self.lowbinSpinBox.setValue(q-dq)
        ind2d=h5texgrp['ind2d'][pointind, :, :]
        ind2dinds=numpy.where((ind2d[0, :]!=32767)&(ind2d[1, :]!=32767))[0]
        ind2d=(ind2d[0, ind2dinds], ind2d[1, ind2dinds])
        self.draw(ind2d=ind2d)

        #the order is importnat here because self.chivalse and self.countvals are se in self.draw() and then again below

        self.chivals=numpy.float32(q_qgrid_ind(h5texgrp.attrs['chigrid']))
        self.countvals=h5texgrp['icounts'][pointind, :]
        countinds=numpy.where(numpy.logical_not(numpy.isnan(self.countvals)))
        self.countvals=self.countvals[countinds]
        self.chivals=self.chivals[countinds]

        h5file.close()
        self.texplotw.performplot([self.chivals, self.countvals], overlay=self.overlayCheckBox.isChecked(), formstr='k-')
        self.texplotw.fig.canvas.draw()


    def drawtexture(self):
        texplotind=self.fulltexplotComboBox.currentIndex()
        kstr=unicode(self.peakComboBox.currentText())
        if kstr!='from2D':
            kind=ind_qgrid_q(self.qgrid, eval(kstr.partition(',')[0]))
            sideind=max([1, numpy.uint16(numpy.round(self.qwidthSpinBox.value()/2.0/self.qgrid[1]))])
            self.highbinSpinBox.setValue(q_qgrid_ind(self.qgrid, index=kind+sideind))
            self.lowbinSpinBox.setValue(q_qgrid_ind(self.qgrid, index=kind-sideind))
        self.draw(bothnegpos=(lambda x: (x<=1 and (0,) or (x-1,))[0])(texplotind))


        if self.rawplotCheckBox.isChecked():
            self.texplotw.performplot([self.chivals, self.countvals], overlay=self.overlayCheckBox.isChecked(), formstr='k.')

#        bins=numpy.uint16(range(numpy.uint16(numpy.round(min(self.chivals))), numpy.uint16(numpy.round(max(self.chivals)))+1))
#        chivalsint=numpy.uint16(numpy.round(self.chivals))
#        binnedchidata=numpy.float32([[chi, self.countvals[chivalsint==chi].mean()] for chi in bins if chi in chivalsint]).T

        sortedchivals=list(set(self.chivals))
        sortedchivals.sort()
        print [self.dqchivals[self.chivals==chi].size for chi in sortedchivals]
        print 'max', [numpy.max(self.dqchivals[self.chivals==chi]) for chi in sortedchivals]
        binnedchidata=numpy.float32([[chi, (self.countvals[self.chivals==chi]*self.dqchivals[self.chivals==chi]).sum()/self.dqchivals[self.chivals==chi].sum()] for chi in sortedchivals if self.dqchivals[self.chivals==chi].sum()>0]).T
        poschiind=numpy.where(binnedchidata[0, :]>0)
        negchiind=numpy.where(binnedchidata[0, :]<0)


        if texplotind==0:
            self.texplotw.performplot([-1.0*binnedchidata[0][negchiind], binnedchidata[1][negchiind]], overlay=(self.overlayCheckBox.isChecked() or self.rawplotCheckBox.isChecked()))
            self.texplotw.performplot([binnedchidata[0][poschiind], binnedchidata[1][poschiind]], overlay=True)
        elif texplotind==1:
            abschi=numpy.abs(binnedchidata[0][:])
            abschireduced=sorted(list(set(abschi)))
            abschidata=numpy.float32([[chi, binnedchidata[1][abschi==chi].sum()/(abschi==chi).sum()] for chi in abschireduced]).T
            print numpy.float32([(abschi==chi).sum() for chi in abschireduced])
            self.texplotw.performplot([abschidata[0][:], abschidata[1][:]], overlay=(self.overlayCheckBox.isChecked() or self.rawplotCheckBox.isChecked()))
        elif texplotind==2:
            self.texplotw.performplot([-1.0*binnedchidata[0][negchiind], binnedchidata[1][negchiind]], overlay=(self.overlayCheckBox.isChecked() or self.rawplotCheckBox.isChecked()))
        else:
            self.texplotw.performplot([binnedchidata[0][poschiind], binnedchidata[1][poschiind]], overlay=(self.overlayCheckBox.isChecked() or self.rawplotCheckBox.isChecked()))

            #for splitting >90 and <90
#            ind90=myargmax(binnedchidata[0, :]//90)
#            self.texplotw.performplot([binnedchidata[0, :ind90], binnedchidata[1, :ind90]], overlay=(self.overlayCheckBox.isChecked() or self.rawplotCheckBox.isChecked()))
#            self.texplotw.performplot([180-binnedchidata[0,ind90:], binnedchidata[1,ind90:]], overlay=True)


        self.texplotw.fig.canvas.draw()


    def draw(self, ind2d=None, bothnegpos=0):#bothnegpos should be 0 for both neative and positive chiinds, 1 for negative only and 2 for positive only, if ind2d is passed then bothnegpos is not used
        self.bckndbool=self.bckndCheckBox.isChecked()
        self.binbool=self.binCheckBox.isChecked()
        self.imname=unicode(self.imComboBox.currentText())

        if not self.imname.isdigit():
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            plotarr=readh5pyarray(h5mar[self.imname])
            h5file.close()

            if plotarr.shape==self.imap.shape:
                imap=self.imap*self.killmap
            elif plotarr.shape==self.imapbin.shape:
                imap=self.imapbin*self.killmapbin
            else:
                QMessageBox.warning(self,"failed",  "cannot draw because array shape does nto match with imap or imapbin")
                return
        else:
            self.imnum=eval(self.imname)

            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            if self.binbool:
                h5arr=h5file['/'.join((self.h5groupstr, 'analysis/'+getxrdname(h5analysis)+'/countsbin%d' %self.bin))]
                imap=self.imapbin*self.killmapbin
            else:
                h5arr=h5file['/'.join((self.h5groupstr,'measurement/'+getxrdname(h5analysis)+'/counts'))]
                imap=self.imap*self.killmap

            plotarr=h5arr[self.imnum, :, :]
            h5file.close()


            if self.bckndbool:
                if self.binbool:
                    if self.bckndarrbin is None:
                        QMessageBox.warning(self,"failed",  "binned background not found")
                    else:
                        if self.bcknd=='minanom':
                            if self.bminanomf[self.imnum, 0]<0:
                                QMessageBox.warning(self,"failed",  "minanom background not available and will not be calculated with binning\n try again without binning but it will take while")
                                self.bckndbool=False
                            else:
                                h5file=h5py.File(self.h5path, mode='r')
                                h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
                                banom=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'banom'))][self.imnum, :, :]
                                h5file.close()
                                plotarr=bckndsubtract(plotarr, self.bckndarrbin, self.imapkillmapbin, btype=self.bcknd, banom_f_f=(banom, self.bminanomf[self.imnum, 0], self.bminanomf[self.imnum, 1]))[0]
                        elif 'lin' in self.bcknd:
                            plotarr=bckndsubtract(plotarr, self.bckndarrbin, self.imapkillmapbin, btype=self.bcknd, linweights=self.blinwts[self.imnum])[0]
                        else:
                            plotarr=bckndsubtract(plotarr, self.bckndarrbin, self.imapkillmapbin, btype=self.bcknd)[0]

                else:
                    if self.bckndarr is None:
                        QMessageBox.warning(self,"failed",  "background not found")
                        self.bckndbool=False
                    else:
                        if self.bcknd=='minanom':
                            if self.bminanomf[self.imnum, 0]<0:
                                print 'WARNING: calculating bminanom background (for imap plotting) on the fly: INEFFICIENT'
                                temp=bckndsubtract(plotarr, self.bckndarr, self.imapkillmap, btype=self.bcknd, banomcalc=self.banomcalc)
                                plotarr=temp[0]
                            else:
                                h5file=h5py.File(self.h5path, mode='r')
                                h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
                                banom=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'banom'))][self.imnum, :, :]
                                h5file.close()
                                plotarr=bckndsubtract(plotarr, self.bckndarr, self.imapkillmap, btype=self.bcknd, banom_f_f=(banom, self.bminanomf[self.imnum, 0], self.bminanomf[self.imnum, 1]))[0]
                        elif 'lin' in self.bcknd:
                            plotarr=bckndsubtract(plotarr, self.bckndarr, self.imapkillmap, btype=self.bcknd, linweights=self.blinwts[self.imnum])[0]
                        else:
                            plotarr=bckndsubtract(plotarr, self.bckndarr, self.imapkillmap, btype=self.bcknd)[0]

        qminind=ind_qgrid_q(self.qgrid, self.lowbinSpinBox.value(), fractional=False)
        qmaxind=ind_qgrid_q(self.qgrid, self.highbinSpinBox.value(), fractional=False)
        if self.texturebool:
            if self.binbool:
                chimap=self.chimapbin
                dqchiimage=self.dqchiimagebin
            else:
                chimap=self.chimap
                dqchiimage=self.dqchiimage
            if ind2d is None:
                if bothnegpos==1:
                    ind2d=numpy.where((imap>=qminind)&(imap<=qmaxind)&(chimap<0))
                elif bothnegpos==2:
                    ind2d=numpy.where((imap>=qminind)&(imap<=qmaxind)&(chimap>0))
                else:
                    ind2d=numpy.where((imap>=qminind)&(imap<=qmaxind)&(chimap!=0)) #as long as the bin vals are not zero this checks for killmap because imap contains killmap, per a few lines above. the chimap!=0 is just to be safe
            self.chivals=q_qgrid_ind(self.chigrid, numpy.abs(chimap[ind2d])-1)*numpy.sign(chimap[ind2d])
            self.countvals=plotarr[ind2d]
            self.dqchivals=dqchiimage[ind2d]
            plotarrcpy=copy.copy(plotarr)
            plotarr=numpy.zeros(plotarr.shape, dtype='float32')
            plotarr[ind2d]=plotarrcpy[ind2d]
            #plotarr[(imap>=qminind)|(imap<=qmaxind)]=0
        self.plotw.performplot(plotarr)

        self.savename2=self.imname
        t1='%.2f' %(self.lowbinSpinBox.value())
        t2='%.2f' %(self.highbinSpinBox.value())
        self.savename2=''.join((self.savename2, '_q', t1, ' to ', t2))
        self.imgLabel.setText(''.join(('plot of image ',self.savename2)))
        self.plotw.fig.canvas.draw()
        print 'stopping', ASDGADF

    def drawimap(self):
        self.binbool=self.binCheckBox.isChecked()
        self.bckndbool=self.bckndCheckBox.isChecked()
        if self.binbool:
            if self.bckndbool:
                self.plotw.performplot(self.imapbin*self.killmapbin)
            else:
                self.plotw.performplot(self.imapbin)
        else:
            if self.bckndbool:
                self.plotw.performplot(self.imap*self.killmap)
            else:
                self.plotw.performplot(self.imap)
        self.repaint()
        self.savename2='imap'
        self.imgLabel.setText('plot of imap')
        self.plotw.fig.canvas.draw()

    def drawchimap(self):
        self.binbool=self.binCheckBox.isChecked()
        if self.binbool:
            self.plotw.performplot(self.chimapbin)
        else:
            self.plotw.performplot(self.chimap)
        self.repaint()
        self.savename2='chimap'
        self.imgLabel.setText('plot of chimap')
        self.plotw.fig.canvas.draw()

    def save(self):
        self.plotw.save(os.path.join(self.runpath, ''.join((self.savename1, self.savename2))).replace('\\','/').encode())
    def savetexpng(self):
        self.texplotw.save(os.path.join(self.runpath, ''.join((self.savename1, self.savename2, '_texture'))).replace('\\','/').encode())

class plot1dintwindow(QDialog):
    def __init__(self, parent, h5path, h5groupstr, runpath, navchoice, bckndedit=False, addpeaks=False, removepeaks=False, type='h5mar:icounts'):
        super(plot1dintwindow, self).__init__(parent)
        self.parent=parent
        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.runpath=runpath
        self.navchoice=navchoice
        self.bckndedit=bckndedit
        self.addpeaks=addpeaks
        self.removepeaks=removepeaks
        self.savename1='_'.join((os.path.split(self.h5path)[1][0:-3], self.h5groupstr, ''))
        self.imnamelist=[]
        self.type=type

        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]

        if 'h5mar' in type:
            self.h5datagrpstr='/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))
            #qgridtemp=getimapqgrid(h5analysis.attrs['imapstr'], imap=False)
            self.pointlist=h5analysis.attrs['pointlist']
            self.overlayifcountsbool='ifcounts' in h5mar
#            self.countsarrstr='/'.join((self.h5groupstr, 'analysis/mar345', 'icounts'))
#            self.processedcountsarrstr='/'.join((self.h5groupstr, 'analysis/mar345', 'ifcounts'))
            self.qgrid=h5mar['icounts'].attrs['qgrid']
        elif 'h5tex' in type:
            h5grpname=type.partition(':')[2]
            h5tex=h5mar['texture']
            h5texgrp=h5tex[h5grpname]
            self.h5datagrpstr='/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'texture', h5grpname))
            #qgridtemp=h5texgrp.attrs['chigrid']
            self.overlayifcountsbool=False
#            self.countsarrstr='/'.join((self.h5groupstr, 'analysis/mar345', 'texture', h5grpname, 'icounts'))
#            self.processedcountsarrstr='/'.join((self.h5groupstr, 'analysis/mar345', 'texture', h5grpname, 'ifcounts'))
            self.pointlist=h5texgrp.attrs['pointlist']
            self.qgrid=h5texgrp.attrs['chigrid']



        self.attrdict=getattr(self.h5path, self.h5groupstr)

        self.qvals=q_qgrid_ind(self.qgrid)

        self.imnamelist=[]
        if 'icounts' in h5file[self.h5datagrpstr]:
            self.imnamelist+=['i%d' %p for p in self.pointlist]
        if 'ifcounts' in h5file[self.h5datagrpstr]:
            self.imnamelist+=['if%d' %p for p in self.pointlist]
        for node in h5file[self.h5datagrpstr].iterobjects():
            if (node.name.rpartition('/')[2]).startswith('i') and isinstance(node, h5py.Dataset) and len(node.shape)==1:
                self.imnamelist+=[node.name.rpartition('/')[2]]


        if 'additionalpeaks' in h5file[self.h5datagrpstr]:
            self.additionalpeaks=list(readh5pyarray(h5file[self.h5datagrpstr]['additionalpeaks']))
        else:
            self.additionalpeaks=[]
        h5file.close()

        L=self.attrdict['cal'][2]
        wl=self.attrdict['wavelength']
        psize=self.attrdict['psize']
        self.tvals=twotheta_q(self.qvals, wl)
        self.dvals=d_q(self.qvals)
        self.pvals=pix_q(self.qvals, L, wl, psize=psize)
        self.wl=wl
        self.L=L
        self.psize=psize
        
        if len(self.imnamelist)==0:
            print 'NO 1D IMAGES FOUND!'
            return
        self.setWindowTitle('Plot intensity vs scattering vector')

        self.savenavimageButton=QPushButton()
        self.savenavimageButton.setText('save .png\nnavigator')
        QObject.connect(self.savenavimageButton,SIGNAL("pressed()"),self.savenavimage)

        self.xgrid=self.attrdict['xgrid']
        self.zgrid=self.attrdict['zgrid']
        self.xcoords=self.attrdict['x']
        self.zcoords=self.attrdict['z']

        if self.navchoice==0:
            self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
        else:
            elstr=self.attrdict['elements']

            if self.navchoice==1:
                infotype='DPmolfracALL'
            else:
                infotype='XRFmolfracALL'
            self.elstrlist, self.compsarr=getternarycomps(self.h5path, self.h5groupstr, elstr=elstr, infotype=infotype)
            if self.compsarr is None:
                print 'NO COMPOSITION NAVIGATOR WINDOW BECAUSE PROBLEM CALCULATING COMPOSITIONS'
                self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
            else:
                print 'COMPS:', self.compsarr
                self.navw = compnavigatorwidget(self, self.compsarr, self.elstrlist)

        QObject.connect(self.navw, SIGNAL("picclicked"), self.picclickprocess)

        self.saveplotsoButton=QPushButton()
        self.saveplotsoButton.setText('save selected\nimage as plotso')
        QObject.connect(self.saveplotsoButton,SIGNAL("pressed()"),self.toplotso)

        self.logCheckBox=QCheckBox()
        self.logCheckBox.setText('logarithmic\nintensity')
        self.logCheckBox.setChecked(False)

        self.overlayCheckBox=QCheckBox()
        self.overlayCheckBox.setText('overlay on\nexisting plots')
        self.overlayCheckBox.setChecked(False)

        self.xaxisComboBox=QComboBox()
        self.xaxisComboBox.clear()
        if 'h5mar' in type:
            self.xaxisComboBox.insertItem(0, 'pixels')
            self.xaxisComboBox.insertItem(0, 'd (nm)')
            self.xaxisComboBox.insertItem(0, '2th (deg)')
            self.xaxisComboBox.insertItem(0, 'q 1/nm')
        elif 'h5tex' in type:
            self.xaxisComboBox.insertItem(0, 'PHI (deg)')
        self.xaxisComboBox.setCurrentIndex(0)

        self.imComboBox=QComboBox()

        self.drawButton=QPushButton()
        self.drawButton.setText('draw image')
        QObject.connect(self.drawButton,SIGNAL("pressed()"),self.draw)

        self.drawpeaksButton=QPushButton()
        self.drawpeaksButton.setText('draw w/ peaks')
        QObject.connect(self.drawpeaksButton,SIGNAL("pressed()"),self.drawwithpeaks)


        genpeakButton=QPushButton()
        genpeakButton.setText('list peaks')
        QObject.connect(genpeakButton,SIGNAL("pressed()"),self.fillpeakComboBox)

        self.peakComboBox=QComboBox()
        peaklabel=QLabel()
        peaklabel.setText('peak q, counts')
        peakslayout=QVBoxLayout()
        peakslayout.addWidget(peaklabel)
        peakslayout.addWidget(self.peakComboBox)

        plotfitpeakButton=QPushButton()
        plotfitpeakButton.setText('overlay\nfitted peak')
        QObject.connect(plotfitpeakButton,SIGNAL("pressed()"),self.plotfitpeak)

        self.addpdfButton=QPushButton()
        self.addpdfButton.setText('add PDF peaks')
        QObject.connect(self.addpdfButton,SIGNAL("pressed()"),self.drawpdfpeaks)

        self.saveButton=QPushButton()
        self.saveButton.setText('save .png')
        QObject.connect(self.saveButton,SIGNAL("pressed()"),self.save)
        toplayout=QHBoxLayout()
        spaceLabel=QLabel()
        spaceLabel.setText('              ')
        toplayout.addWidget(spaceLabel)
        toplayout.addWidget(spaceLabel)
        toplayout.addWidget(spaceLabel)
        toplayout.addWidget(self.saveplotsoButton)
        toplayout.addWidget(self.savenavimageButton)
        toplayout.addWidget(self.logCheckBox)
        toplayout.addWidget(self.overlayCheckBox)
        toplayout.addWidget(self.xaxisComboBox)
        toplayout.addWidget(self.imComboBox)
        toplayout.addWidget(self.drawButton)
        toplayout.addWidget(self.drawpeaksButton)
        toplayout.addWidget(genpeakButton)
        toplayout.addLayout(peakslayout)
        toplayout.addWidget(plotfitpeakButton)
        toplayout.addWidget(self.addpdfButton)
        toplayout.addWidget(self.saveButton)
        layout=QVBoxLayout()
        leftlayout=QVBoxLayout()
        rightlayout=QVBoxLayout()
        lefttoplayout=QGridLayout()
        plotlayout=QHBoxLayout()

        self.zeroSpinBox=QSpinBox()
        self.zeroSpinBox.setValue(0)
        self.zeroSpinBox.setRange(0,1000000 )

        self.offsetSpinBox=QSpinBox()
        self.offsetSpinBox.setValue(0)
        self.offsetSpinBox.setRange(0,1000000 )

        self.zerolineCheckBox=QCheckBox()
        self.zerolineCheckBox.setText('draw zero line\nfor overlays')
        self.zerolineCheckBox.setChecked(False)

        self.logcutSpinBox=QSpinBox()
        self.logcutSpinBox.setValue(101)
        self.logcutSpinBox.setRange(0,1000000 )

        self.imgLabel=QLabel()

        self.plotw = plotwidget(self, width=5, height=5, dpi=100)
        lab0=QLabel()
        lab1=QLabel()
        lab2=QLabel()
        lab3=QLabel()
        if self.bckndedit:
            self.newadditionfrom1dbckndsubtraction=numpy.zeros(self.qgrid[2], dtype='float32')


            self.calc1dbckndButton=QPushButton()
            self.calc1dbckndButton.setText('calc+plot\nnew bcknd')
            QObject.connect(self.calc1dbckndButton,SIGNAL("pressed()"),self.calc1dbcknd)
            lefttoplayout.addWidget(self.calc1dbckndButton, 0, 0)
            self.save1dbckndButton=QPushButton()
            self.save1dbckndButton.setText('save\nnew bcknd')
            QObject.connect(self.save1dbckndButton,SIGNAL("pressed()"),self.save1dbcknd)
            lefttoplayout.addWidget(self.save1dbckndButton, 0, 1)
            self.revert1dbckndButton=QPushButton()
            self.revert1dbckndButton.setText('revert to as\nintegrated icounts')
            QObject.connect(self.revert1dbckndButton,SIGNAL("pressed()"),self.revert1dbcknd)
            lefttoplayout.addWidget(self.revert1dbckndButton, 0, 2)

            lab3.setText('index interval\nfor interp pts')
            self.bckndindexintervalSpinBox=QSpinBox()
            self.bckndindexintervalSpinBox.setValue(2)
            self.bckndindexintervalSpinBox.setRange(1,1000)
            lefttoplayout.addWidget(lab3, 1, 1)
            lefttoplayout.addWidget(self.bckndindexintervalSpinBox, 1, 2)

            lab0.setText('list of Q\n(comma-delim)')
            lab1.setText('image\nindex')
            lab2.setText('num sigma\nkill length')
            lefttoplayout.addWidget(lab0, 2, 0)
            lefttoplayout.addWidget(lab1, 2, 1)
            lefttoplayout.addWidget(lab2, 2, 2)

            self.bckndLineEditlist=[]
            self.bckndComboBoxlist=[]
            self.bckndSpinBoxlist=[]
            self.bckndcolors=['b','g', 'c', 'y']
            fullnamestemp=['blue', 'green', 'cyan', 'yellow']
            for i in range(4):
                ComboBox=QComboBox()
                self.fillimbckndComboBox(ComboBox)
                LineEdit=QLineEdit()
                SpinBox=QDoubleSpinBox()
                SpinBox.setValue(3.5)
                SpinBox.setRange(0.0,100.0)
                Label=QLabel()
                Label.setText(fullnamestemp[i])
                lefttoplayout.addWidget(LineEdit, i+3, 0)
                lefttoplayout.addWidget(ComboBox, i+3, 1)
                lefttoplayout.addWidget(SpinBox, i+3, 2)
                lefttoplayout.addWidget(Label, i+3, 3)
                self.bckndLineEditlist+=[LineEdit]
                self.bckndComboBoxlist+=[ComboBox]
                self.bckndSpinBoxlist+=[SpinBox]
        elif self.addpeaks:
            lab1.setText('click plot->add peak @ position\nclick nav point->add peak to its list')
            lab2.setText('q-scale of new peak')
            lab3.setText('q-posn of new peak')
            self.addpeakclearButton=QPushButton()
            self.addpeakclearButton.setText('clear the entire add\npeak list (all points)')
            QObject.connect(self.addpeakclearButton,SIGNAL("pressed()"),self.addpeakclear)


            self.addpeaksaveButton=QPushButton()
            self.addpeaksaveButton.setText('save add peak list\nand update icounts')
            QObject.connect(self.addpeaksaveButton,SIGNAL("pressed()"),self.addpeaksave)

            self.addpeakscaleSpinBox=QDoubleSpinBox()
            self.addpeakscaleSpinBox.setValue(.5)
            self.addpeakscaleSpinBox.setRange(0.1,100.0)

            self.addpeakposnSpinBox=QDoubleSpinBox()
            self.addpeakposnSpinBox.setValue(50)
            self.addpeakposnSpinBox.setRange(q_qgrid_ind(self.qgrid, 0), q_qgrid_ind(self.qgrid, self.qgrid[2]-1))

            self.addpeakTextBrowser=QTextBrowser()
            self.addpeakTextBrowser.setReadOnly(True)
            self.addpeakTextBrowser.setPlainText('')

            lefttoplayout.addWidget(lab1, 0, 0, 1, 2)
            lefttoplayout.addWidget(self.addpeakclearButton, 1, 0)
            lefttoplayout.addWidget(self.addpeaksaveButton, 1, 1)
            lefttoplayout.addWidget(lab2, 2, 0)
            lefttoplayout.addWidget(lab3, 2, 1)
            lefttoplayout.addWidget(self.addpeakscaleSpinBox, 3, 0)
            lefttoplayout.addWidget(self.addpeakposnSpinBox, 3, 1)
            lefttoplayout.addWidget(self.addpeakTextBrowser, 4, 0, 3, 2)

        elif self.removepeaks:
            lab1.setText('click peak->remove peak @ position\nclick nav point->remove nearest peak in its list')
            self.activeremoveCheckBox=QCheckBox()
            self.activeremoveCheckBox.setText('remove peaks with clicks is active')
            self.activeremoveCheckBox.setChecked(True)
            self.peaksremoved=QSpinBox()
            self.peaksremoved.setValue(0)
            self.peaksremoved.setDisabled(True)
            lab2.setText('number of peaks removed')
            lefttoplayout.addWidget(lab1, 0, 0)
            lefttoplayout.addWidget(self.activeremoveCheckBox, 1, 0)
            lefttoplayout.addWidget(lab2, 2, 0)
            lefttoplayout.addWidget(self.peaksremoved, 3, 0)
            self.qvalueofpeakremoval=None
        else:
            lab1.setText('cutoff intensity\nfor log plots')
            lab2.setText('intensity axis\nlower limit')
            lab3.setText('offset for\noverlays')
            lefttoplayout.addWidget(lab1, 0, 0)
            lefttoplayout.addWidget(lab2, 0, 1)
            lefttoplayout.addWidget(lab3, 0, 2)
            lefttoplayout.addWidget(self.logcutSpinBox, 1, 0)
            lefttoplayout.addWidget(self.zeroSpinBox, 1, 1)
            lefttoplayout.addWidget(self.offsetSpinBox, 1, 2)
            lefttoplayout.addWidget(self.zerolineCheckBox, 1, 3)


        leftlayout.addLayout(lefttoplayout)
        rightlayout.addWidget(self.imgLabel)
        toolbar=self.plotw.gettoolbarinstance()

        leftlayout.addWidget(self.navw)
        rightlayout.addWidget(self.plotw)
        plotlayout.addLayout(leftlayout)
        plotlayout.addLayout(rightlayout)

        layout.addLayout(toplayout)
        layout.addLayout(plotlayout)

        self.setLayout(layout)
        self.fillimComboBox()

        self.numpdflabels=0
        self.offset=0
        self.savecount=0
        self.selectlist=[]
        self.plotpeaklist=None
        self.imnum=0
        self.imname=unicode(self.imComboBox.currentText())


        if self.imname.startswith('if') and self.imname[2:].isdigit():
            self.imnum=eval(self.imname[2:])
        elif self.imname.startswith('i') and self.imname[1:].isdigit():
            self.imnum=eval(self.imname[1:])

        self.navw.plotpoints(self.pointlist, [])
        QObject.connect(self.plotw, SIGNAL("genericclickonplot"), self.clickhandler)

    def clickhandler(self, clickxy):
        if self.addpeaks:
            self.addpeakposnSpinBox.setValue(clickxy[0])
            self.addpeak()
        if self.removepeaks and self.activeremoveCheckBox.isChecked():
            self.qvalueofpeakremoval=clickxy[0]
            self.removepeak()

    def fillimComboBox(self):
        self.imComboBox.clear()
        if len(self.imnamelist)>0:
            for name in self.imnamelist:
                self.imComboBox.insertItem(999, name)
        else:
            self.imComboBox.insertItem(0, 'err')
        self.imComboBox.setCurrentIndex(0)

    def fillimbckndComboBox(self, box):
        box.clear()
        box.insertItem(0, 'notused')
        for pointind in self.pointlist:
            box.insertItem(999, '%d' %pointind)
        box.setCurrentIndex(0)

    def drawwithpeaks(self):
        self.imname=unicode(self.imComboBox.currentText())
        if self.imname.startswith('if'):
            temp=self.imname[2:]
        else:
            temp=self.imname[1:]
        if temp.isdigit():
            self.imnum=eval(temp)
            pkcmd="h5file[self.h5datagrpstr]['pkcounts'][self.imnum,:,:]"
        else:
            pkcmd="h5file[self.h5datagrpstr]['pk'+temp][:,:]"

        h5file=h5py.File(self.h5path, mode='r')

        try:
            peaks=eval(pkcmd)
        except:
            h5file.close()
            print 'abort: problem getting peak data for ', self.imname
            return
        qvals, garb, heights=peakinfo_pksavearr(peaks)
        sortind=numpy.argsort(qvals)
        qvals=qvals[sortind]
        heights=heights[sortind]
        a, b, c=minmaxint_qgrid(self.qgrid)
        withinqgridinds=numpy.where((qvals>a)&(qvals<b))[0]
        if len(withinqgridinds)!=len(qvals):
            QMessageBox.warning(self,"warning",  "some peaks positions beyond edges of dataset")

        if not self.imname.startswith('if'):
            pkinds=numpy.uint16(numpy.round(ind_qgrid_q(self.qgrid, qvals)))
            pkinds=pkinds[withinqgridinds]
            cmpneighbor=pkinds[:-1]==pkinds[1:]
            if numpy.any(cmpneighbor):
                QMessageBox.warning(self,"warning",  "some peaks perfectly overlap, only plotting one of the overlaps with the correct height")
                cmpneighbor=numpy.logical_not(numpy.append(cmpneighbor, numpy.bool_([False])))
                pkinds=pkinds[cmpneighbor]
                withinqgridinds=withinqgridinds[cmpneighbor]
            heights[withinqgridinds]=h5file[self.h5datagrpstr]['icounts'][self.imnum, pkinds]#if icounts then heights of peaks plotted as the ictouns value, except if the posn is beyond the limits

        h5file.close()

        xtype=unicode(self.xaxisComboBox.currentText())
        if 'pix' in xtype:
            xvals=pix_q(qvals, self.L, self.wl, psize=self.psize)
        elif '(nm)' in xtype:
            xvals=d_q(qvals)
        elif '2' in xtype:
            xvals=twotheta_q(qvals, self.wl)
        else:
            xvals=qvals
        self.plotpeaklist=[xvals, heights]
        self.draw()

    def draw(self):
        h5file=h5py.File(self.h5path, mode='r')

        self.imname=unicode(self.imComboBox.currentText())

        if self.imname.startswith('if'):
            temp=self.imname[2:]
            h5counts=h5file[self.h5datagrpstr]['ifcounts']
        else:
            temp=self.imname[1:]
            h5counts=h5file[self.h5datagrpstr]['icounts']
        if temp.isdigit():
            self.imnum=eval(temp)
            icmd="h5counts[self.imnum,:]"
        else:
            icmd="h5file[self.h5datagrpstr][self.imname][:]"

        try:
            plotarr=eval(icmd)
        except:
            h5file.close()
            print 'abort: problem getting data for ', self.imname
            self.plotpeaklist=None
            return

        h5file.close()
        xtype=unicode(self.xaxisComboBox.currentText())
        xtransformed=True
        if 'pix' in xtype:
            xvals=self.pvals
            t1='pix'
        elif '(nm)' in xtype:
            xvals=self.dvals
#            plotarr=numpy.array([plotarr[-1*i-1] for i in range(plotarr.size)])
            t1='d'
        elif '2' in xtype:
            xvals=self.tvals
            t1='2th'
        else:
            xvals=self.qvals
            if 'PHI' in xtype:
                t1='PHI'
            else:
                t1='q'
            xtransformed=False

        notnaninds=numpy.where(numpy.logical_not(numpy.isnan(plotarr)))
        xvals=xvals[notnaninds]
        plotarr=plotarr[notnaninds]

        if self.logCheckBox.isChecked():
            plotarr[plotarr<self.logcutSpinBox.value()]=self.logcutSpinBox.value()

        if self.overlayCheckBox.isChecked():
            if self.logCheckBox.isChecked():
                self.offset+=(self.offset==0)
                self.offset*=self.offsetSpinBox.value()
                plotarr*=self.offset

            else:
                self.offset+=self.offsetSpinBox.value()
                plotarr+=self.offset
            if self.zerolineCheckBox.isChecked():
                xvals=numpy.concatenate((numpy.array([xvals[-1], xvals[0]]), xvals))
                plotarr=numpy.concatenate((numpy.array([self.offset, self.offset]), plotarr))
        else:
            self.offset=0
            self.selectlist=[]
        if not self.imname.startswith('ib'):
            self.selectlist+=[self.imnum]
        if (len(self.selectlist)+self.imname.startswith('ib'))==1:
            self.savename2=''.join(('_Ivs', t1,'_', self.imname))
        else:
            self.savename2=''.join((self.savename2,'_', self.imname))
        ylowlim=self.zeroSpinBox.value()
        if ylowlim==0:
            ylowlim=None
        if self.bckndedit:
            plotarr+=self.newadditionfrom1dbckndsubtraction
        #self.plotw.axes.plot(xvals, plotarr,'k-',  linewidth=2)
        if not self.plotpeaklist is None:
            self.plotpeaklist=[self.plotpeaklist[0], self.plotpeaklist[1]+self.offset]
        self.plotw.performplot([xvals, plotarr], overlay=self.overlayCheckBox.isChecked(), log=self.logCheckBox.isChecked(), ylowlimit=ylowlim, peaklist=self.plotpeaklist)
        self.plotpeaklist=None

        if self.addpeaks:
            if xtransformed:
                print 'added peaks will only be plotted for q-axis'
            else:
                ylim=self.plotw.axes.get_ylim()
                for peak in self.additionalpeaks:
                    if self.imnum==peak[0]:
                        self.plotw.axes.plot([peak[2], peak[2]], [ylim[0], ylim[1]], 'r-')
        self.navw.plotpoints(self.pointlist, [], select=self.selectlist)
        self.imgLabel.setText(self.savename2)
        self.plotw.fig.canvas.draw()
        self.navw.fig.canvas.draw()

    def toplotso(self):
        self.imname=unicode(self.imComboBox.currentText())
        if self.imname.startswith('if'):
            temp=self.imname[2:]
        else:
            temp=self.imname[1:]
        if temp.isdigit():
            self.imnum=eval(temp)
            icmd="h5file[self.h5datagrpstr]['ifcounts'][self.imnum,:]"
        else:
            icmd="h5file[self.h5datagrpstr][temp][:]"

        h5file=h5py.File(self.h5path, mode='r')


        try:
            plotarr=eval(icmd)
        except:
            h5file.close()
            print 'abort: problem getting data for ', self.imname
            self.plotpeaklist=None
            return

        h5file.close()
        xtype=unicode(self.xaxisComboBox.currentText())
        if 'pix' in xtype:
            xvals=self.pvals
            t1='pix'
        elif '(nm)' in xtype:
            xvals=self.dvals
#            plotarr=numpy.array([plotarr[-1*i-1] for i in range(plotarr.size)])
            t1='d'
        elif '2' in xtype:
            xvals=self.tvals
            t1='2th'
        else:
            xvals=self.qvals
            t1='q'

        notnaninds=numpy.where(numpy.logical_not(numpy.isnan(plotarr)))
        xvals=xvals[notnaninds]
        plotarr=plotarr[notnaninds]

        writeplotso(self.runpath, xvals, plotarr, self.attrdict, t1, ''.join((self.savename1, '_Ivs', t1, '_', self.imname)))


    def picclickprocess(self, picnum):
        picname='i%d' %picnum #set selection to innn but then if ifnnn exists, set it to that instead
        if picname in self.imnamelist:
            for i in range(len(self.imnamelist)):
                if self.imnamelist[i]==picname:
                    self.imComboBox.setCurrentIndex(i)
                    break
        picname='if%d' %picnum
        if picname in self.imnamelist:
            for i in range(len(self.imnamelist)):
                if self.imnamelist[i]==picname:
                    self.imComboBox.setCurrentIndex(i)
                    break
#        if not self.overlayCheckBox.isChecked():
#            self.selectlist=[]
#
#        self.selectlist+=[self.imnum]

        self.draw()
        self.navw.plotpoints(self.pointlist, [], select=self.selectlist)
        if self.addpeaks:
            self.addpeak()
        if self.removepeaks and self.activeremoveCheckBox.isChecked() and not (self.qvalueofpeakremoval is None):
            self.removepeak()
        self.navw.fig.canvas.draw()

    def drawpdfpeaks(self):
        if 'h5tex' in self.type:
            idialog=pdfsearchDialog(self.parent, self.plotw, self.offset, filename='TextureDatabase.txt', cvtfcn=lambda x:x)
        else:
            idialog=pdfsearchDialog(self.parent, self.plotw, self.offset)
        idialog.exec_()
#        idialog=pdfDialog(self)
#        if idialog.exec_():
#            label=unicode(idialog.labellineEdit.text())
#            colstr=unicode(idialog.colorlineEdit.text())
#            if colstr=='':
#                colstr='r'
#            pdf=idialog.pdflist[idialog.pdfcomboBox.currentIndex()]
#            h=idialog.heightSpinBox.value()
#            self.plotw.axes.hold(True)
#            for q, height in pdf:
#                if h!=0:
#                    height=h
#                else:
#                    height*=(self.plotw.axes.get_ylim()[1]-self.offset)*0.8
#                self.plotw.axes.plot([q, q], [self.offset, self.offset+height], colstr)
#            if label!='':
#                for garbage in range(self.numpdflabels):
#                    label=''.join(('     ', label))
#                self.numpdflabels+=1
#                ylim=self.plotw.axes.get_ylim()
#                xlim=self.plotw.axes.get_xlim()
#                print xlim, ylim
#                self.plotw.axes.text(xlim[0]+.05*(xlim[1]-xlim[0]), ylim[1]-.05*(ylim[1]-ylim[0]), label, color=colstr, fontsize=14)
#            self.plotw.fig.canvas.draw()

    def calc1dbcknd(self): #only supported for 'h5mar' type
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        ibmin=h5mar['ibmin']
        self.plotw.axes.clear()
        self.plotw.axes.hold(True)
        self.alteredbcknd=ibmin[:]
        self.newadditionfrom1dbckndsubtraction=ibmin[:]*0.0
        self.savedictbcknd1d={}
        self.savedictbcknd1d['imageindeces']=[]
        self.savedictbcknd1d['peakexclusionwidths']=[]
        self.savedictbcknd1d['interpindexinterval']=self.bckndindexintervalSpinBox.value()
        self.savedictbcknd1d['enteredqvals']=[]
        self.savedictbcknd1d['enteredexclusionwidths']=[]
        imnum_sig_col=[]
        enteredqvals_sig_col=[]
        for i in range(4):
            imnumstr=unicode(self.bckndComboBoxlist[i].currentText())
            lestr=str(self.bckndLineEditlist[i].text())
            if len(lestr)>0:
                try:
                    eqv=numpy.float32(eval('['+lestr+']'))
                    if len(eqv.shape)!=1:
                        raise
                    enteredqvals_sig_col+=[(eqv, self.bckndSpinBoxlist[i].value(), self.bckndcolors[i])]
                    continue
                except:
                    print 'FORMAT ERROR ON ENTERED Q-VALS. should be comma delimited Q-vals.'
            if imnumstr.isdigit():
                imnum_sig_col+=[(eval(imnumstr), self.bckndSpinBoxlist[i].value(), self.bckndcolors[i])]
        if len(imnum_sig_col)==0 and len(enteredqvals_sig_col)==0:
            return

        bckndinds=set(range(int(round(self.qgrid[2]))))

        for qvals, sigwidth, col in enteredqvals_sig_col:
            self.savedictbcknd1d['enteredqvals']+=list(qvals)
            self.savedictbcknd1d['enteredexclusionwidths']+=[sigwidth]*len(qvals)
            peakposn=ind_qgrid_q(self.qgrid, qvals, fractional=True)
            s=sigwidth/self.qgrid[1]
            for p in peakposn:
                bckndinds-=set(range(int(round(p-s)), int(round(p+s))+1))

        for imnum, sigwidth, col in imnum_sig_col:
            self.savedictbcknd1d['imageindeces']+=[imnum]
            self.savedictbcknd1d['peakexclusionwidths']+=[sigwidth]
            counts=h5mar['ifcounts'][imnum][:]
            peakposn, peaksig, garb=peakinfo_pksavearr(h5mar['pkcounts'] [imnum, :, :])

            peakposn=ind_qgrid_q(self.qgrid, peakposn, fractional=True)
            peaksig=sigwidth*peaksig/self.qgrid[1]
            for p, s in zip(peakposn, peaksig):
                bckndinds-=set(range(int(round(p-s)), int(round(p+s))+1))
            self.plotw.axes.plot(self.qvals, counts, col)
        bckndinds=sorted(list(bckndinds))
        self.alteredbcknd=fillgapswithinterp(range(int(round(self.qgrid[2]))), bckndinds, ibmin[bckndinds], indexinterval_fitinds=self.bckndindexintervalSpinBox.value())
        self.plotw.axes.plot(self.qvals, ibmin, 'k')
        self.plotw.axes.plot(self.qvals, self.alteredbcknd, 'r')
        self.newadditionfrom1dbckndsubtraction=ibmin-self.alteredbcknd
        self.plotw.fig.canvas.draw()

        self.savename2='1dbckndalteration'
        self.imgLabel.setText(self.savename2)

    def save1dbcknd(self):
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        icountspoint=h5mar['icounts']
        if 'asintegratedicounts' in h5mar:
            del h5mar['asintegratedicounts']
            print 'WARNING:There should not have been an existing icounts_asintegrated but it is being overwritten anyway'
        icountsasint=h5mar.create_dataset('asintegratedicounts', data=icountspoint[:, :])
        icountsasint.attrs['bcknd1daddition']=self.newadditionfrom1dbckndsubtraction
        for key, val in self.savedictbcknd1d.iteritems():
            if isinstance(val, list) and len(val)==0:
                continue
            icountsasint.attrs[key]=val
        for pointind in self.pointlist:
            icountspoint[pointind, :]+=self.newadditionfrom1dbckndsubtraction[:]
        if 'ibckndadd' in h5mar:
            del h5mar['ibckndadd']
        h5mar.create_dataset('ibckndadd', data=self.newadditionfrom1dbckndsubtraction)
        if 'ibminnew' in h5mar:
            del h5mar['ibminnew']
        if 'ibmin' in h5mar:
            h5mar.create_dataset('ibminnew', data=h5mar['ibmin'][:]-self.newadditionfrom1dbckndsubtraction[:])
        h5file.close()

    def revert1dbcknd(self):
        h5file=h5py.File(self.h5path, mode='r+')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        if 'asintegratedicounts' in h5mar:
            icountspoint=h5mar['icounts']
            asintegratedpoint=h5mar['asintegratedicounts']
            for pointind in self.pointlist:
                icountspoint[pointind, :]=asintegratedpoint[pointind, :]
            del h5mar['asintegratedicounts']
        h5file.close()

    def addpeak(self):
        self.additionalpeaks+=[[self.imnum, self.addpeakscaleSpinBox.value(), self.addpeakposnSpinBox.value()]]
        txt=''
        for peak in self.additionalpeaks:
            txt+='%d\t%.2f\t%.2f\n' %(int(round(peak[0])), peak[1], peak[2])
        self.addpeakTextBrowser.setPlainText(txt)

    def addpeakclear(self):
        h5file=h5py.File(self.h5path, mode='r+')
        if 'additionalpeaks' in h5file[self.h5datagrpstr]:
            del h5file[self.h5datagrpstr]['additionalpeaks']
        else:
            self.additionalpeaks=[]
        h5file.close()

    def addpeaksave(self):
        h5file=h5py.File(self.h5path, mode='r+')
        if 'additionalpeaks' in h5file[self.h5datagrpstr]:
            del h5file[self.h5datagrpstr]['additionalpeaks']
        else:
            grp=h5file[self.h5datagrpstr].create_dataset('additionalpeaks', data=numpy.float32(self.additionalpeaks))
            grp.attrs['usedinfitting']=0
        h5file.close()

    def removepeak(self):
        h5file=h5py.File(self.h5path, mode='r+')
        pkqvals=h5file[self.h5datagrpstr]['pkcounts'][self.imnum, 0, :]
        ind=myargmin((pkqvals-self.qvalueofpeakremoval)**2)
        print self.qvalueofpeakremoval
        print (pkqvals-self.qvalueofpeakremoval)**2
        print h5file[self.h5datagrpstr]['pkcounts'][self.imnum, 0, :]
        h5file[self.h5datagrpstr]['pkcounts'][self.imnum, :, ind]=numpy.float32([numpy.nan]*h5file[self.h5datagrpstr]['pkcounts'].shape[1])
        print  self.imnum, ind
        print h5file[self.h5datagrpstr]['pkcounts'][self.imnum, 0, :]

        h5file.close()
        self.peaksremoved.setValue(1+self.peaksremoved.value())

    def fillpeakComboBox(self):
        self.imname=unicode(self.imComboBox.currentText())
        if self.imname.startswith('if'):
            temp=self.imname[2:]
        else:
            temp=self.imname[1:]
        if temp.isdigit():
            self.imnum=eval(temp)

        self.peakComboBox.clear()

        h5file=h5py.File(self.h5path, mode='r')
        if 'pkcounts' in h5file[self.h5datagrpstr]:
            peaks, garb, heights=peakinfo_pksavearr(h5file[self.h5datagrpstr]['pkcounts'][self.imnum, :,:])
            for tup in zip(peaks, heights):
                self.peakComboBox.insertItem(999, '%.2f,%.0f' %tup)
        h5file.close()
        self.peakComboBox.insertItem(999, 'sum of all')

    def plotfitpeak(self):
        if not ('q' in unicode(self.xaxisComboBox.currentText()) or 'PHI' in unicode(self.xaxisComboBox.currentText())):
            print 'overlay fitted peaks only available for plotting vs q'
            return

        h5file=h5py.File(self.h5path, mode='r')
        q_pk, sig_pk, ht_pk=peakinfo_pksavearr(h5file[self.h5datagrpstr]['pkcounts'][self.imnum, :,:]) #this could be done more somply but this is safest
        peakfcn=eval(h5file[self.h5datagrpstr]['pkcounts'].attrs['peakshape'])
        h5file.close()

        if unicode(self.peakComboBox.currentText())=='sum of all':
            qvals=self.qvals
            gaussvals=numpy.zeros(qvals.size, dtype='float32')
            for q, sig, ht in zip(q_pk, sig_pk, ht_pk):
                gaussvals+=peakfcn([q, sig, ht], qvals)#ht*numpy.exp(-0.5*((qvals-q)/sig)**2)
        else:
            pkindex=self.peakComboBox.currentIndex()
            q_pk=q_pk[pkindex]
            sig_pk=sig_pk[pkindex]
            ht_pk=ht_pk[pkindex]
            qvals=self.qvals[(self.qvals>=q_pk-3.0*sig_pk)&(self.qvals<=q_pk+3.0*sig_pk)]
            gaussvals=peakfcn([q_pk, sig_pk, ht_pk], qvals)#ht_pk*numpy.exp(-1.0*((qvals-q_pk)/sig_pk)**2)
        self.plotw.axes.hold(True)
        #self.plotw.axes.plot(qvals, gaussvals, 'r--', linewidth=3)
        self.plotw.performplot([qvals, gaussvals], overlay=True)
        self.plotw.fig.canvas.draw()

    def save(self):
        self.plotw.save(os.path.join(self.runpath, ''.join((self.savename1, self.savename2))).replace('\\','/').encode())

    def savenavimage(self):
        self.navw.save(os.path.join(self.runpath, ''.join((self.savename1, '_IntPlotPoints', '%d' %self.savecount))).replace('\\','/').encode())
        self.savecount+=1

#class associationtree(QDialog,
#        ui_associationtree.Ui_associationtreeForm):
#
#    def __init__(self, parent, maingrp):
#        super(associationtree, self).__init__(parent)
#        self.setupUi(self)
#        dergrp=maingrp.Derived
#        pointlist=maingrp._f_getAttr('pointlist')
#        qgrid=dergrp.imap._f_getAttr('qgrid')
#        qgrid_qq=dergrp.qq._f_getAttr('qgrid')
#        numstrlist=['%03d' %num for num in pointlist]
#
#        qqpkspoint=dergrp.qqpks
#        qqpks=numpy.empty(qqpkspoint.shape, dtype=numpy.uint16)
#        qqpks[:, :]=qqpkspoint[:, :]
#
#        kindsets_innn_qqind=[[set([]) for temp in range(len(pointlist))] for temp2 in range(qqpks.shape[0])]
#        pointcount=-1
#        for numstr in numstrlist:
#            pointcount+=1
##for this routine keep h5file open in read only the whole time so just use the pointers
#            atabnnn=eval(''.join(('dergrp.atab', numstr)))
#            annn=eval(''.join(('dergrp.a', numstr)))
#            knnn=eval(''.join(('dergrp.k', numstr)))
#
##            annnpoint=eval(''.join(('dergrp.a', numstr)))
##            annn=numpy.empty(annnpoint.shape, dtype=numpy.int32)
##            annn[:, :]=annnpoint[:, :]
##
##            knnnpoint=eval(''.join(('dergrp.k', numstr)))
##            knnn=numpy.empty(knnnpoint.shape, dtype=numpy.float32)
##            knnn[:]=knnnpoint[:]
#
#            kindsets_qqind=kindsets_qqind_atab(atabnnn, qqpks.shape[0])
#            qqindsets_kind, unassoc=readannn(annn)
#            mainitemA=QTreeWidgetItem([numstr], 0)
#            mainitemB=QTreeWidgetItem([numstr], 0)
#            self.treeAWidget.addTopLevelItem(mainitemA)
#            self.treeBWidget.addTopLevelItem(mainitemB)
#            count=-1
#            for s in qqindsets_kind:
#                count+=1
#                if len(s)>0:
#                    item=QTreeWidgetItem(['k%d(%.2f)' %(count, q_qgrid_ind(qgrid, knnn[count]))],  0)
#                    mainitemA.addChild(item)
#                    for qqind in s:
#                        subitem=QTreeWidgetItem(['qq%d(%.2f,%.2f)' %(qqind, q_qgrid_ind(qgrid_qq, qqpks[qqind, 0]), q_qgrid_ind(qgrid_qq, qqpks[qqind, 1]))],  0)
#                        item.addChild(subitem)
#            for kind in unassoc:
#                item=QTreeWidgetItem(['k%d(%.2f)' %(kind, q_qgrid_ind(qgrid, knnn[kind]))],  0)
#                mainitemA.addChild(item)
#            count=-1
#            for s in kindsets_qqind:
#                count+=1
#                if len(s)>0:
#                    item=QTreeWidgetItem(['qq%d(%.2f,%.2f)' %(count, q_qgrid_ind(qgrid_qq, qqpks[count, 0]), q_qgrid_ind(qgrid_qq, qqpks[count, 1]))],  0)
#                    mainitemA.addChild(item)
#                    for kind in s:
#                        subitem=QTreeWidgetItem(['k%d(%.2f)' %(kind, q_qgrid_ind(qgrid, knnn[kind]))],  0)
#                        item.addChild(subitem)
#                    kindsets_innn_qqind[count][pointcount]|=s
#        count_qq=-1
#        for list_point in kindsets_innn_qqind:
#            count_qq+=1
#            mainitemC=QTreeWidgetItem(['qq%d(%.2f,%.2f)' %(count_qq, q_qgrid_ind(qgrid_qq, qqpks[count_qq, 0]), q_qgrid_ind(qgrid_qq, qqpks[count_qq, 1]))], 0)
#            self.treeCWidget.addTopLevelItem(mainitemC)
#            count_point=-1
#            for s in list_point:
#                count_point+=1
#                if len(s)>0:
#                    item=QTreeWidgetItem([numstrlist[count_point]],  0)
#                    knnn=eval(''.join(('dergrp.k', numstrlist[count_point])))
#                    mainitemC.addChild(item)
#                    for kind in s:
#                        subitem=QTreeWidgetItem(['k%d(%.2f)' %(kind, q_qgrid_ind(qgrid, knnn[kind]))],  0)
#                        item.addChild(subitem)

class plotqqwindow(QDialog):
    def __init__(self, parent, h5path, h5groupstr, runpath, navchoice, displaytrees=False):
        super(plotqqwindow, self).__init__(parent)
        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.runpath=runpath
        self.navchoice=navchoice
        self.savename1='_'.join((os.path.split(self.h5path)[1][0:-3], self.h5groupstr, ''))
        self.imnamelist=[]

        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        if not ('qq' in h5mar):
            QMessageBox.warning(self,"failed",  'aborted qqplot because cannot find qq')
            h5file.close()
            return
        self.qq=readh5pyarray(h5mar['qq'])
        self.qgrid_qq=h5mar['qq'].attrs['qgrid']

        attrdict=getattr(self.h5path, self.h5groupstr)

        self.pointlist=h5analysis.attrs['pointlist']

        self.qgrid=h5mar['icounts'].attrs['qgrid']
        self.qvals=q_qgrid_ind(self.qgrid)

        self.imnamelist=[]
        if 'qqcounts' in h5mar:#this shouldn't be necessary
            self.imnamelist+=['%d' %p for p in self.pointlist]

        #commenting on April 2009 becvause do not have atab stuff figured out yet
#        testlist=['qq','qqpktab']
#        testlist+=['a%03d' %picnum for picnum in self.pointlist]
#        testlist+=['atab%03d' %picnum for picnum in self.pointlist]
#        testlist+=['k%03d' %picnum for picnum in self.pointlist]
#        boollist=[not st in nodenames for st in testlist]
#        treewidgetbool=numpy.sum(boollist)==0

        treewidgetbool=False

        self.qqnormexists='qqnorm' in h5mar
        self.qqanlzdexists='qqpktab' in h5mar

        h5file.close()


        self.setWindowTitle('Plot scattering vector correlation (qq)')

        self.savenavimageButton=QPushButton()
        self.savenavimageButton.setText('save .png\nnavigator')
        QObject.connect(self.savenavimageButton,SIGNAL("pressed()"),self.savenavimage)

        self.xgrid=attrdict['xgrid']
        self.zgrid=attrdict['zgrid']
        self.xcoords=attrdict['x']
        self.zcoords=attrdict['z']


        if self.navchoice==0:
            self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
        else:
            elstr=attrdict['elements']

            if self.navchoice==1:
                infotype='DPmolfracALL'
            else:
                infotype='XRFmolfracALL'
            self.elstrlist, self.compsarr=getternarycomps(self.h5path, self.h5groupstr, elstr=elstr, infotype=infotype)
            if self.compsarr is None:
                print 'NO COMPOSITION NAVIGATOR WINDOW BECAUSE PROBLEM CALCULATING COMPOSITIONS'
                self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
            else:
                print 'COMPS:', self.compsarr
                self.navw = compnavigatorwidget(self, self.compsarr, self.elstrlist)
        QObject.connect(self.navw, SIGNAL("picclicked"), self.picclickprocess)

        self.logCheckBox=QCheckBox()
        self.logCheckBox.setText('logarithmic\nintensity')
        self.logCheckBox.setChecked(False)

        self.imComboBox=QComboBox()

        self.drawButton=QPushButton()
        self.drawButton.setText('draw image')
        QObject.connect(self.drawButton,SIGNAL("pressed()"),self.draw)
        self.saveButton=QPushButton()
        self.saveButton.setText('save .png')
        QObject.connect(self.saveButton,SIGNAL("pressed()"),self.save)
        toplayout=QHBoxLayout()
        toplayout.addWidget(self.savenavimageButton)
        toplayout.addWidget(self.logCheckBox)
        toplayout.addWidget(self.imComboBox)
        toplayout.addWidget(self.drawButton)
        toplayout.addWidget(self.saveButton)
        layout=QVBoxLayout()
        #leftlayout=QVBoxLayout()
        rightlayout=QVBoxLayout()
        #lefttoplayout=QGridLayout()
        plotlayout=QHBoxLayout()

        self.imgLabel=QLabel()

        self.plotw = plotwidget(self, width=5, height=5, dpi=100)

        rightlayout.addWidget(self.imgLabel)

        rightlayout.addWidget(self.plotw)

        plotlayout.addWidget(self.navw)

        plotlayout.addLayout(rightlayout)

        layout.addLayout(toplayout)
        layout.addLayout(plotlayout)

        if displaytrees and treewidgetbool:
            superlayout=QHBoxLayout()
            superlayout.addLayout(layout)

            treelabelsLayout=QHBoxLayout()
            for msg in ['1d spectrum->instanced qq peak->associated 1d peaks', '1d spectrum->1d peak->associated qq peaks', 'qq peaks->1d spectrum containing peak->1d peaks']:
                aLabel=QLabel()
                aLabel.setText(msg)
                treelabelsLayout.addWidget(aLabel)


            treeLayout=QHBoxLayout()
            self.treeAWidget=QTreeWidget()
            self.treeBWidget=QTreeWidget()
            self.treeCWidget=QTreeWidget()
            treeLayout.addWidget(self.treeAWidget)
            treeLayout.addWidget(self.treeBWidget)
            treeLayout.addWidget(self.treeCWidget)

            treebuttonLayout=QHBoxLayout()
            treeAbutton=QPushButton()
            treeAbutton.setText('plot selection\n(select either type of peak)')
            QObject.connect(treeAbutton,SIGNAL("pressed()"),self.drawtreeA)
            treeBbutton=QPushButton()
            treeBbutton.setText('plot selection\n(select either type of peak)')
            QObject.connect(treeBbutton,SIGNAL("pressed()"),self.drawtreeB)
            treeCbutton=QPushButton()
            treeCbutton.setText('plot selection\n(select either type of peak)')
            QObject.connect(treeCbutton,SIGNAL("pressed()"),self.drawtreeC)
            treebuttonLayout.addWidget(treeAbutton)
            treebuttonLayout.addWidget(treeBbutton)
            treebuttonLayout.addWidget(treeCbutton)

            fulltreeLayout=QVBoxLayout()
            fulltreeLayout.addLayout(treelabelsLayout)
            fulltreeLayout.addLayout(treeLayout)
            fulltreeLayout.addLayout(treebuttonLayout)

            superlayout.addLayout(fulltreeLayout)
            #superlayout.addWidget(associationtree(self, grp))

            #h5file=tables.openFile(self.h5path, mode='r')
            grp=eval(self.fullgrpstr)
            self.fillintrees(grp)
            h5file.close()

            self.setLayout(superlayout)
        else:
            self.setLayout(layout)

        self.fillimComboBox()

        self.imname=unicode(self.imComboBox.currentText())
        if self.imname=='qq':
            self.imnum=999
        elif self.imname=='qqnorm':
            self.imnum=998
        elif self.imname=='qqanlzd':
            self.imnum=997
        else:
            self.imnum=eval(self.imname)

        self.navw.plotpoints(self.pointlist, [])
        self.navw.fig.canvas.draw()

    def fillintrees(self, maingrp):#April 2009 this doesn't work becauseqqpktab and other stuff not worked out yet

        qqpkinds=numpy.uint16([[arow['qqindhigh'], arow['qqindlow']] for arow in dergrp.qqpktab])

        kindsets_innn_qqind=[[set([]) for temp in range(len(self.pointlist))] for temp2 in range(qqpkinds.shape[0])]
        pointcount=-1
        for numstr in numstrlist:
            pointcount+=1
#for this routine keep h5file open in read only the whole time so just use the pointers
            atabnnn=eval(''.join(('dergrp.atab', numstr)))
            annn=eval(''.join(('dergrp.a', numstr)))
            knnn=eval(''.join(('dergrp.k', numstr)))

#            annnpoint=eval(''.join(('dergrp.a', numstr)))
#            annn=numpy.empty(annnpoint.shape, dtype=numpy.int32)
#            annn[:, :]=annnpoint[:, :]
#
#            knnnpoint=eval(''.join(('dergrp.k', numstr)))
#            knnn=numpy.empty(knnnpoint.shape, dtype=numpy.float32)
#            knnn[:]=knnnpoint[:]

            kindsets_qqind=kindsets_qqind_atab(atabnnn, qqpkinds.shape[0])
            qqindsets_kind, unassoc=readannn(annn)
            mainitemA=QTreeWidgetItem([numstr], 0)
            mainitemB=QTreeWidgetItem([numstr], 0)
            self.treeAWidget.addTopLevelItem(mainitemA)
            self.treeBWidget.addTopLevelItem(mainitemB)
            for count,  s in enumerate(qqindsets_kind):
                if len(s)>0:
                    item=QTreeWidgetItem(['k%d(%.2f)' %(count, q_qgrid_ind(self.qgrid, knnn[count]))],  0)
                    mainitemA.addChild(item)
                    for qqind in s:
                        subitem=QTreeWidgetItem(['qq%d(%.2f,%.2f)' %(qqind, q_qgrid_ind(self.qgrid_qq, qqpkinds[qqind, 0]), q_qgrid_ind(self.qgrid_qq, qqpkinds[qqind, 1]))],  0)
                        item.addChild(subitem)
            for kind in unassoc:
                item=QTreeWidgetItem(['k%d(%.2f)' %(kind, q_qgrid_ind(self.qgrid, knnn[kind]))],  0)
                mainitemA.addChild(item)
            for count, s in enumerate(kindsets_qqind):
                if len(s)>0:
                    item=QTreeWidgetItem(['qq%d(%.2f,%.2f)' %(count, q_qgrid_ind(self.qgrid_qq, qqpkinds[count, 0]), q_qgrid_ind(self.qgrid_qq, qqpkinds[count, 1]))],  0)
                    mainitemB.addChild(item)
                    for kind in s:
                        subitem=QTreeWidgetItem(['k%d(%.2f)' %(kind, q_qgrid_ind(self.qgrid, knnn[kind]))],  0)
                        item.addChild(subitem)
                    kindsets_innn_qqind[count][pointcount]|=s
        for count_qq, list_point in enumerate(kindsets_innn_qqind):
            mainitemC=QTreeWidgetItem(['qq%d(%.2f,%.2f)' %(count_qq, q_qgrid_ind(self.qgrid_qq, qqpkinds[count_qq, 0]), q_qgrid_ind(self.qgrid_qq, qqpkinds[count_qq, 1]))], 0)
            self.treeCWidget.addTopLevelItem(mainitemC)
            count_point=-1
            for s in list_point:
                count_point+=1
                if len(s)>0:
                    item=QTreeWidgetItem([numstrlist[count_point]],  0)
                    knnn=eval(''.join(('dergrp.k', numstrlist[count_point])))
                    mainitemC.addChild(item)
                    for kind in s:
                        subitem=QTreeWidgetItem(['k%d(%.2f)' %(kind, q_qgrid_ind(self.qgrid, knnn[kind]))],  0)
                        item.addChild(subitem)


    def fillimComboBox(self):
        self.imComboBox.clear()
        if len(self.imnamelist)>0:
            for name in self.imnamelist:
                self.imComboBox.insertItem(999, name[2:])
        else:
            self.imComboBox.insertItem(0, 'err')

        self.imComboBox.insertItem(999,  'qq')
        if self.qqnormexists:
            self.imComboBox.insertItem(999,  'qqnorm')
            if self.qqanlzdexists:
                self.imComboBox.insertItem(999,  'qqanlzd')


    def drawtreeA(self):
        temp=self.treeAWidget.selectedItems()
        if len(temp)>0:
            item=temp[0]
            if unicode(item.text(0)).startswith('qq'):
                qqlist=[eval(''.join(('[', unicode(item.text(0)).partition('(')[2].partition(')')[0], ']')))]
                klist=[eval(unicode(item.parent().text(0)).partition('(')[2].partition(')')[0])]
            elif unicode(item.text(0)).startswith('k'):
                klist=[eval(unicode(item.text(0)).partition('(')[2].partition(')')[0])]
                qqlist=[]
                for chnum in range(item.childCount()):
                    qqlist+=[eval(''.join(('[', unicode(item.child(chnum).text(0)).partition('(')[2].partition(')')[0], ']')))]
            self.drawfromtree(klist, qqlist)

    def drawtreeB(self):
        temp=self.treeBWidget.selectedItems()
        if len(temp)>0:
            item=temp[0]
            if unicode(item.text(0)).startswith('k'):
                klist=[eval(unicode(item.text(0)).partition('(')[2].partition(')')[0])]
                qqlist=[eval(''.join(('[', unicode(item.parent().text(0)).partition('(')[2].partition(')')[0], ']')))]
            elif unicode(item.text(0)).startswith('qq'):
                qqlist=[eval(''.join(('[', unicode(item.text(0)).partition('(')[2].partition(')')[0], ']')))]
                klist=[]
                for chnum in range(item.childCount()):
                    klist+=[eval(unicode(item.child(chnum).text(0)).partition('(')[2].partition(')')[0])]
            self.drawfromtree(klist, qqlist)

    def drawtreeC(self):
        temp=self.treeCWidget.selectedItems()
        if len(temp)>0:
            item=temp[0]
            if unicode(item.text(0)).startswith('k'):
                klist=[eval(unicode(item.text(0)).partition('(')[2].partition(')')[0])]
                qqlist=[]
            elif unicode(item.text(0)).startswith('qq'):
                qqlist=[eval(''.join(('[', unicode(item.text(0)).partition('(')[2].partition(')')[0], ']')))]
                klist=[]
            self.drawfromtree(klist, qqlist)

    def drawfromtree(self, klist, qqlist):
        if len(klist)==0:
            redindarr=None
        else:
            redindarr=ind_qgrid_q(self.qgrid_qq, numpy.array(klist))
        if len(qqlist)==0:
            blueind2darr=None
        else:
            blueind2darr=ind_qgrid_q(self.qgrid_qq, numpy.array(qqlist))
        self.plotw.performqqtreeplot(self.qq.T, redindarr, blueind2darr, self.qvals)
        self.savename2=''.join(('_qqAssociations'))
        self.navw.plotpoints(self.pointlist, [])
        self.plotw.fig.canvas.draw()
        self.navw.fig.canvas.draw()
        self.imgLabel.setText(self.savename2)

    def draw(self):
        self.imname=unicode(self.imComboBox.currentText())
        if self.imname=='qq':
            self.imnum=999
            self.imname=''
            select=[]
        elif self.imname=='qqnorm':
            self.imnum=998
            self.imname='norm'
            select=[]
        elif self.imname=='qqanlzd':
            self.imnum=997
            self.imname='anlzd'
            select=[]
        else:
            self.imnum=eval(self.imname)
            select=[self.imnum]
        if self.imnum==997:#April 2009 this doesn't work becauseqqpktab and other stuff not worked out yet
            #h5file=tables.openFile(self.h5path, mode='r')
            dergrp=eval(self.fulldergrpstr)
            plotarrtup=makeqqnormpeakplotimage(self.qq, qqpktuplist_h5qqpktab(dergrp.qqpktab))
            h5file.close()
            temp=numpy.empty(plotarrtup[0].shape)
            for i in [0, 1, 2]:
                temp[:, :, i]=plotarrtup[0][:, :, i].T
            self.plotw.performqqnormpeakplot(temp, qvals=self.qvals)
        elif self.imnum==999:
            self.plotw.performplot(self.qq.T, upperorigin=False, axesformat='qq', qvals=self.qvals)
        else:
            h5file=h5py.File(self.h5path, mode='r')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            plotarr=h5mar['qqcounts'][self.imnum, :, :]
            h5file.close()
            self.plotw.performplot(plotarr.T, upperorigin=False, axesformat='qq', qvals=self.qvals)
        self.savename2=''.join(('_qq', self.imname))
        self.navw.plotpoints(self.pointlist, [], select=select)
        self.plotw.fig.canvas.draw()
        self.navw.fig.canvas.draw()
        self.imgLabel.setText(self.savename2)

    def picclickprocess(self, picnum):
        picname='%d' %picnum
        if picname in self.imnamelist:
            for i in range(len(self.imnamelist)):
                if self.imnamelist[i]==picname:
                    self.imComboBox.setCurrentIndex(i)
                    break

        self.draw()

    def save(self):
        self.plotw.save(os.path.join(self.runpath, ''.join((self.savename1, self.savename2))).replace('\\','/').encode())

    def savenavimage(self):
        self.navw.save(os.path.join(self.runpath, ''.join((self.savename1, '_qqpoint'))).replace('\\','/').encode())

class plotdatwindow(QDialog):
    def __init__(self, parent, runpath):
        super(plotdatwindow, self).__init__(parent)
        self.runpath=runpath

        self.setWindowTitle('Plot images from binary files')

        self.logCheckBox=QCheckBox()
        self.logCheckBox.setText('logarithmic\nintensity')
        self.logCheckBox.setChecked(False)

        self.drawButton=QPushButton()
        self.drawButton.setText('select and draw image')
        QObject.connect(self.drawButton,SIGNAL("pressed()"),self.draw)
        self.saveButton=QPushButton()
        self.saveButton.setText('save .png')
        QObject.connect(self.saveButton,SIGNAL("pressed()"),self.save)
        toplayout=QHBoxLayout()
        toplayout.addWidget(self.logCheckBox)
        toplayout.addWidget(self.drawButton)
        toplayout.addWidget(self.saveButton)
        #layout=QVBoxLayout()
        #leftlayout=QVBoxLayout()
        rightlayout=QVBoxLayout()
        #lefttoplayout=QGridLayout()

        self.imgLabel=QLabel()

        self.plotw = plotwidget(self, width=5, height=5, dpi=100)

        rightlayout.addLayout(toplayout)
        rightlayout.addWidget(self.imgLabel)

        rightlayout.addWidget(self.plotw)

        self.setLayout(rightlayout)
        self.datpath=self.runpath

    def draw(self):
        temp = mygetopenfile(self, xpath=self.datpath,markstr='XRD binary image')
        if temp!='':
            self.datpath=temp
            self.savename=os.path.splitext(os.path.split(self.datpath)[1])[0]
            data = numpy.fromfile(self.datpath, dtype='uint16') #TODO: make the data type less constrictive
            data.shape = (numpy.sqrt(len(data)), numpy.sqrt(len(data)))
            self.plotw.performplot(data,  log=self.logCheckBox.isChecked())
            self.plotw.fig.canvas.draw()
            self.imgLabel.setText(self.savename)

    def save(self):
        self.plotw.save(os.path.join(self.runpath, ''.join((self.savename,  '.png'))).replace('\\','/').encode())

class plothistwindow(QDialog):
    def __init__(self, parent, h5path, h5groupstr, runpath, navchoice):
        super(plothistwindow, self).__init__(parent)
        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.runpath=runpath
        self.navchoice=navchoice
        self.savename1='_'.join((os.path.split(self.h5path)[1][0:-3], self.h5groupstr, ''))
        self.imnamelist=[]

        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        h5marcounts=h5file['/'.join((self.h5groupstr,'measurement/'+getxrdname(h5analysis)+'/counts'))]

        self.bin=getbin(h5analysis)
        
        self.attrdict=getattr(self.h5path, self.h5groupstr)

        self.pointlist=h5analysis.attrs['pointlist']

        self.qgrid=h5mar['icounts'].attrs['qgrid']
        self.qvals=q_qgrid_ind(self.qgrid)


        self.imnamelist=[]

        for group in h5mar:
            if isinstance(group, h5py.Group):
                gname=group.name.rpartition('/')[2]
        for node in h5mar.iterobjects():
            if isinstance(node, h5py.Dataset):
                if len(node.shape)==2 and node.shape[0]==h5marcounts.shape[0]:
                    self.imnamelist+= [node.name.rpartition('/')[2]]
                elif len(node.shape)==3 and node.shape[0]==h5marcounts.shape: #this isn't exclusive enough but oh well
                    self.imnamelist+=[node.name.rpartition('/')[2]+'_%d' %p for p in self.pointlist]
        self.imnamelist+=['raw-%d' %p for p in self.pointlist]

        self.killmap=getkillmap(h5analysis.attrs['killmapstr'])
        self.killmapbin=getkillmap(h5analysis.attrs['killmapstr'], bin=self.bin)

#for display killmap also takes out pixels not in imap - for editing killmap, don't involve imap
        self.imap, self.qgrid=getimapqgrid(h5analysis.attrs['imapstr'])
        self.imapbin=getimapqgrid(h5analysis.attrs['imapstr'], qgrid=False, bin=self.bin)

        self.killmap*=(self.imap!=0)
        self.killmapbin*=(self.imapbin!=0)


        self.bcknd=self.attrdict['bcknd']
        bstr=''.join(('b', self.bcknd[:3]))
        self.bckndarr=readh5pyarray(h5mar[bstr])
        bstr=''.join((bstr, 'bin%d' %self.bin))
        self.bckndarrbin=readh5pyarray(h5mar[bstr])
        if self.bcknd=='minanom':
            if 'bimap' in h5mar:
                bimap=readh5pyarray(h5mar['bimap'])
                bqgrid=h5mar['bimap'].attrs['bqgrid']
            else:
                bimap=None
                bqgrid=None
            self.banomcalc=(self.imapbin, self.qgrid, self.attrdict, bimap, bqgrid)
            self.bminanomf=readh5pyarray(h5mar['bminanomf'])


        h5file.close()

        self.imnamelist.sort()

        self.killCheckBox=QCheckBox()
        self.killCheckBox.setText('apply kill map\nin main image')
        self.killCheckBox.setChecked(True)

        self.bckndCheckBox=QCheckBox()
        self.bckndCheckBox.setText('subtract background')
        self.bckndCheckBox.setChecked(True)


        self.setWindowTitle('Plot histogram of single pixel counts')

        self.fromdatButton=QPushButton()
        self.fromdatButton.setText('select .dat\nbinary file')
        QObject.connect(self.fromdatButton,SIGNAL("pressed()"),self.fromdat)

        self.savenavimageButton=QPushButton()
        self.savenavimageButton.setText('save .png\nnavigator')
        QObject.connect(self.savenavimageButton,SIGNAL("pressed()"),self.savenavimage)

        self.xgrid=self.attrdict['xgrid']
        self.zgrid=self.attrdict['zgrid']
        self.xcoords=self.attrdict['x']
        self.zcoords=self.attrdict['z']

        if self.navchoice==0:
            self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
        else:
            elstr=self.attrdict['elements']

            if self.navchoice==1:
                infotype='DPmolfracALL'
            else:
                infotype='XRFmolfracALL'
            self.elstrlist, self.compsarr=getternarycomps(self.h5path, self.h5groupstr, elstr=elstr, infotype=infotype)
            if self.compsarr is None:
                print 'NO COMPOSITION NAVIGATOR WINDOW BECAUSE PROBLEM CALCULATING COMPOSITIONS'
                self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
            else:
                print 'COMPS:', self.compsarr
                self.navw = compnavigatorwidget(self, self.compsarr, self.elstrlist)
        QObject.connect(self.navw, SIGNAL("picclicked"), self.picclickprocess)

        self.savetxtButton=QPushButton()
        self.savetxtButton.setText('save selected\nimage as ASCII')
        QObject.connect(self.savetxtButton,SIGNAL("pressed()"),self.savetxt)

        self.overlayCheckBox=QCheckBox()
        self.overlayCheckBox.setText('overlay on\nexisting plots')
        self.overlayCheckBox.setChecked(False)

        self.imComboBox=QComboBox()

        self.drawButton=QPushButton()
        self.drawButton.setText('draw image')
        QObject.connect(self.drawButton,SIGNAL("pressed()"),self.draw)
        self.saveButton=QPushButton()
        self.saveButton.setText('save .png')
        QObject.connect(self.saveButton,SIGNAL("pressed()"),self.save)
        toplayout=QHBoxLayout()
        toplayout.addWidget(self.fromdatButton)
        toplayout.addWidget(self.killCheckBox)
        toplayout.addWidget(self.bckndCheckBox)
        toplayout.addWidget(self.savenavimageButton)
        toplayout.addWidget(self.overlayCheckBox)
        toplayout.addWidget(self.imComboBox)
        toplayout.addWidget(self.drawButton)
        toplayout.addWidget(self.saveButton)
        toplayout.addWidget(self.savetxtButton)
        layout=QVBoxLayout()
        leftlayout=QVBoxLayout()
        rightlayout=QVBoxLayout()
        lefttoplayout=QGridLayout()
        plotlayout=QHBoxLayout()

        self.startSpinBox=QSpinBox()
        self.startSpinBox.setValue(0)
        self.startSpinBox.setRange(0,10000000 )

        self.intSpinBox=QSpinBox()
        self.intSpinBox.setValue(0)
        self.intSpinBox.setRange(0,10000000 )

        self.numSpinBox=QSpinBox()
        self.numSpinBox.setValue(1000)
        self.numSpinBox.setRange(0,10000000 )

        self.imgLabel=QLabel()

        self.plotw = plotwidget(self, width=5, height=5, dpi=100)

        lab1=QLabel()
        lab2=QLabel()
        lab3=QLabel()
        lab1.setText('lowest counts')
        lab2.setText('width of counts bins\nzero->auto')
        lab3.setText('number of bins')
        lefttoplayout.addWidget(lab1, 0, 0)
        lefttoplayout.addWidget(lab2, 0, 1)
        lefttoplayout.addWidget(lab3, 0, 2)
        lefttoplayout.addWidget(self.startSpinBox, 1, 0)
        lefttoplayout.addWidget(self.intSpinBox, 1, 1)
        lefttoplayout.addWidget(self.numSpinBox, 1, 2)


        leftlayout.addLayout(lefttoplayout)
        rightlayout.addWidget(self.imgLabel)

        leftlayout.addWidget(self.navw)
        rightlayout.addWidget(self.plotw)
        plotlayout.addLayout(leftlayout)
        plotlayout.addLayout(rightlayout)

        layout.addLayout(toplayout)
        layout.addLayout(plotlayout)

        self.setLayout(layout)
        self.fillimComboBox()

        self.savecount=0
        self.selectlist=[]

        #self.imnum=0
        self.imname=unicode(self.imComboBox.currentText())


        self.navw.plotpoints(self.pointlist, [])

        self.killbool=False
        self.bckndbool=False
        self.binbool=False
        self.dat=False

        self.datpath=self.runpath
        
        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5chess=CHESSRUNFILE()
        self.circkillmap=readh5pyarray(h5chess[getxrdname(h5analysis)+'killmap'])
        self.circkillmapbin=readh5pyarray(h5chess[getxrdname(h5analysis)+'killmapbin%d' %self.bin])
        h5chess.close()
        h5file.close()



    def fillimComboBox(self):
        self.imComboBox.clear()
        if len(self.imnamelist)>0:
            for name in self.imnamelist:
                self.imComboBox.insertItem(999, name)
        else:
            self.imComboBox.insertItem(0, 'err')
        self.imComboBox.setCurrentIndex(0)

    def draw(self):
        self.imname=unicode(self.imComboBox.currentText())
        self.dat=False

        h5file=h5py.File(self.h5path, mode='r+')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        h5marcounts=h5file['/'.join((self.h5groupstr,'measurement', getxrdname(h5analysis), 'counts'))]

        if '-' in self.imname:
            imtype, garb, imnum=self.imname.partition('-')
            if imtype=='raw':
                plotarr=h5marcounts[imnum, :, :]
            else:
                plotarr=h5mar[imtype][imnum, :, :]
        else:
            imtype=None
            plotarr=readh5pyarray(h5mar[self.imname])
        h5file.close()

        if not self.overlayCheckBox.isChecked():
            self.selectlist=[]
            self.selectlistnav=[]
        self.selectlist+=[self.imname]
        if len(self.selectlist)==1:
            self.savename2=''.join(('_hist', '_', self.imname))
        else:
            self.savename2=''.join((self.savename2,'_', self.imname))
        temp=self.imname[1:]

        self.killbool=False
        self.bckndbool=False
        self.binbool=False

        diffracbool=not (imtype is None)
        if diffracbool:
            self.selectlistnav+=[imnum]
            self.navw.plotpoints(self.pointlist, [], select=self.selectlistnav)
            self.killbool=self.killCheckBox.isChecked()
            self.bckndbool=self.bckndCheckBox.isChecked()
            self.binbool='bin' in imtype
        else:
            if not self.overlayCheckBox.isChecked():
                self.navw.plotpoints(self.pointlist, [],  select=[])
            self.killbool=self.killCheckBox.isChecked()

        totpix=None
        if diffracbool:
            if self.bckndbool:
                if self.binbool:
                    if self.bckndarrbin is None:
                        QMessageBox.warning(self,"failed",  "binned background not found")
                    else:
                        if self.bcknd=='minanom':
                            if self.bminanomf[imnum, 0]<0:
                                QMessageBox.warning(self,"failed",  "minanom background not available and will not be calculated with binning\n try again without binning but it will take while")
                            else:
                                h5file=h5py.File(self.h5path, mode='r')
                                h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
                                banom=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'banom'))][self.imnum, :, :]
                                h5file.close()
                                plotarr=bckndsubtract(plotarr, self.bckndarrbin, self.killmapbin, btype=self.bcknd, banom_f_f=(banom, self.bminanomf[imnum, 0], self.bminanomf[imnum, 1]))[0]
                        elif 'lin' in self.bcknd:
                            plotarr=bckndsubtract(plotarr, self.bckndarrbin, self.killmapbin, btype=self.bcknd, linweights=self.blinwts[imnum])[0]
                        else:
                            plotarr=bckndsubtract(plotarr, self.bckndarrbin, self.killmapbin, btype=self.bcknd)[0]
                        totpix=self.killmapbin.sum()
                else:
                    if self.bckndarr is None:
                        QMessageBox.warning(self,"failed",  "background not found")
                    else:
                        if self.bcknd=='minanom':
                            if self.bminanomf[imnum, 0]<0:
                                print 'WARNING: calculating bminanom background (for histogram analysis) on the fly: INEFFICIENT'
                                temp=bckndsubtract(plotarr, self.bckndarr, self.killmap, btype=self.bcknd, banomcalc=self.banomcalc)
                                plotarr=temp[0]
                            else:
                                h5file=h5py.File(self.h5path, mode='r')
                                h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
                                banom=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'banom'))][self.imnum, :, :]
                                h5file.close()
                                plotarr=bckndsubtract(plotarr, self.bckndarr, self.killmap, btype=self.bcknd, banom_f_f=(banom, self.bminanomf[imnum, 0], self.bminanomf[imnum, 1]))[0]
                        elif 'lin' in self.bcknd:
                            plotarr=bckndsubtract(plotarr, self.bckndarr, self.killmap, btype=self.bcknd, linweights=self.blinwts[imnum])[0]
                        else:
                            plotarr=bckndsubtract(plotarr, self.bckndarr, self.killmap, btype=self.bcknd)[0]
                        totpix=self.killmap.sum()
            elif self.killbool:
                if self.binbool:
                    plotarr*=self.killmapbin
                    totpix=self.killmapbin.sum()
                else:
                    plotarr*=self.killmap
                    totpix=self.killmap.sum()
        else:#bcknd image or killmap or something
            if self.killbool:
                if plotarr.shape[0]==self.killmap.shape[0]:
                    plotarr*=self.killmap
                    totpix=self.killmap.sum()
                elif plotarr.shape[0]==self.killmapbin.shape[0]:
                    plotarr*=self.killmapbin
                    totpix=self.killmapbin.sum()
                else:
                    QMessageBox.warning(self,"failed",  "killmap selected but neither killmap nor \n binned killmap are correct size")

        self.createhist(plotarr, totpix=totpix)
        self.navw.fig.canvas.draw()
        self.imgLabel.setText(''.join((self.savename2, ': ', self.histstr)))

    def savetxt(self):
        self.imname=unicode(self.imComboBox.currentText())
        if self.dat:
            name=''.join((self.datsavename, '_hist'))
        else:
            name=''.join((self.savename1, self.savename2))
        header=''.join(('!histogram of counts. center values of bins and frequency given below. ', self.histstr))
        writenumtotxtfile(self.runpath, self.vals, self.counts, name,  header=header)

    def picclickprocess(self, picnum):
        picname='raw-%d' %picnum
        if picname in self.imnamelist:
            for i in range(len(self.imnamelist)):
                if self.imnamelist[i]==picname:
                    self.imComboBox.setCurrentIndex(i)
                    break
        self.draw()

    def save(self):
        if self.dat:
            self.plotw.save(os.path.join(self.runpath, ''.join((self.datsavename, '_hist'))).replace('\\','/').encode())
        else:
            self.plotw.save(os.path.join(self.runpath, ''.join((self.savename1, self.savename2))).replace('\\','/').encode())

    def savenavimage(self):
        if self.dat:
            self.navw.save(os.path.join(self.runpath, ''.join((self.datsavename, '_HistPlotPoints', '%d' %self.savecount))).replace('\\','/').encode())
        else:
            self.navw.save(os.path.join(self.runpath, ''.join((self.savename1, '_HistPlotPoints', '%d' %self.savecount))).replace('\\','/').encode())
        self.savecount+=1

    def fromdat(self):
        temp = mygetopenfile(self, xpath=self.datpath,markstr='XRD binary image')
        if temp!='':
            self.datpath=temp
            self.datsavename=os.path.splitext(os.path.split(self.datpath)[1])[0]
            data = numpy.fromfile(self.datpath, dtype='uint16')
            data.shape = (numpy.sqrt(len(data)), numpy.sqrt(len(data)))
            self.dat=True
            self.createhist(data)

    def createhist(self, data, totpix=None):
        #if already applying a killmap, send the total # of pixels used. if not, then will apply the default ciruclar killmap
        a=self.startSpinBox.value()
        b=self.intSpinBox.value()
        c=self.numSpinBox.value()
        if totpix is None:
            if self.circkillmap.shape==data.shape:
                kdata=data*self.circkillmap
                totpix=self.circkillmap.sum()
            elif self.circkillmapbin.shape==data.shape:
                kdata=data*self.circkillmapbin
                totpix=self.circkillmapbin.sum()
            else:
                self.circkillmapbin=binboolimage(self.circkillmap, bin=data.shape[0]/self.circkillmap[0])
                kdata=data*self.circkillmapbin
                totpix=self.circkillmapbin.sum()
        else:
            kdata=data
        if b==0:
            b=(kdata.max()-a)/(1.0*c)
        self.vals=numpy.array(range(c), dtype='float32')*b+a+b/2
        slots=numpy.array(range(c+1), dtype='float32')*b+a
        self.counts=numpy.array([((kdata>slots[i])&(kdata<=slots[i+1])).sum() for i in range(c)])/(1.0*totpix)
        belowcounts=(kdata<=slots[0]).sum()-kdata.shape[0]**2+totpix #get rid of all the zeros from killmap
        abovecounts=(kdata>slots[-1]).sum()
        self.plotw.performplot([self.vals, self.counts], overlay=self.overlayCheckBox.isChecked())
        self.histstr=''.join(('%d'%belowcounts, 'pixels with counts <=', '%d'%slots[0],' and ','%d'%abovecounts, 'pixels with counts >', '%d'%slots[-1],  '. Total pixels: ', '%d'%totpix))
        self.plotw.fig.canvas.draw()

class plotwavetrans1dwindow(QDialog):
    def __init__(self, parent, h5path, h5groupstr, runpath, navchoice, type='h5mar:icounts'):
        super(plotwavetrans1dwindow, self).__init__(parent)

        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.runpath=runpath
        self.navchoice=navchoice
        self.savename1='_'.join((os.path.split(self.h5path)[1][0:-3], self.h5groupstr, ''))
        self.imnamelist=[]

        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]

        if 'h5mar' in type:
            self.wtgrpstr='/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'wavetrans1d'))
            qgridtemp=getimapqgrid(h5analysis.attrs['imapstr'], imap=False)
            self.pointlist=h5analysis.attrs['pointlist']
            self.overlayifcountsbool='ifcounts' in h5mar
            self.countsarrstr='/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'icounts'))
            self.processedcountsarrstr='/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis),'ifcounts'))
        elif 'h5tex' in type:
            h5grpname=type.partition(':')[2]
            h5tex=h5mar['texture']
            h5texgrp=h5tex[h5grpname]
            self.wtgrpstr='/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'texture', h5grpname, 'wavetrans1d'))
            qgridtemp=h5texgrp.attrs['chigrid']
            self.overlayifcountsbool=False
            self.countsarrstr='/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'texture', h5grpname, 'icounts'))
            self.processedcountsarrstr='/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'texture', h5grpname, 'ifcounts'))
            self.pointlist=h5texgrp.attrs['pointlist']

        wtgrp=h5file[self.wtgrpstr]

        self.attrdict=getattr(self.h5path, self.h5groupstr)


        self.qgrid=wtgrp.attrs['qgrid'] #use the wave trans qgrid as the qgrid because it is the union of it and the icounts qgrid
        self.qscalegrid=wtgrp.attrs['qscalegrid']
        self.qposngrid=wtgrp.attrs['qposngrid']

        self.icountsind=numpy.array([qval in q_qgrid_ind(self.qgrid) for qval in q_qgrid_ind(qgridtemp)])

        self.imnamelist=[]

        self.imnamelist+=['%d' %p for p in self.pointlist]


        for node in wtgrp.iterobjects():
            if (node.name.rpartition('/')[2]).startswith('wt') and isinstance(node, h5py.Dataset) and len(node.shape)==2:
                self.imnamelist+=[node.name.rpartition('/')[2]]
        h5file.close()

        if len(self.imnamelist)==0:
            print 'NO 1D IMAGES FOUND!'
            return
        self.setWindowTitle('Plot wavelet trnasform of 1d spectra')

        self.savenavimageButton=QPushButton()
        self.savenavimageButton.setText('save .png\nnavigator')
        QObject.connect(self.savenavimageButton,SIGNAL("pressed()"),self.savenavimage)

        self.xgrid=self.attrdict['xgrid']
        self.zgrid=self.attrdict['zgrid']
        self.xcoords=self.attrdict['x']
        self.zcoords=self.attrdict['z']


        if self.navchoice==0:
            self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
        else:
            elstr=self.attrdict['elements']

            if self.navchoice==1:
                infotype='DPmolfracALL'
            else:
                infotype='XRFmolfracALL'
            self.elstrlist, self.compsarr=getternarycomps(self.h5path, self.h5groupstr, elstr=elstr, infotype=infotype)
            if self.compsarr is None:
                print 'NO COMPOSITION NAVIGATOR WINDOW BECAUSE PROBLEM CALCULATING COMPOSITIONS'
                self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
            else:
                print 'COMPS:', self.compsarr
                self.navw = compnavigatorwidget(self, self.compsarr, self.elstrlist)
        QObject.connect(self.navw, SIGNAL("picclicked"), self.picclickprocess)

        self.colridgesCheckBox=QCheckBox()
        self.colridgesCheckBox.setText('color ridges\nbyWT value')
        self.colridgesCheckBox.setChecked(True)

        self.peaksCheckBox=QCheckBox()
        self.peaksCheckBox.setText('include\npeaks')
        self.peaksCheckBox.setChecked(True)

        if self.overlayifcountsbool:
            self.ifcountsCheckBox=QCheckBox()
            self.ifcountsCheckBox.setText('use ifcounts\nprocessed data')
            self.ifcountsCheckBox.setChecked(False)

        self.plotComboBox=QComboBox()
        self.plotComboBox.clear()
        self.plotComboBox.insertItem(999, '2D W.T. w/ 1D data')
        self.plotComboBox.insertItem(999, '2D W.T. w/ WT@scale')
        self.plotComboBox.insertItem(999, 'overlay 1D data')
        self.plotComboBox.insertItem(999, 'overlay WT@scale')
        self.plotComboBox.setCurrentIndex(0)

        self.imComboBox=QComboBox()
        self.scaleComboBox=QComboBox()

        self.drawButton=QPushButton()
        self.drawButton.setText('draw image')
        QObject.connect(self.drawButton,SIGNAL("pressed()"),self.draw)

        if False:
            self.fittedpeaksButton=QPushButton()
            self.fittedpeaksButton.setText('overlay\nfitted peaks')
            QObject.connect(self.fittedpeaksButton,SIGNAL("pressed()"),self.drawfittedpeaks)

        self.saveButton=QPushButton()
        self.saveButton.setText('save .png')
        QObject.connect(self.saveButton,SIGNAL("pressed()"),self.save)
        toplayout=QHBoxLayout()
        toplayout.addWidget(self.savenavimageButton)
        toplayout.addWidget(self.colridgesCheckBox)
        toplayout.addWidget(self.peaksCheckBox)
        if self.overlayifcountsbool:
            toplayout.addWidget(self.ifcountsCheckBox)
        toplayout.addWidget(self.plotComboBox)
        toplayout.addWidget(self.imComboBox)
        toplayout.addWidget(self.scaleComboBox)
        toplayout.addWidget(self.drawButton)
        if False:
            toplayout.addWidget(self.fittedpeaksButton)
        toplayout.addWidget(self.saveButton)
        layout=QVBoxLayout()
        leftlayout=QVBoxLayout()
        rightlayout=QVBoxLayout()
        lefttoplayout=QGridLayout()
        plotlayout=QHBoxLayout()

        self.unusedSpinBox=QSpinBox()
        self.unusedSpinBox.setValue(0)
        self.unusedSpinBox.setRange(0,1000000 )

        self.imgLabel=QLabel()

        self.plotw=wavelet1dplotwidget(self, self.qgrid, self.qscalegrid, self.qposngrid)
        QObject.connect(self.plotw, SIGNAL("dataaxesclicked"), self.clickhandler)

        lab1=QLabel()
        lab2=QLabel()
        lab1.setText('click peak->remove peak @ position')
        self.activeremoveCheckBox=QCheckBox()
        self.activeremoveCheckBox.setText('remove peaks with clicks is active')
        self.activeremoveCheckBox.setChecked(False)
        self.peaksremoved=QSpinBox()
        self.peaksremoved.setValue(0)
        self.peaksremoved.setDisabled(True)
        lab2.setText('number of peaks removed')

        lefttoplayout.addWidget(self.activeremoveCheckBox, 0, 0, 1, 3)
        lefttoplayout.addWidget(lab1, 1, 0, 1, 3)
        lefttoplayout.addWidget(lab2, 2, 0, 1, 2)
        lefttoplayout.addWidget(self.peaksremoved, 2, 2, 1, 1)
        self.qvalueofpeakremoval=None


        leftlayout.addLayout(lefttoplayout)
        rightlayout.addWidget(self.imgLabel)

        leftlayout.addWidget(self.navw)
        rightlayout.addWidget(self.plotw)
        plotlayout.addLayout(leftlayout)
        plotlayout.addLayout(rightlayout)

        layout.addLayout(toplayout)
        layout.addLayout(plotlayout)

        self.setLayout(layout)
        self.fillimComboBox()
        self.fillscaleComboBox()

        self.savecount=0
        self.selectlist=[]
        self.imnum=0
        self.imname=unicode(self.imComboBox.currentText())

        self.navw.plotpoints(self.pointlist, [])

    def fillimComboBox(self):
        self.imComboBox.clear()
        if len(self.imnamelist)>0:
            for name in self.imnamelist:
                self.imComboBox.insertItem(999, name)
        else:
            self.imComboBox.insertItem(0, 'err')
        self.imComboBox.setCurrentIndex(0)

    def fillscaleComboBox(self):
        self.scaleComboBox.clear()
        for s in scale_scalegrid_ind(self.qscalegrid):
            self.scaleComboBox.insertItem(999, 'scale %.2f' %s)
        self.scaleComboBox.setCurrentIndex(0)

    def clickhandler(self, clickxy):
#        if self.addpeaks:
#            self.addpeakposnSpinBox.setValue(clickxy[0])
#            self.addpeak()
        if self.activeremoveCheckBox.isChecked():
            self.qvalueofpeakremoval=clickxy[0]
            self.removepeak()

    def removepeak(self):
        h5file=h5py.File(self.h5path, mode='r+')
        wtgrp=h5file[self.wtgrpstr]
        if not 'peaks' in wtgrp:
            print "PEAKS HAVE NOT BEEN IDENTIFIED"
            h5file.close()
            return
        pkscaleind=wtgrp['peaks'][self.imnum, 0, :]
        pkposnind=wtgrp['peaks'][self.imnum, 1, :]
        pkqvals=numpy.float32(pkposnind[pkposnind!=32767])
        ind=myargmin((pkqvals-self.qvalueofpeakremoval)**2)
        print 'removing peak at ', self.qvalueofpeakremoval
        #print (pkqvals-self.qvalueofpeakremoval)**2
        print (numpy.append(numpy.append(pkscaleind[:ind],pkscaleind[ind+1:]),numpy.uint16([32767]))).dtype
        wtgrp['peaks'][self.imnum, 0, :]=numpy.append(numpy.append(pkscaleind[:ind],pkscaleind[ind+1:]),numpy.uint16([32767]))[:]
        wtgrp['peaks'][self.imnum, 1, :]=numpy.append(numpy.append(pkposnind[:ind],pkposnind[ind+1:]),numpy.uint16([32767]))[:]


        print  self.imnum, ind


        h5file.close()
        self.peaksremoved.setValue(1+self.peaksremoved.value())

    def picclickprocess(self, picnum):
        picname='%d' %picnum
        if picname in self.imnamelist:
            for i in range(len(self.imnamelist)):
                if self.imnamelist[i]==picname:
                    self.imComboBox.setCurrentIndex(i)
                    break
        self.draw()

    def save(self):
        self.plotw.save(os.path.join(self.runpath, ''.join((self.savename1, self.savename2))).replace('\\','/').encode())

    def savenavimage(self):
        self.navw.save(os.path.join(self.runpath, ''.join((self.savename1, '_WT1dPlotPoints', '%d' %self.savecount))).replace('\\','/').encode())
        self.savecount+=1

    def drawfittedpeaks(self):
        print 'not implemented yet'

    def draw(self):
        self.imname=unicode(self.imComboBox.currentText())

        if self.imname.isdigit():
            self.imnum=eval(self.imname)
        else:
            print 'plotting wavetrans of auxiliary data is not yet supported'

        self.selectlist=[self.imnum]

        if self.colridgesCheckBox.isChecked():
            wtcmap=cm.jet
            ridgecmap=cm.gray
        else:
            wtcmap=cm.gray
            ridgecmap=None

        self.savename2=''.join(('_wavetrans1d_', self.imname))

        plottype=self.plotComboBox.currentIndex()

        if plottype==0: #2D W.T. w/ 1D data
            overlay=False
            w_o_c=self.countsarrstr
            if self.overlayifcountsbool:
                if self.ifcountsCheckBox.isChecked():
                    w_o_c=self.processedcountsarrstr
        elif plottype==1: #2D W.T. w/ WT@scale
            overlay=False
            w_o_c=self.scaleComboBox.currentIndex()
        elif plottype==2: #overlay 1D data
            overlay=True
            w_o_c=self.countsarrstr
            if self.overlayifcountsbool:
                if self.ifcountsCheckBox.isChecked():
                    w_o_c=self.processedcountsarrstr
        elif plottype==3: #overlay WT@scale
            overlay=True
            w_o_c=self.scaleComboBox.currentIndex()
        else:
            QMessageBox.warning(self,"failed",  'ABORTED. PLOTTING NOT SUPPORTED:', unicode(self.plotComboBox.currentText()))
            return

        self.display_wavetrans1dcaller(w_o_c, title='', wtcmap=wtcmap, ridgecmap=ridgecmap, overlay1donly=overlay)

        self.navw.plotpoints(self.pointlist, [], select=self.selectlist)

        self.navw.fig.canvas.draw()
        self.imgLabel.setText(self.savename2)

    def display_wavetrans1dcaller(self, wavescaleind_or_countsname, wtcmap=cm.jet, ridgecmap=cm.gray, title='', overlay1donly=False):
        #datascaleind gives the index of the scale parameter to use in the 1D spectrum plot. if it is None the 1D data from icounts will be displayed
        h5file=h5py.File(self.h5path, mode='r')
        wtgrp=h5file[self.wtgrpstr]

        wt=wtgrp['wavetrans'][self.imnum, :, :]
        if 'ridges' in wtgrp:
            ridges=wtgrp['ridges'][self.imnum, :, :]
            ridges=ridges[ridges.mean(axis=1)!=32767, :]
        else:
            ridges=[]

        datapeakind=None
        if isinstance(wavescaleind_or_countsname, str):
            datascaleind=None
            print h5file[wavescaleind_or_countsname].shape, h5file[wavescaleind_or_countsname][self.imnum].shape, h5file[wavescaleind_or_countsname][self.imnum][self.icountsind].shape
            data=h5file[wavescaleind_or_countsname][self.imnum][self.icountsind]
            if ('peaks' in wtgrp) and self.peaksCheckBox.isChecked():
                datapeakind=wtgrp['peaks'][self.imnum, 1, :]
                datapeakind=datapeakind[datapeakind!=32767]
                datapeakind=ind_qgrid_q(self.qgrid, q_qgrid_ind(self.qposngrid, datapeakind), fractional=True)
        else:
            datascaleind=wavescaleind_or_countsname
            data=wt[datascaleind, :]
            if ('ridges' in wtgrp) and self.peaksCheckBox.isChecked():
                ridgesatscale=ridges[:, wt.shape[0]-1-datascaleind]
                datapeakind=ridgesatscale[(ridgesatscale>=0)&(ridgesatscale!=32767)]
        h5file.close()
        if overlay1donly:
            self.plotw.plot1doverlay(data, datascaleind, datapeakind=datapeakind)
        else:
            self.plotw.display_wavetrans1d(wt, ridges, data, datascaleind=datascaleind, datapeakind=datapeakind, wtcmap=wtcmap, ridgecmap=ridgecmap, title='')
        self.plotw.fig.canvas.draw()


class plotinterpimageof1ddatawindow(QDialog):
    def __init__(self, parent, h5path, h5groupstr, runpath, navchoice, style='interp', type='h5mar'):
        super(plotinterpimageof1ddatawindow, self).__init__(parent)
        self.type=type
        self.texturestyle=False
        if style=='interp' or style=='texture':
            self.interpstyle=True
            self.texturestyle= style=='texture'
            self.infostyle=False
        elif style=='info':
            self.interpstyle=False
            self.infostyle=True
        else:
            self.interpstyle=False
            self.infostyle=False
            print 'PLOTTING TYPE NOT UNDERSTOOD'
        if style=='texture' and 'tex' in type:
            QMessageBox.warning(self,"warning",  "For interp plot, type should be 'h5mar' when style is 'texture'")
        self.navchoice=navchoice

        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.runpath=runpath

        self.savename1='_'.join((os.path.split(self.h5path)[1][0:-3], self.h5groupstr, ''))

        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
        
        self.bin=getbin(h5analysis)
        
        if 'h5mar' in type:
            self.h5datagrpstr='/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))
            qgridtemp=getimapqgrid(h5analysis.attrs['imapstr'], imap=False)
            self.pointlist=h5analysis.attrs['pointlist']
            self.overlayifcountsbool='ifcounts' in h5mar
#            self.countsarrstr='/'.join((self.h5groupstr, 'analysis/mar345', 'icounts'))
#            self.processedcountsarrstr='/'.join((self.h5groupstr, 'analysis/mar345', 'ifcounts'))
            self.qgrid=h5mar['icounts'].attrs['qgrid']
        elif 'h5tex' in type:
            h5grpname=type.partition(':')[2]
            h5tex=h5mar['texture']
            h5texgrp=h5tex[h5grpname]
            self.h5datagrpstr='/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis),'texture', h5grpname))
            qgridtemp=h5texgrp.attrs['chigrid']
            self.overlayifcountsbool=False
#            self.countsarrstr='/'.join((self.h5groupstr, 'analysis/mar345', 'texture', h5grpname, 'icounts'))
#            self.processedcountsarrstr='/'.join((self.h5groupstr, 'analysis/mar345', 'texture', h5grpname, 'ifcounts'))
            self.pointlist=h5texgrp.attrs['pointlist']
            self.qgrid=h5texgrp.attrs['chigrid']

        self.attrdict=getattr(self.h5path, self.h5groupstr)
        self.qvals=q_qgrid_ind(self.qgrid)

        self.sampleinfo,  garbage=getpointinfo(self.h5path, self.h5groupstr)
        self.headings=pointinfodictkeysort(self.sampleinfo)

        if self.interpstyle:
            self.xrdtypeComboBox=QComboBox()
            self.xrdtypeComboBox.clear()
            if 'icounts' in h5file[self.h5datagrpstr]:
                self.xrdtypeComboBox.insertItem(999, 'icounts')
            if 'ifcounts' in h5file[self.h5datagrpstr]:
                self.xrdtypeComboBox.insertItem(999, 'ifcounts')
                self.xrdtypeComboBox.setCurrentIndex(1)
        if self.texturestyle:
            self.killmap=getkillmap(h5analysis.attrs['killmapstr'])
            self.killmapbin=getkillmap(h5analysis.attrs['killmapstr'], bin=self.bin)
            self.imap, qgrid=getimapqgrid(h5analysis.attrs['imapstr'])
            self.imapbin, qgrid=getimapqgrid(h5analysis.attrs['imapstr'], bin=self.bin)
            self.imapkillmap=self.killmap*(self.imap!=0)
            self.imapkillmapbin=self.killmapbin*(self.imapbin!=0)
            self.chimap, self.chigrid=getchimapchigrid(h5analysis.attrs['chimapstr'])
            self.chimapbin, self.chigrid=getchimapchigrid(h5analysis.attrs['chimapstr'], bin=self.bin)
            self.imap*=self.killmap
            self.imapbin*=self.killmapbin
            self.chimap*=self.killmap
            self.chimapbin*=self.killmapbin
            self.dqchiimage=getdqchiimage(h5analysis.attrs['dqchiimagestr'])
            self.dqchiimagebin=getdqchiimage(h5analysis.attrs['dqchiimagestr'], bin=self.bin)

            self.bcknd=self.attrdict['bcknd']
            if 'lin' in self.bcknd:
                self.bckndarr, self.blinwts=readblin(h5mar)
                self.bckndarrbin, self.blinwts=readblin(h5mar, bin=self.bin)
            else:
                bstr=''.join(('b', self.bcknd[:3]))
                self.bckndarr=readh5pyarray(h5mar[bstr])
                bstr=''.join((bstr, 'bin%d' %self.bin))
                self.bckndarrbin=readh5pyarray(h5mar[bstr])

            if self.bcknd=='minanom':
                if 'bimap' in h5mar:
                    bimap=readh5pyarray(h5mar['bimap'])
                    bqgrid=h5mar['bimap'].attrs['bqgrid']
                else:
                    bimap=None
                    bqgrid=None
                self.banomcalc=(self.imapbin, self.qgrid, self.attrdict, bimap, bqgrid)
                self.bminanomf=readh5pyarray(h5mar['bminanomf'])

        h5file.close()
        self.xgrid=self.attrdict['xgrid']
        self.zgrid=self.attrdict['zgrid']
        self.xcoords=self.attrdict['x']
        self.zcoords=self.attrdict['z']

        if self.interpstyle:
            self.setWindowTitle('Plot interpolation of 1d spectra')
        elif self.infostyle:
            self.setWindowTitle('Plot sample info')

#PLOT STYLE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        plotstylelayout=QGridLayout()

        if self.interpstyle:
            self.plotpeaksCheckBox=QCheckBox()
            self.plotpeaksCheckBox.setText('plot peaks')
            self.plotpeaksCheckBox.setChecked(False)
            self.peaksstyleLineEdit=QLineEdit()
            self.peaksstyleLineEdit.setText('w.6')
            self.datamarkerCheckBox=QCheckBox()
            self.datamarkerCheckBox.setText('use marker to\nshow spectra posns')
            self.datamarkerCheckBox.setChecked(True)
            self.datamarkerstyleLineEdit=QLineEdit()
            self.datamarkerstyleLineEdit.setText('r>10')

            self.xrdtypeLabel=QLabel()
            self.xrdtypeLabel.setText('1D-XRD type')


            plotstylelayout.addWidget(self.xrdtypeLabel, 0, 0, 1, 1)
            plotstylelayout.addWidget(self.xrdtypeComboBox, 1, 0, 1, 1)
            plotstylelayout.addWidget(self.plotpeaksCheckBox, 0, 1, 1, 1)
            plotstylelayout.addWidget(self.peaksstyleLineEdit, 1, 1, 1, 1)
            plotstylelayout.addWidget(self.datamarkerCheckBox, 0, 2, 1, 1)
            plotstylelayout.addWidget(self.datamarkerstyleLineEdit, 1, 2, 1, 1)

        elif self.infostyle:
            self.plotxzCheckBox=QCheckBox()
            self.plotxzCheckBox.setText('plot x,z pts')
            self.plotxzCheckBox.setChecked(True)
            self.xzstyleLineEdit=QLineEdit()
            self.xzstyleLineEdit.setText('kx6')
            self.datastyleLabel=QLabel()
            self.datastyleLabel.setText('data plot style(s)')
            self.datastyleLineEdit=QLineEdit()
            self.datastyleLineEdit.setText('ro,r-')

            #plotstylelayout.addWidget(, 0, 0, 1, 1)
            #plotstylelayout.addWidget(, 1, 0, 1, 1)
            plotstylelayout.addWidget(self.plotxzCheckBox, 0, 1, 1, 1)
            plotstylelayout.addWidget(self.xzstyleLineEdit, 1, 1, 1, 1)
            plotstylelayout.addWidget(self.datastyleLabel, 0, 2, 1, 1)
            plotstylelayout.addWidget(self.datastyleLineEdit, 1, 2, 1, 1)

        cmaplab=QLabel()
        cmaplab.setText('colormap\n(cmap or blank)')

        self.cmapLineEdit=QLineEdit()
        self.cmapLineEdit.setText('jet')

        plotstylelayout.addWidget(cmaplab, 0, 3, 1, 1)
        plotstylelayout.addWidget(self.cmapLineEdit, 1, 3, 1, 1)

#PLOT RANGE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if self.interpstyle:
            self.pdfsetupButton=QPushButton()
            self.pdfsetupButton.setText('plot PDF')
            QObject.connect(self.pdfsetupButton,SIGNAL("pressed()"),self.pdfsetup)
            self.pdflineLabel1=QLabel()
            self.pdflineLabel1.setText('pdf ctrl:')
            self.pdflineLabel2=QLabel()
            self.pdflineLabel2.setText('ymin,ymax,colstr,linew')
            self.pdfplotinfoLineEdit=QLineEdit()
            self.pdfplotinfoLineEdit.setText('')

            self.interpCheckBox=QCheckBox()
            self.interpCheckBox.setText('interp y-axis')
            self.interpCheckBox.setChecked(False)

            logcbstr='log int. cutoff'
        else:
            logcbstr='log intensity'

        self.logCheckBox=QCheckBox()
        self.logCheckBox.setText(logcbstr)
        self.logCheckBox.setChecked(False)

        logcutlab=QLabel()
        logcutlab.setText('log int. cutoff:')

        self.logcutSpinBox=QDoubleSpinBox()
        self.logcutSpinBox.setValue(10.0)
        self.logcutSpinBox.setDecimals(8)
        self.logcutSpinBox.setRange(0,1000000 )

        self.cmaponethirdSpinBox=QDoubleSpinBox()
        self.cmaponethirdSpinBox.setValue(.33)
        self.cmaponethirdSpinBox.setRange(.00001, .99999)

        self.cmaptwothirdsSpinBox=QDoubleSpinBox()
        self.cmaptwothirdsSpinBox.setValue(.67)
        self.cmaptwothirdsSpinBox.setRange(.00001, .99999)


        xrangelab=QLabel()
        if self.interpstyle:
            if 'tex' in type:
                xrangelab.setText('PHI-range min, max')
            else:
                xrangelab.setText('Q-range min, max')
        elif self.infostyle:
            xrangelab.setText('X info min, max')

        yrangelab=QLabel()
        yrangelab.setText('Y info min, max')

        ynumlab=QLabel()
        ynumlab.setText('num Y info pts')

        perclab=QLabel()
        perclab.setText('percentile of data for\n1st, 2nd tertile of cmap')


        self.YgetinfominmaxButton=QPushButton()
        self.YgetinfominmaxButton.setText('set min/max\nof info{points}')
        QObject.connect(self.YgetinfominmaxButton,SIGNAL("pressed()"),self.Ygetinfominmax)

        self.XgetinfominmaxButton=QPushButton()
        self.XgetinfominmaxButton.setText('set min/max\nof info{points}')
        QObject.connect(self.XgetinfominmaxButton,SIGNAL("pressed()"),self.Xgetinfominmax)


        self.YinfominSpinBox=QDoubleSpinBox()
        self.YinfominSpinBox.setValue(0)
        self.YinfominSpinBox.setRange(-999999999, 999999999)
        self.YinfominSpinBox.setDecimals(3)

        self.YinfomaxSpinBox=QDoubleSpinBox()
        self.YinfomaxSpinBox.setValue(1)
        self.YinfomaxSpinBox.setRange(-999999999, 999999999)
        self.YinfomaxSpinBox.setDecimals(3)

        self.YinfonumSpinBox=QSpinBox()
        self.YinfonumSpinBox.setValue(100)
        self.YinfonumSpinBox.setRange(1, 100000)

        self.XinfominSpinBox=QDoubleSpinBox()
        self.XinfomaxSpinBox=QDoubleSpinBox()

        if self.interpstyle:
            self.XinfominSpinBox.setValue(q_qgrid_ind(self.qgrid, 0))
            self.XinfominSpinBox.setRange(q_qgrid_ind(self.qgrid, 0), q_qgrid_ind(self.qgrid, self.qgrid[2]-1))

            self.XinfomaxSpinBox.setValue(q_qgrid_ind(self.qgrid, self.qgrid[2]-1))
            self.XinfomaxSpinBox.setRange(q_qgrid_ind(self.qgrid, 0), q_qgrid_ind(self.qgrid, self.qgrid[2]-1))
        elif self.infostyle:
            self.XinfominSpinBox.setValue(0)
            self.XinfominSpinBox.setRange(-999999999, 999999999)
            self.XinfomaxSpinBox.setValue(1)
            self.XinfomaxSpinBox.setRange(-999999999, 999999999)

        plotrangelayout=QGridLayout()

        if self.interpstyle:
            plotrangelayout.addWidget(perclab, 0, 0, 2, 2)
            plotrangelayout.addWidget(self.cmaponethirdSpinBox, 2, 0, 1, 1)
            plotrangelayout.addWidget(self.cmaptwothirdsSpinBox, 2, 1, 1, 1)

            plotrangelayout.addWidget(self.pdfsetupButton, 3, 0, 1, 1)
            plotrangelayout.addWidget(self.pdflineLabel1, 4, 0, 1, 1)
            plotrangelayout.addWidget(self.pdflineLabel2, 3, 1, 1, 1)
            plotrangelayout.addWidget(self.pdfplotinfoLineEdit, 4, 1, 1, 1)

            plotrangelayout.addWidget(self.logCheckBox, 5, 0, 1, 1)
            plotrangelayout.addWidget(self.logcutSpinBox, 5, 1, 1, 1)

            plotrangelayout.addWidget(self.interpCheckBox, 6, 0, 1, 1)

#            plotrangelayout.addWidget(self.logCheckBox, 3, 0, 1, 2)
#            plotrangelayout.addWidget(logcutlab, 4, 0, 1, 1)
#            plotrangelayout.addWidget(self.logcutSpinBox, 4, 1, 1, 1)

        plotrangelayout.addWidget(xrangelab, 0, 2, 1, 1)
        plotrangelayout.addWidget(self.XinfominSpinBox, 1, 2, 1, 1)
        plotrangelayout.addWidget(self.XinfomaxSpinBox, 2, 2, 1, 1)
        plotrangelayout.addWidget(self.XgetinfominmaxButton, 3, 2, 1, 1)


        plotrangelayout.addWidget(yrangelab, 0, 3, 1, 1)
        plotrangelayout.addWidget(self.YinfominSpinBox, 1, 3, 1, 1)
        plotrangelayout.addWidget(self.YinfomaxSpinBox, 2, 3, 1, 1)
        plotrangelayout.addWidget(self.YgetinfominmaxButton, 3, 3, 1, 1)
        if self.interpstyle:
            plotrangelayout.addWidget(ynumlab, 4, 2, 1, 1)
            plotrangelayout.addWidget(self.YinfonumSpinBox, 4, 3, 1, 1)

#PLOT CONTROL+SAVE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        self.savenavimageButton=QPushButton()
        self.savenavimageButton.setText('save .png\nnavigator')
        QObject.connect(self.savenavimageButton,SIGNAL("pressed()"),self.savenavimage)

        self.drawButton=QPushButton()
        self.drawButton.setText('draw image')

        if self.interpstyle:
            QObject.connect(self.drawButton,SIGNAL("pressed()"),self.interpdraw)
        elif self.infostyle:
            QObject.connect(self.drawButton,SIGNAL("pressed()"),self.substrateinfoplot)

        self.saveButton=QPushButton()
        self.saveButton.setText('save .png')
        QObject.connect(self.saveButton,SIGNAL("pressed()"),self.save)

        self.clearplotsButton=QPushButton()
        self.clearplotsButton.setText('clear plots')
        QObject.connect(self.clearplotsButton,SIGNAL("pressed()"),self.clearplots)

        imglabelLabel=QLabel()
        imglabelLabel.setText('Save Name:')

        self.imgLabel=QLineEdit()

        plotlabellayout=QVBoxLayout()
        plotlabellayout.addWidget(imglabelLabel)
        plotlabellayout.addWidget(self.imgLabel)
#        plotcontrollayout.addWidget(imglabelLabel, 0, 0, 1, 1)
#        plotcontrollayout.addWidget(self.imgLabel, 0, 1, 1, 3)


        plotcontrollayout=QGridLayout()
        plotcontrollayout.addWidget(self.clearplotsButton, 0, 0, 1, 1)
        plotcontrollayout.addLayout(plotlabellayout, 0, 1, 1, 3)
        plotcontrollayout.addWidget(self.drawButton, 0, 4, 1, 1)
        plotcontrollayout.addWidget(self.saveButton, 0, 5, 1, 1)
        plotcontrollayout.addWidget(self.savenavimageButton, 0, 6, 1, 1)

#SAMPLE INFO~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.allinfodict={}

        self.InfoTextBrowser=QTextBrowser()
        self.InfoTextBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.InfoTextBrowser.setPlainText('IND: selected spec inds\n')
        for i, h in enumerate(self.headings):
            if i<26:
                k=chr(65+i)
            else:
                k=chr(97+i%26)+chr(97+i%26+i//26-1)
            self.allinfodict[k]=self.sampleinfo[h]
            self.InfoTextBrowser.setPlainText('%s%s: %s\n' %(str(self.InfoTextBrowser.toPlainText()), k, h))

        self.InfoTextBrowser.setReadOnly(True)

        self.YInfoMathTextBrowser=QTextBrowser()
        self.YInfoMathTextBrowser.setReadOnly(False)
        self.YInfoMathTextBrowser.setText('IND')

        self.YappendspdshPushButton=QPushButton()
        self.YappendspdshPushButton.setText('Append to Spread Sheet')

        QObject.connect(self.YappendspdshPushButton,SIGNAL("pressed()"),self.YappendSpreadSheet)
        self.YinfoLabel=QLabel()
        self.YinfoLabel.setText('label:')
        self.YlabelLineEdit=QLineEdit()
        self.YlabelLineEdit.setText('')

        self.XInfoMathTextBrowser=QTextBrowser()
        self.XInfoMathTextBrowser.setReadOnly(False)
        self.XappendspdshPushButton=QPushButton()
        self.XappendspdshPushButton.setText('Append to Spread Sheet')
        QObject.connect(self.XappendspdshPushButton,SIGNAL("pressed()"),self.XappendSpreadSheet)
        self.XinfoLabel=QLabel()
        self.XinfoLabel.setText('label:')
        self.XlabelLineEdit=QLineEdit()
        self.XlabelLineEdit.setText('')

        self.XmathLabel=QLabel()
        self.YmathLabel=QLabel()

        if self.interpstyle:
            self.YmathLabel.setText('expression for interp Y-axis')
            self.XmathLabel.setText('expression for XRD normalization')
        elif self.infostyle:
            self.YmathLabel.setText('expression for info Y-axis')
            self.XmathLabel.setText('expression for info X-axis')


        sampleinfolayout=QGridLayout()

        sampleinfolayout.addWidget(self.InfoTextBrowser, 0, 0, 6, 4)

        sampleinfolayout.addWidget(self.YmathLabel, 0, 4, 1, 4)
        sampleinfolayout.addWidget(self.YInfoMathTextBrowser, 1, 4, 2, 4)

        sampleinfolayout.addWidget(self.YappendspdshPushButton, 1, 8, 1, 3)
        sampleinfolayout.addWidget(self.YinfoLabel, 0, 8, 1, 1)
        sampleinfolayout.addWidget(self.YlabelLineEdit, 0, 9, 1, 2)

        sampleinfolayout.addWidget(self.XmathLabel, 3, 4, 1, 4)
        sampleinfolayout.addWidget(self.XInfoMathTextBrowser, 4, 4, 2, 4)

        sampleinfolayout.addWidget(self.XappendspdshPushButton, 4, 8, 1, 3)
        sampleinfolayout.addWidget(self.XinfoLabel, 3, 8, 1, 1)
        sampleinfolayout.addWidget(self.XlabelLineEdit, 3, 9, 1, 2)


#SPREADSHEET~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.spdshTextBrowser=QTextBrowser()
        self.spdshTextBrowser.setPlainText('')
        self.spdshTextBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.spdshTextBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.spdshTextBrowser.setLineWrapMode(0)

        self.spdshFormatLineEdit=QLineEdit()
        self.spdshFormatLineEdit.setText('.3f')

        spdshFormatLabel=QLabel()
        spdshFormatLabel.setText('format:')

        self.spdshsavenameLineEdit=QLineEdit()
        self.spdshsavenameLineEdit.setText(self.savename1+'.txt')

        self.savespdshPushButton=QPushButton()
        self.savespdshPushButton.setText('save spreadsheet')
        QObject.connect(self.savespdshPushButton,SIGNAL("pressed()"),self.SaveSpreadSheet)

        self.ClearSpreadSheet()

        self.clearspdshPushButton=QPushButton()
        self.clearspdshPushButton.setText('clear\nsheet')
        QObject.connect(self.clearspdshPushButton,SIGNAL("pressed()"),self.ClearSpreadSheet)

        sampleinfolayout.addWidget(spdshFormatLabel, 0, 11, 1, 1)
        sampleinfolayout.addWidget(self.spdshFormatLineEdit, 1, 11, 1, 1)
        sampleinfolayout.addWidget(self.clearspdshPushButton, 0, 12, 2, 1)
        sampleinfolayout.addWidget(self.savespdshPushButton, 0, 13, 1, 3)
        sampleinfolayout.addWidget(self.spdshsavenameLineEdit, 1, 13, 1, 3)
        sampleinfolayout.addWidget(self.spdshTextBrowser, 2, 11, 4, 6)

#SPEC INDEX EDITOR~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.includeallButton=QPushButton()
        self.includeallButton.setText('include all points')
        QObject.connect(self.includeallButton,SIGNAL("pressed()"),self.includeallimages)

        self.parseptsButton=QPushButton()
        self.parseptsButton.setText('parse pts, avoid NaN')
        QObject.connect(self.parseptsButton,SIGNAL("pressed()"),self.ParseIndAvoidNaN)

        self.selectedimagesTextBrowser=QTextBrowser()
        self.selectedimagesTextBrowser.setPlainText('')
        self.selectedimagesTextBrowser.setReadOnly(False)

        specindlayout=QGridLayout()
        specindlayout.addWidget(self.includeallButton, 0, 0, 1, 2)
        specindlayout.addWidget(self.parseptsButton, 1, 0, 1, 2)
        specindlayout.addWidget(self.selectedimagesTextBrowser, 0, 2, 2, 3)




        xyplotlayout=QGridLayout()
#CHI TEXTURE CONTROL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if self.texturestyle:
            labtextinstruction=QLabel()
            labtextinstruction.setText('Will extract highest-intensity peak in Q-range and plot texture averaged over specified Q-width')

            lab6=QLabel()
            lab6.setText('q-range\nmin,max')

            self.peakextractqminSpinBox=QDoubleSpinBox()
            #self.peakextractqminSpinBox.setValue(q_qgrid_ind(self.qgrid, 0))
            self.peakextractqminSpinBox.setValue(27)
            self.peakextractqminSpinBox.setRange(q_qgrid_ind(self.qgrid, 0), q_qgrid_ind(self.qgrid, self.qgrid[2]-1))

            self.peakextractqmaxSpinBox=QDoubleSpinBox()
            #self.peakextractqmaxSpinBox.setValue(q_qgrid_ind(self.qgrid, self.qgrid[2]-1))
            self.peakextractqmaxSpinBox.setValue(28)
            self.peakextractqmaxSpinBox.setRange(q_qgrid_ind(self.qgrid, 0), q_qgrid_ind(self.qgrid, self.qgrid[2]-1))

            lab8=QLabel()
            lab8.setText('# of HWHM or\nQ-width (1/nm)')
            self.chiqwidthCheckBox=QCheckBox()
            self.chiqwidthCheckBox.setText('use HWHM')
            labundercb=QLabel()
            labundercb.setText('(unchecked->fixed width)')
            self.chiqwidthCheckBox.setChecked(True)

            self.chiqwidthSpinBox=QDoubleSpinBox()
            self.chiqwidthSpinBox.setValue(2)
            self.chiqwidthSpinBox.setRange(0, 5)

            lab7=QLabel()
            lab7.setText('PSI plot\nmin,max')

            self.chiminSpinBox=QDoubleSpinBox()
            self.chiminSpinBox.setRange(q_qgrid_ind(self.chigrid, 0), q_qgrid_ind(self.chigrid, self.chigrid[2]-1))
            self.chiminSpinBox.setValue(q_qgrid_ind(self.chigrid, 0))

            self.chimaxSpinBox=QDoubleSpinBox()
            self.chimaxSpinBox.setRange(q_qgrid_ind(self.chigrid, 0), q_qgrid_ind(self.chigrid, self.chigrid[2]-1))
            self.chimaxSpinBox.setValue(q_qgrid_ind(self.chigrid, self.chigrid[2]-1))

            self.fulltexplotComboBox=QComboBox()
            self.fulltexplotComboBox.clear()
            self.fulltexplotComboBox.insertItem(0, 'ave LHS+RHS')
            self.fulltexplotComboBox.insertItem(1, 'only LHS')
            self.fulltexplotComboBox.insertItem(2, 'only RHS')
            self.fulltexplotComboBox.setCurrentIndex(2)

            self.peakextractdrawButton=QPushButton()
            self.peakextractdrawButton.setText('extract peaks,\nplot chi vals')
            QObject.connect(self.peakextractdrawButton,SIGNAL("pressed()"),self.peakextractdraw)

            self.peakextractsaveButton=QPushButton()
            self.peakextractsaveButton.setText('save .png')
            QObject.connect(self.peakextractsaveButton,SIGNAL("pressed()"),self.xyplotsave)

            self.interpchiCheckBox=QCheckBox()
            self.interpchiCheckBox.setText('interpolate in\nPSI direction')
            self.interpchiCheckBox.setChecked(False)

            self.normchivalsCheckBox=QCheckBox()
            self.normchivalsCheckBox.setText('normalize each\nPSI dist by max')
            self.normchivalsCheckBox.setChecked(False)

            texturesavelabel=QLabel()
            texturesavelabel.setText('h5 save name\n(empty->not saved)')
            self.texturesaveLineEdit=QLineEdit()
            self.texturesaveLineEdit.setText('rhs111')

            xyplotlayout.addWidget(labtextinstruction, 0, 0, 1, 12)

            xyplotlayout.addWidget(lab6, 1, 0, 1, 2)
            xyplotlayout.addWidget(self.peakextractqminSpinBox, 2, 0, 1, 2)
            xyplotlayout.addWidget(self.peakextractqmaxSpinBox, 3, 0, 1, 2)

            chiqcblayout=QVBoxLayout()
            chiqcblayout.addWidget(self.chiqwidthCheckBox)
            chiqcblayout.addWidget(labundercb)
            xyplotlayout.addLayout(chiqcblayout, 1, 2, 2, 3)
            xyplotlayout.addWidget(lab8, 3, 2, 1, 2)
            xyplotlayout.addWidget(self.chiqwidthSpinBox, 3, 4, 1, 1)

            xyplotlayout.addWidget(lab7, 1, 5, 1, 2)
            xyplotlayout.addWidget(self.chiminSpinBox, 2, 5, 1, 2)
            xyplotlayout.addWidget(self.chimaxSpinBox, 3, 5, 1, 2)

            xyplotlayout.addWidget(self.fulltexplotComboBox, 1, 7, 1, 3)
            xyplotlayout.addWidget(self.interpchiCheckBox, 2, 7, 1, 3)
            xyplotlayout.addWidget(self.normchivalsCheckBox, 3, 7, 1, 3)

            xyplotlayout.addWidget(self.peakextractdrawButton, 1, 10, 1, 2)
            xyplotlayout.addWidget(self.peakextractsaveButton, 2, 10, 1, 2)

            chisavelinelayout=QVBoxLayout()
            chisavelinelayout.addWidget(texturesavelabel)
            chisavelinelayout.addWidget(self.texturesaveLineEdit)
            xyplotlayout.addLayout(chisavelinelayout, 3, 10, 1, 2)

#X,Y INFO PLOT CONTROL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if self.infostyle:

            self.xyplotoverlayCheckBox=QCheckBox()
            self.xyplotoverlayCheckBox.setText('overlay')
            self.xyplotoverlayCheckBox.setChecked(True)

            self.xyplotButton=QPushButton()
            self.xyplotButton.setText('plot info x-y')
            QObject.connect(self.xyplotButton,SIGNAL("pressed()"),self.xyinfoplot)

            self.xyplotsaveButton=QPushButton()
            self.xyplotsaveButton.setText('save .png')
            QObject.connect(self.xyplotsaveButton,SIGNAL("pressed()"),self.xyplotsave)

            xyplotlayout.addWidget(self.xyplotoverlayCheckBox, 0, 4, 1, 2)
            xyplotlayout.addWidget(self.xyplotButton, 0, 6, 1, 1)
            xyplotlayout.addWidget(self.xyplotsaveButton, 0, 9, 1, 1)

#PLOT WIDGETS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if self.navchoice==0:
            self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
        else:
            elstr=self.attrdict['elements']

            if self.navchoice==1:
                infotype='DPmolfracALL'
            else:
                infotype='XRFmolfracALL'
            self.elstrlist, self.compsarr=getternarycomps(self.h5path, self.h5groupstr, elstr=elstr, infotype=infotype)
            if self.compsarr is None:
                print 'NO COMPOSITION NAVIGATOR WINDOW BECAUSE PROBLEM CALCULATING COMPOSITIONS'
                self.navw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
            else:
                print 'COMPS:', self.compsarr
                self.navw = compnavigatorwidget(self, self.compsarr, self.elstrlist)
        QObject.connect(self.navw, SIGNAL("picclicked"), self.picclickprocess)

        if self.interpstyle:
            self.plotw=plotwidget(self, width=7, height=5, dpi=100)
        elif self.infostyle:
            self.plotw=subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords, width=5, dpi=100)

        if self.texturestyle or self.infostyle:
            self.chipeakorinfoplotw=plotwidget(self, width=7, height=4, dpi=100)


#MAIN GRID~~~~~~~~~~~~~~~~~~~~~~~
        layout=QGridLayout()
        layout.addLayout(plotstylelayout, 0, 0, 1, 4)
        layout.addLayout(plotrangelayout, 1, 0, 3, 4)
        layout.addLayout(specindlayout, 4, 0, 2, 4)
        layout.addWidget(self.navw, 6, 0, 2, 4)



        layout.addLayout(plotcontrollayout, 0, 4, 1, 5)

        if self.texturestyle or self.infostyle:
            layout.addWidget(self.plotw, 1, 4, 7, 5)
            if self.infostyle:
                layout.addLayout(xyplotlayout, 0, 9,  2, 5)
                layout.addWidget(self.chipeakorinfoplotw, 2, 9, 6, 5)
            elif self.texturestyle:
                layout.addLayout(xyplotlayout, 0, 9,  2, 5)
                layout.addWidget(self.chipeakorinfoplotw, 2, 9, 6, 5)
                self.chipeakorinfoplotw.axes.set_xlabel('sample info')
                self.chipeakorinfoplotw.axes.set_ylabel('Q posn of peak used in texture analysis')
        else:
            self.chipeakorinfoplotw=None
            layout.addWidget(self.plotw, 1, 4, 7, 10)

        layout.addLayout(sampleinfolayout, 8, 0, 3, 14)

        self.setLayout(layout)

#layouts done~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.navw.plotpoints(self.pointlist, [])
        QObject.connect(self.plotw, SIGNAL("genericclickonplot"), self.clickhandler)

        self.pointind_extractedpeaks=[]
        self.q_extractedpeaks=[]
        self.hwhm_extractedpeaks=[]
        self.chidrawbool=False
        self.spdshselectlist=[]
        self.includeallimages()
        self.tooltips()
        self.Ygetinfominmax()
#END OF __init__~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clearplots(self):
        self.plotw.reinit()
        if not self.chipeakorinfoplotw is None:
            self.chipeakorinfoplotw.reinit()

    def clickhandler(self, clickxy):
        garb=None

    def chidraw(self):
        interpchibool=self.interpchiCheckBox.isChecked()
        normchivalsbool=self.normchivalsCheckBox.isChecked()
        bin=False
        bckndbool=True

        texturesavename=str(self.texturesaveLineEdit.text())
        savetex = len(texturesavename)>0

        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]

        if bin:
            countspoint=h5mar['countsbin%d' %self.bin]
            imap=self.imapbin
            chimap=self.chimapbin
            dqchi=self.dqchiimagebin
            bckndarr=self.bckndarrbin
            imapkillmap=self.imapkillmapbin
        else:
            countspoint=h5file['/'.join((self.h5groupstr,'measurement', getxrdname(h5analysis), 'counts'))]
            imap=self.imap
            chimap=self.chimap
            dqchi=self.dqchiimage
            bckndarr=self.bckndarr
            imapkillmap=self.imapkillmap

        chiminplot=self.chiminSpinBox.value()
        chimaxplot=self.chimaxSpinBox.value()

        chiindexmin=ind_qgrid_q(self.chigrid, chiminplot, fractional=False)
        chiindexmax=ind_qgrid_q(self.chigrid, chimaxplot, fractional=False)
        chimapinds_plot=numpy.uint16(range(chiindexmin, chiindexmax+1))+1 # THE +1  IS BECAUSE INT HIS ROUTINE WE WILL OPERATE IN THE CHIMAP INDECES WHICH ARE ONE HIGHER THAN CHIGRID INDECES AND CAN BE NEGATIVE
        #savechigrid=qgrid_minmaxint(q_qgrid_ind(self.chigrid, chiindexmin), q_qgrid_ind(self.chigrid, chiindexmax), self.chigrid[1])

        chiqwidthSpinBoxval=self.chiqwidthSpinBox.value()
        if self.chiqwidthCheckBox.isChecked():
            qwidth=chiqwidthSpinBoxval*self.hwhm_extractedpeaks
        else:
            qwidth=[chiqwidthSpinBoxval]*len(self.hwhm_extractedpeaks)

        if savetex:
            npts=numpts_attrdict(self.attrdict)
            saveinds=numpy.uint16(self.pointind_extractedpeaks)
            savearr=numpy.ones((npts, self.chigrid[2]), dtype='float32')*numpy.nan

            q_peaks=numpy.ones(npts, dtype='float32')*numpy.nan
            dq_peaks=numpy.ones(npts, dtype='float32')*numpy.nan
            savenormvals=numpy.ones(npts, dtype='float32')*numpy.nan

            ind2dlist=[]

        self.chicounts=None
        for pointind, centerq, qw in zip(self.pointind_extractedpeaks, self.q_extractedpeaks, qwidth):
            if self.chicounts is None:
                self.chicounts=numpy.zeros((1, len(chimapinds_plot)), dtype='float32')
            else:
                self.chicounts=numpy.concatenate((self.chicounts, numpy.zeros((1, len(chimapinds_plot)), dtype='float32')), axis=0)

            plotarr=countspoint[pointind, :, :]
            lowqbin=ind_qgrid_q(self.qgrid, centerq-qw, fractional=False)+1
            highqbin=ind_qgrid_q(self.qgrid, centerq+qw, fractional=False)+1

            if self.bcknd=='minanom':
                h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
                banom=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis), 'banom'))][self.imnum, :, :]
                plotarr=bckndsubtract(plotarr, bckndarr, imapkillmap, btype=self.bcknd, banom_f_f=(banom, self.bminanomf[pointind, 0], self.bminanomf[pointind, 1]))[0]
            elif 'lin' in self.bcknd:
                plotarr=bckndsubtract(plotarr, bckndarr, imapkillmap, btype=self.bcknd, linweights=self.blinwts[pointind])[0]
            else:
                plotarr=bckndsubtract(plotarr, bckndarr, imapkillmap, btype=self.bcknd)[0]

            texplotind=self.fulltexplotComboBox.currentIndex()
            if texplotind==1:
                ind2d=numpy.where(((imap>=lowqbin)&(imap<=highqbin))&(chimap<0))
            elif texplotind==2:
                ind2d=numpy.where(((imap>=lowqbin)&(imap<=highqbin))&(chimap>0))
            else:
                ind2d=numpy.where(((imap>=lowqbin)&(imap<=highqbin))&(chimap!=0)) #as long as the bin vals are not zero this checks for killmap because imap contains killmap, per a few lines above. the chimap!=0 is just to be safe

            if savetex:
                ind2dlist+=[ind2d]

            if ind2d[0].size==0:
                print 'ERROR - THE ANNULUS FOR PSI PLOTTING WAS NOT FOUND IN THE BINNED MAR IMAGE'

            chimapinds=chimap[ind2d] #do not substract one, see above note. there should be no zeros  in this
            self.countvals=plotarr[ind2d]
            self.dqchivals=dqchi[ind2d]

            sortedchivals=sorted(list(set(chimapinds)))

            binnedchidata=[[chi, (self.countvals[chimapinds==chi]*self.dqchivals[chimapinds==chi]).sum()/(self.dqchivals[chimapinds==chi].sum())] for chi in sortedchivals if self.dqchivals[chimapinds==chi].sum()>0]

            cinds=numpy.int16(map(operator.itemgetter(0),binnedchidata))
            vals=numpy.float32(map(operator.itemgetter(1),binnedchidata))

            if texplotind==0:
                poschiind=numpy.where(cinds>0)
                negchiind=numpy.where(cinds<0)
                abschi=numpy.abs(cinds)
                cinds=sorted(list(set(abschi)))
                vals=numpy.float32([vals[abschi==chi].sum()/(abschi==chi).sum() for chi in cinds])
            elif texplotind==1:
                temp=copy.copy(cinds)
                cinds=numpy.abs(temp[::-1])
                temp=copy.copy(vals)
                vals=temp[::-1]
            cinds=numpy.uint16(cinds)



            if interpchibool:
                usablevals=numpy.float32(scipy.interp(chimapinds_plot, cinds, vals))
                indboolarr=numpy.bool_([True]*len(chimapinds_plot))
            else:
                indboolarr=numpy.array([cmi in cinds for cmi in chimapinds_plot])
                usablevals=numpy.float32([vals[count] for count, ind in enumerate(cinds) if ind in chimapinds_plot])
            if normchivalsbool:
                print 'before', usablevals.sum()
                normval=numpy.max(usablevals)
                usablevals/=normval
                print 'after', usablevals.sum()
            else:
                normval=1.
            if savetex:
                savearr[pointind][cinds-1]=vals/normval
                q_peaks[pointind]=centerq
                dq_peaks[pointind]=qw
                savenormvals[pointind]=normval
            self.chicounts[-1, indboolarr]=usablevals[:]
            print '**', self.chicounts.shape, self.chicounts.sum()
        h5file.close()


        if savetex:
            maxnuminds=max([len(xind) for xind, yind in ind2dlist])
            ind2dsavearr=numpy.ones((npts, 2, maxnuminds), dtype='uint16')*32767
            for pointind, ind2d in zip(saveinds, ind2dlist):
                xind, yind = ind2d
                ind2dsavearr[pointind, 0, :len(xind)]=xind[:]
                ind2dsavearr[pointind, 1, :len(yind)]=yind[:]

            h5file=h5py.File(self.h5path, mode='r+')
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            if 'texture' in h5mar:
                h5tex=h5mar['texture']
            else:
                h5tex=h5mar.create_group('texture')

            if texturesavename in h5tex:
                del h5tex[texturesavename]
            h5texgrp=h5tex.create_group(texturesavename)

            pointlist=[]
            for ind, arr in enumerate(savearr):#do this check in case saveinds included a point where everything ended being nan
                if not numpy.all(numpy.isnan(arr)):
                    pointlist+=[ind]

            h5texgrp.attrs['pointlist']=pointlist
            h5texgrp.attrs['chigrid']=self.chigrid
            h5texgrp.attrs['chiminplot']=chiminplot
            h5texgrp.attrs['chimaxplot']=chimaxplot
            h5texgrp.attrs['chiindexmin']=chiindexmin
            h5texgrp.attrs['chiindexmax']=chiindexmax
            h5texgrp.attrs['q_peaks']=q_peaks
            h5texgrp.attrs['qhalfwidth']=dq_peaks
            h5texgrp.attrs['normvals']=savenormvals #will be 1s and 0s if the was no normalization
            if bin:
                b=self.bin
            else:
                b=0
            h5texgrp.attrs['bin']=b
            h5texgrp.attrs['bckndbool']=int(bckndbool)
            h5texgrp.create_dataset('icounts', data=savearr)
            h5texgrp.create_dataset('ind2d', data=ind2dsavearr)
            h5file.close()

        self.chicounts[numpy.isnan(self.chicounts)]=0. #ideally would use nan to make a masked interp plot but not implemented yet
        self.chidrawbool=True
        self.interpdraw()


    def peakextractdraw(self):
        selectlist=self.getselectlist()
        if len(selectlist)==0:
            print 'abort plotting. no slected images'
            return



        print 'below is the info of the brightest peak in the selected range witha line for every point in poinlist. This is for pasting into a spreadhseet. copy until ^^^^^^^^^^^^\n','\t'.join(('index','q','hwhm','height','sigq','sighwhm','sigheight'))
        self.pointind_extractedpeaks, peakinfo=getpeaksinrange(self.h5path, self.h5groupstr, indlist=selectlist, qmin=self.peakextractqminSpinBox.value(), qmax=self.peakextractqmaxSpinBox.value(), returnonlyq=False,  performprint=True)
        print '^^^^^^^^^^^^^^'

        newimlist=''
        for pointind in self.pointind_extractedpeaks:
            newimlist+=',%d' %pointind
        self.selectedimagesTextBrowser.setPlainText(newimlist[1:])
        self.navw.plotpoints(self.pointlist, [], self.pointind_extractedpeaks)

        self.q_extractedpeaks=numpy.float32(peakinfo[:, 0])
        self.hwhm_extractedpeaks=numpy.float32(peakinfo[:, 1])

        self.chidraw()

        self.chipeakorinfoplotw.performplot([self.infovalsarr, self.q_extractedpeaks])
        self.plotw.fig.canvas.draw()
        self.navw.fig.canvas.draw()

    def interpdraw(self):
        if self.chidrawbool:
            qminplot=self.chiminSpinBox.value()
            qmaxplot=self.chimaxSpinBox.value()
            qgrid=self.chigrid
            selectlist=self.pointind_extractedpeaks
        else:
            qminplot=self.XinfominSpinBox.value()
            qmaxplot=self.XinfomaxSpinBox.value()
            qgrid=self.qgrid

            selectlist=numpy.uint16(self.getselectlist())

        infovalsarr_interpto=numpy.linspace(self.YinfominSpinBox.value(), self.YinfomaxSpinBox.value(), num=self.YinfonumSpinBox.value())
        qindexmin=ind_qgrid_q(qgrid, qminplot, fractional=False)
        qindexmax=ind_qgrid_q(qgrid, qmaxplot, fractional=False)
        qindarr=numpy.uint16(range(qindexmin, qindexmax+1))


        normarray=self.CalculateInfoVals(str(self.XInfoMathTextBrowser.toPlainText()), selectlist)
        self.infovalsarr=self.CalculateInfoVals(str(self.YInfoMathTextBrowser.toPlainText()), selectlist)


        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
        h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]

        if self.chidrawbool:
            counts=self.chicounts
        else:
            datatypestr=unicode(self.xrdtypeComboBox.currentText())
            if datatypestr=='ifcounts':
                counts=readh5pyarray(h5file[self.h5datagrpstr]['ifcounts'])[selectlist][:, qindarr]
            else:
                counts=readh5pyarray(h5file[self.h5datagrpstr]['icounts'])[selectlist][:, qindarr]


        if self.plotpeaksCheckBox.isChecked() and not self.chidrawbool:
            pkcounts=readh5pyarray(h5file[self.h5datagrpstr]['pkcounts'])
        h5file.close()
        if numpy.any(numpy.isnan(counts)):
            QMessageBox.warning(self,"failed",  "In that range, 1d data contained NaN. Aborting")
            return
#        data=None      this method interped in both directions whcih causes problems
#        fullinfovalsarr=[]
#        for cnt, imnum in enumerate(selectlist):
#            fullinfovalsarr+=[infovalsarr[cnt]]*len(qindarr)
#            if data is None:
#                data=counts[imnum, qindarr]
#            else:
#                data=numpy.append(data, counts[imnum, qindarr])
#        fullinfovalsarr=numpy.float32(fullinfovalsarr)
#        fullqindarr=numpy.float32(list(qindarr)*len(selectlist))
#xrdUI.py
#        interpolator=scipy.interpolate.interp2d(fullqindarr,fullinfovalsarr,data)#flattened since not regular. x interpolation in indeces and y in actual values
#
#        plotdata=interpolator(qindarr, infovalsarr_interpto)

#        print infovalsarr_interpto
#        print self.infovalsarr
#        print 'raw', counts[:,0]




#on 17Mar2009 discover problem with Hanjong's BiTiO sample where if interp vs x or z the interp uses the 1st value at a given q for all of info axis. Plotting vs IND is ok and plotting vs -x or -z is ok. But reversing the infovals doesnt change anything. the below sorting solved the problem for some unknown reason
        sortmap=numpy.argsort(self.infovalsarr)
        self.infovalsarr=self.infovalsarr[sortmap]
        normarray=normarray[sortmap]
        counts=counts[sortmap]

        if self.interpCheckBox.isChecked():
            plotdata=numpy.float32([scipy.interp(infovalsarr_interpto, self.infovalsarr, arr/normarray) for arr in counts.T]).T
        else:
            cl=[numpy.argmin((self.infovalsarr-iv)**2) for iv in infovalsarr_interpto]
            plotdata=numpy.float32([counts[c]/normarray[c] for c in cl])

        infoplotindeces=scipy.interp(self.infovalsarr, infovalsarr_interpto, numpy.float32(range(len(infovalsarr_interpto))))#need to plot in indeces since plotting over imshow so use the full interpolated grid with its indeces to figure out where the original data will lie

        cmap=self.getcmap()
        print cmap
        self.plotw.axes.hold(False)
        if self.logCheckBox.isChecked():
            plotdata[plotdata<self.logcutSpinBox.value()]=self.logcutSpinBox.value()
            if (plotdata<=0).sum()==0:
                plotdata=numpy.log10(plotdata+1)
            else:
                print 'log not taken because there is data <=0'

        self.plotw.performplot(plotdata, upperorigin=False, cmap=cmap, aspect=.75*qindarr.size/infovalsarr_interpto.size)

        self.plotw.axes.hold(True)

        if self.datamarkerCheckBox.isChecked():
            marks=([-0.5]*len(infoplotindeces), infoplotindeces)
            styletext=unicode(self.datamarkerstyleLineEdit.text())
            self.plotw.axes.plot(marks[0],marks[1], styletext[:2], markersize=eval(styletext[2:]))

        if self.plotpeaksCheckBox.isChecked() and not self.chidrawbool:
            peakqplotindlist=[]
            peakinfoplotindlist=[]
            selectlist
            for peakind, infoplotind in zip(selectlist[sortmap], infoplotindeces):
                qvalarray, garb, garb=peakinfo_pksavearr(pkcounts[peakind])
                qplotind=ind_qgrid_q(qgrid, qvalarray, fractional=True)-qindexmin #this is based on qindarr=numpy.uint16(range(qindexmin, qindexmax+1))
                maxallowed=qindarr.size-1
                qplotind=qplotind[(qplotind>=0)&(qplotind<=maxallowed)]

                peakinfoplotindlist+=[infoplotind]*qplotind.size
                peakqplotindlist+=list(qplotind)

            styletext=unicode(self.peaksstyleLineEdit.text())
            self.plotw.axes.plot(peakqplotindlist,peakinfoplotindlist, styletext[:2],markersize=eval(styletext[2:]))
            print '$', qvalarray
            print '@', ind_qgrid_q(qgrid, qvalarray, fractional=True)-qindexmin
            print '^', peakqplotindlist
            print '%', peakinfoplotindlist
            print '*1',self.qgrid
        #plot PDF lines
        pdfinfostr=str(self.pdfplotinfoLineEdit.text())
        if len(pdfinfostr.strip())>0:
            #try:
            pdfymin, pdfymax, pdfcolstr, lwstr=[s.strip() for s in pdfinfostr.split(',')]
            pdfrange=numpy.float32([pdfymin, pdfymax])
            pdfrangeind=scipy.interp(pdfrange, infovalsarr_interpto, numpy.float32(range(len(infovalsarr_interpto))))
            h=[]
            pdfqlist=[]
            for d, height in self.pdfentry:
                h+=[height]
                pdfqlist+=[d]
            h=numpy.float32(h)
            h/=h.max()
            pdfqlist=numpy.float32(pdfqlist)
            pdfqindlist=ind_qgrid_q(qgrid, pdfqlist, fractional=True)-qindexmin
            pdflwlist=eval(lwstr)#which may contain the variable 'h' which will be the relative peak height
            if not isinstance(pdflwlist, numpy.ndarray):
                pdflwlist=pdflwlist*numpy.ones(pdfqlist.shape)
            for pdfqind, pdflw in zip(pdfqindlist, pdflwlist):
                self.plotw.axes.plot([pdfqind, pdfqind], pdfrangeind, pdfcolstr, linewidth=pdflw)
            #except:
                #print 'ERROR IN PLOTTING PDF LINES!!'

        qlabelind=numpy.uint16(range(5))*(len(qindarr)-1)//4.0
        qlabels=['%.2f' %q_qgrid_ind(qgrid, qindarr[i]) for i in qlabelind]
        self.plotw.axes.set_xticks(qlabelind)
        self.plotw.axes.set_xticklabels(qlabels)
        if self.chidrawbool or 'tex' in self.type:
            self.plotw.axes.set_xlabel('fiber texture angle (deg)')
        else:
            self.plotw.axes.set_xlabel('scattering vector (1/nm)')

        ylabelind=numpy.uint16(range(5))*(len(infovalsarr_interpto)-1)//4.0
        ylabels=['%.2f' %infovalsarr_interpto[i] for i in ylabelind]
        self.plotw.axes.set_yticks(ylabelind)
        self.plotw.axes.set_yticklabels(ylabels)
        self.plotw.axes.set_ylabel(str(self.YlabelLineEdit.text()))

        self.plotw.axes.set_xlim([-0.5, plotdata.shape[1]+0.5])
        self.plotw.axes.set_ylim([-0.5, plotdata.shape[0]+0.5])

        self.chidrawbool=False

        self.plotw.fig.canvas.draw()
        self.plotw.axes.hold(False)

    def pdfsetup(self):
        if 'h5tex' in self.type:
            idialog=pdfDialog(self, filename='TextureDatabase.txt', cvtfcn=lambda x:x)
        else:
            idialog=pdfDialog(self)
        if idialog.exec_():
            #label=unicode(idialog.labellineEdit.text())
            self.pdfentry=idialog.pdflist[idialog.pdfcomboBox.currentIndex()]
            colstr=unicode(idialog.colorlineEdit.text())
            if colstr=='':
                colstr='k:'
            lwstr='4*h'
            rangestr=`self.YinfominSpinBox.value()`+','+`self.YinfomaxSpinBox.value()`
            self.pdfplotinfoLineEdit.setText(','.join((rangestr, colstr, lwstr)))

    def picclickprocess(self, picnum):
        picname='%d' %picnum

        selectlist=sorted(list(set(self.getselectlist()+[picnum])))

        newimlist=''
        for pointind in selectlist:
            newimlist+=',%d' %pointind

        self.selectedimagesTextBrowser.setPlainText(newimlist[1:])
        self.navw.plotpoints(self.pointlist, [], selectlist)
        self.navw.fig.canvas.draw()

    def tooltips(self):
        try:
            self.xrdtypeComboBox.setToolTip('choose name of dataset to be plotted')
        except:
            None

        try:
            self.peaksstyleLineEdit.setToolTip('matplotlib style string without quotation\nmarks, e.g. <color><pointstyle><linestyle>')
        except:
            None

        try:
            self.datamarkerCheckBox.setToolTip('matplotlib stytle string for markers\nthat will appear on the y-axis to denote\nthe positions of data')
        except:
            None

        try:
            self.xrdtypeLabel.setToolTip('')
        except:
            None

        try:
            self.plotxzCheckBox.setToolTip('')
        except:
            None

        try:
            self.xzstyleLineEdit.setToolTip('matplotlib style string for\nplots of Xinfo vs Yinfo')
        except:
            None

        try:
            self.datastyleLineEdit.setToolTip('matplotlib style string')
        except:
            None

        try:
            self.cmapLineEdit.setToolTip('any cmap name from matplotlib.cm\ndefault is jet')
        except:
            None

        try:
            self.pdfplotinfoLineEdit.setToolTip('ymin and ymax are numeric values of\nthe y-axis over which the PDF lines will\nbe plotted. colstr is the matplotlib color character,\nlinew is the width of the PDF lines and the character\n"h" can be used to represent the peak height so that the\nline width can be made proportional to the peak height.')
        except:
            None

        try:
            self.interpCheckBox.setToolTip('if unchecked, the number of "pixels" in\nthe y-direction will be "numy Y info pts",\nif unchecked there will be one pixel for each datapoint')
        except:
            None

        try:
            self.logCheckBox.setToolTip('the false color scale will be\nlogarithmic and the numbers in the\ncolorbar will be the log10 values')
        except:
            None

        try:
            self.logcutSpinBox.setToolTip('everything below this value\nwill be set to this value')
        except:
            None

        try:
            self.cmaponethirdSpinBox.setToolTip('if this value is smaller (larger) than .33,\nthe bottom third of the cmap color range will\nbe shrunk (expanded). if the colorbar does\nnot change as you expect, try closing and\nreopening this window.')
        except:
            None

        try:
            self.YinfominSpinBox.setToolTip('The min and max values will become\nthe limits of the plot axis. In some cases,\nthe range cannot extend beyond the available data\nbut sometimes that is fine.')
        except:
            None

        try:
            self.XinfominSpinBox.setToolTip('The min and max values will become\nthe limits of the plot axis. In some cases,\nthe range cannot extend beyond the available data\nbut sometimes that is fine.')
        except:
            None

        try:
            self.clearplotsButton.setToolTip('The main image will be plotted over\nolder images, but any symbols\nwill cummulate with repeated plotting commands.\nPress this to clear everything')
        except:
            None

        try:
            self.imgLabel.setToolTip('will appear in filename of saved figure\n(AVOID ILLEGAL CHARACTERS)')
        except:
            None

        try:
            self.InfoTextBrowser.setToolTip('')
        except:
            None

        try:
            self.YInfoMathTextBrowser.setToolTip('This string can contain math commands and the\nkeys indicates in the list to the left\n(capital letters for the corresponding sample\ninfo and IND for the spec index. For example,\n"IND*numpy.sqrt(B**2+A**2)"')
        except:
            None

        try:
            self.XInfoMathTextBrowser.setToolTip('')
        except:
            None

        try:
            self.spdshFormatLineEdit.setToolTip('The expression will be evaluated and the numeric\nresults will be pu into the spreadhseet string\nusing this Python number->string conversion code')
        except:
            None

        try:
            self.selectedimagesTextBrowser.setToolTip('When the expressions in the below fields are evaluated,\nonly the spec indeces included in this comma-delimited\nlist will be used. You can delete indeces by removing\nthe text or "parse pts, avoid NaN" which will evaluate\nthe expressions and remove the indeces that yielded a NaN\nresult. You can add indeces by typing the numbers,\nclicking the navigator, or "include all points"')
        except:
            None

        try:
            self.peakextractqminSpinBox.setToolTip('The center of the Q-window used for gathering fiber\ntexture data will be the position of the largest\n(biggest "height" value) peak in the range of Q values\nspecified here.')
        except:
            None

        try:
            self.chiqwidthCheckBox.setToolTip('Select whether to use the specified Q-width\nfor every spec index or to use the specifiec\nnumber of HWHM from the curve fitting')
        except:
            None

        try:
            self.chiqwidthSpinBox.setToolTip('This is a half-interval of Q for the texture or\na number of half-widths of the identified Bragg peak -\nthis determines the Q-window used in the\ntexture calculation')
        except:
            None

        try:
            self.chiminSpinBox.setToolTip('The PSI range over which the texture will\nbe analyzed is specified here. This will\ndefault to the range indicate by measurement grid,\nbut for a given Q-range the PSI-range may be smaller.\nIf the specified range reaches beyond the data, the texture\nresults in the non-existent range will be NaN')
        except:
            None

        try:
            self.fulltexplotComboBox.setToolTip('The sides of the detector can be analyzed\nseparately or avergaed together (only average if\nyou know the symmetry is near perfect).')
        except:
            None

        try:
            self.interpchiCheckBox.setToolTip('If unchecked the pixel width in the PSI-axis will\nbe the spacing in the PSI measurement grid, if check\ninterpolation will be used to make a smoother image.')
        except:
            None

        try:
            self.normchivalsCheckBox.setToolTip('')
        except:
            None

        try:
            self.texturesaveLineEdit.setToolTip('This will be the name of the\ntexture group in the .h5 file.')
        except:
            None
    
    def includeallimages(self):
        newimlist=''
        for pointind in self.pointlist:
            newimlist+=',%d' %pointind

        self.selectedimagesTextBrowser.setPlainText(newimlist[1:])

        self.navw.plotpoints(self.pointlist, [])
        self.navw.fig.canvas.draw()

    def save(self):
        self.plotw.save(os.path.join(self.runpath, ''.join((self.savename1, unicode(self.imgLabel.text())))).replace('\\','/').encode())

    def savenavimage(self):
        self.navw.save(os.path.join(self.runpath, ''.join((self.savename1, '_2DIntPlotPoints', unicode(self.imgLabel.text())))).replace('\\','/').encode())

    def getcmap(self):
        try:
            cmap=eval('matplotlib.cm.'+str(self.cmapLineEdit.text()))
            initvals=numpy.arange(256)
            rgblist=cmap(initvals)[:, :3]
        except:
            initvals=numpy.array([0, 0.333, .666, 1.0])
            rgblist=numpy.array([[0,.1,0],[.3,.4,.33],[.6,.7,.66],[.9,1.0,1.0]])
        inds=numpy.arange(initvals.size)/(initvals.size-1.0)
        interppoints=numpy.arange(4)/(3.0)
        interpvals=numpy.array([0.0, self.cmaponethirdSpinBox.value(), self.cmaptwothirdsSpinBox.value(),  1.0])
        stretchedvals=numpy.interp(inds, interppoints, interpvals)
        cdict=dict(red=[], green=[], blue=[])
        for v,col in zip(stretchedvals,rgblist):
            r,g,b=col
            cdict['red'].append((v, r, r))
            cdict['green'].append((v, g, g))
            cdict['blue'].append((v, b, b))
        return matplotlib.colors.LinearSegmentedColormap('mycolors', cdict)

    def substrateinfoplot(self):
        if not len(self.attrdict['acquisition_shape'])!=2:
            print 'ABORTING PLOT: ONLY SUPPORT FOR MESH' # if support for linear scans is added, the 'USER-COMPILED' cases need special treatment as xgrid and zgrid are meaningless
            return

        selectlist=numpy.uint16(self.getselectlist())
        valarr=self.CalculateInfoVals(str(self.YInfoMathTextBrowser.toPlainText()), selectlist)
        xarr=self.sampleinfo['x(mm)'][selectlist]
        zarr=self.sampleinfo['z(mm)'][selectlist]

        #ylim=self.plotw.axes.get_ylim()
        #xlim=self.plotw.axes.get_xlim()

        self.plotw.axes.hold(False)

        x_interpto=numpy.linspace(xarr.min(), xarr.max(), self.xgrid[2])
        z_interpto=numpy.linspace(zarr.min(), zarr.max(), self.zgrid[2])

        interpolator=scipy.interpolate.interp2d(xarr, zarr, valarr)#flattened since not regular. x interpolation in indeces and y in actual values
        plotdata=interpolator(x_interpto, z_interpto)

        self.plotw.performplot(plotdata, upperorigin=True, cmap=str(self.cmapLineEdit), extent=(xarr.min(), xarr.max(), zarr.min(), zarr.max()))

        #self.plotw.axes.set_ylim(ylim)
        #self.plotw.axes.set_xlim(xlim)

        self.plotw.axes.hold(True)

        if self.plotxzCheckBox.isChecked():
            self.plotw.inmark=str(self.xzstyleLineEdit)
            plotpts=selectlist
        else:
            plotpts=[]
        self.plotw.plotpoints(self.pointlist, [], plotpts) #this include plotting circle and formatting axis
        self.plotw.fig.canvas.draw()

    def SaveSpreadSheet(self):
        f=open(os.path.join(self.runpath, str(self.spdshsavenameLineEdit.text())).replace('\\','/').encode(), 'w')
        f.write(str(self.spdshTextBrowser.toPlainText()))
        f.close()

    def xyplotsave(self):
        if self.interpstyle:
            temp='_extractedpeaks'
        elif self.infostyle:
            temp='_'+str(self.YlabelLineEdit.text())+'vs'+str(self.XlabelLineEdit.text())
        self.chipeakorinfoplotw.save(os.path.join(self.runpath, ''.join((self.savename1, unicode(self.imgLabel.text()), temp))).replace('\\','/').encode())

    def xyinfoplot(self):
        selectlist=numpy.uint16(self.getselectlist())
        yarr=self.CalculateInfoVals(str(self.YInfoMathTextBrowser.toPlainText()), selectlist)
        xarr=self.CalculateInfoVals(str(self.XInfoMathTextBrowser.toPlainText()), selectlist)

        datastylestr=str(self.datastyleLineEdit.text())
        stylelist=[]
        while ',' in datastylestr:
            temp, garbage, datastylestr=datastylestr.partition(',')
            temp.replace(' ', '')
            datastylestr.replace(' ', '')
            stylelist+=[temp]
        datastylestr.replace(' ', '')
        stylelist+=[datastylestr]
        self.chipeakorinfoplotw.axes.hold(self.xyplotoverlayCheckBox.isChecked())
        for style in stylelist:
            #self.chipeakorinfoplotw.performplot([xarr, yarr], overlay=True, axesformat='', formstr=style)
            self.chipeakorinfoplotw.axes.plot(xarr, yarr, style)
            self.chipeakorinfoplotw.axes.hold(True)


        self.chipeakorinfoplotw.axes.set_ylabel(str(self.YlabelLineEdit.text()))
        self.chipeakorinfoplotw.axes.set_xlabel(str(self.XlabelLineEdit.text()))

        self.chipeakorinfoplotw.axes.set_ylim([self.YinfominSpinBox.value(), self.YinfomaxSpinBox.value()])
        self.chipeakorinfoplotw.axes.set_xlim([self.XinfominSpinBox.value(), self.XinfomaxSpinBox.value()])
        self.chipeakorinfoplotw.fig.canvas.draw()

    def Ygetinfominmax(self):
        selectlist=numpy.uint16(self.getselectlist())
        if len(selectlist)==0:
            return
        infovalsarr=self.CalculateInfoVals(str(self.YInfoMathTextBrowser.toPlainText()), selectlist)

        self.YinfominSpinBox.setValue(numpy.min(infovalsarr))
        self.YinfomaxSpinBox.setValue(numpy.max(infovalsarr))

    def Xgetinfominmax(self):
        selectlist=numpy.uint16(self.getselectlist())
        if self.interpstyle:
            h5file=h5py.File(self.h5path, mode='r')
            datatypestr=unicode(self.xrdtypeComboBox.currentText())
            if datatypestr=='ifcounts':
                counts=readh5pyarray(h5file[self.h5datagrpstr]['ifcounts'])[selectlist]
            else:
                counts=readh5pyarray(h5file[self.h5datagrpstr]['icounts'])[selectlist]

            notnanbool=numpy.bool_([numpy.logical_not(numpy.any(numpy.bool_(numpy.isnan(arr)))) for arr in counts.T])
            self.XinfominSpinBox.setValue(numpy.min(self.qvals[notnanbool]))
            self.XinfomaxSpinBox.setValue(numpy.max(self.qvals[notnanbool]))
            h5file.close()
        elif self.infostyle:
            if len(selectlist)==0:
                return
            infovalsarr=self.CalculateInfoVals(str(self.XInfoMathTextBrowser.toPlainText()), selectlist)

            self.XinfominSpinBox.setValue(numpy.min(infovalsarr))
            self.XinfomaxSpinBox.setValue(numpy.max(infovalsarr))

    def CalculateInfoVals(self, mathstr, pts):
        if mathstr=='':
            return numpy.ones(len(pts), dtype='float32')
        pts=numpy.uint16(pts)
        mathstr=mathstr.replace('IND', 'numpy.float32(pts)')
        d=self.allinfodict
        for vc in d.keys():
            mathstr=mathstr.replace(vc,"d['%s'][pts]" %vc)
        print 'Calculating: ', mathstr
        try:
            arr=eval(mathstr)
            return arr
        except:
            print 'ERROR IN INFO CALCULATION - using ones'
            return numpy.ones(len(pts), dtype='float32')


    def getselectlist(self):
        imlist=unicode(self.selectedimagesTextBrowser.toPlainText())
        selectlist=[]
        while len(imlist.partition(',')[0])>0:
            numstr, garb, imlist=imlist.partition(',')
            selectlist+=[eval(numstr)]
        if len(selectlist)==0:
            print 'WARNING. no slected images'
            return []
        return sorted(list(set(selectlist)))

    def AppendToSpreadSheet(self, mathstr, label=''):
        selectlist=self.getselectlist()
        if len(selectlist)==0:
            print 'ABORTING: no indeces selected'
            return
        if len(self.spdshselectlist)>0 and selectlist!=self.spdshselectlist:
            print 'ABORTING: cannot append to spreadsheet because the select index set is different'
            return
        if len(self.spdshselectlist)==0:
            temp=['SpecInd']+[`int(round(i))` for i in selectlist]
            self.spdshTextBrowser.setPlainText('\n'.join(temp))
            self.spdshselectlist=selectlist
        arr=self.CalculateInfoVals(mathstr, selectlist)
        fs='%'+str(self.spdshFormatLineEdit.text())
        temp=[label]+[fs %val for val in arr]
        lines=str(self.spdshTextBrowser.toPlainText()).splitlines()
        for i, st in enumerate(temp):
            lines[i]+='\t%s' %st
        self.spdshTextBrowser.setPlainText('\n'.join(lines))


    def ClearSpreadSheet(self):
        self.spdshselectlist=[]
        self.spdshTextBrowser.setPlainText('')


    def YappendSpreadSheet(self):
        self.AppendToSpreadSheet(str(self.YInfoMathTextBrowser.toPlainText()), str(self.YlabelLineEdit.text()))

    def XappendSpreadSheet(self):
        self.AppendToSpreadSheet(str(self.XInfoMathTextBrowser.toPlainText()), str(self.XlabelLineEdit.text()))

    def ParseIndAvoidNaN(self):
        selectlist=numpy.uint16(self.getselectlist())
        yarr=self.CalculateInfoVals(str(self.YInfoMathTextBrowser.toPlainText()), selectlist)
        xarr=self.CalculateInfoVals(str(self.XInfoMathTextBrowser.toPlainText()), selectlist)
        selectlist=selectlist[numpy.logical_not(numpy.isnan(yarr)) & numpy.logical_not(numpy.isnan(xarr))]
        newimlist=''
        for pointind in selectlist:
            newimlist+=',%d' %pointind

        self.selectedimagesTextBrowser.setPlainText(newimlist[1:])

        self.navw.plotpoints(self.pointlist, [], selectlist)
        self.navw.fig.canvas.draw()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

class neighborwindow(QDialog):
    def __init__(self, parent, h5path, h5groupstr, runpath):
        super(neighborwindow, self).__init__(parent)
        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.runpath=runpath
        self.savename1='_'.join((os.path.split(self.h5path)[1][0:-3], self.h5groupstr, ''))
        self.imnamelist=[]

        h5file=h5py.File(self.h5path, mode='r')
        h5analysis=h5file['/'.join((h5groupstr, 'analysis'))]

        self.attrdict=getattr(self.h5path, self.h5groupstr)
        self.bin=getbin(h5analysis)
        
        self.pointlist=self.attrdict['pointlist']
        elstr=self.attrdict['elements']

        self.DPelstrlist, self.DPcompsarr=(None, None)
        #using only tenrary compositions!
        if 'depprof' in h5analysis:
            self.DPelstrlist, self.DPcompsarr=getternarycomps(self.h5path, self.h5groupstr, elstr=elstr, infotype='DPmolfracALL')
        self.XRFelstrlist, self.XRFcompsarr=(None, None)
        if 'xrf' in h5analysis:
            self.XRFelstrlist, self.XRFcompsarr=getternarycomps(self.h5path, self.h5groupstr, elstr=elstr, infotype='XRFmolfracALL')

        h5file.close()



        self.xgrid=self.attrdict['xgrid']
        self.zgrid=self.attrdict['zgrid']
        self.xcoords=self.attrdict['x']
        self.zcoords=self.attrdict['z']
        self.typeComboBox=QComboBox()

        self.compnavw=None
        if not self.DPcompsarr is None:
            self.compnavw = compnavigatorwidget(self, self.DPcompsarr, self.DPelstrlist)
            self.typeComboBox.insertItem(999, 'COMP:DepProf with '+','.join(self.DPelstrlist))
        elif not self.XRFcompsarr is None:
            self.compnavw = compnavigatorwidget(self, self.XRFcompsarr, self.XRFelstrlist)
        if not self.XRFcompsarr is None:
            self.typeComboBox.insertItem(999, 'COMP:XRF with '+','.join(self.XRFelstrlist))

        self.posnnavw = subnavigatorwidget(self, self.xgrid, self.zgrid, self.xcoords, self.zcoords)
        self.typeComboBox.insertItem(999, 'POSITION')

        #QObject.connect(self.navw, SIGNAL("picclicked"), self.picclickprocess)

        #QObject.connect(self.typeComboBox,SIGNAL("currentIndexChanged()"),self.typechanged)
        QObject.connect(self.typeComboBox,SIGNAL("activated(QString)"),self.typechanged)

        self.typeLabel=QLabel()
        self.typeLabel.setText('type of data for\nneighbor calc')

        self.dlnyCheckBox=QCheckBox()
        self.dlnyCheckBox.setText('Use Delaunay Triangulation')
        self.dlnyCheckBox.setChecked(True)

        self.setWindowTitle('Calculate and plot map of data point neighbor')

        self.calcButton=QPushButton()
        self.calcButton.setText('calculate neighbors')
        QObject.connect(self.calcButton,SIGNAL("pressed()"),self.neighborcalc)

        self.saveButton=QPushButton()
        self.saveButton.setText('save neighbors\nfor analysis')
        QObject.connect(self.saveButton,SIGNAL("pressed()"),self.saveneigh)

        self.saveposnnavimageButton=QPushButton()
        self.saveposnnavimageButton.setText('save .png\npositions')
        QObject.connect(self.saveposnnavimageButton,SIGNAL("pressed()"),self.saveposnnavimage)

        self.savecompnavimageButton=QPushButton()
        self.savecompnavimageButton.setText('save .png\ncompositions')
        QObject.connect(self.savecompnavimageButton,SIGNAL("pressed()"),self.savecompnavimage)

        self.radiusLabel=QLabel()
        self.radiusLabel.setText('radius for neighbor\nassociation, at.frac or mm')
        self.radiusSpinBox=QDoubleSpinBox()
        self.radiusSpinBox.setRange(0, 999.)
        self.radiusSpinBox.setValue(.15)


        layout=QGridLayout()

        layout.addWidget(self.radiusLabel, 1, 0, 1, 1)
        layout.addWidget(self.radiusSpinBox, 2, 0, 1, 1)
        layout.addWidget(self.typeLabel, 3, 0, 1, 1)
        layout.addWidget(self.typeComboBox, 4, 0, 1, 1)
        layout.addWidget(self.dlnyCheckBox, 5, 0, 1, 1)
        layout.addWidget(self.calcButton, 6, 0, 1, 1)
        layout.addWidget(self.saveButton, 7, 0, 1, 1)

        layout.addWidget(self.saveposnnavimageButton, 0, 4, 1, 1)
        layout.addWidget(self.posnnavw, 1, 1, 8, 4)
        self.posnnavw.plotpoints(self.pointlist, [])
        if not self.compnavw is None:
            layout.addWidget(self.savecompnavimageButton, 0, 8, 1, 1)
            layout.addWidget(self.compnavw, 1, 5, 8, 4)
            self.compnavw.plotpoints(self.pointlist, [])

        self.setLayout(layout)
        self.neighbors=None
        self.typeComboBox.setCurrentIndex(0)


    def typechanged(self, garbage):
        typestr=unicode(self.typeComboBox.currentText())
        if 'COMP' in typestr:
            if 'DepProf' in typestr:
                self.compnavw.reinit(comp=self.DPcompsarr, elstrlist=self.DPelstrlist)
            elif 'XRF' in typestr:
                self.compnavw.reinit(comp=self.XRFcompsarr, elstrlist=self.XRFelstrlist)
            self.compnavw.fig.canvas.draw()


    def neighborcalc(self):
        self.usedlny=self.dlnyCheckBox.isChecked()
        self.critdist=self.radiusSpinBox.value()
        self.typestr=unicode(self.typeComboBox.currentText())
        if 'COMP' in self.typestr:
            if 'DepProf' in self.typestr:
                if self.usedlny:
                    self.neighbors=findcompnieghbors(self.DPcompsarr, pointlist=self.pointlist)
                else:
                    self.neighbors=findneighborswithinradius(compdistarr_comp(self.DPcompsarr), self.critdist, pointlist=self.pointlist)
            elif 'XRF' in self.typestr:
                if self.usedlny:
                    self.neighbors=findcompnieghbors(self.XRFcompsarr, pointlist=self.pointlist)
                else:
                    self.neighbors=findneighborswithinradius(compdistarr_comp(self.XRFcompsarr), self.critdist, pointlist=self.pointlist)
        elif 'POSITION' in self.typestr:
            if self.usedlny:
                self.neighbors=findposnnieghbors(self.xcoords, self.zcoords, pointlist=self.pointlist, critdist=self.critdist)
            else:
                dist=numpy.sqrt(numpy.add.outer(self.xcoords, -1.0*self.xcoords)**2+numpy.add.outer(self.zcoords, -1.0*self.zcoords)**2)
                self.neighbors=findneighborswithinradius(dist, self.critdist, pointlist=self.pointlist)

        print 'Neighbors'
        print self.neighbors
        if not self.neighbors is None:
            self.posnnavw.reinit()
            self.compnavw.reinit()
            self.posnnavw.plotneighbors(self.neighbors)
            self.compnavw.plotneighbors(self.neighbors)
            self.posnnavw.fig.canvas.draw()
            self.compnavw.fig.canvas.draw()

    def saveneigh(self):
        if self.neighbors is None:
            QMessageBox.warning(self,"failed",  'Neighbors have not been successfully calculated')
        else:
            pardict={}
            pardict['calctype']=str(self.typestr)
            pardict['critdist']=self.critdist
            if self.usedlny:
                pardict['dlny']=1
            else:
                pardict['dlny']=0
            saveneighbors(self.h5path, self.h5groupstr, self.neighbors, pardict)

    def savecompnavimage(self):
        self.compnavw.save(os.path.join(self.runpath, ''.join((self.savename1, '_NeighborComposition')).replace('\\','/').encode()))
    def saveposnnavimage(self):
        self.posnnavw.save(os.path.join(self.runpath, ''.join((self.savename1, '_NeighborPosition')).replace('\\','/').encode()))

class plot2dchessrunwindow(QDialog):
    def __init__(self, parent, path, runpath):
        super(plot2dchessrunwindow, self).__init__(parent)
        self.path=path
        self.runpath=runpath


        self.savename1=os.path.split(self.path)[1][0:-2]

        h5chessrun=h5py.File(self.path, mode='r')
        self.treeWidget=QTreeWidget()
        self.rootitem=QTreeWidgetItem([os.path.split(self.path)[1]],  0)
        self.treeWidget.addTopLevelItem(self.rootitem)
        self.createTree(h5chessrun, self.rootitem)
        h5chessrun.close()

        self.logCheckBox=QCheckBox()
        self.logCheckBox.setText('logarithmic\nintensity')
        self.logCheckBox.setChecked(False)

        self.drawButton=QPushButton()
        self.drawButton.setText('draw image')
        QObject.connect(self.drawButton,SIGNAL("pressed()"),self.draw)
        self.saveButton=QPushButton()
        self.saveButton.setText('save .png')
        QObject.connect(self.saveButton,SIGNAL("pressed()"),self.save)


        rangelayout=QVBoxLayout()
        rangelabel=QLabel()
        rangelabel.setText('Range for cbar:')
        self.rangeLineEdit=QLineEdit()
        rangelayout.addWidget(rangelabel)
        rangelayout.addWidget(self.rangeLineEdit)

        cmaplayout=QVBoxLayout()
        cmaplabel=QLabel()
        cmaplabel.setText('cmap:')
        self.cmapLineEdit=QLineEdit()
        self.cmapLineEdit.setText('jet')
        cmaplayout.addWidget(cmaplabel)
        cmaplayout.addWidget(self.cmapLineEdit)

        toplayout=QHBoxLayout()
        toplayout.addWidget(self.drawButton)
        toplayout.addLayout(cmaplayout)
        toplayout.addLayout(rangelayout)
        toplayout.addWidget(self.logCheckBox)
        toplayout.addWidget(self.saveButton)

        self.plotw = plotwidget(self, width=5, height=5, dpi=100)

        layout=QGridLayout()
        layout.addLayout(toplayout, 1, 1, 1, 10)

        layout.addWidget(self.treeWidget, 2, 1, 10, 4)
        layout.addWidget(self.plotw, 2, 5, 10, 6)
        self.setLayout(layout)


    def createTree(self, startnode, parentitem):
        #print startnode
        #print startnode.listobjects()
        for node in startnode.iterobjects():
            if isinstance(node, h5py.Dataset) and len(node.shape)==2:
                item=QTreeWidgetItem([node.name.rpartition('/')[2]+`node.shape`],  0)
                parentitem.addChild(item)
            elif isinstance(node, h5py.Group):
                item=QTreeWidgetItem([node.name.rpartition('/')[2]],  0)
                parentitem.addChild(item)
                self.createTree(node,  item)

    def draw(self):
        items=self.treeWidget.selectedItems()
        if len(items)==0:
            return
        item=items[0]
        if not '(' in str(item.text(0)):
            return
        h5grpstr=''
        childname=''
        while item!=self.rootitem:
            name=str(item.text(0))
            if '(' in name:
                name=name.partition('(')[0]
            if childname=='':
                childname=name
            h5grpstr='/'.join((name, h5grpstr))
            item=item.parent()
        h5grpstr=h5grpstr[:-1]
        self.arrname='_'.join((name, childname)) #name will be the chessrun name
        h5chessrun=h5py.File(self.path, mode='r')
        plotarr=readh5pyarray(h5chessrun[h5grpstr])
        h5chessrun.close()

        rangestr=unicode(self.rangeLineEdit.text())
        try:
            range=eval(rangestr)
            if isinstance(range,(int,float)):
                range=(0., 1.*range)
            if len(range)==1:
                range=(0., range[0])
        except:
            range=None

        self.plotw.performplot(plotarr, log=self.logCheckBox.isChecked(), colrange=range)

    def save(self):
        self.plotw.save(os.path.join(self.runpath, ''.join((self.savename1, self.arrname))).replace('\\','/').encode())


class buildnewscanDialog(QDialog,
        ui_buildnewscan.Ui_buildnewscanDialog):
    #in order to get here, h5path and groupstr exist and analysis has been started. can replace images and a new scan will be created with the images replaced in the XRD and XRF data as well as in the analysis attrdict, but the x,z coordinates of the original scan are maintained. Can also append data from otehr scans. in this case, even if the set of x,z would coincide with a spec command, the command becomes 'USER-COMPILED' and is treated as a a sort of a2scan with arbitrary 1-D path.
    def __init__(self, parent, h5path, h5groupstr):
        super(buildnewscanDialog, self).__init__(parent)
        self.setupUi(self)
        self.h5path=h5path

        self.copygroupindex=0
        self.validgrp_name=[]
        self.validgrp_attr=[]
        self.copyable_validgrpind=[]# a list of the indeces of validgrp_ that can be copied from
        h5file=h5py.File(self.h5path, mode='r')
        detectors=[]
        for group in h5file.iterobjects():
            if isinstance(group,h5py.Group) and 'analysis' in group:
                detectors=[getxrdname(group['analysis'])]
        if len(detectors)==0:
            h5chess=CHESSRUNFILE()
            detectors=h5chess.attrs['DetectorNames']
            h5chess.close()
        count=0
        for group in h5file.iterobjects():
            if isinstance(group,h5py.Group) and ('measurement' in group) and (True in [dn in group['measurement'] for dn in detectors]):
                grpname=group.name.rpartition('/')[2]
                self.validgrp_name+=[grpname]
                if ('analysis' in group and getxrdname(group['analysis']) in group['analysis']):
                    self.copyable_validgrpind+=[count]
                    self.validgrp_attr+=[copy.deepcopy(getattr(self.h5path, grpname))]
                else:


                    temp_acsh=group.attrs['acquisition_shape']
                    if isinstance(temp_acsh, str):
                        temp_acsh=eval(temp_acsh)
                    npts=numpy.prod(numpy.int16(temp_acsh))

                    samx=None
                    samz=None
                    if 'samx' in group['measurement/scalar_data']:
                        samx=group['measurement/scalar_data/samx'][:]
                    if 'samz' in group['measurement/scalar_data']:
                        samz=group['measurement/scalar_data/samz'][:]

                    if samx is None:
                        samx=numpy.ones(npts, dtype='float32')*group['measurement/positioners/samx'].value
                    if samz is None:
                        samz=numpy.ones(npts, dtype='float32')*group['measurement/positioners/samz'].value

                    tempd={}
                    tempd['x']=samx
                    tempd['z']=samz
                    tempd['command']=group.attrs['acquisition_command']
                    self.validgrp_attr+=[copy.deepcopy(tempd)]
                if grpname==h5groupstr:
                    self.copygroupindex=count
                count+=1

        h5file.close()

        QObject.connect(self.copynameComboBox,SIGNAL("activated(QString)"),self.fillreplaceimageComboBox)
        QObject.connect(self.replaceimageComboBox,SIGNAL("activated(QString)"),self.fillnewimageComboBox)
        QObject.connect(self.radiusSpinBox,SIGNAL("valueChange(int)"),self.fillnewimageComboBox)

        self.initcomboboxes()

    def initcomboboxes(self):
        self.copynameComboBox.clear()
        self.appendnameComboBox.clear()
        for count, ind in enumerate(self.copyable_validgrpind):
            self.copynameComboBox.insertItem(count, ':'.join((self.validgrp_name[ind], self.validgrp_attr[ind]['command'])))
        self.copynameComboBox.setCurrentIndex(self.copyable_validgrpind.index(self.copygroupindex))

        for count, (nam, d) in enumerate(zip(self.validgrp_name, self.validgrp_attr)):
            self.appendnameComboBox.insertItem(count, ':'.join((nam, d['command'])))
        self.appendnameComboBox.setCurrentIndex(0)
        self.fillreplaceimageComboBox()

    def fillreplaceimageComboBox(self):
        self.replaceimageComboBox.clear()
        self.copygroupindex=self.copyable_validgrpind[self.copynameComboBox.currentIndex()]
        attrdict=self.validgrp_attr[self.copygroupindex]
        for count in range(numpts_attrdict(attrdict)):
            self.replaceimageComboBox.insertItem(count, '%d' %count)
        self.replaceimageComboBox.setCurrentIndex(0)
        self.fillnewimageComboBox()

        self.replacelistLineEdit.setText('')
        self.newlistLineEdit.setText('')

    def fillnewimageComboBox(self):
        radius=self.radiusSpinBox.value()
        imind=self.replaceimageComboBox.currentIndex()
        x0=self.validgrp_attr[self.copygroupindex]['x'][imind]
        z0=self.validgrp_attr[self.copygroupindex]['z'][imind]
        possbielreplacements=[]
        for count, (nam, attr) in enumerate(zip(self.validgrp_name, self.validgrp_attr)):
            if count==self.copygroupindex:#do not allow replacements from within own scan - this could be achieved by user through a copy and then a copy+replace
                continue
            distsq=(numpy.float32(attr['x'])-x0)**2+(numpy.float32(attr['z'])-z0)**2
            possbielreplacements+=['%s:%d' %(nam, i) for i in numpy.where(distsq<radius**2)[0]]
        self.newimageComboBox.clear()
        for count, s in enumerate(possbielreplacements):
            self.newimageComboBox.insertItem(count, s)
        self.newimageComboBox.setCurrentIndex(0)


    @pyqtSignature("")
    def on_replacePushButton_clicked(self):
        self.appendcomboboxtolineedit(self.replacelistLineEdit, self.replaceimageComboBox)
        self.appendcomboboxtolineedit(self.newlistLineEdit, self.newimageComboBox)

    @pyqtSignature("")
    def on_appendPushButton_clicked(self):
        self.appendcomboboxtolineedit(self.appendlistLineEdit, self.appendnameComboBox)

    def lineedittolist(self, le):
        lestr=str(unicode(le.text()))
        strlist=[]
        lestr.strip()
        while len(lestr)>0:
            temp, garbage, lestr=lestr.partition(',')
            temp=temp.strip()
            if len(temp)>0:
                strlist+=[temp]
        return strlist

    def appendcomboboxtolineedit(self, le, cb):
        temp=str(unicode(le.text()))
        if temp!='':
            temp+=', '
        #temp+=str(unicode(cb.currentText())).partition(':')[0]
        temp+=str(unicode(cb.currentText()))
        le.setText(temp)

    def createnewscandict(self):
        newscandict={}
        sourcegrpname=str(unicode(self.copynameComboBox.currentText())).partition(':')[0]

        newscandict['sourcename']=sourcegrpname
        try:
            xrdname=self.validgrp_attr[self.validgrp_name.index(sourcegrpname)]['xrdname']
        except:
            print 'FAILED TO GET THE XRD DETECTOR NAME. EITHER THIS IS AN .h5 FROM BEFORE NOV 2010 OR THERE IS A PROBLEM FINDING IT. THE SOURCE GROUP NAME IS ',  sourcegrpname, ' WHICH WAS BEING LOCATED IN THE VALID GROUP LIST: ', self.validgrp_name
            xrdname='mar345'
        newscandict['xrdname']=xrdname
        
        repimagelist=self.lineedittolist(self.replacelistLineEdit)
        newimagelist=self.lineedittolist(self.newlistLineEdit)

        replist=[]
        namlist=[]
        indlist=[]

        for repim, newim in zip(repimagelist, newimagelist):
            try:
                indlist+=[eval(newim.partition(':')[2])]
                namlist+=[newim.partition(':')[0]]
                replist+=[eval(repim)]
            except:
                QMessageBox.warning(self,"failed",  "Aborting because there is a formatting error in the replacement of %s by %s." %(repim, newim))
                return None

        newscandict['ind_tobereplaced']=replist
        newscandict['newimage_scanname']=namlist
        newscandict['newimage_ind']=indlist

        appnamelist=self.lineedittolist(self.appendlistLineEdit)
        appattrlist=[]
        for appname in appnamelist:
            if not appname in self.validgrp_name:
#                    print '*', appname, '*', len(appname)
#                    print self.validgrp_name, appname in self.validgrp_name
                QMessageBox.warning(self,"failed",  "Aborting because the append scan %s was not found." %appname)
                return None
            appattrlist+=[self.validgrp_attr[self.validgrp_name.index(appname)]]
        newscandict['appendscan_name']=appnamelist
        newscandict['appendscan_attr']=copy.deepcopy(appattrlist)

        return newscandict


class xrfanalysisDialog(QDialog,
        ui_xrf_analysis.Ui_XRFAnalysisDialog):
    def __init__(self, parent, h5path, h5groupstr): #if pass pointlist then assume the DepProf data is there to perform the cal

        super(xrfanalysisDialog, self).__init__(parent)
        self.setupUi(self)
#        self.FluxMethodComboBox.clear()
#        self.FluxMethodComboBox.insertItem(0, 'Use Default Value')
#        self.FluxMethodComboBox.insertItem(1, 'Enter Flux Value')
#        QObject.connect(self.FluxMethodComboBox, SIGNAL("currentIndexChanged()"), self.fluxmethodchanged)

        self.attrdict=getattr(h5path, h5groupstr)
        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.databasedictlist=readxrfinfodatabase()
        for count, d in enumerate(self.databasedictlist):
            self.chessrunComboBox.insertItem(count, d['name'])
        QObject.connect(self.chessrunComboBox,SIGNAL("activated(QString)"),self.chessrunchanged)

        self.gunpropdict, self.dpcomp, self.dpnm=getinfoforxrf(h5path, h5groupstr)

        self.ElLines=[self.ElLineEdit0, self.ElLineEdit1, self.ElLineEdit2, self.ElLineEdit3, self.ElLineEdit4]

        for el, lineedit in zip(self.gunpropdict['symbol'], self.ElLines):
            lineedit.setText(el)
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)


        self.beamenergy=eV_nm(self.attrdict['wavelength'])/1000.0

        self.dpissufficient=not (self.dpcomp is None)
        if self.dpissufficient:
#            self.radioButtonInd.setVisible(True)
#            self.FluxIndComboBox.setVisible(True)
            pointlist=self.attrdict['pointlist']
            self.FluxIndComboBox.clear()
            for ind in pointlist:
                self.FluxIndComboBox.insertItem(999, '%d' %ind)
            dist=(numpy.float32(pointlist)-numpts_attrdict(self.attrdict)//2)**2 #this is to try to default to the substrate center index
            self.FluxIndComboBox.setCurrentIndex(numpy.where(dist==dist.min())[0][0])
        else:
            self.FluxIndComboBox.setDisabled(True)
            self.radioButtonInd.setDisabled(True)
            self.DepProfEstCheckBox.setChecked(False)
            self.DepProfEstCheckBox.setDisabled(True)

        self.UnderLineEdit.setText('Ti')
        self.UnderSpinBox.setValue(12)
        self.SicmSpinBox.setValue(0.45)

        p=PYMCACFGpath()
        self.cfgpathstart,garbage=os.path.split(p)
        crs=self.attrdict['chessrunstr']
        self.cfgfilenames=[[f, crs in f] for f in os.listdir(self.cfgpathstart) if os.path.splitext(f)[1]==os.path.splitext(p)[1]]
        self.cfgfilenames.sort(key=operator.itemgetter(1), reverse=True)
        self.cfgfilenames=[f[0] for f in self.cfgfilenames]
        for count, fname in enumerate(self.cfgfilenames):
            self.cfgComboBox.insertItem(count, fname)

        self.bckndeltr_rate=[]
        self.cfgpath=None

    def chessrunchanged(self):
        name=str(self.chessrunComboBox.currentText())
        d=self.databasedictlist[[i for i, d in enumerate(self.databasedictlist) if d['name']==name][0]]
        if 'Sicm' in d:
            self.SicmSpinBox.setValue(d['Sicm'])
        if 'enmin' in d:
            self.enminSpinBox.setValue(d['enmin'])
        if 'enmax' in d:
            self.enmaxSpinBox.setValue(d['enmax'])
        if 'underlayer' in d:
            self.UnderLineEdit.setText(d['underlayer'][0])
            self.UnderSpinBox.setValue(d['underlayer'][1])
        if 'time' in d:
            self.timeLineEdit.setText(d['time'])
        if 'cfgfile' in d and d['cfgfile'] in self.cfgfilenames:
            self.cfgComboBox.setCurrentIndex(self.cfgfilenames.index(d['cfgfile']))
        if 'BckndCounts' in d:
            self.bckndeltr_rate=[[' '.join((el, tr)), ct] for (el,tr,ct) in d['BckndCounts']]

    def fluxmethodchanged(self):
        a='Select image\nfor flux cal'
        print'Enter flux\nvalue', self.FluxMethodComboBox.currentIndex()


    def eltr_cfg(self, el, tr):
        if isinstance(tr, list):
            return [' '.join((el, t)) for t in tr]
        else:
            return [' '.join((el, tr))]

    @pyqtSignature("")
    def on_transitionsPushButton_clicked(self):

        try:
            h5file=h5py.File(self.h5path, mode='r')
            self.time=readh5pyarray(h5file['/'.join((self.h5groupstr, 'measurement/scalar_data', str(self.timeLineEdit.text())))])
            h5file.close()
        except:
            QMessageBox.warning(self,"aborting",  "aborting calculation because could not find that scalar_data")
            print '/'.join((self.h5groupstr, 'measurement/scalar_data', str(self.timeLineEdit.text())))
            return
        self.el=[]
        for le in self.ElLines:
            s=str(le.text())
            if s!='':
                self.el+=[s]



        self.cfgpath=os.path.join(self.cfgpathstart, str(self.cfgComboBox.currentText()))
        self.pymca_config = getcfgdict_txt(self.cfgpath)
        dfltfitlist=flatten([self.eltr_cfg(el, tr) for el, tr in self.pymca_config['peaks'].iteritems()])

        allpeaksdictlist, quantlist, foundpeaks=FindXrays(self.el, energy=self.beamenergy)
        self.el=numpy.array(self.el)
        self.el=self.el[numpy.bool_(foundpeaks)]

        repen=[d['repen'] for d in allpeaksdictlist if d['eltr'] in quantlist]

        filmfitlist=[d['eltr'] for d in allpeaksdictlist]
        if self.UnderSpinBox.value()>0:
            underlayerdictlist, garbage, und_foundpk=FindXrays([str(self.UnderLineEdit.text())], energy=self.beamenergy)
            filmfitlist+=[d['eltr'] for d in underlayerdictlist]

        alreadyinlist=list(set(dfltfitlist)&set(quantlist))
        fitlist=list(set(dfltfitlist)|set(filmfitlist))

        bcknd=numpy.zeros(len(self.el), dtype='float32')
        bckndind_rate=[[quantlist.index(eltr), rate] for eltr, rate in self.bckndeltr_rate if eltr in quantlist]
        if len(bckndind_rate)>0:
            bckndind, rate=zip(*bckndind_rate)
            bcknd[bckndind]=numpy.float32(rate)*numpy.max(self.time)

        dens=numpy.ones(len(self.el), dtype='float32')
        mass=numpy.ones(len(self.el), dtype='float32')
        comp=numpy.ones(len(self.el), dtype='float32')/len(self.el) #this way if the composition is not available then it will guess something reasonable

        elmap=[el in self.gunpropdict['symbol'] for el in self.el]
        elmap=numpy.bool_(elmap)
        gpdmap=[el in self.el for el in self.gunpropdict['symbol']]
        gpdmap=numpy.bool_(gpdmap)


        dens[elmap]=numpy.float32(self.gunpropdict['d'])[gpdmap]
        mass[elmap]=numpy.float32(self.gunpropdict['M'])[gpdmap]
        cmr=numpy.float32(self.gunpropdict['CenterMolRates'])[gpdmap]
        cmr/=cmr.sum()
        comp[elmap]=cmr
        comp/=comp.sum()

        if not numpy.all(elmap): #not all of the quant elements were in funpropdict. even if they were, availability of dep prof is not guaranteed
            elsym, elM, eld = zip(*get_elMd_el(self.el[numpy.logical_not(elmap)]))# assume that if xray were found for an element then the mass and density can be found. If this fails, the next line will fail
            dens[numpy.logical_not(elmap)]=numpy.float32(eld)
            mass[numpy.logical_not(elmap)]=numpy.float32(elM)
            self.dpissufficient=False
        else:
            self.dpissufficient= not (self.dpcomp is None)

        if not self.dpissufficient:
            if self.DepProfEstCheckBox.isChecked() or self.radioButtonInd.isChecked():
                QMessageBox.warning(self,"problem",  "calibration and dep prof estimates not possible with that set of elements")
                self.DepProfEstCheckBox.setChecked(False)
                self.radioButtonDef.setChecked(False)


        self.alreadyinlistLineEdit.setText(', '.join(alreadyinlist))
        self.fitLineEdit.setText(','.join(fitlist))
        self.quantLineEdit.setText(','.join(quantlist))
        self.bckndLineEdit.setText(self.strformat(bcknd, ['%.3e'])[1:-1])
        self.densityLineEdit.setText(self.strformat(dens, ['%.2f'])[1:-1])
        self.massLineEdit.setText(self.strformat(mass, ['%.2f'])[1:-1])
        self.compLineEdit.setText(self.strformat(comp, ['%.2f'])[1:-1])
        self.repenLineEdit.setText(self.strformat(repen, ['%.2f'])[1:-1])

        self.dfltfitlist=dfltfitlist



    def readlineedit(self, le, numcvt=True):
        c=str(le.text())
        c=c.strip()
        ans=[]
        while len(c)>0:
            a, b, c=c.partition(',')
            a=a.strip()
            c=c.strip()
            try:
                if not numcvt:
                    raise
                b=eval(a)
            except:
                b=a
            ans+=[b]
        return ans

    def strformat(self, val, frmt):
        s=''
        v=val
        f=frmt
        if f is None:
            s+=`v`
        elif isinstance(f, list):
            s+='['
            for count, subv in enumerate(v):
                if count>0:
                    s+=','
                s+=f[0] %subv
            s+=']'
        else:
            s+=f %v
        return s

    def buildparstr(self, el, quant, dens, mass, comp, bcknd, repen, cfgpath, addlist, fluxcalstr, dpbool, under, sicm, time, dlambdastr, mflambdastr):
        vl=[el, quant, dens, mass, comp, bcknd, repen, cfgpath, addlist, fluxcalstr, dpbool, under, sicm, time, dlambdastr, mflambdastr]
        nl=["elements", "quantElTr", 'eld', 'elM', 'approxstoich', "BckndCounts", 'RepEn','cfgpath',  'otherElTr', 'FluxCal', 'DepProfEst',  'Underlayer', 'Sicm', 'time', 'dlambda', 'mflambda']
        #fl=[None, None, ['%.2f'], ['%.2f'], ['%.2f'], ['%.3e'],  ['%.2f'], None, None, None, '%.3f', None, None]
        fl=[None, None, ['%s'], ['%s'], ['%.2f'], ['%s'],  ['%s'], None, None, '%s', None, None, '%.3f',  None,  None,  None]
        al=["SecondaryAction='Notify'"]
        s=''
        for count, (n, v, f) in enumerate(zip(nl, vl, fl)):
            if count>0:
                s+=", "
            s+=n+"="
            s+=self.strformat(v, f)
        for a in al:
            s+=", "+a
        return s

    def ExitRoutine(self):
#        try:
#            if self.cfgpath is None:
#                raise

        if self.radioButtonEnt.isChecked():
            self.fluxcalstr='%.10e' %self.FluxSpinBox.value()
        elif self.radioButtonInd.isChecked():
            self.fluxcalstr="'CalUsing%s'" %str(self.FluxIndComboBox.currentText())
        else:
            self.fluxcalstr="'Default'"

        fitlist=self.readlineedit(self.fitLineEdit)
        quantlist=self.readlineedit(self.quantLineEdit)
        BckndCounts=self.readlineedit(self.bckndLineEdit, numcvt=False)
        dens=self.readlineedit(self.densityLineEdit, numcvt=False)
        mass=self.readlineedit(self.massLineEdit, numcvt=False)
        comp=numpy.float32(self.readlineedit(self.compLineEdit), numcvt=True)
        comp/=comp.sum()
        repen=self.readlineedit(self.repenLineEdit, numcvt=False)
        dlambdastr=str(self.dlambdaLineEdit.text())
        mflambdastr=str(self.mflambdaLineEdit.text())


        addlist=list((set(fitlist)-set(self.dfltfitlist))-set(quantlist))


        unel=str(self.UnderLineEdit.text())
        uneldict=GunPropertyDict([unel])
        if uneldict is None:
            print 'WARNING: UNDERLAYER ELEMENT NOT FOUND - effectively removing underlayer'
            self.Underlayer=('Ti', 0.1, 0)
        else:
            self.Underlayer=(unel, uneldict['d'][0], self.UnderSpinBox.value())
        self.Sicm=self.SicmSpinBox.value()
        self.DepProfEst=self.DepProfEstCheckBox.isChecked()

        self.parstr=self.buildparstr(list(self.el), quantlist, dens, mass, comp, BckndCounts, repen, self.cfgpath, addlist, self.fluxcalstr, self.DepProfEst, self.Underlayer, self.Sicm, str(self.timeLineEdit.text()), dlambdastr, mflambdastr)
#        except:
#            self.parstr = None




class pdfsearchDialog(QDialog,
        ui_pdfsearch.Ui_pdfsearchDialog):
    def __init__(self, parent, plotw, offset=0., filename='PDFentries.txt', cvtfcn=lambda x:d_q(x/10.0)):

        super(pdfsearchDialog, self).__init__(parent)
        self.setupUi(self)
        self.plotw=plotw
        self.ax=self.plotw.axes
        self.startinglineindex=len(self.ax.lines)
        self.startingtextindex=len(self.ax.texts)
        self.afterpdflistlinesindex=self.startinglineindex
        self.offset=offset
        self.dfltheight=(self.ax.get_ylim()[1]-self.offset)*0.8
        self.heightSpinBox.setValue(self.dfltheight)
        self.lineind_textind_plotlist=[]
        self.numpdflabels=0

        self.pdfname, self.pdflist=readpdffile(os.path.join(defaultdir('pdfentries'), filename))
        self.pdflist=[[[cvtfcn(d), h] for d, h in pdf] for pdf in self.pdflist]
        QObject.connect(self.pdfListWidget,SIGNAL("itemSelectionChanged()"),self.plotsinglepdfentry)

        for l in self.pdfname:
            self.pdfListWidget.addItem(l)

    @pyqtSignature("")
    def on_findPushButton_clicked(self):
        lelist=[self.searchLineEdit0, self.searchLineEdit1, self.searchLineEdit2, self.searchLineEdit3]
        slist=[str(le.text()) for le in lelist]
        for count, pdfname in enumerate(self.pdfname):
            searchbool=True
            for s in slist:
                searchbool*=s in pdfname
            plotbool=True
            for ind in range(self.plotListWidget.count()):
                plotbool*=not str(self.plotListWidget.item(ind).text()) in self.pdfname
            self.pdfListWidget.item(count).setHidden(not (searchbool and plotbool))

    def plotsinglepdfentry(self):
        if self.plotsingleCheckBox.isChecked():
            row=self.pdfListWidget.currentRow()
            self.clearpdfplots(self.afterpdflistlinesindex)
            self.drawpdfpeaks(row)

    def plotpdflist(self):
        self.clearpdfplots(self.startinglineindex)
        self.numpdflabels=0
        for i in range(self.plotListWidget.count()):
            if not self.plotListWidget.item(i).isHidden():
                self.drawpdfpeaks(i, fromplotlist=True)
        self.afterpdflistlinesindex=len(self.ax.lines)
    def clearpdfplots(self, startind, stopind=None):
        if stopind is None:
            stopind=len(self.ax.lines)
        reduceind=lambda ind, redbool: (((ind is None) and (None, )) or (redbool and (ind-1, )) or (ind,))[0]
        for i in range(startind, stopind)[::-1]:# go through the delete indeces but if one peak is in the dleete indeces then delete the entire pdf entry and the label
            ind=[cnt for cnt, lineinds in enumerate(map(operator.itemgetter(0),self.lineind_textind_plotlist)) if i in lineinds]
            if len(ind)>0:
                ind=ind[0]
                lineinds, textind=self.lineind_textind_plotlist.pop(ind)
                if textind is None:
                    textind=99999
                else:
                    del self.ax.texts[textind]
                for li in sorted(lineinds)[::-1]:
                    del self.ax.lines[li]
                self.lineind_textind_plotlist=[[list(reduceind(numpy.int16(li), li[0]>lineinds[0])), reduceind(ti, ti>textind)] for li, ti in self.lineind_textind_plotlist]
        if len([ti for li, ti in self.lineind_textind_plotlist if not ti is None])==0:#if all the label indeces are None there are no indeces so start the counter over
            self.numpdflabels=0

    @pyqtSignature("")
    def on_addPushButton_clicked(self):

        self.plotListWidget.addItem(self.pdfname[self.pdfListWidget.currentRow()])
        self.pdfListWidget.currentItem().setHidden(True)

        self.labelListWidget.addItem(self.labelLineEdit.text())
        self.colListWidget.addItem(self.colLineEdit.text())
        self.heightListWidget.addItem('%.2f' %self.heightSpinBox.value())
        self.plotpdflist()

    @pyqtSignature("")
    def on_removePushButton_clicked(self):
        item=self.plotListWidget.currentItem()
        if not item is None:
            txt=str(item.text())
            if txt in self.pdfname:
                self.pdfListWidget.item(self.pdfname.index(txt)).setHidden(False)
            row=self.plotListWidget.currentRow()
            for ListWidget in [self.plotListWidget, self.labelListWidget, self.colListWidget, self.heightListWidget]:
                ListWidget.item(row).setHidden(True)
                #ListWidget.removeItemWidget(ListWidget.item(row))
            self.plotpdflist()
    def drawpdfpeaks(self, pdfindex, fromplotlist=False):
        if fromplotlist:
            label=str(self.labelListWidget.item(pdfindex).text())
            colstr=str(self.colListWidget.item(pdfindex).text())
            try:
                height=eval(str(self.heightListWidget.item(pdfindex).text()))*1.0
            except:
                print 'height interpretation error'
                height=self.dfltheight
            pdfindex=self.pdfname.index(str(self.plotListWidget.item(pdfindex).text()))
        else:
            label=str(self.labelLineEdit.text())
            colstr=str(self.colLineEdit.text())
            height=self.heightSpinBox.value()
        if colstr=='':
            colstr='r'
        pdf=self.pdflist[pdfindex]
        self.ax.hold(True)
        lineindstart=len(self.ax.lines)
        for q, h in pdf:
            h*=height
            self.ax.plot([q, q], [self.offset, self.offset+h], colstr)
        lineindstop=len(self.ax.lines)
        if label=='':
            textind=None
        else:
            textind=len(self.ax.texts)
            for garbage in range(self.numpdflabels):
                label=''.join(('     ', label))
            self.numpdflabels+=1
            ylim=self.ax.get_ylim()
            xlim=self.ax.get_xlim()
            fs=14
            sp=(fs*1.4/72.)/self.ax.figure.get_figheight()
            self.ax.text(xlim[1]-.03*(xlim[1]-xlim[0]), ylim[1]-(.03+self.numpdflabels*sp)*(ylim[1]-ylim[0]), label, color=colstr[0], fontsize=fs, horizontalalignment='right')

        self.lineind_textind_plotlist+=[[range(lineindstart, lineindstop), textind]]
        self.plotw.fig.canvas.draw()


class editrawxrdwindow(QDialog,
        ui_editrawxrdDialog.Ui_editrawxrdDialog):
    #***
    def __init__(self, parent, h5path, h5groupstr=None,  h5grppath=None):#either pass  h5grppath which is the entire path to the XRD group that contains counts or the normal h5groupstr
        super(editrawxrdwindow, self).__init__(parent)
        self.setupUi(self)
        
        self.h5path=h5path
        self.h5groupstr=h5groupstr
        self.h5grppath=h5grppath
        
        h5file=h5py.File(self.h5path, mode='r')
        if self.h5grppath is None:
            h5analysis=h5file['/'.join((self.h5groupstr, 'analysis'))]
            h5mar=h5file['/'.join((self.h5groupstr, 'analysis', getxrdname(h5analysis)))]
            h5marcounts=h5file['/'.join((self.h5groupstr,'measurement/'+getxrdname(h5analysis)+'/counts'))]
            h5sd=h5file['/'.join((self.h5groupstr,'measurement', 'scalar_data'))]
        else:
            h5marcounts=h5file[h5grppath]['counts']
            if 'scalar_data' in h5file[h5grppath].parent:
                h5sd=(h5file[h5grppath].parent)['scalar_data']
            else:
                h5sd=None
        s=''
        for k, v in h5marcounts.attrs.iteritems():
            if k.startswith('mod_'):
                s+=': '.join((k.partition('mod_')[2], `v`))+'\n'
        if len(s)>0:
            s="This raw data has already been modified with the following settings:\n"+s
            QMessageBox.warning(self, "REPEAT EDIT",  s)
        
        if h5sd is None:
            self.normCheckBox.setChecked(False)
            self.normCheckBox.setEnabled(False)
            prefind=None
        else:
            count=0
            prefind=None
            for dset in h5sd.iterobjects():
                if isinstance(dset, h5py.Dataset) and dset.shape==h5marcounts.shape[0:1]:
                    nam=dset.name.rpartition('/')[2]
                    self.normComboBox.insertItem(count, nam)
                    if nam=='IC3':
                        prefind=count
                    count+=1
        if not prefind is None:
            self.normComboBox.setCurrentIndex(prefind)
        h5file.close()
        self.dezingComboBox.insertItem(0, 'outlier method')
        self.dezingComboBox.insertItem(1, 'by image max val')
        self.dezingComboBox.setCurrentIndex(0)
        QObject.connect(self.dezingComboBox,SIGNAL("activated(QString)"),self.dezingchanged)
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)

    def dezingchanged(self, garbage):
        show=self.dezingComboBox.currentIndex()==0
        self.dezingLabel.setVisible(show)
        self.dezingSpinBox.setVisible(show)
    def ExitRoutine(self):
        dezingbool=self.dezingCheckBox.isChecked()
        normbool=self.normCheckBox.isChecked() 
        multbool=self.multCheckBox.isChecked()
        if dezingbool or normbool or multbool:
            a=dezingbool and self.dezingComboBox.currentIndex()==1
            b=normbool and str(self.normComboBox.currentText()) or None
            c=multbool and self.multSpinBox.value() or None
            d=(dezingbool and self.dezingComboBox.currentIndex()==0) and self.dezingSpinBox.value() or None
            if self.h5grppath is None:
                xrdraw_dezing_rescale(self.h5path, h5groupstr=self.h5groupstr, dezingbool=a, normdsetname=b, multval=c, outlier_nieghbratio=d)
            else:
                xrdraw_dezing_rescale(self.h5path, h5grppath=self.h5grppath, dezingbool=a, normdsetname=b, multval=c, outlier_nieghbratio=d)
