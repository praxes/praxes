#/*##########################################################################
# Copyright (C) 2004-2007 European Synchrotron Radiation Facility
#
# This file is part of the PyMCA X-ray Fluorescence Toolkit developed at
# the ESRF by the Beamline Instrumentation Software Support (BLISS) group.
#
# This toolkit is free software; you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option) 
# any later version.
#
# PyMCA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PyMCA; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# PyMCA follows the dual licensing model of Trolltech's Qt and Riverbank's PyQt
# and cannot be used as a free plugin for a non-free program. 
#
# Please contact the ESRF industrial unit (industry@esrf.fr) if this license 
# is a problem to you.
#############################################################################*/
/*char RcsId[] = "$Header: /segfs/bliss/source/python/specfile/specfile-3.1/src/RCS/specfile_py.c,v 1.9 2005/05/25 13:30:16 sole Exp $"; */
/************************************************************************
 *
 *   File:          specfile_py.c
 *
 *   Project:       SpecFile library
 *
 *   Description:   python interface to Specfile library
 * 
 *   Author:        V.Rey
 *
 *   Date:          $Date: 2005/05/25 13:30:16 $
 *
 ************************************************************************/
/*
 *   Log: $Log: specfile_py.c,v $
 *   Log: Revision 1.9  2005/05/25 13:30:16  sole
 *   Log: Enormous memory leak corrected
 *   Log:
 *   Log: Revision 1.8  2005/05/18 10:47:30  sole
 *   Log: Problem with ifdef solved
 *   Log:
 *   Log: Revision 1.7  2004/05/21 12:33:02  sole
 *   Log: Working windows version
 *   Log:
 *   Log: Revision 1.6  2003/03/06 17:02:09  sole
 *   Log: Check for number of lines less than 0
 *   Log: (At most should be -1, but I let it as less than 0)
 *   Log:
 *   Log: Revision 1.5  2002/11/15 10:11:19  sole
 *   Log: Memory leak corrected in scandata_data
 *   Log:
 *   Log: Revision 1.4  2002/11/15 09:29:23  sole
 *   Log: PyArray_Return put back
 *   Log: Several memory leaks removed.
 *   Log:
 *   Log: Revision 1.3  2002/11/12 13:11:29  sole
 *   Log: <= -1 replaced by == -1
 *   Log:
 *
 *       New command for Scandata:  motorpos()
 *       interfaces with the library function 
 *       SfMotorPosByName()
 *
 *   Log: Revision 3.0  2000/12/20 14:17:19  rey
 *   Log: Python version available
 *   Log:
 *   Log: Revision 2.2  2000/12/20 12:12:08  rey
 *   Log: bug corrected with SfAllMotors
 *   Log:
 * Revision 2.1  2000/07/31  19:03:11  19:03:11  rey (Vicente Rey-Bakaikoa)
 * SfUpdate and bug corrected in ReadIndex
 * 
 * Revision 1.5  2000/02/16  13:58:27  13:58:27  rey (Vicente Rey-Bakaikoa)
 * Version before major changes for MCA support
 * 
 * Revision 1.1  99/10/19  15:28:32  15:28:32  rey (Vicente Rey-Bakaikoa)
 * Initial revision
 * 
 */

/************************************************************************
 
  Copyright 1999  by European Synchrotron Radiation Facility, Grenoble, 
                  France

                               ----------
 
                           All Rights Reserved
 
                               ----------

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the names of European Synchrotron
Radiation Facility or ESRF or BLISS not be used in advertising or 
publicity pertaining to distribution of the software without specific, 
written prior permission.

EUROPEAN SYNCHROTRON RADIATION FACILITY DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL EUROPEAN SYNCHROTRON
RADIATION FACILITY OR ESRF BE LIABLE FOR ANY SPECIAL, INDIRECT OR 
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, 
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

**************************************************************************/
#ifdef WIN32
#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#else
#include <Python.h>
#endif
#endif

#ifndef WIN32
#include <Python.h>
#endif

#include <numpy/arrayobject.h>
#include <SpecFile.h>

/*
 * Specfile exceptions
 */
static PyObject *ErrorObject;

     /* except specfile.error */
#define onError(message)  \
     {PyErr_SetString (ErrorObject,message); return NULL; }  

/*
 * Data types
 */
typedef struct {
   PyObject_HEAD
   SpecFile *sf;
   char     *name;
   short     length;
} specfileobject;

typedef struct {
   PyObject_HEAD
   specfileobject *file;
   long            index;
   long            cols;
} scandataobject;

staticforward PyTypeObject Specfiletype;
staticforward PyTypeObject Scandatatype;

#define is_specfileobject(v) ((v)->type == &Specfiletype)
#define is_scandataobject(v) ((v)->type == &Scandatatype)


/*
 * Function prototypes
 */
   /*
    * Utility function
    */
static char           * compList(long *nolist,long howmany);

   /*
    * Specfile methods
    */
static PyObject  * specfile_list      (PyObject *self,PyObject *args);
static PyObject  * specfile_allmotors (PyObject *self,PyObject *args);
static PyObject  * specfile_title     (PyObject *self,PyObject *args);
static PyObject  * specfile_user      (PyObject *self,PyObject *args);
static PyObject  * specfile_date      (PyObject *self,PyObject *args);
static PyObject  * specfile_epoch     (PyObject *self,PyObject *args);
static PyObject  * specfile_update    (PyObject *self,PyObject *args);
static PyObject  * specfile_scanno    (PyObject *self,PyObject *args);
static PyObject  * specfile_select    (PyObject *self,PyObject *args);
static PyObject  * specfile_show      (PyObject *self,PyObject *args);

static struct PyMethodDef  specfile_methods[] = 
{
   {"list",      specfile_list,      1},
   {"allmotors", specfile_allmotors, 1},
   {"title",     specfile_title,     1},
   {"user",      specfile_user,      1},
   {"date",      specfile_date,      1},
   {"epoch",     specfile_epoch,     1},
   {"update",    specfile_update,    1},
   {"scanno",    specfile_scanno,    1},
   {"select",    specfile_select,    1},
   {"show",      specfile_show,      1},
   { NULL, NULL}
};

   /*
    * Specfile python basic operations
    */
static PyObject * specfile_open   (char *filename);             /* create  */
static PyObject * specfile_close  (PyObject *self);             /* dealloc */
static int        specfile_noscans(PyObject *self);             /* length  */
static PyObject * specfile_scan   (PyObject *self,int index);   /* item    */
static int        specfile_print  (PyObject *self,FILE *fp, 
                                                   int flags);  /* print*/
static PyObject * specfile_getattr(PyObject *self,char *name);  /* getattr */


   /*
    * Scandata methods
    */

static PyObject   * scandata_data         (PyObject *self,PyObject *args);
static PyObject   * scandata_dataline     (PyObject *self,PyObject *args);
static PyObject   * scandata_datacol      (PyObject *self,PyObject *args);
static PyObject   * scandata_alllabels    (PyObject *self,PyObject *args);
static PyObject   * scandata_allmotorpos  (PyObject *self,PyObject *args);
static PyObject   * scandata_motorpos     (PyObject *self,PyObject *args);
static PyObject   * scandata_hkl          (PyObject *self,PyObject *args);
static PyObject   * scandata_number       (PyObject *self,PyObject *args);
static PyObject   * scandata_order        (PyObject *self,PyObject *args);
static PyObject   * scandata_command      (PyObject *self,PyObject *args);
static PyObject   * scandata_date         (PyObject *self,PyObject *args);
static PyObject   * scandata_cols         (PyObject *self,PyObject *args);
static PyObject   * scandata_lines        (PyObject *self,PyObject *args);
static PyObject   * scandata_header       (PyObject *self,PyObject *args);
static PyObject   * scandata_fileheader   (PyObject *self,PyObject *args);
static PyObject   * scandata_nbmca        (PyObject *self,PyObject *args);
static PyObject   * scandata_mca          (PyObject *self,PyObject *args);
static PyObject   * scandata_show         (PyObject *self,PyObject *args);

static struct PyMethodDef  scandata_methods[] = {
   {"data",        scandata_data,        1},
   {"dataline",    scandata_dataline,    1},
   {"datacol",     scandata_datacol,     1},
   {"alllabels",   scandata_alllabels,   1},
   {"allmotorpos", scandata_allmotorpos, 1},
   {"motorpos",    scandata_motorpos,    1},
   {"hkl",         scandata_hkl,         1},
   {"number",      scandata_number,      1},
   {"order",       scandata_order,       1},
   {"command",     scandata_command,     1},
   {"date",        scandata_date,        1},
   {"cols",        scandata_cols,        1},
   {"lines",       scandata_lines,       1},
   {"header",      scandata_header,      1},
   {"fileheader",  scandata_fileheader,  1},
   {"nbmca",       scandata_nbmca,       1},
   {"mca",         scandata_mca,         1},
   {"show",        scandata_show,        1},
   { NULL, NULL}
};

   /*
    * Scandata python basic operation
    */
static PyObject * scandata_new    (void);                         /* create */
static PyObject * scandata_free   (PyObject *self);               /* dealloc */
static int        scandata_size   (PyObject *self);               /* length */
static PyObject * scandata_col    (PyObject *self,int index);     /* item */
static PyObject * scandata_slice  (PyObject *self,int lidx,int hidx);/* slice */
static int        scandata_print  (PyObject *self,FILE *fp, 
                                                   int flags);    /* print*/
static PyObject * scandata_getattr(PyObject *self,char *name);    /* getattr */

/*
 * module init
 */
#ifndef WIN32
 void initspecfile(void);
#endif
   /*
    * Creators
    */
static PyObject *specfiletype_new(PyObject *self,PyObject *args);
static PyObject *scandatatype_new(PyObject *self,PyObject *args);


/*
 *  Specfile class
 * 
 *************************************************/
  /*
   * Instance methods
   */
static PyObject *
specfile_list(PyObject *self,PyObject *args)
{
    long      *scanlist; 
    long      no_scans;
    int       error = 0;
    char     *strlist;
    PyObject *pstr;

    specfileobject *v = (specfileobject *) self;

    if (!PyArg_ParseTuple(args, ""))   
        return NULL;

    no_scans = SfScanNo(v->sf);
    scanlist = SfList(v->sf,&error);

    if ( scanlist == NULL || no_scans == 0) {
        PyErr_SetString(PyExc_TypeError,"Cannot get scan list for file");
        return NULL;
    } else {
        strlist = (char *)compList(scanlist,no_scans);
        pstr = Py_BuildValue("s",strlist);
        free(scanlist);
        return pstr;
    } 
}

static PyObject *
specfile_allmotors(PyObject *self,PyObject *args)
{
    
    int error,i;
    char **motornames;
    long nb_motors;
    PyObject *t,*x;

    specfileobject *v = (specfileobject *) self;

    if (!PyArg_ParseTuple(args, ""))   
        return NULL;

    nb_motors = SfAllMotors(v->sf,1,&motornames,&error);

    if ( nb_motors == -1 ) 
           onError("cannot get motor names for specfile");

    t = PyList_New(nb_motors);
    for ( i = 0 ;i<nb_motors;i++) {
       x = PyString_FromString(motornames[i]);
       PyList_SetItem(t,i,x);
    }

    return t;
}

static PyObject *
specfile_title(PyObject *self,PyObject *args)
{
    int error;
    char *title;
    PyObject *pyo;

    specfileobject *v = (specfileobject *) self;

    if (!PyArg_ParseTuple(args, ""))   
        return NULL;

    title = SfTitle(v->sf,1,&error);
   
    if (title == NULL) 
        onError("cannot get title for specfile")

    pyo = Py_BuildValue("s",title);
    free(title);
    return pyo;
}

static PyObject *
specfile_user(PyObject *self,PyObject *args)
{
    int error;
    char *user;

    specfileobject *v = (specfileobject *) self;

    if (!PyArg_ParseTuple(args, ""))   
        return NULL;

    user = SfUser(v->sf,1,&error);
   
    if (user != NULL) {
        free(user);
        return Py_BuildValue("s",user);
    } else {
        onError("cannot get user for specfile");
    }
}

static PyObject *
specfile_date(PyObject *self,PyObject *args)
{
    int error;
    char *date;
    PyObject *pyo;

    specfileobject *v = (specfileobject *) self;

    if (!PyArg_ParseTuple(args, ""))   
        return NULL;

    date = SfFileDate(v->sf,1,&error);
   
    if (date == NULL) 
       onError("cannot get data for specfile")

    pyo = Py_BuildValue("s",date);
    free(date);
    return pyo;
}

static PyObject *
specfile_epoch(PyObject *self,PyObject *args)
{
    int error;
    long epoch;

    specfileobject *v = (specfileobject *) self;

    if (!PyArg_ParseTuple(args, ""))   
        return NULL;

    epoch = SfEpoch(v->sf,1,&error);
   
    if (epoch != -1) {
        return Py_BuildValue("l",epoch);
    } else {
        onError("cannot get epoch for specfile");
    }
}

static PyObject *
specfile_update(PyObject *self,PyObject *args)
{
    int error;
    short ret;

    specfileobject *v = (specfileobject *) self;
   
    if (!PyArg_ParseTuple(args, ""))   
        return NULL;

    ret = SfUpdate(v->sf,&error);
    if (ret == 1){
       v->length = SfScanNo(v->sf);
    }
    return(Py_BuildValue("i",ret));
}

static PyObject *
specfile_scanno(PyObject *self,PyObject *args)
{
    long scanno;
    specfileobject *v = (specfileobject *) self;
   

    if (!PyArg_ParseTuple(args, ""))   
        return NULL;

    scanno = v->length;

    return Py_BuildValue("l",scanno);
}

static PyObject *
specfile_select(PyObject *self,PyObject *args) 
{

    int  n,number,order,index; 
    char   *scanstr;
    int error;

    scandataobject *v;
    specfileobject *f = (specfileobject *)self;
    
   if (!PyArg_ParseTuple(args,"s",&scanstr)) {
       return NULL;
   } else {
       n = sscanf(scanstr,"%d.%d",&number,&order);
       if ( n < 1 || n > 2 ) onError("cannot decode scan number/order"); 
       if ( n == 1) order = 1;
   }

    index = SfIndex(f->sf,number,order);

    if (index == -1 ) 
          onError("scan not found");

    v = PyObject_NEW(scandataobject,&Scandatatype);
 
    if (v == NULL)
        return NULL;

    v->file  = f;
    v->index = index;
    v->cols  = SfNoColumns(f->sf,v->index,&error);

    Py_INCREF(self);

    return (PyObject *) v;
}

static PyObject *
specfile_show(PyObject *self,PyObject *args) 
{

    specfileobject *f = (specfileobject *)self;

    SfShow(f->sf);

    return (Py_BuildValue("l",0));
}


  /*
   * Basic specfiletype operations
   */
static PyObject *
specfile_open(char *filename) {      /* on x = specfile.Specfile(name) */
    specfileobject *self;
    SpecFile       *sf;
    int             error;

    self = PyObject_NEW(specfileobject,&Specfiletype);

    if (self == NULL)
        return NULL;

    if (( sf = SfOpen(filename,&error)) == NULL )
        onError("cannot open file");

    self->sf = sf;
    self->length = SfScanNo(sf);
    self->name = (char *)strdup(filename);
    strcpy(self->name,filename);

/*  Py_INCREF(self); */
    return (PyObject *)self;
}

static PyObject *
specfile_close(PyObject *self) {

    specfileobject *f = (specfileobject *) self;

    SfClose(f->sf);
    free(f->name);

    PyObject_DEL(f);

    return NULL;
}


  /*
   * Sequence type methods
   */
static int
specfile_noscans(PyObject *self) {
    int       no_scans;

    specfileobject *f = (specfileobject *)self;
    no_scans = f->length;

    return no_scans;

}

static PyObject *
specfile_scan(PyObject *self,int index) {
    int error;

    scandataobject *v;
    specfileobject *f = (specfileobject *)self;

    if ( index < 0 || index >= f->length) {
         PyErr_SetString(PyExc_IndexError,"scan out of bounds");
         return NULL;
    }

    v = PyObject_NEW(scandataobject,&Scandatatype);
 
    if (v == NULL)
        return NULL;

    v->file  = f;
    v->index = index+1;
    v->cols  = SfNoColumns(f->sf,v->index,&error);

    Py_INCREF(self);

    return (PyObject *) v;
}


static int
specfile_print(PyObject *self,FILE *fp,int flags) {
    int ok=0;
    specfileobject *f = (specfileobject *)self;
    fprintf(fp,"specfile('%s')", f->name);
    return ok;
}

static PyObject *
specfile_getattr(PyObject *self,char *name) {
   return Py_FindMethod(specfile_methods,self,name);
}


/*
 * Type descriptors
 */
static PySequenceMethods specfile_as_sequence = {
  (inquiry)        specfile_noscans,    /*     length len(sf)     */
  (binaryfunc)          0,              /*     concat sf1 + sf2   */
  (intargfunc)          0,              /*     repeat sf * n      */
  (intargfunc)     specfile_scan,       /*     item  sf[i], in    */
  (intintargfunc)       0,              /*     slice sf[i:j]      */
  (intobjargproc)       0,              /*     asset sf[i] = v    */
  (intintobjargproc)    0,              /* slice ass. sf[i:j] = v */
};

static PyTypeObject Specfiletype = {
    /* type header */ 
#ifdef WIN32
       PyObject_HEAD_INIT(NULL)
#else
       PyObject_HEAD_INIT(&PyType_Type)
#endif       
	   0,
       "specfile",
       sizeof(specfileobject),
       0,

    /* standard methods */
       (destructor)   specfile_close,    /*  tp-dealloc   ref-count = 0  */
       (printfunc)    specfile_print,    /*  tp-print     print sf       */
       (getattrfunc)  specfile_getattr,  /*  tp-getattr   sf.attr        */
       (setattrfunc)  0,                 /*  tp-setattr   sf.attr = v    */
       (cmpfunc)      0,                 /*  tp-setattr   sf1 > sf2      */
       (reprfunc)     0,                 /*  tp-repr      'sf', print sf */

    /* type categories */
       0,                                /* tp as number   +,-,....      */
       &specfile_as_sequence,            /* tp as sequence +,[i],[i:j]...*/
       0,                                /* tp as mapping [key], len, ...*/

    /* more methods */
       (hashfunc)     0,                 /* tp_hash  dict(sf) */
       /* (binaryfunc)   0,               tp_call  sf()     */
       /* (reprfunc)     0,               tp_str   str(x)   */
};

/* end specfile class */


/* begin scandata */
static PyObject *
scandata_data(PyObject *self,PyObject *args) {
   
    int     error;
    int     ret;
    double  **data;
    long     *data_info;
    int       dimensions[2],i,j;

    SpecFile *sf;
    int     idx,didx;

    PyArrayObject *array;

    scandataobject *s = (scandataobject *) self;

    sf  = (s->file)->sf;
    idx = s->index;

    if (!PyArg_ParseTuple(args,"") )
           onError("wrong arguments for data");
    ret = SfData(sf,idx,&data,&data_info,&error);
    if ( ret == -1 )
           onError("cannot read data");

/*    printf("DATA: %d rows / %d columns\n", data_info[1], data_info[0]);*/

    dimensions[0] = data_info[1];
    dimensions[1] = data_info[0];
    array = (PyArrayObject *)PyArray_FromDims(2,dimensions,PyArray_DOUBLE);

   /*
    * Copy
    *   I should write a specfile function that copies all data in a 
    *   single pointer array
    */
    for (i=0;i<dimensions[0];i++) {
       for (j=0;j<dimensions[1];j++) {
          didx = j + i * dimensions[1];
          ((double *)array->data)[didx] = data[j][i];
       }
    }
    /* memcpy(array->data,data,PyArray_NBYTES(array)); */

    freeArrNZ((void ***)&data,data_info[ROW]);
    free(data_info);
    if (data != (double **) NULL) {
        free(data);
    }
/*    return (PyObject *)array; */
    return PyArray_Return(array);
}

static PyObject *
scandata_dataline(PyObject *self,PyObject *args) {
    int     error;
    int     ret, lineno;
    double  *data;

    PyArrayObject *array;

    SpecFile *sf;
    int     idx;

    scandataobject *s = (scandataobject *) self;

    sf  = (s->file)->sf;
    idx = s->index;

    if (!PyArg_ParseTuple(args,"i",&lineno)) 
            onError("cannot decode arguments for line data"); 
    
    ret = SfDataLine(sf,idx,lineno,&data,&error);
     
    if (ret == -1 )
          onError("cannot get data for line");

    array  = (PyArrayObject *)PyArray_FromDims(1,&ret,PyArray_DOUBLE);

    memcpy(array->data,data,PyArray_NBYTES(array));

    return (PyObject *)array;
}

static PyObject *
scandata_datacol(PyObject *self,PyObject *args) {
    int     error;
    int     ret, colno;
    char    *colname;
    double  *data;

    PyArrayObject *array;

    SpecFile *sf;
    int     idx;
    scandataobject *s = (scandataobject *) self;

    sf  = (s->file)->sf;
    idx = s->index;

    if (!PyArg_ParseTuple(args,"i",&colno)) {
      PyErr_Clear() ; 
      if (!PyArg_ParseTuple(args,"s",&colname)) {
	onError("cannot decode arguments for column data"); 
      } else {
	ret = SfDataColByName(sf,idx,colname,&data,&error);
      }
    } else {
      ret = SfDataCol(sf,idx,colno,&data,&error);
    }
    
    if (ret == -1 )
      onError("cannot get data for column");
    
    array      = (PyArrayObject *)PyArray_FromDims(1,&ret,PyArray_DOUBLE);
    
   if (data != (double *) NULL){
        memcpy(array->data,data,PyArray_NBYTES(array));
        free(data);
    }else{
        /* return an empty array? */
        printf("I should return an empty array ...\n");
        ;
    }

    /* put back PyArray_Return */ 
/*    return (PyObject *)array; */
    return PyArray_Return(array);
    /*
      it does not work for solaris and linux
      I should check the call to PyErr_Occurred()) in Numeric/Src/arrayobject.c
      PyArray_Return(array); 
     */
}


static PyObject * 
scandata_alllabels  (PyObject *self,PyObject *args)
{
    int error,i;
    char **labels;
    long nb_labels;
    PyObject *t,*x;

    scandataobject *v = (scandataobject *) self;

    if (!PyArg_ParseTuple(args, ""))   
        return NULL;

    nb_labels = SfAllLabels((v->file)->sf,v->index,&labels,&error);

    t = PyList_New(nb_labels);
    for ( i = 0 ;i<nb_labels;i++) {
       x = PyString_FromString(labels[i]);
       PyList_SetItem(t,i,x);
    }

    return t;
}

static PyObject   * 
scandata_allmotorpos  (PyObject *self,PyObject *args)
{
    int error,i;
    double *motorpos;
    long nb_motors;
    PyObject *t,*x;

    scandataobject *v = (scandataobject *) self;

    if (!PyArg_ParseTuple(args, ""))   
        return NULL;

    nb_motors = SfAllMotorPos((v->file)->sf,v->index,&motorpos,&error);

    t = PyList_New(nb_motors);

    for ( i = 0 ;i<nb_motors;i++) {
       x = PyFloat_FromDouble(motorpos[i]);
       PyList_SetItem(t,i,x);
    }

    return t;
}

static PyObject   * 
scandata_motorpos  (PyObject *self,PyObject *args)
{
    char   *motorname;
    int     error;
    double  motorpos;

    scandataobject *v = (scandataobject *) self;

    if (!PyArg_ParseTuple(args,"s",&motorname)) {
       return NULL;
    } 

    motorpos = SfMotorPosByName((v->file)->sf,v->index,motorname,&error);

    if (motorpos != HUGE_VAL) {
        return Py_BuildValue("f",motorpos);
    } else {
        onError("cannot get position for motor");
    }
   
}

static PyObject * 
scandata_hkl          (PyObject *self,PyObject *args)
{
    int idx,error;
    double *hkl;
    PyObject *pyo;

    SpecFile *sf;

    scandataobject *s = (scandataobject *) self;

    idx = s->index;
    if (idx == -1 ) {
        onError("empty scan data");
    }
    sf  = (s->file)->sf;

    hkl = SfHKL(sf,idx,&error);

    if (hkl == NULL) 
        onError("cannot get data for column");

    pyo = Py_BuildValue("ddd",hkl[0],hkl[1],hkl[2]);
    free(hkl);
    return pyo;

}

static PyObject * 
scandata_number       (PyObject *self,PyObject *args)
{
    int number,idx;
    SpecFile *sf;

    scandataobject *s = (scandataobject *) self;

    sf  = (s->file)->sf;
    idx = s->index;

    number = SfNumber(sf,idx);

    return Py_BuildValue("i",number);

}

static PyObject   * 
scandata_order        (PyObject *self,PyObject *args)
{
    int order,idx;
    SpecFile *sf;

    scandataobject *s = (scandataobject *) self;

    sf  = (s->file)->sf;
    idx = s->index;

    order = SfOrder(sf,idx);

    return Py_BuildValue("i",order);

}

static PyObject   * 
scandata_command      (PyObject *self,PyObject *args)
{
    int idx,error;
    char *command;
    PyObject *pyo;

    SpecFile *sf;

    scandataobject *s = (scandataobject *) self;

    idx = s->index;
    if (idx == -1 ) {
        onError("empty scan data");
    }
    sf  = (s->file)->sf;

    command = SfCommand(sf,idx,&error);

    if (command == NULL) 
       onError("cannot get command for scan")

    pyo = Py_BuildValue("s",command);
    free(command);
    return pyo;

}

static PyObject   * 
scandata_date      (PyObject *self,PyObject *args)
{
    int idx,error;
    char *date;
    PyObject *pyo;

    SpecFile *sf;

    scandataobject *s = (scandataobject *) self;

    idx = s->index;
    if (idx == -1 ) {
        onError("empty scan data");
    }
    sf  = (s->file)->sf;

    date = SfDate(sf,idx,&error);

    if (date == NULL) 
        onError("cannot get date for scan");

    pyo =  Py_BuildValue("s",date);
    free(date);
    return pyo;

}

static PyObject   * 
scandata_cols      (PyObject *self,PyObject *args)
{
    int cols,idx;

    scandataobject *s = (scandataobject *) self;

    idx = s->index;
    if (idx == -1 ) 
        onError("empty scan data");
   
    cols = s->cols; 

    if (cols == -1)
        onError("cannot get cols for scan");

    return Py_BuildValue("l",cols);
}

static PyObject   * 
scandata_lines      (PyObject *self,PyObject *args)
{
    int lines,idx,error;

    SpecFile *sf;

    scandataobject *s = (scandataobject *) self;

    idx = s->index;
    if (idx == -1 ) 
        onError("empty scan data");
    
    sf  = (s->file)->sf;

    lines = SfNoDataLines(sf,idx,&error);

    /*if (lines == -1){*/
    if (lines < 0){
        onError("cannot get lines for scan");
        lines=0;
    }

    return Py_BuildValue("l",lines);
}

static PyObject   * 
scandata_fileheader     (PyObject *self,PyObject *args)
{
    int i,no_lines,idx,error;
    char **lines;
    char *searchstr;
    PyObject *t,*x;

    SpecFile *sf;

    scandataobject *s = (scandataobject *) self;

    if (!PyArg_ParseTuple(args,"s",&searchstr)) 
      return NULL;

    idx = s->index;
    if (idx == -1 ) 
        onError("empty scan data");
    
    sf  = (s->file)->sf;

    no_lines = SfFileHeader(sf,idx,searchstr,&lines,&error);

    if (no_lines == -1)
        onError("cannot get lines for scan");

    t = PyList_New(no_lines);
    for ( i = 0 ;i<no_lines;i++) {
       x = PyString_FromString(lines[i]);
       PyList_SetItem(t,i,x);
    }

    return t;

    return Py_BuildValue("l",no_lines);
}

static PyObject   * 
scandata_header     (PyObject *self,PyObject *args)
{
    int i,no_lines,idx,error;
    char **lines;
    char *searchstr;
    PyObject *t,*x;

    SpecFile *sf;

    scandataobject *s = (scandataobject *) self;

    if (!PyArg_ParseTuple(args,"s",&searchstr)) 
      return NULL;

    idx = s->index;
    if (idx == -1 ) 
        onError("empty scan data");
    
    sf  = (s->file)->sf;

    no_lines = SfHeader(sf,idx,searchstr,&lines,&error);

    if (no_lines == -1)
        onError("cannot get lines for scan");

    t = PyList_New(no_lines);
    for ( i = 0 ;i<no_lines;i++) {
       x = PyString_FromString(lines[i]);
       PyList_SetItem(t,i,x);
    }

    return t;

    return Py_BuildValue("l",no_lines);
}

static PyObject   * 
scandata_nbmca      (PyObject *self,PyObject *args)
{
    int nomca,idx,error;

    PyObject *pyo;
    SpecFile *sf;

    scandataobject *s = (scandataobject *) self;

    idx = s->index;
    if (idx == -1 ) {
        onError("empty scan data");
    }
    sf  = (s->file)->sf;

    nomca = SfNoMca(sf,idx,&error);

    if (nomca == -1) 
        onError("cannot get number of mca for scan");

    pyo =  Py_BuildValue("l",nomca);
    return pyo;
}

static PyObject   * 
scandata_mca      (PyObject *self,PyObject *args)
{
    int    ret,error;
    long   idx,mcano;

    double         *mcadata = NULL;
    PyArrayObject  *array;

    SpecFile *sf;

    scandataobject *s = (scandataobject *) self;

    if (!PyArg_ParseTuple(args,"l",&mcano)) 
            onError("cannot decode arguments for line data"); 
    
    idx = s->index;

    if (idx == -1 ) {
        onError("empty scan data");
    }

    sf  = (s->file)->sf;

    ret = SfGetMca(sf,idx,mcano,&mcadata,&error);

    if (ret == -1) 
        onError("cannot get mca for scan");

    array = (PyArrayObject *)PyArray_FromDims(1,&ret,PyArray_DOUBLE);


    if (mcadata != (double *) NULL){
        memcpy(array->data,mcadata,PyArray_NBYTES(array));
        free(mcadata);
    }else{
        printf("I should give back an empty array\n");
    }
 
/*    return (PyObject *)array; */
    
    return PyArray_Return(array);
    /*
      it does not work for solaris and linux
      I should check the call to PyErr_Occurred()) in Numeric/Src/arrayobject.c
      PyArray_Return(array); 
     */
}

static PyObject   * 
scandata_show      (PyObject *self,PyObject *args)
{
    int idx;

    SpecFile *sf;

    scandataobject *s = (scandataobject *) self;

    idx = s->index;

    if (idx == -1 ) 
        onError("empty scan data");
    
    sf  = (s->file)->sf;

    SfShowScan(sf,idx);

    return Py_BuildValue("l",0);
}


   /*
    * Scandata basic python operations
    */
static PyObject *
scandata_new(void) {      /* on x = specfile.Scandata() */
    scandataobject *self;

    self = PyObject_NEW(scandataobject,&Scandatatype);

    if (self == NULL)
        return NULL;

    self->file  = NULL;
    self->index = -1;
    self->cols  = 0;

    return (PyObject *)self;
}

static PyObject *
scandata_free(PyObject *self) {
    scandataobject *s =(scandataobject *)self; 
    specfileobject *f = s->file; 
    Py_DECREF((PyObject *)f);
    PyObject_DEL(self);

    return NULL;
}

static int
scandata_size(PyObject *self) {

    scandataobject *s = (scandataobject *) self;
  
    return s->cols;
}

static PyObject *
scandata_col(PyObject *self,int index) {
    int     error;
    int     ret;
    double  *data;

    PyArrayObject *array;

    SpecFile *sf;
    int      idx,col;

    scandataobject *s = (scandataobject *) self;
    

    if ( index < 0 || index > (s->cols - 1) ) {
         PyErr_SetString(PyExc_IndexError,"column out of bounds");
         return NULL;
    }

    sf  = (s->file)->sf;
    idx = s->index;
    col = index + 1;

    ret = SfDataCol(sf,idx,col,&data,&error);

    if (ret == -1 )
          onError("cannot get data for column");

    array = (PyArrayObject *)PyArray_FromDims(1,&ret,PyArray_DOUBLE);

    if ( array == NULL ) 
          onError("cannot get memory for array data");

    if (data != (double *) NULL){
        memcpy(array->data,data,PyArray_NBYTES(array));
        free(data);
    }else{
        /* return an empty array? */
        printf("I should return an empty array ...\n");
        ;
    }

/*    return (PyObject *)array; */
/* put back the PyArray_Return call instead of the previous line */
    return PyArray_Return(array);

    /*
      it does not work for solaris and linux
      I should check the call to PyErr_Occurred()) in Numeric/Src/arrayobject.c
      PyArray_Return(array); 
     */
}

static PyObject *
scandata_slice(PyObject *self,int ilow,int ihigh) {
    return NULL;
}

static int
scandata_print(PyObject *self,FILE *fp,int flags) {
    int ok=0;
    SpecFile *sf;
    int idx;

    scandataobject *s = (scandataobject *) self;

    idx = s->index;
    if (idx == -1 ) {
        fprintf(fp,"scandata('empty')");
    } else {
        sf  = (s->file)->sf;
        fprintf(fp,"scandata('source: %s,scan: %d.%d')",
                                    (s->file)->name,
                                    (int) SfNumber(sf,idx), 
                                    (int) SfOrder (sf,idx)); 
    }
    return ok;
}

static PyObject *
scandata_getattr(PyObject *self,char *name) {

   scandataobject *s = (scandataobject *)self;

   if (strcmp(name,"file") == 0) {
        return (PyObject *) s->file;
   }

   if (strcmp(name,"index") == 0) {
        return Py_BuildValue("l",s->index);
   }

   return Py_FindMethod(scandata_methods,self,name);
}


/*
 * Type descriptors
 */
static PySequenceMethods scandata_as_sequence = {
  (inquiry)        scandata_size,       /*     length len(sf)     */
  (binaryfunc)          0,              /*     concat sf1 + sf2   */
  (intargfunc)          0,              /*     repeat sf * n      */
  (intargfunc)     scandata_col,        /*     item  sf[i], in    */
  (intintargfunc)  scandata_slice,      /*     slice sf[i:j]      */
  (intobjargproc)       0,              /*     asset sf[i] = v    */
  (intintobjargproc)    0,              /* slice ass. sf[i:j] = v */
};

static PyTypeObject Scandatatype = {
    /* type header */   
#ifdef WIN32
       PyObject_HEAD_INIT(NULL)
#else
       PyObject_HEAD_INIT(&PyType_Type)
#endif       
       0,
       "scandata",
       sizeof(scandataobject),
       0,

    /* standard methods */
       (destructor)   scandata_free,     /*  tp-dealloc   ref-count = 0  */
       (printfunc)    scandata_print,    /*  tp-print     print sf       */
       (getattrfunc)  scandata_getattr,  /*  tp-getattr   sf.attr        */
       (setattrfunc)  0,                 /*  tp-setattr   sf.attr = v    */
       (cmpfunc)      0,                 /*  tp-setattr   sf1 > sf2      */
       (reprfunc)     0,                 /*  tp-repr      'sf', print sf */

    /* type categories */
       0,                                /* tp as number   +,-,....      */
       &scandata_as_sequence,            /* tp as sequence +,[i],[i:j]...*/
       0,                                /* tp as mapping [key], len, ...*/

    /* more methods */
       (hashfunc)     0,                 /* tp_hash  dict(sf) */
      /* (binaryfunc)   0,                 tp_call  sf()     */
      /* (reprfunc)     0,                 tp_str   str(x)   */
};

/* end scandata */


/*
 * Class creators
 */
static struct PyMethodDef specfiletype_methods[] = {
   {"Specfile",  specfiletype_new,  1},
   {"Scandata",  scandatatype_new,  1},
   { NULL, NULL}
};


static PyObject *
specfiletype_new(self,args)
  PyObject *self;
  PyObject *args;
{
   PyObject *ret;
   char *filename;

   if (!PyArg_ParseTuple(args,"s",&filename)) 
      return NULL;
   ret = (PyObject *)specfile_open(filename);

   return ret;
 
}

static PyObject *
scandatatype_new(self,args)
  PyObject *self;
  PyObject *args;
{
   PyObject *ret;

   if (!PyArg_ParseTuple(args,"")) 
      return NULL;
   ret = (PyObject *)scandata_new();
   return ret;
 
}

/*
 * Module init
 */
DL_EXPORT(void)
initspecfile(void) {
    PyObject *m,*d;

	Specfiletype.ob_type = &PyType_Type;
    Scandatatype.ob_type = &PyType_Type;
    m = Py_InitModule("specfile",specfiletype_methods);
	
/*    printf("Loading test specfile module\n");*/

    import_array();

    d = PyModule_GetDict(m);
    ErrorObject = Py_BuildValue("s","specfile.error");
    PyDict_SetItemString(d,"error",ErrorObject);

    if (PyErr_Occurred())
        Py_FatalError("can't initialize module specfile");
}



/*
 * Utility functions
 */
static char *
compList(long *nolist,long howmany)
{
     long this,colon;
     char buf[30];
     static char str[5000];
     char *retstr;

     if (howmany < 1) { return((char *)NULL);}

     sprintf(buf,"%d",(int) nolist[0]);

     *str = '\0';

     strcat(str,buf); 

     colon=0;
     for(this=1;this<howmany;this++) {
         if ((nolist[this] - nolist[this-1]) == 1) {
            colon = 1;
         } else {
            if (colon) {
               sprintf(buf,":%d,%d",(int) nolist[this-1],(int) nolist[this]);
               colon=0;
            } else {
               sprintf(buf,",%d",(int) nolist[this]);
            }
            strcat(str,buf); 
         }
     }

     if (howmany != 1 ) {
        if (colon) {
           sprintf(buf,":%d",(int) nolist[howmany-1]);
           strcat(str,buf); 
        }
     }
     retstr = (char *)strdup(str);
     return(retstr);
}
